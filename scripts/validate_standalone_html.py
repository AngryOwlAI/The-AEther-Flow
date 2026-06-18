#!/usr/bin/env python3
"""Validate tracked HTML explainers are standalone no-network documents."""

from __future__ import annotations

import argparse
from pathlib import Path

from explainer_validation_lib import ValidationResult, read_text


BANNED = [
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
]

SVG_NAMESPACE_MARKERS = [
    "http://www.w3.org/2000/svg",
    "http://www.w3.org/1999/xlink",
]


def normalized_for_scan(text: str) -> str:
    for marker in SVG_NAMESPACE_MARKERS:
        text = text.replace(marker, "")
    return text


def validate_standalone_html(root: Path) -> ValidationResult:
    result = ValidationResult()
    for html_path in sorted((root / "html").glob("*.html")):
        relative = html_path.relative_to(root).as_posix()
        text = normalized_for_scan(read_text(html_path))
        lowered = text.lower()
        for token in BANNED:
            if token.lower() in lowered:
                result.error(f"{relative}: banned external/runtime marker found: {token}")
        if "class=\"mermaid\"" in lowered and "diagram-source" not in lowered:
            result.error(f"{relative}: browser-side Mermaid marker without preserved build-time source")
        result.count("checked_html_files")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true", help="Reserved for bootstrap strict-docs mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_standalone_html(args.root.resolve())
    result.print("Standalone HTML validation PASS")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
