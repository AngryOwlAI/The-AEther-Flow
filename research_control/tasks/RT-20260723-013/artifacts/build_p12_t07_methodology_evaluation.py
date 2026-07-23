#!/usr/bin/env python3
"""Build deterministic P12-T07 methodology-evaluation artifacts.

This task-local builder reads only hash-bound predecessor evidence. It reports
decision hygiene and identifiability; it does not infer theorem truth,
scientific status, causal superiority, or physics progress.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "research_control/tasks/RT-20260723-013"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
CREATED_AT = "2026-07-23T20:19:27Z"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/v21_recommendation_backlog.yaml": "849a4e8dfe848e80bc0c8236252b924e636e5c95ac1a090478a69f7f5377559f",
    "research_control/handoffs/handoff-0845.yaml": "ccd5dad7312905d771e72451db31b8e0175b7c507ff8efdbdc3ad8146eac18e1",
    "research_control/tasks/RT-20260722-012/artifacts/physics_payload_admission_report.json": "01599b670aa33468ef8759197aa226914b2647f7c2f06eda3af1ae830f590d19",
    "research_control/tasks/RT-20260722-013/artifacts/family_freeze_validation_report.json": "660382dd28e09a312f56e51d041c6696671b2e23d732afafaa1909298e9a023a",
    "research_control/tasks/RT-20260722-014/artifacts/dual_budget_validation_report.json": "03732b26ff2d88e887c4dce0b793cbb21f1c2df07570bf33b82fac9d63cd2082",
    "research_control/tasks/RT-20260722-015/artifacts/ordinary_route_guard_validation_report.json": "6dfd2a1c941ec26051f46d5b6e7494efea9590d6b1f8d87b4bafa0c73763c950",
    "research_control/tasks/RT-20260722-010/artifacts/review_agreement_and_leakage_analysis.json": "8e57d7813843fd9f383a930773876018c64cc622763960277052e789c01808b4",
    "research_control/tasks/RT-20260722-011/artifacts/p11_scientific_qa_compact_receipt.json": "e99347c8ad1864deda009bdbedabdc79553992d976030477fb3975dc5dce7368",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_validation_report.json": "6082c5c23d93741f01e61dcdf48c76fe4c7b723605440261dea95c94c399fd6e",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_compact_receipt.json": "5aeeb1c5b33b229843b5033d85b66098719b50ec1e775a8ae2e46df832801ffa",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json": "788289c942bdcc5fff2f1337998f50d2b6fe89ca541de65a0ae24a651da97489",
    "research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json": "f32e7d272d3d99a339a2cfd81e56b1d44e51e1449b2e34e9dd111161397c1ba2",
    "research_control/tasks/RT-20260723-004/artifacts/fixtures/scientific_quality_metric_cases.json": "60bcb8819734e5e565b08a46b29e85ebffde14f6c1e33dd13cfdd1c02628d003",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_calibration_warning_policy_v1.md": "b9b4e4fcc603c9eee508456999936a4e0378b188235f73f35c454009728648cb",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_metric_taxonomy_v1.md": "b2e31738a445e68e4de6ea20381886bcd6c3747cccd693187f0904a7742ad308",
    "research_control/tasks/RT-20260723-004/artifacts/validate_scientific_quality_metrics.py": "e4102ac5ce28653e9c8195762aeb519c1f5c08e615aa03221d18b0906fd73260",
    "scripts/research_control/render_ai_methodology_metrics_dashboard.py": "059ff7191575cb865fac020c010314901e04aa11e0054706866be62b81ac17af",
    "scripts/research_control/report_physics_progress_metrics.py": "07cd220950e4b85632385da1dcaa932c8a6c48c50b33e2736dd6f181bc9abfd1",
    "scripts/research_control/scientific_quality_metrics.py": "2e9b443da0e9beeccd08a54936972a8438ba64b7fcc12dccd4d4793b7111ccc9",
    "research_control/tasks/RT-20260723-011/artifacts/attempt_rework_dashboard.json": "5fc9a671fe5212d6623905dc7d4cef9a89d56ba9f189f42caf01c4c7587e1c32",
    "research_control/tasks/RT-20260723-011/artifacts/attempt_rework_compact_receipt.json": "4cc99fbe23855f6e59e21f46a66fe195d2f8a04c4239df5a003cd2bb2c5578e2",
}

CHILD_PATHS = {
    "child_phys_math": "research_control/tasks/RT-20260723-013/artifacts/child_phys_math_methodology_ablation.yaml",
    "child_phys_phil": "research_control/tasks/RT-20260723-013/artifacts/child_phys_phil_methodology_ablation.yaml",
    "conflict_review": "research_control/tasks/RT-20260723-013/artifacts/parent_conflict_review_methodology_ablation.yaml",
    "fusion_notes": "research_control/tasks/RT-20260723-013/artifacts/parent_fusion_notes_methodology_ablation.md",
}

OUTPUT_PATHS = {
    "results": "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_ablation_results.json",
    "memo": "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_evaluation_memo.md",
    "limitations": "research_control/tasks/RT-20260723-013/artifacts/p12_t07_limitations_and_next_study.md",
    "receipt": "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_compact_receipt.json",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(relative_path: str) -> str:
    return sha256_bytes((ROOT / relative_path).read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_bound_json(relative_path: str) -> dict[str, Any]:
    observed = sha256_path(relative_path)
    expected = SOURCE_HASHES[relative_path]
    if observed != expected:
        raise ValueError(
            f"source hash mismatch for {relative_path}: {observed} != {expected}"
        )
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def load_bound_yaml(relative_path: str) -> dict[str, Any]:
    observed = sha256_path(relative_path)
    expected = SOURCE_HASHES[relative_path]
    if observed != expected:
        raise ValueError(
            f"source hash mismatch for {relative_path}: {observed} != {expected}"
        )
    value = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping in {relative_path}")
    return value


def load_child(relative_path: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping in {relative_path}")
    return value


def count_where(rows: list[dict[str, Any]], field: str, value: str) -> int:
    return sum(1 for row in rows if row.get(field) == value)


def build_results() -> dict[str, Any]:
    payload_path = (
        "research_control/tasks/RT-20260722-012/artifacts/"
        "physics_payload_admission_report.json"
    )
    family_path = (
        "research_control/tasks/RT-20260722-013/artifacts/"
        "family_freeze_validation_report.json"
    )
    route_path = (
        "research_control/tasks/RT-20260722-015/artifacts/"
        "ordinary_route_guard_validation_report.json"
    )
    dual_budget_path = (
        "research_control/tasks/RT-20260722-014/artifacts/"
        "dual_budget_validation_report.json"
    )
    review_path = (
        "research_control/tasks/RT-20260722-010/artifacts/"
        "review_agreement_and_leakage_analysis.json"
    )
    qa_path = (
        "research_control/tasks/RT-20260722-011/artifacts/"
        "p11_scientific_qa_compact_receipt.json"
    )
    quality_path = (
        "research_control/tasks/RT-20260723-004/artifacts/"
        "scientific_quality_validation_report.json"
    )
    quality_receipt_path = (
        "research_control/tasks/RT-20260723-004/artifacts/"
        "scientific_quality_compact_receipt.json"
    )
    attempt_path = (
        "research_control/tasks/RT-20260723-011/artifacts/"
        "attempt_rework_dashboard.json"
    )
    attempt_receipt_path = (
        "research_control/tasks/RT-20260723-011/artifacts/"
        "attempt_rework_compact_receipt.json"
    )
    handoff_path = "research_control/handoffs/handoff-0845.yaml"

    payload = load_bound_json(payload_path)
    family = load_bound_json(family_path)
    dual_budget = load_bound_json(dual_budget_path)
    ordinary = load_bound_json(route_path)
    review = load_bound_json(review_path)
    qa = load_bound_json(qa_path)
    quality = load_bound_json(quality_path)
    quality_receipt = load_bound_json(quality_receipt_path)
    attempt = load_bound_json(attempt_path)
    attempt_receipt = load_bound_json(attempt_receipt_path)
    handoff = load_bound_yaml(handoff_path)

    payload_rows = payload["results"]
    payload_rejected = [
        row for row in payload_rows if row.get("observed_status") == "rejected"
    ]
    payload_admitted = [
        row for row in payload_rows if row.get("observed_status") == "admitted"
    ]
    payload_legacy = [
        row
        for row in payload_rows
        if row.get("observed_status") == "legacy_readable"
    ]

    family_rows = family["results"]
    repeated_cycle_ids = {
        "frozen_family_repeat_blocked",
        "renamed_same_assumption_blocked",
        "rename_or_repackage_always_barred",
    }
    repeated_cycle_suppressed = [
        row for row in family_rows if row.get("case_id") in repeated_cycle_ids
    ]
    lawful_family_routes = [
        row
        for row in family_rows
        if str(row.get("observed_status", "")).startswith("admitted")
    ]

    route_rows = ordinary["case_results"]
    dual_budget_rows = dual_budget["results"]
    live_guard = handoff["ordinary_route_guard"]

    reviewer_metrics = review["reviewer_metric_aggregate"]["metrics"]
    context_counts = review["review_context_classification_counts"]
    qa_finding_counts = qa["finding_counts"]
    quality_source_mismatches = []
    for path, embedded_sha256 in sorted(quality["source_hashes"].items()):
        observed_sha256 = sha256_path(path)
        if observed_sha256 != embedded_sha256:
            quality_source_mismatches.append(
                {
                    "path": path,
                    "embedded_sha256": embedded_sha256,
                    "observed_sha256": observed_sha256,
                }
            )

    source_bindings = [
        {"path": path, "sha256": expected}
        for path, expected in sorted(SOURCE_HASHES.items())
    ]
    synthesis_bindings = [
        {
            "kind": kind,
            "path": path,
            "sha256": sha256_path(path),
        }
        for kind, path in CHILD_PATHS.items()
    ]

    results = {
        "schema_id": "v21_p12_t07_methodology_ablation_results_v1",
        "task_id": "RT-20260723-013",
        "plan_task_id": "P12-T07",
        "created_at": CREATED_AT,
        "status": "PASS_CALIBRATED_WITH_SOURCE_INTEGRITY_DEFECT",
        "evaluation_design": {
            "design": "retrospective_hash_bound_fixture_and_route_history_ablation",
            "unit_of_analysis": [
                "policy fixture case",
                "reviewed object by assessment axis",
                "bounded attempt-ledger event",
                "live ordinary-route decision",
            ],
            "control_on_basis": "exact predecessor reports and tracked live handoff",
            "control_off_basis": "guard-removal exposure analysis only",
            "causal_inference_status": "not_identified",
            "scientific_outcome_ground_truth_available": False,
            "randomized_assignment_present": False,
            "pre_registered_outcome_present": False,
        },
        "mechanisms": [
            {
                "mechanism_id": "physics_payload_admission_gate",
                "control_on": {
                    "case_count": len(payload_rows),
                    "rejected_case_count": len(payload_rejected),
                    "admitted_case_count": len(payload_admitted),
                    "legacy_readable_case_count": len(payload_legacy),
                    "rejected_case_ids": [
                        row["case_id"] for row in payload_rejected
                    ],
                },
                "control_off_ablation": {
                    "kind": "unchecked_exposure_not_observed_admission",
                    "guarded_exposure_count": len(payload_rejected),
                    "interpretation": "Without the gate these five fixture risks lose this specific hard rejection; the analysis does not assert that every risk would have entered production.",
                },
                "decision_relevance": "supported",
                "research_outcome_effect": "not_identified",
                "verdict": "bounded_support_for_admission_selectivity",
            },
            {
                "mechanism_id": "family_freeze_and_reopening_gate",
                "control_on": {
                    "case_count": len(family_rows),
                    "repeated_cycle_suppression_count": len(
                        repeated_cycle_suppressed
                    ),
                    "lawful_route_preservation_count": len(lawful_family_routes),
                    "frozen_family_count": family["freeze_count"],
                    "global_no_go_inferred": family["global_no_go_inferred"],
                },
                "control_off_ablation": {
                    "kind": "repeat_guard_removed_exposure",
                    "repeat_or_repackage_exposure_count": len(
                        repeated_cycle_suppressed
                    ),
                    "interpretation": "The ablation exposes three repeated-family or repackaging cases to reconsideration while leaving other schema and human-gate checks conceptually intact.",
                },
                "decision_relevance": "supported",
                "research_outcome_effect": "not_identified",
                "verdict": "bounded_support_for_orbit_suppression_with_open_distinct_routes",
            },
            {
                "mechanism_id": "dual_budget_and_ordinary_route_guard",
                "control_on": {
                    "dual_budget_fixture_case_count": len(dual_budget_rows),
                    "dual_budget_admitted_count": count_where(
                        dual_budget_rows, "observed_status", "admitted"
                    ),
                    "dual_budget_rejected_count": count_where(
                        dual_budget_rows, "observed_status", "rejected"
                    ),
                    "dual_budget_rejected_error_count": sum(
                        row["error_count"]
                        for row in dual_budget_rows
                        if row["observed_status"] == "rejected"
                    ),
                    "dual_budget_category_coverage": dual_budget[
                        "category_coverage"
                    ],
                    "system_success_counts_as_physics": dual_budget[
                        "system_success_counts_as_physics"
                    ],
                    "system_success_counts_as_distance_to_gr": dual_budget[
                        "system_success_counts_as_distance_to_gr"
                    ],
                    "fixture_case_count": len(route_rows),
                    "fixture_fail_expected_count": count_where(
                        route_rows, "observed_status", "FAIL"
                    ),
                    "fixture_warn_expected_count": count_where(
                        route_rows, "observed_status", "WARN"
                    ),
                    "fixture_pass_expected_count": count_where(
                        route_rows, "observed_status", "PASS"
                    ),
                    "live_consecutive_project_system_tasks": live_guard[
                        "consecutive_project_system_tasks_before_selection"
                    ],
                    "live_ready_science_plan_task_ids": live_guard[
                        "ready_science_plan_task_ids"
                    ],
                    "live_selected_plan_task_id": live_guard[
                        "selected_plan_task_id"
                    ],
                    "live_outcome": live_guard["outcome"],
                },
                "control_off_ablation": {
                    "kind": "route_constraint_removed",
                    "dual_budget_rejection_exposure_count": count_where(
                        dual_budget_rows, "observed_status", "rejected"
                    ),
                    "live_counterfactual_route": "indeterminate",
                    "interpretation": "Removing the dual-budget evaluator exposes seven malformed allocation fixtures, while removing the ordinary-route guard leaves the live counterfactual route indeterminate. The tracked evidence proves taxonomy-compliant guard engagement at a nine-task project-system run, not actual physics progress or which route an unconstrained Director would have selected.",
                },
                "decision_relevance": "supported_live_and_fixture",
                "research_outcome_effect": "not_identified",
                "verdict": "bounded_support_for_budget_separation_and_route_intervention",
            },
            {
                "mechanism_id": "review_context_diversity",
                "control_on": {
                    "review_record_count": review["review_record_count"],
                    "reviewed_object_count": review["reviewed_object_count"],
                    "eligible_cross_context_axis_count": reviewer_metrics[
                        "eligible_pair_axis_comparison_count"
                    ],
                    "assessment_disagreement_count": reviewer_metrics[
                        "assessment_disagreement_count"
                    ],
                    "exact_agreement_count": reviewer_metrics[
                        "exact_assessment_agreement_count"
                    ],
                    "false_consensus_risk_count": reviewer_metrics[
                        "false_consensus_risk_count"
                    ],
                    "context_classification_counts": context_counts,
                    "p11_repair_required_count": qa_finding_counts[
                        "repair_required"
                    ],
                },
                "control_off_ablation": {
                    "kind": "single_context_projection",
                    "cross_context_disagreements_not_observable_count": reviewer_metrics[
                        "assessment_disagreement_count"
                    ],
                    "interpretation": "Removing either context arm eliminates the paired comparison that surfaced three configuration-sensitive assessments.",
                },
                "decision_relevance": "mixed",
                "research_outcome_effect": "not_identified",
                "verdict": "partial_support_for_context_variation_insufficient_for_reviewer_independence",
            },
            {
                "mechanism_id": "denominator_bound_scientific_quality_metrics",
                "control_on": {
                    "metric_count": quality["metric_count"],
                    "live_measured_count": quality["live_status_counts"][
                        "measured"
                    ],
                    "live_not_measured_count": quality["live_status_counts"][
                        "not_measured"
                    ],
                    "live_invalid_count": quality["live_status_counts"]["invalid"],
                    "fixture_case_count": quality["fixture_case_count"],
                    "check_count": quality["check_count"],
                    "stored_report_status": quality["status"],
                    "stored_receipt_status": quality_receipt["status"],
                    "live_source_binding_status": (
                        "stale" if quality_source_mismatches else "current"
                    ),
                    "live_source_hash_mismatch_count": len(
                        quality_source_mismatches
                    ),
                    "live_source_hash_mismatches": quality_source_mismatches,
                },
                "control_off_ablation": {
                    "kind": "volume_proxy_or_zero_fill_exposure",
                    "unknown_population_misread_exposure_count": quality[
                        "live_status_counts"
                    ]["not_measured"],
                    "interpretation": "Without denominator-bound status, five unknown live populations are exposed to false-zero or volume-proxy interpretation; no historical decision is asserted to have made that error.",
                },
                "decision_relevance": "integrity_qualified",
                "research_outcome_effect": "not_identified",
                "verdict": "definition_level_support_only_pending_source_reseal",
            },
        ],
        "attempt_rework_visibility": {
            "event_count": attempt["bounded_scope"]["event_count"],
            "represented_task_count": attempt["bounded_scope"][
                "represented_task_count"
            ],
            "validation_catch_count": attempt["headline_counts"][
                "validation_catch_count"
            ],
            "audit_objection_count": attempt["headline_counts"][
                "audit_objection_count"
            ],
            "repair_event_count": attempt["headline_counts"]["repair_event_count"],
            "physics_failure_count": attempt["failure_categories"]["physics"],
            "abandonment_status": attempt["abandonment_metric"]["status"],
            "historical_completeness_claimed": attempt["bounded_scope"][
                "historical_completeness_claimed"
            ],
            "source_receipt_result": attempt_receipt["result_status"],
            "verdict": "bounded_visibility_only",
        },
        "cross_mechanism_assessment": {
            "bounded_support_mechanism_count": 3,
            "mixed_support_mechanism_count": 1,
            "integrity_qualified_mechanism_count": 1,
            "causal_superiority_established_count": 0,
            "calibrated_conclusion": "The evidence supports bounded decision selectivity and route intervention in fixed fixtures and one live route. Reviewer-context evidence is mixed. Quality-metric semantics are definition-level only because the stored P12-T05 report and receipt are stale against three live sources. No effect on scientific truth, theorem survival, or Distance-to-GR progress is identified.",
            "work_item_disposition": "completed_with_causal_and_source_integrity_limitations",
        },
        "confounders": [
            "Most policy results are authored fixtures rather than randomized production comparisons.",
            "The live ordinary-route result is one selected route after nine project-system tasks and has no observed no-guard twin.",
            "The attempt ledger contains eight bounded events across seven tasks and explicitly disclaims historical completeness.",
            "The reviewer comparison uses same-model internal AI contexts; different-model, human-expert, and independent-replication counts are zero.",
            "Five of eight live durable-quality metrics remain not_measured because eligible denominators are absent.",
            "The stored P12-T05 quality report and receipt embed stale hashes for the taxonomy, calibration policy, and fixture corpus; the current predecessor validator returns FAIL until those artifacts are resealed.",
            "Mechanisms were introduced sequentially and interact, so isolated effect sizes are not identified.",
            "Validator and checkpoint PASS establish operational conformity only.",
        ],
        "source_bindings": source_bindings,
        "synthesis_bindings": synthesis_bindings,
        "authority_boundary": {
            "methodology_evidence_is_physics_progress": False,
            "theorem_truth_evaluated": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "external_review_completed": False,
            "human_expert_review_completed": False,
            "independent_replication_completed": False,
            "causal_superiority_established": False,
            "ontology_adoption_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authority": False,
        },
    }
    return results


def render_memo(results: dict[str, Any]) -> str:
    by_id = {row["mechanism_id"]: row for row in results["mechanisms"]}
    payload = by_id["physics_payload_admission_gate"]
    family = by_id["family_freeze_and_reopening_gate"]
    route = by_id["dual_budget_and_ordinary_route_guard"]
    review = by_id["review_context_diversity"]
    quality = by_id["denominator_bound_scientific_quality_metrics"]
    attempts = results["attempt_rework_visibility"]
    quality_mismatches = quality["control_on"]["live_source_hash_mismatches"]
    quality_mismatch_paths = ", ".join(
        f"`{row['path']}`" for row in quality_mismatches
    )
    return f"""<!-- authority: science_draft -->

