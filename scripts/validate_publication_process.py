#!/usr/bin/env python3
"""Validate the Documentation Curator Publication Process."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
STRICT_YAML_DIR = REPO_ROOT / "scripts" / "research_control"
if str(STRICT_YAML_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_YAML_DIR))

from strict_yaml import StrictYamlError, load_frontmatter  # noqa: E402


BRIEF_REGISTRY = "registries/PUBLICATION_BRIEF_REGISTRY.csv"
REQUIRED_BRIEF_COLUMNS = {
    "brief_id",
    "page_title",
    "document_type",
    "migration_status",
    "brief_path",
    "source_spec_path",
    "github_markdown_path",
    "html_output_path",
    "source_materials",
    "visual_strategy",
    "review_status",
    "screenshot_desktop_path",
    "screenshot_mobile_path",
    "before_after_review_path",
    "owner_role",
    "approval_required_before_corpus_migration",
    "notes",
}
BRIEF_FRONTMATTER_FIELDS = {
    "brief_id",
    "subject",
    "reader",
    "reader_job",
    "document_type",
    "reading_experience",
    "narrative_structure",
    "visual_strategy",
    "source_basis",
    "authority_boundaries",
    "output_surfaces",
    "acceptance_criteria",
    "forbidden_patterns",
    "migration_status",
}
MIGRATED_STATUSES = {"publication_brief_drafted", "publication_pilot", "pilot_approved", "migrated", "reviewed"}
ALLOWED_MIGRATION_STATUSES = MIGRATED_STATUSES | {"deferred"}
ALLOWED_DOCUMENT_TYPES = {
    "overview_article",
    "concept_explainer",
    "workflow_guide",
    "decision_or_lifecycle_guide",
    "reference_catalog",
    "troubleshooting_guide",
    "visual_brief",
    "comparison_or_boundary_map",
    "contributor_operator_guide",
}
ALLOWED_VISUAL_STRATEGIES = {
    "no_diagram",
    "bespoke_mermaid_diagram",
    "annotated_table",
    "process_timeline",
    "source_matrix",
    "role_matrix",
    "decision_tree",
    "state_model",
    "layered_architecture",
    "custom_html_visual",
}
FORBIDDEN_MIGRATED_HEADINGS = {
    "What This Does",
    "Why AEther Needs It",
    "System Map",
}
GENERIC_VISUAL_TERMS = {
    "Source bundle",
    "Reader model",
    "Source-backed output",
    "Validation",
}
AUTHORITY_TERMS = (
    "noncanonical",
    "non-authority",
    "does not change",
    "does not authorize",
    "not authority",
    "generated noncanonical",
)
BANNED_HTML_TOKENS = (
    "<script src=",
    "<link rel=\"stylesheet\" href=",
    "https://",
    "http://",
    "cdn.",
    "unpkg",
    "jsdelivr",
    "mermaid.min.js",
    "@agent-native",
    "plan.agent-native.com",
    "localhost",
    "127.0.0.1",
    "npx ",
)
SVG_NAMESPACE_MARKERS = (
    "http://www.w3.org/2000/svg",
    "http://www.w3.org/1999/xlink",
)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
MERMAID_BLOCK_RE = re.compile(r"(?ms)^```mermaid\s+(.*?)^```")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def count(self, key: str, amount: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + amount

    @property
    def ok(self) -> bool:
        return not self.errors

    def print(self) -> None:
        if self.ok:
            print("Publication process validation PASS")
        for error in self.errors:
            print(f"ERROR: {error}")
        for warning in self.warnings:
            print(f"WARNING: {warning}")
        for key, value in sorted(self.counts.items()):
            print(f"- {key}: {value}")


def read_csv(root: Path, path_text: str) -> list[dict[str, str]]:
    path = root / path_text
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def list_value(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def normalized_html(text: str) -> str:
    for marker in SVG_NAMESPACE_MARKERS:
        text = text.replace(marker, "")
    return text


def markdown_headings(text: str) -> tuple[str, ...]:
    return tuple(match.group(1).strip() for match in HEADING_RE.finditer(text))


def has_authority_boundary(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in AUTHORITY_TERMS)


def validate_registry_shapes(root: Path, report: Report) -> list[dict[str, str]]:
    brief_rows = read_csv(root, BRIEF_REGISTRY)
    if not brief_rows:
        report.error(f"{BRIEF_REGISTRY} is missing or empty")
    elif REQUIRED_BRIEF_COLUMNS - set(brief_rows[0]):
        missing = ", ".join(sorted(REQUIRED_BRIEF_COLUMNS - set(brief_rows[0])))
        report.error(f"{BRIEF_REGISTRY} missing columns: {missing}")
    return brief_rows


def validate_retired_topic_registry_absent(root: Path, report: Report) -> None:
    retired_path = root / "registries" / "EXPLAINER_TOPIC_REGISTRY.csv"
    if retired_path.exists():
        report.error("registries/EXPLAINER_TOPIC_REGISTRY.csv is retired and must not exist")


def validate_no_network_html(root: Path, report: Report) -> None:
    for html_path in sorted((root / "html").glob("*.html")):
        relative = html_path.relative_to(root).as_posix()
        lowered = normalized_html(read_text(html_path)).lower()
        for token in BANNED_HTML_TOKENS:
            if token.lower() in lowered:
                report.error(f"{relative}: banned public-doc runtime marker found: {token}")
        if "mermaid.initialize(" in lowered or "mermaid.render(" in lowered:
            report.error(f"{relative}: browser-side Mermaid execution is forbidden")
        report.count("checked_html_runtime")


def validate_no_orphan_public_surfaces(
    root: Path,
    brief_rows: list[dict[str, str]],
    report: Report,
) -> None:
    expected_specs = {row.get("source_spec_path", "").strip() for row in brief_rows}
    expected_github = {row.get("github_markdown_path", "").strip() for row in brief_rows}
    expected_html = {row.get("html_output_path", "").strip() for row in brief_rows}
    surface_sets = [
        ("source spec", root / "markdown" / "html-explainer-specs", "*-explainer.md", expected_specs),
        ("GitHub Markdown", root / "github-facing", "*-explainer.md", expected_github),
        ("HTML", root / "html", "*-explainer.html", expected_html),
    ]
    for label, directory, pattern, expected in surface_sets:
        for path in sorted(directory.glob(pattern)):
            relative = path.relative_to(root).as_posix()
            if relative not in expected:
                report.error(f"{relative}: orphan public {label} not listed in {BRIEF_REGISTRY}")


def validate_migrated_brief(root: Path, row: dict[str, str], report: Report) -> tuple[dict[str, object], str] | None:
    brief_id = row["brief_id"].strip()
    brief_path = root / row["brief_path"].strip()
    if row["migration_status"].strip() not in MIGRATED_STATUSES:
        return None
    if not brief_path.exists():
        report.error(f"{brief_id}: missing brief {row['brief_path']}")
        return None
    try:
        frontmatter, body = load_frontmatter(brief_path)
    except StrictYamlError as exc:
        report.error(f"{brief_id}: invalid brief frontmatter: {exc}")
        return None
    missing = BRIEF_FRONTMATTER_FIELDS - set(frontmatter)
    if missing:
        report.error(f"{brief_id}: brief missing fields: {', '.join(sorted(missing))}")
    if str(frontmatter.get("brief_id", "")).strip() != brief_id:
        report.error(f"{brief_id}: brief_id mismatch")
    if str(frontmatter.get("document_type", "")).strip() not in ALLOWED_DOCUMENT_TYPES:
        report.error(f"{brief_id}: invalid document_type")
    if str(frontmatter.get("visual_strategy", "")).strip() not in ALLOWED_VISUAL_STRATEGIES:
        report.error(f"{brief_id}: invalid visual_strategy")
    if str(frontmatter.get("migration_status", "")).strip() != row["migration_status"].strip():
        report.error(f"{brief_id}: migration_status mismatch between registry and brief")
    report.count("checked_briefs")
    return frontmatter, body


def validate_migrated_surfaces(
    root: Path,
    row: dict[str, str],
    brief_frontmatter: dict[str, object],
    report: Report,
) -> tuple[str, str] | None:
    brief_id = row["brief_id"].strip()
    spec_path = root / row["source_spec_path"].strip()
    github_path = root / row["github_markdown_path"].strip()
    html_path = root / row["html_output_path"].strip()
    for label, path in [("source spec", spec_path), ("GitHub Markdown", github_path), ("HTML", html_path)]:
        if not path.exists():
            report.error(f"{brief_id}: missing {label}: {path.relative_to(root).as_posix()}")
    if not spec_path.exists() or not github_path.exists() or not html_path.exists():
        return None
    try:
        spec_frontmatter, _spec_body = load_frontmatter(spec_path)
    except StrictYamlError as exc:
        report.error(f"{brief_id}: invalid source spec frontmatter: {exc}")
        return None
    if str(spec_frontmatter.get("publication_brief", "")).strip() != row["brief_path"].strip():
        report.error(f"{brief_id}: source spec publication_brief mismatch")
    for field in ["document_type", "visual_strategy", "migration_status"]:
        if str(spec_frontmatter.get(field, "")).strip() != row[field].strip():
            report.error(f"{brief_id}: source spec {field} mismatch")
    if str(spec_frontmatter.get("github_markdown_output_path", "")).strip() != row["github_markdown_path"].strip():
        report.error(f"{brief_id}: source spec github_markdown_output_path mismatch")
    if str(spec_frontmatter.get("output_path", "")).strip() != row["html_output_path"].strip():
        report.error(f"{brief_id}: source spec output_path mismatch")
    if spec_frontmatter.get("human_visual_only") is not True:
        report.error(f"{brief_id}: source spec human_visual_only must be true")
    if spec_frontmatter.get("no_external_runtime") is not True:
        report.error(f"{brief_id}: source spec no_external_runtime must be true")
    if "reader_blocks" in spec_frontmatter or "github_markdown_parity" in spec_frontmatter:
        report.error(f"{brief_id}: source spec still declares retired parity fields")
    source_materials = split_semicolon(row["source_materials"])
    brief_sources = list_value(brief_frontmatter.get("source_basis", []))
    spec_sources = list_value(spec_frontmatter.get("source_materials", []))
    if set(source_materials) != set(brief_sources) or set(source_materials) != set(spec_sources):
        report.error(f"{brief_id}: source_materials mismatch across registry, brief, and source spec")
    github_text = read_text(github_path)
    html_text = read_text(html_path)
    for source_path in source_materials:
        if source_path not in github_text:
            report.error(f"{brief_id}: GitHub Markdown missing source path {source_path}")
        if source_path not in html_text:
            report.error(f"{brief_id}: HTML missing source path {source_path}")
    if not has_authority_boundary(github_text):
        report.error(f"{brief_id}: GitHub Markdown missing non-authority boundary language")
    if not has_authority_boundary(html_text):
        report.error(f"{brief_id}: HTML missing non-authority boundary language")
    headings = set(markdown_headings(github_text))
    unauthorized = FORBIDDEN_MIGRATED_HEADINGS & headings
    if unauthorized:
        report.error(f"{brief_id}: migrated GitHub Markdown uses forbidden old heading(s): {', '.join(sorted(unauthorized))}")
    if any(term in github_text or term in html_text for term in GENERIC_VISUAL_TERMS):
        report.error(f"{brief_id}: migrated page contains generic visual vocabulary from the retired process")
    if MERMAID_BLOCK_RE.search(github_text) and "reader learns" not in github_text.lower():
        report.error(f"{brief_id}: Mermaid visual lacks reader-purpose prose")
    for evidence_field in ["screenshot_desktop_path", "screenshot_mobile_path", "before_after_review_path"]:
        evidence_path = root / row[evidence_field].strip()
        if not evidence_path.exists():
            report.error(f"{brief_id}: missing review evidence {evidence_field}: {row[evidence_field]}")
    if row.get("approval_required_before_corpus_migration", "").strip().lower() != "true":
        report.error(f"{brief_id}: approval_required_before_corpus_migration must be true")
    report.count("checked_migrated_surfaces")
    return github_text, html_text


def validate_duplicate_skeletons(surface_texts: dict[str, str], report: Report) -> None:
    seen: dict[tuple[str, ...], str] = {}
    for brief_id, text in sorted(surface_texts.items()):
        skeleton = markdown_headings(text)
        if not skeleton:
            report.error(f"{brief_id}: GitHub Markdown has no level-two sections")
            continue
        previous = seen.get(skeleton)
        if previous:
            report.error(f"{brief_id}: duplicate section skeleton matches {previous}")
        seen[skeleton] = brief_id


def validate_publication_process(root: Path) -> Report:
    report = Report()
    brief_rows = validate_registry_shapes(root, report)
    validate_retired_topic_registry_absent(root, report)
    validate_no_orphan_public_surfaces(root, brief_rows, report)
    validate_no_network_html(root, report)
    migrated_markdown: dict[str, str] = {}
    seen_briefs: set[str] = set()
    for row in brief_rows:
        brief_id = row.get("brief_id", "").strip()
        if not brief_id:
            report.error("publication brief row has blank brief_id")
            continue
        if brief_id in seen_briefs:
            report.error(f"{brief_id}: duplicate brief_id")
        seen_briefs.add(brief_id)
        if row.get("owner_role", "").strip() != "documentation-curator":
            report.error(f"{brief_id}: owner_role must be documentation-curator")
        if row.get("document_type", "").strip() not in ALLOWED_DOCUMENT_TYPES:
            report.error(f"{brief_id}: invalid registry document_type")
        if row.get("visual_strategy", "").strip() not in ALLOWED_VISUAL_STRATEGIES:
            report.error(f"{brief_id}: invalid registry visual_strategy")
        if row.get("migration_status", "").strip() not in ALLOWED_MIGRATION_STATUSES:
            report.error(f"{brief_id}: invalid registry migration_status")
        brief = validate_migrated_brief(root, row, report)
        if brief:
            surface_pair = validate_migrated_surfaces(root, row, brief[0], report)
            if surface_pair:
                migrated_markdown[brief_id] = surface_pair[0]
    validate_duplicate_skeletons(migrated_markdown, report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Accepted for bootstrap compatibility.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_publication_process(args.root.resolve())
    report.print()
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
