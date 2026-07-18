#!/usr/bin/env python3
"""Validate the bounded P11-T04 hosted-CI authority evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ARTIFACT_DIR.parents[3]
EVIDENCE_PATH = ARTIFACT_DIR / "planner_hosted_ci_authority_evidence.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    repository = evidence["repository"]
    hosted_ci = evidence["hosted_ci"]
    authority = evidence["authority"]
    decision = evidence["decision"]
    source_hashes = evidence["source_hashes"]
    errors: list[str] = []

    checkpoint = repository["local_checkpoint_sha"]
    branch = repository["branch"]
    if run("git", "cat-file", "-e", f"{checkpoint}^{{commit}}").returncode != 0:
        errors.append("recorded checkpoint is not a local commit")
    current_branch = run("git", "branch", "--show-current")
    if current_branch.returncode != 0 or current_branch.stdout.strip() != branch:
        errors.append("current branch differs from recorded branch")

    remote = run("git", "ls-remote", "--heads", "origin", branch)
    if remote.returncode != 0:
        errors.append("origin branch query failed")
    elif remote.stdout.strip():
        errors.append("recorded absent origin branch now exists")
    if repository["origin_branch_exists"] is not False:
        errors.append("evidence must record absent origin branch")

    runs = run(
        "gh",
        "run",
        "list",
        "--commit",
        checkpoint,
        "--json",
        "databaseId,headSha,headBranch,event,status,conclusion,workflowName,url",
        "--limit",
        "100",
    )
    if runs.returncode != 0:
        errors.append("GitHub Actions query failed")
    else:
        live_runs = json.loads(runs.stdout or "[]")
        if live_runs:
            errors.append("recorded checkpoint now has hosted-CI runs")
    if hosted_ci["github_actions_runs"] != []:
        errors.append("evidence must retain the empty hosted-run result")

    manifest_path = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("migration_epoch") != "shadow_planner":
        errors.append("live migration epoch is not shadow_planner")
    if manifest.get("execution_authority") != "legacy":
        errors.append("live execution authority is not legacy")

    expected_hashes = {
        "implementation_plan_sha256": REPO_ROOT
        / "implementations_plans/recommendations_implementation_plan_continue_task-v19.md",
        "migration_policy_sha256": REPO_ROOT
        / "research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md",
        "live_manifest_sha256": manifest_path,
        "adapter_bindings_sha256": REPO_ROOT
        / "research_control/design/validation_adapter_bindings_v1.json",
        "project_control_workflow_sha256": REPO_ROOT
        / ".github/workflows/project-control-validation.yml",
        "scheduled_full_workflow_sha256": REPO_ROOT
        / ".github/workflows/scheduled-full-validation.yml",
        "predecessor_completion_sha256": REPO_ROOT
        / "research_control/tasks/RT-20260718-007/jobs/completions/AJC-AJ-RT-20260718-007-001.yaml",
    }
    for key, path in expected_hashes.items():
        if source_hashes.get(key) != sha256(path):
            errors.append(f"source hash mismatch: {key}")

    if authority["push_authority_present_in_invocation"] is not False:
        errors.append("push authority must remain absent")
    if any(
        authority[key]
        for key in (
            "push_performed",
            "hosted_workflow_dispatch_performed",
            "branch_protection_mutated",
            "live_defaults_mutated",
            "scientific_claims_changed",
            "physics_promotion_authorized",
            "proof_authority",
        )
    ):
        errors.append("a forbidden authority or mutation is recorded")
    if decision["status"] != "BLOCKED_EXTERNAL_PUBLICATION_AUTHORITY":
        errors.append("decision is not the bounded blocked state")
    if any(
        decision[key]
        for key in (
            "cutover_authorized",
            "p11_t04_completed",
            "p11_t05_dependency_ready",
        )
    ):
        errors.append("cutover or downstream readiness is overstated")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": evidence["task_id"],
        "checkpoint": checkpoint,
        "origin_branch_exists": bool(remote.stdout.strip()) if remote.returncode == 0 else None,
        "hosted_run_count": len(json.loads(runs.stdout or "[]"))
        if runs.returncode == 0
        else None,
        "live_migration_epoch": manifest.get("migration_epoch"),
        "live_execution_authority": manifest.get("execution_authority"),
        "decision": decision["status"],
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
