#!/usr/bin/env python3
"""Validate governed Mermaid diagrams in registered Markdown and tracked HTML."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[6]
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

try:
    from strict_yaml import StrictYamlError, load_frontmatter
except ImportError:  # pragma: no cover - alternate import path under tests
    from scripts.research_control.strict_yaml import StrictYamlError, load_frontmatter


ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
MARKER_RE = re.compile(r"^<!--\s*mermaid-diagram-id:\s*([^>]+?)\s*-->$")
MERMAID_FENCE_RE = re.compile(r"^\s*```\s*mermaid\s*$")
FENCE_CLOSE_RE = re.compile(r"^\s*```\s*$")
AUTHORITY_RE = re.compile(r"<!--\s*authority:\s*(explanatory|control)\s*-->")
HTML_ATTR_RE = r"""{name}\s*=\s*(?:"([^"]*)"|'([^']*)')"""
SCRIPT_RE = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.I | re.S)
SECTION_RE = re.compile(r"<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>", re.I | re.S)
BARE_PRE_RE = re.compile(
    r"<pre\b[^>]*class\s*=\s*(?:\"[^\"]*\bmermaid\b[^\"]*\"|'[^']*\bmermaid\b[^']*')",
    re.I,
)
REMOTE_MERMAID_RE = re.compile(
    r"(?:import\s+mermaid\s+from\s*[\"']https?://|src\s*=\s*[\"']https?://[^\"']*mermaid)",
    re.I,
)
MERMAID_RUNTIME_RE = re.compile(
    r"(?:import\s+mermaid|mermaid\.render\s*\(|mermaid\.initialize\s*\(|mermaid\.esm|(?:\./|html/)?assets/(?:mermaid|chunks/mermaid))",
    re.I,
)
ELK_LAYOUT_RE = re.compile(r"layout\s*:\s*[\"']elk[\"']")
MERMAID_INDICATOR_RE = re.compile(
    r"(diagram-source|mermaid\.esm|class\s*=\s*[\"'][^\"']*\bmermaid\b|<pre\b[^>]*\bmermaid\b)",
    re.I,
)
SVG_RE = re.compile(r"<svg\b(?P<attrs>[^>]*)>.*?</svg>", re.I | re.S)
CANVAS_RE = re.compile(
    r"<div\b(?P<attrs>[^>]*class\s*=\s*(?:\"[^\"]*\bmermaid-canvas\b[^\"]*\"|'[^']*\bmermaid-canvas\b[^']*')[^>]*)>(?P<body>.*?)</div>",
    re.I | re.S,
)
ZOOM_LABEL_RE = re.compile(
    r"<(?:span|div)\b(?P<attrs>[^>]*class\s*=\s*(?:\"[^\"]*\bzoom-label\b[^\"]*\"|'[^']*\bzoom-label\b[^']*')[^>]*)>(?P<body>.*?)</(?:span|div)>",
    re.I | re.S,
)
STALE_ZOOM_LABELS = {"Loading", "Render failed", "Local server required"}
RENDERER_PREFIX = "mermaid@11.15.0;mermaid-inline-svg-renderer@"
FIRST_LINE_RE = re.compile(
    r"^(flowchart|graph|sequenceDiagram|stateDiagram-v2|stateDiagram|"
    r"classDiagram-v2|classDiagram|erDiagram|gantt|timeline|gitGraph|"
    r"mindmap|journey|pie|quadrantChart|requirementDiagram)\b"
)

MIXED_MARKDOWN_PATHS = {
    "README.md",
    "AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
}
AGENT_GUIDANCE_MERMAID_BLOCKED = {"AGENTS.md", "research_control/AGENTS.md"}


@dataclass
class MermaidBlock:
    path: str
    start_line: int
    source: str
    diagram_id: str = ""


@dataclass
class HtmlDiagramSource:
    path: str
    diagram_id: str
    source: str
    attrs: str
    body: str


@dataclass
class MermaidValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    render_skipped: bool = False

    def ok(self) -> bool:
        return not self.errors


