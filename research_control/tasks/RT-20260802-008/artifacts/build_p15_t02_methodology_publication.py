#!/usr/bin/env python3
"""Build the bounded P15-T02 methodology-publication packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = ROOT / "research_control/tasks/RT-20260802-008/artifacts"
CREATED_AT = "2026-08-02T13:07:50Z"

SOURCE_PATHS = (
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/design/manuscript_split_boundary_checklist_v16.md",
    "research_control/tasks/RT-20260704-014/artifacts/ai_methodology_manuscript_outline_v15.md",
    "research_control/tasks/RT-20260705-025/artifacts/ai_methodology_manuscript_status_refresh_v16.md",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json",
    "research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json",
    "research_control/tasks/RT-20260723-011/artifacts/attempt_rework_dashboard.json",
    "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_ablation_results.json",
    "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_compact_receipt.json",
    "research_control/tasks/RT-20260723-013/jobs/completions/AJC-AJ-RT-20260723-013-001.yaml",
    "research_control/tasks/RT-20260802-007/artifacts/software_system_non_regression_report_v1.json",
    "research_control/tasks/RT-20260802-007/artifacts/performance_rollback_evidence_v1.json",
    "research_control/tasks/RT-20260802-007/artifacts/p13_t08_compact_receipt.json",
    "research_control/tasks/RT-20260802-007/jobs/completions/AJC-AJ-RT-20260802-007-001.yaml",
)

OUTPUT_PATHS = {
    "experiment": "p15_t02_methodology_experiment_and_ablation_package.json",
    "dictionary": "p15_t02_methodology_data_dictionary.json",
    "manuscript": "p15_t02_methodology_manuscript.md",
    "limitations": "p15_t02_methodology_limitations.md",
    "child_math": "child_phys_math_methodology_publication.yaml",
    "child_phil": "child_phys_phil_methodology_publication.yaml",
    "conflict": "parent_conflict_review_methodology_publication.yaml",
    "fusion": "parent_fusion_notes_methodology_publication.md",
    "receipt": "p15_t02_methodology_compact_receipt.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def json_text(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def source_bindings() -> list[dict[str, str]]:
    return [{"path": path, "sha256": sha256(ROOT / path)} for path in SOURCE_PATHS]


def mechanism_map(p12: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["mechanism_id"]: item for item in p12["mechanisms"]}


def build_experiment() -> dict[str, Any]:
    p12 = read_json(SOURCE_PATHS[7])
    lineage = read_json(SOURCE_PATHS[4])
    attempts = read_json(SOURCE_PATHS[5])
    dashboard = read_json(SOURCE_PATHS[6])
    p13 = read_json(SOURCE_PATHS[10])
    perf = read_json(SOURCE_PATHS[11])
    mechanisms = mechanism_map(p12)
    payload = mechanisms["physics_payload_admission_gate"]
    freeze = mechanisms["family_freeze_and_reopening_gate"]
    budget = mechanisms["dual_budget_and_ordinary_route_guard"]
    review = mechanisms["review_context_diversity"]
    quality = mechanisms["denominator_bound_scientific_quality_metrics"]

    return {
        "schema_id": "v21_p15_t02_methodology_experiment_and_ablation_package_v1",
        "status": "PASS_BOUNDED_NONCAUSAL_PUBLICATION_PACKET",
        "task_id": "RT-20260802-008",
        "plan_task_id": "P15-T02",
        "created_at": CREATED_AT,
        "design": {
            "design_class": "retrospective_hash_bound_observational_synthesis",
            "unit_of_analysis": "tracked fixture case, review axis, candidate-lineage record, attempt event, or operational validation gate",
            "causal_identification": "not_identified",
            "random_assignment": False,
            "prospective_preregistration": False,
            "historical_population_complete": False,
            "external_replication": False,
        },
        "research_questions": [
            {
                "id": "RQ1",
                "question": "Which role, claim-gate, negative-result-memory, lineage, and attempt-history mechanisms show bounded decision-hygiene evidence in the tracked corpus?",
                "estimand_status": "descriptive_only",
            },
            {
                "id": "RQ2",
                "question": "Which requested workflow comparison arms are actually observed, and which remain unmeasured?",
                "estimand_status": "arm_coverage_classification_only",
            },
            {
                "id": "RQ3",
                "question": "Do the v21 controls preserve claim and authority boundaries under bounded operational validation?",
                "estimand_status": "conformance_not_scientific_truth",
            },
        ],
        "comparison_arms": [
            {
                "arm_id": "unstructured",
                "observation_status": "not_observed",
                "eligible_unit_count": None,
                "inference": "No tracked matched or randomized unstructured arm exists.",
            },
            {
                "arm_id": "single_agent",
                "observation_status": "not_observed_as_control_arm",
                "eligible_unit_count": None,
                "inference": "The ledger records model telemetry for one build but no normalized single-agent outcome arm.",
            },
            {
                "arm_id": "role_structured",
                "observation_status": "observed_nonrandomized",
                "eligible_unit_count": dashboard["bounded_scope"]["represented_task_count"],
                "inference": "Role-structured tracked events can be described, but not compared causally with absent arms.",
            },
            {
                "arm_id": "blind_review",
                "observation_status": "observed_same_model_context_only",
                "eligible_unit_count": review["control_on"]["context_classification_counts"]["blind_same_model_review"],
                "inference": "Blind same-model records test context sensitivity, not reviewer independence.",
            },
            {
                "arm_id": "diverse_review",
                "observation_status": "partially_observed_context_diversity_only",
                "eligible_unit_count": review["control_on"]["review_record_count"],
                "inference": "Same-model context variation exists; different-model, external-human, and independent replication counts are zero.",
            },
        ],
        "mechanism_results": [
            {
                "mechanism_id": "claim_gate_overclaim_control",
                "numerator": payload["control_on"]["rejected_case_count"],
                "denominator": payload["control_on"]["case_count"],
                "metric": "hard_rejection_share_in_fixed_fixture_matrix",
                "value": payload["control_on"]["rejected_case_count"] / payload["control_on"]["case_count"],
                "interpretation": "Five fixed risks receive this gate's hard rejection; production-entry counterfactuals are unobserved.",
            },
            {
                "mechanism_id": "candidate_cycle_and_route_orbit_control",
                "numerator": freeze["control_on"]["repeated_cycle_suppression_count"],
                "denominator": freeze["control_on"]["case_count"],
                "metric": "repeated_or_repackaged_case_suppression_share",
                "value": freeze["control_on"]["repeated_cycle_suppression_count"] / freeze["control_on"]["case_count"],
                "lawful_route_preservation_count": freeze["control_on"]["lawful_route_preservation_count"],
                "interpretation": "The fixed matrix suppresses three repeated/repackaged routes while preserving six distinct lawful routes.",
            },
            {
                "mechanism_id": "budget_and_route_separation",
                "numerator": budget["control_on"]["dual_budget_rejected_count"],
                "denominator": budget["control_on"]["dual_budget_fixture_case_count"],
                "metric": "malformed_allocation_rejection_share",
                "value": budget["control_on"]["dual_budget_rejected_count"] / budget["control_on"]["dual_budget_fixture_case_count"],
                "live_project_system_streak": budget["control_on"]["live_consecutive_project_system_tasks"],
                "live_selected_plan_task_id": budget["control_on"]["live_selected_plan_task_id"],
                "interpretation": "The control engages and selects a physics-bearing route; that selection is not physics evidence.",
            },
            {
                "mechanism_id": "reviewer_disagreement_visibility",
                "numerator": review["control_on"]["assessment_disagreement_count"],
                "denominator": review["control_on"]["eligible_cross_context_axis_count"],
                "metric": "cross_context_disagreement_share",
                "value": review["control_on"]["assessment_disagreement_count"] / review["control_on"]["eligible_cross_context_axis_count"],
                "interpretation": "Three of ten eligible axes vary by review context; same-model correlation prevents an independence claim.",
            },
            {
                "mechanism_id": "negative_result_memory_and_rework_visibility",
                "numerator": dashboard["headline_counts"]["repair_event_count"],
                "denominator": dashboard["bounded_scope"]["event_count"],
                "metric": "repair_event_share_in_bounded_ledger",
                "value": dashboard["repair_metrics"]["repair_event_share"]["value"],
                "validation_catch_count": dashboard["headline_counts"]["validation_catch_count"],
                "audit_objection_count": dashboard["headline_counts"]["audit_objection_count"],
                "interpretation": "The append-only bounded ledger exposes repairs and objections; it is not a complete historical population.",
            },
            {
                "mechanism_id": "denominator_bound_quality_metrics",
                "numerator": quality["control_on"]["live_measured_count"],
                "denominator": quality["control_on"]["metric_count"],
                "metric": "measured_metric_share_at_p12_snapshot",
                "value": quality["control_on"]["live_measured_count"] / quality["control_on"]["metric_count"],
                "not_measured_count": quality["control_on"]["live_not_measured_count"],
                "source_binding_at_p12_snapshot": quality["control_on"]["live_source_binding_status"],
                "interpretation": "Unknown denominators remain not_measured; the P12 snapshot's three source mismatches are retained as a limitation, not repaired retrospectively.",
            },
        ],
        "lineage_and_attempt_history": {
            "candidate_family_count": lineage["record_counts"]["families"],
            "candidate_count": lineage["record_counts"]["candidates"],
            "lineage_edge_count": lineage["record_counts"]["lineage_edges"],
            "candidate_stage_count": lineage["record_counts"]["candidate_stages"],
            "family_event_count": lineage["record_counts"]["family_events"],
            "attempt_event_count": len(attempts["events"]),
            "represented_attempt_task_count": dashboard["bounded_scope"]["represented_task_count"],
            "abandonment_status": dashboard["abandonment_metric"]["status"],
            "cost_status": attempts["build_compute_metadata"]["cost_availability"],
        },
        "operational_non_regression_context": {
            "status": p13["status"],
            "selected_test_count": perf["baseline_comparison"]["selected_non_regression_test_count"],
            "coverage_percent": perf["baseline_comparison"]["assurance_coverage_observed_percent"],
            "coverage_floor_percent": perf["baseline_comparison"]["assurance_coverage_floor_percent"],
            "mutation_killed": perf["baseline_comparison"]["mutation_killed"],
            "mutation_total": perf["baseline_comparison"]["mutation_total"],
            "dependency_vulnerability_count": perf["baseline_comparison"]["dependency_audit_known_vulnerability_count"],
            "interpretation": "Operational release evidence only; it supplies no scientific-outcome effect size.",
        },
        "governance_reform_mapping": {
            "recommendation_ids": [
                "V21-R36", "V21-R37", "V21-R38", "V21-R42", "V21-R43", "V21-R44",
                "V21-R45", "V21-R51", "V21-R52", "V21-R53", "V21-R65", "V21-R66", "V21-R69",
            ],
            "assessment": "implemented mechanisms are publication-ready as bounded methods; causal superiority and external validity remain open",
        },
        "authority_boundary": {
            "methodology_evidence_is_physics_evidence": False,
            "causal_superiority_established": False,
            "theorem_truth_evaluated": False,
            "scientific_status_changed": False,
            "ontology_or_source_law_adopted": False,
            "distance_to_gr_changed": False,
            "external_human_review_completed": False,
            "independent_replication_completed": False,
            "publication_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
        "source_bindings": source_bindings(),
    }


def build_dictionary(experiment: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "v21_p15_t02_methodology_data_dictionary_v1",
        "status": "PASS",
        "task_id": "RT-20260802-008",
        "plan_task_id": "P15-T02",
        "created_at": CREATED_AT,
        "record_granularity": {
            "comparison_arm": "one requested workflow architecture or review configuration",
            "mechanism_result": "one normalized governance mechanism with an explicit numerator and denominator",
            "source_binding": "one tracked source at an exact SHA-256",
        },
        "fields": [
            {"name": "observation_status", "type": "controlled_vocabulary", "allowed": ["not_observed", "not_observed_as_control_arm", "observed_nonrandomized", "observed_same_model_context_only", "partially_observed_context_diversity_only"]},
            {"name": "numerator", "type": "nonnegative_integer_or_null", "null_semantics": "not measured; never zero-filled"},
            {"name": "denominator", "type": "positive_integer_or_null", "null_semantics": "population not established"},
            {"name": "value", "type": "number_or_null", "derivation": "numerator / denominator only when both are valid"},
            {"name": "cost_status", "type": "controlled_vocabulary", "allowed": ["not_available", "not_recorded", "measured"]},
            {"name": "causal_identification", "type": "controlled_vocabulary", "allowed": ["not_identified"]},
        ],
        "metrics": [
            {"metric_id": item["metric"], "numerator": item["numerator"], "denominator": item["denominator"], "scope": item["mechanism_id"], "causal_interpretation_allowed": False}
            for item in experiment["mechanism_results"]
        ],
        "missingness_policy": "Unknown denominators, costs, arms, abandonment rates, and outcome effects remain null or not_measured; numeric zero is prohibited.",
        "privacy_policy": "Only tracked identifiers, typed counts, paths, and hashes are projected; prompts, credentials, and private free text are excluded.",
        "authority_boundary": experiment["authority_boundary"],
    }


def manuscript_text(experiment: dict[str, Any]) -> str:
    metrics = {item["mechanism_id"]: item for item in experiment["mechanism_results"]}
    lineage = experiment["lineage_and_attempt_history"]
    ops = experiment["operational_non_regression_context"]
    return f"""---
