#!/usr/bin/env python3
"""Explicit adapter for advisory local-retrieval health validation.

Inputs are a repository root plus optional vault and SQLite-index paths. The
output is a ``ValidationReport`` with gate ID ``local_retrieval_health``.
Findings are advisory by default and become blocking only when an authorized
memory-maintenance caller explicitly selects ``required=True``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MEMORY_SCRIPT_DIR = REPO_ROOT / ".codex/skills/project-memory-system/scripts"
if str(MEMORY_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(MEMORY_SCRIPT_DIR))

from memory_operations import ValidationReport  # noqa: E402
from obsidian_wiki_lib import local_retrieval_warning_records  # noqa: E402


GATE_ID = "local_retrieval_health"
CHECK_ID = "local_retrieval_health.freshness"


def _resolved_optional_path(repo_root: Path, value: Path | None) -> Path | None:
    if value is None:
        return None
    return value if value.is_absolute() else repo_root / value


def local_retrieval_health(
    repo_root: Path = REPO_ROOT,
    *,
    vault: Path | None = None,
    index_path: Path | None = None,
    required: bool = False,
) -> ValidationReport:
    """Inspect local retrieval state without mutating tracked or local files."""

    report = ValidationReport(gate_id=GATE_ID, check_ids=[CHECK_ID])
    records = local_retrieval_warning_records(
        repo_root,
        _resolved_optional_path(repo_root, vault),
        _resolved_optional_path(repo_root, index_path),
    )
    for record in records:
        category = record.get("category", "local_cache_only")
        message = f"Local retrieval freshness: {record.get('message', '')}"
        finding_id = f"{GATE_ID}.{category}"
        if required:
            report.error(message, finding_id=finding_id)
        else:
            report.warning(message, finding_id=finding_id)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--vault", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--required", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = local_retrieval_health(
        args.root.resolve(),
        vault=args.vault,
        index_path=args.index,
        required=args.required,
    )
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        report.print()
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