def rel_path(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def read_csv_rows(repo_root: Path, registry_name: str) -> list[dict[str, str]]:
    path = repo_root / "registries" / registry_name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def attr_value(attrs: str, name: str) -> str:
    match = re.search(HTML_ATTR_RE.format(name=re.escape(name)), attrs, re.I)
    if not match:
        return ""
    return match.group(1) if match.group(1) is not None else match.group(2)


def class_has(attrs: str, class_name: str) -> bool:
    classes = attr_value(attrs, "class").split()
    return class_name in classes


def html_has_class(fragment: str, class_name: str) -> bool:
    class_re = re.compile(
        r"class\s*=\s*(?:\"[^\"]*\b"
        + re.escape(class_name)
        + r"\b[^\"]*\"|'[^']*\b"
        + re.escape(class_name)
        + r"\b[^']*')",
        re.I,
    )
    return bool(class_re.search(fragment))


def normalize_mermaid_source(source: str) -> str:
    lines = textwrap.dedent(source).splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(line.rstrip() for line in lines)


def mermaid_source_hash(source: str) -> str:
    return hashlib.sha256(normalize_mermaid_source(source).encode("utf-8")).hexdigest()


def normalized_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(text).strip()


def first_semantic_line(source: str) -> str:
    for line in normalize_mermaid_source(source).splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("%%"):
            return stripped
    return ""


def validate_diagram_id(result: MermaidValidationResult, path: str, line: int, diagram_id: str) -> None:
    if not ID_RE.fullmatch(diagram_id):
        result.errors.append(f"{path}:{line}: invalid Mermaid diagram ID {diagram_id!r}")


def validate_mermaid_structure(
    result: MermaidValidationResult, path: str, line: int, source: str
) -> None:
    normalized = normalize_mermaid_source(source)
    if not normalized:
        result.errors.append(f"{path}:{line}: Mermaid source is empty")
        return
    first = first_semantic_line(normalized)
    if not FIRST_LINE_RE.match(first):
        result.errors.append(
            f"{path}:{line}: first Mermaid line has unsupported diagram type: {first!r}"
        )


def extract_markdown_mermaid_blocks(
    path: Path, repo_root: Path, result: MermaidValidationResult
) -> list[MermaidBlock]:
    relative = rel_path(path, repo_root)
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[MermaidBlock] = []
    index = 0
    while index < len(lines):
        if not MERMAID_FENCE_RE.match(lines[index]):
            index += 1
            continue
        start_line = index + 1
        diagram_id = ""
        if index > 0:
            marker = MARKER_RE.match(lines[index - 1].strip())
            if marker:
                diagram_id = marker.group(1).strip()
        body: list[str] = []
        index += 1
        while index < len(lines) and not FENCE_CLOSE_RE.match(lines[index]):
            body.append(lines[index])
            index += 1
        if index >= len(lines):
            result.errors.append(f"{relative}:{start_line}: unclosed Mermaid fence")
            break
        blocks.append(
            MermaidBlock(
                path=relative,
                start_line=start_line,
                source="\n".join(body),
                diagram_id=diagram_id,
            )
        )
        index += 1
    return blocks


def authority_by_line(path: Path, line_number: int) -> str:
    active = ""
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        marker = AUTHORITY_RE.search(line)
        if marker:
            active = marker.group(1)
        if index >= line_number:
            break
    return active or "unmarked"


def duplicate_ids(blocks: Iterable[MermaidBlock]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for block in blocks:
        if not block.diagram_id:
            continue
        if block.diagram_id in seen:
            duplicates.add(block.diagram_id)
        seen.add(block.diagram_id)
    return duplicates


def parse_mermaid_diagrams_contract(
    frontmatter: dict[str, object], path: str, result: MermaidValidationResult
) -> tuple[bool, list[str], bool]:
    if "mermaid_diagrams" not in frontmatter:
        return False, [], False
    value = frontmatter.get("mermaid_diagrams")
    if not isinstance(value, dict):
        result.errors.append(f"{path}: mermaid_diagrams must be a map")
        return False, [], True
    required = value.get("required", False)
    ids = value.get("ids", [])
    if not isinstance(required, bool):
        result.errors.append(f"{path}: mermaid_diagrams.required must be true or false")
        required = False
    if not isinstance(ids, list):
        result.errors.append(f"{path}: mermaid_diagrams.ids must be a list")
        ids = []
    ids_text = [str(item).strip() for item in ids if str(item).strip()]
    if required and not ids_text:
        result.errors.append(f"{path}: mermaid_diagrams.required true requires non-empty ids")
    for diagram_id in ids_text:
        if not ID_RE.fullmatch(diagram_id):
            result.errors.append(f"{path}: invalid mermaid_diagrams ID {diagram_id!r}")
    if len(ids_text) != len(set(ids_text)):
        result.errors.append(f"{path}: mermaid_diagrams.ids contains duplicates")
    return bool(required), ids_text, True


def validate_html_spec_markdown(
    row: dict[str, str],
    repo_root: Path,
    result: MermaidValidationResult,
) -> tuple[list[str], dict[str, MermaidBlock]]:
    path_text = row.get("path", "")
    path = repo_root / path_text
    if not path.exists():
        return [], {}
    try:
        frontmatter, _body = load_frontmatter(path)
    except StrictYamlError as exc:
        result.errors.append(f"{path_text}: invalid frontmatter for Mermaid validation: {exc}")
        return [], {}
    _required, declared_ids, has_contract = parse_mermaid_diagrams_contract(
        frontmatter, path_text, result
    )
    blocks = extract_markdown_mermaid_blocks(path, repo_root, result)
    for block in blocks:
        if not block.diagram_id:
            result.errors.append(
                f"{block.path}:{block.start_line}: HTML explainer Mermaid fence missing mermaid-diagram-id marker"
            )
            continue
        validate_diagram_id(result, block.path, block.start_line, block.diagram_id)
        validate_mermaid_structure(result, block.path, block.start_line, block.source)

    for diagram_id in sorted(duplicate_ids(blocks)):
        result.errors.append(f"{path_text}: duplicate Mermaid diagram ID {diagram_id}")

    marked_ids = [block.diagram_id for block in blocks if block.diagram_id]
    if marked_ids and not has_contract:
        result.errors.append(f"{path_text}: Mermaid diagrams require mermaid_diagrams frontmatter")
    if has_contract:
        declared_set = set(declared_ids)
        marked_set = set(marked_ids)
        for missing in sorted(declared_set - marked_set):
            result.errors.append(f"{path_text}: declared Mermaid ID missing from Markdown: {missing}")
        for extra in sorted(marked_set - declared_set):
            result.errors.append(f"{path_text}: Markdown Mermaid ID not declared: {extra}")
    return declared_ids, {block.diagram_id: block for block in blocks if block.diagram_id}


def validate_ordinary_markdown(
    row: dict[str, str], repo_root: Path, result: MermaidValidationResult
) -> None:
    path_text = row.get("path", "")
    path = repo_root / path_text
    if not path.exists() or row.get("role") == "html_explainer_source_spec":
        return
    blocks = extract_markdown_mermaid_blocks(path, repo_root, result)
    if not blocks:
        return
    for block in blocks:
        if not block.diagram_id:
            if row.get("authority_status") in {"canonical_markdown_source", "explanatory_noncanonical"}:
                result.warnings.append(
                    f"{block.path}:{block.start_line}: untracked Mermaid block has no mermaid-diagram-id"
                )
            continue
        validate_diagram_id(result, block.path, block.start_line, block.diagram_id)
        validate_mermaid_structure(result, block.path, block.start_line, block.source)
        if path_text in AGENT_GUIDANCE_MERMAID_BLOCKED:
            result.errors.append(
                f"{block.path}:{block.start_line}: governed Mermaid blocks are not allowed in AGENTS guidance"
            )
        elif path_text in {"README.md", "research_control/README.md"}:
            authority = authority_by_line(path, block.start_line)
            if authority != "explanatory":
                result.errors.append(
                    f"{block.path}:{block.start_line}: governed Mermaid block is outside an explanatory authority section"
                )
        elif path_text.startswith(".agents/roles/") or path_text.startswith(".agents/schemas/"):
            result.errors.append(
                f"{block.path}:{block.start_line}: governed Mermaid blocks are not allowed in role or schema contracts"
            )
    for diagram_id in sorted(duplicate_ids(blocks)):
        result.errors.append(f"{path_text}: duplicate Mermaid diagram ID {diagram_id}")


def extract_html_diagram_sources(
    html_path: Path, repo_root: Path, result: MermaidValidationResult
) -> dict[str, HtmlDiagramSource]:
    relative = rel_path(html_path, repo_root)
    text = html_path.read_text(encoding="utf-8")
    sources: dict[str, HtmlDiagramSource] = {}
    seen: set[str] = set()
    for match in SCRIPT_RE.finditer(text):
        attrs = match.group("attrs")
        if not class_has(attrs, "diagram-source"):
            continue
        diagram_id = attr_value(attrs, "data-mermaid-diagram-id").strip()
        if not diagram_id:
            result.errors.append(f"{relative}: diagram-source missing data-mermaid-diagram-id")
            continue
        if diagram_id in seen:
            result.errors.append(f"{relative}: duplicate HTML Mermaid diagram source {diagram_id}")
        seen.add(diagram_id)
        if attr_value(attrs, "type") != "text/plain":
            result.errors.append(f"{relative}: diagram-source {diagram_id} must use type=\"text/plain\"")
        sources[diagram_id] = HtmlDiagramSource(
            path=relative,
            diagram_id=diagram_id,
            source=html.unescape(match.group("body")),
            attrs=attrs,
            body=text,
        )
    return sources


def shell_fragments_for_id(html_text: str, diagram_id: str) -> list[str]:
    shells: list[str] = []
    for match in SECTION_RE.finditer(html_text):
        attrs = match.group("attrs")
        if class_has(attrs, "diagram-shell") and attr_value(attrs, "data-mermaid-diagram-id") == diagram_id:
            shells.append(match.group(0))
    return shells


def shell_fragment_for_id(html_text: str, diagram_id: str) -> str:
    shells = shell_fragments_for_id(html_text, diagram_id)
    return shells[0] if shells else ""


def validate_inline_svg_artifact(
    result: MermaidValidationResult,
    relative: str,
    diagram_id: str,
    shell: str,
    source: str,
) -> None:
    canvas_matches = list(CANVAS_RE.finditer(shell))
    if len(canvas_matches) != 1:
        result.errors.append(f"{relative}: Mermaid ID {diagram_id} must have exactly one .mermaid-canvas")
        return
    canvas_attrs = canvas_matches[0].group("attrs")
    canvas_body = canvas_matches[0].group("body")
    expected_hash = mermaid_source_hash(source)
    actual_hash = attr_value(canvas_attrs, "data-render-source-sha256")
    if actual_hash != expected_hash:
        result.errors.append(
            f"{relative}: Mermaid ID {diagram_id} data-render-source-sha256 does not match preserved source"
        )
    renderer = attr_value(canvas_attrs, "data-renderer")
    if not renderer.startswith(RENDERER_PREFIX):
        result.errors.append(f"{relative}: Mermaid ID {diagram_id} missing deterministic data-renderer")
    svg_matches = list(SVG_RE.finditer(canvas_body))
    if len(svg_matches) != 1:
        result.errors.append(f"{relative}: Mermaid ID {diagram_id} must embed exactly one inline SVG")
        return
    svg_attrs = svg_matches[0].group("attrs")
    if attr_value(svg_attrs, "data-mermaid-rendered") != "true":
        result.errors.append(f"{relative}: Mermaid ID {diagram_id} inline SVG missing data-mermaid-rendered")
    if attr_value(svg_attrs, "data-mermaid-diagram-id") != diagram_id:
        result.errors.append(f"{relative}: Mermaid ID {diagram_id} inline SVG diagram ID mismatch")
    for label_match in ZOOM_LABEL_RE.finditer(shell):
        label = normalized_text(label_match.group("body"))
        if label in STALE_ZOOM_LABELS:
            result.errors.append(f"{relative}: Mermaid ID {diagram_id} has stale zoom label {label!r}")


def validate_html_shell(
    result: MermaidValidationResult,
    html_path: Path,
    repo_root: Path,
    diagram_id: str,
    source: str,
) -> None:
    relative = rel_path(html_path, repo_root)
    html_text = html_path.read_text(encoding="utf-8")
    shells = shell_fragments_for_id(html_text, diagram_id)
    if not shells:
        result.errors.append(f"{relative}: missing diagram-shell for Mermaid ID {diagram_id}")
        return
    if len(shells) > 1:
        result.errors.append(f"{relative}: duplicate diagram-shell for Mermaid ID {diagram_id}")
        return
    shell = shells[0]
    for class_name in [
        "mermaid-wrap",
        "zoom-controls",
        "mermaid-viewport",
        "mermaid-canvas",
        "diagram-source",
    ]:
        if not html_has_class(shell, class_name):
            result.errors.append(f"{relative}: Mermaid ID {diagram_id} missing .{class_name}")
    validate_inline_svg_artifact(result, relative, diagram_id, shell, source)


def validate_html_runtime_policy(
    result: MermaidValidationResult, html_path: Path, repo_root: Path
) -> None:
    relative = rel_path(html_path, repo_root)
    text = html_path.read_text(encoding="utf-8")
    if BARE_PRE_RE.search(text):
        result.errors.append(f"{relative}: tracked HTML must not use bare <pre class=\"mermaid\">")
    if REMOTE_MERMAID_RE.search(text):
        result.errors.append(f"{relative}: tracked HTML must not import Mermaid from a remote URL")
    if MERMAID_RUNTIME_RE.search(text):
        result.errors.append(f"{relative}: governed Mermaid HTML must not execute or import Mermaid in the browser")
    if ELK_LAYOUT_RE.search(text):
        result.errors.append(f"{relative}: tracked HTML must not use layout \"elk\" without a local ELK runtime")


def validate_html_parity(
    html_row: dict[str, str],
    markdown_rows_by_id: dict[str, dict[str, str]],
    spec_blocks_by_id: dict[str, MermaidBlock],
    declared_ids: list[str],
    repo_root: Path,
    result: MermaidValidationResult,
) -> None:
    html_path = repo_root / html_row.get("path", "")
    if not html_path.exists():
        return
    html_text = html_path.read_text(encoding="utf-8")
    sources = extract_html_diagram_sources(html_path, repo_root, result)
    has_mermaid_indicator = bool(MERMAID_INDICATOR_RE.search(html_text))
    declared_set = set(declared_ids)
    html_set = set(sources)

    if not declared_set and has_mermaid_indicator:
        result.errors.append(
            f"{html_row.get('path', '')}: tracked HTML contains Mermaid markers without declared source parity"
        )
        return
    if not declared_set:
        return

    validate_html_runtime_policy(result, html_path, repo_root)
    for missing in sorted(declared_set - html_set):
        result.errors.append(f"{html_row.get('path', '')}: declared Mermaid ID missing from HTML: {missing}")
    for extra in sorted(html_set - declared_set):
        result.errors.append(f"{html_row.get('path', '')}: HTML Mermaid ID not declared in source spec: {extra}")
    source_basis = html_row.get("source_basis", "")
    if source_basis not in markdown_rows_by_id:
        result.errors.append(f"{html_row.get('path', '')}: missing registered Mermaid source basis")
        return
    for diagram_id in sorted(declared_set & html_set):
        validate_html_shell(result, html_path, repo_root, diagram_id, sources[diagram_id].source)
        if diagram_id not in spec_blocks_by_id:
            result.errors.append(
                f"{html_row.get('path', '')}: declared Mermaid ID missing from Markdown source for ID {diagram_id}"
            )
            continue
        md_source = normalize_mermaid_source(spec_blocks_by_id[diagram_id].source)
        html_source = normalize_mermaid_source(sources[diagram_id].source)
        if md_source != html_source:
            result.errors.append(
                f"{html_row.get('path', '')}: Mermaid source differs from Markdown for ID {diagram_id}"
            )
        validate_mermaid_structure(result, html_row.get("path", ""), 1, sources[diagram_id].source)


def run_render_check(
    result: MermaidValidationResult, blocks: list[MermaidBlock | HtmlDiagramSource]
) -> None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        result.render_skipped = True
        return
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for index, block in enumerate(blocks, start=1):
            source_path = tmp_path / f"diagram-{index}.mmd"
            output_path = tmp_path / f"diagram-{index}.svg"
            source_path.write_text(normalize_mermaid_source(block.source), encoding="utf-8")
            completed = subprocess.run(
                [mmdc, "-i", str(source_path), "-o", str(output_path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if completed.returncode != 0:
                result.errors.append(
                    f"{block.path}: mmdc render failed for Mermaid ID {block.diagram_id or '<untracked>'}: {completed.stderr.strip()}"
                )


def validate_mermaid_sources(
    repo_root: Path | None = None,
    markdown_rows: list[dict[str, str]] | None = None,
    html_rows: list[dict[str, str]] | None = None,
    *,
    render_check: bool = False,
) -> MermaidValidationResult:
    repo_root = (repo_root or REPO_ROOT).resolve()
    markdown_rows = markdown_rows if markdown_rows is not None else read_csv_rows(repo_root, "MARKDOWN_SOURCE_REGISTRY.csv")
    html_rows = html_rows if html_rows is not None else read_csv_rows(repo_root, "HTML_EXPLAINER_REGISTRY.csv")
    result = MermaidValidationResult()
    markdown_rows_by_id = {row.get("object_id", ""): row for row in markdown_rows}
    spec_declared_by_object_id: dict[str, list[str]] = {}
    spec_blocks_by_object_id: dict[str, dict[str, MermaidBlock]] = {}
    render_blocks: list[MermaidBlock | HtmlDiagramSource] = []

    for row in markdown_rows:
        path_text = row.get("path", "")
        path = repo_root / path_text
        if not path.exists():
            continue
        if row.get("role") == "html_explainer_source_spec":
            declared_ids, blocks_by_id = validate_html_spec_markdown(row, repo_root, result)
            spec_declared_by_object_id[row.get("object_id", "")] = declared_ids
            spec_blocks_by_object_id[row.get("object_id", "")] = blocks_by_id
            render_blocks.extend(blocks_by_id.values())
        else:
            before_count = len(result.errors)
            validate_ordinary_markdown(row, repo_root, result)
            if len(result.errors) == before_count:
                blocks = extract_markdown_mermaid_blocks(path, repo_root, MermaidValidationResult())
                render_blocks.extend(block for block in blocks if block.diagram_id)

    html_rows_by_path = {row.get("path", ""): row for row in html_rows}
    for html_path in sorted((repo_root / "html").glob("*.html")):
        path_text = rel_path(html_path, repo_root)
        row = html_rows_by_path.get(path_text)
        if not row:
            continue
        source_basis = row.get("source_basis", "")
        declared_ids = spec_declared_by_object_id.get(source_basis, [])
        blocks_by_id = spec_blocks_by_object_id.get(source_basis, {})
        validate_html_parity(
            row,
            markdown_rows_by_id,
            blocks_by_id,
            declared_ids,
            repo_root,
            result,
        )
        if declared_ids:
            render_blocks.extend(extract_html_diagram_sources(html_path, repo_root, result).values())
        elif MERMAID_INDICATOR_RE.search(html_path.read_text(encoding="utf-8")):
            if BARE_PRE_RE.search(html_path.read_text(encoding="utf-8")):
                result.errors.append(f"{path_text}: tracked HTML must not use bare <pre class=\"mermaid\">")
            if REMOTE_MERMAID_RE.search(html_path.read_text(encoding="utf-8")):
                result.errors.append(f"{path_text}: tracked HTML must not import Mermaid from a remote URL")

    if render_check:
        run_render_check(result, render_blocks)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Repository root to validate.")
    parser.add_argument("--render-check", action="store_true", help="Optionally render diagrams with mmdc when available.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable diagnostics.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = validate_mermaid_sources(Path(args.repo_root), render_check=args.render_check)
    if args.json:
        print(
            json.dumps(
                {
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "render_skipped": result.render_skipped,
                },
                indent=2,
            )
        )
    else:
        if result.errors:
            print("Mermaid validation failed:")
            for error in result.errors:
                print(f"- {error}")
        else:
            print("Mermaid validation passed.")
        for warning in result.warnings:
            print(f"Warning: {warning}")
        if result.render_skipped:
            print("Render check skipped: mmdc is not available.")
    return 0 if result.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
