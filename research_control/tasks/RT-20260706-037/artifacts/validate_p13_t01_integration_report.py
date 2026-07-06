#!/usr/bin/env python3
"""Validate the v17 P13-T01 integration report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TASK_DIR.parents[2]
REPORT_PATH = TASK_DIR / "artifacts" / "v17_integration_report.md"
REPORT_OUT = TASK_DIR / "artifacts" / "p13_t01_integration_report_validation.json"

REQUIRED_SECTIONS = [
    "Implemented tasks",
    "Deferred tasks",
    "Candidate construction status",
    "Audit and stress status",
    "Accepted-language calibration status",
    "Detector-semantics status",
    "Metric-use ledger status",
    "Upstream-burden status",
    "Proof-normal-form status",
    "Formalization status",
    "Dashboard status",
    "Task-index status",
    "CI status",
    "AI-methodology metrics status",
    "Distance-to-GR effect",
    "Next route candidates",
]

REQUIRED_TOKENS = [
    "Implemented v17 plan tasks after this packet: 54 of 57.",
    "deferred_v17_plan_tasks: 3",
    "P13-T02",
    "P13-T03",
    "P13-T04",
    "no_distance_delta",
    "P13-T01 does not choose among those ordinary route families",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "matter coupling is derived",
    "matter coupling has been derived",
    "einstein equations are derived",
    "einstein equations have been derived",
    "benchmark is promoted",
    "benchmark has been promoted",
    "gate chair verdict is granted",
    "completed derivation is achieved",
    "coupling law is adopted",
    "source law is adopted",
    "g_eff is the physical metric",
]


def validate() -> dict[str, object]:
    errors: list[str] = []
    text = REPORT_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^## {re.escape(section)}$", text, re.MULTILINE):
            errors.append(f"missing required section: {section}")

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"missing required token: {token}")

    for phrase in FORBIDDEN_POSITIVE_CLAIMS:
        if phrase in lower:
            errors.append(f"forbidden positive claim phrase present: {phrase}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "report_path": str(REPORT_PATH.relative_to(REPO_ROOT)),
        "required_section_count": len(REQUIRED_SECTIONS),
        "implemented_v17_plan_tasks": 54,
        "deferred_v17_plan_tasks": 3,
        "next_route": "P13-T02",
        "distance_to_gr_effect": "no_distance_delta",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write_report:
        REPORT_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
