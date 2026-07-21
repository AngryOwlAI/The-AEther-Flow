#!/usr/bin/env python3
"""Focused validator for the v21 P4-T03 emergence-first proposal packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260720-032"
ART = TASK / "artifacts"
REPORT = ART / "emergence_first_validation_v1.json"

PATHS = {
    "math": ART / "child_phys_math_emergence_first_option.yaml",
    "phil": ART / "child_phys_phil_emergence_first_option.yaml",
    "conflict": ART / "parent_conflict_review_emergence_first_option.yaml",
    "fusion": ART / "parent_fusion_notes_emergence_first_option.md",
    "candidate": ART / "emergence_first_process_order_ontology_option_v1.tex",
    "burdens": ART / "emergence_first_manifoldlikeness_burden_map_v1.yaml",
    "examples": ART / "emergence_first_finite_and_continuum_examples_v1.yaml",
    "vocabulary": ART / "emergence_first_claim_vocabulary_v1.yaml",
    "receipt": ART / "emergence_first_compact_receipt_v1.json",
    "task": TASK / "00_TASK.yaml",
    "decision": TASK / "DDR-20260720-032.md",
    "job": TASK / "jobs/AJ-RT-20260720-032-001.yaml",
    "role": TASK / "roles/ontology-formalizer@0.2.0--RT-20260720-032.yaml",
    "completion": TASK / "jobs/completions/AJC-AJ-RT-20260720-032-001.yaml",
    "documentation": TASK / "documentation_impact.yaml",
    "handoff_yaml": ROOT / "research_control/handoffs/handoff-0802.yaml",
    "handoff_md": ROOT / "research_control/handoffs/handoff-0802.md",
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
        return finish(report(checks), args)

    math = load_yaml(PATHS["math"])
    phil = load_yaml(PATHS["phil"])
    conflict = load_yaml(PATHS["conflict"])
    burdens = load_yaml(PATHS["burdens"])
    examples = load_yaml(PATHS["examples"])
    vocab = load_yaml(PATHS["vocabulary"])
    receipt = load_json(PATHS["receipt"])
    job = load_yaml(PATHS["job"])
    completion = load_yaml(PATHS["completion"])
    handoff = load_yaml(PATHS["handoff_yaml"])
    candidate_text = PATHS["candidate"].read_text(encoding="utf-8")
    fusion_text = PATHS["fusion"].read_text(encoding="utf-8")

    primary = (math, phil, conflict, burdens, examples, vocab, receipt, job, completion, handoff)
    check("task_identity", all(item.get("task_id") == "RT-20260720-032" for item in primary), "all primary records bind RT-20260720-032")
    job_records = (math, phil, conflict, burdens, examples, vocab, receipt, job, completion, handoff)
    check("job_identity", all(item.get("job_id") == "AJ-RT-20260720-032-001" for item in job_records), "all executable records bind one outer AgentJob")
    check("plan_identity", receipt.get("plan_task_id") == "P4-T03" and completion.get("implementation_plan_receipt", {}).get("plan_task_id") == "P4-T03", "P4-T03 only")

    decomposition = job.get("role_decomposition", {})
    children = decomposition.get("children", [])
    check("decomposition_mode", decomposition.get("mode") == "parent_child_parallel_synthesis" and decomposition.get("decomposition_version") == "0.1.0", "required parent-child mode")
    check("two_children", [item.get("execution_unit_id") for item in children] == ["child_phys_math", "child_phys_phil"], "exact internal execution units")
    check("child_receipts", math.get("execution_unit_id") == "child_phys_math" and phil.get("execution_unit_id") == "child_phys_phil", "both child analyses present")
    check("conflict_resolution", conflict.get("status") == "resolved" and not conflict.get("blocking_conflict_present") and conflict.get("unresolved_conflicts") == [], "three nonblocking differences resolved")
    check("fusion_boundary", "not independent AgentJobs" in fusion_text and "P4-T04 is now dependency-ready" in fusion_text, "single authority and separate successor")

    signature = burdens.get("minimum_source_signature", {})
    strict = burdens.get("strict_weakness_certificate", {})
    burden_rows = burdens.get("burdens", [])
    check("minimum_signature", signature.get("primitive_package_count") == 2 and signature.get("target_import") is False, "only carrier and locally finite order")
    check("strict_weakness", strict.get("status") == "PASS_AT_DECLARED_SIGNATURE_SCOPE" and len(strict.get("absent", [])) == 6, "target manifold data absent")
    required_burdens = {f"EF-ML-{i:02d}-{suffix}" for i, suffix in enumerate(("SCALE-LIMIT", "TOPOLOGY", "DIMENSION", "DIFFERENTIABILITY", "CAUSAL-SEMANTICS", "MEASURE-SCALE", "METRIC-GEOMETRY", "DYNAMICS-TYPICALITY", "DISCRIMINATOR", "UNIQUENESS-STABILITY", "OPERATIONAL-GR"), start=1)}
    check("burden_map", {item.get("burden_id") for item in burden_rows} == required_burdens and burdens.get("counts", {}).get("burden_count") == 11, "eleven exact reconstruction burdens")
    check("burdens_open", all(item.get("status") == "open" for item in burden_rows), "no burden falsely discharged")

    finite = examples.get("finite_source_examples", [])
    targets = examples.get("target_only_continuum_examples", [])
    witness = examples.get("dimension_nonselection_witness", {})
    check("finite_examples", len(finite) == 2 and all(item.get("local_finiteness") is True for item in finite), "two finite source controls")
    check("target_examples", len(targets) == 2 and {item.get("target_dimension") for item in targets} == {2, 4}, "two evaluator-side continuum targets")
    check("target_separation", all(item.get("target_data_in_source") is False for item in targets), "no target data enters source")
    check("dimension_nonselection", witness.get("witness_id") == "EF-WIT-DIAMOND-DIMENSION-NONSELECTION-001" and len(witness.get("compatible_target_ids", [])) == 2, "finite dimension nonselection witness")
    check("no_emergence_overread", examples.get("continuum_emergence_status") == "not_established" and examples.get("counts", {}).get("full_continuum_emergence_witness_count") == 0, "continuum remains unestablished")

    allowed = vocab.get("allowed_claims", [])
    blocked = vocab.get("blocked_claims", [])
    check("vocabulary_counts", len(allowed) == 15 and len(blocked) == 18, "controlled vocabulary totals")
    check("adoption_vocabulary", vocab.get("adoption_status") == "blocked_adoption_open_continuation", "exact route status vocabulary")
    blocked_terms = {item.get("term") for item in blocked}
    check("blocked_overreads", {"adopted emergence-first ontology", "continuum or spacetime emerged", "prec is physical time", "prec is relativistic causal order", "Einstein equations or GR were derived", "ontology regime selected"}.issubset(blocked_terms), "high-risk overreads blocked")

    check("candidate_signature", "\\mathfrak O_{\\mathrm{EF}}^{\\mathrm{LF}}=(E,\\prec)" in candidate_text, "minimum source tuple fused")
    check("candidate_target_import_guard", "They may not define source" in candidate_text and "target metric" in candidate_text, "target-only evaluator boundary fused")
    check("candidate_literature_scope", all(name in candidate_text for name in ("Bombelli", "Rideout", "Major")), "three primary sources cited with bounded scope")
    check("candidate_p4_route", "P4-T04 is now dependency-ready" in candidate_text and "P4-T05 remains human-gated" in candidate_text, "next route and protected gate preserved")

    artifact_mapping = {
        "child_phys_math": PATHS["math"],
        "child_phys_phil": PATHS["phil"],
        "parent_conflict_review": PATHS["conflict"],
        "parent_fusion_notes": PATHS["fusion"],
        "emergence_first_candidate": PATHS["candidate"],
        "manifoldlikeness_burden_map": PATHS["burdens"],
        "finite_and_continuum_examples": PATHS["examples"],
        "claim_vocabulary": PATHS["vocabulary"],
    }
    for key, expected in receipt.get("artifact_hashes", {}).items():
        check(f"hash_{key}", key in artifact_mapping and sha256(artifact_mapping[key]) == expected, expected)

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
    progress = completion.get("physics_progress_status", {})
    delta = completion.get("distance_to_gr_delta", {})
    forbidden = completion.get("forbidden_conclusion_summary", {})
    check("ontology_packet_route", packet.get("route") == "ontology-law-research-packet" and packet.get("trigger_classification") == "derivation_critical_missing_source_law", "named route receipt")
    check("ontology_packet_status", packet.get("adoption_status", {}).get("status_pair") == "blocked_adoption_open_continuation", "adoption blocked continuation open")
    check("human_gate_boundary", packet.get("human_gate_request", {}).get("required_before_adoption") is True, "adoption remains protected")
    check("physics_progress", progress.get("status") == "candidate_constructed_pending_audit" and progress.get("physics_promotion_authorized") is False, "candidate only, no promotion")
    check("no_distance_delta", delta.get("changed") is False and delta.get("ledger_row_updated") is False, "scientific ledger unchanged")
    check("forbidden_summary", forbidden.get("physics_promotion_authorized") is False and len(forbidden.get("forbidden_conclusions", [])) >= 12, "downstream conclusions blocked")
    check("handoff_route", handoff.get("selected_next_route", {}).get("plan_task_id") == "P4-T04" and handoff.get("selected_next_route", {}).get("executed") is False, "only P4-T04 selected for future execution")

    return finish(report(checks), args)


def report(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "V21-P4-T03-EMERGENCE-FIRST-VALIDATION",
        "task_id": "RT-20260720-032",
        "job_id": "AJ-RT-20260720-032-001",
        "status": "PASS" if not failed else "FAIL",
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
    }


def finish(result: dict[str, Any], args: argparse.Namespace) -> int:
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.json:
        print(rendered, end="")
    else:
        print(f"{result['status']}: {result['passed_check_count']} passed, {result['failed_check_count']} failed")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