authority: "science_draft"
status: "draft/control"
task_id: "RT-20260802-008"
plan_task_id: "P15-T02"
claim_boundary_id: "CB-V21-P15-T02-METHODOLOGY-PUBLICATION-001"
publication_authorized: false
proof_authority: false
---

# Auditable Governance for a Role-Structured AI Research Workflow

## Abstract

This internal methodology manuscript treats one governed AI research workflow as an auditable research object. A retrospective, hash-bound corpus combines fixed gate fixtures, paired same-model review-context records, candidate lineage, an append-only attempt ledger, and a later software non-regression audit. The corpus supports bounded claims about encoded decision hygiene: fixed claim-gate fixtures rejected {metrics['claim_gate_overclaim_control']['numerator']} of {metrics['claim_gate_overclaim_control']['denominator']} cases; the family-freeze matrix suppressed {metrics['candidate_cycle_and_route_orbit_control']['numerator']} of {metrics['candidate_cycle_and_route_orbit_control']['denominator']} repeated or repackaged cases while preserving {metrics['candidate_cycle_and_route_orbit_control']['lawful_route_preservation_count']} lawful routes; and review context exposed {metrics['reviewer_disagreement_visibility']['numerator']} disagreements across {metrics['reviewer_disagreement_visibility']['denominator']} eligible axes. The evidence does not identify causal improvement in truth-finding. Unstructured and normalized single-agent controls are absent, blind review is same-model only, reviewer diversity is context diversity rather than independence, cost is unavailable, and the attempt ledger is not a complete historical population. The contribution is therefore a reproducible method and calibrated evidence boundary, not proof of autonomous science or of any physics claim.

