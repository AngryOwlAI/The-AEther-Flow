#!/usr/bin/env python3
"""Validate the bounded v21 P9-T01 benchmark protocol and target-import firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "source_derived_benchmark_protocol_validation_v1.json"

PROTOCOL_PATH = ARTIFACT_DIR / "source_derived_benchmark_protocol_v1.tex"
CASE_SCHEMA_PATH = ARTIFACT_DIR / "source_derived_benchmark_case_schema_v1.yaml"
FIREWALL_PATH = ARTIFACT_DIR / "target_import_firewall_v1.yaml"
GATE_E_PATH = ARTIFACT_DIR / "gate_e_readiness_checklist_v1.yaml"
MATH_CHILD_PATH = ARTIFACT_DIR / "child_phys_math_p9_t01_benchmark_protocol.yaml"
PHIL_CHILD_PATH = ARTIFACT_DIR / "child_phys_phil_p9_t01_benchmark_protocol.yaml"
REVIEW_PATH = ARTIFACT_DIR / "parent_conflict_review_p9_t01_benchmark_protocol.yaml"
FUSION_PATH = ARTIFACT_DIR / "parent_fusion_notes_p9_t01_benchmark_protocol.md"
RECEIPT_PATH = ARTIFACT_DIR / "source_derived_benchmark_protocol_compact_receipt_v1.json"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/handoffs/handoff-0907.yaml":
        "d4229819dd85f4ae8b290c15dc408b036d2bf2644f2fd691b5ebea26c6f8c835",
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex":
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260726-001/artifacts/p6_geometry_input_contract_v1.yaml":
        "7b0eee4ea249a3acf99d38d312bd14619dedea79977d7b802062e9410f5b8557",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml":
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_spec_v1.yaml":
        "417c604bad008b85b153718ae04aa43307c2ff3cfa3a5c3f242e70b013c86ba4",
    "research_control/tasks/RT-20260728-003/artifacts/common_source_propagation_spec_v1.yaml":
        "91422c4db2b3166da6cab9391ff3f1109d43a683d9624f8086e23d7d8ddf7001",
    "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex":
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
    "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_assumption_envelope_v1.yaml":
        "da939b16a0cb4da082068ab9954d11c4c7a7a658e746c50295dc20347fc82a65",
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_spec_v1.yaml":
        "8840b205e8aa12d73f3e782ec6936eb96385bb5694c298b1bf41a2bdfe472626",
    "research_control/tasks/RT-20260729-007/artifacts/finite_source_field_equation_identity_spec_v1.yaml":
        "d37fdff6d320751d0174459c3d10bec75aa04be62c72c368480f1cafdb46e5f8",
    "research_control/tasks/RT-20260729-008/artifacts/finite_constraint_stability_phase_diagram_v1.yaml":
        "59ac3d8baf948f2def63df6052b066fdce876cc48223652a8b64845334286473",
    "research_control/tasks/RT-20260729-009/artifacts/blind_mathematical_review_status_v1.yaml":
        "31df9d0532a29dc3a716d2c3e5059839f258e5346952efb96d9fe676029e13f0",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_verdict_matrix_v1.yaml":
        "89e484d18aca681a9f79484331a38ee9b98478e5169af4bb9de2762c71e473a4",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_relativistic_recovery.tex":
        "77d5c2db56f122870343834f853bf2f375a912116a347d7c5710405c8707d69c",
    "ontology/tex/aether_flow_consistency.tex":
        "d965519639ee8764a5c5a63798d15e8a9a380d7e208dffc43a0be02b6f245ba1",
}

EXPECTED_CASES = {
    "P9-BENCH-VACUUM-MINKOWSKI-V1": "P9-T02",
    "P9-BENCH-WEAK-FIELD-CLOCK-V1": "P9-T03",
    "P9-BENCH-CAUSAL-FREEFALL-V1": "P9-T04",
    "P9-BENCH-FLRW-COSMOLOGY-V1": "P9-T05",
    "P9-BENCH-RADIATIVE-SECTOR-V1": "P9-T06",
    "P9-BENCH-NONLINEAR-COMPACT-SOURCE-V1": "P9-T07",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "downstream_plan_task_id",
    "benchmark_scope",
    "source_inputs",
    "derived_intermediate_objects",
    "target_observable",
    "imported_assumptions",
    "approximation_order",
    "residual_corrections",
    "analytic_equivalence",
    "numerical_tolerance",
    "success_criteria",
    "failure_criteria",
    "inconclusive_criteria",
    "source_hash_manifest",
    "code_hash_manifest",
    "provenance_dag",
    "source_output_seal",
    "independent_reproduction",
    "model_to_world_map",
    "target_exposure_ledger",
    "execution_status",
}

REQUIRED_FORBIDDEN_CLASSES = {
    "target_atlas",
    "target_metric",
    "target_solution",
    "Einstein_Hilbert_action",
    "Einstein_equations",
    "target_boundary_or_initial_data",
    "observed_target_residual_or_desired_agreement",
    "target_tuned_parameter_calibration_or_regularization",
    "target_selected_branch_basis_or_gauge",
    "benchmark_success_label",
    "target_contaminated_code_lookup_table_training_data_prior_or_cache",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

    required_paths = [
        PROTOCOL_PATH,
        CASE_SCHEMA_PATH,
        FIREWALL_PATH,
        GATE_E_PATH,
        MATH_CHILD_PATH,
        PHIL_CHILD_PATH,
        REVIEW_PATH,
        FUSION_PATH,
        RECEIPT_PATH,
    ]
    for artifact_path in required_paths:
        check(
            f"exists:{artifact_path.name}",
            artifact_path.is_file(),
            str(artifact_path.relative_to(ROOT)),
        )

    try:
        case_schema = load_yaml(CASE_SCHEMA_PATH)
        firewall = load_yaml(FIREWALL_PATH)
        gate_e = load_yaml(GATE_E_PATH)
        math_child = load_yaml(MATH_CHILD_PATH)
        phil_child = load_yaml(PHIL_CHILD_PATH)
        review = load_yaml(REVIEW_PATH)
        receipt = load_json(RECEIPT_PATH)
    except Exception as exc:
        check("structured_artifact_load", False, str(exc))
        case_schema = firewall = gate_e = math_child = phil_child = review = receipt = {}
    else:
        check("structured_artifact_load", True, "Six YAML artifacts and one JSON receipt parsed.")

    declared_fields = set(case_schema.get("required_case_fields", []))
    check(
        "declared_required_case_fields",
        declared_fields == REQUIRED_CASE_FIELDS,
        ",".join(sorted(declared_fields)),
    )

    cases = case_schema.get("case_templates", [])
    case_map = {
        item.get("case_id"): item
        for item in cases
        if isinstance(item, dict)
    }
    check("case_count", len(cases) == 6, str(len(cases)))
    check("case_identity_set", set(case_map) == set(EXPECTED_CASES), ",".join(sorted(str(key) for key in case_map)))
    check(
        "case_plan_mapping",
        all(case_map.get(case_id, {}).get("downstream_plan_task_id") == plan_id for case_id, plan_id in EXPECTED_CASES.items()),
        json.dumps({key: case_map.get(key, {}).get("downstream_plan_task_id") for key in EXPECTED_CASES}, sort_keys=True),
    )
    check(
        "case_field_completeness",
        all(REQUIRED_CASE_FIELDS.issubset(set(item)) for item in case_map.values()),
        json.dumps({key: sorted(REQUIRED_CASE_FIELDS - set(value)) for key, value in case_map.items()}, sort_keys=True),
    )
    check(
        "all_cases_not_run",
        all(item.get("execution_status") == "NOT_RUN" for item in case_map.values()),
        ",".join(str(item.get("execution_status")) for item in case_map.values()),
    )
    check(
        "all_cases_have_source_inputs",
        all(isinstance(item.get("source_inputs"), list) and item.get("source_inputs") for item in case_map.values()),
        str(sum(bool(item.get("source_inputs")) for item in case_map.values())),
    )
    check(
        "all_cases_have_intermediates",
        all(isinstance(item.get("derived_intermediate_objects"), list) and item.get("derived_intermediate_objects") for item in case_map.values()),
        str(sum(bool(item.get("derived_intermediate_objects")) for item in case_map.values())),
    )
    check(
        "no_imported_target_assumptions",
        all(item.get("imported_assumptions") == [] for item in case_map.values()),
        json.dumps({key: value.get("imported_assumptions") for key, value in case_map.items()}, sort_keys=True),
    )
    check(
        "success_failure_inconclusive_present",
        all(
            str(item.get(field, "")).strip()
            for item in case_map.values()
            for field in ("success_criteria", "failure_criteria", "inconclusive_criteria")
        ),
        "All six cases carry three nonblank outcome criteria.",
    )

    current_result = case_schema.get("current_result", {})
    check("lawful_program_defined", current_result.get("lawful_benchmark_program_defined") is True, str(current_result.get("lawful_benchmark_program_defined")))
    check("next_plan_task", current_result.get("next_plan_task_id") == "P9-T02", str(current_result.get("next_plan_task_id")))
    check("next_role", current_result.get("next_role_family") == "candidate-constructor@0.2.0", str(current_result.get("next_role_family")))
    check("no_physical_recovery", current_result.get("physical_benchmark_recovery_established") is False, str(current_result.get("physical_benchmark_recovery_established")))

    forbidden_classes = {
        item.get("class")
        for item in firewall.get("forbidden_upstream_roots", [])
        if isinstance(item, dict)
    }
    check(
        "forbidden_root_classes",
        REQUIRED_FORBIDDEN_CLASSES.issubset(forbidden_classes),
        ",".join(sorted(str(value) for value in forbidden_classes)),
    )
    check("firewall_fail_closed", firewall.get("enforcement") == "fail_closed", str(firewall.get("enforcement")))

    graph = firewall.get("provenance_graph", {})
    check("provenance_dag_required", graph.get("graph_kind") == "finite_directed_acyclic_graph" and graph.get("acyclicity_required") is True, json.dumps(graph, sort_keys=True))
    check("complete_edges_required", graph.get("complete_edge_manifest_required") is True, str(graph.get("complete_edge_manifest_required")))

    state_machine = firewall.get("stage_machine", {}).get("states", {})
    source_state = state_machine.get("SOURCE_EXECUTION", {})
    oracle_state = state_machine.get("TARGET_ORACLE_OPEN", {})
    check("target_oracle_closed_during_source", source_state.get("target_oracle_available") is False, str(source_state.get("target_oracle_available")))
    check("oracle_requires_seal", oracle_state.get("precondition") == "seal verifies byte-for-byte", str(oracle_state.get("precondition")))
    check("post_seal_source_immutable", oracle_state.get("source_mutation_allowed") is False, str(oracle_state.get("source_mutation_allowed")))

    theorem = firewall.get("soundness_theorem", {})
    hypotheses = theorem.get("hypotheses", [])
    check("theorem_identity", theorem.get("theorem_id") == "TargetImportFirewallSoundness_v1", str(theorem.get("theorem_id")))
    check("theorem_hypothesis_count", len(hypotheses) == 6, str(len(hypotheses)))
    check("theorem_proof_method", theorem.get("proof_method") == "topological induction over source-stage nodes followed by seal immutability", str(theorem.get("proof_method")))
    check("theorem_limitations", len(theorem.get("necessary_not_sufficient", [])) >= 5, str(len(theorem.get("necessary_not_sufficient", []))))

    counterexample = firewall.get("counterexample_control", {})
    check("minimal_counterexample_rejected", counterexample.get("expected_firewall_result") == "FAIL_FIREWALL", str(counterexample.get("expected_firewall_result")))
    check("post_hoc_tolerance_rejected", firewall.get("tolerance_firewall", {}).get("post_hoc_tolerance_change") == "FAIL_FIREWALL", str(firewall.get("tolerance_firewall", {}).get("post_hoc_tolerance_change")))
    check("same_context_not_independent", firewall.get("independent_reproduction_firewall", {}).get("same_context_role_separation_counts_as_independent") is False, str(firewall.get("independent_reproduction_firewall", {}).get("same_context_role_separation_counts_as_independent")))
    check("independent_method_required", firewall.get("independent_reproduction_firewall", {}).get("independent_code_or_method_provenance_required") is True, str(firewall.get("independent_reproduction_firewall", {}).get("independent_code_or_method_provenance_required")))
    suite_firewall = firewall.get("suite_and_exposure_firewall", {})
    check("suite_parameter_freeze", suite_firewall.get("suite_global_parameter_freeze_before_holdout_oracle") is True, str(suite_firewall.get("suite_global_parameter_freeze_before_holdout_oracle")))
    check("target_exposure_ledger", suite_firewall.get("target_exposure_ledger_required") is True, str(suite_firewall.get("target_exposure_ledger_required")))
    check("model_to_world_required", suite_firewall.get("model_to_world_map_required_for_physical_claim") is True, str(suite_firewall.get("model_to_world_map_required_for_physical_claim")))

    gate_criteria = gate_e.get("criteria", [])
    gate_statuses = [item.get("status") for item in gate_criteria if isinstance(item, dict)]
    check("gate_e_not_ready", gate_e.get("overall_readiness") == "NOT_READY_NO_BENCHMARK_CASE_EXECUTED", str(gate_e.get("overall_readiness")))
    check("gate_e_criterion_count", len(gate_criteria) == 10, str(len(gate_criteria)))
    check("gate_e_protocol_pass_count", sum(str(status).startswith("PASS") for status in gate_statuses) == 2, str(sum(str(status).startswith("PASS") for status in gate_statuses)))
    check("gate_e_deferred_count", sum(str(status).startswith("DEFERRED") for status in gate_statuses) == 1, str(sum(str(status).startswith("DEFERRED") for status in gate_statuses)))
    check("gate_e_no_verdict", gate_e.get("Gate_E_verdict_issued") is False, str(gate_e.get("Gate_E_verdict_issued")))
    check("gate_d_unchanged", gate_e.get("Gate_D_status_changed") is False, str(gate_e.get("Gate_D_status_changed")))

    check("math_child_complete", math_child.get("status") == "completed", str(math_child.get("status")))
    check("phil_child_complete", phil_child.get("status") == "completed", str(phil_child.get("status")))
    check(
        "parent_conflicts_resolved",
        review.get("status") == "resolved" and review.get("unresolved_conflicts") == [],
        json.dumps(review.get("unresolved_conflicts")),
    )
    fusion_result = review.get("fusion_result", {})
    check("one_outer_agentjob", fusion_result.get("outer_agentjob_count") == 1, str(fusion_result.get("outer_agentjob_count")))
    check("no_child_agentjobs", fusion_result.get("child_agentjob_count") == 0, str(fusion_result.get("child_agentjob_count")))
    check("two_internal_subagents", fusion_result.get("child_subagent_count") == 2, str(fusion_result.get("child_subagent_count")))

    protocol_text = PROTOCOL_PATH.read_text(encoding="utf-8") if PROTOCOL_PATH.is_file() else ""
    fusion_text = FUSION_PATH.read_text(encoding="utf-8") if FUSION_PATH.is_file() else ""
    check("tex_theorem_present", "TargetImportFirewallSoundness\\_v1" in protocol_text, "TargetImportFirewallSoundness_v1")
    check("tex_proof_present", "\\begin{proof}" in protocol_text and "topological ordering" in protocol_text, "Proof uses topological ordering.")
    check("tex_post_seal_boundary", "only then is a read-only target oracle opened" in protocol_text, "Post-seal target oracle boundary.")
    check("tex_protocol_not_recovery", "necessary protocol discipline, not a recovery theorem" in protocol_text, "Protocol and recovery are separated.")
    check("fusion_preserves_gate_d", "Gate D" in fusion_text and "NOT READY" in fusion_text, "Fusion preserves Gate D NOT READY.")

    receipt_counts = receipt.get("finding_counts", {})
    check("receipt_status", receipt.get("status") == "PASS_PROTOCOL_DEFINED_NO_CASE_EXECUTED", str(receipt.get("status")))
    check("receipt_case_count", receipt_counts.get("case_template_count") == 6, str(receipt_counts.get("case_template_count")))
    check("receipt_execution_count", receipt_counts.get("executed_case_count") == 0, str(receipt_counts.get("executed_case_count")))
    check("receipt_pass_count", receipt_counts.get("passed_case_count") == 0, str(receipt_counts.get("passed_case_count")))
    check("receipt_validator_id", "p9_t01_benchmark_protocol_local_validator" in receipt.get("validator_ids", []), json.dumps(receipt.get("validator_ids")))

    authority_surfaces = [case_schema, firewall, gate_e, receipt]
    barred_flags = {
        "canonical_ontology_modified",
        "source_law_adopted_or_rejected",
        "benchmark_case_executed",
        "benchmark_result_established",
        "exact_GR_recovery_proved",
        "Gate_D_reversed",
        "Gate_E_verdict_issued",
        "benchmark_promotion_authorized",
        "physics_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
    }
    for surface in authority_surfaces[:3]:
        limits = surface.get("authority_limits", {})
        present_flags = [flag for flag in barred_flags if flag in limits]
        check(
            f"authority_flags_false:{surface.get('artifact_id', surface.get('schema_id', 'unknown'))}",
            all(limits.get(flag) is False for flag in present_flags),
            ",".join(sorted(present_flags)),
        )

    for relative_path, expected_hash in SOURCE_HASHES.items():
        source_path = ROOT / relative_path
        actual_hash = sha256(source_path) if source_path.is_file() else ""
        check(f"source_hash:{relative_path}", actual_hash == expected_hash, actual_hash)

    failures = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "source_derived_benchmark_protocol_validation_v1",
        "task_id": "RT-20260729-012",
        "plan_task_id": "P9-T01",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "protocol_id": "SourceDerivedBenchmarkProtocol_v1",
        "firewall_id": "TargetImportFirewall_v1",
        "theorem_id": "TargetImportFirewallSoundness_v1",
        "case_template_count": len(cases),
        "executed_case_count": 0,
        "passed_case_count": 0,
        "next_plan_task_id": "P9-T02",
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "checks": checks,
    }

    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.json or not args.check:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
