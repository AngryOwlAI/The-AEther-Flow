#!/usr/bin/env python3
"""Focused validator for RT-20260809-022.

Checks the fixed audit subject, exhaustive field and obligation coverage,
theorem-scope counterexample, parent-child fusion, exact next-route limits, and
fail-closed authority flags.  PASS is transaction evidence only.
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
REPORT_PATH = ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_audit_validation.json"
COMPACT_PATH = ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_audit_compact_receipt.json"


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
            {"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail}
        )

    @property
    def failures(self) -> list[dict[str, str]]:
        return [item for item in self.checks if item["status"] != "PASS"]


def run() -> dict[str, Any]:
    review = Review()
    paths = {
        "tex": ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_smuggling_audit_v1.tex",
        "fields": ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_field_audit_matrix_v1.yaml",
        "theorems": ARTIFACT_DIR / "v22_p4_t02_b2_theorem_hypothesis_audit_v1.yaml",
        "obligations": ARTIFACT_DIR / "v22_p4_t02_b2_atomic_obligation_smuggling_audit_v1.yaml",
        "invariance": ARTIFACT_DIR / "v22_p4_t02_b2_authority_invariance_witnesses_v1.yaml",
        "disposition": ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_audit_disposition_v1.yaml",
        "child_math": ARTIFACT_DIR / "child_phys_math_p4_t02_b2_descriptor_audit.yaml",
        "child_phil": ARTIFACT_DIR / "child_phys_phil_p4_t02_b2_descriptor_audit.yaml",
        "conflict": ARTIFACT_DIR / "parent_conflict_review_p4_t02_b2_descriptor_audit.yaml",
        "fusion": ARTIFACT_DIR / "parent_fusion_notes_p4_t02_b2_descriptor_audit.md",
        "model": ARTIFACT_DIR / "v22_p4_t02_b2_descriptor_audit_model.py",
    }
    for name, path in paths.items():
        review.check(f"FILE-{name.upper()}", path.is_file(), f"required artifact {rel(path)} exists")

    fields = load_yaml(paths["fields"])
    theorems = load_yaml(paths["theorems"])
    obligations = load_yaml(paths["obligations"])
    invariance = load_yaml(paths["invariance"])
    disposition = load_yaml(paths["disposition"])
    child_math = load_yaml(paths["child_math"])
    child_phil = load_yaml(paths["child_phil"])
    conflict = load_yaml(paths["conflict"])
    tex = paths["tex"].read_text(encoding="utf-8")
    fusion = paths["fusion"].read_text(encoding="utf-8")

    fixed_hashes = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
        "research_control/handoffs/handoff-0991.yaml": "d4ca051a725237f9f5c0c2884f0c8df70751a913ae045f5edb79ff2177c70033",
        "research_control/tasks/RT-20260809-021/artifacts/v22_p4_t02_b2_continuum_lift_descriptor_formalization_v1.tex": "6b3e454048f1645f164e06dbebac08d1bd29b8a61918d98dcbf77d09c82156c0",
        "research_control/tasks/RT-20260809-021/artifacts/v22_p4_t02_b2_continuum_lift_descriptor_specification_v1.yaml": "82a48f1e82f45012908d9eb8df389ed256bafba937ef6c8de0776b630ab71a65",
        "research_control/tasks/RT-20260809-021/artifacts/v22_p4_t02_b2_proof_obligation_matrix_v1.yaml": "53e78abd61db464bd13b666a5cb2351b41877e31b0efac84a00a97333c9378d1",
        "research_control/tasks/RT-20260809-021/artifacts/v22_p4_t02_b2_finite_input_underdetermination_counterpair_v1.yaml": "e3a8d24c5eda70aa5c8a7c389828ddaee58887e90ab9260f381748423460f9a6",
    }
    for path_text, expected in fixed_hashes.items():
        source = REPO_ROOT / path_text
        review.check(f"HASH-{source.name.upper()}", source.is_file() and sha256(source) == expected, f"fixed source hash {path_text}")

    component_rows = fields.get("components", [])
    expected_component_ids = {
        "D0_SECTOR_SET", "D1_CONTINUUM_FIELDS", "D2_FINITE_TO_CONTINUUM_LIFT",
        "D3_SOURCE_QUOTIENT", "D3_OUTPUT_QUOTIENT", "D4_SECTOR_EQUATIONS",
        "D5_COMPATIBILITY_RELATION", "D5_COMMON_PRINCIPAL_TARGET",
        "D6_OPERATIONAL_NO_TARGET_RECEIPT", "D7_ADEQUACY_PROCEDURE",
    }
    component_ids = {row.get("component_id") for row in component_rows}
    review.check("FIELDS-COUNT", len(component_rows) == 10, "ten component audit rows")
    review.check("FIELDS-IDENTITIES", component_ids == expected_component_ids, "exact ten component identities")
    review.check("FIELDS-NO-TARGET", all(row.get("direct_target_import") is False for row in component_rows), "zero direct target imports")
    review.check("FIELDS-NO-AUTHORITY", all(row.get("direct_authority_import") is False for row in component_rows), "zero direct authority imports")
    review.check("FIELDS-NO-INSTANCE", fields.get("summary", {}).get("instance_validated_count") == 0, "no populated instance is validated")
    review.check("FIELDS-CLASSIFICATION", fields.get("source_extension_classification", {}).get("classification") == "conservative_definitional_extension_schema_with_uninstantiated_primitive_slots", "exact source-extension classification")

    source_matrix = load_yaml(REPO_ROOT / "research_control/tasks/RT-20260809-021/artifacts/v22_p4_t02_b2_proof_obligation_matrix_v1.yaml")
    expected_obligation_ids = {
        item.get("obligation_id")
        for family in source_matrix.get("families", [])
        for item in family.get("obligations", [])
    }
    audit_rows = [item for family in obligations.get("families", []) for item in family.get("records", [])]
    audit_ids = {item.get("obligation_id") for item in audit_rows}
    review.check("OBLIGATION-COUNT", len(audit_rows) == obligations.get("atomic_obligation_count") == 35, "35 audit rows")
    review.check("OBLIGATION-IDENTITIES", audit_ids == expected_obligation_ids and len(audit_ids) == 35, "every source obligation audited exactly once")
    review.check("OBLIGATION-NO-TARGET", all(row.get("direct_target_import") is False for row in audit_rows), "no explicit target imports in obligations")
    review.check("OBLIGATION-NO-AUTHORITY", all(row.get("direct_authority_import") is False for row in audit_rows), "no explicit authority imports in obligations")
    class_counts = {name: sum(row.get("audit_class") == name for row in audit_rows) for name in ("clean_guard", "clean_open", "clean_high_risk", "scope_repair")}
    summary_counts = obligations.get("summary", {})
    review.check("OBLIGATION-CLASS-COUNTS", class_counts == {"clean_guard": 9, "clean_open": 17, "clean_high_risk": 7, "scope_repair": 2}, "audit classifications sum to 35")
    review.check("OBLIGATION-SUMMARY-COUNTS", all(summary_counts.get(f"{name}_count") == value for name, value in class_counts.items()), "summary classification counts agree")
    review.check("OBLIGATION-NONE-DISCHARGED", obligations.get("authority_limits", {}).get("obligation_discharged_count") == 0, "audit discharges no instance obligation")

    core = theorems.get("projective_gluing_core", {})
    hypotheses = core.get("hypotheses", [])
    counter = theorems.get("uniqueness_addendum", {}).get("counterexample", {})
    finite = theorems.get("finite_trace_counterpair_audit", {})
    review.check("THEOREM-CORE", core.get("core_result") == "PASS_CONDITIONAL", "conditional gluing core retained")
    review.check("THEOREM-HYPOTHESES", len(hypotheses) == 6 and all(row.get("target_import") is False and row.get("authority_import") is False for row in hypotheses), "six clean core hypotheses")
    review.check("THEOREM-UNIQUENESS-FAIL", theorems.get("uniqueness_addendum", {}).get("audit_result") == "FAIL_SCOPE_OVERCLAIM", "uniqueness scope defect recorded")
    review.check("THEOREM-COUNTEREXAMPLE-P", counter.get("first_generator") == "P(k)=k0", "first generator fixed")
    review.check("THEOREM-COUNTEREXAMPLE-Q", counter.get("second_generator") == "Q(k)=k0*(k0^2+k1^2)", "second generator fixed")
    review.check("THEOREM-NONUNIT", counter.get("quotient_is_nowhere_zero_unit") is False, "quotient is not a unit")
    review.check("THEOREM-CORE-UNAFFECTED", theorems.get("uniqueness_addendum", {}).get("effect_on_core_theorem", "").startswith("none"), "scope defect does not refute explicit-hypothesis core")
    review.check("COUNTERPAIR-SCOPED-PASS", finite.get("audit_result") == "PASS_WITH_DECLARED_SCOPE", "finite-trace counterpair retained in scope")
    review.check("COUNTERPAIR-PREMISES", len(finite.get("premises", [])) == 4, "four counterpair premises audited")

    witness_rows = invariance.get("witnesses", [])
    review.check("INVARIANCE-COUNT", len(witness_rows) == invariance.get("witness_count") == 6, "six authority-invariance witnesses")
    review.check("INVARIANCE-PASS", all(str(row.get("audit_result", "")).startswith("PASS") for row in witness_rows), "all specification-level witnesses pass")
    review.check("INVARIANCE-INSTANCE-OPEN", invariance.get("summary", {}).get("instance_authority_invariance_established") is False, "populated-instance invariance remains open")

    review.check("DISPOSITION-VERDICT", disposition.get("audit_verdict") == "conditional_specification_level_no_smuggling_pass_with_one_theorem_scope_obstruction_and_instance_audit_required", "exact audit verdict")
    review.check("DISPOSITION-NEXT-ROLE", disposition.get("next_route", {}).get("role_family") == "candidate-constructor@0.2.0", "next role is a fresh Candidate Constructor")
    review.check("DISPOSITION-NEXT-LOCKED", disposition.get("next_route", {}).get("execution_authorized_in_this_task") is False, "next route not executed here")
    review.check("DISPOSITION-UNIQUENESS", disposition.get("candidate_disposition", {}).get("uniqueness_addendum_status") == "quarantined_not_available_as_instance_evidence", "uniqueness addendum quarantined")
    review.check("DISPOSITION-VECTOR", disposition.get("activation_readiness", {}).get("vector") == [1, 1, 1, 1, 0, 0], "readiness vector unchanged")
    review.check("DISPOSITION-ACTIVATION", disposition.get("activation_readiness", {}).get("activation_value") == 0, "B2 activation remains false")

    review.check("CHILD-MATH", child_math.get("status") == "completed", "mathematical child complete")
    review.check("CHILD-PHIL", child_phil.get("status") == "completed", "philosophical child complete")
    review.check("CONFLICT-STATUS", conflict.get("status") == "completed_no_unresolved_blocking_conflict", "parent conflict review complete")
    review.check("CONFLICT-EMPTY", conflict.get("unresolved_conflicts") == [], "no unresolved parent conflict")
    review.check("CONFLICT-BUDGET", conflict.get("resolution_rounds", 99) <= conflict.get("max_resolution_rounds", 0), "conflict resolved within budget")

    required_tex_markers = [
        "Source-fiber factorization criterion",
        "P(k)=k_0",
        "Q(k)=k_0\\bigl(k_0^2+k_1^2\\bigr)",
        "real projective zero sets are equal",
        "35 atomic obligations",
        "$(1,1,1,1,0,0)$",
        "P4-T03 remains locked",
    ]
    for index, marker in enumerate(required_tex_markers, 1):
        review.check(f"TEX-MARKER-{index:02d}", marker in tex, f"TeX marker present: {marker}")
    review.check("FUSION-VERDICT", disposition.get("audit_verdict", "") in fusion, "fusion contains exact verdict")
    review.check("FUSION-NEXT", "Candidate Constructor" in fusion, "fusion records distinct next role")

    model_process = subprocess.run([sys.executable, str(paths["model"]), "--json"], cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    try:
        model_output: dict[str, Any] = json.loads(model_process.stdout)
    except json.JSONDecodeError:
        model_output = {"status": "FAIL", "stdout": model_process.stdout, "stderr": model_process.stderr}
    review.check("MODEL-EXIT", model_process.returncode == 0, "support model exits successfully")
    review.check("MODEL-STATUS", model_output.get("status") == "PASS", "support model reports PASS")
    review.check("MODEL-ZERO-SET", model_output.get("polynomial_counterexample", {}).get("real_zero_set_mismatch_count") == 0, "bounded zero-set witness agrees")
    review.check("MODEL-NONUNIT", model_output.get("polynomial_counterexample", {}).get("quotient_factor_is_nowhere_zero") is False, "bounded nonunit witness exists")

    for field in (
        "canonical_ontology_edit_authorized", "source_law_adoption_authorized",
        "descriptor_instance_constructed", "adequacy_reevaluated", "b2_activated",
        "p4_t03_unlocked", "physical_causal_geometry_established",
        "effective_metric_constructed", "distance_to_gr_ledger_changed",
        "proof_authority", "physics_promotion_authorized", "publication_authorized",
        "push_authorized", "external_action_authorized",
    ):
        review.check(f"AUTH-{field.upper()}", disposition.get("authority", {}).get(field) is False, f"authority limit {field} remains false")

    result = {
        "schema_id": "v22_p4_t02_b2_descriptor_audit_validation_v1",
        "task_id": "RT-20260809-022",
        "job_id": "AJ-RT-20260809-022-001",
        "status": "PASS" if not review.failures else "FAIL",
        "counts": {"check_count": len(review.checks), "failure_count": len(review.failures), "warning_count": 0},
        "checks": review.checks,
        "classification_counts": class_counts,
        "model_summary": {"status": model_output.get("status"), "check_count": model_output.get("check_count"), "failure_count": model_output.get("failure_count")},
        "artifact_sha256": {rel(path): sha256(path) for path in paths.values() if path.is_file()},
        "authority_note": "PASS is transaction evidence only. It does not construct or adopt a descriptor instance, activate B2, reevaluate adequacy, unlock P4-T03, create physical geometry, or authorize promotion.",
    }
    return result


def write_outputs(result: dict[str, Any]) -> None:
    REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_descriptor_audit_compact_receipt_v1",
        "task_id": result["task_id"],
        "job_id": result["job_id"],
        "status": result["status"],
        "counts": result["counts"],
        "classification_counts": result["classification_counts"],
        "report_path": rel(REPORT_PATH),
        "report_sha256": sha256(REPORT_PATH),
        "tree_scope": "RT-20260809-022 task-local audit artifacts plus immutable RT-20260809-021 subject hashes",
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
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
