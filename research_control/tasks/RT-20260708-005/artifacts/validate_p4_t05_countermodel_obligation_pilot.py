#!/usr/bin/env python3
"""Validate v18 P4-T05 countermodel-obligation pilot outputs."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / "registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv"
REPORT_MD = ROOT / "research_control/tasks/RT-20260708-005/artifacts/countermodel_obligation_pilot_report_v1.md"
REPORT_JSON = ROOT / "research_control/tasks/RT-20260708-005/artifacts/p4_t05_countermodel_obligation_pilot_report.json"

REQUIRED_EQSRC_SLOTS = {
    "missing_inverse_countermodel",
    "missing_composition_countermodel",
    "invariant_ledger_not_family_stable_countermodel",
    "target_import_needed_countermodel",
    "RetainH_needed_countermodel",
    "GenH_needed_countermodel",
}

PILOT_LABELS = {
    "not_applicable",
    "attempted",
    "satisfied",
    "deferred_with_reason",
}

FORBIDDEN_PATTERNS = [
    re.compile(
        r"\b(?:local\s+)?countermodel\s+(?:proves|establishes|means|is)\s+"
        r"(?:a\s+)?(?:program-wide|global)\s+no-go\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:local\s+)?countermodel\s+(?:proves|establishes|means)\s+"
        r"(?:future\s+)?source-extension\s+impossible\b",
        re.IGNORECASE,
    ),
]


def read_rows() -> list[dict[str, str]]:
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    rows = read_rows()
    report_text = REPORT_MD.read_text(encoding="utf-8")

    eqsrc_rows = [row for row in rows if row.get("theorem_family") == "eqsrc"]
    observed_slots = {row.get("countermodel_slot", "") for row in eqsrc_rows}
    missing_slots = sorted(REQUIRED_EQSRC_SLOTS - observed_slots)

    deferred_rows = [
        row
        for row in eqsrc_rows
        if row.get("countermodel_slot") == "invariant_ledger_not_family_stable_countermodel"
    ]
    deferred_row_ok = (
        len(deferred_rows) == 1
        and deferred_rows[0].get("status") == "deferred_by_ddr"
        and deferred_rows[0].get("obligation_id") == "CMO-V18-P4T05-EQSRC-INVARIANT-LEDGER-DEFERRED"
        and "DDR-20260708-005" in deferred_rows[0].get("notes", "")
        and (ROOT / deferred_rows[0].get("result_artifact", "")).exists()
        and deferred_rows[0].get("global_no_go_claimed") == "false"
    )

    rows_with_broad_no_go = [
        row.get("obligation_id", "<missing>")
        for row in eqsrc_rows
        if row.get("global_no_go_claimed") != "false"
    ]
    forbidden_hits = [
        pattern.pattern
        for pattern in FORBIDDEN_PATTERNS
        if pattern.search(report_text)
    ]
    labels_present = sorted(label for label in PILOT_LABELS if label in report_text)
    required_report_snippets = {
        "next_route_p4_t06": "next_route: P4-T06" in report_text or "next route is `P4-T06`" in report_text,
        "deferred_reason": "deferred_with_reason" in report_text and "DDR-20260708-005" in report_text,
        "all_slots_table": all(slot in report_text for slot in REQUIRED_EQSRC_SLOTS),
        "no_broad_no_go": "No broad no-go conclusion is claimed" in report_text
        or "No broad no-go is claimed" in report_text,
    }

    status = "PASS"
    if missing_slots or not deferred_row_ok or rows_with_broad_no_go or forbidden_hits:
        status = "FAIL"
    if not all(required_report_snippets.values()):
        status = "FAIL"

    report = {
        "task_id": "RT-20260708-005",
        "plan_task_id": "P4-T05",
        "validator_id": "validate_p4_t05_countermodel_obligation_pilot",
        "status": status,
        "required_eqsrc_slots": sorted(REQUIRED_EQSRC_SLOTS),
        "observed_eqsrc_slots": sorted(observed_slots),
        "missing_eqsrc_slots": missing_slots,
        "deferred_invariant_row_ok": deferred_row_ok,
        "rows_with_broad_no_go": rows_with_broad_no_go,
        "forbidden_overread_hits": forbidden_hits,
        "pilot_labels_present": labels_present,
        "required_report_snippets": required_report_snippets,
        "next_route": "P4-T06",
        "physics_promotion_authorized": False,
        "distance_to_gr_delta": False,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
