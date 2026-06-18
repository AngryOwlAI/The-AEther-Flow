#!/usr/bin/env python3
"""Validate GitHub Markdown / HTML parity for atlas explainers."""

from __future__ import annotations

import argparse
from pathlib import Path

from explainer_validation_lib import (
    ValidationResult,
    bool_value,
    declared_reader_blocks,
    declared_visual_ids,
    html_data_values,
    html_has_block,
    html_has_diagram_id,
    list_value,
    markdown_code_spans,
    markdown_headings,
    read_text,
    reader_heading_for,
    repo_path,
    spec_frontmatter_for,
)


REQUIRED_BOUNDARY_HEADING = "What This Does Not Authorize"


def validate_parity(root: Path) -> ValidationResult:
    result = ValidationResult()
    for spec_path in sorted((root / "markdown" / "html-explainer-specs").glob("*-explainer.md")):
        relative_spec = spec_path.relative_to(root).as_posix()
        try:
            frontmatter, body = spec_frontmatter_for(root, relative_spec)
        except ValueError as exc:
            result.error(f"{relative_spec}: invalid source spec frontmatter: {exc}")
            continue

        github_path = str(frontmatter.get("github_markdown_output_path", "")).strip()
        html_path = str(frontmatter.get("output_path", "")).strip()
        if not github_path:
            github_path = f"github-facing/{spec_path.name}"
        if bool_value(frontmatter.get("github_markdown_parity", False)) and not repo_path(root, github_path).exists():
            result.error(f"{relative_spec}: github_markdown_parity true but output missing: {github_path}")
            continue
        if bool_value(frontmatter.get("standalone_html", False)) and not repo_path(root, html_path).exists():
            result.error(f"{relative_spec}: standalone_html true but output missing: {html_path}")
            continue
        if not repo_path(root, github_path).exists() or not repo_path(root, html_path).exists():
            continue

        github_text = read_text(repo_path(root, github_path))
        html_text = read_text(repo_path(root, html_path))
        headings = markdown_headings(github_text)
        github_sources = markdown_code_spans(github_text)
        html_sources = html_data_values("data-source-path", html_text)
        source_materials = set(list_value(frontmatter.get("source_materials", [])))

        reader_blocks = declared_reader_blocks(frontmatter)
        for block_id in reader_blocks:
            if block_id == "subject_summary":
                continue
            heading = reader_heading_for(block_id)
            if heading not in headings:
                result.error(f"{github_path}: missing reader block heading: {heading}")
            if not html_has_block(html_text, block_id):
                result.error(f"{html_path}: missing data-content-block for reader block: {block_id}")

        for diagram_id in declared_visual_ids(frontmatter, body):
            if f"mermaid-diagram-id: {diagram_id}" not in github_text:
                result.error(f"{github_path}: missing diagram marker: {diagram_id}")
            if not html_has_diagram_id(html_text, diagram_id):
                result.error(f"{html_path}: missing diagram id: {diagram_id}")

        for source_path in source_materials:
            if source_path not in github_sources:
                result.error(f"{github_path}: missing source path in Source Map: {source_path}")
            if source_path not in html_sources:
                result.error(f"{html_path}: missing visible source chip: {source_path}")

        if REQUIRED_BOUNDARY_HEADING not in headings:
            result.error(f"{github_path}: missing {REQUIRED_BOUNDARY_HEADING}")
        for required in ["Example", "Non-Example", "Common Confusions", "Source Map", "Next Reading Path"]:
            if required not in headings:
                result.error(f"{github_path}: missing {required}")
        for required_block in ["example", "non_example", "common_confusions", "source_map", "next_reading_path"]:
            if not html_has_block(html_text, required_block):
                result.error(f"{html_path}: missing required atlas block: {required_block}")
        result.count("checked_explainer_pairs")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Reserved for bootstrap strict-docs mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_parity(args.root.resolve())
    result.print("Explainer parity PASS")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