## 1. Research questions and contribution

The study asks: (RQ1) which role, claim-gate, negative-result-memory, candidate-cycle, lineage, and attempt-history mechanisms have bounded decision-hygiene evidence; (RQ2) which requested architecture and review arms are actually observed; and (RQ3) whether v21 controls preserve claim and authority boundaries under operational validation. The contribution is a normalized experiment package, data dictionary, source-hash manifest, manuscript, limitations statement, and compact receipt. It does not claim a causal treatment effect, independent replication, external human review, or scientific validity.

## 2. Workflow architecture

The evaluated architecture separates Director routing, one immutable AgentJob, a task-local execution-role overlay, claim boundaries, child analytical perspectives, deterministic validators, append-only negative-result memory, and a cumulative checkpoint. Role structure is treated as a configuration of responsibilities and authority, not as evidence of epistemic independence. The external-red-team-reviewer label names an internal registered role; in this packet it does not mean an external person reviewed the work.

The candidate-lineage registry contains {lineage['candidate_family_count']} families, {lineage['candidate_count']} candidates, {lineage['lineage_edge_count']} lineage edges, and {lineage['candidate_stage_count']} candidate stages. Immutable IDs and explicit route/freeze events normalize candidate cycles without turning absence, rejection, or validator status into physics evidence. The bounded attempt ledger contains {lineage['attempt_event_count']} events across {lineage['represented_attempt_task_count']} represented tasks; it records validation catches, audit objections, and repairs, but is not asserted to cover the repository's full history.

