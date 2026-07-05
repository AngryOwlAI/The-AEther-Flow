#!/usr/bin/env python3
"""Validate the v16 recommendation coverage audit table."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EXPECTED_IDS = [f"V16-R{i:02d}" for i in range(1, 16)]
EXPECTED_COLUMNS = [
    "recommendation_id",
    "implemented",
    "status",
    "evidence_path",
    "phase",
    "task",
    "notes",
    "physics_promotion_authorized",
    "next_route_if_partial",
]
ALLOWED_STATUSES = {
    "implemented",
    "implemented_by_later_tracked_state",
    "partially_implemented",
    "deferred_with_reason",
    "blocked_by_human_gate",
    "superseded_by_source_evidence",
    "not_applicable_after_baseline_change",
}


def extract_csv_block(text: str) -> str:
    marker = "```csv"
    start = text.find(marker)
    if start == -1:
        raise ValueError("missing csv fenced block")
    start += len(marker)
    end = text.find("```", start)
    if end == -1:
        raise ValueError("unterminated csv fenced block")
    return text[start:end].strip()


def validate(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    csv_text = extract_csv_block(path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    columns = list(rows[0].keys()) if rows else []

    if columns != EXPECTED_COLUMNS:
        errors.append(f"columns mismatch: {columns}")

    seen = [row.get("recommendation_id", "") for row in rows]
    for recommendation_id in EXPECTED_IDS:
        if recommendation_id not in seen:
            errors.append(f"missing recommendation_id {recommendation_id}")
    for recommendation_id in seen:
        if recommendation_id not in EXPECTED_IDS:
            errors.append(f"unexpected recommendation_id {recommendation_id}")
    if len(seen) != len(set(seen)):
        errors.append("duplicate recommendation_id present")

    for row in rows:
        rid = row.get("recommendation_id", "<missing>")
        for column in EXPECTED_COLUMNS:
            if not row.get(column, "").strip():
                errors.append(f"{rid}: blank column {column}")
        if row.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{rid}: invalid status {row.get('status')}")
        if row.get("physics_promotion_authorized") != "false":
            errors.append(f"{rid}: physics_promotion_authorized must be false")
        if row.get("implemented") != "true":
            errors.append(f"{rid}: implemented must be true for final v16 audit")
        if row.get("status") in {"partially_implemented", "deferred_with_reason"}:
            if row.get("next_route_if_partial") == "not_applicable":
                errors.append(f"{rid}: partial or deferred row needs exact next route")
        for raw_path in row.get("evidence_path", "").split(";"):
            evidence_path = raw_path.strip()
            if not evidence_path:
                errors.append(f"{rid}: empty evidence path")
                continue
            if not (ROOT / evidence_path).exists():
                errors.append(f"{rid}: missing evidence path {evidence_path}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "row_count": len(rows),
        "expected_row_count": len(EXPECTED_IDS),
        "implemented_count": sum(1 for row in rows if row.get("implemented") == "true"),
        "physics_promotion_authorized_count": sum(
            1 for row in rows if row.get("physics_promotion_authorized") == "true"
        ),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit",
        default="research_control/tasks/RT-20260705-039/artifacts/v16_recommendation_coverage_audit.md",
    )
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(ROOT / args.audit)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
