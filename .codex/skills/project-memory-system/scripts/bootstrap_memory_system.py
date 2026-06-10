#!/usr/bin/env python3
"""Bootstrap and validate the repository memory, registry, and wiki system."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from obsidian_wiki_lib import (  # noqa: E402
    GENERATED_REGISTRY_COLUMNS as OBSIDIAN_GENERATED_REGISTRY_COLUMNS,
    write_generated_registries,
)
from strict_yaml import StrictYamlError, load_frontmatter  # noqa: E402

COMMON_COLUMNS = [
    "object_id",
    "path",
    "format",
    "role",
    "authority_status",
    "audience",
    "source_hash",
    "related_source",
    "generated_from",
    "generated_outputs",
    "owner_skill",
    "validation_status",
    "last_validated_at",
    "notes",
]

TEX_COLUMNS = COMMON_COLUMNS + [
    "pdf_required",
    "pdf_object_id",
    "pdf_path",
    "claim_status",
    "research_status",
    "ontology_promotion_status",
    "equation_scope",
]
PDF_COLUMNS = COMMON_COLUMNS + [
    "source_tex_object_id",
    "source_tex_path",
    "source_tex_hash",
    "pdf_hash",
    "build_command",
    "build_status",
    "built_at",
]
MARKDOWN_COLUMNS = COMMON_COLUMNS + [
    "github_facing",
    "agent_documentation",
    "contains_mermaid",
    "contains_math",
]
HTML_COLUMNS = COMMON_COLUMNS + [
    "human_visual_only",
    "source_basis",
    "source_basis_hash",
    "html_hash",
    "visual_explainer_skill_version",
]
WIKI_COLUMNS = COMMON_COLUMNS + [
    "source_object_id",
    "source_path",
    "source_object_hash",
    "wiki_hash",
    "wiki_kind",
    "generated_at",
]
FILE_OBJECT_COLUMNS = COMMON_COLUMNS + ["source_registry"]

MECHANICAL_REFRESH_COLUMNS = {
    "path",
    "format",
    "source_hash",
    "generated_outputs",
    "validation_status",
    "last_validated_at",
    "pdf_object_id",
    "pdf_path",
    "github_facing",
    "agent_documentation",
    "contains_mermaid",
    "contains_math",
}

REGISTRIES = {
    "MARKDOWN_SOURCE_REGISTRY.csv": MARKDOWN_COLUMNS,
    "TEX_SOURCE_REGISTRY.csv": TEX_COLUMNS,
    "PDF_DERIVATIVE_REGISTRY.csv": PDF_COLUMNS,
    "HTML_EXPLAINER_REGISTRY.csv": HTML_COLUMNS,
    "WIKI_ARTIFACT_REGISTRY.csv": WIKI_COLUMNS,
    "FILE_OBJECT_REGISTRY.csv": FILE_OBJECT_COLUMNS,
}
REGISTRIES.update(OBSIDIAN_GENERATED_REGISTRY_COLUMNS)

SOURCE_REGISTRY_NAMES = [
    "MARKDOWN_SOURCE_REGISTRY.csv",
    "TEX_SOURCE_REGISTRY.csv",
    "PDF_DERIVATIVE_REGISTRY.csv",
    "HTML_EXPLAINER_REGISTRY.csv",
]
GENERATED_REGISTRY_NAMES = [
    "WIKI_ARTIFACT_REGISTRY.csv",
    "OBSIDIAN_VAULT_REGISTRY.csv",
    "CONTENT_SEMANTIC_REGISTRY.csv",
    "OBJECT_RELATIONSHIP_REGISTRY.csv",
    "FILE_OBJECT_REGISTRY.csv",
]

FOLDER_MAP_PATH = REPO_ROOT / "FOLDER_MAP.md"
FOLDER_MAP_CATEGORIES = {
    "canonical source",
    "control authority",
    "generated derivative",
    "local retrieval",
    "tooling",
    "reserved lane",
}
FOLDER_WALK_SKIP_NAMES = {".git", ".venv", "__pycache__"}
FOLDER_MAP_EXCLUDED_FILES = {"FOLDER_MAP.md"}

REQUIRED_DIRS = [
    "ontology/tex",
    "ontology/pdfs",
    "manuscripts/tex",
    "manuscripts/pdfs",
    "markdown",
    "markdown/html-explainer-specs",
    "markdown/ontology-promotions",
    "tex_shared",
    "html",
    "registries",
    "wiki/markdown",
    "wiki/tex",
    "wiki/pdf",
    "wiki/html",
    "wiki/indexes",
]

PROJECT_MARKDOWN_FILES = [
    ".agents/AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
    "research_control/approvals/README.md",
]
PROJECT_MARKDOWN_GLOBS = [
    ".agents/roles/**/*.md",
    ".agents/schemas/*.md",
    ".codex/skills/*/SKILL.md",
    "research_control/design/*.md",
]

CANONICAL_LANES = [
    "ontology",
    "manuscripts",
    "markdown",
    "html",
    "registries",
    "wiki",
]

EQUATION_SCOPE_VALUES = {
    "none",
    "local_equations",
    "derivation_sequence",
    "gr_benchmark",
    "control_only",
}
CLAIM_STATUS_VALUES = {
    "benchmark_claim",
    "open_derivation_claim",
    "proposal",
    "rejected",
    "superseded",
    "control_only",
    "explanatory_only",
}
RESEARCH_STATUS_VALUES = {
    "canonical_ontology",
    "active_manuscript",
    "draft",
    "paused",
    "stopped_negative_result",
    "rejected",
    "superseded",
    "project_control",
}
PROMOTION_STATUS_VALUES = {
    "proposed",
    "accepted",
    "rejected",
    "superseded",
    "not_applicable",
}

PDF_BUILD_COMMAND = (
    "pdflatex -interaction=nonstopmode -halt-on-error <source.tex> (x3)"
)
HTML_SPEC_REQUIRED_FIELDS = {
    "title",
    "purpose",
    "audience",
    "output_path",
    "renderer_skill",
    "source_materials",
    "claim_boundary",
    "human_visual_only",
}
HTML_SOURCE_BASIS_META_RE = re.compile(
    r'<meta\s+name=["\']aether-flow-source-basis["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
HTML_SOURCE_BASIS_HASH_META_RE = re.compile(
    r'<meta\s+name=["\']aether-flow-source-basis-hash["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
HTML_HUMAN_VISUAL_META_RE = re.compile(
    r'<meta\s+name=["\']aether-flow-human-visual-only["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


@dataclass
class ValidationReport:
    """Collect validation errors and warnings."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors

    def print(self) -> None:
        for message in self.errors:
            print(f"ERROR: {message}")
        for message in self.warnings:
            print(f"WARNING: {message}")
        if self.ok:
            print("Validation PASS")
        else:
            print(f"Validation FAIL: {len(self.errors)} error(s)")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def registry_path(name: str) -> Path:
    return REPO_ROOT / "registries" / name


