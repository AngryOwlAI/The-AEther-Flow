#!/usr/bin/env python3
"""Validate the bounded P15-T05 Gate E no-manuscript disposition."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260731-010"

EXPECTED_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/v21_recommendation_backlog.yaml":
        "849a4e8dfe848e80bc0c8236252b924e636e5c95ac1a090478a69f7f5377559f",
    "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex":
        "7f28103e40664f0a004af0134f3216932136f8efb160f0c7c59039efa5225b0b",
    "research_control/tasks/RT-20260731-004/jobs/completions/AJC-AJ-RT-20260731-004-001.yaml":
        "5c64250eea3f702051c1403b1ec9b2edd85f00d7937b2647965526f124ab3ee6",
    "research_control/handoffs/handoff-0931.yaml":
        "b0a72a9f55178ef71bf0bc529534711b35b4fe130b62286ddcb162d047fbb7b2",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(rel: str):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    findings: list[dict[str, str]] = []

    def check(ok: bool, code: str, detail: str) -> None:
        if not ok:
            findings.append({"code": code, "detail": detail})

    for rel, expected in EXPECTED_HASHES.items():
        path = ROOT / rel
        check(path.is_file() and not path.is_symlink(), "SOURCE_MISSING", rel)
        if path.is_file():
            check(sha(path) == expected, "SOURCE_HASH_MISMATCH", rel)

    approval = load_yaml("research_control/approvals/approval-20260731-003.yaml")
    check(approval.get("status") == "consumed", "APPROVAL_NOT_CONSUMED", str(approval.get("status")))
    check(approval.get("consumed_by") == "AJ-RT-20260731-010-001", "APPROVAL_JOB_MISMATCH", str(approval.get("consumed_by")))
    check(approval.get("one_time_use") is True, "APPROVAL_NOT_ONE_TIME", "one_time_use must be true")
    check(approval.get("source_message_sha256") == "15029c7d9ad3d753722db20238c8e7a102a0425cb4b82fa671bc1c28dcb8b4cf", "AUTH_MESSAGE_HASH_MISMATCH", "exact user message")
    check(approval.get("source_goal_journal_entry_sha256") == "7b4640454127637f0b510bfbae3f673b1b691b3aa1fcd23a6c69569b3827cc99", "GOAL_JOURNAL_HASH_MISMATCH", "journal sequence 1504")

    route = load_yaml("research_control/tasks/RT-20260731-010/artifacts/protected_recursive_goal_route_receipt_v1.yaml")
    check(route.get("generation") == 198, "ROUTE_GENERATION_MISMATCH", str(route.get("generation")))
    check(route.get("route_sha256") == "a93a851265a073a15e3c91028bbc0890924ca083107d0a75a7adea4e8be06bc1", "ROUTE_HASH_MISMATCH", str(route.get("route_sha256")))
    check(route.get("consumed_worker_invocation_count") == 1, "INVOCATION_COUNT_MISMATCH", str(route.get("consumed_worker_invocation_count")))

    gate_text = (ROOT / "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex").read_text(encoding="utf-8")
    for token in (
        "NOT\\_READY\\_BENCHMARK\\_AND\\_COMPLETED\\_DERIVATION\\_REQUIREMENTS\\_UNMET",
        "zero passes",
        "zero qualifying independent replications",
        "Reopening requires materially new",
    ):
        check(token in gate_text, "GATE_E_TOKEN_MISSING", token)

    tex_path = TASK / "artifacts/p15_t05_gate_e_no_manuscript_disposition_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    for token in (
        "P15T05-PROP-FIXED-GATE-E-NO-MANUSCRIPT-V1",
        "CONDITIONALLY\\_NOT\\_REQUIRED\\_GATE\\_E\\_NOT\\_READY\\_NO\\_MANUSCRIPT",
        "P_M(E_0)\\Longleftrightarrow G_E(E_0)",
        "No derivation manuscript is created",
        "changes no physical",
    ):
        check(token in tex, "DISPOSITION_TOKEN_MISSING", token)

    for child in ("child_phys_math", "child_phys_phil"):
        rel = f"research_control/tasks/RT-20260731-010/artifacts/{child}_p15_t05_gate_e_disposition.yaml"
        path = ROOT / rel
        check(path.is_file() and not path.is_symlink(), "CHILD_OUTPUT_MISSING", rel)
        if path.is_file():
            data = load_yaml(rel)
            check(data.get("status") == "completed", "CHILD_NOT_COMPLETED", rel)
            check(data.get("blocking_conflict_present") is False, "CHILD_BLOCKING_CONFLICT", rel)

    for rel in (
        "research_control/tasks/RT-20260731-010/artifacts/parent_conflict_review_p15_t05_gate_e_disposition.yaml",
        "research_control/tasks/RT-20260731-010/artifacts/parent_fusion_notes_p15_t05_gate_e_disposition.md",
        "research_control/tasks/RT-20260731-010/artifacts/p15_t05_claim_to_evidence_map_v1.yaml",
        "research_control/tasks/RT-20260731-010/artifacts/p15_t05_reproducibility_manifest_v1.yaml",
        "research_control/tasks/RT-20260731-010/jobs/completions/AJC-AJ-RT-20260731-010-001.yaml",
        "research_control/handoffs/handoff-0932.yaml",
        "research_control/handoffs/handoff-0932.md",
    ):
        check((ROOT / rel).is_file() and not (ROOT / rel).is_symlink(), "OUTPUT_MISSING", rel)

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260731-010-001.yaml"
    if completion_path.is_file():
        completion = yaml.safe_load(completion_path.read_text(encoding="utf-8"))
        check(completion.get("objective_result") == "conditionally_not_required_gate_e_not_ready_no_manuscript", "COMPLETION_RESULT_MISMATCH", str(completion.get("objective_result")))
        check(completion.get("work_item_status") == "conditionally_not_required", "WORK_ITEM_STATUS_MISMATCH", str(completion.get("work_item_status")))
        check(completion.get("physics_promotion_authorized") is False, "PROMOTION_FLAG_TRUE", "completion")
        check(completion.get("proof_authority") is False, "PROOF_FLAG_TRUE", "completion")
        check(completion.get("distance_to_gr_delta", {}).get("changed") is False, "DISTANCE_DELTA_TRUE", "completion")
        evidence = completion.get("artifact_evidence", {})
        for key in ("protected_disposition", "claim_map", "reproducibility_manifest", "child_phys_math", "child_phys_phil"):
            item = evidence.get(key, {})
            rel = item.get("path", "")
            recorded = item.get("sha256", "")
            check(bool(rel and recorded), "COMPLETION_EVIDENCE_MISSING", key)
            if rel and (ROOT / rel).is_file():
                check(sha(ROOT / rel) == recorded, "COMPLETION_EVIDENCE_HASH_MISMATCH", key)

    handoff_md = ROOT / "research_control/handoffs/handoff-0932.md"
    if handoff_md.is_file():
        text = handoff_md.read_text(encoding="utf-8")
        check("handoff-0932" in text, "HANDOFF_MARKDOWN_IDENTITY_MISMATCH", "handoff-0932 literal missing")

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"], cwd=ROOT, check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8", errors="replace").split("\0")
    changed = [entry[3:] for entry in status if len(entry) >= 4]
    forbidden_changed = [
        path for path in changed
        if path.startswith("manuscripts/") or path.startswith("markdown/publication-briefs/")
    ]
    check(not forbidden_changed, "FORBIDDEN_MANUSCRIPT_OR_PUBLICATION_PATH_CHANGED", ",".join(forbidden_changed))

    result = {
        "schema_id": "p15_t05_gate_e_no_manuscript_validation_v1",
        "status": "PASS" if not findings else "FAIL",
        "task_id": "RT-20260731-010",
        "job_id": "AJ-RT-20260731-010-001",
        "plan_task_id": "P15-T05",
        "disposition": "CONDITIONALLY_NOT_REQUIRED_GATE_E_NOT_READY_NO_MANUSCRIPT",
        "source_hash_check_count": len(EXPECTED_HASHES),
        "finding_count": len(findings),
        "findings": findings,
        "manuscript_artifact_count": 0,
        "publication_or_push_performed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
