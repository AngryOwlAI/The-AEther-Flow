#!/usr/bin/env python3
"""Validate the v15 P10-T02 route-orbit extractor pilot output."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-03T15:07:00Z"
SCRIPT_PATH = "scripts/research_control/extract_route_signatures.py"
TEST_PATH = "tests/test_route_signature_extractor.py"
PILOT_REPORT_PATH = (
    "research_control/tasks/RT-20260703-018/artifacts/"
    "p10_t02_route_signature_pilot_report.json"
)
RECEIPT_PATH = (
    "research_control/tasks/RT-20260703-018/artifacts/"
    "p10_t02_route_orbit_extractor_pilot_receipt.md"
)
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v15.md"

REQUIRED_REPORT_KEYS = [
    "route_signature_count",
    "repeated_burden_cycle_count",
    "repeated_no_new_payload_cycle_count",
    "no_new_mathematical_payload_tasks",
    "route_orbit_warning_should_emit",
    "suggested_freeze_or_continuation_consequence",
    "pilot_blocks_research",
    "advisory_only",
]

REQUIRED_SIGNATURE_FIELDS = [
    "target_derivation_milestone",
    "milestone_burden",
    "object_or_claim_name",
    "route_family",
    "role_family",
    "mathematical_payload_class",
    "distance_to_gr_delta",
    "source_extension_classification",
    "obstruction_id",
    "freeze_criteria_status",
    "next_route_selected",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    return json.loads(read_text(path))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(
    script_hash: str,
    test_hash: str,
    pilot_report_hash: str,
    plan_hash: str,
    pilot_report: dict[str, Any],
) -> str:
    no_payload_tasks = "\n".join(
        f"- `{task['task_id']}`: `{task['mathematical_payload_class']}` via `{task['route_family']}`"
        for task in pilot_report["no_new_mathematical_payload_tasks"]
    )
    receipt = f"""<!-- authority: control -->