def rel_path(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def object_suffix_from_stem(stem: str) -> str:
    return slugify(stem).upper()


def object_suffix_from_path(path_text: str) -> str:
    return slugify(path_text).upper()


def wiki_lane_for_format(format_value: str) -> str:
    if format_value == "tex":
        return "tex"
    if format_value == "pdf":
        return "pdf"
    if format_value == "html":
        return "html"
    return "markdown"


def wiki_object_id(source_object_id: str) -> str:
    return f"WIKI-{source_object_id}"


def wiki_path_for_source(row: dict[str, str]) -> str:
    lane = wiki_lane_for_format(row.get("format", "markdown"))
    return f"wiki/{lane}/{slugify(row['object_id'])}.md"


def validate_relative_path(path_text: str) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path.is_absolute():
        return "absolute paths are not allowed"
    if any(part == ".." for part in path.parts):
        return "path traversal is not allowed"
    return None


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [{key: value or "" for key, value in row.items()} for row in reader]


def csv_text(fieldnames: list[str], rows: list[dict[str, str]]) -> str:
    handle = io.StringIO()
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fieldnames})
    return handle.getvalue()


def write_text_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def write_csv_if_changed(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> bool:
    return write_text_if_changed(path, csv_text(fieldnames, rows))


def normalize_row(row: dict[str, str], fieldnames: list[str]) -> dict[str, str]:
    return {field: row.get(field, "") or "" for field in fieldnames}


def existing_by_id(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("object_id", ""): row for row in rows if row.get("object_id")}


def merge_authored_registry(
    name: str,
    fieldnames: list[str],
    discovered_rows: list[dict[str, str]],
    refresh_existing: bool,
) -> list[dict[str, str]]:
    path = registry_path(name)
    existing_rows = read_csv_rows(path)
    existing = existing_by_id(existing_rows)
    discovered = existing_by_id(discovered_rows)
    merged: list[dict[str, str]] = []
    all_ids = sorted(set(existing) | set(discovered))
    for object_id in all_ids:
        if object_id in existing and object_id in discovered and not refresh_existing:
            row = normalize_row(existing[object_id], fieldnames)
            discovered_row = normalize_row(discovered[object_id], fieldnames)
            previous_hash = row.get("source_hash", "")
            for field in MECHANICAL_REFRESH_COLUMNS & set(fieldnames):
                row[field] = discovered_row.get(field, "")
            if previous_hash == row.get("source_hash", ""):
                row["last_validated_at"] = existing[object_id].get("last_validated_at", "")
            merged.append(row)
        elif object_id in existing and (object_id not in discovered or not refresh_existing):
            merged.append(normalize_row(existing[object_id], fieldnames))
        else:
            merged.append(normalize_row(discovered[object_id], fieldnames))
    write_csv_if_changed(path, fieldnames, merged)
    return merged


def ensure_directories() -> None:
    for directory in REQUIRED_DIRS:
        (REPO_ROOT / directory).mkdir(parents=True, exist_ok=True)


def markdown_object_id(path: Path) -> str:
    relative = rel_path(path)
    if relative == "README.md":
        return "MD-README"
    if relative == "AGENTS.md":
        return "MD-AGENTS"
    if relative.endswith("/AGENTS.md"):
        return f"MD-AGENTS-{object_suffix_from_path(str(Path(relative).parent))}"
    if relative.endswith("/README.md"):
        return f"MD-README-{object_suffix_from_path(str(Path(relative).parent))}"
    if relative.startswith(".agents/roles/"):
        return f"MD-ROLE-{object_suffix_from_path(relative)}"
    if relative.startswith(".agents/schemas/"):
        return f"MD-SCHEMA-{object_suffix_from_stem(path.stem)}"
    if relative.startswith(".codex/skills/") and path.name == "SKILL.md":
        return f"MD-SKILL-{object_suffix_from_path(Path(relative).parts[2])}"
    if relative.startswith("research_control/design/"):
        return f"MD-RESEARCH-CONTROL-DESIGN-{object_suffix_from_stem(path.stem)}"
    if relative == "ontology/aether-and-aether-flow.md":
        return "MD-ONTOLOGY-AETHER-AND-AETHER-FLOW"
    if relative == "markdown/grill-memory-wiki-registry-design-handoff.md":
        return "MD-PROJECT-CONTROL-GRILL-MEMORY-WIKI-REGISTRY-DESIGN-HANDOFF"
    if relative.startswith("markdown/html-explainer-specs/"):
        return f"MD-HTML-SPEC-{object_suffix_from_stem(path.stem)}"
    if relative.startswith("markdown/ontology-promotions/"):
        return f"MD-ONTOLOGY-PROMOTION-{object_suffix_from_stem(path.stem)}"
    return f"MD-{object_suffix_from_stem(path.stem)}"


def markdown_role(path: Path) -> tuple[str, str, str, str, str]:
    relative = rel_path(path)
    if relative == "README.md":
        return (
            "project_front_door",
            "project_control",
            "humans_and_agents",
            "project-memory-system",
            "Project overview and repository file map.",
        )
    if relative == "AGENTS.md":
        return (
            "agent_guidance",
            "project_control",
            "agents",
            "project-memory-system",
            "Root agent instructions and repository authority hierarchy.",
        )
    if relative == ".agents/AGENTS.md":
        return (
            "scoped_agent_guidance",
            "project_control",
            "agents",
            "project-memory-system",
            "Scoped guidance for role and schema contracts.",
        )
    if relative == "research_control/README.md":
        return (
            "research_control_documentation",
            "project_control",
            "humans_and_agents",
            "project-memory-system",
            "Research-control authority model and validation commands.",
        )
    if relative == "research_control/AGENTS.md":
        return (
            "scoped_agent_guidance",
            "project_control",
            "agents",
            "project-memory-system",
            "Scoped guidance for tracked research-control state.",
        )
    if relative == "research_control/approvals/README.md":
        return (
            "approval_documentation",
            "project_control",
            "humans_and_agents",
            "project-memory-system",
            "Human-gate approval lane documentation.",
        )
    if relative.startswith("research_control/design/"):
        return (
            "research_control_design",
            "project_control",
            "agents",
            "project-memory-system",
            "Authored design note for research-control architecture.",
        )
    if relative.startswith(".agents/roles/"):
        return (
            "role_contract",
            "project_control",
            "agents",
            "project-memory-system",
            "Registered execution role contract.",
        )
    if relative.startswith(".agents/schemas/"):
        return (
            "schema_contract",
            "project_control",
            "agents",
            "project-memory-system",
            "Registered project-control schema contract.",
        )
    if relative.startswith(".codex/skills/") and path.name == "SKILL.md":
        return (
            "skill_contract",
            "project_control",
            "agents",
            Path(relative).parts[2],
            "Repo-local skill contract.",
        )
    if relative == "ontology/aether-and-aether-flow.md":
        return (
            "ontology_adjacent_explanatory_documentation",
            "explanatory_noncanonical",
            "humans_and_agents",
            "markdown-wiki",
            "Ontology-adjacent explanatory documentation; TeX remains scientific authority.",
        )
    if relative == "markdown/grill-memory-wiki-registry-design-handoff.md":
        return (
            "project_control_design_handoff",
            "project_control",
            "agents",
            "project-memory-system",
            "Accepted memory, wiki, registry, and file-format design decisions.",
        )
    if relative.startswith("markdown/html-explainer-specs/"):
        return (
            "html_explainer_source_spec",
            "canonical_markdown_source",
            "humans_and_agents",
            "html-visual-explainer",
            "Canonical source spec for a generated human-only HTML explainer.",
        )
    if relative.startswith("markdown/ontology-promotions/"):
        return (
            "ontology_promotion_note",
            "project_control",
            "humans_and_agents",
            "ontology-promotion",
            "Authored ontology promotion packet note.",
        )
    return (
        "authored_markdown",
        "canonical_markdown_source",
        "humans_and_agents",
        "markdown-wiki",
        "Authored Markdown source.",
    )


def contains_text(path: Path, needle: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "false"
    return "true" if needle in text else "false"


def discover_markdown_rows(now: str) -> list[dict[str, str]]:
    paths: list[Path] = []
    for root_path in [REPO_ROOT / "README.md", REPO_ROOT / "AGENTS.md"]:
        if root_path.exists():
            paths.append(root_path)
    for path_text in PROJECT_MARKDOWN_FILES:
        path = REPO_ROOT / path_text
        if path.exists():
            paths.append(path)
    for pattern in PROJECT_MARKDOWN_GLOBS:
        paths.extend(sorted(REPO_ROOT.glob(pattern)))
    paths.extend(sorted((REPO_ROOT / "ontology").glob("*.md")))
    paths.extend(sorted((REPO_ROOT / "markdown").rglob("*.md")))

    rows = []
    for path in sorted(set(paths)):
        relative = rel_path(path)
        object_id = markdown_object_id(path)
        role, authority, audience, owner_skill, notes = markdown_role(path)
        wiki_path = wiki_path_for_source({"object_id": object_id, "format": "markdown"})
        rows.append(
            {
                "object_id": object_id,
                "path": rel_path(path),
                "format": "markdown",
                "role": role,
                "authority_status": authority,
                "audience": audience,
                "source_hash": sha256_file(path),
                "related_source": "",
                "generated_from": "",
                "generated_outputs": wiki_path,
                "owner_skill": owner_skill,
                "validation_status": "PASS",
                "last_validated_at": now,
                "notes": notes,
                "github_facing": "true" if path.name == "README.md" else "false",
                "agent_documentation": "true"
                if (
                    path.name == "AGENTS.md"
                    or "handoff" in path.name
                    or relative.startswith(".agents/")
                    or relative.startswith(".codex/skills/")
                    or relative.startswith("research_control/")
                )
                else "false",
                "contains_mermaid": contains_text(path, "```mermaid"),
                "contains_math": "true"
                if contains_text(path, "$$") == "true" or contains_text(path, "$") == "true"
                else "false",
            }
        )
    return rows


def tex_object_id(path: Path) -> str:
    relative = rel_path(path)
    lane = "ONTOLOGY" if relative.startswith("ontology/tex/") else "MANUSCRIPT"
    return f"TEX-{lane}-{object_suffix_from_stem(path.stem)}"


def pdf_object_id_for_tex(path: Path) -> str:
    relative = rel_path(path)
    lane = "ONTOLOGY" if relative.startswith("ontology/tex/") else "MANUSCRIPT"
    return f"PDF-{lane}-{object_suffix_from_stem(path.stem)}"


def pdf_path_for_tex_path(path: str | Path) -> str:
    source = Path(path)
    if source.is_absolute():
        relative = source.resolve().relative_to(REPO_ROOT)
    else:
        relative = source
    if relative.parts[:2] == ("ontology", "tex"):
        return f"ontology/pdfs/{relative.stem}.pdf"
    if relative.parts[:2] == ("manuscripts", "tex"):
        return f"manuscripts/pdfs/{relative.stem}.pdf"
    raise ValueError(f"Unsupported TeX lane: {relative.as_posix()}")


def discover_tex_rows(now: str) -> list[dict[str, str]]:
    paths = sorted((REPO_ROOT / "ontology" / "tex").glob("*.tex"))
    paths.extend(sorted((REPO_ROOT / "manuscripts" / "tex").glob("*.tex")))
    rows = []
    for path in paths:
        relative = rel_path(path)
        is_ontology = relative.startswith("ontology/tex/")
        object_id = tex_object_id(path)
        pdf_object_id = pdf_object_id_for_tex(path)
        pdf_path = pdf_path_for_tex_path(relative)
        wiki_path = wiki_path_for_source({"object_id": object_id, "format": "tex"})
        rows.append(
            {
                "object_id": object_id,
                "path": relative,
                "format": "tex",
                "role": "ontology_source" if is_ontology else "manuscript_source",
                "authority_status": "canonical" if is_ontology else "manuscript_source",
                "audience": "humans_and_agents",
                "source_hash": sha256_file(path),
                "related_source": "",
                "generated_from": "",
                "generated_outputs": f"{pdf_path};{wiki_path}",
                "owner_skill": "tex-wiki",
                "validation_status": "PASS",
                "last_validated_at": now,
                "notes": (
                    "Current canonical ontology package; does not prove the broader "
                    "first-principles GR derivation is solved."
                    if is_ontology
                    else "Manuscript source; ontology promotion requires an accepted packet."
                ),
                "pdf_required": "true",
                "pdf_object_id": pdf_object_id,
                "pdf_path": pdf_path,
                "claim_status": "benchmark_claim" if is_ontology else "proposal",
                "research_status": "canonical_ontology" if is_ontology else "active_manuscript",
                "ontology_promotion_status": "accepted" if is_ontology else "not_applicable",
                "equation_scope": "gr_benchmark" if is_ontology else "derivation_sequence",
            }
        )
    return rows


def generate_pdf_rows(
    tex_rows: list[dict[str, str]],
    now: str,
    rebuilt_pdf_paths: Iterable[str] | None = None,
) -> list[dict[str, str]]:
    existing = existing_by_id(read_csv_rows(registry_path("PDF_DERIVATIVE_REGISTRY.csv")))
    rebuilt_paths = set(rebuilt_pdf_paths or [])
    rows = []
    for tex_row in tex_rows:
        if tex_row.get("pdf_required") != "true":
            continue
        pdf_path = tex_row["pdf_path"]
        pdf_abs = REPO_ROOT / pdf_path
        pdf_hash = sha256_file(pdf_abs) if pdf_abs.exists() else ""
        object_id = tex_row["pdf_object_id"]
        existing_row = existing.get(object_id, {})
        built_at = existing_row.get("built_at", "")
        last_validated_at = existing_row.get("last_validated_at", "")
        if (
            existing_row.get("source_tex_hash") != tex_row["source_hash"]
            or existing_row.get("pdf_hash") != pdf_hash
        ):
            built_at = ""
            last_validated_at = now
        if pdf_path in rebuilt_paths and pdf_abs.exists():
            built_at = now
            last_validated_at = now
        if not last_validated_at:
            last_validated_at = now
        wiki_path = wiki_path_for_source({"object_id": object_id, "format": "pdf"})
        rows.append(
            {
                "object_id": object_id,
                "path": pdf_path,
                "format": "pdf",
                "role": "pdf_derivative",
                "authority_status": "generated_noncanonical",
                "audience": "human_readers",
                "source_hash": pdf_hash,
                "related_source": tex_row["object_id"],
                "generated_from": tex_row["object_id"],
                "generated_outputs": wiki_path,
                "owner_skill": "pdf-derivative-build",
                "validation_status": "PASS" if pdf_abs.exists() else "FAIL",
                "last_validated_at": last_validated_at,
                "notes": "Generated human-reading derivative from registered TeX source.",
                "source_tex_object_id": tex_row["object_id"],
                "source_tex_path": tex_row["path"],
                "source_tex_hash": tex_row["source_hash"],
                "pdf_hash": pdf_hash,
                "build_command": PDF_BUILD_COMMAND,
                "build_status": "built" if pdf_abs.exists() else "missing",
                "built_at": built_at,
            }
        )
    write_csv_if_changed(registry_path("PDF_DERIVATIVE_REGISTRY.csv"), PDF_COLUMNS, rows)
    return rows


def html_spec_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    try:
        frontmatter, _body = load_frontmatter(path)
    except StrictYamlError as exc:
        return {}, str(exc)
    return frontmatter, ""


def html_spec_rows_by_output(markdown_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    specs: dict[str, dict[str, str]] = {}
    for row in markdown_rows:
        if row.get("role") != "html_explainer_source_spec":
            continue
        path = REPO_ROOT / row.get("path", "")
        frontmatter, error = html_spec_frontmatter(path)
        if error:
            continue
        output_path = str(frontmatter.get("output_path", "")).strip()
        if output_path:
            specs[output_path] = {
                "object_id": row["object_id"],
                "source_hash": row["source_hash"],
                "renderer_skill": str(frontmatter.get("renderer_skill", "")).strip(),
            }
    return specs


def html_meta_value(pattern: re.Pattern[str], html_text: str) -> str:
    match = pattern.search(html_text)
    return match.group(1).strip() if match else ""


def generate_html_rows(now: str, markdown_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    existing = existing_by_id(read_csv_rows(registry_path("HTML_EXPLAINER_REGISTRY.csv")))
    specs_by_output = html_spec_rows_by_output(markdown_rows)
    rows = []
    for path in sorted((REPO_ROOT / "html").glob("*.html")):
        relative = rel_path(path)
        existing_row = next(
            (row for row in existing.values() if row.get("path") == relative),
            {},
        )
        spec_row = specs_by_output.get(relative, {})
        if existing_row:
            object_id = existing_row["object_id"]
        else:
            object_id = f"HTML-{object_suffix_from_stem(path.stem)}"
        html_hash = sha256_file(path)
        html_changed = existing_row.get("html_hash") != html_hash
        if not existing_row or html_changed:
            source_basis = spec_row.get("object_id", "")
            source_basis_hash = spec_row.get("source_hash", "")
            skill_version = spec_row.get("renderer_skill", "")
        else:
            source_basis = spec_row.get("object_id", existing_row.get("source_basis", ""))
            source_basis_hash = existing_row.get("source_basis_hash", "")
            skill_version = spec_row.get(
                "renderer_skill", existing_row.get("visual_explainer_skill_version", "")
            )
        last_validated_at = existing_row.get("last_validated_at", "")
        if html_changed:
            last_validated_at = now
        if not last_validated_at:
            last_validated_at = now
        rows.append(
            {
                "object_id": object_id,
                "path": relative,
                "format": "html",
                "role": "html_visual_explainer",
                "authority_status": "generated_noncanonical",
                "audience": "humans",
                "source_hash": html_hash,
                "related_source": source_basis,
                "generated_from": source_basis,
                "generated_outputs": wiki_path_for_source(
                    {"object_id": object_id, "format": "html"}
                ),
                "owner_skill": "html-visual-explainer",
                "validation_status": "PASS",
                "last_validated_at": last_validated_at,
                "notes": "Human-only generated visual explainer.",
                "human_visual_only": "true",
                "source_basis": source_basis,
                "source_basis_hash": source_basis_hash,
                "html_hash": html_hash,
                "visual_explainer_skill_version": skill_version,
            }
        )
    write_csv_if_changed(registry_path("HTML_EXPLAINER_REGISTRY.csv"), HTML_COLUMNS, rows)
    return rows


def source_rows_by_registry() -> dict[str, list[dict[str, str]]]:
    return {name: read_csv_rows(registry_path(name)) for name in SOURCE_REGISTRY_NAMES}


def all_source_rows(rows_by_registry: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for registry_name in SOURCE_REGISTRY_NAMES:
        rows.extend(rows_by_registry.get(registry_name, []))
    return rows


def related_lines(source_row: dict[str, str], lookup: dict[str, dict[str, str]]) -> list[str]:
    lines: list[str] = []
    related_source = source_row.get("related_source", "")
    generated_from = source_row.get("generated_from", "")
    if related_source:
        target = lookup.get(related_source, {})
        lines.append(f"- Related source: `{related_source}` `{target.get('path', '')}`")
    if generated_from and generated_from != related_source:
        target = lookup.get(generated_from, {})
        lines.append(f"- Generated from: `{generated_from}` `{target.get('path', '')}`")
    generated_outputs = [
        item.strip() for item in source_row.get("generated_outputs", "").split(";") if item.strip()
    ]
    for output in generated_outputs:
        object_target = lookup.get(output, {})
        if object_target:
            lines.append(f"- Generated output object: `{output}` `{object_target.get('path', '')}`")
        else:
            lines.append(f"- Generated output path: `{output}`")
    for object_id, target in sorted(lookup.items()):
        if target.get("related_source") == source_row["object_id"] or target.get(
            "generated_from"
        ) == source_row["object_id"]:
            lines.append(f"- Backlink from `{object_id}` `{target.get('path', '')}`")
    return lines


def wiki_note_text(source_row: dict[str, str], lookup: dict[str, dict[str, str]]) -> str:
    lines = [
        f"# {wiki_object_id(source_row['object_id'])}",
        "",
        "Generated metadata note. Not canonical authority. Update the source file and registry row, then regenerate.",
        "",
        "## Source",
        "",
        f"- Source object: `{source_row['object_id']}`",
        f"- Source path: `{source_row.get('path', '')}`",
        f"- Format: `{source_row.get('format', '')}`",
        f"- Role: `{source_row.get('role', '')}`",
        f"- Authority status: `{source_row.get('authority_status', '')}`",
        f"- Owner skill: `{source_row.get('owner_skill', '')}`",
        f"- Source hash: `{source_row.get('source_hash', '')}`",
        "",
        "## Related Objects",
        "",
    ]
    related = related_lines(source_row, lookup)
    lines.extend(related if related else ["- None registered."])
    lines.extend(
        [
            "",
            "## Validation",
            "",
            f"- Validation status: `{source_row.get('validation_status', '')}`",
            f"- Last validated at: `{source_row.get('last_validated_at', '')}`",
            "",
        ]
    )
    return "\n".join(lines)


def generate_wiki(rows_by_registry: dict[str, list[dict[str, str]]], now: str) -> list[dict[str, str]]:
    source_rows = all_source_rows(rows_by_registry)
    lookup = {row["object_id"]: row for row in source_rows}
    existing = existing_by_id(read_csv_rows(registry_path("WIKI_ARTIFACT_REGISTRY.csv")))
    wiki_rows: list[dict[str, str]] = []

    for source_row in sorted(source_rows, key=lambda row: row["object_id"]):
        object_id = wiki_object_id(source_row["object_id"])
        note_path = wiki_path_for_source(source_row)
        text = wiki_note_text(source_row, lookup)
        write_text_if_changed(REPO_ROOT / note_path, text)
        wiki_hash = sha256_text(text)
        existing_row = existing.get(object_id, {})
        generated_at = existing_row.get("generated_at", "")
        last_validated_at = existing_row.get("last_validated_at", "")
        if (
            existing_row.get("source_object_hash") != source_row.get("source_hash")
            or existing_row.get("wiki_hash") != wiki_hash
        ):
            generated_at = now
            last_validated_at = now
        if not generated_at:
            generated_at = now
        if not last_validated_at:
            last_validated_at = now
        wiki_rows.append(
            {
                "object_id": object_id,
                "path": note_path,
                "format": "wiki_markdown",
                "role": "generated_metadata_note",
                "authority_status": "generated_noncanonical",
                "audience": "humans_and_agents",
                "source_hash": wiki_hash,
                "related_source": source_row["object_id"],
                "generated_from": source_row["object_id"],
                "generated_outputs": "",
                "owner_skill": "markdown-wiki",
                "validation_status": "PASS",
                "last_validated_at": last_validated_at,
                "notes": "Generated metadata note; not canonical authority.",
                "source_object_id": source_row["object_id"],
                "source_path": source_row.get("path", ""),
                "source_object_hash": source_row.get("source_hash", ""),
                "wiki_hash": wiki_hash,
                "wiki_kind": wiki_lane_for_format(source_row.get("format", "markdown")),
                "generated_at": generated_at,
            }
        )

    write_csv_if_changed(
        registry_path("WIKI_ARTIFACT_REGISTRY.csv"), WIKI_COLUMNS, wiki_rows
    )
    write_meta_if_needed(
        "WIKI_ARTIFACT_REGISTRY",
        [registry_path(name) for name in SOURCE_REGISTRY_NAMES],
        now,
    )
    return wiki_rows


def group_index_text(title: str, groups: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        f"# {title}",
        "",
        "Generated metadata index. Not canonical authority. Update source registries, then regenerate.",
        "",
    ]
    for key in sorted(groups):
        lines.extend([f"## {key or 'blank'}", ""])
        for row in sorted(groups[key], key=lambda item: item["object_id"]):
            lines.append(f"- `{row['object_id']}` `{row.get('path', '')}`")
        lines.append("")
    return "\n".join(lines)


def generate_indexes(rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    rows = all_source_rows(rows_by_registry)
    wiki_rows = read_csv_rows(registry_path("WIKI_ARTIFACT_REGISTRY.csv"))
    all_rows = rows + wiki_rows

    for filename, title, field_name in [
        ("by-format.md", "Index By Format", "format"),
        ("by-authority-status.md", "Index By Authority Status", "authority_status"),
        ("by-owner-skill.md", "Index By Owner Skill", "owner_skill"),
    ]:
        groups: dict[str, list[dict[str, str]]] = {}
        for row in all_rows:
            groups.setdefault(row.get(field_name, ""), []).append(row)
        write_text_if_changed(
            REPO_ROOT / "wiki" / "indexes" / filename, group_index_text(title, groups)
        )

    groups = {}
    for row in rows_by_registry.get("TEX_SOURCE_REGISTRY.csv", []):
        groups.setdefault(row.get("ontology_promotion_status", ""), []).append(row)
    write_text_if_changed(
        REPO_ROOT / "wiki" / "indexes" / "by-ontology-promotion-status.md",
        group_index_text("Index By Ontology Promotion Status", groups),
    )


def generate_file_object_registry(
    rows_by_registry: dict[str, list[dict[str, str]]], now: str
) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    mirrored_registry_names = SOURCE_REGISTRY_NAMES + [
        name for name in GENERATED_REGISTRY_NAMES if name != "FILE_OBJECT_REGISTRY.csv"
    ]
    for registry_name in mirrored_registry_names:
        for row in rows_by_registry.get(registry_name, []):
            output = {field: row.get(field, "") for field in COMMON_COLUMNS}
            output["source_registry"] = registry_name
            output_rows.append(output)
    output_rows.sort(key=lambda row: row["object_id"])
    write_csv_if_changed(
        registry_path("FILE_OBJECT_REGISTRY.csv"), FILE_OBJECT_COLUMNS, output_rows
    )
    write_meta_if_needed(
        "FILE_OBJECT_REGISTRY",
        [registry_path(name) for name in mirrored_registry_names],
        now,
    )
    return output_rows


def path_is_under(path_text: str, folder: str) -> bool:
    if folder == ".":
        return bool(path_text)
    return path_text == folder or path_text.startswith(f"{folder}/")


def project_directories() -> list[str]:
    directories = {"."}
    for root, dirnames, _filenames in os.walk(REPO_ROOT):
        dirnames[:] = sorted(
            name for name in dirnames if name not in FOLDER_WALK_SKIP_NAMES
        )
        root_path = Path(root)
        if root_path == REPO_ROOT:
            continue
        directories.add(rel_path(root_path))
    return sorted(directories, key=lambda value: (value.count("/"), value))


def registry_counts_for_folder(
    folder: str, rows_by_registry: dict[str, list[dict[str, str]]]
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for registry_name, rows in rows_by_registry.items():
        count = 0
        for row in rows:
            path_text = row.get("path", "")
            if path_text and path_is_under(path_text, folder):
                count += 1
        if count:
            counts[registry_name] = count
    return counts


def csv_relation_for_folder(
    folder: str, rows_by_registry: dict[str, list[dict[str, str]]]
) -> str:
    if folder == "registries":
        return "CSV authority directory."
    counts = registry_counts_for_folder(folder, rows_by_registry)
    if not counts:
        return "No registered object rows."
    parts = [
        f"{name.replace('.csv', '')}: {counts[name]}"
        for name in sorted(counts)
    ]
    return "; ".join(parts)


def source_object_ids_for_folder(
    folder: str, rows_by_registry: dict[str, list[dict[str, str]]]
) -> set[str]:
    object_ids: set[str] = set()
    for registry_name in SOURCE_REGISTRY_NAMES:
        for row in rows_by_registry.get(registry_name, []):
            path_text = row.get("path", "")
            if path_text and path_is_under(path_text, folder):
                object_ids.add(row.get("object_id", ""))
    return {object_id for object_id in object_ids if object_id}


def wiki_relation_for_folder(
    folder: str, rows_by_registry: dict[str, list[dict[str, str]]]
) -> str:
    if folder == "wiki" or folder.startswith("wiki/"):
        return "Generated wiki metadata lives here; edit sources and registries instead."
    if folder == "registries":
        return "Registry rows drive generated wiki notes and indexes."
    source_ids = source_object_ids_for_folder(folder, rows_by_registry)
    if not source_ids:
        return "No direct generated wiki notes."
    wiki_rows = rows_by_registry.get("WIKI_ARTIFACT_REGISTRY.csv", [])
    note_count = sum(
        1 for row in wiki_rows if row.get("source_object_id", "") in source_ids
    )
    if note_count:
        return f"{note_count} generated wiki note(s) point back to sources here."
    return "Registered source lane; wiki note missing until bootstrap regenerates."


def folder_contains_files(folder: str) -> bool:
    path = REPO_ROOT if folder == "." else REPO_ROOT / folder
    if not path.exists():
        return False
    return any(
        child.is_file() and child.name not in FOLDER_MAP_EXCLUDED_FILES
        for child in path.iterdir()
    )


def classify_folder(
    folder: str, rows_by_registry: dict[str, list[dict[str, str]]]
) -> tuple[str, str]:
    if folder == ".":
        return "control authority", "Repository front door and validation entrypoint."
    if folder == ".local" or folder.startswith(".local/"):
        return "local retrieval", "Ignored local cache, vault, extracted text, or search index."
    if folder == ".codex" or folder.startswith(".codex/"):
        return "tooling", "Repo-local skill, prompt, template, or script tooling."
    if folder == "scripts" or folder.startswith("scripts/"):
        return "tooling", "Validation and research-control support scripts."
    if folder == "tests" or folder.startswith("tests/"):
        return "tooling", "Smoke and regression tests for the memory/control system."
    if folder == ".agents" or folder.startswith(".agents/"):
        return "control authority", "Versioned role contracts and schemas."
    if folder == "registries":
        return "control authority", "CSV authority layer for provenance, routing, and generated-output tracking."
    if folder == "research_control" or folder.startswith("research_control/"):
        return "control authority", "Tracked Director decisions, AgentJobs, handoffs, tasks, and claim boundaries."
    if folder == "wiki" or folder.startswith("wiki/"):
        return "generated derivative", "Generated metadata notes and indexes; not source authority."
    if folder.endswith("/pdfs") or folder == "ontology/pdfs" or folder == "manuscripts/pdfs":
        return "generated derivative", "Human-reading PDF derivatives from registered TeX."
    if folder == "html" or folder.startswith("html/"):
        category = "generated derivative" if folder_contains_files(folder) else "reserved lane"
        return category, "Generated human-only visual explainer lane."
    if folder == "ontology" or folder == "ontology/tex":
        return "canonical source", "Ontology and exact-GR benchmark source lane."
    if folder == "manuscripts" or folder == "manuscripts/tex":
        category = "canonical source" if folder_contains_files(folder) else "reserved lane"
        return category, "Future manuscript source lane."
    if folder == "markdown" or folder.startswith("markdown/"):
        category = "canonical source" if folder_contains_files(folder) else "reserved lane"
        return category, "Authored Markdown source or reserved source-spec lane."
    if folder == "tex_shared" or folder.startswith("tex_shared/"):
        return "canonical source", "Shared TeX inputs included by registered TeX sources."
    if folder == "assets" or folder.startswith("assets/"):
        return "reserved lane", "Project media assets; outside current registry authority."
    if folder == "Step-by-step-Comments" or folder.startswith("Step-by-step-Comments/"):
        return "local retrieval", "Ignored local reference notes; not canonical authority."

    counts = registry_counts_for_folder(folder, rows_by_registry)
    if any(name.startswith("WIKI_") for name in counts):
        return "generated derivative", "Generated registry-backed derivative lane."
    if counts:
        return "control authority", "Contains registered objects; inspect CSV rows for authority."
    return "reserved lane", "No registered objects currently live here."


def folder_research_role(folder: str, category: str) -> str:
    if folder == ".":
        return "Repository front door for project identity, instructions, validation, and generated folder classification."
    if folder == "ontology" or folder.startswith("ontology/"):
        return "Holds the ontology and benchmark package used as the derivation target and constraint set."
    if folder == "research_control" or folder.startswith("research_control/tasks"):
        return "Runs bounded proposal, audit, refutation, repair, and handoff transactions."
    if folder == "registries":
        return "Makes research state machine-checkable through object IDs, hashes, status, and relationships."
    if folder == "wiki" or folder.startswith("wiki/"):
        return "Makes registered objects easier to browse without changing authority."
    if folder == ".local" or folder.startswith(".local/"):
        return "Supports retrieval and semantic search for agents; ignored by Git."
    if folder == ".agents" or folder.startswith(".agents/"):
        return "Defines permitted agent behavior and claim boundaries."
    if category == "local retrieval":
        return "Supports local retrieval, semantic search, or ignored reference use; not tracked authority."
    if category == "tooling":
        return "Operates or tests the research memory/control workflow."
    if category == "generated derivative":
        return "Provides generated reading surfaces derived from registered sources."
    if category == "control authority":
        return "Maintains project governance, validation, routing, or registry authority."
    if category == "reserved lane":
        return "Reserved for future project material; currently not active authority."
    return "Provides authored source material used by the research workflow."


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def folder_map_text(rows_by_registry: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        "# Folder Map",
        "",
        "Generated folder map. Not canonical authority. Update source files, registry rows, or folder contents, then regenerate with bootstrap.",
        "",
        "## Source Basis",
        "",
        "- Live repository directory tree, excluding `.git/`, `.venv/`, and `__pycache__/`.",
        "- Source and generated CSV registries under `registries/`.",
        "- Project authority rules in `AGENTS.md` and the memory-system bootstrap script.",
        "",
        "## Category Key",
        "",
        "- `canonical source`: authored source material that can carry project meaning.",
        "- `control authority`: tracked governance, routing, validation, registry, or task-control material.",
        "- `generated derivative`: generated human or agent reading surfaces.",
        "- `local retrieval`: ignored local cache, vault, semantic extraction, or search layer.",
        "- `tooling`: scripts, skills, prompts, templates, or tests.",
        "- `reserved lane`: intentional placeholder or support lane without active registered authority.",
        "",
        "## Folder Table",
        "",
        "| Folder | Category | CSV Relation | Wiki Relation | Research Role |",
        "| --- | --- | --- | --- | --- |",
    ]
    for folder in project_directories():
        category, default_role = classify_folder(folder, rows_by_registry)
        if category not in FOLDER_MAP_CATEGORIES:
            raise ValueError(f"Invalid folder category for {folder}: {category}")
        research_role = folder_research_role(folder, category) or default_role
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_table_cell(folder)}`",
                    f"`{category}`",
                    escape_table_cell(csv_relation_for_folder(folder, rows_by_registry)),
                    escape_table_cell(wiki_relation_for_folder(folder, rows_by_registry)),
                    escape_table_cell(research_role),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def generate_folder_map(rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    write_text_if_changed(FOLDER_MAP_PATH, folder_map_text(rows_by_registry))


def validate_folder_map(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    if not FOLDER_MAP_PATH.exists():
        report.error("missing generated folder map: FOLDER_MAP.md")
        return
    expected = folder_map_text(rows_by_registry)
    actual = FOLDER_MAP_PATH.read_text(encoding="utf-8")
    if actual != expected:
        report.error("stale generated folder map: FOLDER_MAP.md")


def write_meta_if_needed(name: str, inputs: list[Path], now: str) -> None:
    meta_path = REPO_ROOT / "registries" / f"{name}.meta.json"
    existing: dict[str, object] = {}
    if meta_path.exists():
        try:
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    input_hashes = {
        rel_path(path): sha256_file(path) for path in inputs if path.exists()
    }
    generated_at = existing.get("generated_at", "")
    if existing.get("input_hashes") != input_hashes:
        generated_at = now
    if not generated_at:
        generated_at = now
    payload = {
        "registry": f"registries/{name}.csv",
        "generator_command": ".venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
        "generated_at": generated_at,
        "input_hashes": input_hashes,
    }
    write_text_if_changed(meta_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def find_duplicate_object_ids(
    rows_by_registry: dict[str, list[dict[str, str]]]
) -> list[str]:
    seen: dict[str, str] = {}
    errors: list[str] = []
    for registry_name, rows in rows_by_registry.items():
        if registry_name == "FILE_OBJECT_REGISTRY.csv":
            continue
        for row in rows:
            object_id = row.get("object_id", "")
            if not object_id:
                errors.append(f"{registry_name}: row missing object_id")
                continue
            if object_id in seen:
                errors.append(
                    f"duplicate object_id {object_id} in {seen[object_id]} and {registry_name}"
                )
            else:
                seen[object_id] = registry_name
    return errors


def validate_columns(report: ValidationReport) -> None:
    for name, fieldnames in REGISTRIES.items():
        path = registry_path(name)
        if not path.exists():
            report.error(f"missing registry: registries/{name}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            try:
                header = next(reader)
            except StopIteration:
                report.error(f"empty registry: registries/{name}")
                continue
        missing = [field for field in fieldnames if field not in header]
        if missing:
            report.error(f"registries/{name} missing columns: {', '.join(missing)}")


def validate_paths(report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    path_fields = [
        "path",
        "related_source",
        "generated_from",
        "generated_outputs",
        "pdf_path",
        "source_tex_path",
        "source_path",
    ]
    for registry_name, rows in rows_by_registry.items():
        for row in rows:
            for field_name in path_fields:
                value = row.get(field_name, "")
                if not value:
                    continue
                for part in str(value).split(";"):
                    part = part.strip()
                    if not part or re.match(r"^[A-Z]+-", part):
                        continue
                    reason = validate_relative_path(part)
                    if reason:
                        report.error(
                            f"{registry_name} {row.get('object_id', '')} {field_name}: {reason}"
                        )


def validate_source_hashes(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    for registry_name in SOURCE_REGISTRY_NAMES + ["WIKI_ARTIFACT_REGISTRY.csv"]:
        for row in rows_by_registry.get(registry_name, []):
            path_text = row.get("path", "")
            if not path_text:
                continue
            path = REPO_ROOT / path_text
            if not path.exists():
                report.error(f"{registry_name} {row.get('object_id', '')}: missing path {path_text}")
                continue
            expected = sha256_file(path)
            if row.get("source_hash", "") != expected:
                report.error(
                    f"{registry_name} {row.get('object_id', '')}: stale source_hash for {path_text}"
                )


def validate_pdf_registry(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    tex_rows = existing_by_id(rows_by_registry.get("TEX_SOURCE_REGISTRY.csv", []))
    pdf_rows = existing_by_id(rows_by_registry.get("PDF_DERIVATIVE_REGISTRY.csv", []))
    registered_pdf_paths = {row.get("path", "") for row in pdf_rows.values()}

    for lane in ["ontology/pdfs", "manuscripts/pdfs"]:
        directory = REPO_ROOT / lane
        for pdf_path in sorted(directory.glob("*.pdf")):
            relative = rel_path(pdf_path)
            if relative not in registered_pdf_paths:
                report.error(f"unregistered project PDF: {relative}")

    for row in pdf_rows.values():
        object_id = row.get("object_id", "")
        source_object_id = row.get("source_tex_object_id", "")
        tex_row = tex_rows.get(source_object_id)
        if not tex_row:
            report.error(f"{object_id}: missing source TeX object {source_object_id}")
            continue
        expected_pdf_path = pdf_path_for_tex_path(tex_row["path"])
        if row.get("path", "") != expected_pdf_path:
            report.error(f"{object_id}: PDF path does not match TeX lane mapping")
        if row.get("source_tex_path", "") != tex_row.get("path", ""):
            report.error(f"{object_id}: source_tex_path does not match TeX registry")
        if row.get("source_tex_hash", "") != tex_row.get("source_hash", ""):
            report.error(f"{object_id}: stale source_tex_hash")
        pdf_path = REPO_ROOT / row.get("path", "")
        if not pdf_path.exists():
            report.error(f"{object_id}: missing PDF {row.get('path', '')}")
            continue
        pdf_hash = sha256_file(pdf_path)
        if row.get("pdf_hash", "") != pdf_hash:
            report.error(f"{object_id}: stale pdf_hash")
        if row.get("authority_status") != "generated_noncanonical":
            report.error(f"{object_id}: PDF authority_status must be generated_noncanonical")


def validate_html_specs(report: ValidationReport, markdown_rows: list[dict[str, str]]) -> None:
    output_paths: dict[str, str] = {}
    for row in markdown_rows:
        if row.get("role") != "html_explainer_source_spec":
            continue
        object_id = row.get("object_id", "")
        path_text = row.get("path", "")
        path = REPO_ROOT / path_text
        if not path.exists():
            report.error(f"{object_id}: missing HTML explainer spec {path_text}")
            continue
        frontmatter, error = html_spec_frontmatter(path)
        if error:
            report.error(f"{object_id}: invalid HTML explainer spec frontmatter: {error}")
            continue
        for field_name in sorted(HTML_SPEC_REQUIRED_FIELDS):
            value = frontmatter.get(field_name)
            if field_name not in frontmatter or value is None or value == "":
                report.error(f"{object_id}: HTML explainer spec missing {field_name}")
        output_path = str(frontmatter.get("output_path", "")).strip()
        if output_path:
            reason = validate_relative_path(output_path)
            if reason:
                report.error(f"{object_id}: invalid output_path: {reason}")
            elif not output_path.startswith("html/") or not output_path.endswith(".html"):
                report.error(f"{object_id}: output_path must be a tracked html/*.html file")
            elif not (REPO_ROOT / output_path).exists():
                report.error(f"{object_id}: output_path does not exist: {output_path}")
            previous = output_paths.get(output_path)
            if previous:
                report.error(
                    f"{object_id}: output_path duplicates {previous}: {output_path}"
                )
            output_paths[output_path] = object_id
        if bool(frontmatter.get("human_visual_only", False)) is not True:
            report.error(f"{object_id}: human_visual_only must be true")
        source_materials = frontmatter.get("source_materials", [])
        if not isinstance(source_materials, list) or not source_materials:
            report.error(f"{object_id}: source_materials must be a non-empty list")


def validate_tex_vocab(report: ValidationReport, rows: list[dict[str, str]]) -> None:
    for row in rows:
        object_id = row.get("object_id", "")
        if row.get("equation_scope", "") not in EQUATION_SCOPE_VALUES:
            report.error(f"{object_id}: invalid equation_scope")
        if row.get("claim_status", "") not in CLAIM_STATUS_VALUES:
            report.error(f"{object_id}: invalid claim_status")
        if row.get("research_status", "") not in RESEARCH_STATUS_VALUES:
            report.error(f"{object_id}: invalid research_status")
        if row.get("ontology_promotion_status", "") not in PROMOTION_STATUS_VALUES:
            report.error(f"{object_id}: invalid ontology_promotion_status")
        if row.get("pdf_required") not in {"true", "false", ""}:
            report.error(f"{object_id}: pdf_required must be true or false")


def validate_html_registry(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    markdown_rows = existing_by_id(rows_by_registry.get("MARKDOWN_SOURCE_REGISTRY.csv", []))
    html_rows = existing_by_id(rows_by_registry.get("HTML_EXPLAINER_REGISTRY.csv", []))
    registered_html_paths = {row.get("path", "") for row in html_rows.values()}

    for html_path in sorted((REPO_ROOT / "html").glob("*.html")):
        relative = rel_path(html_path)
        if relative not in registered_html_paths:
            report.error(f"unregistered tracked HTML explainer: {relative}")

    for row in html_rows.values():
        object_id = row.get("object_id", "")
        if row.get("human_visual_only") != "true":
            report.error(f"{object_id}: human_visual_only must be true")
        source_basis = row.get("source_basis", "")
        source_row = markdown_rows.get(source_basis)
        if not source_row:
            report.error(f"{object_id}: source_basis must be a registered Markdown object ID")
            continue
        if source_row.get("role") != "html_explainer_source_spec":
            report.error(f"{object_id}: source_basis must point to an HTML explainer spec")
        if row.get("source_basis_hash", "") != source_row.get("source_hash", ""):
            report.error(f"{object_id}: stale source_basis_hash")
        html_path = REPO_ROOT / row.get("path", "")
        if html_path.exists() and row.get("html_hash", "") != sha256_file(html_path):
            report.error(f"{object_id}: stale html_hash")
        if not html_path.exists():
            report.error(f"{object_id}: missing HTML explainer {row.get('path', '')}")
            continue
        html_text = html_path.read_text(encoding="utf-8")
        html_source_basis = html_meta_value(HTML_SOURCE_BASIS_META_RE, html_text)
        html_source_basis_hash = html_meta_value(HTML_SOURCE_BASIS_HASH_META_RE, html_text)
        html_human_visual_only = html_meta_value(HTML_HUMAN_VISUAL_META_RE, html_text)
        if html_source_basis != source_basis:
            report.error(f"{object_id}: HTML source-basis metadata is stale or missing")
        if html_source_basis_hash != row.get("source_basis_hash", ""):
            report.error(f"{object_id}: HTML source-basis hash metadata is stale or missing")
        if html_human_visual_only != "true":
            report.error(f"{object_id}: HTML human-visual-only metadata must be true")


def validate_wiki_registry(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    source_rows = all_source_rows(rows_by_registry)
    source_lookup = {row["object_id"]: row for row in source_rows}
    wiki_rows = existing_by_id(rows_by_registry.get("WIKI_ARTIFACT_REGISTRY.csv", []))

    for source_row in source_rows:
        wiki_id = wiki_object_id(source_row["object_id"])
        wiki_row = wiki_rows.get(wiki_id)
        if not wiki_row:
            report.error(f"missing generated wiki note row for {source_row['object_id']}")
            continue
        expected_path = wiki_path_for_source(source_row)
        if wiki_row.get("path") != expected_path:
            report.error(f"{wiki_id}: wiki path does not match source object ID")
        note_path = REPO_ROOT / expected_path
        if not note_path.exists():
            report.error(f"{wiki_id}: missing wiki note {expected_path}")
            continue
        if wiki_row.get("wiki_hash", "") != sha256_file(note_path):
            report.error(f"{wiki_id}: stale wiki_hash")
        if wiki_row.get("source_object_hash", "") != source_row.get("source_hash", ""):
            report.error(f"{wiki_id}: stale source_object_hash")

    for wiki_row in wiki_rows.values():
        source_id = wiki_row.get("source_object_id", "")
        if source_id not in source_lookup:
            report.error(f"{wiki_row.get('object_id', '')}: source object no longer exists")


def validate_file_object_registry(
    report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]
) -> None:
    file_rows = existing_by_id(rows_by_registry.get("FILE_OBJECT_REGISTRY.csv", []))
    expected_ids = set()
    mirrored_registry_names = SOURCE_REGISTRY_NAMES + [
        name for name in GENERATED_REGISTRY_NAMES if name != "FILE_OBJECT_REGISTRY.csv"
    ]
    for registry_name in mirrored_registry_names:
        for row in rows_by_registry.get(registry_name, []):
            expected_ids.add(row.get("object_id", ""))
            mirror = file_rows.get(row.get("object_id", ""))
            if not mirror:
                report.error(f"FILE_OBJECT_REGISTRY missing {row.get('object_id', '')}")
                continue
            for field_name in COMMON_COLUMNS:
                if mirror.get(field_name, "") != row.get(field_name, ""):
                    report.error(
                        f"FILE_OBJECT_REGISTRY stale field {field_name} for {row.get('object_id', '')}"
                    )
                    break
    extra_ids = set(file_rows) - expected_ids
    for object_id in sorted(extra_ids):
        report.error(f"FILE_OBJECT_REGISTRY has stale extra object {object_id}")


def validate_tracked_local_noise(report: ValidationReport) -> None:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        report.warning("Could not inspect tracked files with git ls-files")
        return
    for line in result.stdout.splitlines():
        if not any(line == lane or line.startswith(f"{lane}/") for lane in CANONICAL_LANES):
            continue
        name = Path(line).name
        if name == ".DS_Store" or name.startswith("._"):
            report.error(f"tracked local noise in canonical lane: {line}")


def validate_all() -> ValidationReport:
    report = ValidationReport()
    validate_columns(report)
    rows_by_registry = {
        name: read_csv_rows(registry_path(name))
        for name in SOURCE_REGISTRY_NAMES + GENERATED_REGISTRY_NAMES
    }
    for error in find_duplicate_object_ids(rows_by_registry):
        report.error(error)
    validate_paths(report, rows_by_registry)
    validate_source_hashes(report, rows_by_registry)
    validate_tex_vocab(report, rows_by_registry.get("TEX_SOURCE_REGISTRY.csv", []))
    validate_pdf_registry(report, rows_by_registry)
    validate_html_specs(report, rows_by_registry.get("MARKDOWN_SOURCE_REGISTRY.csv", []))
    validate_html_registry(report, rows_by_registry)
    validate_wiki_registry(report, rows_by_registry)
    validate_file_object_registry(report, rows_by_registry)
    validate_folder_map(report, rows_by_registry)
    validate_tracked_local_noise(report)
    return report


def bootstrap(
    refresh_existing: bool = False,
    rebuilt_pdf_paths: Iterable[str] | None = None,
) -> ValidationReport:
    ensure_directories()
    now = utc_now()
    markdown_rows = merge_authored_registry(
        "MARKDOWN_SOURCE_REGISTRY.csv",
        MARKDOWN_COLUMNS,
        discover_markdown_rows(now),
        refresh_existing,
    )
    tex_rows = merge_authored_registry(
        "TEX_SOURCE_REGISTRY.csv", TEX_COLUMNS, discover_tex_rows(now), refresh_existing
    )
    pdf_rows = generate_pdf_rows(tex_rows, now, rebuilt_pdf_paths=rebuilt_pdf_paths)
    html_rows = generate_html_rows(now, markdown_rows)
    rows_by_registry = {
        "MARKDOWN_SOURCE_REGISTRY.csv": markdown_rows,
        "TEX_SOURCE_REGISTRY.csv": tex_rows,
        "PDF_DERIVATIVE_REGISTRY.csv": pdf_rows,
        "HTML_EXPLAINER_REGISTRY.csv": html_rows,
    }
    wiki_rows = generate_wiki(rows_by_registry, now)
    generate_indexes(rows_by_registry)
    rows_by_registry["WIKI_ARTIFACT_REGISTRY.csv"] = wiki_rows
    generated_rows = write_generated_registries(
        REPO_ROOT,
        rows_by_registry,
        now,
        write_semantic_text=True,
    )
    rows_by_registry.update(generated_rows)
    file_object_rows = generate_file_object_registry(rows_by_registry, now)
    rows_by_registry["FILE_OBJECT_REGISTRY.csv"] = file_object_rows
    generate_folder_map(rows_by_registry)
    return validate_all()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap or validate the repository memory/wiki/registry system."
    )
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Refresh existing authored source registry rows.",
    )
    parser.add_argument(
        "--validate-only",
        "--check",
        action="store_true",
        dest="validate_only",
        help="Validate current registries and generated outputs without writing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.validate_only:
        report = validate_all()
    else:
        report = bootstrap(refresh_existing=args.refresh_existing)
    report.print()
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
