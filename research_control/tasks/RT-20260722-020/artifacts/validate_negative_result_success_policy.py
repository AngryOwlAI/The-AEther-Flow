#!/usr/bin/env python3
"""Deterministically validate the bounded P14-T05 negative-result packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "negative_result_success_validation_report.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def minimal_hitting_sets(universe: set[str], clauses: list[set[str]]) -> set[frozenset[str]]:
    hits: list[frozenset[str]] = []
    ordered = sorted(universe)
    for size in range(len(ordered) + 1):
        for values in itertools.combinations(ordered, size):
            candidate = frozenset(values)
            if all(candidate & clause for clause in clauses):
                hits.append(candidate)
    return {hit for hit in hits if not any(other < hit for other in hits)}


def build_report() -> dict[str, Any]:
    scope = load_yaml("negative_result_scope_reopening_schema_v1.yaml")
    publication = load_yaml("negative_result_publication_readiness_v1.yaml")
    math_child = load_yaml("child_phys_math_negative_result_success.yaml")
    phil_child = load_yaml("child_phys_phil_negative_result_success.yaml")
    conflict = load_yaml("parent_conflict_review_negative_result_success.yaml")
    tex = (ARTIFACT_DIR / "negative_result_success_pathway_v1.tex").read_text(encoding="utf-8")
    fusion = (ARTIFACT_DIR / "parent_fusion_notes_negative_result_success.md").read_text(encoding="utf-8")

    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    check("scope_schema", scope.get("schema_id") == "negative_result_scope_reopening_schema_v1", "scope schema identity")
    check("publication_schema", publication.get("schema_id") == "negative_result_publication_readiness_v1", "publication schema identity")
    check("task_identity_scope", scope.get("task_id") == "RT-20260722-020", "scope task identity")
    check("task_identity_publication", publication.get("task_id") == "RT-20260722-020", "publication task identity")
    check("job_identity_scope", scope.get("job_id") == "AJ-RT-20260722-020-001", "scope job identity")
    check("plan_identity_scope", scope.get("plan_task_id") == "P14-T05", "plan task identity")
    check("milestone_identity", scope.get("target_derivation_milestone") == "source_equivalence_eqsrc", "target milestone")
    check(
        "milestone_burden",
        scope.get("milestone_burden") == "Ensure negative science can close a line without becoming global theory rejection.",
        "exact plan burden",
    )

    ladder = scope.get("strength_ladder", [])
    strength_ids = [item.get("strength_id") for item in ladder]
    expected_strengths = [
        "finite_countermodel",
        "scoped_obstruction",
        "scoped_no_go_theorem",
        "minimum_extension_theorem",
        "future_extension_impossibility",
    ]
    check("strength_count", len(ladder) == 5, "five distinct strength levels")
    check("strength_order", strength_ids == expected_strengths, "strength ladder order and identity")
    check("finite_countermodel_scope", "declared finite domain" in ladder[0].get("quantifier_scope", ""), "finite witness scope")
    check("scoped_obstruction_inventory", "sealed family inventory" in ladder[1].get("minimum_evidence", []), "family inventory required")
    check("scoped_no_go_proof", "proof" in ladder[2].get("minimum_evidence", []), "no-go proof required")
    check("minimum_extension_soundness", "clause-soundness qualification" in ladder[3].get("minimum_evidence", []), "clause soundness required")
    check("future_impossibility_blocked", ladder[4].get("current_status") == "not_established_and_blocked", "global strength blocked")

    exact_fields = scope.get("exact_question_record", {}).get("required_fields", [])
    check("question_field_count", len(exact_fields) == 6, "six exact identity fields")
    for field in ["question_id", "instance_domain", "admissible_construction_family", "assumptions", "tested_claim", "source_paths_and_sha256es"]:
        check(f"question_field_{field}", field in exact_fields, f"required exact question field {field}")

    completion = scope.get("scientific_completion_predicate", {})
    required = completion.get("all_required", [])
    check("completion_predicate_id", completion.get("predicate_id") == "NR-EXACT-SCOPE-COMPLETE-V1", "completion predicate identity")
    check("completion_requirement_count", len(required) == 8, "eight completion conjuncts")
    check("reopening_required", "reopening_predicate_explicit" in required, "reopening is mandatory")
    check("authority_separation_required", "authority_surfaces_separated" in required, "authority separation is mandatory")
    check("programme_non_effect", "programme completion" in completion.get("non_effects", []), "programme completion blocked")
    check("publication_non_effect", "publication authority" in completion.get("non_effects", []), "publication authority blocked")

    closure_states = scope.get("closure_states", [])
    closure_ids = [item.get("state") for item in closure_states]
    check("closure_state_count", len(closure_states) == 5, "five closure dispositions")
    for state in ["keep_open", "close_exact_route", "freeze_family", "close_scoped_question", "protected_global_closure"]:
        check(f"closure_{state}", state in closure_ids, f"closure state {state}")
    check("global_closure_unavailable", closure_states[-1].get("current_status") == "not_available", "protected global closure unavailable")

    triggers = scope.get("reopening_trigger_classes", [])
    trigger_ids = {item.get("trigger_id") for item in triggers}
    check("reopening_trigger_count", len(triggers) == 7, "seven reopening classes")
    for trigger in ["assumption_change", "domain_enlargement", "new_construction_family", "new_capability", "proof_defect", "operational_bridge", "material_independent_review"]:
        check(f"reopening_{trigger}", trigger in trigger_ids, f"reopening trigger {trigger}")

    classifications = scope.get("current_eqsrc_classifications", [])
    by_result = {item.get("result_id"): item for item in classifications}
    check("classification_count", len(classifications) == 4, "four current result classes")
    check("p2_scope_preserved", by_result["P2-T08-DETERMINISTIC-EQUIVARIANT-SELECTOR"].get("closure") == "exact_declared_selector_question_only", "P2-T08 exact scope")
    check("p2_review_calibrated", by_result["P2-T08-DETERMINISTIC-EQUIVARIANT-SELECTOR"].get("review_provenance") == "internal_AI_no_blocking_defect_not_external_human_review", "internal review is calibrated")
    check("p3_family_local", "locally frozen" in by_result["P3-T07-HISTORICAL-FAMILY-FREEZE"].get("closure", ""), "historical family freeze remains local")
    check("general_eqsrc_open", by_result["GENERAL-EQSRC"].get("closure") == "keep_open", "general EqSrc stays open")

    model = scope.get("minimum_extension_model", {})
    signatures = model.get("provisional_signatures", [])
    check("theorem_identity", model.get("theorem_id") == "NR-MINIMUM-EXTENSION-HITTING-SET-THEOREM-V1", "theorem identity")
    check("minimal_semantics", model.get("minimum_semantics") == "inclusion_minimal_unless_declared_cost_function", "minimum semantics")
    check("capability_universe_incomplete", model.get("capability_universe_complete") is False, "universe incompleteness explicit")
    check("physical_sufficiency_false", model.get("clause_system_physically_sufficient") is False, "clause system not physically sufficient")
    check("signature_count", len(signatures) == 3, "three provisional routing signatures")
    check("signatures_nonexhaustive", model.get("authority_limits", {}).get("signatures_exhaustive") is False, "signatures non-exhaustive")
    check("signature_not_selected", model.get("authority_limits", {}).get("signature_selected") is False, "no signature selected")

    computed = minimal_hitting_sets({"d", "n", "q"}, [{"d", "q"}, {"n", "q"}])
    expected = {frozenset({"q"}), frozenset({"d", "n"})}
    check("finite_hitting_set_example", computed == expected, "toy model has exactly {q} and {d,n}")
    check("empty_signature_fails", frozenset() not in computed, "empty signature does not escape")
    check("singleton_d_fails", frozenset({"d"}) not in computed, "{d} does not escape")
    check("singleton_n_fails", frozenset({"n"}) not in computed, "{n} does not escape")

    authority = scope.get("authority_limits", {})
    for key in [
        "global_no_go_established",
        "future_extension_impossibility_established",
        "canonical_ontology_changed",
        "scientific_ledger_changed",
        "physical_interpretation_authorized",
        "publication_authorized",
        "physics_promotion_authorized",
        "completed_derivation_claimed",
    ]:
        check(f"authority_{key}", authority.get(key) is False, f"authority limit {key} is false")
    check("blocked_adoption_open_continuation", authority.get("current_adoption_status") == "blocked_adoption_open_continuation", "precise adoption disposition")
    check("same_milestone_open", authority.get("same_milestone_continuation_open") is True, "same-milestone continuation open")

    levels = publication.get("readiness_levels", [])
    current = publication.get("current_assessment", {})
    pub_auth = publication.get("authority_limits", {})
    check("readiness_level_count", len(levels) == 4, "four readiness levels")
    check("current_draft_control", current.get("achieved_level") == "draft_control_only", "current achieved level")
    check("internal_integration_ready", current.get("internal_manuscript_integration_ready") is True, "internal integration criteria met")
    check("external_review_absent", current.get("external_human_review_present") is False, "no external human review")
    check("submission_ineligible", current.get("publication_submission_eligible") is False, "submission eligibility false")
    check("publication_unauthorized", current.get("publication_authorized") is False, "publication authority false")
    check("validator_not_peer_review", pub_auth.get("validator_pass_is_peer_review") is False, "validator is not peer review")
    check("human_submission_gate", pub_auth.get("human_submission_gate_required") is True, "human submission gate required")

    check("math_child_completed", math_child.get("status") == "completed", "mathematics child complete")
    check("math_payload_type", math_child.get("payload", {}).get("payload_type") == "theorem_with_hypotheses_and_proof", "qualifying mathematical payload")
    check("math_payload_count", len(math_child.get("payload", {}).get("new_mathematical_payload", [])) >= 5, "new mathematical payload present")
    check("phil_child_completed", phil_child.get("status") == "completed", "philosophy child complete")
    check("phil_payload_type", phil_child.get("payload", {}).get("payload_type") == "countermodel_or_obstruction", "qualifying philosophical payload")
    check("children_shared_boundary", math_child.get("claim_boundary_id") == phil_child.get("claim_boundary_id") == "CB-V21-P14-T05-NEGATIVE-RESULT-SUCCESS-001", "shared child claim boundary")
    check("conflicts_resolved", conflict.get("unresolved_conflict_count") == 0, "no unresolved parent conflict")
    check("conflict_count", len(conflict.get("tensions", [])) == 5, "five reviewed tensions")
    check("fusion_proceeds", conflict.get("fusion_disposition", {}).get("proceed") is True, "parent fusion proceeds")
    check("fusion_notes_boundary", "No external human review" in fusion, "fusion notes preserve review boundary")

    tex_tokens = [
        "Exact question record",
        "Negative-result strength ladder",
        "Finite minimum-extension signatures",
        "No global conclusion from an incomplete universe",
        "Conservative classification of the EqSrc frontier",
        "Provisional EqSrc extension signatures",
        "Closure and reopening policy",
        "Publication-readiness criteria",
        "Distance-to-GR disposition",
        "draft/control",
    ]
    for index, token in enumerate(tex_tokens, start=1):
        check(f"tex_required_section_{index:02d}", token in tex, f"TeX contains {token}")

    source_hashes = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
        "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
        "ontology/tex/aether_flow_geometry.tex": "ad43e3408fe2d9686a52a71de7ab8326668e8f04ebe2d2845986898b7d2c000f",
        "research_control/tasks/RT-20260720-021/jobs/completions/AJC-AJ-RT-20260720-021-001.yaml": "35c4b7e44cc1dbf73f9e908b1452ee967ed73d3c1908d40d0566322172f769a0",
        "research_control/tasks/RT-20260720-029/jobs/completions/AJC-AJ-RT-20260720-029-001.yaml": "17e8314c2a5ae3aa257b693cd20df9fa055c3abb2bf1e8b890776d70544b8bf1",
        "research_control/tasks/RT-20260722-019/jobs/completions/AJC-AJ-RT-20260722-019-001.yaml": "1996cb234816a9043ea8928661314055570ec1c9c872a7331d0a2a0ef8da5eec",
        "research_control/tasks/RT-20260722-019/artifacts/no_target_positive_provenance_sufficiency_policy_v1.tex": "52c30a55019d38dbc5cb697749189dba4a0bc17db9566dd4c505b21f7db2e456",
    }
    for index, (relative, expected_hash) in enumerate(source_hashes.items(), start=1):
        path = ROOT / relative
        check(f"source_hash_{index:02d}", path.exists() and sha256(path) == expected_hash, f"immutable source {relative}")

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "negative_result_success_validation_report_v1",
        "task_id": "RT-20260722-020",
        "job_id": "AJ-RT-20260722-020-001",
        "plan_task_id": "P14-T05",
        "validation_status": f"{'PASS' if not failures else 'FAIL'}_{len(checks)}_CHECKS",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "checks": checks,
        "authority_summary": {
            "exact_scope_policy_complete": not failures,
            "same_milestone_continuation_open": True,
            "general_eqsrc_discharged": False,
            "global_no_go_established": False,
            "future_extension_impossibility_established": False,
            "scientific_ledger_changed": False,
            "ontology_changed": False,
            "publication_authorized": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    if args.check:
        if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != rendered:
            report["validation_status"] = "FAIL_REPORT_DRIFT"
            report["failure_count"] = int(report.get("failure_count", 0)) + 1
    if args.json:
        print(json.dumps({
            "validation_status": report["validation_status"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "failure_count": report["failure_count"],
            "report_path": str(REPORT_PATH.relative_to(ROOT)),
        }, sort_keys=True))
    return 0 if report["validation_status"].startswith("PASS") and report["failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