# P10-T02 Route-Orbit Extractor Pilot Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. The v15 extractor produced a route signature report for recent
`matter_coupling` tasks, counted repeated burden cycles, listed tasks with no
new mathematical payload, and recorded the advisory continuation consequence.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{SCRIPT_PATH}` | `{script_hash}` |
| `{TEST_PATH}` | `{test_hash}` |
| `{PILOT_REPORT_PATH}` | `{pilot_report_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |

## Pilot Summary

| Field | Value |
| --- | --- |
| Route signatures | `{pilot_report['route_signature_count']}` |
| Repeated burden cycles | `{pilot_report['repeated_burden_cycle_count']}` |
| Repeated no-new-payload cycles | `{pilot_report['repeated_no_new_payload_cycle_count']}` |
| Route-orbit warning should emit | `{pilot_report['route_orbit_warning_should_emit']}` |
| Pilot blocks research | `{pilot_report['pilot_blocks_research']}` |
| Suggested consequence | `{pilot_report['suggested_freeze_or_continuation_consequence']}` |

## No-New-Payload Tasks

{no_payload_tasks}

## Boundary

The pilot is advisory-only. It does not freeze a route, block research by
itself, adopt a source law, derive matter coupling, derive Einstein equations,
promote a benchmark, issue a Gate Chair verdict, claim completed derivation,
authorize a global no-go conclusion, or authorize future source-extension
impossibility.

## Next Route

P10-T03 should define the freeze threshold policy for when repeated burden
cycles require freeze review.
"""
    receipt_path = REPO_ROOT / RECEIPT_PATH
    receipt_path.write_text(receipt, encoding="utf-8")
    return sha256_text(receipt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    script_text = read_text(SCRIPT_PATH)
    test_text = read_text(TEST_PATH)
    plan_text = read_text(PLAN_PATH)
    pilot_report_text = read_text(PILOT_REPORT_PATH)
    pilot_report = json.loads(pilot_report_text)

    errors: list[str] = []
    if "P10-T02" not in plan_text or "route_orbit_extractor_pilot" not in plan_text:
        errors.append(f"{PLAN_PATH} no longer contains the P10-T02 route-orbit extractor task")
    if "route_signature_schema_v1" not in script_text:
        errors.append(f"{SCRIPT_PATH} does not reference route_signature_schema_v1")
    if "RouteSignatureExtractorTests" not in test_text:
        errors.append(f"{TEST_PATH} missing focused route signature extractor tests")
    for key in REQUIRED_REPORT_KEYS:
        if key not in pilot_report:
            errors.append(f"{PILOT_REPORT_PATH} missing report key: {key}")
    if pilot_report.get("schema_id") != "route_signature_pilot_report_v1":
        errors.append(f"{PILOT_REPORT_PATH} has wrong schema_id")
    if pilot_report.get("signature_schema_id") != "route_signature_schema_v1":
        errors.append(f"{PILOT_REPORT_PATH} has wrong signature_schema_id")
    if pilot_report.get("task_count") != 23:
        errors.append(f"{PILOT_REPORT_PATH} expected 23 recent matter-coupling tasks")
    if pilot_report.get("route_signature_count") != 23:
        errors.append(f"{PILOT_REPORT_PATH} expected 23 route signatures")
    if pilot_report.get("pilot_blocks_research") is not False:
        errors.append(f"{PILOT_REPORT_PATH} must keep pilot_blocks_research false")
    if pilot_report.get("advisory_only") is not True:
        errors.append(f"{PILOT_REPORT_PATH} must be advisory_only")
    if not isinstance(pilot_report.get("repeated_burden_cycle_count"), int):
        errors.append(f"{PILOT_REPORT_PATH} repeated_burden_cycle_count must be an int")
    if not isinstance(pilot_report.get("repeated_no_new_payload_cycle_count"), int):
        errors.append(f"{PILOT_REPORT_PATH} repeated_no_new_payload_cycle_count must be an int")
    if pilot_report.get("route_orbit_warning_should_emit") is not False:
        errors.append(f"{PILOT_REPORT_PATH} expected route_orbit_warning_should_emit false for this pilot")
    if (
        pilot_report.get("suggested_freeze_or_continuation_consequence")
        != "no_freeze_from_pilot_continue_to_p10_t03_freeze_threshold_policy"
    ):
        errors.append(f"{PILOT_REPORT_PATH} has unexpected continuation consequence")

    signatures = pilot_report.get("route_signatures", [])
    if not isinstance(signatures, list) or not signatures:
        errors.append(f"{PILOT_REPORT_PATH} missing route signatures")
    else:
        for index, signature in enumerate(signatures):
            for field in REQUIRED_SIGNATURE_FIELDS:
                if field not in signature:
                    errors.append(f"{PILOT_REPORT_PATH} signature {index} missing {field}")

    no_payload_ids = {
        task.get("task_id", "")
        for task in pilot_report.get("no_new_mathematical_payload_tasks", [])
        if isinstance(task, dict)
    }
    for task_id in ("RT-20260701-010", "RT-20260701-021", "RT-20260701-031"):
        if task_id not in no_payload_ids:
            errors.append(f"{PILOT_REPORT_PATH} missing expected no-new-payload task {task_id}")

    claim_boundary = pilot_report.get("claim_boundary", {})
    for field in (
        "route_freeze_authorized",
        "physics_promotion_authorized",
        "source_law_adoption_authorized",
        "completed_derivation_authorized",
    ):
        if claim_boundary.get(field) is not False:
            errors.append(f"{PILOT_REPORT_PATH} claim_boundary.{field} must be false")

    script_hash = sha256_text(script_text)
    test_hash = sha256_text(test_text)
    pilot_report_hash = sha256_text(pilot_report_text)
    plan_hash = sha256_text(plan_text)
    receipt_hash = ""
    if not errors:
        receipt_hash = write_receipt(
            script_hash=script_hash,
            test_hash=test_hash,
            pilot_report_hash=pilot_report_hash,
            plan_hash=plan_hash,
            pilot_report=pilot_report,
        )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "generated_at": GENERATED_AT,
        "script_path": SCRIPT_PATH,
        "script_hash": script_hash,
        "test_path": TEST_PATH,
        "test_hash": test_hash,
        "pilot_report_path": PILOT_REPORT_PATH,
        "pilot_report_hash": pilot_report_hash,
        "plan_path": PLAN_PATH,
        "plan_hash": plan_hash,
        "route_signature_count": pilot_report.get("route_signature_count", 0),
        "repeated_burden_cycle_count": pilot_report.get("repeated_burden_cycle_count", 0),
        "repeated_no_new_payload_cycle_count": pilot_report.get("repeated_no_new_payload_cycle_count", 0),
        "route_orbit_warning_should_emit": pilot_report.get("route_orbit_warning_should_emit"),
        "suggested_freeze_or_continuation_consequence": pilot_report.get(
            "suggested_freeze_or_continuation_consequence", ""
        ),
        "receipt_path": RECEIPT_PATH if not errors else "",
        "receipt_hash": receipt_hash,
        "errors": errors,
    }
    output_path = REPO_ROOT / args.output
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
