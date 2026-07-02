#!/usr/bin/env python3
"""Validate the bounded P13-T02 RR_E allowed-identification checklist packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DOC_PATH = "research_control/design/rr_e_allowed_identification_checklist.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
HANDOFF_PATH = "research_control/handoffs/handoff-0497.yaml"

REQUIRED_QUESTIONS = [
    "What declared object `F` or source object is under review?",
    "Which exact `RR_E` records are being identified or compared?",
    "Is there a source transport certificate?",
    "Is there a source invariance certificate?",
    "Is there a source factorization certificate?",
    "Are certificates declared-object indexed?",
    "Are certificates source-side and no-target-import audited?",
    "Does missing certificate fail closed?",
    "Is detector semantics being smuggled?",
    "Is `g_eff` or `MetricData(E)` being imported?",
    "Is benchmark behavior being imported?",
    "Does the result claim unrestricted irrelevance?",
    "What separation or obstruction remains?",
]

REQUIRED_FLAGS = [
    "requires_declared_object_or_source_object: true",
    "requires_exact_rr_e_records: true",
    "allows_source_transport_certificate: true",
    "allows_source_invariance_certificate: true",
    "allows_source_factorization_certificate: true",
    "requires_declared_object_indexing: true",
    "requires_source_side_no_target_import_audit: true",
    "missing_certificate_fails_closed: true",
    "detector_semantics_identification_pressure_forbidden: true",
    "g_eff_or_metricdata_e_identification_pressure_forbidden: true",
    "benchmark_behavior_identification_pressure_forbidden: true",
    "unrestricted_irrelevance_claim_requires_certificate_indexed_source_support: true",
    "remaining_separation_or_obstruction_required: true",
    "no_physics_promotion_authorized: true",
    'next_required_packet: "P13-T03 RR_E test fixtures for linter/support formalization"',
]


def digest(rel: str) -> str:
    return hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()


def load_handoff_task_type() -> str:
    text = (REPO_ROOT / HANDOFF_PATH).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("task_type:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def validate() -> dict[str, object]:
    errors: list[str] = []
    doc = (REPO_ROOT / DOC_PATH).read_text(encoding="utf-8")

    missing_questions = [item for item in REQUIRED_QUESTIONS if item not in doc]
    if missing_questions:
        errors.append(f"missing checklist questions: {missing_questions}")

    missing_flags = [item for item in REQUIRED_FLAGS if item not in doc]
    if missing_flags:
        errors.append(f"missing machine flags: {missing_flags}")

    for required in [
        "Fail-closed means separation or obstruction is preserved.",
        "does not adopt a source law",
        "prove unrestricted `RR_E` irrelevance",
        "promote any downstream physics claim",
    ]:
        if required not in doc:
            errors.append(f"missing boundary phrase: {required}")

    if load_handoff_task_type() != "v14_p13_t03_rr_e_test_fixtures_linter_support":
        errors.append("handoff-0497 must route to P13-T03 RR_E test fixtures")

    return {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260702-044",
        "validator_id": "validate_p13_t02_rr_e_checklist",
        "doc_path": DOC_PATH,
        "doc_hash": digest(DOC_PATH),
        "plan_path": PLAN_PATH,
        "plan_hash": digest(PLAN_PATH),
        "required_question_count": len(REQUIRED_QUESTIONS),
        "machine_flag_count": len(REQUIRED_FLAGS),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