# P12-T07 governance and methodology evaluation

## Result

The five reforms show bounded evidence of better decision hygiene, but the
available record does not identify a causal improvement in scientific truth or
Distance-to-GR progress. Four mechanisms have direct fixture or live-route
support for the control behavior they were designed to provide. Reviewer
context variation has mixed support: it surfaced disagreements, but every
executed review remained internal and correlated.

This is a methodology result. It is not physics evidence, theorem proof,
ontology adoption, external review, independent replication, or promotion
authority.

## Evaluation design

The study is a retrospective, hash-bound fixture and route-history ablation.
“Control on” means the exact tracked policy result. “Control off” means only
that the named guard is removed from the same fixed case. It is an exposure
analysis, not an observed alternate history. There is no randomized assignment,
pre-registered scientific outcome, or complete historical attempt population.

## Mechanism findings

### Physics-payload admission

The gate evaluated {payload["control_on"]["case_count"]} cases, rejected
{payload["control_on"]["rejected_case_count"]}, admitted
{payload["control_on"]["admitted_case_count"]}, and preserved
{payload["control_on"]["legacy_readable_case_count"]} legacy-readable case.
Removing this gate exposes {payload["control_off_ablation"]["guarded_exposure_count"]}
fixture risks to unchecked admission. This supports admission selectivity; it
does not show that admitted payloads are true or scientifically valuable.

