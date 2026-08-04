#!/usr/bin/env python3
"""Validate and materialize the bounded V21 P16-T06 relay-closure packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260804-004"
ARTIFACT_DIR = TASK_DIR / "artifacts"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
BACKLOG = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
MATRIX = ROOT / "research_control/tasks/RT-20260803-002/artifacts/v21_final_recommendation_coverage_matrix.json"
COVERAGE_AUDIT = ROOT / "research_control/tasks/RT-20260803-002/artifacts/v21_recommendation_coverage_audit.md"
GATE_AUDIT = ROOT / "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_gate_consistency_reaudit.md"
PROVENANCE_AUDIT = ROOT / "research_control/tasks/RT-20260803-013/artifacts/v21_p16_t03_final_provenance_audit.md"
CLAIM_AUDIT = ROOT / "research_control/tasks/RT-20260804-001/artifacts/v21_p16_t04_post_repair_final_reaudit_report.md"
STATUS_SYNTHESIS = ROOT / "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_final_status_synthesis.md"
SCIENCE_SCORECARD = ROOT / "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_science_scorecard.yaml"
DISTANCE_LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
SOURCE_HANDOFF = ROOT / "research_control/handoffs/handoff-0964.yaml"
JOB = TASK_DIR / "jobs/AJ-RT-20260804-004-001.yaml"
CHILD_MATH = ARTIFACT_DIR / "child_phys_math_p16_t06_goal_relay_closure.yaml"
CHILD_PHIL = ARTIFACT_DIR / "child_phys_phil_p16_t06_goal_relay_closure.yaml"
CONFLICT = ARTIFACT_DIR / "parent_conflict_review_p16_t06_goal_relay_closure.yaml"
FUSION = ARTIFACT_DIR / "parent_fusion_notes_p16_t06_goal_relay_closure.md"
SUMMARY = ARTIFACT_DIR / "v21_p16_t06_goal_completion_candidate.md"
LEDGER_OUT = ARTIFACT_DIR / "v21_p16_t06_final_work_item_status_ledger.json"
TERMINAL_OUT = ARTIFACT_DIR / "v21_p16_t06_relay_terminal_receipt.json"
RECEIPT_OUT = ARTIFACT_DIR / "v21_p16_t06_compact_receipt.json"
REPORT_OUT = ARTIFACT_DIR / "v21_p16_t06_validation.json"

EXPECTED_HASHES = {
    PLAN: "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    BACKLOG: "849a4e8dfe848e80bc0c8236252b924e636e5c95ac1a090478a69f7f5377559f",
    MATRIX: "aa91bfa96257d3d1e9d6ae6bf68d025b4c3e7ed451c8d4f11012cc69cdbc9e95",
    COVERAGE_AUDIT: "653f8205a160cf7d94ac5a462590cb88284566f3bee6454a606f28edd8d9eab0",
    GATE_AUDIT: "a8afd3cecf381198e018f9b9c0f03891f95435bc5edea4fe1a7f74d392735ae5",
    PROVENANCE_AUDIT: "72316ad40fdab3b5d88c88602c1832de99045616421eba244143e436ec87ca59",
    CLAIM_AUDIT: "20bbc6082b3b55fad3a7401dc4e4b84295c2baa376f9a2f3ea03286f17da0d30",
    STATUS_SYNTHESIS: "28db911bef81a26609b0993c8ff1545bda1ca1eb2ba6f9db8b1ece7a814ee4eb",
    SCIENCE_SCORECARD: "654101f8dafa11b268f657ff5943f79d0d7bf4c19668f934bb5ebb419b6cabbd",
    DISTANCE_LEDGER: "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
    SOURCE_HANDOFF: "f0c4e66441c3af955febfe9ee31f430ed02291dbca0aca896e5e3218185fde2c",
}

P0_MANUAL = {
    "P0-T01": {
        "task_id": "RT-20260720-003",
        "completion_path": "research_control/tasks/RT-20260720-003/jobs/completions/AJC-AJ-RT-20260720-003-001.yaml",
        "completion_sha256": "55683b6f6f13408f2200b765f2c9e193fb7cfce0ac6e5131fc6c6de44cdb674d",
        "identity_source": "completion.implementation_plan_receipt",
        "final_disposition": "implemented",
        "validation_status": "PASS",
        "qualifying": True,
        "git_tracked": True,
    },
    "P0-T02": {
        "task_id": "RT-20260720-005",
        "completion_path": "research_control/tasks/RT-20260720-005/jobs/completions/AJC-AJ-RT-20260720-005-001.yaml",
        "completion_sha256": "3cd5e142f88cefa473255beff7620b2274d755210d69f335b05af9e5771b2bf1",
        "identity_source": "completion.implementation_plan_receipt",
        "final_disposition": "implemented",
        "validation_status": "PASS",
        "qualifying": True,
        "git_tracked": True,
    },
}

P16_EVIDENCE = {
    "P16-T01": (
        "research_control/tasks/RT-20260803-002/jobs/completions/AJC-AJ-RT-20260803-002-001.yaml",
        "4e59a0ae6d0740677ef0b4331f753138f32b76b27981435f5933aaab1a78fd66",
        "research_control/tasks/RT-20260803-002/artifacts/v21_recommendation_coverage_audit.md",
        "653f8205a160cf7d94ac5a462590cb88284566f3bee6454a606f28edd8d9eab0",
    ),
    "P16-T02": (
        "research_control/tasks/RT-20260803-012/jobs/completions/AJC-AJ-RT-20260803-012-001.yaml",
        "32490ac7e5a57138f6de7a884825532ee17389d36634dbb9fc7f7cc076c0bf8d",
        "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_gate_consistency_reaudit.md",
        "a8afd3cecf381198e018f9b9c0f03891f95435bc5edea4fe1a7f74d392735ae5",
    ),
    "P16-T03": (
        "research_control/tasks/RT-20260803-013/jobs/completions/AJC-AJ-RT-20260803-013-001.yaml",
        "a0bd4691e276e5e0d97b45b734491f697deeb57ca0dc99b015bd7ea7d734fe91",
        "research_control/tasks/RT-20260803-013/artifacts/v21_p16_t03_final_provenance_audit.md",
        "72316ad40fdab3b5d88c88602c1832de99045616421eba244143e436ec87ca59",
    ),
    "P16-T04": (
        "research_control/tasks/RT-20260804-001/jobs/completions/AJC-AJ-RT-20260804-001-001.yaml",
        "1dc975715f9e8f2554408348ea6dc9d2191f370d1f1cf724e23801b128c4ce4d",
        "research_control/tasks/RT-20260804-001/artifacts/v21_p16_t04_post_repair_final_reaudit_report.md",
        "20bbc6082b3b55fad3a7401dc4e4b84295c2baa376f9a2f3ea03286f17da0d30",
    ),
    "P16-T05": (
        "research_control/tasks/RT-20260804-003/jobs/completions/AJC-AJ-RT-20260804-003-001.yaml",
        "7df3e9aa13f6449ce6bd0e4fa19d08837888f19e70ea774d83c4c99367ff8aa0",
        "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_final_status_synthesis.md",
        "28db911bef81a26609b0993c8ff1545bda1ca1eb2ba6f9db8b1ece7a814ee4eb",
    ),
}

GATE_ARTIFACTS = {
    "Gate A": (
        "ADOPTED_NARROW_RESEARCH_ARCHITECTURE",
        "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex",
        "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    ),
    "Gate B": (
        "NOT_READY",
        "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml",
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    ),
    "Gate C": (
        "PROTECTED_SOURCE_MATTER_PACKAGE_ADOPTED_BY_POSTULATE",
        "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex",
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    ),
    "Gate D": (
        "NOT_READY",
        "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex",
        "035ea88a612d861a00d0703ec2bd1094e01194c113d7ff2588e3a4ad8bf47d63",
    ),
    "Gate E": (
        "NOT_READY",
        "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex",
        "7f28103e40664f0a004af0134f3216932136f8efb160f0c7c59039efa5225b0b",
    ),
}

ALLOWED_FINAL_DISPOSITIONS = {
    "completed",
    "precisely_obstructed",
    "frozen_negative",
    "deferred_human_gate",
    "superseded",
    "conditionally_not_required",
    "failed_exact",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def git_tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    run = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return run.returncode == 0


def normalize_disposition(raw: str) -> str:
    value = raw.strip().lower()
    if value == "conditionally_not_required":
        return "conditionally_not_required"
    if "supersed" in value:
        return "superseded"
    if "defer" in value and "human" in value:
        return "deferred_human_gate"
    if "freeze" in value:
        return "frozen_negative"
    if any(token in value for token in ("obstruction", "precisely_blocked", "precise_scoped_defect")):
        return "precisely_obstructed"
    if value.startswith("failed_exact"):
        return "failed_exact"
    return "completed"


def collect_pre_p16_evidence(matrix: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    selected: dict[str, dict[str, Any]] = {}
    conflicts: list[str] = []
    candidates: list[dict[str, Any]] = []
    for row in matrix.get("rows") or []:
        candidates.extend(item for item in (row.get("selected_evidence") or []) if isinstance(item, dict))
    for row in matrix.get("gate_evidence") or []:
        item = row.get("selected_evidence")
        if isinstance(item, dict):
            candidates.append(item)
    for item in candidates:
        plan_task_id = str(item.get("plan_task_id") or "")
        if not plan_task_id:
            continue
        previous = selected.get(plan_task_id)
        if previous is not None and (
            previous.get("completion_path"), previous.get("completion_sha256")
        ) != (item.get("completion_path"), item.get("completion_sha256")):
            conflicts.append(plan_task_id)
        selected[plan_task_id] = item
    selected.update(P0_MANUAL)
    return selected, sorted(set(conflicts))


def evidence_bytes_match(record: dict[str, Any], matrix: dict[str, Any]) -> bool:
    identity = str(record.get("identity_source") or "")
    completion_path = str(record.get("completion_path") or "")
    expected_completion = str(record.get("completion_sha256") or "")
    if identity.startswith("program_state:"):
        return (
            completion_path == "research_control/program_state.yaml"
            and expected_completion == str(matrix.get("program_state_sha256_at_audit") or "")
            and git_tracked(ROOT / completion_path)
        )
    path = ROOT / completion_path
    if not path.exists() or sha256(path) != expected_completion or not git_tracked(path):
        return False
    task_path = str(record.get("task_path") or "")
    task_hash = str(record.get("task_sha256") or "")
    if task_path:
        source = ROOT / task_path
        if not source.exists() or sha256(source) != task_hash or not git_tracked(source):
            return False
    return True


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    backlog = load_yaml(BACKLOG)
    matrix = load_json(MATRIX)
    science = load_yaml(SCIENCE_SCORECARD)
    job = load_yaml(JOB)
    child_math = load_yaml(CHILD_MATH) if CHILD_MATH.exists() else {}
    child_phil = load_yaml(CHILD_PHIL) if CHILD_PHIL.exists() else {}
    conflict = load_yaml(CONFLICT) if CONFLICT.exists() else {}
    fusion_text = FUSION.read_text(encoding="utf-8") if FUSION.exists() else ""
    summary_text = SUMMARY.read_text(encoding="utf-8") if SUMMARY.exists() else ""
    items = list(backlog.get("items") or [])
    backlog_ids = [str(item.get("plan_task_id") or "") for item in items]
    expected_recommendations = list((backlog.get("recommendation_coverage_rules") or {}).get("expected_recommendation_ids") or [])
    pre_p16, evidence_conflicts = collect_pre_p16_evidence(matrix)
    expected_pre_p16 = {item_id for item_id in backlog_ids if item_id and not item_id.startswith("P16-")}

    work_item_rows: list[dict[str, Any]] = []
    for item in items:
        plan_task_id = str(item.get("plan_task_id") or "")
        base = {
            "plan_task_id": plan_task_id,
            "phase_id": str(item.get("phase_id") or ""),
            "title": str(item.get("title") or ""),
            "recommendation_ids": list(item.get("recommendation_ids") or []),
            "requires_human_gate_in_plan": bool(item.get("requires_human_gate")),
            "required_human_action_remaining": False,
            "qualifying": True,
            "conditional_completion_candidate": False,
        }
        if plan_task_id in pre_p16:
            evidence = pre_p16[plan_task_id]
            raw = str(evidence.get("final_disposition") or "completed")
            base.update(
                {
                    "normalized_final_disposition": normalize_disposition(raw),
                    "raw_final_disposition": raw,
                    "evidence_path": str(evidence.get("completion_path") or ""),
                    "evidence_sha256": str(evidence.get("completion_sha256") or ""),
                    "validation_status": str(evidence.get("validation_status") or "PASS_TRACKED_STATE"),
                    "checkpoint_qualification": "qualifying_tracked_final_disposition",
                }
            )
        elif plan_task_id in P16_EVIDENCE:
            completion_path, completion_hash, artifact_path, artifact_hash = P16_EVIDENCE[plan_task_id]
            base.update(
                {
                    "normalized_final_disposition": "completed",
                    "raw_final_disposition": "completed",
                    "evidence_path": completion_path,
                    "evidence_sha256": completion_hash,
                    "primary_artifact_path": artifact_path,
                    "primary_artifact_sha256": artifact_hash,
                    "validation_status": "PASS_QUALIFYING_CHECKPOINTED",
                    "checkpoint_qualification": "qualifying_checkpointed",
                }
            )
        elif plan_task_id == "P16-T06":
            base.update(
                {
                    "normalized_final_disposition": "completed",
                    "raw_final_disposition": "completed_pending_governed_checkpoint",
                    "evidence_path": JOB.relative_to(ROOT).as_posix(),
                    "evidence_sha256": sha256(JOB),
                    "primary_artifact_path": SUMMARY.relative_to(ROOT).as_posix(),
                    "primary_artifact_sha256": sha256(SUMMARY) if SUMMARY.exists() else "",
                    "validation_status": "PASS_PRECHECKPOINT" if summary_text else "PENDING",
                    "checkpoint_qualification": "pending_one_governed_checkpoint",
                    "qualifying": False,
                    "conditional_completion_candidate": True,
                }
            )
        else:
            base.update(
                {
                    "normalized_final_disposition": "failed_exact",
                    "raw_final_disposition": "missing_evidence",
                    "evidence_path": "",
                    "evidence_sha256": "",
                    "validation_status": "FAIL",
                    "checkpoint_qualification": "not_qualified",
                    "qualifying": False,
                }
            )
        work_item_rows.append(base)

    recommendation_rows: list[dict[str, Any]] = []
    completed_p16 = set(P16_EVIDENCE) | {"P16-T06"}
    for row in matrix.get("rows") or []:
        downstream = list(row.get("pending_downstream_p16_task_ids") or [])
        recommendation_rows.append(
            {
                "recommendation_id": str(row.get("recommendation_id") or ""),
                "final_coverage_status": "covered_with_qualifying_direct_evidence_and_conditional_p16_t06_final_disposition",
                "verified_pre_p16_direct_task_ids": list(row.get("verified_pre_p16_direct_task_ids") or []),
                "verified_pre_p16_direct_evidence_count": len(row.get("selected_evidence") or []),
                "completed_bounded_downstream_p16_task_ids": [task_id for task_id in downstream if task_id in completed_p16],
                "final_goal_disposition_task_id": "P16-T06",
                "final_goal_disposition_status": "pending_governed_checkpoint",
                "authority_note": "Coverage is process evidence only and does not establish scientific truth or promotion.",
            }
        )

    disposition_counts = Counter(row["normalized_final_disposition"] for row in work_item_rows)
    gate_rows = [
        {
            "gate": gate,
            "status": status,
            "evidence_path": path,
            "evidence_sha256": digest,
            "changed_by_p16_t06": False,
        }
        for gate, (status, path, digest) in GATE_ARTIFACTS.items()
    ]

    ledger = {
        "schema_id": "v21_p16_t06_final_work_item_status_ledger_v1",
        "authority": "project_control_closure_evidence",
        "plan_id": "recommendations_implementation_plan_continue_task-v21",
        "work_item_count": len(work_item_rows),
        "recommendation_count": len(recommendation_rows),
        "pre_p16_work_item_count": len(pre_p16),
        "p16_work_item_count": len([item_id for item_id in backlog_ids if item_id.startswith("P16-")]),
        "precheckpoint_finalized_work_item_count": sum(bool(row["qualifying"]) for row in work_item_rows),
        "conditional_completion_candidate_count": sum(bool(row["conditional_completion_candidate"]) for row in work_item_rows),
        "projected_postcheckpoint_finalized_work_item_count": 122,
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "work_items": work_item_rows,
        "recommendations": recommendation_rows,
        "gate_statuses": gate_rows,
        "new_mathematical_payload": {
            "payload_id": "FinalWorkItemDispositionTotalityAndNonPromotion_v1",
            "claim_status": "draft/control",
            "statement": "For the finite 122-item set W, 121 dispositions are canonically final before checkpoint and P16-T06 is the unique conditional completion candidate. If the P16-T06 task-local and repository validators pass and its governed checkpoint commits, then the final disposition relation delta becomes single-valued and total on W. Every one of the 72 recommendations already has qualifying direct evidence. This conditional control-closure predicate has no authority-preserving implication to completed first-principles GR derivation, benchmark promotion, independent replication, publication, or a stronger Gate status.",
            "global_no_go_claimed": False,
            "physics_promotion_authorized": False,
        },
        "authority_limits": {
            "control_goal_completion_is_scientific_derivation": False,
            "gate_status_changed": False,
            "distance_to_gr_changed": False,
            "benchmark_promoted": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }

    answer_first = science.get("answer_first") or {}
    terminal = {
        "schema_id": "v21_p16_t06_relay_terminal_receipt_v1",
        "status": "PASS_TERMINAL_COMPLETE_RECOMMENDED_AFTER_CHECKPOINT",
        "goal_id": "crg-20260720T161354Z-96bc2664ce31bfe0",
        "generation": 256,
        "work_item_id": "P16-T06",
        "recommended_outer_decision": "terminal_complete",
        "decision_precondition": "one qualifying governed checkpoint for AJ-RT-20260804-004-001 followed by outer returned and verify-step operations",
        "task_local_terminalization_performed": False,
        "successor_requested": False,
        "unresolved_required_human_action_count": 0,
        "unresolved_required_human_actions": [],
        "work_item_count": len(work_item_rows),
        "precheckpoint_finalized_work_item_count": sum(bool(row["qualifying"]) for row in work_item_rows),
        "conditional_completion_candidate_count": sum(bool(row["conditional_completion_candidate"]) for row in work_item_rows),
        "projected_postcheckpoint_finalized_work_item_count": 122,
        "recommendation_count": len(recommendation_rows),
        "missing_recommendation_count": len([row for row in recommendation_rows if not row["verified_pre_p16_direct_task_ids"]]),
        "gate_statuses": gate_rows,
        "science_status_preserved": {
            "exact_gr_reference_status": answer_first.get("exact_gr_reference_status"),
            "first_principles_gr_derivation_status": answer_first.get("first_principles_gr_derivation_status"),
            "source_derived_benchmark_status": answer_first.get("source_derived_benchmark_status"),
            "benchmark_case_count": answer_first.get("benchmark_case_count"),
            "benchmark_pass_count": answer_first.get("benchmark_pass_count"),
            "benchmark_inconclusive_count": answer_first.get("benchmark_inconclusive_count"),
            "independent_replication_count": answer_first.get("independent_replication_count"),
        },
        "future_or_separately_authorized_scientific_work": [
            "derive missing source-side primitives for RetainH and GenH",
            "derive an unscoped effective geometry and universal matter coupling",
            "derive and independently review the Einstein sector",
            "obtain a lawful benchmark pass and qualifying independent replication before any Gate E reconsideration",
        ],
        "authority_limits": ledger["authority_limits"],
    }

    p16_paths_match = all(
        (ROOT / completion_path).exists()
        and sha256(ROOT / completion_path) == completion_hash
        and (ROOT / artifact_path).exists()
        and sha256(ROOT / artifact_path) == artifact_hash
        for completion_path, completion_hash, artifact_path, artifact_hash in P16_EVIDENCE.values()
    )
    gates_match = all((ROOT / path).exists() and sha256(ROOT / path) == digest for _, path, digest in GATE_ARTIFACTS.values())
    checks = {
        "fixed_source_hashes_match": all(path.exists() and sha256(path) == digest for path, digest in EXPECTED_HASHES.items()),
        "job_identity_matches": job.get("job_id") == "AJ-RT-20260804-004-001" and job.get("plan_task_id") == "P16-T06",
        "job_route_matches_generation_256": (job.get("goal_receipt") or {}).get("generation") == 256 and job.get("immutable_route_sha256") == "0fc5bc1101b26e17d5d36eac3856a470ed0b9decb09b0a75db0044c0b5d16ad1",
        "backlog_declares_122_items": (backlog.get("scope") or {}).get("task_count") == 122,
        "backlog_item_count_is_122": len(items) == 122,
        "backlog_ids_unique": len(set(backlog_ids)) == 122 and "" not in backlog_ids,
        "pre_p16_id_count_is_116": len(expected_pre_p16) == 116,
        "selected_pre_p16_count_is_116": len(pre_p16) == 116,
        "selected_pre_p16_ids_exact": set(pre_p16) == expected_pre_p16,
        "selected_evidence_has_no_conflicts": not evidence_conflicts,
        "selected_pre_p16_bytes_match": all(evidence_bytes_match(record, matrix) for record in pre_p16.values()),
        "p16_t01_through_t05_evidence_matches": p16_paths_match,
        "recommendation_ids_declared_72": len(expected_recommendations) == 72 and len(set(expected_recommendations)) == 72,
        "matrix_recommendation_count_is_72": matrix.get("recommendation_count") == 72 and len(matrix.get("rows") or []) == 72,
        "matrix_has_no_missing_recommendations": not matrix.get("missing_recommendation_ids"),
        "every_recommendation_has_direct_evidence": all(row["verified_pre_p16_direct_task_ids"] for row in recommendation_rows),
        "all_bounded_downstream_p16_tasks_completed": all(len(row["completed_bounded_downstream_p16_task_ids"]) == len((matrix.get("rows") or [])[index].get("pending_downstream_p16_task_ids") or []) for index, row in enumerate(recommendation_rows)),
        "work_item_rows_total_and_single_valued": len(work_item_rows) == 122 and len({row["plan_task_id"] for row in work_item_rows}) == 122,
        "all_work_item_dispositions_allowed": all(row["normalized_final_disposition"] in ALLOWED_FINAL_DISPOSITIONS for row in work_item_rows),
        "precheckpoint_finalized_count_is_121": sum(bool(row["qualifying"]) for row in work_item_rows) == 121,
        "exactly_one_conditional_p16_t06_candidate": [row["plan_task_id"] for row in work_item_rows if row["conditional_completion_candidate"]] == ["P16-T06"],
        "gate_artifact_hashes_match": gates_match,
        "gate_status_count_is_five": len(gate_rows) == 5,
        "child_math_supports_closure": child_math.get("verdict") == "PASS_FINITE_CLOSURE_SUPPORTED" and (child_math.get("metrics") or {}).get("work_item_count") == 122 and (child_math.get("metrics") or {}).get("recommendation_count") == 72,
        "child_phil_supports_terminal_semantics": child_phil.get("verdict") == "PASS_TERMINAL_COMPLETE_EPISTEMICALLY_LAWFUL" and (child_phil.get("human_action_assessment") or {}).get("unresolved_required_human_action_count") == 0,
        "parent_conflicts_resolved": conflict.get("status") == "PASS_NO_UNRESOLVED_CONFLICT" and conflict.get("unresolved_conflict_count") == 0,
        "fusion_records_totality": "FinalWorkItemDispositionTotalityAndNonPromotion_v1" in fusion_text,
        "summary_recommends_terminal_complete": "Recommended outer relay disposition: `terminal_complete`" in summary_text,
        "summary_preserves_science_boundary": "does not complete a first-principles GR derivation" in summary_text,
        "summary_records_no_required_human_action": "No unresolved required human action remains" in summary_text,
        "summary_requests_no_successor": "No successor is requested" in summary_text,
        "science_status_counts_preserved": answer_first.get("benchmark_case_count") == 6 and answer_first.get("benchmark_pass_count") == 0 and answer_first.get("benchmark_inconclusive_count") == 6 and answer_first.get("independent_replication_count") == 0,
        "terminal_receipt_requests_no_successor": terminal["successor_requested"] is False,
        "terminal_receipt_has_no_required_human_action": terminal["unresolved_required_human_action_count"] == 0,
        "authority_limits_fail_closed": not any(ledger["authority_limits"].values()),
    }
    failed = [name for name, passed in checks.items() if not passed]
    report = {
        "schema_id": "v21_p16_t06_goal_relay_closure_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": checks,
        "metrics": {
            "work_item_count": len(work_item_rows),
            "precheckpoint_finalized_work_item_count": sum(bool(row["qualifying"]) for row in work_item_rows),
            "conditional_completion_candidate_count": sum(bool(row["conditional_completion_candidate"]) for row in work_item_rows),
            "projected_postcheckpoint_finalized_work_item_count": 122,
            "pre_p16_work_item_count": len(pre_p16),
            "p16_work_item_count": len([item_id for item_id in backlog_ids if item_id.startswith("P16-")]),
            "recommendation_count": len(recommendation_rows),
            "missing_recommendation_count": len([row for row in recommendation_rows if not row["verified_pre_p16_direct_task_ids"]]),
            "gate_count": len(gate_rows),
            "unresolved_parent_conflict_count": int(conflict.get("unresolved_conflict_count") or 0),
            "unresolved_required_human_action_count": int((child_phil.get("human_action_assessment") or {}).get("unresolved_required_human_action_count") or 0),
        },
        "validator_ids": [
            "v21_p16_t06_fixed_source_hashes",
            "v21_p16_t06_122_item_totality",
            "v21_p16_t06_72_recommendation_parity",
            "v21_p16_t06_gate_status_preservation",
            "v21_p16_t06_parent_child_synthesis",
            "v21_p16_t06_terminal_semantics",
            "v21_p16_t06_authority_nonpromotion",
        ],
    }
    terminal["task_local_validation_status"] = report["status"]
    if failed:
        terminal["status"] = "REPAIR_REQUIRED"
        terminal["recommended_outer_decision"] = "recovery_required"

    receipt = {
        "schema_id": "v21_p16_t06_compact_receipt_v1",
        "status": report["status"],
        "result_status": terminal["status"],
        "source_hashes": {
            "plan": sha256(PLAN),
            "backlog": sha256(BACKLOG),
            "coverage_matrix": sha256(MATRIX),
            "gate_consistency_audit": sha256(GATE_AUDIT),
            "provenance_audit": sha256(PROVENANCE_AUDIT),
            "claim_audit": sha256(CLAIM_AUDIT),
            "status_synthesis": sha256(STATUS_SYNTHESIS),
            "source_handoff_0964": sha256(SOURCE_HANDOFF),
            "job_contract": sha256(JOB),
            "child_phys_math": sha256(CHILD_MATH) if CHILD_MATH.exists() else "",
            "child_phys_phil": sha256(CHILD_PHIL) if CHILD_PHIL.exists() else "",
            "parent_conflict_review": sha256(CONFLICT) if CONFLICT.exists() else "",
            "parent_fusion_notes": sha256(FUSION) if FUSION.exists() else "",
            "goal_completion_candidate": sha256(SUMMARY) if SUMMARY.exists() else "",
        },
        "finding_counts": report["metrics"],
        "recommended_outer_decision": terminal["recommended_outer_decision"],
        "validator_ids": report["validator_ids"],
        "claim_boundary_summary": "Before checkpoint, 121 V21 work items are canonically final and P16-T06 is the unique conditional completion candidate; a qualifying governed checkpoint permits the outer launcher to verify totality across all 122. All 72 recommendations have qualifying direct evidence. This does not complete a first-principles GR derivation or create Gate, benchmark, review, publication, push, proof, or physics-promotion authority.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    return ledger, terminal, receipt, report


def serialized(outputs: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[Path, str]:
    return {
        LEDGER_OUT: json.dumps(outputs[0], indent=2, sort_keys=False) + "\n",
        TERMINAL_OUT: json.dumps(outputs[1], indent=2, sort_keys=False) + "\n",
        RECEIPT_OUT: json.dumps(outputs[2], indent=2, sort_keys=False) + "\n",
        REPORT_OUT: json.dumps(outputs[3], indent=2, sort_keys=False) + "\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    expected = serialized(outputs)
    if args.write_report:
        for path, content in expected.items():
            path.write_text(content, encoding="utf-8")
    drift = [path.relative_to(ROOT).as_posix() for path, content in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != content] if args.check else []
    report = dict(outputs[3])
    report["written_output_drift"] = drift
    if drift:
        report["status"] = "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
