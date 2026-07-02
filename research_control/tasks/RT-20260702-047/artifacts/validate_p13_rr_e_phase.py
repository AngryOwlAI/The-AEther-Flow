#!/usr/bin/env python3
"""Validate v14 P13 RR_E separation phase controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]


PATHS = {
    "plan": "implementations_plans/recommendations_implementation_plan_continue_task-v14.md",
    "boundary": "research_control/design/rr_e_separation_boundary_control_note.md",
    "checklist": "research_control/design/rr_e_allowed_identification_checklist.md",
    "taxonomy": "research_control/design/claim_language_linter_taxonomy.yaml",
    "examples": "research_control/design/scoped_claim_language_examples.md",
    "fixture": "tests/fixtures/claim_language/rr_e_overread.md",
    "inventory": "research_control/design/frontier_theorem_inventory.md",
    "p13_t01_report": "research_control/tasks/RT-20260702-043/artifacts/p13_t01_rr_e_boundary_report.json",
    "p13_t02_report": "research_control/tasks/RT-20260702-044/artifacts/p13_t02_rr_e_checklist_report.json",
    "p13_t03_report": "research_control/tasks/RT-20260702-045/artifacts/p13_t03_rr_e_fixtures_report.json",
    "p13_t04_report": "research_control/tasks/RT-20260702-046/artifacts/p13_t04_rr_e_inventory_crosslinks_report.json",
    "handoff_0499": "research_control/handoffs/handoff-0499.yaml",
}


REQUIRED_RULE = (
    "RR_E records may be identified only under explicit source transport, "
    "source invariance, or source factorization certificates for a declared "
    "object. Otherwise separation or obstruction is preserved."
)


CHECKLIST_QUESTIONS = [
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


FIXTURE_LINES = [
    "same-support different-RR_E records identified without certificate.",
    "RR_E identified without source transport certificate.",
    "RR_E identified without source invariance certificate.",
    "RR_E identified without source factorization certificate.",
    "RR_E collapses by detector semantics.",
    "g_eff collapses RR_E.",
    "benchmark behavior collapses RR_E.",
    "process authority collapses RR_E.",
    "support-only formalization collapses RR_E.",
    "RR_ETransportCompletenessOrInvarianceLaw_v1 adopted.",
    "scoped RR_E evidence/precondition adopts source law.",
    "RR_E support formalization proves source law adoption.",
]


INVENTORY_MARKERS = [
    "P13-T04 `RR_E` crosslink receipt:",
    "`PositiveMSProfile_v1` links to `RR_E` separation/transport boundary",
    "`SourceMatterSemanticsAdoptionReadinessLaw_v1` links to `RR_E` non-collapse pressure",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1` links to obstruction and certificate-indexed scope",
    "no inventory item may erase `RR_E` separation without a declared object plus source transport",
    "Missing certificate data preserves separation or obstruction",
]


CLAIM_BOUNDARY_MARKERS = [
    "unrestricted RR_E irrelevance remains unproved",
    "not source-law adoption",
    "not unrestricted RR_E irrelevance",
    "not downstream physics promotion",
    "RR_ETransportCompletenessOrInvarianceLaw_v1 source-law overclaim",
    "Unrestricted RR_E irrelevance overclaim",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("`", "")).strip()


def status_pass(report_path: str) -> bool:
    report = read_json(report_path)
    return report.get("status") == "PASS" and not report.get("errors")


def add_check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    plan = read_text(PATHS["plan"])
    boundary = read_text(PATHS["boundary"])
    checklist = read_text(PATHS["checklist"])
    taxonomy = read_text(PATHS["taxonomy"])
    examples = read_text(PATHS["examples"])
    fixture = read_text(PATHS["fixture"])
    inventory = read_text(PATHS["inventory"])
    handoff = read_text(PATHS["handoff_0499"])
    normalized_boundary = normalize(boundary)
    normalized_inventory = normalize(inventory)
    normalized_taxonomy = normalize(taxonomy)
    normalized_examples = normalize(examples)

    add_check(
        checks,
        "plan_routes_p13_t05_to_p14_t01",
        "P13-T05" in plan and "P14-T01" in plan and "V14 coverage audit" in plan,
        "v14 plan contains the P13-T05 phase validation and downstream P14-T01 coverage audit route.",
    )
    add_check(
        checks,
        "p13_t01_report_pass",
        status_pass(PATHS["p13_t01_report"]),
        "P13-T01 boundary note validator report is PASS.",
    )
    add_check(
        checks,
        "p13_t02_report_pass",
        status_pass(PATHS["p13_t02_report"]),
        "P13-T02 checklist validator report is PASS.",
    )
    add_check(
        checks,
        "p13_t03_report_pass",
        status_pass(PATHS["p13_t03_report"]),
        "P13-T03 RR_E fixture validator report is PASS.",
    )
    add_check(
        checks,
        "p13_t04_report_pass",
        status_pass(PATHS["p13_t04_report"]),
        "P13-T04 inventory crosslink validator report is PASS.",
    )
    add_check(
        checks,
        "required_rule_present",
        normalize(REQUIRED_RULE) in normalized_boundary,
        "P13-T01 boundary note preserves the required explicit-certificate rule.",
    )
    missing_questions = [q for q in CHECKLIST_QUESTIONS if q not in checklist]
    add_check(
        checks,
        "checklist_questions_complete",
        not missing_questions,
        f"missing_questions={missing_questions}",
    )
    missing_fixture_lines = [line for line in FIXTURE_LINES if line not in fixture]
    add_check(
        checks,
        "rr_e_overread_fixture_complete",
        not missing_fixture_lines,
        f"missing_fixture_lines={missing_fixture_lines}",
    )
    missing_inventory_markers = [
        marker for marker in INVENTORY_MARKERS if normalize(marker) not in normalized_inventory
    ]
    add_check(
        checks,
        "inventory_crosslink_receipt_present",
        not missing_inventory_markers,
        f"missing_inventory_markers={missing_inventory_markers}",
    )
    missing_claim_markers = [
        marker
        for marker in CLAIM_BOUNDARY_MARKERS
        if normalize(marker) not in normalized_taxonomy and normalize(marker) not in normalized_examples
    ]
    add_check(
        checks,
        "claim_language_controls_preserve_rr_e_boundary",
        not missing_claim_markers,
        f"missing_claim_boundary_markers={missing_claim_markers}",
    )
    add_check(
        checks,
        "handoff_0499_routes_to_p13_t05",
        "Run one bounded v14 P13-T05 RR_E separation phase validation packet." in handoff,
        "handoff-0499 routes to P13-T05.",
    )

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "validator_id": "validate_p13_rr_e_phase",
        "task_id": "RT-20260702-047",
        "status": status,
        "checks": checks,
        "source_hashes": {name: digest(path) for name, path in PATHS.items()},
        "claim_boundary": {
            "proof_authority": False,
            "source_law_adoption_authorized": False,
            "rr_e_transport_law_adoption_authorized": False,
            "unrestricted_rr_e_irrelevance_authorized": False,
            "matter_semantics_adoption_authorized": False,
            "detector_semantics_adoption_authorized": False,
            "downstream_physics_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
        "phase_result": {
            "p13_validated": status == "PASS",
            "next_plan_task_id": "P14-T01",
            "next_route": "v14 coverage audit",
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