### Family freeze and reopening

The policy evaluated {family["control_on"]["case_count"]} cases, suppressed
{family["control_on"]["repeated_cycle_suppression_count"]} repeat or
repackaging cases, and preserved
{family["control_on"]["lawful_route_preservation_count"]} lawful distinct,
reopened, or unfrozen routes. Five families remain locally frozen without a
global no-go inference. This supports route-orbit control while keeping
materially distinct work open.

### Dual budgets and ordinary-route guard

The dual-budget evaluator admitted {route["control_on"]["dual_budget_admitted_count"]}
and rejected {route["control_on"]["dual_budget_rejected_count"]} of
{route["control_on"]["dual_budget_fixture_case_count"]} fixed cases. All
{route["control_on"]["fixture_case_count"]} ordinary-route guard cases matched
their expected result. In the live handoff, the guard was decision-relevant after
{route["control_on"]["live_consecutive_project_system_tasks"]} consecutive
project-system tasks and selected
`{route["control_on"]["live_selected_plan_task_id"]}` while preserving the
human gate on the other ready item. The no-guard live route is unobserved, so
the evidence supports taxonomy-compliant intervention and budget separation,
not actual physics progress or a causal outcome gain. A plan-classified,
physics-facing route is not physics evidence.

### Reviewer context variation