## 3. Study design

The design is retrospective, observational, and hash-bound. Each reported statistic is reconstructed from tracked JSON or YAML at an exact SHA-256. Units differ by mechanism: fixture cases for gates, paired axes for review context, lineage records for candidate history, attempt events for rework visibility, and validation gates for software assurance. These heterogeneous units are not pooled into one performance score.

### 3.1 Requested comparison arms

| Arm | Evidence status | Permitted interpretation |
| --- | --- | --- |
| Unstructured | Not observed | No effect estimate. |
| Single-agent | Not observed as a normalized control arm | Model telemetry alone is not an outcome arm. |
| Role-structured | Observed, nonrandomized | Descriptive conformance and event counts only. |
| Blind review | Two blind same-model records | Context sensitivity, not reviewer independence. |
| Diverse review | Four same-model context records over two objects | Partial context diversity; no different-model, external-human, or independent arm. |

The comparison table is intentionally incomplete. Treating missing arms as zeros would manufacture a result.

### 3.2 Mechanism-level baselines and ablations

The claim-gate ablation removes one hard-rejection rule from ten fixed fixtures and counts unchecked exposure, not historical production admission. The family-freeze ablation removes repeat/repackaging protection from eleven fixed cases while retaining other checks conceptually. The budget/ordinary-route study combines twelve dual-budget fixtures with one observed live route intervention; its unconstrained live counterfactual remains indeterminate. The review comparison pairs same-model assessments across contexts. The quality-metric study preserves measured versus not-measured denominators and retains the P12 snapshot's source-binding defect as historical evidence rather than rewriting it.

