#!/usr/bin/env python3
"""Focused validator for RT-20260809-021.

The validator checks specification shape, fixed source hashes, theorem markers,
the finite counterpair support model, parent-child synthesis, and fail-closed
authority flags. PASS is operational evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_validation.json"
COMPACT_PATH = ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_compact_receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a YAML mapping")
    return payload


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


class Review:
    def __init__(self) -> None:
        self.checks: list[dict[str, str]] = []

    def check(self, check_id: str, condition: bool, detail: str) -> None:
        self.checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    @property
    def failures(self) -> list[dict[str, str]]:
        return [item for item in self.checks if item["status"] != "PASS"]


def run() -> dict[str, Any]:
    review = Review()
    paths = {
        "tex": ARTIFACT_DIR / "v22_p4_t02_b2_continuum_lift_descriptor_formalization_v1.tex",
        "spec": ARTIFACT_DIR / "v22_p4_t02_b2_continuum_lift_descriptor_specification_v1.yaml",
        "matrix": ARTIFACT_DIR / "v22_p4_t02_b2_proof_obligation_matrix_v1.yaml",
        "counterpair": ARTIFACT_DIR / "v22_p4_t02_b2_finite_input_underdetermination_counterpair_v1.yaml",
        "adequacy": ARTIFACT_DIR / "v22_p4_t02_b2_p2_t01_adequacy_interface_v1.yaml",
        "provenance": ARTIFACT_DIR / "v22_p4_t02_b2_source_provenance_manifest_v1.yaml",
        "child_math": ARTIFACT_DIR / "child_phys_math_p4_t02_b2_descriptor.yaml",
        "child_phil": ARTIFACT_DIR / "child_phys_phil_p4_t02_b2_descriptor.yaml",
        "conflict": ARTIFACT_DIR / "parent_conflict_review_p4_t02_b2_descriptor.yaml",
        "fusion": ARTIFACT_DIR / "parent_fusion_notes_p4_t02_b2_descriptor.md",
        "model": ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_model.py",
    }
    for name, path in paths.items():
        review.check(f"FILE-{name.upper()}", path.is_file(), f"required artifact {rel(path)} exists")

    spec = load_yaml(paths["spec"])
    matrix = load_yaml(paths["matrix"])
    counterpair = load_yaml(paths["counterpair"])
    adequacy = load_yaml(paths["adequacy"])
    provenance = load_yaml(paths["provenance"])
    child_math = load_yaml(paths["child_math"])
    child_phil = load_yaml(paths["child_phil"])
    conflict = load_yaml(paths["conflict"])
    tex = paths["tex"].read_text(encoding="utf-8")
    fusion = paths["fusion"].read_text(encoding="utf-8")

    review.check("SPEC-SCHEMA", spec.get("schema_id") == "v22_p4_t02_b2_continuum_lift_descriptor_specification_v1", "descriptor schema identity")
    review.check("SPEC-CANDIDATE", spec.get("candidate_id") == "CAND-V22-B2-P7-COMMON-PRINCIPAL-LIFT-V1", "exact B2 candidate identity")
    review.check("SPEC-FAMILY", spec.get("candidate_family_id") == "FAM-V22-B2-MATTER-PRINCIPAL-POLYNOMIAL", "exact B2 family identity")
    review.check("SPEC-ROUTE", spec.get("route_label") == "ontology-law-research-packet", "ontology-law route label")
    review.check("SPEC-TRIGGER", spec.get("trigger_classification") == "derivation_critical_missing_source_law", "derivation-critical trigger")
    review.check("SPEC-ADOPTION", spec.get("adoption_status") == "blocked_adoption_open_continuation", "blocked adoption and open continuation")
    review.check("SPEC-SPEC-COMPLETE", spec.get("descriptor_specification_complete") is True, "descriptor specification is complete")
    review.check("SPEC-INSTANCE-OPEN", spec.get("descriptor_instance_complete") is False, "descriptor instance remains unconstructed")
    review.check("SPEC-B2-INACTIVE", spec.get("b2_activated") is False, "B2 remains inactive")
    review.check("SPEC-P4T03-LOCKED", spec.get("p4_t03_unlocked") is False, "P4-T03 remains locked")

    formal = spec.get("formal_descriptor", {})
    components = formal.get("ordered_components", [])
    review.check("SPEC-COMPONENT-COUNT", formal.get("component_count") == 10 and len(components) == 10, "ten descriptor components are typed")
    component_ids = [item.get("component_id") for item in components if isinstance(item, dict)]
    review.check("SPEC-COMPONENT-UNIQUE", len(component_ids) == len(set(component_ids)) == 10, "descriptor component identities are unique")
    review.check("SPEC-COMMON-NO-QUADRATIC", spec.get("common_principal_contract", {}).get("quadratic_form_assumed") is False, "no quadratic form is assumed")
    review.check("SPEC-COMMON-NO-LORENTZ", spec.get("common_principal_contract", {}).get("lorentzian_signature_assumed") is False, "no Lorentzian signature is assumed")
    review.check("SPEC-COMMON-NO-SCALE", spec.get("common_principal_contract", {}).get("physical_scale_assumed") is False, "no physical scale is assumed")

    payloads = spec.get("new_mathematical_payload", [])
    payload_ids = {item.get("payload_id") for item in payloads if isinstance(item, dict)}
    review.check("PAYLOAD-GLUING", "THM-V22-P4T02-B2-PROJECTIVE-COMMON-PRINCIPAL-GLUING" in payload_ids, "gluing theorem payload recorded")
    review.check("PAYLOAD-UNDERDETERMINATION", "THM-V22-P4T02-B2-FINITE-TRACE-PRINCIPAL-UNDERDETERMINATION" in payload_ids, "finite-trace theorem payload recorded")
    review.check("PAYLOAD-DESCRIPTOR", "DEF-V22-P4T02-B2-TEN-COMPONENT-DESCRIPTOR-LAW" in payload_ids, "descriptor-law definition recorded")

    families = matrix.get("families", [])
    obligations = [obligation for family in families for obligation in family.get("obligations", [])]
    review.check("MATRIX-FAMILY-COUNT", matrix.get("obligation_family_count") == 7 and len(families) == 7, "seven proof-obligation families")
    review.check("MATRIX-ATOMIC-COUNT", matrix.get("atomic_obligation_count") == 35 and len(obligations) == 35, "35 atomic proof obligations")
    obligation_ids = [item.get("obligation_id") for item in obligations]
    review.check("MATRIX-ATOMIC-UNIQUE", len(obligation_ids) == len(set(obligation_ids)) == 35, "atomic obligation identities are unique")
    review.check("MATRIX-INSTANCE-OPEN", matrix.get("instance_evidence_status") == "not_supplied", "no instance evidence is claimed")

    comparison = counterpair.get("exact_comparison", {})
    review.check("COUNTERPAIR-TRACE-EQUALITY", comparison.get("finite_traces_equal") is True, "finite traces are held equal")
    review.check("COUNTERPAIR-COMMON", comparison.get("sector_principal_classes_equal_in_completion_a") is True, "completion A has a common projective class")
    review.check("COUNTERPAIR-SPLIT", comparison.get("sector_principal_classes_equal_in_completion_b_where_f_nonzero") is False, "completion B has split projective classes")
    review.check("COUNTERPAIR-SCOPED", counterpair.get("global_no_go_claimed") is False, "counterpair is not a global no-go")
    review.check("COUNTERPAIR-NO-TARGET", counterpair.get("interpretation_boundary", {}).get("target_atlas_or_metric_imported") is False, "counterpair uses no target atlas or metric")

    required_fields = adequacy.get("required_fields", [])
    expected_field_ids = {
        "source_state_and_domain",
        "regularity",
        "source_equivalence",
        "output_equivalence",
        "reconstruction",
        "factor_statistic",
        "operational_typing",
        "independence",
        "stochastic_scope",
        "escape_and_global_scope",
    }
    actual_field_ids = {item.get("field_id") for item in required_fields if isinstance(item, dict)}
    review.check("ADEQUACY-FIELD-COUNT", len(required_fields) == 10, "ten P2-T01 fields are mapped")
    review.check("ADEQUACY-FIELD-SET", actual_field_ids == expected_field_ids, "exact P2-T01 field identities are preserved")
    review.check("ADEQUACY-NOT-RUN", adequacy.get("evaluation_executed") is False, "adequacy reevaluation has not run")
    review.check("ADEQUACY-INSTANCE-MISSING", adequacy.get("descriptor_instance_available") is False, "adequacy remains blocked by the missing instance")

    expected_hashes = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
        "research_control/tasks/RT-20260809-020/artifacts/v22_p4_t02_b2_fallback_descriptor_selection_v1.tex": "544b7a533c47835d3e6173dff35547bf3ce04278085d3b02b1445642001bca02",
        "research_control/tasks/RT-20260809-020/artifacts/parent_fusion_notes_p4_t02_b2_selector.md": "4a960c423dbe86f4a7adc73704e62fbe96fab86112305953297705c168496909",
        "research_control/tasks/RT-20260809-003/artifacts/v22_p1_t03_p7_conditional_input_contract_v1.yaml": "e1acd64ea434f3dc6a0607c17f69162f0e242bc92d5490eb84ff3d3afd92a3c4",
        "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_fallback_matter_principal_candidate_v1.yaml": "11917a5c868b6ed50633e1b7528b59079db40f10c003c32176d1887df5dae6e5",
        "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_source_adequacy_checklist_v1.yaml": "a9b59df7b5b2d1203fef53cf23817400c6d1511836e97ff1ae21b819dc064e68",
        "research_control/tasks/RT-20260809-020/artifacts/v22_p4_t02_b2_descriptor_dependency_map_v1.yaml": "100160e31e8ffe31a18a9b2160c7dfbda4a946a42c625df570294764d54bd256",
        "research_control/handoffs/handoff-0990.yaml": "59c98cc57da0d44cd8f15231ca11bbac417e048f6b557df680454dd09c539ab4",
    }
    for path_text, expected in expected_hashes.items():
        path = REPO_ROOT / path_text
        review.check(f"HASH-{path.name.upper()}", path.is_file() and sha256(path) == expected, f"fixed source hash {path_text}")

    source_rows = provenance.get("sources", [])
    review.check("PROVENANCE-COUNT", provenance.get("source_count") == len(source_rows) == 8, "eight fixed source records are preserved")
    review.check("PROVENANCE-NONAUTHORITY", provenance.get("retrieval_evidence", {}).get("retrieval_layers_are_authority") is False, "retrieval layers are not authority")

    review.check("CHILD-MATH-COMPLETE", child_math.get("status") == "completed", "Physicist-Mathematician child completed")
    review.check("CHILD-PHIL-COMPLETE", child_phil.get("status") == "completed", "Physicist-Philosopher child completed")
    review.check("CONFLICT-STATUS", conflict.get("status") == "completed_no_unresolved_blocking_conflict", "parent conflict review completed")
    review.check("CONFLICT-EMPTY", conflict.get("unresolved_conflicts") == [], "no unresolved parent-child conflict")
    review.check("CONFLICT-ROUNDS", conflict.get("resolution_rounds", 99) <= conflict.get("max_resolution_rounds", 0), "conflicts resolved within the declared budget")

    required_tex_markers = [
        "THM-V22-P4T02-B2-PROJECTIVE-COMMON-PRINCIPAL-GLUING",
        "THM-V22-P4T02-B2-FINITE-TRACE-PRINCIPAL-UNDERDETERMINATION",
        "blocked_adoption_open_continuation",
        "$(1,1,1,1,0,0)$",
        "P4-T03 remains locked",
    ]
    for index, marker in enumerate(required_tex_markers, start=1):
        review.check(f"TEX-MARKER-{index:02d}", marker in tex, f"TeX marker present: {marker}")
    review.check("FUSION-STATUS", "descriptor schema is not a descriptor instance" in fusion, "fusion record preserves schema/instance distinction")
    review.check("FUSION-NEXT-ROLE", "Smuggling Auditor" in fusion, "fusion record selects a concrete next role")

    model_process = subprocess.run(
        [sys.executable, str(paths["model"]), "--json"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    model_output: dict[str, Any]
    try:
        model_output = json.loads(model_process.stdout)
    except json.JSONDecodeError:
        model_output = {"status": "FAIL", "stderr": model_process.stderr, "stdout": model_process.stdout}
    review.check("MODEL-EXIT", model_process.returncode == 0, "support model exits successfully")
    review.check("MODEL-STATUS", model_output.get("status") == "PASS", "support model reports PASS")
    review.check("MODEL-AUTHORITY", model_output.get("authority_limits", {}).get("descriptor_instance_constructed") is False, "support model creates no descriptor instance")

    activation = spec.get("activation_readiness", {})
    review.check("ACTIVATION-VECTOR", activation.get("vector") == [1, 1, 1, 1, 0, 0], "activation vector remains 1-1-1-1-0-0")
    review.check("ACTIVATION-FALSE", activation.get("activation_value") == 0, "activation remains false")
    review.check("NEXT-ROLE", spec.get("next_route", {}).get("role_family") == "smuggling-auditor@0.2.0", "next role is the separate smuggling audit")

    authority = spec.get("authority_limits", {})
    false_authority_fields = [
        "scientific_status_changed",
        "physical_status_changed",
        "source_law_adopted",
        "canonical_ontology_modified",
        "descriptor_instance_constructed",
        "b2_activated",
        "adequacy_reevaluated",
        "p4_t03_unlocked",
        "physical_cone_constructed",
        "effective_metric_constructed",
        "distance_to_gr_changed",
        "gate_b_verdict_issued",
        "proof_authority",
        "physics_promotion_authorized",
        "global_no_go_claimed",
    ]
    for field in false_authority_fields:
        review.check(f"AUTH-{field.upper()}", authority.get(field) is False, f"authority limit {field} remains false")

    artifact_hashes = {rel(path): sha256(path) for path in paths.values() if path.is_file()}
    result = {
        "schema_id": "v22_p4_t02_b2_descriptor_validation_v1",
        "task_id": "RT-20260809-021",
        "job_id": "AJ-RT-20260809-021-001",
        "status": "PASS" if not review.failures else "FAIL",
        "counts": {
            "check_count": len(review.checks),
            "failure_count": len(review.failures),
            "warning_count": 0,
        },
        "checks": review.checks,
        "model_summary": {
            "status": model_output.get("status"),
            "check_count": model_output.get("check_count"),
            "failure_count": model_output.get("failure_count"),
        },
        "artifact_sha256": artifact_hashes,
        "authority_note": "PASS is operational evidence only. It does not construct or adopt a descriptor instance, activate B2, unlock P4-T03, prove physical geometry, or authorize promotion.",
    }
    return result


def write_outputs(result: dict[str, Any]) -> None:
    REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_descriptor_compact_receipt_v1",
        "task_id": result["task_id"],
        "job_id": result["job_id"],
        "status": result["status"],
        "counts": result["counts"],
        "report_path": rel(REPORT_PATH),
        "report_sha256": sha256(REPORT_PATH),
        "tree_scope": "RT-20260809-021 task-local descriptor artifacts plus exact fixed source hashes",
        "authority_note": result["authority_note"],
    }
    COMPACT_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.write_report:
        write_outputs(result)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