Four internal reviews of two objects produced
{review["control_on"]["assessment_disagreement_count"]} disagreements across
{review["control_on"]["eligible_cross_context_axis_count"]} paired axes, with
{review["control_on"]["false_consensus_risk_count"]} exact-agreement axes still
flagged for correlated-review risk. Removing either context arm would make the
three paired disagreements unobservable. Different-model, human-expert, and
independent-replication counts remain zero. Context variation is useful; broad
reviewer-diversity benefit is not yet established.

### Durable quality metrics

Eight denominator-bound metrics yielded
{quality["control_on"]["live_measured_count"]} measured and
{quality["control_on"]["live_not_measured_count"]} not-measured live values.
Their stored report and compact receipt are stale against
{quality["control_on"]["live_source_hash_mismatch_count"]} live inputs:
{quality_mismatch_paths}. The predecessor validator currently returns FAIL
until those task-local artifacts are resealed. The metric definitions preserve
unknown denominators and demote raw volume to operational context, but the
reported validation counts are integrity-qualified rather than reproducible
current evidence. This does not create an aggregate scientific-truth score.

## Route-history and rework visibility

The bounded attempt projection contains {attempts["event_count"]} events across
{attempts["represented_task_count"]} tasks, including
{attempts["validation_catch_count"]} validation catch,
{attempts["audit_objection_count"]} audit objection, and
{attempts["repair_event_count"]} repair events. It records zero physics-failure
events, which must not be read as a zero physics-failure rate because the
population is incomplete and abandonment is not measured.

