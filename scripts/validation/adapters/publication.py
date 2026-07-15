#!/usr/bin/env python3
"""Explicit adapter for the blocking publication-validation gate.

Inputs are a repository root and the legacy strict-mode compatibility flag.
The output is a ``ValidationReport`` with gate ID ``publication_validation``;
publication errors remain blocking and publication warnings remain advisory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MEMORY_SCRIPT_DIR = REPO_ROOT / ".codex/skills/project-memory-system/scripts"
SCRIPTS_DIR = REPO_ROOT / "scripts"
for directory in (MEMORY_SCRIPT_DIR, SCRIPTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from memory_operations import ValidationReport  # noqa: E402
from validate_publication_process import validate_publication_process  # noqa: E402


GATE_ID = "publication_validation"
CHECK_ID = "publication_validation.process"


def publication_validation(
    repo_root: Path = REPO_ROOT,
    *,
    strict: bool = False,
) -> ValidationReport:
    """Run the active publication-process validator as one explicit gate."""

    del strict  # Accepted until the legacy compatibility surface is retired.
    source_report = validate_publication_process(repo_root)
    report = ValidationReport(gate_id=GATE_ID, check_ids=[CHECK_ID])
    for message in source_report.errors:
        report.error(message, finding_id=f"{CHECK_ID}.error")
    for message in source_report.warnings:
        report.warning(message, finding_id=f"{CHECK_ID}.warning")
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = publication_validation(args.root.resolve(), strict=args.strict)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        report.print()
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
