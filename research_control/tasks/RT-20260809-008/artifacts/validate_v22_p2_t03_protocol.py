#!/usr/bin/env python3
"""Validate the V22 P2-T03 extension-budget and hard-fail protocol.

This task-local validator checks deterministic protocol structure, prospective
family identity, sequential-state invariants, adversarial fixture decisions,
source hashes, and authority boundaries. It is operational evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260809-008"
ARTIFACTS = TASK_ROOT / "artifacts"
PROTOCOL_PATH = ARTIFACTS / "v22_p2_t03_extension_budget_protocol_v1.yaml"
REGISTRY_PATH = ARTIFACTS / "v22_p2_t03_candidate_family_registry_v1.yaml"
MATRIX_PATH = ARTIFACTS / "v22_p2_t03_hard_fail_matrix_v1.yaml"
FIXTURE_PATH = ARTIFACTS / "fixtures/v22_p2_t03_protocol_adversarial_cases.yaml"
TEX_PATH = ARTIFACTS / "v22_p2_t03_source_extension_budget_hard_fail_protocol_v1.tex"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p2_t03_budget_protocol.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p2_t03_smuggling_scope_audit.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p2_t03_protocol.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p2_t03_protocol.md"
REPORT_PATH = ARTIFACTS / "v22_p2_t03_protocol_validation.json"


SOURCE_SNAPSHOTS = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0977.yaml":
        "9145365ac95d3dccd0ecca8fbe584814a81a59d7ea781a5147766c2dd86bf8c4",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_local_source_information_capacity_theorem_v1.tex":
        "2ba813e4e961b9ea2709a31c6e06152b1cb4d50ebd90185c2ed93d7aeb132439",
    "research_control/tasks/RT-20260809-004/artifacts/v22_p1_t04_gate_b_only_physics_lock_v1.tex":
        "28334e08c64cdf7ea5588e553a974eb7c37114e6792b8dcb98ea9b6b259a6408",
    "research_control/design/source_extension_classification_checklist_v1.md":
        "ecf6db3bd8372801e6c7ac12d6727e7eb270d1605747af77194b90815faaf6c0",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}

EXPECTED_FAMILY_IDS = [
    "FAM-V22-B1-LOCAL-MULTIFIELD-CONTINUUM",
    "FAM-V22-B2-MATTER-PRINCIPAL-POLYNOMIAL",
    "FAM-V22-B3-CONTROLLED-DISCRETE-CONTINUUM",
]

EXPECTED_GATE_B_IDS = [
    "GB01_TARGET_ATLAS_FREE",
    "GB02_REDUCED_HYPERBOLIC_PRINCIPAL",
    "GB03_STABLE_LORENTZIAN_CONE",
    "GB04_UNIVERSAL_MATTER_COMPATIBILITY",
    "GB05_OPERATIONAL_SCALE",
    "GB06_TENSORIAL_GLUING",
    "GB07_VARIATION_COARSE_GRAINING_ROBUSTNESS",
    "GB08_NO_HIDDEN_METRIC_EQUIVALENT",
]

EXPECTED_HARD_FAIL_IDS = [
    "HF01_METRIC_EQUIVALENT_IMPORT",
    "HF02_OBSERVABLE_LABEL_BY_FIAT",
    "HF03_GR_TARGET_FITTING",
    "HF04_NONUNIVERSAL_OR_UNSELECTED_MULTICONE",
    "HF05_INSTABILITY_NONHYPERBOLICITY_DEGENERACY",
    "HF06_NO_CONTROLLED_CONTINUUM_LIMIT",
    "HF07_EINSTEIN_STRUCTURE_POSTULATED",
    "HF08_FROZEN_ROUTE_REPACKAGED",
]

EXPECTED_SUPPLEMENTAL_FIELDS = [
    "regularity",
    "time orientation",
    "nondegeneracy",
    "conditioning",
    "second-clock-effect analysis",
]

EXPECTED_OUTCOME_IDS = [
    "FIRST_PRINCIPLES_WITHIN_SCOPE",
    "CONTROLLED_APPROXIMATE_RECOVERY",
    "CURRENT_ONTOLOGY_INSUFFICIENT_UNDER_PREREGISTERED_BUDGET",
    "EXACT_GR_INTERPRETATION_RETAINED_WITHOUT_SOURCE_DERIVATION",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} is not a YAML mapping")
    return value


def bool_value(case: dict[str, Any], key: str) -> bool:
    return case.get(key) is True


def evaluate_case(case: dict[str, Any]) -> str:
    family_count = int(case.get("candidate_family_count", 0))
    active_count = int(case.get("active_family_count", 0))
    if family_count > 3:
        return "REJECT_BUDGET_GROWTH"
    if active_count > 1:
        return "REJECT_CONCURRENT_ACTIVATION"
    if bool_value(case, "family_identity_defined_after_result"):
        return "REJECT_POST_RESULT_FAMILY_DEFINITION"
    if bool_value(case, "renamed_identity_matches_existing"):
        return "HARD_FAIL_HF08_FROZEN_ROUTE_REPACKAGED"
    if bool_value(case, "assumption_signature_matches_existing") and not bool_value(
        case, "material_difference_proved"
    ):
        return "HARD_FAIL_HF08_FROZEN_ROUTE_REPACKAGED"
    if bool_value(case, "ambiguous_family_equivalence"):
        return "REJECT_AMBIGUOUS_EQUIVALENCE_FAIL_CLOSED"
    if bool_value(case, "deletes_or_weakens_failure_record"):
        return "REJECT_FAILURE_LEDGER_MUTATION"

    if bool_value(case, "overlap_requested"):
        required = (
            int(case.get("overlap_family_count", 0)) >= 2
            and active_count == 1
            and bool_value(case, "single_source_law")
            and bool_value(case, "primary_family_declared")
            and bool_value(case, "prospective_overlap_evidence")
        )
        if not required or not bool_value(case, "all_implicated_slots_debited"):
            return "REJECT_OVERLAP_BUDGET_EVASION"
        return "OVERLAP_VALID_SINGLE_ACTIVE"

    if bool_value(case, "fallback_activation_requested"):
        if not bool_value(case, "primary_terminated"):
            return "REJECT_FALLBACK_WITHOUT_TERMINATION"
        if not bool_value(case, "fresh_selector_decision"):
            return "REJECT_FALLBACK_WITHOUT_FRESH_SELECTOR"
        if not bool_value(case, "failure_history_preserved"):
            return "REJECT_FAILURE_LEDGER_MUTATION"
        if active_count != 1:
            return "REJECT_CONCURRENT_ACTIVATION"
        return "FALLBACK_ACTIVATION_VALID"

    if bool_value(case, "third_slot_allocation_requested"):
        if not bool_value(case, "qualifying_independent_review"):
            return "REJECT_THIRD_SLOT_WITHOUT_INDEPENDENT_REVIEW"
        if not bool_value(case, "explicit_program_decision"):
            return "REJECT_THIRD_SLOT_WITHOUT_PROGRAM_DECISION"
        if not bool_value(case, "failure_history_preserved"):
            return "REJECT_FAILURE_LEDGER_MUTATION"
        return "THIRD_SLOT_ALLOCATION_VALID"

    hard_fail_triggers = case.get("hard_fail_triggers", [])
    if hard_fail_triggers:
        trigger = str(hard_fail_triggers[0])
        return f"HARD_FAIL_{trigger}"

    passed = set(case.get("gate_b_passed_ids", []))
    if passed:
        supplemental = set(case.get("supplemental_fields_present", []))
        if passed == set(EXPECTED_GATE_B_IDS) and supplemental == set(
            EXPECTED_SUPPLEMENTAL_FIELDS
        ):
            return "ELIGIBLE_FOR_PROTECTED_REVIEW_NOT_GATE_B_POSITIVE"
        return "INELIGIBLE_INCOMPLETE_GATE_B_PACKET"

    if bool_value(case, "activation_requested"):
        complete = all(
            bool_value(case, key)
            for key in (
                "descriptor_complete",
                "assumption_ledger_complete",
                "family_fingerprint_sealed",
                "test_plan_sealed",
            )
        )
        if not complete or active_count != 1:
            return "REJECT_INCOMPLETE_ACTIVATION_PACKET"
        return "ACTIVATION_VALID_SINGLE_FAMILY"

    if bool_value(case, "selection_requested"):
        if (
            bool_value(case, "primary_selected")
            and bool_value(case, "fallback_selected")
            and not bool_value(case, "third_slot_allocated")
            and active_count == 0
        ):
            return "SELECTION_VALID_NO_ACTIVATION"
        return "REJECT_INCOMPLETE_SELECTION"

    return "PROTOCOL_VALID_IDLE"


def compute_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        status = "PASS" if condition else "FAIL"
        checks.append({"check_id": check_id, "status": status, "detail": detail})
        if not condition:
            errors.append(f"{check_id}: {detail}")

    required_paths = [
        PROTOCOL_PATH,
        REGISTRY_PATH,
        MATRIX_PATH,
        FIXTURE_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required_paths:
        check(
            f"path_exists:{path.name}",
            path.is_file(),
            str(path.relative_to(REPO_ROOT)),
        )

    if errors:
        return {
            "schema_id": "v22_p2_t03_protocol_validation_v1",
            "status": "FAIL",
            "task_id": "RT-20260809-008",
            "job_id": "AJ-RT-20260809-008-001",
            "error_count": len(errors),
            "errors": errors,
            "checks": checks,
        }

    protocol = load_yaml(PROTOCOL_PATH)
    registry = load_yaml(REGISTRY_PATH)
    matrix = load_yaml(MATRIX_PATH)
    fixtures = load_yaml(FIXTURE_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")
    fusion = FUSION_PATH.read_text(encoding="utf-8")

    budget = protocol.get("budget", {})
    check("budget_max_three", budget.get("maximum_material_family_count") == 3,
          "maximum_material_family_count must equal 3")
    check("budget_three_preregistered", budget.get("preregistered_family_count") == 3,
          "preregistered_family_count must equal 3")
    check("single_active_family", budget.get("active_family_limit") == 1,
          "active_family_limit must equal 1")
    check("current_zero_active", budget.get("current_active_family_id") == "",
          "P2-T03 must not activate a family")
    check("append_only_failures", budget.get("failures_append_only") is True,
          "failure history must be append-only")
    check("no_budget_growth", budget.get("automatic_budget_growth") is False,
          "automatic budget growth must be false")
    check("fourth_slot_forbidden", budget.get("fourth_slot_available") is False,
          "fourth slot must be unavailable")

    third_slot = protocol.get("slot_policy", {}).get("third_slot", {})
    check("third_slot_reserved", third_slot.get("allocation_status") == "reserved_unallocated",
          "third slot must remain reserved and unallocated")
    check("third_slot_no_reviewer_contact", third_slot.get("reviewer_contact_authorized_here") is False,
          "P2-T03 does not authorize reviewer contact")

    overlap = protocol.get("overlap_policy", {})
    check("overlap_debits_all_slots", overlap.get("debits_every_implicated_family_slot") is True,
          "lawful overlap must debit every implicated family slot")
    check("overlap_secondary_not_active", overlap.get("secondary_family_active") is False,
          "secondary overlap family must not become concurrently active")
    check("overlap_no_growth", overlap.get("overlap_grows_budget") is False,
          "overlap must not grow the budget")

    families = registry.get("families", [])
    family_ids = [item.get("family_id") for item in families]
    check("exact_family_ids", family_ids == EXPECTED_FAMILY_IDS,
          f"family ids must equal {EXPECTED_FAMILY_IDS}")
    check("exact_family_slots", [item.get("slot") for item in families] == [1, 2, 3],
          "family slots must be 1, 2, 3 in order")
    for family in families:
        family_id = str(family.get("family_id"))
        identity_basis = str(family.get("identity_basis", ""))
        expected_hash = sha256_bytes(identity_basis.encode("utf-8"))
        check(
            f"family_hash:{family_id}",
            family.get("family_identity_sha256") == expected_hash,
            f"identity hash must be {expected_hash}",
        )
        check(
            f"family_inactive:{family_id}",
            family.get("active") is False,
            "all P2-T03 family records must be inactive",
        )
        check(
            f"family_not_adopted:{family_id}",
            family.get("adopted") is False,
            "family registration cannot adopt an extension",
        )

    classification = registry.get("source_extension_classification", {})
    check("registry_status_boundary_only",
          classification.get("classification") == "status_boundary_evidence_only",
          "registry must be classification evidence only")
    check("registry_no_promotion", classification.get("physics_promotion_authorized") is False,
          "registry classification cannot promote physics")

    gate_ids = [item.get("criterion_id") for item in matrix.get("gate_b_criteria", [])]
    hard_fail_ids = [item.get("trigger_id") for item in matrix.get("hard_fail_triggers", [])]
    supplemental = matrix.get("supplemental_positive_packet_fields", [])
    outcome_ids = [item.get("outcome_id") for item in matrix.get("final_verdict_templates", [])]
    check("exact_gate_b_criteria", gate_ids == EXPECTED_GATE_B_IDS,
          "all eight Gate B criteria must be preregistered in order")
    check("all_gate_b_fail_closed",
          all(item.get("fail_closed_when_missing") is True for item in matrix.get("gate_b_criteria", [])),
          "every missing Gate B criterion must fail closed")
    check("exact_hard_fail_triggers", hard_fail_ids == EXPECTED_HARD_FAIL_IDS,
          "all eight hard-fail triggers must be preregistered in order")
    check("exact_supplemental_fields", supplemental == EXPECTED_SUPPLEMENTAL_FIELDS,
          "all five supplemental positive-packet fields must be present")
    check("exact_terminal_outcomes", outcome_ids == EXPECTED_OUTCOME_IDS,
          "all four scoped terminal outcomes must be present")

    verdict_text = " ".join(
        str(item.get("template", "")) for item in matrix.get("final_verdict_templates", [])
    ).lower()
    check("scoped_budget_exhaustion_wording",
          "within the current ontology and the preregistered three-family extension budget" in verdict_text,
          "budget-exhaustion wording must name current ontology and the preregistered budget")
    check("no_global_impossibility_template",
          "not a global impossibility theorem or future-extension closure" in verdict_text,
          "terminal wording must explicitly block global impossibility overread")
    check("all_templates_no_global_no_go",
          all(item.get("global_no_go_claimed") is False for item in matrix.get("final_verdict_templates", [])),
          "every final template must keep global_no_go_claimed false")

    cases = fixtures.get("cases", [])
    fixture_results: list[dict[str, Any]] = []
    for case in cases:
        observed = evaluate_case(case)
        expected = case.get("expected_decision")
        passed = observed == expected
        fixture_results.append(
            {
                "case_id": case.get("case_id"),
                "expected_decision": expected,
                "observed_decision": observed,
                "status": "PASS" if passed else "FAIL",
            }
        )
        if not passed:
            errors.append(
                f"fixture:{case.get('case_id')}: expected {expected}, observed {observed}"
            )
    check("fixture_count", len(cases) == fixtures.get("case_count") == 30,
          "fixture case_count and list length must both equal 30")
    check("fixture_ids_unique", len({case.get("case_id") for case in cases}) == len(cases),
          "fixture IDs must be unique")
    check("all_fixtures_pass", all(item["status"] == "PASS" for item in fixture_results),
          "all adversarial fixtures must match their preregistered decisions")

    check("child_math_complete", child_math.get("status") == "completed",
          "Physicist-Mathematician child must be complete")
    check("child_phil_complete", child_phil.get("status") == "completed",
          "Physicist-Philosopher child must be complete")
    check("children_nonexternal",
          child_math.get("review_classification", {}).get("external_review") is False
          and child_phil.get("review_classification", {}).get("external_review") is False,
          "both internal children must be classified nonexternal")
    check("conflicts_resolved", conflict.get("status") == "resolved"
          and conflict.get("blocking_conflict_count") == 0
          and conflict.get("fusion_authorized") is True,
          "parent conflict review must resolve all blocking conflicts")
    check("fusion_preserves_limitations", "## Remaining limitations" in fusion,
          "fusion notes must preserve remaining limitations")

    required_tex_fragments = [
        "Finite-budget termination theorem",
        "Failure-monotonicity lemma",
        "Exactly three preregistered families",
        "Sequential activation state machine",
        "Gate B eligibility predicate",
        "Hard-fail predicate",
        "not a global impossibility theorem",
        "physical Distance-to-GR delta is zero",
        "P2-T04 may select one primary and one fallback only after this packet checkpoints",
    ]
    for fragment in required_tex_fragments:
        check(f"tex_fragment:{fragment}", fragment in tex,
              f"TeX must include fragment: {fragment}")

    source_hashes: list[dict[str, Any]] = []
    for relative, expected_hash in SOURCE_SNAPSHOTS.items():
        path = REPO_ROOT / relative
        observed_hash = sha256_path(path) if path.is_file() else ""
        source_hashes.append(
            {
                "path": relative,
                "expected_sha256": expected_hash,
                "observed_sha256": observed_hash,
                "match": observed_hash == expected_hash,
            }
        )
        check(f"source_hash:{relative}", observed_hash == expected_hash,
              f"source snapshot must remain {expected_hash}")

    authority_limits = [
        protocol.get("authority_limits", {}),
        registry.get("authority_limits", {}),
        matrix.get("authority_limits", {}),
    ]
    forbidden_true_keys = {
        "candidate_selected",
        "candidate_activated",
        "source_extension_adopted",
        "canonical_ontology_modified",
        "unscoped_g_eff_constructed",
        "gate_b_verdict_issued",
        "external_review_completed",
        "reviewer_contact_authorized",
        "scientific_status_changed",
        "distance_to_gr_changed",
        "physics_promotion_authorized",
        "global_no_go_claim_authorized",
        "publication_or_push_authorized",
    }
    authority_violations: list[str] = []
    for block in authority_limits:
        for key, value in block.items():
            if key in forbidden_true_keys and value is not False:
                authority_violations.append(f"{key}={value!r}")
    check("authority_limits_false", not authority_violations,
          "forbidden authority flags must be false: " + ", ".join(authority_violations))

    artifact_hashes = {
        str(path.relative_to(REPO_ROOT)): sha256_path(path)
        for path in required_paths
    }
    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v22_p2_t03_protocol_validation_v1",
        "status": status,
        "task_id": "RT-20260809-008",
        "job_id": "AJ-RT-20260809-008-001",
        "plan_task_id": "P2-T03",
        "focused_check_count": len(checks),
        "focused_check_failure_count": sum(1 for item in checks if item["status"] == "FAIL"),
        "fixture_count": len(cases),
        "fixture_pass_count": sum(1 for item in fixture_results if item["status"] == "PASS"),
        "fixture_failure_count": sum(1 for item in fixture_results if item["status"] == "FAIL"),
        "family_count": len(families),
        "active_family_count": sum(1 for item in families if item.get("active") is True),
        "gate_b_criterion_count": len(gate_ids),
        "hard_fail_trigger_count": len(hard_fail_ids),
        "terminal_template_count": len(outcome_ids),
        "source_snapshot_count": len(source_hashes),
        "source_hashes": source_hashes,
        "artifact_hashes": artifact_hashes,
        "fixture_results": fixture_results,
        "checks": checks,
        "error_count": len(errors),
        "errors": errors,
        "authority_limits": {
            "candidate_selected": False,
            "candidate_activated": False,
            "source_extension_adopted": False,
            "canonical_ontology_modified": False,
            "unscoped_g_eff_constructed": False,
            "gate_b_verdict_issued": False,
            "external_review_completed": False,
            "reviewer_contact_authorized": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "global_no_go_claim_authorized": False,
            "publication_or_push_authorized": False,
        },
    }


def normalized_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic report")
    parser.add_argument("--json", action="store_true", help="print report as JSON")
    args = parser.parse_args()

    report = compute_report()
    rendered = normalized_json(report)
    if args.write:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    elif REPORT_PATH.is_file() and REPORT_PATH.read_text(encoding="utf-8") != rendered:
        report["status"] = "FAIL"
        report["error_count"] = int(report.get("error_count", 0)) + 1
        report.setdefault("errors", []).append(
            "tracked validation report is stale; rerun with --write"
        )
        rendered = normalized_json(report)

    if args.json:
        print(rendered, end="")
    else:
        print(
            f"{report['status']} checks={report.get('focused_check_count', 0)} "
            f"fixtures={report.get('fixture_pass_count', 0)}/{report.get('fixture_count', 0)} "
            f"errors={report.get('error_count', 0)}"
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
