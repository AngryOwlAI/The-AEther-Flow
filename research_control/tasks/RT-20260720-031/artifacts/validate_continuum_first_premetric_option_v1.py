#!/usr/bin/env python3
"""Focused validator for the v21 P4-T02 continuum-first proposal packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260720-031"
ART = TASK / "artifacts"
REPORT = ART / "continuum_first_premetric_validation_v1.json"

PATHS = {
    "math": ART / "child_phys_math_continuum_first_option.yaml",
    "phil": ART / "child_phys_phil_continuum_first_option.yaml",
    "conflict": ART / "parent_conflict_review_continuum_first_option.yaml",
    "fusion": ART / "parent_fusion_notes_continuum_first_option.md",
    "candidate": ART / "continuum_first_premetric_ontology_option_v1.tex",
    "burdens": ART / "continuum_first_premetric_assumption_burden_table_v1.yaml",
    "vocabulary": ART / "continuum_first_claim_vocabulary_v1.yaml",
    "receipt": ART / "continuum_first_premetric_compact_receipt_v1.json",
    "task": TASK / "00_TASK.yaml",
    "decision": TASK / "DDR-20260720-031.md",
    "job": TASK / "jobs/AJ-RT-20260720-031-001.yaml",
    "role": TASK / "roles/ontology-formalizer@0.2.0--RT-20260720-031.yaml",
    "completion": TASK / "jobs/completions/AJC-AJ-RT-20260720-031-001.yaml",
    "documentation": TASK / "documentation_impact.yaml",
    "handoff_yaml": ROOT / "research_control/handoffs/handoff-0801.yaml",
    "handoff_md": ROOT / "research_control/handoffs/handoff-0801.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    for name, path in PATHS.items():
        check(f"path_{name}", path.is_file(), str(path.relative_to(ROOT)))

    if any(item["status"] == "FAIL" for item in checks):
        report = _report(checks)
        return _finish(report, args)

    math = load_yaml(PATHS["math"])
    phil = load_yaml(PATHS["phil"])
    conflict = load_yaml(PATHS["conflict"])
    burdens = load_yaml(PATHS["burdens"])
    vocab = load_yaml(PATHS["vocabulary"])
    receipt = load_json(PATHS["receipt"])
    job = load_yaml(PATHS["job"])
    completion = load_yaml(PATHS["completion"])
    handoff = load_yaml(PATHS["handoff_yaml"])
    candidate_text = PATHS["candidate"].read_text(encoding="utf-8")
    fusion_text = PATHS["fusion"].read_text(encoding="utf-8")

    check("task_identity", all(data.get("task_id") == "RT-20260720-031" for data in (math, phil, conflict, burdens, vocab, receipt, job, completion, handoff)), "all primary records bind RT-20260720-031")
    check("job_identity", all(data.get("job_id") == "AJ-RT-20260720-031-001" for data in (math, phil, conflict, burdens, vocab, receipt, job, completion, handoff)), "all executable records bind the one outer AgentJob")
    check("plan_identity", receipt.get("plan_task_id") == "P4-T02" and completion.get("implementation_plan_receipt", {}).get("plan_task_id") == "P4-T02", "P4-T02 only")

    decomposition = job.get("role_decomposition", {})
    children = decomposition.get("children", [])
    check("decomposition_mode", decomposition.get("mode") == "parent_child_parallel_synthesis" and decomposition.get("decomposition_version") == "0.1.0", "required parent-child mode")
    check("two_children", [item.get("execution_unit_id") for item in children] == ["child_phys_math", "child_phys_phil"], "exact internal execution units")
    check("child_completion", math.get("execution_unit_id") == "child_phys_math" and phil.get("execution_unit_id") == "child_phys_phil", "both child receipts complete")
    check("conflict_resolution", conflict.get("status") == "resolved" and not conflict.get("blocking_conflict_present") and conflict.get("unresolved_conflicts") == [], "three nonblocking differences resolved")
    check("fusion_boundary", "not independent AgentJobs" in fusion_text and "P4-T03 stays open" in fusion_text, "single outer authority and next-option guard")

    primitive = burdens.get("primitive_assumptions", [])
    nonassumptions = burdens.get("explicit_nonassumptions", [])
    remaining = burdens.get("remaining_burdens", [])
    check("primitive_count", len(primitive) == 6 and burdens.get("counts", {}).get("primitive_assumption_count") == 6, "six explicit primitive packages")
    check("primitive_status", all(item.get("structural_role") == "primitive" and item.get("authority_status") == "proposed" for item in primitive), "primitive never collapses to adopted")
    check("target_import_flags", all(item.get("target_import") is False for item in primitive), "no primitive imports target data")
    check("nonassumption_count", len(nonassumptions) == 9, "nine explicit nonassumptions")
    required_burdens = {"CF-BURDEN-METRIC-001", "CF-BURDEN-CLOCK-001", "CF-BURDEN-MATTER-001", "CF-BURDEN-COUPLING-001", "CF-BURDEN-DYNAMICS-001", "CF-BURDEN-BRIDGE-001", "CF-BURDEN-REGIME-001"}
    check("remaining_burdens", {item.get("burden_id") for item in remaining} == required_burdens, "all seven exact remaining burdens present")
    check("regime_human_gate", next(item for item in remaining if item.get("burden_id") == "CF-BURDEN-REGIME-001").get("status") == "human-gated", "ontology-regime decision protected")

    allowed = vocab.get("allowed_claims", [])
    blocked = vocab.get("blocked_claims", [])
    check("vocabulary_counts", len(allowed) == 14 and len(blocked) == 18, "controlled vocabulary totals")
    check("adoption_vocabulary", vocab.get("adoption_status") == "blocked_adoption_open_continuation", "exact route status vocabulary")
    blocked_terms = {item.get("term") for item in blocked}
    check("blocked_overreads", {"adopted continuum-first ontology", "Phi is physical time", "G_src is physical gauge", "Einstein equations were derived", "P4-T03 is rejected or unnecessary"}.issubset(blocked_terms), "high-risk overreads blocked")

    theorem = math.get("conditional_metric_normalization_theorem", {})
    check("theorem_identity", theorem.get("theorem_id") == "THM-P4T02-CONSTANT-RESCALING-UNDERDETERMINATION", "new theorem identity")
    check("theorem_proof", len(theorem.get("hypotheses", [])) == 3 and len(theorem.get("proof", [])) >= 4 and len(theorem.get("exact_limits", [])) >= 5, "hypotheses proof and limits explicit")
    check("theorem_in_fused_tex", "Order invariance does not fix metric normalization" in candidate_text and "It does not prove that any Lorentzian" in candidate_text, "theorem and exact scope fused")
    check("premetric_tuple", "Continuum-first premetric source option" in candidate_text and "The tuple is deliberately \\emph{premetric}" in candidate_text, "typed premetric tuple fused")
    check("exact_gr_relation", "The bare equality $\\A=M$ is not an allowed bridge proof" in candidate_text, "identity-by-fiat blocked")
    check("p4_t03_open", "P4-T03" in candidate_text and receipt.get("next_plan_route", {}).get("plan_task_id") == "P4-T03", "emergence-first option remains next and unexecuted")

    for key, expected in receipt.get("artifact_hashes", {}).items():
        mapping = {
            "child_phys_math": PATHS["math"],
            "child_phys_phil": PATHS["phil"],
            "parent_conflict_review": PATHS["conflict"],
            "parent_fusion_notes": PATHS["fusion"],
            "continuum_first_candidate": PATHS["candidate"],
            "assumption_burden_table": PATHS["burdens"],
            "claim_vocabulary": PATHS["vocabulary"],
        }
        check(f"hash_{key}", key in mapping and sha256(mapping[key]) == expected, expected)

    source_mapping = {
        "ontology_foundations": ROOT / "ontology/tex/aether_flow_foundations.tex",
        "ontology_dynamics": ROOT / "ontology/tex/aether_flow_dynamics.tex",
        "ontology_geometry": ROOT / "ontology/tex/aether_flow_geometry.tex",
        "frontier_theorem_inventory": ROOT / "research_control/design/frontier_theorem_inventory.md",
        "epistemic_category_glossary": ROOT / "research_control/design/epistemic_category_glossary.md",
        "gr_derivation_burden_map": ROOT / "research_control/design/gr_derivation_burden_map.md",
        "v21_plan": ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
        "p4_t01_ledger": ROOT / "research_control/tasks/RT-20260720-030/artifacts/comprehensive_source_assumption_ledger_v1.tex",
        "p4_t01_matrix": ROOT / "research_control/tasks/RT-20260720-030/artifacts/frontier_object_assumption_matrix_v1.yaml",
        "distance_to_gr_ledger_before": ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv",
        "metric_use_ledger_before": ROOT / "registries/METRIC_USE_LEDGER.csv",
    }
    for key, expected in receipt.get("source_hashes", {}).items():
        check(f"source_hash_{key}", key in source_mapping and sha256(source_mapping[key]) == expected, "authoritative source unchanged")

    packet = completion.get("ontology_law_research_packet", {})
    check("ontology_packet_route", packet.get("route") == "ontology-law-research-packet" and packet.get("trigger_classification") == "derivation_critical_missing_source_law", "named route receipt")
    check("ontology_packet_status", packet.get("adoption_status", {}).get("status_pair") == "blocked_adoption_open_continuation", "adoption blocked continuation open")
    check("human_gate_boundary", packet.get("human_gate_request", {}).get("required_before_adoption") is True, "adoption remains protected")
    progress = completion.get("physics_progress_status", {})
    check("physics_progress", progress.get("status") == "candidate_constructed_pending_audit" and progress.get("physics_promotion_authorized") is False, "candidate only, no promotion")
    delta = completion.get("distance_to_gr_delta", {})
    check("no_distance_delta", delta.get("changed") is False and delta.get("ledger_row_updated") is False, "scientific ledger unchanged")
    forbidden = completion.get("forbidden_conclusion_summary", {})
    check("forbidden_summary", forbidden.get("physics_promotion_authorized") is False and len(forbidden.get("forbidden_conclusions", [])) >= 10, "downstream conclusions blocked")
    check("handoff_route", handoff.get("selected_next_route", {}).get("plan_task_id") == "P4-T03" and handoff.get("selected_next_route", {}).get("executed") is False, "only P4-T03 selected for future execution")

    report = _report(checks)
    return _finish(report, args)


def _report(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "V21-P4-T02-CONTINUUM-FIRST-PREMETRIC-VALIDATION",
        "task_id": "RT-20260720-031",
        "job_id": "AJ-RT-20260720-031-001",
        "status": "PASS" if not failed else "FAIL",
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
    }


def _finish(report: dict[str, Any], args: argparse.Namespace) -> int:
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.json:
        print(rendered, end="")
    else:
        print(f"{report['status']}: {report['passed_check_count']} passed, {report['failed_check_count']} failed")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
