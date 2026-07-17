#!/usr/bin/env python3
"""Synchronize, validate, stage, and commit one research-control transaction."""

from __future__ import annotations

import argparse
import copy
import csv
import fnmatch
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

try:
    from strict_yaml import StrictYamlError, load as load_yaml
except ImportError:  # pragma: no cover
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
REGISTRY_DIR = REPO_ROOT / "registries"
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"
VALIDATION_MANIFEST_PATH = (
    REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
)
MEMORY_BOOTSTRAP_PATH = (
    REPO_ROOT
    / ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"
)
PROJECT_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
if str(PROJECT_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_CONTROL_SCRIPT_DIR))

from project_improvement_handoff_validation import conditional_checkpoint_sidecar_paths  # noqa: E402
from run_full_research_control_validation import claim_language_summary  # noqa: E402
from classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.executor import (  # noqa: E402
    AdapterResult,
    ExecutionContext,
    execute_plan,
)
from scripts.validation.plan import build_plan, load_manifest  # noqa: E402
from scripts.validation.precheck import run_precheck  # noqa: E402
from scripts.validation.profiles import resolve_profile  # noqa: E402
from scripts.validation.staged import (  # noqa: E402
    GateOutcome,
    StagedExecutionContext,
    run_staged_acceptance,
)

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
MAX_STAGED_SYNC_PASSES = 3
CLAIM_SUPERSEDENCE_PREDICATE_ID = "rc_diff_satisfies_claim_language_same_scope_v1"
CLAIM_LANGUAGE_SCRIPT = "scripts/project_control/validate_claim_language.py"
CHECKPOINT_VALIDATION_MODES = {"legacy", "compare"}
SUPPORTED_TRACKED_GENERATORS = {"memory_sync", "targeted_pdf_build"}


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float = 0.0

    def as_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": self.duration_seconds,
            "output_bytes": len(self.stdout.encode("utf-8"))
            + len(self.stderr.encode("utf-8")),
        }


@dataclass(frozen=True)
class CheckpointValidationPlan:
    manifest: dict[str, object]
    classification: dict[str, object]
    selected_gate_ids: tuple[str, ...]
    generator_gate_ids: tuple[str, ...]
    local_only_gate_ids: tuple[str, ...]
    orchestrator_gate_ids: tuple[str, ...]

    def receipt(self) -> dict[str, object]:
        return {
            "selected_gate_ids": list(self.selected_gate_ids),
            "tracked_generator_gate_ids": list(self.generator_gate_ids),
            "local_only_gate_ids": list(self.local_only_gate_ids),
            "orchestrator_gate_ids": list(self.orchestrator_gate_ids),
        }


@dataclass
class CheckpointCommandAdapter:
    gate_id: str
    command: tuple[str, ...]
    command_results: list[CommandResult]
    legacy_statuses: dict[str, str]

    def run(self, context: ExecutionContext) -> AdapterResult:
        result = run_command(list(self.command))
        self.command_results.append(result)
        self.legacy_statuses[self.gate_id] = (
            "PASS" if result.returncode == 0 else "FAIL"
        )
        context.stdout_path.write_text(result.stdout, encoding="utf-8")
        context.stderr_path.write_text(result.stderr, encoding="utf-8")
        return AdapterResult(exit_code=result.returncode)


def run_command(command: list[str]) -> CommandResult:
    started = time.perf_counter()
    process = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CommandResult(
        command,
        process.returncode,
        process.stdout,
        process.stderr,
        time.perf_counter() - started,
    )


