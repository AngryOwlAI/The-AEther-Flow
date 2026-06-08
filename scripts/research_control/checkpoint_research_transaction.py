#!/usr/bin/env python3
"""Synchronize, validate, stage, and commit one research-control transaction."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from strict_yaml import StrictYamlError, load as load_yaml
except ImportError:  # pragma: no cover
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = REPO_ROOT / "registries"
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"
GLOBAL_SYNC_ALLOWLIST = {
    "registries/FILE_OBJECT_REGISTRY.csv",
    "registries/FILE_OBJECT_REGISTRY.meta.json",
    "registries/WIKI_ARTIFACT_REGISTRY.csv",
    "registries/WIKI_ARTIFACT_REGISTRY.meta.json",
    "registries/CONTENT_SEMANTIC_REGISTRY.csv",
    "registries/CONTENT_SEMANTIC_REGISTRY.meta.json",
    "registries/OBJECT_RELATIONSHIP_REGISTRY.csv",
    "registries/OBJECT_RELATIONSHIP_REGISTRY.meta.json",
    "registries/OBSIDIAN_VAULT_REGISTRY.csv",
    "registries/OBSIDIAN_VAULT_REGISTRY.meta.json",
    "wiki/indexes/**",
}


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    def as_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def run_command(command: list[str]) -> CommandResult:
    process = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CommandResult(command, process.returncode, process.stdout, process.stderr)


def read_csv_registry(name: str) -> list[dict[str, str]]:
    path = REGISTRY_DIR / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def by_id(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def git_status_paths() -> dict[str, str]:
    result = run_command(["git", "status", "--porcelain"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    paths: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths[path] = status
    return paths


def path_matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def allowed_by_any(path: str, patterns: Iterable[str]) -> bool:
    if path.startswith(".local/"):
        return True
    return any(path_matches(path, pattern) for pattern in patterns)


def load_job_contract(job_row: dict[str, str]) -> dict[str, object]:
    job_path = REPO_ROOT / job_row["job_path"]
    if not job_path.exists():
        raise RuntimeError(f"missing AgentJob {job_row['job_path']}")
    try:
        return load_yaml(job_path)
    except StrictYamlError as exc:
        raise RuntimeError(f"{job_row['job_path']}: {exc}") from exc


def select_job(job_id: str | None) -> dict[str, str]:
    jobs = by_id(read_csv_registry("AGENT_JOB_REGISTRY.csv"), "job_id")
    if job_id:
        if job_id not in jobs:
            raise RuntimeError(f"unknown AgentJob: {job_id}")
        return jobs[job_id]
    try:
        state = load_yaml(PROGRAM_STATE_PATH)
    except StrictYamlError as exc:
        raise RuntimeError(f"program_state parse failed: {exc}") from exc
    active_task_id = str(state.get("active_task_id", ""))
    tasks = by_id(read_csv_registry("RESEARCH_TASK_REGISTRY.csv"), "task_id")
    task = tasks.get(active_task_id, {})
    current_job_id = task.get("current_job_id", "")
    if current_job_id in jobs:
        return jobs[current_job_id]
    candidates = [row for row in jobs.values() if row.get("status") in {"active", "completed"}]
    if not candidates:
        raise RuntimeError("no active or completed AgentJob is available for checkpointing")
    return sorted(
        candidates,
        key=lambda row: row.get("completed_at") or row.get("started_at") or row.get("created_at"),
    )[-1]


def execution_role_ref_for_job(job_id: str, job_contract: dict[str, object]) -> str:
    contract_ref = str(job_contract.get("execution_role_ref", ""))
    if contract_ref:
        return contract_ref
    rows = [
        row
        for row in read_csv_registry("ROLE_EXECUTION_REGISTRY.csv")
        if row.get("agent_job_id") == job_id
    ]
    return rows[0]["execution_role_ref"] if rows else ""


def allowed_patterns(job_row: dict[str, str], job_contract: dict[str, object]) -> list[str]:
    allowed = []
    allowed.extend(split_semicolon(job_row.get("allowed_write_paths", "")))
    allowed.extend(split_semicolon(job_row.get("output_paths", "")))
    generated = job_contract.get("allowed_generated_paths", [])
    if isinstance(generated, list):
        allowed.extend(str(item) for item in generated if str(item))
    allowed.extend(sorted(GLOBAL_SYNC_ALLOWLIST))
    return sorted(set(allowed))


def changed_registered_tex_requiring_pdf(changed_paths: Iterable[str]) -> list[str]:
    changed = set(changed_paths)
    rows = read_csv_registry("TEX_SOURCE_REGISTRY.csv")
    targets = [
        row["path"]
        for row in rows
        if row.get("path") in changed and row.get("pdf_required") == "true"
    ]
    return sorted(targets)


def handoff_for_job(job_id: str) -> dict[str, str]:
    handoff_dir = REPO_ROOT / "research_control" / "handoffs"
    matches: list[tuple[str, dict[str, str]]] = []
    for path in handoff_dir.glob("handoff-*.yaml"):
        try:
            data = load_yaml(path)
        except StrictYamlError:
            continue
        if data.get("job_id") == job_id:
            matches.append((path.name, {key: str(value) for key, value in data.items()}))
    return sorted(matches)[-1][1] if matches else {}


def commit_message(job_row: dict[str, str], execution_role_ref: str, handoff: dict[str, str]) -> list[str]:
    subject = f"Research control: {job_row['task_id']} {execution_role_ref} completion"
    body = [
        f"Decision: {job_row['decision_id']}",
        f"AgentJob: {job_row['job_id']}",
        f"Handoff: {handoff.get('handoff_id', '')}",
        f"Summary: {handoff.get('summary', job_row.get('notes', ''))}",
        "Validation: memory bootstrap PASS; research-control PASS; diff allowlist PASS",
        "Push: not performed",
    ]
    return [subject, *body]


def block_report(
    reason: str,
    job_row: dict[str, str],
    changed_paths: Iterable[str],
    command_results: list[CommandResult],
    validation_errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "status": "blocked",
        "reason": reason,
        "active_task": job_row.get("task_id", ""),
        "active_agent_job": job_row.get("job_id", ""),
        "changed_paths": sorted(changed_paths),
        "failed_commands": [result.as_dict() for result in command_results if result.returncode != 0],
        "validation_errors": validation_errors or [],
        "suggested_repair_role": "process-integrity-auditor",
        "staged": False,
        "committed": False,
    }


def checkpoint(job_id: str | None = None, *, no_commit: bool = False) -> dict[str, object]:
    job_row = select_job(job_id)
    job_contract = load_job_contract(job_row)
    execution_ref = execution_role_ref_for_job(job_row["job_id"], job_contract)
    allowed = allowed_patterns(job_row, job_contract)

    preflight = git_status_paths()
    disallowed_preexisting = [
        path for path in preflight if not allowed_by_any(path, allowed)
    ]
    if disallowed_preexisting:
        return block_report(
            "preexisting changes outside the AgentJob or sync allowlist",
            job_row,
            preflight,
            [],
            disallowed_preexisting,
        )

    commands: list[CommandResult] = []
    bootstrap = run_command([
        ".venv/bin/python",
        ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
    ])
    commands.append(bootstrap)
    if bootstrap.returncode != 0:
        return block_report("memory bootstrap failed", job_row, git_status_paths(), commands)

    after_bootstrap = git_status_paths()
    tex_targets = changed_registered_tex_requiring_pdf(after_bootstrap)
    if tex_targets:
        pdf_build = run_command([
            ".venv/bin/python",
            ".codex/skills/project-memory-system/scripts/build_pdf_derivatives.py",
            *tex_targets,
        ])
        commands.append(pdf_build)
        if pdf_build.returncode != 0:
            return block_report("targeted PDF build failed", job_row, git_status_paths(), commands)
        bootstrap_after_pdf = run_command([
            ".venv/bin/python",
            ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
        ])
        commands.append(bootstrap_after_pdf)
        if bootstrap_after_pdf.returncode != 0:
            return block_report("post-PDF memory bootstrap failed", job_row, git_status_paths(), commands)

    validation_commands = [
        [
            ".venv/bin/python",
            ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
            "--validate-only",
        ],
        [".venv/bin/python", "scripts/research_control/validate_research_control.py"],
        [
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
        ],
    ]
    for command in validation_commands:
        result = run_command(command)
        commands.append(result)
        if result.returncode != 0:
            return block_report("post-execution validation failed", job_row, git_status_paths(), commands)

    final_changes = git_status_paths()
    disallowed_final = [
        path for path in final_changes if not allowed_by_any(path, allowed)
    ]
    if disallowed_final:
        return block_report(
            "post-sync changes outside the AgentJob or sync allowlist",
            job_row,
            final_changes,
            commands,
            disallowed_final,
        )
    if not final_changes:
        return {
            "status": "no_action",
            "reason": "no tracked or untracked transaction changes to commit",
            "active_task": job_row.get("task_id", ""),
            "active_agent_job": job_row.get("job_id", ""),
            "changed_paths": [],
            "staged": False,
            "committed": False,
        }

    paths_to_stage = sorted(final_changes)
    add_result = run_command(["git", "add", "--", *paths_to_stage])
    commands.append(add_result)
    if add_result.returncode != 0:
        return block_report("git add failed", job_row, final_changes, commands)

    staged_check = run_command([
        ".venv/bin/python",
        "scripts/research_control/validate_research_control.py",
        "--check-diff",
        "--staged-only",
    ])
    commands.append(staged_check)
    if staged_check.returncode != 0:
        run_command(["git", "restore", "--staged", "--", *paths_to_stage])
        return block_report("staged diff allowlist validation failed", job_row, final_changes, commands)

    if no_commit:
        return {
            "status": "ready_to_commit",
            "active_task": job_row.get("task_id", ""),
            "active_agent_job": job_row.get("job_id", ""),
            "execution_role_ref": execution_ref,
            "changed_paths": paths_to_stage,
            "staged": True,
            "committed": False,
            "command_results": [result.as_dict() for result in commands],
        }

    message = commit_message(job_row, execution_ref, handoff_for_job(job_row["job_id"]))
    commit_command = ["git", "commit", "-m", message[0]]
    for line in message[1:]:
        commit_command.extend(["-m", line])
    commit_result = run_command(commit_command)
    commands.append(commit_result)
    if commit_result.returncode != 0:
        return block_report("git commit failed", job_row, final_changes, commands)
    rev_parse = run_command(["git", "rev-parse", "HEAD"])
    commands.append(rev_parse)
    return {
        "status": "committed",
        "active_task": job_row.get("task_id", ""),
        "active_agent_job": job_row.get("job_id", ""),
        "execution_role_ref": execution_ref,
        "changed_paths": paths_to_stage,
        "commit_hash": rev_parse.stdout.strip() if rev_parse.returncode == 0 else "",
        "push": "not performed",
        "staged": True,
        "committed": True,
        "command_results": [result.as_dict() for result in commands],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-id", help="Checkpoint a specific AgentJob.")
    parser.add_argument("--no-commit", action="store_true", help="Stage validated changes but do not commit.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = checkpoint(args.job_id, no_commit=args.no_commit)
    except RuntimeError as exc:
        result = {
            "status": "blocked",
            "reason": str(exc),
            "staged": False,
            "committed": False,
        }
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"committed", "no_action", "ready_to_commit"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
