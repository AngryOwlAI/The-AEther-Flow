#!/usr/bin/env python3
"""Collect tracked project-improvement signals."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNAL_REGISTRY = REPO_ROOT / "registries" / "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
OPEN_STATUSES = {"open", "pending", "active"}


def read_signals() -> list[dict[str, str]]:
    if not SIGNAL_REGISTRY.exists():
        return []
    with SIGNAL_REGISTRY.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def collect_signals(*, status: str | None = None, signal_type: str | None = None) -> dict[str, object]:
    rows = read_signals()
    if status:
        rows = [row for row in rows if row.get("status") == status]
    if signal_type:
        rows = [row for row in rows if row.get("signal_type") == signal_type]
    open_rows = [row for row in rows if row.get("status") in OPEN_STATUSES]
    return {
        "signal_count": len(rows),
        "open_signal_count": len(open_rows),
        "signals": rows,
        "open_signals": open_rows,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--status", help="Filter by status.")
    parser.add_argument("--type", dest="signal_type", help="Filter by signal type.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(json.dumps(collect_signals(status=args.status, signal_type=args.signal_type), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