@lru_cache(maxsize=1)
def _load_memory_sync():
    """Load the write-only memory synchronizer without changing CLI semantics."""

    module_name = "checkpoint_memory_bootstrap"
    script_dir = str(MEMORY_BOOTSTRAP_PATH.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(module_name, MEMORY_BOOTSTRAP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {MEMORY_BOOTSTRAP_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.memory_sync


def memory_sync(*, rebuilt_pdf_paths: Iterable[str] | None = None) -> CommandResult:
    """Run one tracked-state synchronization pass without validation."""

    command = ["memory_sync()"]
    rebuilt = sorted(set(rebuilt_pdf_paths or []))
    if rebuilt:
        command.extend(["rebuilt_pdf_paths", *rebuilt])
    started = time.perf_counter()
    try:
        receipt = _load_memory_sync()(
            rebuilt_pdf_paths=rebuilt,
            include_local_retrieval=False,
        )
        mutation = receipt.to_dict()
        payload = {
            "gate_id": "memory_sync",
            "operation": "write_only_tracked_state",
            "mutated": mutation["mutated"],
            "counts": mutation["counts"],
            "changed": mutation["changed"],
            "created": mutation["created"],
            "pruned": mutation["pruned"],
            "local_retrieval_enabled": mutation["local_retrieval_enabled"],
        }
        return CommandResult(
            command,
            0,
            json.dumps(payload, sort_keys=True),
            "",
            time.perf_counter() - started,
        )
    except Exception as exc:
        return CommandResult(
            command,
            1,
            "",
            f"{type(exc).__name__}: {exc}",
            time.perf_counter() - started,
        )


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
            source_path, destination_path = path.split(" -> ", 1)
            paths[source_path] = status
            paths[destination_path] = status
        else:
            paths[path] = status
    return paths


def checkpoint_planning_paths(statuses: Mapping[str, str]) -> tuple[str, ...]:
    """Expand Git's collapsed untracked directories for path-level planning."""

    paths: set[str] = set()
    for path in statuses:
        if not path.endswith("/"):
            paths.add(path)
            continue
        result = run_command(
            ["git", "ls-files", "--others", "--exclude-standard", "--", path]
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or f"could not expand {path}")
        expanded = {value for value in result.stdout.splitlines() if value}
        if not expanded:
            raise RuntimeError(f"Git reported an empty untracked directory: {path}")
        paths.update(expanded)
    return tuple(sorted(paths))


def path_matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def allowed_by_any(path: str, patterns: Iterable[str]) -> bool:
    if path.startswith(".local/"):
        return True
    return any(path_matches(path, pattern) for pattern in patterns)


def tracked_local_paths(paths: Iterable[str]) -> set[str]:
    local_paths = sorted({path for path in paths if path.startswith(".local/")})
    if not local_paths:
        return set()
    result = run_command(["git", "ls-files", "--", *local_paths])
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def stageable_paths(paths: Iterable[str], tracked_local: set[str] | None = None) -> list[str]:
    unique_paths = sorted(set(paths))
    if tracked_local is None:
        tracked_local = tracked_local_paths(unique_paths)
    return [
        path
        for path in unique_paths
        if not path.startswith(".local/") or path in tracked_local
    ]


def add_stageable_paths(paths: Iterable[str]) -> list[CommandResult]:
    unique_paths = sorted(set(paths))
    normal_paths = [path for path in unique_paths if not path.startswith(".local/")]
    local_paths = [path for path in unique_paths if path.startswith(".local/")]
    results: list[CommandResult] = []
    if normal_paths:
        results.append(run_command(["git", "add", "--", *normal_paths]))
    if local_paths:
        # Git ignored-directory rules can reject tracked files under .local/
        # without -f. stageable_paths already limits this set to tracked paths.
        results.append(run_command(["git", "add", "-f", "--", *local_paths]))
    return results


def git_index_paths() -> set[str]:
    result = run_command(["git", "ls-files", "-z"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "git ls-files failed")
    return {path for path in result.stdout.split("\0") if path}


def unstaged_stageable_paths(statuses: dict[str, str]) -> list[str]:
    candidates = [
        path
        for path, status in statuses.items()
        if status == "??" or len(status) < 2 or status[1] != " "
    ]
    return stageable_paths(candidates)


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


def allowed_patterns_for_changed_paths(
    job_row: dict[str, str],
    job_contract: dict[str, object],
    changed_paths: Iterable[str],
) -> list[str]:
    allowed = allowed_patterns(job_row, job_contract)
    allowed.extend(
        conditional_checkpoint_sidecar_paths(REPO_ROOT, changed_paths, allowed)
    )
    return sorted(set(allowed))


def plan_checkpoint_validation(
    changed_paths: Iterable[str],
) -> CheckpointValidationPlan:
    """Build the shadow checkpoint plan and identify checkpoint-owned generators."""

    paths = tuple(sorted(set(changed_paths)))
    manifest = load_manifest(VALIDATION_MANIFEST_PATH)
    classification = classify_paths(paths, registry_root=REPO_ROOT)
    resolution = resolve_profile(
        manifest,
        classification,
        requested_profile="checkpoint",
        scopes=("staged",),
        shadow=True,
    )
    plan = resolution.plan
    if (
        plan.status != "READY"
        or plan.blocked_paths
        or plan.unknown_paths
        or plan.execution_authority != "legacy"
        or not resolution.comparison_required
    ):
        raise RuntimeError("checkpoint planner did not produce a safe shadow plan")

    gates = {
        str(gate["gate_id"]): gate
        for gate in manifest.get("gates", [])
        if isinstance(gate, dict) and gate.get("gate_id")
    }
    tracked: list[str] = []
    local_only: list[str] = []
    orchestrators: list[str] = []
    for gate_id in plan.ordered_gate_ids:
        gate = gates[gate_id]
        if gate.get("mutating") is not True:
            continue
        if gate_id == "checkpoint_transaction":
            orchestrators.append(gate_id)
            continue
        outputs = [str(value) for value in gate.get("output_globs", [])]
        if outputs and all(value.startswith(".local/") for value in outputs):
            local_only.append(gate_id)
        else:
            tracked.append(gate_id)
    unsupported = sorted(set(tracked) - SUPPORTED_TRACKED_GENERATORS)
    if unsupported:
        raise RuntimeError(
            "checkpoint planner selected unsupported tracked generators: "
            + ", ".join(unsupported)
        )
    return CheckpointValidationPlan(
        manifest=manifest,
        classification=classification,
        selected_gate_ids=tuple(plan.ordered_gate_ids),
        generator_gate_ids=tuple(tracked),
        local_only_gate_ids=tuple(local_only),
        orchestrator_gate_ids=tuple(orchestrators),
    )


def staged_gate_command(gate_id: str) -> list[str]:
    commands = {
        "classify_changes": [
            ".venv/bin/python",
            "scripts/project_control/classify_project_changes.py",
            "--staged",
            "--json",
        ],
        "project_improvement_signals": [
            ".venv/bin/python",
            "scripts/project_control/collect_project_improvement_signals.py",
            "--validate-emitted",
        ],
        "documentation_impact": [
            ".venv/bin/python",
            "scripts/project_control/validate_documentation_impact.py",
            "--staged",
        ],
        "memory_core": final_memory_validation_command(),
        "research_control_diff": [
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
            "--staged-only",
            "--json",
        ],
        "test_shard_repository": [
            ".venv/bin/python",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
        ],
        "claim_language_changed": [
            ".venv/bin/python",
            CLAIM_LANGUAGE_SCRIPT,
            "--staged",
            "--json",
        ],
        "git_diff_check": ["git", "diff", "--cached", "--check"],
    }
    try:
        return list(commands[gate_id])
    except KeyError as exc:
        raise RuntimeError(f"no checkpoint adapter command for gate {gate_id}") from exc


def _project_executor_manifest(
    manifest: Mapping[str, object], gate_ids: Sequence[str]
) -> dict[str, object]:
    """Project canonical planner selections into one executor-valid subplan."""

    selected = set(gate_ids)
    projected = copy.deepcopy(dict(manifest))
    projected_gates: list[dict[str, object]] = []
    for raw_gate in manifest.get("gates", []):
        if not isinstance(raw_gate, dict) or raw_gate.get("gate_id") not in selected:
            continue
        gate = copy.deepcopy(raw_gate)
        gate["prerequisites"] = [
            value for value in gate.get("prerequisites", []) if value in selected
        ]
        gate["supersedes"] = [
            value
            for value in gate.get("supersedes", [])
            if isinstance(value, dict) and value.get("gate_id") in selected
        ]
        gate["selection"] = {
            "operator": "all",
            "conditions": [
                {
                    "condition_id": "checkpoint_selected",
                    "kind": "always",
                    "values": [],
                }
            ],
        }
        projected_gates.append(gate)
    if {str(gate["gate_id"]) for gate in projected_gates} != selected:
        raise RuntimeError("checkpoint executor projection omitted a selected gate")
    projected["gates"] = projected_gates
    return projected


def run_checkpoint_staged_acceptance(
    repo_root: Path,
    *,
    transaction_paths: Iterable[str],
    allowed_path_globs: Iterable[str],
    manifest: Mapping[str, object],
    agent_job_id: str,
    command_results: list[CommandResult],
    classifier: Callable[..., dict[str, object]] = classify_paths,
) -> tuple[dict[str, object], dict[str, object]]:
    """Execute planner-selected staged blockers once and compare legacy statuses."""

    legacy_statuses: dict[str, str] = {}
    child_receipts: list[dict[str, str]] = []

    def gate_executor(
        required: tuple[str, ...], context: StagedExecutionContext
    ) -> Sequence[GateOutcome]:
        projected = _project_executor_manifest(manifest, required)
        classification = classifier(context.staged_paths, registry_root=context.repo_root)
        plan = build_plan(
            projected,
            classification,
            profile="checkpoint",
            scopes=("staged",),
        )
        gates = {
            str(gate["gate_id"]): gate
            for gate in projected["gates"]  # type: ignore[index]
            if isinstance(gate, dict)
        }
        adapters = {
            str(gates[gate_id]["adapter"]): CheckpointCommandAdapter(
                gate_id,
                tuple(staged_gate_command(gate_id)),
                command_results,
                legacy_statuses,
            )
            for gate_id in required
        }
        run_digest = hashlib.sha256(
            f"{context.tree_hash}:{time.time_ns()}".encode("utf-8")
        ).hexdigest()[:16]
        outcome = execute_plan(
            plan,
            projected,
            adapters,
            receipt_root=context.repo_root / ".local/validation-receipts",
            max_workers=1,
            run_id=f"RUN-CHECKPOINT-{run_digest}",
        )
        if outcome.receipt_path is not None:
            receipt_path = outcome.receipt_path
            try:
                relative = receipt_path.relative_to(context.repo_root).as_posix()
            except ValueError:
                relative = str(receipt_path)
            child_receipts.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
                }
            )
        gate_results = outcome.receipt.get("gate_results", [])
        if not isinstance(gate_results, list):
            raise RuntimeError("checkpoint executor receipt omitted gate results")
        outcomes: list[GateOutcome] = []
        for item in gate_results:
            if not isinstance(item, dict):
                raise RuntimeError("checkpoint executor emitted an invalid gate result")
            gate_id = str(item.get("gate_id", ""))
            status = str(item.get("status", ""))
            legacy_statuses.setdefault(gate_id, status)
            outcomes.append(
                GateOutcome(gate_id, status, context.scope, context.tree_hash)
            )
        return outcomes

    receipt = run_staged_acceptance(
        repo_root,
        transaction_paths=transaction_paths,
        allowed_path_globs=allowed_path_globs,
        manifest=manifest,
        classifier=classifier,
        gate_executor=gate_executor,
        legacy_status_provider=lambda required: {
            gate_id: legacy_statuses[gate_id] for gate_id in required
        },
        base_ref="HEAD",
        agent_job_id=agent_job_id,
    )
    execution = receipt.get("execution", {})
    integration = {
        "status": receipt.get("status", "BLOCKED_CONFIGURATION"),
        "tree_hash": receipt.get("tree_hash", ""),
        "required_gate_ids": (
            execution.get("required_gate_ids", [])
            if isinstance(execution, dict)
            else []
        ),
        "gate_results": (
            execution.get("gate_results", []) if isinstance(execution, dict) else []
        ),
        "shadow_comparison": receipt.get("shadow_comparison", {}),
        "checks": receipt.get("checks", {}),
        "index": receipt.get("index", {}),
        "finding": receipt.get("finding", {}),
        "child_receipts": child_receipts,
    }
    return receipt, integration


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
        "Validation: memory sync PASS; final memory core PASS; research-control PASS; diff allowlist PASS",
        "Push: not performed",
    ]
    return [subject, *body]


def block_report(
    reason: str,
    job_row: dict[str, str],
    changed_paths: Iterable[str],
    command_results: list[CommandResult],
    validation_errors: list[str] | None = None,
    suggested_repair_role: str = "process-integrity-auditor",
    planner_integration: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": "blocked",
        "reason": reason,
        "active_task": job_row.get("task_id", ""),
        "active_agent_job": job_row.get("job_id", ""),
        "changed_paths": sorted(changed_paths),
        "failed_commands": [result.as_dict() for result in command_results if result.returncode != 0],
        "validation_errors": validation_errors or [],
        "suggested_repair_role": suggested_repair_role,
        "command_counts": checkpoint_command_counts(command_results),
        "performance": checkpoint_performance(command_results),
        "checkpoint_receipt": checkpoint_receipt(
            command_results,
            planner_integration=planner_integration,
        ),
        "staged": False,
        "committed": False,
    }


def post_sync_validation_commands() -> list[list[str]]:
    return [
        [".venv/bin/python", "scripts/project_control/classify_project_changes.py", "--json"],
        [
            ".venv/bin/python",
            "scripts/project_control/collect_project_improvement_signals.py",
            "--validate-emitted",
        ],
        [".venv/bin/python", "scripts/project_control/validate_documentation_impact.py"],
        [
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
        ],
    ]


def final_memory_validation_command() -> list[str]:
    return [
        ".venv/bin/python",
        ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
        "--validate-only",
    ]


def checkpoint_performance(command_results: Iterable[CommandResult]) -> dict[str, object]:
    results = list(command_results)
    return {
        "duration_seconds": round(sum(result.duration_seconds for result in results), 6),
        "subprocess_count": sum(
            1 for result in results if result.command[:1] != ["memory_sync()"]
        ),
        "output_bytes": sum(
            len(result.stdout.encode("utf-8")) + len(result.stderr.encode("utf-8"))
            for result in results
        ),
        "cache_hits": 0,
        "cache_misses": 0,
        "cache_scope": "not_applicable_tracked_memory_sync",
        "measurement_scope": "recorded_checkpoint_operations",
    }


def checkpoint_receipt(
    command_results: Iterable[CommandResult],
    *,
    final_index_tree: str = "",
    planner_integration: Mapping[str, object] | None = None,
) -> dict[str, object]:
    results = list(command_results)
    sync_results = [
        result for result in results if result.command[:1] == ["memory_sync()"]
    ]
    sync_receipts: list[dict[str, object]] = []
    for result in sync_results:
        try:
            payload = json.loads(result.stdout) if result.stdout else {}
        except json.JSONDecodeError:
            payload = {"raw_stdout": result.stdout}
        sync_receipts.append(
            {
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "command": result.command,
                "receipt": payload,
            }
        )
    final_results = [
        result for result in results if result.command == final_memory_validation_command()
    ]
    final_result = final_results[-1] if final_results else None
    receipt = {
        "generator_gate_id": "memory_sync",
        "generator_passes": len(sync_results),
        "generator_receipts": sync_receipts,
        "compatibility_bootstrap_passes": sum(
            1
            for result in results
            if result.command
            == [
                ".venv/bin/python",
                ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
            ]
        ),
        "final_validator": {
            "gate_id": "memory_legacy_composite",
            "satisfies_obligation": "memory_core",
            "command": final_memory_validation_command(),
            "tree_state": "final_staged",
            "git_index_tree": final_index_tree,
            "status": (
                "PASS"
                if final_result is not None and final_result.returncode == 0
                else "FAIL"
                if final_result is not None
                else "NOT_RUN"
            ),
            "execution_count": len(final_results),
        },
        "no_physics_authority": True,
    }
    if planner_integration is not None:
        receipt["planner_integration"] = dict(planner_integration)
    return receipt


def checkpoint_command_counts(command_results: Iterable[CommandResult]) -> dict[str, object]:
    results = list(command_results)
    commands = [result.command for result in results]
    research_control_commands = [
        command
        for command in commands
        if "scripts/research_control/validate_research_control.py" in command
    ]
    plain_working = [
        command for command in research_control_commands if "--check-diff" not in command
    ]
    diff_working = [
        command
        for command in research_control_commands
        if "--check-diff" in command and "--staged-only" not in command
    ]
    diff_staged = [
        command
        for command in research_control_commands
        if "--check-diff" in command and "--staged-only" in command
    ]
    standalone_claim_commands = [
        command
        for command in commands
        if CLAIM_LANGUAGE_SCRIPT in command
    ]
    integrated_claim_summaries = [
        {
            "tree_state": "staged" if "--staged-only" in result.command else "working",
            **claim_language_summary(result.stdout),
        }
        for result in results
        if "scripts/research_control/validate_research_control.py" in result.command
        and "--check-diff" in result.command
    ]
    sync_commands = [command for command in commands if command[:1] == ["memory_sync()"]]
    memory_core_commands = [
        command for command in commands if command == final_memory_validation_command()
    ]
    compatibility_bootstrap_commands = [
        command
        for command in commands
        if command
        == [
            ".venv/bin/python",
            ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
        ]
    ]
    return {
        "total": len(commands),
        "memory_sync": len(sync_commands),
        "memory_core": len(memory_core_commands),
        "compatibility_bootstrap": len(compatibility_bootstrap_commands),
        "research_control_total": len(research_control_commands),
        "research_control_plain_working": len(plain_working),
        "research_control_diff_working": len(diff_working),
        "research_control_diff_staged": len(diff_staged),
        "working_and_staged_scopes_distinct": bool(diff_working and diff_staged),
        "claim_language_standalone_working": len(
            [command for command in standalone_claim_commands if "--staged" not in command]
        ),
        "claim_language_standalone_staged": len(
            [command for command in standalone_claim_commands if "--staged" in command]
        ),
        "claim_language_obligation_satisfied_by": "research_control_diff",
        "claim_language_supersedence_predicate_id": CLAIM_SUPERSEDENCE_PREDICATE_ID,
        "claim_language_integrated_summaries": integrated_claim_summaries,
    }


def _checkpoint_impl(
    job_id: str | None = None,
    *,
    no_commit: bool = False,
    validation_mode: str = "legacy",
) -> dict[str, object]:
    if validation_mode not in CHECKPOINT_VALIDATION_MODES:
        raise RuntimeError(f"unsupported checkpoint validation mode: {validation_mode}")
    job_row = select_job(job_id)
    job_contract = load_job_contract(job_row)
    execution_ref = execution_role_ref_for_job(job_row["job_id"], job_contract)

    preflight = git_status_paths()
    allowed = allowed_patterns_for_changed_paths(job_row, job_contract, preflight)
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

    planner_plan: CheckpointValidationPlan | None = None
    planner_integration: dict[str, object] | None = None
    if validation_mode == "compare":
        try:
            planning_paths = checkpoint_planning_paths(preflight)
            planner_plan = plan_checkpoint_validation(planning_paths)
            precheck = run_precheck(
                REPO_ROOT,
                planning_paths,
                only_gate="path_policy_sanity",
                manifest=planner_plan.manifest,
            )
        except (OSError, RuntimeError, TypeError, ValueError) as exc:
            return block_report(
                "checkpoint planner preflight failed",
                job_row,
                preflight,
                [],
                [str(exc)],
            )
        planner_integration = {
            "schema_id": "checkpoint_planner_integration_receipt_v1",
            "validation_mode": validation_mode,
            "precheck": {
                "status": precheck.get("status", "BLOCKED_CONFIGURATION"),
                "tree_hash": precheck.get("tree_hash", ""),
                "requested_gate": precheck.get("requested_gate", ""),
                "counts": precheck.get("counts", {}),
                "checkpoint_acceptance": False,
            },
            "generator_selection": planner_plan.receipt(),
            "staged_acceptance": {"status": "NOT_RUN"},
            "fallback_switch": "--legacy-validation",
        }
        if precheck.get("status") != "PASS":
            return block_report(
                "cheap checkpoint preflight found a working-tree blocker",
                job_row,
                preflight,
                [],
                planner_integration=planner_integration,
            )

    commands: list[CommandResult] = []
    index_snapshot = run_command(["git", "write-tree"])
    commands.append(index_snapshot)
    if index_snapshot.returncode != 0 or not index_snapshot.stdout.strip():
        return block_report(
            "could not snapshot the original Git index",
            job_row,
            preflight,
            commands,
            planner_integration=planner_integration,
        )
    original_index_tree = index_snapshot.stdout.strip()
    index_mutated = False

    def restore_original_index() -> CommandResult | None:
        if not index_mutated:
            return None
        restore = run_command(["git", "read-tree", original_index_tree])
        commands.append(restore)
        return restore

    def rollback_block(
        reason: str,
        changed_paths: Iterable[str],
        validation_errors: list[str] | None = None,
        suggested_repair_role: str = "process-integrity-auditor",
    ) -> dict[str, object]:
        errors = list(validation_errors or [])
        restore = restore_original_index()
        if restore is not None and restore.returncode != 0:
            raise RuntimeError(
                restore.stderr or "failed to restore the original Git index"
            )
        return block_report(
            reason,
            job_row,
            changed_paths,
            commands,
            errors,
            suggested_repair_role=suggested_repair_role,
            planner_integration=planner_integration,
        )

    initial_paths = stageable_paths(preflight)
    index_mutated = bool(initial_paths)
    initial_add_results = add_stageable_paths(initial_paths)
    commands.extend(initial_add_results)
    if any(result.returncode != 0 for result in initial_add_results):
        return rollback_block("pre-sync git add failed", preflight)

    sync_passes = 0
    pdf_targets_processed = False
    planned_generators = (
        set(planner_plan.generator_gate_ids) if planner_plan is not None else set()
    )
    for sync_pass in range(1, MAX_STAGED_SYNC_PASSES + 1):
        index_paths_before_sync = git_index_paths()
        run_sync = validation_mode == "legacy" or "memory_sync" in planned_generators
        if run_sync:
            sync_passes = sync_pass
            sync_result = memory_sync()
            commands.append(sync_result)
            if sync_result.returncode != 0:
                return rollback_block("memory synchronization failed", git_status_paths())
        synced_changes = git_status_paths()
        if not pdf_targets_processed:
            tex_targets = changed_registered_tex_requiring_pdf(synced_changes)
            pdf_targets_processed = True
            if tex_targets:
                if (
                    validation_mode == "compare"
                    and "targeted_pdf_build" not in planned_generators
                ):
                    return rollback_block(
                        "checkpoint planner omitted a required targeted PDF generator",
                        synced_changes,
                        tex_targets,
                    )
                pdf_build = run_command([
                    ".venv/bin/python",
                    ".codex/skills/project-memory-system/scripts/build_pdf_derivatives.py",
                    *tex_targets,
                ])
                commands.append(pdf_build)
                if pdf_build.returncode != 0:
                    return rollback_block("targeted PDF build failed", git_status_paths())
                if validation_mode == "compare" and "memory_sync" not in planned_generators:
                    return rollback_block(
                        "checkpoint planner omitted required post-PDF synchronization",
                        git_status_paths(),
                    )
                sync_after_pdf = memory_sync(rebuilt_pdf_paths=tex_targets)
                commands.append(sync_after_pdf)
                if sync_after_pdf.returncode != 0:
                    return rollback_block("post-PDF memory synchronization failed", git_status_paths())
                synced_changes = git_status_paths()

        allowed = allowed_patterns_for_changed_paths(job_row, job_contract, synced_changes)
        disallowed_sync = [
            path for path in synced_changes if not allowed_by_any(path, allowed)
        ]
        if disallowed_sync:
            return rollback_block(
                "synchronized changes outside the AgentJob or sync allowlist",
                synced_changes,
                disallowed_sync,
            )

        synchronized_paths = stageable_paths(synced_changes)
        if synchronized_paths:
            index_mutated = True
        sync_add_results = add_stageable_paths(synchronized_paths)
        commands.extend(sync_add_results)
        if any(result.returncode != 0 for result in sync_add_results):
            return rollback_block("post-sync git add failed", synced_changes)

        if git_index_paths() == index_paths_before_sync:
            break
    else:
        return rollback_block(
            "staged tracked path set did not converge after bounded synchronization",
            git_status_paths(),
        )

    working_commands = (
        post_sync_validation_commands() if validation_mode == "legacy" else []
    )
    for command in working_commands:
        result = run_command(command)
        commands.append(result)
        if result.returncode != 0:
            suggested_role = (
                "documentation-curator"
                if "validate_documentation_impact.py" in command
                else "process-integrity-auditor"
            )
            return rollback_block(
                "post-execution validation failed",
                git_status_paths(),
                suggested_repair_role=suggested_role,
            )

    final_changes = git_status_paths()
    allowed = allowed_patterns_for_changed_paths(job_row, job_contract, final_changes)
    disallowed_final = [
        path for path in final_changes if not allowed_by_any(path, allowed)
    ]
    if disallowed_final:
        return rollback_block(
            "post-sync changes outside the AgentJob or sync allowlist",
            final_changes,
            disallowed_final,
        )
    if not final_changes:
        restore = restore_original_index()
        if restore is not None and restore.returncode != 0:
            raise RuntimeError(
                restore.stderr or "failed to restore the original Git index"
            )
        return {
            "status": "no_action",
            "reason": "no tracked or untracked transaction changes to commit",
            "active_task": job_row.get("task_id", ""),
            "active_agent_job": job_row.get("job_id", ""),
            "changed_paths": [],
            "command_counts": checkpoint_command_counts(commands),
            "performance": checkpoint_performance(commands),
            "checkpoint_receipt": checkpoint_receipt(
                commands,
                planner_integration=planner_integration,
            ),
            "staged": False,
            "committed": False,
        }

    paths_to_stage = stageable_paths(final_changes)
    if not paths_to_stage:
        restore = restore_original_index()
        if restore is not None and restore.returncode != 0:
            raise RuntimeError(
                restore.stderr or "failed to restore the original Git index"
            )
        return {
            "status": "no_action",
            "reason": "only ignored cache changes remain after validation",
            "active_task": job_row.get("task_id", ""),
            "active_agent_job": job_row.get("job_id", ""),
            "changed_paths": [],
            "ignored_changed_paths": sorted(final_changes),
            "command_counts": checkpoint_command_counts(commands),
            "performance": checkpoint_performance(commands),
            "checkpoint_receipt": checkpoint_receipt(
                commands,
                planner_integration=planner_integration,
            ),
            "staged": False,
            "committed": False,
        }

    if validation_mode == "compare":
        assert planner_plan is not None and planner_integration is not None
        staged_receipt, staged_integration = run_checkpoint_staged_acceptance(
            REPO_ROOT,
            transaction_paths=paths_to_stage,
            allowed_path_globs=allowed,
            manifest=planner_plan.manifest,
            agent_job_id=job_row["job_id"],
            command_results=commands,
        )
        planner_integration["staged_acceptance"] = staged_integration
        if staged_receipt.get("status") != "PASS":
            finding = staged_receipt.get("finding", {})
            finding_code = (
                str(finding.get("code", "")) if isinstance(finding, dict) else ""
            )
            return rollback_block(
                "planner staged acceptance or legacy comparison failed",
                final_changes,
                [finding_code] if finding_code else [],
            )
        index_record = staged_receipt.get("index", {})
        final_index_tree = (
            str(index_record.get("final_staged_tree", ""))
            if isinstance(index_record, dict)
            else ""
        )
        if not final_index_tree:
            return rollback_block(
                "planner staged acceptance omitted the final index tree",
                final_changes,
            )
    else:
        staged_project_classifier = run_command([
            ".venv/bin/python",
            "scripts/project_control/classify_project_changes.py",
            "--staged",
            "--json",
        ])
        commands.append(staged_project_classifier)
        if staged_project_classifier.returncode != 0:
            return rollback_block(
                "staged project-change classification failed", final_changes
            )

        staged_project_signals = run_command([
            ".venv/bin/python",
            "scripts/project_control/collect_project_improvement_signals.py",
            "--validate-emitted",
        ])
        commands.append(staged_project_signals)
        if staged_project_signals.returncode != 0:
            return rollback_block(
                "staged project-improvement signal validation failed",
                final_changes,
                suggested_repair_role="validator-engineer",
            )

        staged_documentation_impact = run_command([
            ".venv/bin/python",
            "scripts/project_control/validate_documentation_impact.py",
            "--staged",
        ])
        commands.append(staged_documentation_impact)
        if staged_documentation_impact.returncode != 0:
            return rollback_block(
                "staged documentation-impact validation failed",
                final_changes,
                suggested_repair_role="documentation-curator",
            )

        staged_check = run_command([
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
            "--staged-only",
            "--json",
        ])
        commands.append(staged_check)
        if staged_check.returncode != 0:
            return rollback_block(
                "staged diff allowlist validation failed", final_changes
            )

        final_index_snapshot = run_command(["git", "write-tree"])
        commands.append(final_index_snapshot)
        if final_index_snapshot.returncode != 0 or not final_index_snapshot.stdout.strip():
            return rollback_block(
                "could not identify the final staged tree before memory validation",
                final_changes,
            )
        final_index_tree = final_index_snapshot.stdout.strip()

        final_memory_validation = run_command(final_memory_validation_command())
        commands.append(final_memory_validation)
        if final_memory_validation.returncode != 0:
            return rollback_block(
                "final staged-scope memory validation failed",
                git_status_paths(),
            )

    final_status = git_status_paths()
    final_allowed = allowed_patterns_for_changed_paths(job_row, job_contract, final_status)
    final_disallowed = [
        path for path in final_status if not allowed_by_any(path, final_allowed)
    ]
    if final_disallowed:
        return rollback_block(
            "final staged scope contains paths outside the AgentJob or sync allowlist",
            final_status,
            final_disallowed,
        )
    unstaged_residue = unstaged_stageable_paths(final_status)
    if unstaged_residue:
        return rollback_block(
            "unstaged transaction changes remain after final validation",
            final_status,
            unstaged_residue,
        )
    paths_to_stage = stageable_paths(final_status)

    if no_commit:
        return {
            "status": "ready_to_commit",
            "active_task": job_row.get("task_id", ""),
            "active_agent_job": job_row.get("job_id", ""),
            "execution_role_ref": execution_ref,
            "changed_paths": paths_to_stage,
            "sync_passes": sync_passes,
            "command_counts": checkpoint_command_counts(commands),
            "performance": checkpoint_performance(commands),
            "checkpoint_receipt": checkpoint_receipt(
                commands,
                final_index_tree=final_index_tree,
                planner_integration=planner_integration,
            ),
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
        return rollback_block("git commit failed", final_status)
    rev_parse = run_command(["git", "rev-parse", "HEAD"])
    commands.append(rev_parse)
    return {
        "status": "committed",
        "active_task": job_row.get("task_id", ""),
        "active_agent_job": job_row.get("job_id", ""),
        "execution_role_ref": execution_ref,
        "changed_paths": paths_to_stage,
        "sync_passes": sync_passes,
        "command_counts": checkpoint_command_counts(commands),
        "performance": checkpoint_performance(commands),
        "checkpoint_receipt": checkpoint_receipt(
            commands,
            final_index_tree=final_index_tree,
            planner_integration=planner_integration,
        ),
        "commit_hash": rev_parse.stdout.strip() if rev_parse.returncode == 0 else "",
        "push": "not performed",
        "staged": True,
        "committed": True,
        "command_results": [result.as_dict() for result in commands],
    }


def checkpoint(
    job_id: str | None = None,
    *,
    no_commit: bool = False,
    validation_mode: str = "legacy",
) -> dict[str, object]:
    """Run a checkpoint and restore the exact entry index on helper exceptions."""
    entry_snapshot = run_command(["git", "write-tree"])
    if entry_snapshot.returncode != 0 or not entry_snapshot.stdout.strip():
        raise RuntimeError(entry_snapshot.stderr or "could not snapshot the entry Git index")
    entry_index_tree = entry_snapshot.stdout.strip()
    try:
        return _checkpoint_impl(
            job_id,
            no_commit=no_commit,
            validation_mode=validation_mode,
        )
    except RuntimeError:
        restore = run_command(["git", "read-tree", entry_index_tree])
        if restore.returncode != 0:
            raise RuntimeError(
                restore.stderr or "checkpoint failed and the entry Git index could not be restored"
            )
        raise


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-id", help="Checkpoint a specific AgentJob.")
    parser.add_argument("--no-commit", action="store_true", help="Stage validated changes but do not commit.")
    validation = parser.add_mutually_exclusive_group()
    validation.add_argument(
        "--legacy-validation",
        dest="validation_mode",
        action="store_const",
        const="legacy",
        help="Use the pre-planner checkpoint validation path.",
    )
    validation.add_argument(
        "--compare-validation",
        dest="validation_mode",
        action="store_const",
        const="compare",
        help="Use planner selection and fail-closed legacy status comparison.",
    )
    parser.set_defaults(validation_mode="compare")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = checkpoint(
            args.job_id,
            no_commit=args.no_commit,
            validation_mode=args.validation_mode,
        )
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
