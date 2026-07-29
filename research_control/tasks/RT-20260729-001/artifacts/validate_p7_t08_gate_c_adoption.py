#!/usr/bin/env python3
"""Validate the exact protected P7-T08 physical-matter adoption transaction."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260729-001"
ART = TASK / "artifacts"
REPORT = ART / "p7_t08_gate_c_validation_v1.json"
AUTHORIZATION_ID = "HUMAN-AUTH-P7-T08-PHYSICAL-MATTER-ADOPTION-2026-07-28-001"
DECISION_CODE = "ADOPTED_AS_CANONICAL_PHYSICAL_MATTER_BY_EXPLICIT_HUMAN_POSTULATE"
OBSTRUCTION_ID = "OBST-P7T07-CROSS-LAYER-COMPOSITION-GAP-001"

SOURCES = {
    "TEX-V21-P7-T01-SOURCE-MATTER-ONTOLOGY-SECTOR-TAXONOMY-V1": (
        "research_control/tasks/RT-20260727-007/artifacts/source_matter_ontology_and_sector_taxonomy_v1.tex",
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
    ),
    "TEX-V21-P7-T02-SOURCE-MATTER-FINITE-TRANSITION-KERNEL-V1": (
        "research_control/tasks/RT-20260728-001/artifacts/source_matter_finite_transition_kernel_candidate_v1.tex",
        "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
    ),
    "TEX-V21-P7-T03-SOURCE-OPERATIONAL-DEVICE-SUITE-V1": (
        "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_candidate_v1.tex",
        "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
    ),
    "TEX-V21-P7-T04-COMMON-SOURCE-PROPAGATION-PROFILE-V1": (
        "research_control/tasks/RT-20260728-003/artifacts/common_source_propagation_profile_candidate_v1.tex",
        "87014253023cdb8945ed67f606355d762486884ce3a6de4fa2d32e2af32e2b43",
    ),
    "TEX-V21-P7-T05-UNIVERSAL-SOURCE-COUPLING-MAP-V1": (
        "research_control/tasks/RT-20260728-004/artifacts/universal_source_coupling_map_candidate_v1.tex",
        "5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b",
    ),
    "TEX-V21-P7-T06-SOURCE-KERNEL-VARIATIONAL-OBJECT-V1": (
        "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex",
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is not a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    try:
        approval = load_yaml(ROOT / "research_control/approvals/approval-20260729-001.yaml")
        authorization = load_yaml(ART / "human_authorization_p7_t08_physical_matter_adoption_v1.yaml")
        task = load_yaml(TASK / "00_TASK.yaml")
        job = load_yaml(TASK / "jobs/AJ-RT-20260729-001-001.yaml")
        matrix = load_yaml(ART / "p7_t08_dimension_adoption_matrix_v1.yaml")
        ledger = load_yaml(ART / "p7_t08_constitutive_postulate_ledger_v1.yaml")
        status = load_yaml(ART / "p7_t08_scientific_status_v1.yaml")
        compact = load_json(ART / "p7_t08_gate_c_compact_receipt_v1.json")
        child_math = load_yaml(ART / "child_phys_math_p7_t08_gate_c_adoption.yaml")
        child_phil = load_yaml(ART / "child_phys_phil_p7_t08_gate_c_adoption.yaml")
        conflict = load_yaml(ART / "parent_conflict_review_p7_t08_gate_c_adoption.yaml")
        completion = load_yaml(TASK / "jobs/completions/AJC-AJ-RT-20260729-001-001.yaml")
        handoff = load_yaml(ROOT / "research_control/handoffs/handoff-0897.yaml")
        program_state = load_yaml(ROOT / "research_control/program_state.yaml")
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        report = {
            "schema_id": "p7_t08_gate_c_validation_v1",
            "status": "FAIL",
            "check_count": 1,
            "failure_count": 1,
            "checks": [{"check_id": "required_artifacts_load", "status": "FAIL", "detail": str(exc)}],
        }
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 1

    attachment = Path(str(approval["source_attachment_path"]))
    check("authorization_id", approval.get("human_authorization_id") == AUTHORIZATION_ID, "approval binds the exact authorization ID")
    check("authorization_decision_code", approval.get("decision_code") == DECISION_CODE, "approval carries the affirmative protected verdict")
    check("approval_consumed_once", approval.get("one_time_use") is True and approval.get("status") == "consumed" and approval.get("consumed_by") == job.get("job_id"), "one approval is consumed by the exact job")
    check("authorization_record", authorization.get("human_authorization_id") == AUTHORIZATION_ID and authorization.get("status") == "consumed", "task-local authorization is exact and consumed")
    check("authorization_non_authorizations", bool(authorization.get("non_authorizations")), "authorization records explicit non-authorizations")
    check("attachment_regular", attachment.is_file() and not attachment.is_symlink(), "source attachment is a regular file")
    check("attachment_hash", attachment.is_file() and sha256(attachment) == approval.get("source_attachment_sha256"), "source attachment hash matches")

    protected_changed: set[str] = set()
    diff = subprocess.run(
        ["git", "diff", "--name-only", "--"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    changed_paths = {line.strip() for line in diff.stdout.splitlines() if line.strip()}
    for object_id, (path_text, expected_hash) in SOURCES.items():
        path = ROOT / path_text
        check(f"source_regular:{object_id}", path.is_file() and not path.is_symlink(), f"{path_text} is a regular file")
        check(f"source_hash:{object_id}", path.is_file() and sha256(path) == expected_hash, f"{path_text} retains {expected_hash}")
        if path_text in changed_paths:
            protected_changed.add(path_text)
    check("package_math_unchanged_in_diff", not protected_changed, f"changed protected package paths: {sorted(protected_changed)}")

    p7_audit = ROOT / "research_control/tasks/RT-20260728-006/artifacts/matter_package_smuggling_audit_v1.tex"
    p7_matrix = load_yaml(ROOT / "research_control/tasks/RT-20260728-006/artifacts/gate_c_readiness_matrix_v1.yaml")
    check("p7_t07_audit_hash", sha256(p7_audit) == "f6e0b456dcef8ec4285d6293c76ccc6c6fbe04095e3f0d17023565ee9337187c", "historical audit bytes are unchanged")
    check("p7_t07_gate_outcome", p7_matrix.get("outcome") == "blocked", "historical Gate C audit remains blocked")
    historical = matrix.get("historical_evidence_readiness", {})
    check("historical_zero_of_seven", historical.get("gate_c_ready_dimension_count") == 0 and historical.get("gate_c_required_dimension_count") == 7, "P7-T07 remains zero of seven")
    check("historical_zero_of_ten", historical.get("plan_ready_criterion_count") == 0 and historical.get("plan_required_criterion_count") == 10, "P7-T07 remains zero of ten")
    check("historical_record_not_rewritten", historical.get("historical_record_rewritten") is False, "historical audit is additive and unchanged")

    expected_verdicts = {
        "matter_ontology": "ADOPTED_BY_HUMAN_POSTULATE",
        "source_matter_dynamics": "ADOPTED_BY_HUMAN_POSTULATE",
        "operational_semantics": "ADOPTED_BY_HUMAN_POSTULATE",
        "propagation_geometry_or_structure": "ADOPTED_AS_SOURCE_SIDE_PHYSICAL_PROPAGATION_STRUCTURE",
        "universal_coupling": "ADOPTED_BY_HUMAN_POSTULATE",
        "matter_action": "ADOPTED_BY_HUMAN_POSTULATE",
        "stress_energy_input": "ADOPTED_AS_SOURCE_SIDE_VARIATIONAL_INPUT",
        "physical_conservation": "ADOPTED_WITH_COMPONENTWISE_SCOPE",
        "p8_matter_input": "AUTHORIZED",
    }
    dimensions = matrix.get("protected_dimensions", {})
    check("dimension_key_set", set(dimensions) == set(expected_verdicts), "exact nine protected dimensions are present")
    for name, verdict in expected_verdicts.items():
        check(f"dimension_verdict:{name}", isinstance(dimensions.get(name), dict) and dimensions[name].get("verdict") == verdict, f"{name} has verdict {verdict}")

    postulates = ledger.get("postulates", [])
    expected_postulate_ids = [f"P7-MATTER-POSTULATE-{index:02d}" for index in range(1, 9)]
    check("postulate_id_order", [item.get("postulate_id") for item in postulates] == expected_postulate_ids, "all eight postulates occur once in exact order")
    for item in postulates:
        postulate_id = str(item.get("postulate_id", "unknown"))
        check(f"postulate_source:{postulate_id}", bool(item.get("source_artifact")) and bool(item.get("source_sha256")), f"{postulate_id} binds a source and hash")
        check(f"postulate_math_unchanged:{postulate_id}", item.get("mathematical_content_unchanged") is True, f"{postulate_id} leaves mathematics unchanged")
        check(f"postulate_adopted_not_derived:{postulate_id}", item.get("interpretation_status") == "adopted_not_derived", f"{postulate_id} is adopted rather than derived")
        check(f"postulate_scope:{postulate_id}", bool(item.get("scope")) and bool(item.get("physical_interpretation")), f"{postulate_id} has exact scope and interpretation")
        check(f"postulate_boundaries:{postulate_id}", bool(item.get("downstream_uses")) and bool(item.get("forbidden_overreads")) and bool(item.get("reopening_or_revision_conditions")), f"{postulate_id} has uses, overreads, and revision conditions")

    check("scientific_status_authority", status.get("dimensions", {}).get("authority") == "adopted", "scientific status records adopted authority")
    check("scientific_status_empirical", status.get("dimensions", {}).get("empirical_status") == "untested", "empirical status remains untested")
    check("scientific_status_dynamics", status.get("dimensions", {}).get("dynamics") == "specified", "dynamics is specified, not derived or validated")
    check("scientific_status_operational", status.get("dimensions", {}).get("operational_meaning") == "specified", "operational meaning is specified, not derived or validated")
    check("scientific_status_gate", status.get("authority", {}).get("authority_kind") == "protected_human_gate" and status.get("authority", {}).get("gate_id") == "P7-T08", "adoption binds protected Gate C authority")
    check("no_matter_derivation_authority", status.get("authorization_layers", {}).get("matter_coupling_derivation_authorized") is False, "matter-coupling derivation remains unauthorized")
    check("limited_p7_promotion_authority", status.get("authorization_layers", {}).get("downstream_physics_promotion_authorized") is True, "only the exact P7 physical-status promotion is recorded")

    decision_text = (ART / "p7_t08_gate_c_decision_v1.tex").read_text(encoding="utf-8")
    for token in (
        "ADOPTED\\_AS\\_CANONICAL\\_PHYSICAL\\_MATTER\\_BY\\_EXPLICIT\\_HUMAN\\_POSTULATE",
        OBSTRUCTION_ID,
        "zero of seven",
        "zero of ten",
        "not a mathematical derivation",
        "target-side tensor $T_{\\mu\\nu}$",
        "P8-T01",
    ):
        check(f"decision_token:{token}", token in decision_text, f"decision TeX contains {token}")

    check("child_math_completed", child_math.get("execution_unit_id") == "child_phys_math" and child_math.get("status") == "completed", "physicist-mathematician child completed")
    check("child_phil_completed", child_phil.get("execution_unit_id") == "child_phys_phil" and child_phil.get("status") == "completed", "physicist-philosopher child completed")
    check("conflict_review_resolved", conflict.get("status") == "resolved" and conflict.get("unresolved_conflicts") == [], "parent conflict review has no unresolved conflicts")

    obstruction = matrix.get("obstruction_treatment", {})
    check("obstruction_visible", obstruction.get("obstruction_id") == OBSTRUCTION_ID, "P7-T07 obstruction remains visible")
    check("obstruction_open_gap", obstruction.get("status") == "open_derivational_gap_after_constitutive_adoption", "obstruction is an open derivational gap after adoption")
    check("obstruction_not_adoption_block", obstruction.get("effect_on_adoption") == "does_not_block_human_postulate_adoption", "obstruction no longer blocks protected adoption")

    distance_text = (ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv").read_text(encoding="utf-8")
    frontier_text = (ROOT / "research_control/design/frontier_theorem_inventory.md").read_text(encoding="utf-8")
    claim_registry = (ROOT / "registries/CLAIM_BOUNDARY_REGISTRY.csv").read_text(encoding="utf-8")
    tex_registry = (ROOT / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    check("distance_ledger_adoption", "ADOPTED_AS_CANONICAL_PHYSICAL_MATTER_BY_EXPLICIT_HUMAN_POSTULATE" in distance_text, "Distance-to-GR matter-coupling row records protected adoption")
    check("distance_ledger_gap", "open_derivational_gap_after_constitutive_adoption" in distance_text, "Distance-to-GR ledger preserves the derivational gap")
    check("frontier_decision", "P7-T08 protected physical-matter adoption" in frontier_text and OBSTRUCTION_ID in frontier_text, "frontier inventory records decision and obstruction")
    check("claim_boundary_registry", "CB-V21-P7-T08-PHYSICAL-MATTER-ADOPTION-001" in claim_registry, "claim-boundary registry contains P7-T08")
    check("tex_registry_decision", "TEX-V21-P7-T08-PHYSICAL-MATTER-ADOPTION-DECISION-V1" in tex_registry, "Gate C decision TeX is registered")

    check("task_identity", task.get("implementation_plan", {}).get("plan_task_id") == "P7-T08", "task binds P7-T08")
    check("job_route", job.get("goal_receipt", {}).get("generation") == 154 and job.get("goal_receipt", {}).get("route_worker_skill") == "continue-research", "job binds generation 154 and the immutable worker")
    check("completion_result", completion.get("result_disposition") == "ADOPTED_CANONICAL_PHYSICAL_MATTER_BY_PROTECTED_HUMAN_POSTULATE_READY_FOR_CHECKPOINT", "completion records the affirmative ready-for-checkpoint disposition")
    check("handoff_next", handoff.get("next_plan_task_id") == "P8-T01" and handoff.get("selected_next_route", {}).get("plan_task_id") == "P8-T01", "handoff selects P8-T01 after checkpoint")
    check("handoff_precheckpoint_guard", handoff.get("active_state_boundary", {}).get("checkpoint_completed") is False and handoff.get("active_state_boundary", {}).get("selected_next_execution_ready_now") is False, "handoff does not make P8 executable before checkpoint")
    check("program_state_next", program_state.get("next_plan_task_id") == "P8-T01", "program state points to P8-T01 after checkpoint")
    check("compact_receipt_result", compact.get("result_status") == "ADOPTED_CANONICAL_PHYSICAL_MATTER_BY_PROTECTED_HUMAN_POSTULATE", "compact receipt records the affirmative result")
    check("compact_receipt_counts", compact.get("finding_counts", {}).get("constitutive_postulate_count") == 8 and compact.get("finding_counts", {}).get("protected_adopted_dimension_count") == 9, "compact receipt counts eight postulates and nine dimensions")

    diff_check = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    check("git_diff_check", diff_check.returncode == 0, diff_check.stdout + diff_check.stderr or "git diff --check passes")

    failures = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "p7_t08_gate_c_validation_v1",
        "task_id": "RT-20260729-001",
        "job_id": "AJ-RT-20260729-001-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "source_hash_count": len(SOURCES),
        "postulate_count": len(postulates),
        "dimension_count": len(dimensions),
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
