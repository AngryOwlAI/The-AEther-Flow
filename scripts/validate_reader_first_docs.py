#!/usr/bin/env python3
"""Lint atlas explainers for reader-first subject explanation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from explainer_validation_lib import ValidationResult, read_text


METADATA_TERMS = re.compile(
    r"\b(source binding|generated_noncanonical|derived from spec|renderer|layout intent|source spec)\b",
    re.IGNORECASE,
)
FUNCTION_TERMS = re.compile(
    r"\b(does|needs|works|workflow|authority|claim|agentjob|derivation|ontology|validator|source|role|memory|benchmark|project)\b",
    re.IGNORECASE,
)
OBSOLETE_LABELS = (
    "Reader orientation",
    "What This Explainer Describes",
)
SELF_REFERENTIAL_START = re.compile(
    r"\b(this page explains|this explainer describes|this page describes|this explainer explains)\b",
    re.IGNORECASE,
)


def first_words(text: str, limit: int = 500) -> str:
    stripped = re.sub(r"(?ms)^---\n.*?\n---\n", "", text)
    stripped = re.sub(r"`{3}.*?`{3}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    words = re.findall(r"\S+", stripped)
    return " ".join(words[:limit])


def validate_markdown(path: Path, root: Path, result: ValidationResult) -> None:
    relative = path.relative_to(root).as_posix()
    text = read_text(path)
    opening = first_words(text, 500)
    first_120 = " ".join(opening.split()[:120])
    if "generated_noncanonical" in first_120 and not FUNCTION_TERMS.search(first_120):
        result.error(f"{relative}: generated_noncanonical appears before functional explanation")
    if METADATA_TERMS.search(first_120) and not FUNCTION_TERMS.search(first_120):
        result.error(f"{relative}: opening is metadata-first rather than subject-first")
    if SELF_REFERENTIAL_START.search(first_120):
        result.error(f"{relative}: opening self-describes the page instead of the subject")
    for label in OBSOLETE_LABELS:
        if label in text:
            result.error(f"{relative}: obsolete reader label is present: {label}")
    for needed in ["## Example", "## Non-Example", "## Common Confusions"]:
        if needed not in text:
            result.warning(f"{relative}: missing reader-first device: {needed}")
    result.count("checked_markdown_docs")


def validate_html(path: Path, root: Path, result: ValidationResult) -> None:
    relative = path.relative_to(root).as_posix()
    text = read_text(path)
    opening = first_words(text, 500)
    first_120 = " ".join(opening.split()[:120])
    if SELF_REFERENTIAL_START.search(first_120):
        result.error(f"{relative}: opening self-describes the page instead of the subject")
    for label in OBSOLETE_LABELS:
        if label in text:
            result.error(f"{relative}: obsolete reader label is present: {label}")
    for block in ["example", "non_example", "common_confusions"]:
        if f'data-content-block="{block}"' not in text:
            result.warning(f"{relative}: missing reader-first content block: {block}")
    result.count("checked_html_docs")


def validate_reader_first(root: Path, *, strict: bool = False) -> ValidationResult:
    result = ValidationResult()
    for path in sorted((root / "github-facing").glob("*-explainer.md")):
        validate_markdown(path, root, result)
    for path in sorted((root / "html").glob("*-explainer.html")):
        validate_html(path, root, result)
    if strict:
        for warning in result.warnings:
            result.error(warning)
        result.warnings.clear()
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Fail on warnings.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_reader_first(args.root.resolve(), strict=args.strict)
    result.print("Reader-first docs validation PASS")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
