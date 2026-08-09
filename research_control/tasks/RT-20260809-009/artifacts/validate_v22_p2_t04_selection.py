#!/usr/bin/env python3
"""Validate the V22 P2-T04 primary/fallback selection packet.

The validator checks source snapshots, candidate identities, minimum adequacy,
selection/activation separation, family budget, assumption disclosure,
smuggling boundaries, frozen routes, adversarial fixtures, and fused-source
coverage. Its PASS is operational evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260809-009"
ARTIFACTS = TASK_ROOT / "artifacts"
PRIMARY_PATH = ARTIFACTS / "v22_p2_t04_primary_local_multifield_candidate_v1.yaml"
FALLBACK_PATH = ARTIFACTS / "v22_p2_t04_fallback_matter_principal_candidate_v1.yaml"
COMPARISON_PATH = ARTIFACTS / "v22_p2_t04_candidate_comparison_selection_v1.yaml"
ADEQUACY_PATH = ARTIFACTS / "v22_p2_t04_source_adequacy_results_v1.yaml"
ASSUMPTIONS_PATH = ARTIFACTS / "v22_p2_t04_assumption_delta_v1.yaml"
FROZEN_PATH = ARTIFACTS / "v22_p2_t04_frozen_route_map_v1.yaml"
ACTIVATION_PATH = ARTIFACTS / "v22_p2_t04_activation_handoff_v1.yaml"
FIXTURE_PATH = ARTIFACTS / "fixtures/v22_p2_t04_selection_adversarial_cases.yaml"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p2_t04_selection_stress.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p2_t04_smuggling_audit.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p2_t04_selection.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p2_t04_selection.md"
TEX_PATH = ARTIFACTS / "v22_p2_t04_primary_fallback_selection_v1.tex"
REPORT_PATH = ARTIFACTS / "v22_p2_t04_selection_validation.json"
RECEIPT_PATH = ARTIFACTS / "v22_p2_t04_compact_receipt.json"

PRIMARY_ID = "CAND-V22-B1-LOCAL-SIX-FIELD-RESPONSE-SEED-V1"
FALLBACK_ID = "CAND-V22-B2-P7-COMMON-PRINCIPAL-LIFT-V1"
FAMILY_IDS = [
    "FAM-V22-B1-LOCAL-MULTIFIELD-CONTINUUM",
    "FAM-V22-B2-MATTER-PRINCIPAL-POLYNOMIAL",
    "FAM-V22-B3-CONTROLLED-DISCRETE-CONTINUUM",
]

SOURCE_SNAPSHOTS = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0978.yaml":
        "13dca24ba535b09c98dfdfa9eb7886015b1b3b613a7249041802e29ea3db64bf",
    "research_control/tasks/RT-20260809-008/artifacts/v22_p2_t03_candidate_family_registry_v1.yaml":
        "af294001a2773735e5a4ab94bed0f5eccb3f72ce089e95afc99832f6fc835d5c",
    "research_control/tasks/RT-20260809-008/artifacts/v22_p2_t03_extension_budget_protocol_v1.yaml":
        "736c9914a287863f5bad7d456e20f2a67520ad377b95dca89027c7323fc4b1d7",
    "research_control/tasks/RT-20260809-008/artifacts/v22_p2_t03_hard_fail_matrix_v1.yaml":
        "f362ba5f52d472a02d2345760f9ad80b05af31b9973cb5d264ba1929ad16c9d0",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_local_source_information_capacity_theorem_v1.tex":
        "2ba813e4e961b9ea2709a31c6e06152b1cb4d50ebd90185c2ed93d7aeb132439",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_source_adequacy_checklist_v1.yaml":
        "a9b59df7b5b2d1203fef53cf23817400c6d1511836e97ff1ae21b819dc064e68",
    "research_control/tasks/RT-20260809-003/artifacts/v22_p1_t03_p7_conditional_input_contract_v1.yaml":
        "e1acd64ea434f3dc6a0607c17f69162f0e242bc92d5490eb84ff3d3afd92a3c4",
    "research_control/tasks/RT-20260809-004/artifacts/v22_p1_t04_gate_b_only_physics_lock_v1.tex":
        "28334e08c64cdf7ea5588e553a974eb7c37114e6792b8dcb98ea9b6b259a6408",
    "research_control/design/source_extension_classification_checklist_v1.md":
        "ecf6db3bd8372801e6c7ac12d6727e7eb270d1605747af77194b90815faaf6c0",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_yaml(path: Path) -> dict[str, Any]:
    result = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} is not a YAML mapping")
    return result


def flag(case: dict[str, Any], key: str) -> bool:
    return case.get(key) is True


def evaluate_case(case: dict[str, Any]) -> str:
    if flag(case, "target_metric_imported") or flag(case, "target_coframe_imported"):
        return "HARD_FAIL_TARGET_IMPORT"
    if flag(case, "desired_lorentzian_factor_imposed"):
        return "HARD_FAIL_TARGET_IMPORT"
    if flag(case, "gr_target_fit_used"):
        return "HARD_FAIL_GR_TARGET_FIT"
    if flag(case, "target_observable_labels_by_fiat"):
        return "HARD_FAIL_OBSERVABLE_FIAT"
    if flag(case, "scalar_amplitude_repackaged") or flag(
        case, "unchanged_graph_decoder_repackaged"
    ):
        return "HARD_FAIL_FROZEN_ROUTE_REPACKAGED"
    if flag(case, "protected_p7_postulate_used_as_gate_credit"):
        return "REJECT_PROTECTED_POSTULATE_LAUNDERING"
    if flag(case, "internal_review_claimed_external"):
        return "REJECT_INTERNAL_AS_EXTERNAL_REVIEW"
    if flag(case, "canonical_adoption_claimed") and not flag(
        case, "protected_authority_present"
    ):
        return "REJECT_UNAUTHORIZED_ADOPTION"
    if flag(case, "fallback_autoactivation"):
        return "REJECT_AUTOMATIC_FALLBACK"
    if flag(case, "fallback_activation_requested"):
        if not flag(case, "primary_terminated"):
            return "REJECT_FALLBACK_WITHOUT_PRIMARY_TERMINATION"
        if not flag(case, "exact_fallback_identity"):
            return "REJECT_FALLBACK_IDENTITY_DRIFT"
        ready = all(
            flag(case, key)
            for key in (
                "continuum_lift_present",
                "adequacy_reevaluated",
                "fresh_selector_decision",
            )
        )
        return (
            "PASS_FALLBACK_ELIGIBILITY_NOT_ACTIVATION"
            if ready
            else "REJECT_INCOMPLETE_FALLBACK_PACKET"
        )
    if "primary_capacity_rank" in case:
        return (
            "PASS_MINIMUM_ADEQUACY_ONLY"
            if int(case["primary_capacity_rank"]) >= int(case["required_response_rank"])
            else "REJECT_INADEQUATE_PRIMARY"
        )
    if flag(case, "differential_adequacy_claimed") and not flag(
        case, "fallback_continuum_state_present"
    ):
        return "REJECT_FALLBACK_SCOPE_OVERREACH"
    if flag(case, "family_name_changed_only") and not flag(
        case, "material_difference_proved"
    ):
        return "REJECT_RENAMED_FAMILY"
    if "b3_descriptor_present" in case:
        return (
            "PASS_B3_RESERVED_UNALLOCATED"
            if not flag(case, "b3_descriptor_present")
            and not flag(case, "third_slot_allocated")
            else "REJECT_THIRD_SLOT_ALLOCATION"
        )
    if flag(case, "determinant_of_source_coefficient_matrix"):
        return "PASS_STRUCTURAL_PRINCIPAL_TARGET_ONLY"
    if "primary_assumption_count" in case:
        return (
            "PASS_ASSUMPTION_DELTA"
            if int(case["primary_assumption_count"]) == 4
            and flag(case, "assumptions_individually_classified")
            else "REJECT_INCOMPLETE_ASSUMPTION_DELTA"
        )
    descriptor_keys = (
        "fields_present",
        "locality_present",
        "symmetry_present",
        "dynamics_present",
        "observables_present",
        "continuum_present",
        "assumptions_present",
        "principal_present",
    )
    if any(key in case for key in descriptor_keys):
        return (
            "PASS_COMPLETE_DESCRIPTOR"
            if all(flag(case, key) for key in descriptor_keys)
            else "REJECT_INCOMPLETE_DESCRIPTOR"
        )
    if "target_agreement_used_as_merit" in case:
        return (
            "PASS_NONCOMPENSATORY_SOURCE_MERIT"
            if not flag(case, "target_agreement_used_as_merit")
            and not flag(case, "scalar_score_total_used")
            else "REJECT_TARGET_OR_COMPENSATORY_SELECTION"
        )
    if flag(case, "selection_activation_distinction_explicit"):
        return (
            "PASS_SELECTION_ACTIVATION_DISTINCTION"
            if int(case.get("active_program_routes", -1)) == 1
            and int(case.get("scientific_activations", -1)) == 0
            else "REJECT_SELECTION_ACTIVATION_COLLAPSE"
        )
    if not flag(case, "primary_selected"):
        return "REJECT_MISSING_PRIMARY"
    if not flag(case, "fallback_selected"):
        return "REJECT_MISSING_FALLBACK"
    if flag(case, "third_slot_allocated"):
        return "REJECT_THIRD_SLOT_ALLOCATION"
    if int(case.get("active_program_routes", 0)) != 1:
        return "REJECT_PARALLEL_PROGRAM_ROUTES"
    if int(case.get("scientific_activations", 0)) != 0:
        return "REJECT_PREMATURE_SCIENTIFIC_ACTIVATION"
    return "PASS_SELECTION"


def compute_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: list[dict[str, str]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        status = "PASS" if condition else "FAIL"
        checks.append({"check_id": check_id, "status": status, "detail": detail})
        if not condition:
            errors.append(f"{check_id}: {detail}")

    required = [
        PRIMARY_PATH, FALLBACK_PATH, COMPARISON_PATH, ADEQUACY_PATH,
        ASSUMPTIONS_PATH, FROZEN_PATH, ACTIVATION_PATH, FIXTURE_PATH,
        CHILD_MATH_PATH, CHILD_PHIL_PATH, CONFLICT_PATH, FUSION_PATH, TEX_PATH,
    ]
    for path in required:
        check(f"path_exists:{path.name}", path.is_file(), str(path.relative_to(REPO_ROOT)))
    if errors:
        return {
            "schema_id": "v22_p2_t04_selection_validation_v1",
            "status": "FAIL", "task_id": "RT-20260809-009",
            "job_id": "AJ-RT-20260809-009-001", "error_count": len(errors),
            "errors": errors, "checks": checks,
        }

    primary = load_yaml(PRIMARY_PATH)
    fallback = load_yaml(FALLBACK_PATH)
    comparison = load_yaml(COMPARISON_PATH)
    adequacy = load_yaml(ADEQUACY_PATH)
    assumptions = load_yaml(ASSUMPTIONS_PATH)
    frozen = load_yaml(FROZEN_PATH)
    activation = load_yaml(ACTIVATION_PATH)
    fixtures = load_yaml(FIXTURE_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")
    fusion = FUSION_PATH.read_text(encoding="utf-8")

    for rel, expected in SOURCE_SNAPSHOTS.items():
        actual = sha256_path(REPO_ROOT / rel)
        check(f"source_snapshot:{rel}", actual == expected, f"expected {expected}; actual {actual}")

    for name, packet in (("primary", primary), ("fallback", fallback)):
        expected = sha256_bytes(packet["candidate_identity_basis"].encode("utf-8"))
        check(
            f"{name}_identity_hash",
            packet.get("candidate_identity_sha256") == expected,
            f"identity must hash to {expected}",
        )

    selection = comparison.get("selection_result", {})
    distinction = comparison.get("selection_activation_distinction", {})
    rows = comparison.get("candidate_rows", [])
    check("primary_identity", primary.get("candidate_id") == PRIMARY_ID, PRIMARY_ID)
    check("fallback_identity", fallback.get("candidate_id") == FALLBACK_ID, FALLBACK_ID)
    check("candidate_row_count", len(rows) == 3, "exactly three family-slot rows")
    check("family_ids_exact", [row.get("family_id") for row in rows] == FAMILY_IDS, "B1 B2 B3 order")
    check("primary_selected", selection.get("selected_primary_candidate_id") == PRIMARY_ID, PRIMARY_ID)
    check("fallback_preregistered", selection.get("preregistered_fallback_candidate_id") == FALLBACK_ID, FALLBACK_ID)
    check("third_slot_unallocated", selection.get("third_slot_status") == "reserved_unallocated", "slot 3 remains unallocated")
    check("one_program_route", selection.get("selected_primary_program_route_count") == 1, "one program route")
    check("zero_scientific_activation", selection.get("scientific_candidate_activation_count") == 0, "zero scientific activation")
    check("zero_parallel_candidates", selection.get("concurrent_candidate_count") == 0, "no parallel candidate")
    check("activation_separate", distinction.get("activation_authority", "").startswith("separate P3-T01"), "P3-T01 transition")
    check("no_target_merit", comparison.get("selection_method", {}).get("target_agreement_used_as_merit") is False, "target agreement forbidden")
    check("no_scalar_total", comparison.get("selection_method", {}).get("scalar_total_used") is False, "noncompensatory vector")

    screen = primary.get("source_adequacy_screen", {})
    check("primary_rank_two", screen.get("computed_capacity_rank") == 2, "rank 2")
    check("primary_required_rank_two", screen.get("required_response_rank") == 2, "required rank 2")
    check("primary_minimum_verdict", screen.get("theorem_result") == "necessary_condition_met_not_sufficient", "necessary only")
    check("no_geometry_sufficiency", screen.get("geometry_sufficiency_claimed") is False, "no geometry sufficiency")
    check("fallback_outside_scope", fallback.get("source_adequacy_screen", {}).get("theorem_result") == "outside_differential_scope", "no differential continuum")
    check("adequacy_primary_summary", adequacy.get("minimum_screen_summary", {}).get("primary_clears_minimum_screen") is True, "primary clears minimum")
    check("adequacy_fallback_fail_closed", adequacy.get("minimum_screen_summary", {}).get("fallback_clears_minimum_screen") is False, "fallback not yet adequate")

    primary_assumptions = assumptions.get("primary_delta", {}).get("assumptions", [])
    fallback_assumptions = assumptions.get("fallback_delta", {}).get("assumptions", [])
    check("four_primary_assumptions", len(primary_assumptions) == 4, "exactly four disclosed")
    check("four_fallback_assumptions", len(fallback_assumptions) == 4, "exactly four disclosed")
    check("zero_metric_debt", assumptions.get("comparison", {}).get("metric_equivalent_input_count") == 0, "no metric-equivalent input")
    check("zero_gr_fit", assumptions.get("comparison", {}).get("gr_target_fit_count") == 0, "no GR fit")
    check("zero_postulate_gate_credit", assumptions.get("comparison", {}).get("protected_postulate_gate_credit_count") == 0, "no postulate Gate credit")

    routes = frozen.get("frozen_routes", [])
    check("two_frozen_routes", len(routes) == 2, "scalar and graph routes")
    check("scalar_frozen", routes[0].get("preserved_status") == "frozen_negative", "scalar remains frozen")
    check("graph_frozen", routes[1].get("preserved_status") == "frozen_negative", "graph remains frozen")
    check("fallback_not_automatic", fallback.get("fallback_activation_criteria", {}).get("automatic_activation") is False, "fresh selector required")
    check("activation_not_executed", activation.get("authority_limits", {}).get("activation_executed_here") is False, "selection only")
    check("next_transition_p3_t01", activation.get("next_transition", {}).get("executing_plan_task_id") == "P3-T01", "P3-T01")

    decision = comparison.get("theoretical_decision_output", {})
    required_decision_fields = {
        "selected_next_packet_type", "decision_basis", "theoretical_method",
        "preserves_claim_blocks", "requires_human_gate", "human_gate_reason",
        "source_extension_category", "source_extension_import_classification",
    }
    check("selector_output_complete", required_decision_fields <= set(decision), "all role-required fields")
    check("selector_preserves_blocks", decision.get("preserves_claim_blocks") is True, "claim blocks preserved")
    check("selector_no_gate_for_construction", decision.get("requires_human_gate") is False, "proposal construction not gated")

    fixture_cases = fixtures.get("cases", [])
    check("fixture_count_30", fixtures.get("case_count") == 30 and len(fixture_cases) == 30, "exactly 30 cases")
    fixture_failures = []
    fixture_outcomes = []
    for case in fixture_cases:
        actual = evaluate_case(case)
        expected = case.get("expected")
        fixture_outcomes.append({"case_id": case.get("case_id"), "expected": expected, "actual": actual, "status": "PASS" if actual == expected else "FAIL"})
        if actual != expected:
            fixture_failures.append(f"{case.get('case_id')}: expected {expected}; actual {actual}")
    check("all_fixtures_pass", not fixture_failures, "; ".join(fixture_failures) or "30/30")

    check("math_child_complete", child_math.get("status") == "completed", "math/refuter child")
    check("math_rank_result", child_math.get("rank_two_certificate", {}).get("local_rank") == 2, "rank two")
    check("phil_child_complete", child_phil.get("status") == "completed", "smuggling child")
    check("phil_eight_findings", len(child_phil.get("findings", [])) == 8, "eight audit findings")
    check("conflicts_resolved", conflict.get("blocking_conflict_count") == 0 and not conflict.get("unresolved_conflicts"), "zero blocking conflicts")
    check(
        "fusion_marks_internal",
        "internal review is" in fusion and "external review" in fusion,
        "review classification",
    )

    tex_fragments = [
        "rank-two response certificate",
        "selection--activation noncollapse",
        "necessary\\_condition\\_met\\_not\\_sufficient",
        "Noncompensatory comparison",
        "Expanded Distance-to-GR matrix",
        "physical Distance-to-GR delta is zero",
        "P3-T01",
        "not target clocks, rods",
    ]
    for fragment in tex_fragments:
        check(f"tex_fragment:{fragment}", fragment in tex, f"TeX must include {fragment}")

    authority_maps = [
        primary.get("authority_limits", {}), fallback.get("authority_limits", {}),
        comparison.get("authority_limits", {}), assumptions.get("authority_limits", {}),
        activation.get("authority_limits", {}), child_math.get("authority_limits", {}),
        child_phil.get("authority_limits", {}), conflict.get("authority_limits", {}),
    ]
    check(
        "all_promotion_flags_false",
        all(item.get("physics_promotion_authorized") is False for item in authority_maps),
        "every authority surface blocks physics promotion",
    )

    return {
        "schema_id": "v22_p2_t04_selection_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260809-009",
        "job_id": "AJ-RT-20260809-009-001",
        "plan_task_id": "P2-T04",
        "check_count": len(checks),
        "pass_count": sum(item["status"] == "PASS" for item in checks),
        "error_count": len(errors),
        "errors": errors,
        "fixture_count": len(fixture_cases),
        "fixture_outcomes": fixture_outcomes,
        "checks": checks,
        "authority_note": "Validator PASS is internal operational evidence only. It does not activate or adopt a candidate, establish a metric or Gate result, provide external review, change Distance-to-GR, or authorize physics promotion.",
    }


def compact_receipt(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        PRIMARY_PATH, FALLBACK_PATH, COMPARISON_PATH, ADEQUACY_PATH,
        ASSUMPTIONS_PATH, FROZEN_PATH, ACTIVATION_PATH, FIXTURE_PATH,
        CHILD_MATH_PATH, CHILD_PHIL_PATH, CONFLICT_PATH, FUSION_PATH, TEX_PATH,
    ]
    return {
        "schema_id": "v22_p2_t04_compact_receipt_v1",
        "status": report["status"],
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "plan_task_id": report["plan_task_id"],
        "selected_primary_candidate_id": PRIMARY_ID,
        "preregistered_fallback_candidate_id": FALLBACK_ID,
        "third_slot_status": "reserved_unallocated",
        "active_program_route_count": 1,
        "scientific_candidate_activation_count": 0,
        "minimum_adequacy_verdict": "necessary_condition_met_not_sufficient",
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "fixture_count": report["fixture_count"],
        "artifact_sha256": {
            str(path.relative_to(REPO_ROOT)): sha256_path(path) for path in paths
        },
        "authority_note": report["authority_note"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write validation report and compact receipt")
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = compute_report()
    if args.write:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        RECEIPT_PATH.write_text(json.dumps(compact_receipt(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report.get('pass_count', 0)}/{report.get('check_count', 0)} checks; {report.get('fixture_count', 0)} fixtures")
        for error in report.get("errors", []):
            print(error)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