## Calibrated conclusion

The controls improve observable process selectivity, preserve lawful
alternatives, force a live route intervention, and expose context-sensitive
review differences in the bounded corpus. Quality-metric wording and
denominator semantics remain useful, but its stored validation evidence has a
source-integrity defect and needs a separate project-system reseal.
No available comparison identifies whether those changes improve theorem
truth, independent survival, empirical adequacy, or progress toward deriving
GR. P12-T07 is therefore complete as a calibrated methodology evaluation with
causal limitations.

## Parent-child synthesis

The Physicist-Mathematician child supplied the count reconstruction,
counterfactual identifiability classification, and denominator discipline. The
Physicist-Philosopher child supplied the methodology/science distinction,
Goodhart and authority analysis, and wording limits. The parent resolved the
central tension by using “bounded support for decision hygiene” and rejecting
“scientific superiority” or causal language.

## References

The Æther-Flow Research Project. (2026a). *Recommendations implementation plan
continue task v21* [Project-control implementation plan].

The Æther-Flow Research Project. (2026b). *P11 scientific QA non-regression
compact receipt* [Project-control audit receipt].

The Æther-Flow Research Project. (2026c). *P12 attempt and rework dashboard*
[Draft/control methodology artifact].
"""


def render_limitations(results: dict[str, Any]) -> str:
    confounders = "\n".join(f"- {item}" for item in results["confounders"])
    return f"""<!-- authority: science_draft -->