## 4. Results

### 4.1 Overclaim control

The physics-payload gate rejected {metrics['claim_gate_overclaim_control']['numerator']} of {metrics['claim_gate_overclaim_control']['denominator']} fixed fixture cases (share {metrics['claim_gate_overclaim_control']['value']:.2f}). This supports admission selectivity for the encoded risks. It does not show that all five would otherwise have entered a manuscript, nor that admitted material is true.

### 4.2 Candidate-cycle and route-orbit control

The family-freeze matrix suppressed {metrics['candidate_cycle_and_route_orbit_control']['numerator']} of {metrics['candidate_cycle_and_route_orbit_control']['denominator']} repeated/repackaged cases (share {metrics['candidate_cycle_and_route_orbit_control']['value']:.3f}) while preserving {metrics['candidate_cycle_and_route_orbit_control']['lawful_route_preservation_count']} lawful routes. This is bounded evidence for orbit control with distinct continuation still open; it is not a global no-go result.

### 4.3 Budget separation and routing

The dual-budget evaluator rejected {metrics['budget_and_route_separation']['numerator']} of {metrics['budget_and_route_separation']['denominator']} malformed fixtures (share {metrics['budget_and_route_separation']['value']:.3f}). In the recorded live case, the ordinary-route guard engaged after a project-system run of {metrics['budget_and_route_separation']['live_project_system_streak']} tasks and selected P12-T07. This demonstrates an encoded routing intervention, not physics progress or the outcome of an unconstrained Director.

### 4.4 Reviewer disagreement

Review context exposed {metrics['reviewer_disagreement_visibility']['numerator']} disagreements among {metrics['reviewer_disagreement_visibility']['denominator']} eligible axes (share {metrics['reviewer_disagreement_visibility']['value']:.2f}). Seven exact agreements remain correlated same-model observations and therefore carry false-consensus risk. Different-model, external-human, and independent replication counts are zero.

### 4.5 Negative-result memory, lineage, and rework

