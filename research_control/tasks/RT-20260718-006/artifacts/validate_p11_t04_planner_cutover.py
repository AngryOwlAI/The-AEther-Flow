#!/usr/bin/env python3
"""Build the bounded P11-T04 planner-cutover evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-006"
ARTIFACTS = TASK / "artifacts"
LOCAL = ROOT / ".local/v19_p11_t04"
EVIDENCE_PATH = ARTIFACTS / "planner_cutover_evidence.json"
RECEIPT_PATH = ARTIFACTS / "planner_cutover_validation_receipt.json"
DECISION_PATH = ARTIFACTS / "planner_cutover_decision.md"

MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
POLICY_PATH = ROOT / "research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md"
BUDGET_PATH = ROOT / "research_control/design/v19_validation_performance_and_safety_budget.md"
P2_AUDIT_PATH = ROOT / "research_control/tasks/RT-20260715-006/artifacts/v19_first_wave_equivalence_audit.json"
P11_T02_PATH = ROOT / "research_control/tasks/RT-20260718-004/artifacts/ci_shadow_run_report.json"
PROJECT_WORKFLOW = ROOT / ".github/workflows/project-control-validation.yml"
SCHEDULED_WORKFLOW = ROOT / ".github/workflows/scheduled-full-validation.yml"
RUNNER_PATH = ROOT / "scripts/validation/run.py"
CHECKPOINT_PATH = ROOT / "scripts/research_control/checkpoint_research_transaction.py"

AUTHORIZED_TRANSACTION_PATHS = {
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def run(label: str, command: list[str], timeout: int = 1800) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    process = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    duration = time.monotonic() - started
    stdout = process.stdout or ""
    stderr = process.stderr or ""
    stdout_path = LOCAL / f"{label}.stdout.log"
    stderr_path = LOCAL / f"{label}.stderr.log"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    receipt = {
        "label": label,
        "command": command,
        "returncode": process.returncode,
        "status": "PASS" if process.returncode == 0 else "FAIL",
        "duration_seconds": round(duration, 6),
        "stdout": {
            "path": stdout_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stdout_path),
            "bytes": stdout_path.stat().st_size,
        },
        "stderr": {
            "path": stderr_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stderr_path),
            "bytes": stderr_path.stat().st_size,
        },
    }
    raw_path = LOCAL / f"{label}.receipt.json"
    raw_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt["receipt_path"] = raw_path.relative_to(ROOT).as_posix()
    receipt["receipt_sha256"] = sha256(raw_path)
    return receipt


def command_stdout(receipt: dict[str, Any]) -> str:
    return (ROOT / str(receipt["stdout"]["path"])).read_text(encoding="utf-8")


def status_paths() -> tuple[list[str], list[str]]:
    output = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout
    paths: list[str] = []
    unexpected: list[str] = []
    for line in output.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
        if not (
            path in AUTHORIZED_TRANSACTION_PATHS
            or path.startswith("research_control/tasks/RT-20260718-006/")
        ):
            unexpected.append(path)
    return sorted(paths), sorted(unexpected)


def write_outputs(evidence: dict[str, Any], receipt: dict[str, Any]) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt["evidence_path"] = EVIDENCE_PATH.relative_to(ROOT).as_posix()
    receipt["evidence_sha256"] = sha256(EVIDENCE_PATH)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    blockers = evidence["cutover_decision"]["blocking_findings"]
    safeguards = evidence["cutover_decision"]["safety_failures"]
    decision = evidence["cutover_decision"]["verdict"]
    lines = [
        "# P11-T04 planner cutover decision",
        "",
        f"Decision: `{decision}`.",
        "",
        "## Result",
        "",
        evidence["cutover_decision"]["summary"],
        "",
        "## Blocking findings",
        "",
    ]
    lines.extend(f"- `{item}`" for item in blockers)
    if not blockers:
        lines.append("- None.")
    lines.extend(["", "## Safety failures", ""])
    lines.extend(f"- `{item}`" for item in safeguards)
    if not safeguards:
        lines.append("- None observed in the bounded local audit.")
    lines.extend(
        [
            "",
            "## Authority boundary",
            "",
            "Legacy validation remains authoritative unless every cutover criterion is directly proven. This operational decision does not change ordinary research, scientific claims, proof authority, benchmark status, ontology, or Distance-to-GR status.",
            "",
            "## Next route",
            "",
            evidence["cutover_decision"]["next_route"],
            "",
        ]
    )
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()

    focused = run(
        "focused-equivalence",
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_validation_equivalence",
            "tests.test_checkpoint_validation_planner",
            "tests.test_validation_profiles",
            "tests.test_validation_precheck",
            "tests.test_staged_validation",
            "tests.test_ci_validation_plan",
        ],
    )
    full_wrapper = run(
        "legacy-full-wrapper",
        [
            sys.executable,
            "scripts/research_control/run_full_research_control_validation.py",
            "--output",
            ".local/v19_p11_t04/legacy-full-report.json",
            "--json",
        ],
    )
    full_plan = run(
        "full-plan",
        [
            sys.executable,
            "-m",
            "scripts.validation.cli",
            "plan",
            "--profile",
            "full",
            "--scope",
            "repository",
            "--paths",
            "--json",
        ],
    )
    current_head_ci = run(
        "current-head-ci",
        [
            "gh",
            "run",
            "list",
            "--commit",
            head,
            "--limit",
            "20",
            "--json",
            "databaseId,workflowName,status,conclusion,headSha,url",
        ],
        timeout=120,
    )

    p2_audit = load_json(P2_AUDIT_PATH)
    p11_t02 = load_json(P11_T02_PATH)
    manifest = load_json(MANIFEST_PATH)
    plan = json.loads(command_stdout(full_plan)) if full_plan["status"] == "PASS" else {}
    head_ci_runs = json.loads(command_stdout(current_head_ci)) if current_head_ci["status"] == "PASS" else []
    if not isinstance(head_ci_runs, list):
        head_ci_runs = []
    project_workflow = PROJECT_WORKFLOW.read_text(encoding="utf-8")
    scheduled_workflow = SCHEDULED_WORKFLOW.read_text(encoding="utf-8")
    runner = RUNNER_PATH.read_text(encoding="utf-8")
    checkpoint = CHECKPOINT_PATH.read_text(encoding="utf-8")
    changed_paths, unexpected_paths = status_paths()

    safety_failures: list[str] = []
    if focused["status"] != "PASS":
        safety_failures.append("focused_equivalence_or_checkpoint_shadow_failed")
    if full_wrapper["status"] != "PASS":
        safety_failures.append("legacy_full_validation_failed")
    if p2_audit.get("status") != "PASS":
        safety_failures.append("first_wave_equivalence_not_pass")
    if p11_t02.get("status") != "PASS":
        safety_failures.append("ci_shadow_topology_not_pass")
    if unexpected_paths:
        safety_failures.append("unexpected_worktree_path")

    blocking_findings: list[str] = []
    if manifest.get("migration_epoch") != "planner_authoritative":
        blocking_findings.append("tracked_manifest_epoch_remains_shadow_planner")
    if manifest.get("execution_authority") != "manifest_planner":
        blocking_findings.append("tracked_manifest_execution_authority_remains_legacy")
    if plan.get("planner_executes_commands") is not True:
        blocking_findings.append("full_profile_plan_is_selection_only")
    if "shadow executor requires legacy execution authority" in runner:
        blocking_findings.append("standalone_executor_rejects_planner_authority")
    if "--adapter-commands" in runner:
        blocking_findings.append("no_tracked_default_adapter_binding_for_full_planner_execution")
    if not head_ci_runs:
        blocking_findings.append("no_official_ci_shadow_run_for_current_head")
    if "continue-on-error: true" in project_workflow:
        blocking_findings.append("ci_shadow_shards_remain_non_authoritative")
    if "validation_shards_shadow" in project_workflow:
        blocking_findings.append("ci_default_still_names_shadow_execution")
    if (
        'parser.set_defaults(validation_mode="compare")' not in checkpoint
        or "--legacy-validation" not in checkpoint
    ):
        safety_failures.append("checkpoint_compare_or_legacy_fallback_missing")
    if "schedule:" not in scheduled_workflow or "--profile full" not in scheduled_workflow:
        safety_failures.append("scheduled_full_workflow_missing_or_filtered")
    if full_wrapper["status"] == "PASS" and plan.get("planner_executes_commands") is not True:
        blocking_findings.append("matched_authoritative_planner_full_receipt_absent")

    if safety_failures:
        verdict = "ROLLBACK_REQUIRED"
        summary = "The bounded audit observed a non-negotiable safety or legacy-acceptance failure, so cutover is blocked and the last authoritative legacy path must be retained."
        next_route = "Create one separately bounded P11-T04 rollback or safety-repair packet for the named failure; do not route to P11-T05."
    elif blocking_findings:
        verdict = "REPAIR_REQUIRED"
        summary = "Local equivalence and rollback checks pass, but planner authority cannot be cut over because required execution and current-head hosted-CI evidence is absent while tracked defaults still preserve shadow-planner legacy authority."
        next_route = "Create one separately bounded P11-T04 Validator Engineer repair that implements an explicit planner-authoritative execution binding and obtains matched current-head local checkpoint full and hosted-CI receipts while retaining the tested legacy fallback; do not execute P11-T05 yet."
    else:
        verdict = "CUTOVER_AUTHORIZED"
        summary = "Every bounded cutover criterion is directly proven with no safety mismatch and the tracked authoritative execution surfaces are active with legacy fallback retained."
        next_route = "After governed checkpoint PASS route one separately bounded P11-T05 compatibility-retirement packet."

    evidence = {
        "schema_id": "v19_p11_t04_planner_cutover_evidence_v1",
        "task_id": "RT-20260718-006",
        "job_id": "AJ-RT-20260718-006-001",
        "plan_task_id": "P11-T04",
        "repository": {
            "root": ROOT.as_posix(),
            "branch": branch,
            "head": head,
            "changed_paths": changed_paths,
            "unexpected_paths": unexpected_paths,
        },
        "canonical_sources": {
            "migration_policy": {"path": POLICY_PATH.relative_to(ROOT).as_posix(), "sha256": sha256(POLICY_PATH)},
            "budget_policy": {"path": BUDGET_PATH.relative_to(ROOT).as_posix(), "sha256": sha256(BUDGET_PATH)},
            "manifest": {"path": MANIFEST_PATH.relative_to(ROOT).as_posix(), "sha256": sha256(MANIFEST_PATH)},
        },
        "prior_evidence": {
            "p2_first_wave": {"path": P2_AUDIT_PATH.relative_to(ROOT).as_posix(), "sha256": sha256(P2_AUDIT_PATH), "status": p2_audit.get("status")},
            "p11_t02_ci_shadow": {"path": P11_T02_PATH.relative_to(ROOT).as_posix(), "sha256": sha256(P11_T02_PATH), "status": p11_t02.get("status")},
        },
        "current_execution_state": {
            "manifest_migration_epoch": manifest.get("migration_epoch"),
            "manifest_execution_authority": manifest.get("execution_authority"),
            "full_plan_status": plan.get("status"),
            "full_plan_selected_gate_count": len(plan.get("selected_gate_ids", [])) if isinstance(plan.get("selected_gate_ids"), list) else 0,
            "full_plan_planner_executes_commands": plan.get("planner_executes_commands"),
            "checkpoint_default_compare": 'parser.set_defaults(validation_mode="compare")' in checkpoint,
            "checkpoint_explicit_legacy_fallback": "--legacy-validation" in checkpoint,
            "ci_shadow_continue_on_error": "continue-on-error: true" in project_workflow,
            "scheduled_full_present": "schedule:" in scheduled_workflow and "--profile full" in scheduled_workflow,
            "official_current_head_run_count": len(head_ci_runs),
            "official_current_head_runs": head_ci_runs,
        },
        "command_receipts": {
            "focused_equivalence": focused,
            "legacy_full_wrapper": full_wrapper,
            "full_plan": full_plan,
            "current_head_ci": current_head_ci,
        },
        "cutover_decision": {
            "verdict": verdict,
            "summary": summary,
            "safety_failures": safety_failures,
            "blocking_findings": blocking_findings,
            "performance_hard_guards_activated": False,
            "cache_mode": "off",
            "output_mode": "legacy",
            "legacy_fallback": "enabled",
            "planner_authority_changed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "next_route": next_route,
        },
    }
    receipt = {
        "schema_id": "v19_p11_t04_planner_cutover_validation_receipt_v1",
        "task_id": "RT-20260718-006",
        "job_id": "AJ-RT-20260718-006-001",
        "status": "PASS",
        "decision": verdict,
        "safety_failure_count": len(safety_failures),
        "blocking_finding_count": len(blocking_findings),
        "required_output_count": 3,
        "authority": {
            "operational_validation_only": True,
            "planner_authority_changed": False,
            "legacy_fallback_retained": True,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }

    if args.write_report:
        write_outputs(evidence, receipt)
    summary = {
        "status": receipt["status"],
        "decision": verdict,
        "safety_failure_count": len(safety_failures),
        "blocking_finding_count": len(blocking_findings),
        "evidence_path": EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "receipt_path": RECEIPT_PATH.relative_to(ROOT).as_posix(),
    }
    print(json.dumps(summary, sort_keys=True) if args.json else summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
