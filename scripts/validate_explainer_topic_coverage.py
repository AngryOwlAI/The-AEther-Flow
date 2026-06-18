#!/usr/bin/env python3
"""Validate Documentation Curator Visual Atlas topic coverage."""

from __future__ import annotations

import argparse
from pathlib import Path

from explainer_validation_lib import (
    ValidationResult,
    declared_reader_blocks,
    declared_visual_ids,
    iter_required_topics,
    list_value,
    repo_path,
    spec_frontmatter_for,
    split_semicolon,
    topic_rows,
)


REQUIRED_COLUMNS = {
    "topic_id",
    "topic_name",
    "required",
    "status",
    "primary_audience",
    "source_spec_path",
    "github_markdown_path",
    "html_output_path",
    "wiki_index_path",
    "primary_sources",
    "required_visuals",
    "required_reader_blocks",
    "teaching_packet_required",
    "claim_boundary_id",
    "owner_role",
    "validation_status",
    "notes",
}


def validate_topic_coverage(root: Path) -> ValidationResult:
    result = ValidationResult()
    rows = topic_rows(root)
    if not rows:
        result.error("registries/EXPLAINER_TOPIC_REGISTRY.csv is missing or empty")
        return result
    missing_columns = REQUIRED_COLUMNS - set(rows[0])
    if missing_columns:
        result.error(
            "registries/EXPLAINER_TOPIC_REGISTRY.csv missing columns: "
            + ", ".join(sorted(missing_columns))
        )
        return result

    seen_topic_ids: set[str] = set()
    for row in rows:
        topic_id = row["topic_id"].strip()
        if not topic_id:
            result.error("topic row has blank topic_id")
            continue
        if topic_id in seen_topic_ids:
            result.error(f"{topic_id}: duplicate topic_id")
        seen_topic_ids.add(topic_id)
        if row["status"].strip() != "active":
            continue
        if row["validation_status"].strip() != "PASS":
            result.error(f"{topic_id}: validation_status must be PASS")
        if row["owner_role"].strip() != "documentation-curator":
            result.error(f"{topic_id}: owner_role must be documentation-curator")

    for row in iter_required_topics(rows):
        topic_id = row["topic_id"].strip()
        spec_path = row["source_spec_path"].strip()
        github_path = row["github_markdown_path"].strip()
        html_path = row["html_output_path"].strip()
        wiki_path = row["wiki_index_path"].strip()
        for label, path_text in [
            ("source_spec_path", spec_path),
            ("github_markdown_path", github_path),
            ("html_output_path", html_path),
        ]:
            if not path_text:
                result.error(f"{topic_id}: missing {label}")
            elif not repo_path(root, path_text).exists():
                result.error(f"{topic_id}: {label} does not exist: {path_text}")
        if wiki_path and not repo_path(root, wiki_path).exists():
            result.warning(f"{topic_id}: wiki_index_path not generated yet: {wiki_path}")
        if not spec_path or not repo_path(root, spec_path).exists():
            continue
        try:
            frontmatter, body = spec_frontmatter_for(root, spec_path)
        except ValueError as exc:
            result.error(f"{topic_id}: invalid source spec frontmatter: {exc}")
            continue

        if str(frontmatter.get("topic_id", "")).strip() != topic_id:
            result.error(f"{topic_id}: source spec topic_id does not match registry")
        if str(frontmatter.get("github_markdown_output_path", "")).strip() != github_path:
            result.error(f"{topic_id}: source spec github_markdown_output_path mismatch")
        if str(frontmatter.get("output_path", "")).strip() != html_path:
            result.error(f"{topic_id}: source spec output_path mismatch")
        if str(frontmatter.get("wiki_output_path", "")).strip() != wiki_path:
            result.error(f"{topic_id}: source spec wiki_output_path mismatch")

        source_materials = set(list_value(frontmatter.get("source_materials", [])))
        for source_path in split_semicolon(row["primary_sources"]):
            if source_path not in source_materials:
                result.error(f"{topic_id}: primary source missing from source_materials: {source_path}")

        visual_ids = declared_visual_ids(frontmatter, body)
        for visual_id in split_semicolon(row["required_visuals"]):
            if visual_id not in visual_ids:
                result.error(f"{topic_id}: required visual missing from source spec: {visual_id}")

        reader_blocks = declared_reader_blocks(frontmatter)
        for block_id in split_semicolon(row["required_reader_blocks"]):
            if block_id not in reader_blocks:
                result.error(f"{topic_id}: required reader block missing from source spec: {block_id}")
        if row["teaching_packet_required"].strip().lower() == "true":
            teaching_loop = frontmatter.get("teaching_loop", {})
            if not isinstance(teaching_loop, dict) or str(teaching_loop.get("enabled", "")).lower() != "true":
                result.error(f"{topic_id}: teaching_packet_required true but teaching_loop.enabled is not true")
            else:
                packet_path = str(teaching_loop.get("qa_packet", "")).strip()
                if not packet_path:
                    result.error(f"{topic_id}: teaching_loop missing qa_packet")
                elif not repo_path(root, packet_path).exists():
                    result.error(f"{topic_id}: qa_packet does not exist: {packet_path}")
        result.count("checked_required_topics")

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Reserved for bootstrap strict-docs mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_topic_coverage(args.root.resolve())
    result.print("Explainer topic coverage PASS")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