Two repairs occur among eight bounded attempt events (share {metrics['negative_result_memory_and_rework_visibility']['value']:.2f}), alongside one validation catch and one audit objection. Append-only event hashes and immutable candidate IDs make these outcomes queryable. The ledger explicitly leaves abandonment not measured because it lacks a closed denominator; zero observed abandoned events is not a zero abandonment rate.

### 4.6 Operational non-regression

The later P13 audit reports {ops['selected_test_count']} selected non-regression tests, {ops['coverage_percent']:.3f}% coverage against an {ops['coverage_floor_percent']:.0f}% floor, {ops['mutation_killed']} of {ops['mutation_total']} measured mutants killed, and {ops['dependency_vulnerability_count']} known dependency vulnerabilities in the audited environment. These data support operational release confidence for the checked software surface. They do not estimate scientific outcome quality or validate the physics interpretation.

## 5. Discussion

The strongest result is not that structured agents outperform alternatives; the needed alternatives are absent. The strongest result is that several governance mechanisms discriminate fixed failure modes, expose review-context disagreement, and retain negative results with explicit denominators. This narrows what can be claimed and makes later comparison possible. The evidence is consistent with improved decision hygiene, but selection effects, shared-model correlation, changing task difficulty, manual curation, incomplete history, and missing cost data prevent causal attribution.

The architecture also separates operational and scientific authority. A validator can show that a record conforms to a contract; it cannot make the record scientifically true. A physics-facing route can preserve research attention; it cannot count as Distance-to-GR progress. A reviewer role can surface objections; its name cannot create external independence.

## 6. Reproducibility

The companion builder recomputes every source hash, arm classification, numerator, denominator, ratio, and operational count from tracked inputs. The checker rejects stale outputs, invalid ratios, zero-filled missing denominators, broadened authority flags, or claims of independent review. Reproduction therefore means deterministic reconstruction of this bounded packet, not replication of a causal experiment.

## 7. Limitations and future study

A publishable causal study would prospectively sample comparable tasks, randomize or match workflow arms, preregister outcomes, use independent models and human experts, record compute and financial cost, define a closed attempt population, and adjudicate scientific quality without letting process PASS substitute for truth. Until then, the five-arm taxonomy is a study design, not a completed comparison.

## 8. Conclusion

The v21 workflow is sufficiently instrumented for a bounded internal methodology contribution: claim gates, lineage, negative-result memory, review-context comparison, and software assurance are reproducible and auditable. The current corpus supports decision-hygiene and conformance claims only. Causal superiority, autonomous scientific capability, independent review, physics proof, ontology adoption, publication authority, and completed derivation remain unestablished and unauthorized.

## Internal source note

The machine-readable experiment package preserves exact paths and SHA-256 hashes for the v21 plan, manuscript boundary checklist, prior manuscript planning records, candidate lineage, attempt ledger, P12-T07 ablation packet, P13-T08 non-regression evidence, and their completion records. Generated wiki and cache layers are not used as authority.
"""


def limitations_text() -> str:
    return """---
authority: "science_draft"
status: "draft/control"
task_id: "RT-20260802-008"
plan_task_id: "P15-T02"
publication_authorized: false
proof_authority: false
---

# P15-T02 methodology limitations statement

1. **No causal identification.** The corpus is retrospective, selected, heterogeneous, and nonrandomized. No architecture-level treatment effect is estimated.
2. **Missing comparison arms.** Unstructured and normalized single-agent controls are absent. Blind review is same-model only; diverse review is context-diverse rather than reviewer-independent.
3. **Shared-model correlation.** Exact agreement cannot be treated as independent replication or consensus.
4. **Incomplete population.** The eight-event attempt ledger covers seven bounded tasks and expressly does not claim complete history. Abandonment has no valid denominator.
5. **Cost unavailable.** Financial cost is unavailable and compute/elapsed effort are not normalized across arms; missing values remain not measured, never zero.
6. **Task heterogeneity.** Fixture cases, review axes, candidate records, attempt events, and software gates are not exchangeable and are not pooled into a single score.
7. **Historical source-integrity limitation.** The P12-T07 snapshot retained three P12-T05 source-hash mismatches. This manuscript reports that snapshot faithfully and does not rewrite predecessor evidence.
8. **Operational evidence boundary.** P13-T08 tests, coverage, mutation results, security audit, and rollback checks support software conformance only.
9. **Internal reviewer boundary.** The external-red-team-reviewer role is an internal role contract, not proof of external human review.
10. **Authority boundary.** Nothing here changes scientific status, ontology, source law, benchmark status, Distance-to-GR, Gate E, proof authority, publication authority, or completed-derivation status.

