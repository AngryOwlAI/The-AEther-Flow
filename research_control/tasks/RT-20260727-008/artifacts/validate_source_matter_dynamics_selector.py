#!/usr/bin/env python3
"""Validate the bounded P7-T02 source-matter dynamics packet selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260727-008"
ART = TASK / "artifacts"
REPORT = ART / "source_matter_dynamics_selector_validation_v1.json"
COMPACT = ART / "source_matter_dynamics_selector_compact_receipt_v1.json"

SOURCE_HASHES = {
    "research_control/handoffs/handoff-0889.yaml": (
        "5dabdb01ed339a3e276e42420c15f3700b37db58fd8a07d923ef8d65197607b8"
    ),
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_and_sector_taxonomy_v1.tex": (
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d"
    ),
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_spec_v1.yaml": (
        "a5563edddaff90ebab6ac4d3d4e2dc0425fea23b5f27c1c6174cb28b1f4652be"
    ),
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_sector_charge_taxonomy_v1.yaml": (
        "0b7bb06a63b20469185badab4b2664eaa23d5b4e47752b953d51c2508f283c59"
    ),
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_assumption_dependency_table_v1.yaml": (
        "c665dbc7522d4ee1b6aa01db14100689c8d9acc28c7e659c33b4272d32976991"
    ),
    "research_control/tasks/RT-20260727-007/jobs/completions/"
    "AJC-AJ-RT-20260727-007-001.yaml": (
        "4d1fc3d7d045defa6000dc0860973fba50280ddd1ee72cb4881d8ee2de2ddc1c"
    ),
}

CHILD_PATHS = {
    "child_phys_math": ART
    / "child_phys_math_p7_t02_source_matter_dynamics_selector.yaml",
    "child_phys_phil": ART
    / "child_phys_phil_p7_t02_source_matter_dynamics_selector.yaml",
}

REQUIRED_AUTHORITY_FLAGS = {
    "canonical_ontology_modified": False,
    "source_law_adopted": False,
    "matter_ontology_adopted": False,
    "selected_dynamics_executed_here": False,
    "physical_time_established": False,
    "physical_probability_established": False,
    "physical_conservation_law_established": False,
    "detector_semantics_established": False,
    "effective_geometry_assumed": False,
    "matter_action_established": False,
    "stress_energy_established": False,
    "matter_coupling_derived": False,
    "einstein_equations_derived": False,
    "benchmark_promotion_authorized": False,
    "physics_promotion_authorized": False,
    "proof_authority": False,
    "publication_authorized": False,
    "push_performed": False,
    "global_no_go_claimed": False,
    "future_source_extension_impossibility_claimed": False,
    "completed_derivation_claimed": False,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} did not contain a mapping")
    return value


def string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def add_check(
    checks: list[dict[str, Any]], check_id: str, ok: bool, detail: str
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    selection = load_yaml(ART / "source_matter_dynamics_packet_selection_v1.yaml")
    conflict = load_yaml(
        ART / "parent_conflict_review_p7_t02_source_matter_dynamics_selector.yaml"
    )
    task = load_yaml(TASK / "00_TASK.yaml")
    job = load_yaml(TASK / "jobs/AJ-RT-20260727-008-001.yaml")
    children = {name: load_yaml(path) for name, path in CHILD_PATHS.items()}

    add_check(
        checks,
        "selection_identity",
        selection.get("schema_id")
        == "source_matter_dynamics_packet_selection_v1"
        and selection.get("task_id") == "RT-20260727-008"
        and selection.get("status") == "draft/control",
        "The fused selector artifact has the exact task-local identity and status.",
    )
    add_check(
        checks,
        "fixed_candidate",
        selection.get("fixed_basis", {}).get("candidate_id")
        == "SourceMatterIncidenceCandidate_v1"
        and selection.get("fixed_basis", {}).get("candidate_status")
        == "proposal-only",
        "The P7-T01 proposal-only candidate remains the fixed comparison basis.",
    )
    add_check(
        checks,
        "kinematics_not_dynamics",
        selection.get("fixed_basis", {}).get("dynamics_selected") is False
        and selection.get("fixed_basis", {}).get("action_defined") is False,
        "P7-T01 transition admissibility is not reclassified as dynamics or action.",
    )

    comparisons = selection.get("branch_comparison")
    comparisons = comparisons if isinstance(comparisons, list) else []
    branch_ids = {str(row.get("branch_id", "")).strip() for row in comparisons}
    add_check(
        checks,
        "three_branch_coverage",
        branch_ids
        == {"source_action", "source_evolution_equation", "source_transition_law"},
        "Action, evolution-equation, and transition-law branches are each compared once.",
    )
    for row in comparisons:
        branch_id = str(row.get("branch_id", "")).strip() or "missing"
        add_check(
            checks,
            f"branch_assumptions:{branch_id}",
            len(string_list(row.get("minimum_added_primitives"))) >= 2,
            f"{branch_id} names at least two exact added primitives.",
        )
        add_check(
            checks,
            f"branch_constraint_target:{branch_id}",
            bool(str(row.get("conserved_or_constraint_target", "")).strip()),
            f"{branch_id} names a future conserved or constraint target.",
        )
        add_check(
            checks,
            f"branch_target_import:{branch_id}",
            bool(str(row.get("target_import_risk", "")).strip())
            and row.get("target_import_required") is False,
            f"{branch_id} names import risk while requiring no target import.",
        )
        add_check(
            checks,
            f"branch_not_executed:{branch_id}",
            row.get("executed_here") is False,
            f"{branch_id} remains unexecuted in the selector.",
        )

    recommendation = selection.get("recommendation")
    recommendation = recommendation if isinstance(recommendation, dict) else {}
    add_check(
        checks,
        "selected_branch",
        recommendation.get("selected_branch") == "source_transition_law",
        "Exactly the source-transition-law branch is selected.",
    )
    add_check(
        checks,
        "selected_packet_type",
        recommendation.get("selected_next_packet_type")
        == "ontology_law_research_packet",
        "The selected theoretical packet type is ontology_law_research_packet.",
    )
    add_check(
        checks,
        "selected_route_and_role",
        recommendation.get("selected_next_route_family")
        == "ontology-law-research-packet"
        and recommendation.get("selected_next_role_family")
        == "candidate-constructor@0.2.0",
        "The future route and execution-role family are exact.",
    )
    add_check(
        checks,
        "future_candidate_identity",
        recommendation.get("proposed_future_candidate_id")
        == "SourceMatterFiniteTransitionKernelCandidate_v1",
        "The future proposal-only transition-kernel candidate has one stable identity.",
    )
    add_check(
        checks,
        "future_assumption_budget",
        len(string_list(recommendation.get("minimum_future_assumptions"))) >= 5,
        "The future packet names at least five explicit source-side assumptions.",
    )
    add_check(
        checks,
        "future_deliverables",
        len(string_list(recommendation.get("future_mathematical_deliverables")))
        >= 5,
        "The future packet names at least five mathematical deliverables.",
    )
    add_check(
        checks,
        "future_controls",
        len(string_list(recommendation.get("positive_and_degenerate_controls")))
        >= 4,
        "The future packet requires positive, null, interacting, and degenerate controls.",
    )
    add_check(
        checks,
        "selector_only",
        recommendation.get("selected_dynamics_executed_here") is False
        and selection.get("selected_dynamics_packet_executed_here") is False,
        "The selected dynamics packet is not executed in this task.",
    )
    add_check(
        checks,
        "claim_blocks",
        recommendation.get("preserves_claim_blocks") is True,
        "The recommendation explicitly preserves claim blocks.",
    )

    ontology_packet = selection.get("ontology_law_research_packet")
    ontology_packet = ontology_packet if isinstance(ontology_packet, dict) else {}
    add_check(
        checks,
        "ontology_route_trigger",
        ontology_packet.get("route") == "ontology-law-research-packet"
        and ontology_packet.get("trigger_classification")
        == "derivation_critical_missing_source_law",
        "The ontology-law route is used only for a derivation-critical missing transition law.",
    )
    adoption = ontology_packet.get("adoption_status")
    adoption = adoption if isinstance(adoption, dict) else {}
    add_check(
        checks,
        "open_continuation_status",
        adoption.get("status_pair") == "blocked_adoption_open_continuation"
        and adoption.get("current_adoption") == "blocked"
        and adoption.get("continuation") == "open",
        "Current adoption is blocked while same-milestone continuation remains open.",
    )
    add_check(
        checks,
        "no_go_boundary",
        ontology_packet.get("no_go_theorem_status") == "not_proved",
        "No global or local impossibility theorem is inferred from underdetermination.",
    )

    add_check(
        checks,
        "conflict_review",
        conflict.get("status") == "PASS"
        and conflict.get("unresolved_blocking_conflict_count") == 0
        and conflict.get("selected_branch") == "source_transition_law",
        "The parent conflict review resolves the child analyses with zero blockers.",
    )
    for child_name, child in children.items():
        child_rec = child.get("recommendation")
        child_rec = child_rec if isinstance(child_rec, dict) else {}
        add_check(
            checks,
            f"child_selection:{child_name}",
            child_rec.get("selected_branch") == "source_transition_law"
            and child_rec.get("selected_dynamics_executed_here") is False,
            f"{child_name} independently selects the unexecuted transition-law branch.",
        )

    decomposition = job.get("role_decomposition")
    decomposition = decomposition if isinstance(decomposition, dict) else {}
    child_rows = decomposition.get("children")
    child_rows = child_rows if isinstance(child_rows, list) else []
    add_check(
        checks,
        "parent_child_contract",
        decomposition.get("mode") == "parent_child_parallel_synthesis"
        and len(child_rows) == 2
        and all(row.get("status") == "completed" for row in child_rows),
        "The one outer AgentJob records two completed internal child units.",
    )

    authority = selection.get("authority_flags")
    authority = authority if isinstance(authority, dict) else {}
    for field_name, expected in REQUIRED_AUTHORITY_FLAGS.items():
        add_check(
            checks,
            f"authority:{field_name}",
            authority.get(field_name) is expected,
            f"authority_flags.{field_name} is {str(expected).lower()}.",
        )

    add_check(
        checks,
        "task_boundary",
        task.get("claim_boundary_id")
        == "CB-V21-P7-T02-SOURCE-MATTER-DYNAMICS-SELECTOR-001"
        and task.get("plan_task_id") == "P7-T02",
        "The task is bound to the exact P7-T02 selector claim boundary.",
    )
    for relative, expected_hash in SOURCE_HASHES.items():
        source = ROOT / relative
        add_check(
            checks,
            f"source_hash:{relative}",
            source.is_file() and digest(source) == expected_hash,
            f"{relative} matches its admitted SHA-256.",
        )

    failures = [row for row in checks if row["status"] != "PASS"]
    return {
        "schema_id": "source_matter_dynamics_selector_validation_v1",
        "task_id": "RT-20260727-008",
        "job_id": "AJ-RT-20260727-008-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "finding_counts": {
            "compared_branch_count": len(comparisons),
            "selected_branch_count": 1
            if recommendation.get("selected_branch") == "source_transition_law"
            else 0,
            "child_output_count": len(children),
            "unresolved_blocking_conflict_count": conflict.get(
                "unresolved_blocking_conflict_count", -1
            ),
            "executed_dynamics_packet_count": 0
            if selection.get("selected_dynamics_packet_executed_here") is False
            else 1,
            "adopted_source_law_count": 0
            if authority.get("source_law_adopted") is False
            else 1,
        },
        "validator_ids": [
            "p7_t02_three_branch_comparison_v1",
            "p7_t02_theoretical_decision_output_v1",
            "p7_t02_ontology_law_route_boundary_v1",
            "p7_t02_parent_child_synthesis_v1",
            "p7_t02_source_hash_guard_v1",
            "p7_t02_authority_flag_guard_v1",
        ],
        "claim_boundary_summary": (
            "One source-transition-law construction packet is selected but not "
            "executed; no source law, action, probability, physical conservation, "
            "ontology, detector, geometry, stress energy, coupling, GR, benchmark, "
            "proof, publication, push, no-go, or completed derivation is established."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.write_report and args.check:
        parser.error("--write-report and --check are mutually exclusive")

    report = build_report()
    compact = {
        "schema_id": "source_matter_dynamics_selector_compact_receipt_v1",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "selected_branch": "source_transition_law",
        "selected_next_packet_type": "ontology_law_research_packet",
        "selected_next_role_family": "candidate-constructor@0.2.0",
        "selected_dynamics_executed_here": False,
        "report_path": REPORT.relative_to(ROOT).as_posix(),
        "claim_boundary_summary": report["claim_boundary_summary"],
    }

    mode = "check" if args.check else "write"
    if mode == "write":
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    else:
        if not REPORT.is_file() or not COMPACT.is_file():
            report["status"] = "FAIL"
            report["failure_count"] += 1
        else:
            expected_report = json.dumps(report, indent=2, sort_keys=True) + "\n"
            expected_compact = json.dumps(compact, indent=2, sort_keys=True) + "\n"
            if REPORT.read_text(encoding="utf-8") != expected_report:
                report["status"] = "FAIL"
                report["failure_count"] += 1
            if COMPACT.read_text(encoding="utf-8") != expected_compact:
                report["status"] = "FAIL"
                report["failure_count"] += 1

    output = {
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "mode": mode,
        "report_path": REPORT.relative_to(ROOT).as_posix(),
        "compact_receipt_path": COMPACT.relative_to(ROOT).as_posix(),
    }
    if args.json:
        print(json.dumps(output, sort_keys=True))
    else:
        print(
            f"{output['status']}: {output['check_count']} checks, "
            f"{output['failure_count']} failures ({mode})"
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