# P12-T07 limitations and next-study plan

## Limitations

{confounders}

## What would identify stronger effects

1. Pre-register decision-quality outcomes before new routes are selected.
2. Use a fixed historical corpus with blinded control-on/control-off routing by
   evaluators who did not author the policies.
3. Add different-model, human-expert, and genuinely independent replication
   arms with exact provenance labels.
4. Expand the attempt ledger to a declared complete sampling frame before
   estimating abandonment, repair, or survival rates.
5. Measure denominator-bound outcomes at multiple later checkpoints rather
   than replacing unknown populations with zero.
6. Separate mechanism effects through staged or factorial activation where
   operationally safe.

## Next-study boundary

The next study may strengthen methodology evidence only. It cannot promote a
physics claim, adopt ontology, infer theorem truth from agreement, or treat
system performance as Distance-to-GR progress. P13-T01 is a separate included
work item and is not executed here.
"""


def build_outputs() -> dict[str, str]:
    results = build_results()
    results_text = canonical_json(results)
    memo_text = render_memo(results)
    limitations_text = render_limitations(results)
    output_hashes = {
        OUTPUT_PATHS["results"]: sha256_bytes(results_text.encode("utf-8")),
        OUTPUT_PATHS["memo"]: sha256_bytes(memo_text.encode("utf-8")),
        OUTPUT_PATHS["limitations"]: sha256_bytes(
            limitations_text.encode("utf-8")
        ),
    }
    receipt = {
        "schema_id": "v21_p12_t07_methodology_compact_receipt_v1",
        "task_id": "RT-20260723-013",
        "plan_task_id": "P12-T07",
        "result_status": results["status"],
        "work_item_disposition": results["cross_mechanism_assessment"][
            "work_item_disposition"
        ],
        "source_hashes": dict(sorted(SOURCE_HASHES.items())),
        "synthesis_hashes": {
            path: sha256_path(path) for path in CHILD_PATHS.values()
        },
        "output_hashes": output_hashes,
        "mechanism_count": len(results["mechanisms"]),
        "bounded_support_mechanism_count": results[
            "cross_mechanism_assessment"
        ]["bounded_support_mechanism_count"],
        "mixed_support_mechanism_count": results[
            "cross_mechanism_assessment"
        ]["mixed_support_mechanism_count"],
        "integrity_qualified_mechanism_count": results[
            "cross_mechanism_assessment"
        ]["integrity_qualified_mechanism_count"],
        "source_integrity_mismatch_count": len(
            next(
                item
                for item in results["mechanisms"]
                if item["mechanism_id"]
                == "denominator_bound_scientific_quality_metrics"
            )["control_on"]["live_source_hash_mismatches"]
        ),
        "causal_superiority_established_count": 0,
        "attempt_event_count": results["attempt_rework_visibility"]["event_count"],
        "confounder_count": len(results["confounders"]),
        "validator_ids": [
            "source_hash_exactness",
            "payload_gate_ablation_counts",
            "family_freeze_ablation_counts",
            "ordinary_route_live_and_fixture_counts",
            "review_context_disagreement_counts",
            "quality_metric_status_counts",
            "attempt_rework_visibility_counts",
            "parent_child_synthesis",
            "causal_identifiability_guard",
            "methodology_science_authority_boundary",
        ],
        "claim_boundary_summary": "Bounded methodology evidence supports decision hygiene in fixed fixtures and one live route; causal scientific superiority theorem truth ontology Distance-to-GR promotion proof publication and external-review claims remain unauthorized.",
        "authority": results["authority_boundary"],
    }
    return {
        OUTPUT_PATHS["results"]: results_text,
        OUTPUT_PATHS["memo"]: memo_text,
        OUTPUT_PATHS["limitations"]: limitations_text,
        OUTPUT_PATHS["receipt"]: canonical_json(receipt),
    }


def write_outputs(outputs: dict[str, str]) -> None:
    for relative_path, content in outputs.items():
        path = ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.write:
        write_outputs(outputs)
    print(
        canonical_json(
            {
                "status": "PASS",
                "write_performed": args.write,
                "output_hashes": {
                    path: sha256_bytes(content.encode("utf-8"))
                    for path, content in outputs.items()
                },
            }
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