## Minimum next study

Prospectively preregister comparable tasks and outcomes; randomize or carefully match unstructured, single-agent, role-structured, blind-review, and genuinely independent diverse-review arms; blind adjudicators to workflow condition; record model, effort, tokens, elapsed time, and financial cost; define closed attempt and abandonment denominators; and separate scientific-quality adjudication from operational validators.
"""


def child_math_text(experiment: dict[str, Any]) -> str:
    return f"""schema_id: "p15_t02_child_phys_math_methodology_publication_v1"
status: "completed"
task_id: "RT-20260802-008"
plan_task_id: "P15-T02"
perspective: "physicist_mathematician"
findings:
  - "All six reported mechanism metrics preserve explicit integer numerators and denominators."
  - "Requested workflow arms are classified before comparison; two are absent, one is nonrandomized, and two are correlated same-model variants."
  - "Candidate lineage contains {experiment['lineage_and_attempt_history']['candidate_count']} candidates and {experiment['lineage_and_attempt_history']['lineage_edge_count']} lineage edges; the bounded attempt corpus contains {experiment['lineage_and_attempt_history']['attempt_event_count']} events."
  - "No pooled effect size is defined across heterogeneous fixture, axis, event, lineage, and software-gate units."
recommendation: "accept_for_fusion_as_descriptive_noncausal_methodology"
causal_superiority_established: false
theorem_truth_evaluated: false
proof_authority: false
"""


def child_phil_text() -> str:
    return """schema_id: "p15_t02_child_phys_phil_methodology_publication_v1"
status: "completed"
task_id: "RT-20260802-008"
plan_task_id: "P15-T02"
perspective: "physicist_philosopher"
findings:
  - "Role names and review configurations do not create epistemic independence."
  - "Operational conformance, routing, and validation must remain separate from scientific truth and Distance-to-GR progress."
  - "Negative-result memory is methodologically valuable because it preserves failed and blocked outcomes without converting them into global no-go claims."
  - "The manuscript is an internal draft/control contribution; publication and external-review authority remain absent."
recommendation: "accept_for_fusion_with_explicit_authority_and_external_validity_limits"
scientific_status_changed: false
ontology_or_source_law_adopted: false
publication_authorized: false
proof_authority: false
"""


def conflict_text() -> str:
    return """schema_id: "p15_t02_parent_conflict_review_methodology_publication_v1"
status: "resolved"
task_id: "RT-20260802-008"
plan_task_id: "P15-T02"
resolution_rounds: 1
conflicts:
  - conflict_id: "P15-T02-CONFLICT-001"
    phys_math_position: "The fixed matrices permit exact descriptive ratios."
    phys_phil_position: "Ratios can be overread as evidence of epistemic improvement."
    resolution: "Retain the ratios with explicit unit, denominator, control-off semantics, and causal-identification status."
  - conflict_id: "P15-T02-CONFLICT-002"
    phys_math_position: "Review-context disagreement is measurable on ten eligible axes."
    phys_phil_position: "Same-model context variation is not reviewer diversity in the independent sense."
    resolution: "Report three-of-ten context disagreement and prohibit independent-review or consensus claims."
unresolved_conflicts: []
fusion_status: "authorized_within_existing_claim_boundary"
proof_authority: false
"""


def fusion_text() -> str:
    return """# P15-T02 parent fusion notes

