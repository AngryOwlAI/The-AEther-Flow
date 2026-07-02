#!/usr/bin/env python3
"""Validate the v14 P14-T01 coverage audit artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
AUDIT_PATH = "research_control/tasks/RT-20260702-048/artifacts/v14_coverage_audit.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"

RECOMMENDATIONS = [f"V14-R{i:02d}" for i in range(1, 14)]
REQUIRED_STATUSES = [
    "completed_by_v14",
    "implemented_by_existing_tracked_state",
    "implemented_by_later_tracked_state",
    "superseded_by_tracked_state",
    "blocked_by_human_gate",
    "deferred_with_reason",
    "failed_with_repair_task",
    "not_applicable_with_reason",
]
REQUIRED_ACCEPTANCE_MARKERS = [
    "P5-T06 is not ambiguous",
    "Claim-language linter status: implemented and integrated",
    "Validation-status schema status: implemented and validated",
    "Public status-layer propagation status: implemented and validated",
    "External red-team status: implemented and validated",
    "Literature-comparison status: implemented and public-boundary closed",
    "RT-20260701-031",
    "RT-20260702-047",
    "P14-T02 physics-progress metrics report",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def add_check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def validate() -> dict[str, Any]:
    audit = read_text(AUDIT_PATH)
    plan = read_text(PLAN_PATH)
    registry = read_text(REGISTRY_PATH)
    normalized_audit = normalize(audit)
    checks: list[dict[str, Any]] = []

    missing_recommendations = [item for item in RECOMMENDATIONS if item not in audit]
    add_check(
        checks,
        "all_v14_recommendations_mapped",
        not missing_recommendations,
        f"missing_recommendations={missing_recommendations}",
    )
    missing_statuses = [status for status in REQUIRED_STATUSES if status not in audit]
    add_check(
        checks,
        "required_status_vocabulary_present",
        not missing_statuses,
        f"missing_statuses={missing_statuses}",
    )
    missing_markers = [
        marker for marker in REQUIRED_ACCEPTANCE_MARKERS if normalize(marker) not in normalized_audit
    ]
    add_check(
        checks,
        "p14_t01_acceptance_markers_present",
        not missing_markers,
        f"missing_markers={missing_markers}",
    )
    missing_task_ids = [
        task_id
        for task_id in [
            "RT-20260701-031",
            "RT-20260701-037",
            "RT-20260702-002",
            "RT-20260702-007",
            "RT-20260702-028",
            "RT-20260702-033",
            "RT-20260702-047",
        ]
        if task_id not in registry or task_id not in audit
    ]
    add_check(
        checks,
        "required_tracked_task_evidence_present",
        not missing_task_ids,
        f"missing_task_ids={missing_task_ids}",
    )
    add_check(
        checks,
        "plan_contains_p14_t01_acceptance",
        "Every `V14-R01` through `V14-R13`" in plan and "P5-T06 is not left ambiguous" in plan,
        "v14 plan P14-T01 acceptance criteria inspected.",
    )
    add_check(
        checks,
        "downstream_p14_tasks_deferred_not_skipped",
        all(
            marker in audit
            for marker in [
                "| `P14-T02` Physics-progress metrics report | `deferred_with_reason` |",
                "| `P14-T03` Current frontier final refresh | `deferred_with_reason` |",
                "| `P14-T04` V14 final validation | `deferred_with_reason` |",
                "| `P14-T05` Ordinary research continuation handoff | `deferred_with_reason` |",
            ]
        ),
        "P14-T02 through P14-T05 are marked as required downstream packets.",
    )

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "validator_id": "validate_p14_t01_v14_coverage_audit",
        "task_id": "RT-20260702-048",
        "status": status,
        "checks": checks,
        "source_hashes": {
            "audit": digest(AUDIT_PATH),
            "plan": digest(PLAN_PATH),
            "research_task_registry": digest(REGISTRY_PATH),
        },
        "coverage_summary": {
            "recommendations_mapped": 13 - len(missing_recommendations),
            "recommendations_expected": 13,
            "p14_downstream_tasks_pending": ["P14-T02", "P14-T03", "P14-T04", "P14-T05"],
            "next_plan_task_id": "P14-T02",
        },
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
