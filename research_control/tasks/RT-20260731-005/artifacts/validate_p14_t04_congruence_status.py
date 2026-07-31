#!/usr/bin/env python3
"""Validate the bounded P14-T04 protected congruence-status decision."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260731-005"
JOB_ID = "AJ-RT-20260731-005-001"
TASK_DIR = ROOT / "research_control" / "tasks" / TASK_ID
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "p14_t04_congruence_status_validation_v1.json"

IMMUTABLE_HASHES = {
    "ontology/tex/aether_flow_foundations.tex": "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_geometry.tex": "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7",
    "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex": "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260724-009/jobs/completions/AJC-AJ-RT-20260724-009-001.yaml": "58bde0ab8c95797fef15323cf9d6ae12a2b45f0d18de7b2f016d5bef525dc3c4",
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex": "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260726-001/jobs/completions/AJC-AJ-RT-20260726-001-001.yaml": "d866758ebe728146486b117d5825a687035dda311ada6c59eb4c17cde482dcb0",
    "research_control/tasks/RT-20260722-019/artifacts/no_target_positive_provenance_sufficiency_policy_v1.tex": "52c30a55019d38dbc5cb697749189dba4a0bc17db9566dd4c505b21f7db2e456",
    "research_control/tasks/RT-20260722-019/jobs/completions/AJC-AJ-RT-20260722-019-001.yaml": "1996cb234816a9043ea8928661314055570ec1c9c872a7331d0a2a0ef8da5eec",
    "research_control/handoffs/handoff-0926.yaml": "d1d3b56b0a40417a87118f026ccdb5c1ce923e2759da2b24e1c3cff28c10db42",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def csv_row(path: Path, key: str, value: str) -> dict[str, str] | None:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    for rel, expected in IMMUTABLE_HASHES.items():
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else "missing"
        check(f"immutable_hash:{rel}", actual == expected, f"expected={expected} actual={actual}")

    approval = load_yaml(ROOT / "research_control/approvals/approval-20260731-002.yaml")
    check("authorization_exact_text", approval.get("source_message_text") == "I give you authorization", str(approval.get("source_message_text")))
    check("authorization_message_hash", approval.get("source_message_sha256") == "57a11f3bfec16c3614062858678fc415a640e935c5b7ab2e82c2bac973911fbb", str(approval.get("source_message_sha256")))
    check("authorization_journal_binding", approval.get("source_goal_journal_sequence") == 1459 and approval.get("source_goal_journal_entry_sha256") == "8f7fdb5ae10219eec9c1039c31b0eb1e781182443f0d459fca63e123d9651005", "journal sequence and hash")
    check("authorization_consumed_once", approval.get("one_time_use") is True and approval.get("status") == "consumed" and approval.get("consumed_by") == JOB_ID, "one-time use")

    task = load_yaml(TASK_DIR / "00_TASK.yaml")
    job = load_yaml(TASK_DIR / "jobs" / f"{JOB_ID}.yaml")
    role = load_yaml(TASK_DIR / "roles" / f"gate-chair@0.1.0--{TASK_ID}.yaml")
    completion = load_yaml(TASK_DIR / "jobs" / "completions" / f"AJC-{JOB_ID}.yaml")
    downstream = load_yaml(ARTIFACT_DIR / "p14_t04_downstream_requirement_update_v1.yaml")
    child_math = load_yaml(ARTIFACT_DIR / "child_phys_math_p14_t04_congruence_status.yaml")
    child_phil = load_yaml(ARTIFACT_DIR / "child_phys_phil_p14_t04_congruence_status.yaml")
    conflict = load_yaml(ARTIFACT_DIR / "parent_conflict_review_p14_t04_congruence_status.yaml")
    compact = load_json(ARTIFACT_DIR / "p14_t04_congruence_status_compact_receipt_v1.json")
    decision_text = (ARTIFACT_DIR / "p14_t04_congruence_status_decision_v1.tex").read_text(encoding="utf-8")
    fusion_text = (ARTIFACT_DIR / "parent_fusion_notes_p14_t04_congruence_status.md").read_text(encoding="utf-8")

    check("task_completed", task.get("status") == "completed" and task.get("validation_status") == "PASS", f"status={task.get('status')}")
    check("job_completed", job.get("status") == "completed" and job.get("validation_status") == "PASS", f"status={job.get('status')}")
    check("completion_completed", completion.get("status") == "completed" and completion.get("work_item_status") == "completed", f"status={completion.get('status')}")
    check("exact_plan_task", all(obj.get("plan_task_id") == "P14-T04" for obj in (task, job, downstream)), "P14-T04")
    check("exact_milestone_burden", task.get("target_derivation_milestone") == "source_ontology" and task.get("milestone_burden") == "Eliminate ambiguity between interpretation and physical field content.", "source_ontology burden")

    job_writes = job.get("allowed_write_paths")
    role_writes = role.get("allowed_write_paths")
    check("job_role_write_order_identity", isinstance(job_writes, list) and job_writes == role_writes, f"count={len(job_writes or [])}")
    check("canonical_ontology_write_forbidden", "ontology/**" in (job.get("forbidden_paths") or []) and not any(str(item).startswith("ontology/") for item in (job_writes or [])), "ontology write blocked")

    check("math_child_completed", child_math.get("execution_unit_id") == "child_phys_math" and child_math.get("status") == "completed", str(child_math.get("status")))
    check("phil_child_completed", child_phil.get("execution_unit_id") == "child_phys_phil" and child_phil.get("status") == "completed", str(child_phil.get("status")))
    math_blob = json.dumps(child_math, sort_keys=True)
    phil_blob = json.dumps(child_phil, sort_keys=True)
    check("math_child_representative_theorem", "P14T04-THM-TARGET-BENCHMARK-REPRESENTATIVE-INDEPENDENCE-V1" in math_blob and "pure_gauge" in math_blob, "theorem and gauge boundary")
    check("phil_child_status_boundary", "representative" in phil_blob.lower() and "independent" in phil_blob.lower() and "gauge" in phil_blob.lower(), "status vocabulary")

    required_decision_markers = [
        "INTERPRETIVE\\_REPRESENTATIVE\\_TARGET\\_CONGRUENCE\\_ONLY",
        "P14T04-THM-TARGET-BENCHMARK-REPRESENTATIVE-INDEPENDENCE-V1",
        "not a claim that all observer",
        "a source-side gauge-equivalence theorem",
        "does not reduce a physical source-to-GR burden",
        "does not adopt or",
        "modify canonical ontology",
    ]
    check("decision_required_markers", all(marker in decision_text for marker in required_decision_markers), "protected verdict theorem and limits")
    check("downstream_selected_status", downstream.get("decision_code") == "INTERPRETIVE_REPRESENTATIVE_TARGET_CONGRUENCE_ONLY" and downstream.get("status_matrix", {}).get("interpretive_representative", {}).get("status") == "selected", "interpretive representative selected")
    check("downstream_stronger_statuses_blocked", all(downstream.get("status_matrix", {}).get(key, {}).get("status") == "not_established" for key in ("pure_gauge", "dynamically_selected", "independent_dynamical_field")), "three stronger readings not established")
    check("downstream_no_promotion", all(downstream.get("authority", {}).get(key) is False for key in ("canonical_ontology_modified", "source_law_adopted", "physical_field_adopted", "distance_to_gr_delta_changed", "physics_promotion_authorized", "proof_authority", "publication_authorized", "push_authorized")), "all authority flags false")

    check("conflicts_resolved", conflict.get("status") == "resolved" and conflict.get("blocking_conflict_present") is False and conflict.get("unresolved_conflicts") == [], "no unresolved child conflict")
    check("fusion_preserves_children", "Physicist-Mathematician" in fusion_text and "Physicist-Philosopher" in fusion_text and "observer-relative" in fusion_text, "both child perspectives and limit preserved")
    check("completion_parent_child", completion.get("parent_child_synthesis", {}).get("mode") == "parent_child_parallel_synthesis" and completion.get("parent_child_synthesis", {}).get("conflict_review", {}).get("blocking_conflict_present") is False, "parallel synthesis")
    check("completion_no_distance_delta", completion.get("distance_to_gr_delta", {}).get("changed") is False and completion.get("distance_to_gr_delta", {}).get("ledger_row_updated") is False, "no ledger update")
    check("completion_no_promotion", completion.get("physics_promotion_authorized") is False and completion.get("proof_authority") is False, "authority false")

    artifact_map = compact.get("artifact_receipts", {})
    for rel in [
        "child_phys_math_p14_t04_congruence_status.yaml",
        "child_phys_phil_p14_t04_congruence_status.yaml",
        "parent_conflict_review_p14_t04_congruence_status.yaml",
        "parent_fusion_notes_p14_t04_congruence_status.md",
        "p14_t04_congruence_status_decision_v1.tex",
        "p14_t04_downstream_requirement_update_v1.yaml",
    ]:
        expected = artifact_map.get(rel)
        actual = sha256(ARTIFACT_DIR / rel)
        check(f"compact_hash:{rel}", expected == actual, f"expected={expected} actual={actual}")

    task_row = csv_row(ROOT / "registries/RESEARCH_TASK_REGISTRY.csv", "task_id", TASK_ID)
    job_row = csv_row(ROOT / "registries/AGENT_JOB_REGISTRY.csv", "job_id", JOB_ID)
    role_row = csv_row(ROOT / "registries/ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", f"gate-chair@0.1.0--{TASK_ID}")
    decision_row = csv_row(ROOT / "registries/DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260731-005")
    claim_row = csv_row(ROOT / "registries/CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V21-P14-T04-CONGRUENCE-INTERPRETIVE-REPRESENTATIVE-001")
    tex_row = csv_row(ROOT / "registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V21-P14-T04-PROTECTED-CONGRUENCE-STATUS-DECISION-V1")
    md_row = csv_row(ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V21-P14-T04-PARENT-FUSION-CONGRUENCE-STATUS-V1")
    check("task_registry_row", bool(task_row and task_row.get("status") == "completed"), str(task_row and task_row.get("status")))
    check("job_registry_row", bool(job_row and job_row.get("status") == "completed"), str(job_row and job_row.get("status")))
    check("role_registry_row", bool(role_row and role_row.get("validation_status") == "PASS"), str(role_row and role_row.get("validation_status")))
    check("decision_registry_row", bool(decision_row and decision_row.get("status") == "completed"), str(decision_row and decision_row.get("status")))
    check("claim_registry_row", bool(claim_row and claim_row.get("status") == "completed"), str(claim_row and claim_row.get("status")))
    check("registry_write_order_identity", bool(job_row and role_row and job_row.get("allowed_write_paths", "").split(";") == job_writes == role_row.get("allowed_write_paths", "").split(";")), "job role and registry order")
    check("tex_registry_hash", bool(tex_row and tex_row.get("source_hash") == sha256(ARTIFACT_DIR / "p14_t04_congruence_status_decision_v1.tex")), str(tex_row and tex_row.get("source_hash")))
    check("markdown_registry_hash", bool(md_row and md_row.get("source_hash") == sha256(ARTIFACT_DIR / "parent_fusion_notes_p14_t04_congruence_status.md")), str(md_row and md_row.get("source_hash")))

    program = load_yaml(ROOT / "research_control/program_state.yaml")
    handoff = load_yaml(ROOT / "research_control/handoffs/handoff-0927.yaml")
    check("program_state_active", program.get("active_task_id") == TASK_ID and program.get("latest_handoff_id") == "handoff-0927", f"{program.get('active_task_id')} {program.get('latest_handoff_id')}")
    check("handoff_identity", handoff.get("task_id") == TASK_ID and handoff.get("job_id") == JOB_ID and handoff.get("plan_task_id") == "P14-T04", "handoff-0927")
    check("handoff_completion_hash", handoff.get("completion_sha256") == sha256(TASK_DIR / "jobs" / "completions" / f"AJC-{JOB_ID}.yaml"), str(handoff.get("completion_sha256")))

    failures = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "v21_p14_t04_congruence_status_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "checks": checks,
        "authority_note": "This operational validation does not create theorem truth, ontology adoption, field content, physics promotion, proof, publication, or push authority.",
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.check:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