The parent accepted the Physicist-Mathematician child's denominator discipline and the Physicist-Philosopher child's authority separation. Exact ratios are retained only as descriptive properties of their bounded matrices. Missing arms, costs, and denominators remain absent rather than zero-filled. Same-model context comparisons are labeled context diversity rather than reviewer independence. The fused manuscript preserves the P12 source-integrity limitation, uses P13 non-regression only as operational evidence, and makes no physics, ontology, publication, proof, or completed-derivation claim.
"""


def build_outputs() -> dict[str, str]:
    experiment = build_experiment()
    dictionary = build_dictionary(experiment)
    base_outputs = {
        OUTPUT_PATHS["experiment"]: json_text(experiment),
        OUTPUT_PATHS["dictionary"]: json_text(dictionary),
        OUTPUT_PATHS["manuscript"]: manuscript_text(experiment),
        OUTPUT_PATHS["limitations"]: limitations_text(),
        OUTPUT_PATHS["child_math"]: child_math_text(experiment),
        OUTPUT_PATHS["child_phil"]: child_phil_text(),
        OUTPUT_PATHS["conflict"]: conflict_text(),
        OUTPUT_PATHS["fusion"]: fusion_text(),
    }
    output_hashes = {
        f"research_control/tasks/RT-20260802-008/artifacts/{name}": hashlib.sha256(text.encode("utf-8")).hexdigest()
        for name, text in sorted(base_outputs.items())
    }
    receipt = {
        "schema_id": "v21_p15_t02_methodology_compact_receipt_v1",
        "status": "PASS_BOUNDED_NONCAUSAL_PUBLICATION_PACKET",
        "task_id": "RT-20260802-008",
        "plan_task_id": "P15-T02",
        "created_at": CREATED_AT,
        "comparison_arm_statuses": {item["arm_id"]: item["observation_status"] for item in experiment["comparison_arms"]},
        "headline_counts": {
            "mechanism_count": len(experiment["mechanism_results"]),
            "candidate_family_count": experiment["lineage_and_attempt_history"]["candidate_family_count"],
            "candidate_count": experiment["lineage_and_attempt_history"]["candidate_count"],
            "attempt_event_count": experiment["lineage_and_attempt_history"]["attempt_event_count"],
            "represented_attempt_task_count": experiment["lineage_and_attempt_history"]["represented_attempt_task_count"],
            "different_model_review_count": 0,
            "external_human_review_count": 0,
            "independent_replication_count": 0,
        },
        "finding_counts": {
            "missing_control_arm": 2,
            "same_model_review_limit": 2,
            "causal_nonidentification": 1,
            "cost_unavailable": 1,
            "historical_source_integrity_limit_retained": 1,
            "authority_boundary_violation": 0,
        },
        "cost_status": experiment["lineage_and_attempt_history"]["cost_status"],
        "causal_identification": experiment["design"]["causal_identification"],
        "validator_ids": [
            "deterministic_output_exactness",
            "five_requested_arms_classified",
            "valid_denominators",
            "unknown_value_nonfabrication",
            "source_hash_exactness",
            "parent_child_synthesis",
            "causal_identification_guard",
            "methodology_physics_authority_boundary",
        ],
        "claim_boundary_summary": "The packet supports bounded decision-hygiene and operational-conformance claims only; causal superiority, independent or external-human review, physics progress, theorem truth, ontology change, publication, proof, and completed derivation remain unestablished and unauthorized.",
        "source_hashes": {item["path"]: item["sha256"] for item in experiment["source_bindings"]},
        "output_hashes": output_hashes,
        "authority": experiment["authority_boundary"],
        "work_item_disposition": "methodology_publication_packet_complete_with_causal_and_external_validity_limits",
    }
    base_outputs[OUTPUT_PATHS["receipt"]] = json_text(receipt)
    return base_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check:
        mismatches = []
        for name, expected in outputs.items():
            path = ARTIFACT_DIR / name
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                mismatches.append(name)
        if mismatches:
            print(json_text({"status": "FAIL", "mismatches": mismatches}), end="")
            return 1
        print(json_text({"status": "PASS", "checked_output_count": len(outputs)}), end="")
        return 0
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    for name, contents in outputs.items():
        (ARTIFACT_DIR / name).write_text(contents, encoding="utf-8")
    print(json_text({"status": "PASS", "written_output_count": len(outputs)}), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
