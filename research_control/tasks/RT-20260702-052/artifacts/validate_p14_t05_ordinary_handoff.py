#!/usr/bin/env python3
"""Validate v14 P14-T05 ordinary continuation handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260702-052"

PATHS = {
    "task": "research_control/tasks/RT-20260702-052/00_TASK.yaml",
    "decision": "research_control/tasks/RT-20260702-052/DDR-20260702-052.md",
    "handoff_report": "research_control/tasks/RT-20260702-052/artifacts/p14_t05_ordinary_research_continuation_handoff.md",
    "completion": "research_control/tasks/RT-20260702-052/jobs/completions/AJC-AJ-RT-20260702-052-001.yaml",
    "handoff": "research_control/handoffs/handoff-0505.yaml",
    "program_state": "research_control/program_state.yaml",
    "current_frontier": "research_control/current_frontier.md",
    "ledger": "registries/DISTANCE_TO_GR_LEDGER.csv",
    "plan": "implementations_plans/recommendations_implementation_plan_continue_task-v14.md",
}

REQUIRED_REPORT_MARKERS = [
    "V14 is completed through P14-T05.",
    "Active Scientific Frontier",
    "Current Distance-To-GR State",
    "Current Adopted Objects",
    "Current Accepted Evidence And Preconditions",
    "Current Open Or Blocked Physical Targets",
    "RR_E Separation Status",
    "No-Target Certificate Hygiene Status",
    "Selected Ordinary Next Route",
    "No project-improvement sidecar exists",
    "does not authorize source-law adoption",
]

FORBIDDEN_OVERREAD_MARKERS = [
    "direct universal matter-coupling derivation",
    "Einstein-equation derivation",
    "benchmark promotion",
    "completed derivation routes remain forbidden",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def add_check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def flat_text(text: str) -> str:
    return " ".join(text.split())


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    task = read_text(PATHS["task"])
    decision = read_text(PATHS["decision"])
    report = read_text(PATHS["handoff_report"])
    completion = read_text(PATHS["completion"])
    handoff = read_text(PATHS["handoff"])
    program_state = read_text(PATHS["program_state"])
    current_frontier = read_text(PATHS["current_frontier"])
    ledger = read_text(PATHS["ledger"])
    plan = read_text(PATHS["plan"])
    flat_report = flat_text(report)
    lower_report = flat_report.lower()
    lower_plan = flat_text(plan).lower()

    selected_route = "narrow_source_side_matter_semantics_equivalence_theorem_under_explicit_certificates"
    selected_route_phrase = "narrow source-side matter-semantics equivalence theorem under explicit source certificates"
    add_check(
        checks,
        "plan_contains_p14_t05",
        "P14-T05: Ordinary research continuation handoff" in plan
        and "Candidate ordinary next routes after v14" in plan,
        "v14 plan contains P14-T05 and the candidate route list.",
    )
    add_check(
        checks,
        "exactly_one_selected_route",
        selected_route in task
        and selected_route in completion
        and selected_route in handoff
        and selected_route_phrase in program_state,
        "the same selected route appears in task completion handoff and program state.",
    )
    add_check(
        checks,
        "selected_route_is_candidate_one",
        "narrow source-side matter-semantics equivalence theorem under explicit certificates" in decision
        and "selected_from_candidate_number: 1" in completion,
        "selected route is candidate 1 from the P14-T05 list.",
    )
    missing_report_markers = [marker for marker in REQUIRED_REPORT_MARKERS if marker not in report]
    add_check(
        checks,
        "handoff_report_has_required_fields",
        not missing_report_markers,
        f"missing_report_markers={missing_report_markers}",
    )
    add_check(
        checks,
        "rr_e_separation_preserved",
        "Missing certificates fail closed" in report
        and "does not prove unrestricted `RR_E`" in report,
        "RR_E separation and fail-closed certificate status are explicit.",
    )
    add_check(
        checks,
        "no_target_hygiene_preserved",
        "No-target certificate hygiene remains active" in report
        and "Target-side detector semantics" in report,
        "no-target certificate hygiene is explicit.",
    )
    add_check(
        checks,
        "frontier_and_ledger_support_summary",
        "M_src" in current_frontier
        and "g_eff" in current_frontier
        and "matter_coupling" in ledger
        and "accepted_as_scoped_evidence_precondition" in ledger,
        "current frontier and ledger support the adopted/evidence summary.",
    )
    add_check(
        checks,
        "handoff_next_action_matches_selected_route",
        "Run one bounded post-v14 ontology-formalizer packet" in handoff
        and selected_route in handoff,
        "handoff-0505 routes to the selected post-v14 packet.",
    )
    add_check(
        checks,
        "v14_all_phases_completed",
        "v14_all_phases_completed: true" in completion
        and "all_applicable_plan_tasks_proven: true" in completion,
        "completion records v14 completion.",
    )
    add_check(
        checks,
        "no_physics_promotion",
        "downstream_physics_promotion_authorized: false" in completion
        and "completed_derivation_authorized: false" in completion
        and "matter-coupling derivation or adoption" in lower_report,
        "completion and report preserve no physics promotion.",
    )
    add_check(
        checks,
        "forbidden_direct_routes_still_blocked",
        all(marker.lower() in lower_report or marker.lower() in lower_plan for marker in FORBIDDEN_OVERREAD_MARKERS),
        "direct matter-coupling Einstein-equation benchmark and completed-derivation routes remain blocked.",
    )

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "validator_id": "validate_p14_t05_ordinary_handoff",
        "task_id": TASK_ID,
        "status": status,
        "checks": checks,
        "source_hashes": {name: digest(path) for name, path in PATHS.items()},
        "selected_next_route": selected_route,
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
            "p14_t05_validated": status == "PASS",
            "v14_all_phases_completed": status == "PASS",
            "next_route": selected_route,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    output_path = ROOT / args.output
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
