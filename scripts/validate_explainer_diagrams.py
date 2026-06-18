#!/usr/bin/env python3
"""Validate declared atlas diagram IDs across source specs and derivatives."""

from __future__ import annotations

import argparse
from pathlib import Path

from explainer_validation_lib import (
    ValidationResult,
    declared_visual_ids,
    html_has_diagram_id,
    read_text,
    repo_path,
    spec_frontmatter_for,
)


def validate_diagrams(root: Path) -> ValidationResult:
    result = ValidationResult()
    for spec_path in sorted((root / "markdown" / "html-explainer-specs").glob("*-explainer.md")):
        relative_spec = spec_path.relative_to(root).as_posix()
        try:
            frontmatter, body = spec_frontmatter_for(root, relative_spec)
        except ValueError as exc:
            result.error(f"{relative_spec}: invalid source spec frontmatter: {exc}")
            continue
        github_path = str(frontmatter.get("github_markdown_output_path", "")).strip() or f"github-facing/{spec_path.name}"
        html_path = str(frontmatter.get("output_path", "")).strip()
        if not repo_path(root, github_path).exists() or not repo_path(root, html_path).exists():
            continue
        github_text = read_text(repo_path(root, github_path))
        html_text = read_text(repo_path(root, html_path))
        for diagram_id in declared_visual_ids(frontmatter, body):
            if f"mermaid-diagram-id: {diagram_id}" not in body:
                result.error(f"{relative_spec}: declared diagram id lacks source marker: {diagram_id}")
            if f"mermaid-diagram-id: {diagram_id}" not in github_text:
                result.error(f"{github_path}: missing Mermaid diagram marker: {diagram_id}")
            if not html_has_diagram_id(html_text, diagram_id):
                result.error(f"{html_path}: missing rendered diagram id: {diagram_id}")
            if "mermaid.initialize(" in html_text or "mermaid.render(" in html_text:
                result.error(f"{html_path}: imports or executes Mermaid at browser runtime")
            if f'data-mermaid-diagram-id="{diagram_id}"' in html_text and "<svg" not in html_text:
                result.error(f"{html_path}: diagram id lacks inline SVG or local semantic markup: {diagram_id}")
        result.count("checked_diagram_specs")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Reserved for bootstrap strict-docs mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_diagrams(args.root.resolve())
    result.print("Explainer diagram validation PASS")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
