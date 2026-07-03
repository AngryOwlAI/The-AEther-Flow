#!/usr/bin/env python3
"""Validate the bounded P5-T02 dependency consequence selector artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "research_control" / "tasks" / "RT-20260703-005"
ARTIFACT = TASK_ROOT / "artifacts" / "dependency_consequence_selector_v1.md"
COMPLETION = TASK_ROOT / "jobs" / "completions" / "AJC-AJ-RT-20260703-005-001.yaml"


REQUIRED_STRINGS = [
    "P6-T01 source-extension classification checklist",
    "| `selected_next_packet_type` | `source_extension_candidate` |",
    "| `selected_next_route_family` | `source_extension_classification` |",
    "Exactly one route is selected",
    "general `EqSrc` not required for the current explicit-certificate theorem scope",
    "P5-T01 explicitly did not trigger freeze",
    "Gate verdict issued | false",
    "This selector changes no Distance-to-GR ledger row",
    "completed derivation",
]

FORBIDDEN_PROMOTION_STRINGS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "matter coupling is derived",
    "Einstein equations are derived",
    "benchmark is promoted",
    "completed derivation is claimed",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks = []

    artifact_text = ARTIFACT.read_text(encoding="utf-8")
    completion_text = COMPLETION.read_text(encoding="utf-8")

    for needle in REQUIRED_STRINGS:
        checks.append(
            {
                "check": f"required:{needle}",
                "status": "PASS" if needle in artifact_text else "FAIL",
            }
        )

    for needle in FORBIDDEN_PROMOTION_STRINGS:
        checks.append(
            {
                "check": f"forbidden:{needle}",
                "status": "FAIL" if needle in artifact_text else "PASS",
            }
        )

    checks.append(
        {
            "check": "completion_theoretical_decision_output",
            "status": "PASS"
            if "theoretical_decision_output:" in completion_text
            and 'selected_next_route_family: "source_extension_classification"'
            in completion_text
            else "FAIL",
        }
    )
    checks.append(
        {
            "check": "completion_next_recommendation",
            "status": "PASS"
            if "Run one bounded v15 P6-T01 source-extension classification checklist packet."
            in completion_text
            else "FAIL",
        }
    )

    failed = [check for check in checks if check["status"] != "PASS"]
    report = {
        "task_id": "RT-20260703-005",
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
