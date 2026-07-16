"""Bounded read-only execution for validated v19 shadow plans.

The executor emits operational evidence only.  It does not make the manifest
planner authoritative and it never confers scientific, ontology, benchmark,
proof, or Gate Chair authority.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import time
from typing import Mapping, Protocol, Sequence

from scripts.validation.plan import PlannerError, ValidationPlan, build_plan


class ExecutorError(ValueError):
    """Fail-closed executor configuration error."""


class ExecutionCancelled(RuntimeError):
    """Internal signal used by adapters that observe cancellation."""


@dataclass(frozen=True, slots=True)
class AdapterResult:
    """Bounded process metadata; raw output belongs in the context paths."""

    exit_code: int = 0
    child_gates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.exit_code, int):
            raise TypeError("adapter exit_code must be an integer")
        object.__setattr__(self, "child_gates", tuple(self.child_gates))
        if any(not isinstance(value, str) or not value for value in self.child_gates):
            raise ValueError("child_gates must contain nonblank strings")


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    gate_id: str
    timeout_seconds: int
    stdout_path: Path
    stderr_path: Path
    cancellation: threading.Event


class ValidationAdapter(Protocol):
    def run(self, context: ExecutionContext) -> AdapterResult:
        """Run one declared read-only gate."""


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    status: str
    exit_code: int
    receipt: dict[str, object]
    receipt_path: Path | None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class SubprocessAdapter:
    """Shell-free adapter that captures complete process output to files."""

    command: tuple[str, ...]
    cwd: Path | None = None
    poll_interval_seconds: float = 0.02

    def __post_init__(self) -> None:
        object.__setattr__(self, "command", tuple(self.command))
        if not self.command or any(not isinstance(value, str) or not value for value in self.command):
            raise ValueError("subprocess command must contain nonblank arguments")
        if self.poll_interval_seconds <= 0:
            raise ValueError("poll_interval_seconds must be positive")

    @staticmethod
    def _stop(process: subprocess.Popen[bytes]) -> None:
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    def run(self, context: ExecutionContext) -> AdapterResult:
        started = time.monotonic()
        with context.stdout_path.open("wb") as stdout, context.stderr_path.open("wb") as stderr:
            process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                shell=False,
            )
            while process.poll() is None:
                if context.cancellation.is_set():
                    self._stop(process)
                    raise ExecutionCancelled("execution cancelled")
                if time.monotonic() - started >= context.timeout_seconds:
                    self._stop(process)
                    raise TimeoutError(f"gate exceeded {context.timeout_seconds}s timeout")
                time.sleep(self.poll_interval_seconds)
        assert process.returncode is not None
        if process.returncode < 0:
            raise ChildProcessError(f"process terminated by signal {-process.returncode}")
        return AdapterResult(exit_code=process.returncode)


_COST_PRIORITY = {"fast": 0, "medium": 1, "slow": 2}


def _classification_for(plan: ValidationPlan) -> dict[str, object]:
    return {
        "changed_paths": list(plan.changed_paths),
        "blocked_paths": list(plan.blocked_paths),
        "path_family_tags": list(plan.path_tags),
        "path_family_details": [
            {"path": path, "tags": ["unknown_governed_path"]}
            for path in plan.unknown_paths
        ],
    }


def _validate_read_only_plan(
    plan: ValidationPlan,
    manifest: Mapping[str, object],
    adapters: Mapping[str, ValidationAdapter],
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    if not isinstance(plan, ValidationPlan):
        raise ExecutorError("plan must be a ValidationPlan")
    try:
        rebuilt = build_plan(
            manifest,
            _classification_for(plan),
            profile=plan.requested_profile,
            scopes=plan.scopes,
            role_obligations=plan.role_obligations,
        )
    except PlannerError as error:
        raise ExecutorError(f"manifest or plan validation failed: {error}") from error
    if rebuilt.canonical_json() != plan.canonical_json():
        raise ExecutorError("plan does not match the validated manifest and inputs")
    if plan.status != "READY":
        raise ExecutorError(f"plan is not executable: {plan.status}")
    if plan.execution_authority != "legacy" or manifest.get("execution_authority") != "legacy":
        raise ExecutorError("shadow executor requires legacy execution authority")

    raw_gates = manifest.get("gates")
    assert isinstance(raw_gates, list)
    gates = {str(gate["gate_id"]): gate for gate in raw_gates if isinstance(gate, dict)}
    entries = {
        str(entry["gate_id"]): entry
        for entry in plan.entries
        if isinstance(entry.get("gate_id"), str)
    }
    for gate_id in plan.ordered_gate_ids:
        gate = gates.get(gate_id)
        if gate is None:
            raise ExecutorError(f"unknown selected gate: {gate_id}")
        if gate.get("mutating") is not False:
            raise ExecutorError(f"mutating gate is forbidden in P6-T01: {gate_id}")
        adapter_id = gate.get("adapter")
        if not isinstance(adapter_id, str) or adapter_id not in adapters:
            raise ExecutorError(f"missing adapter for selected gate: {gate_id}")
        if gate_id not in entries:
            raise ExecutorError(f"missing selected plan entry: {gate_id}")
    return gates, entries


def _failure_status(severity: str) -> str:
    return "FAIL" if severity == "blocking" else "WARN"


def _file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _run_gate(
    gate_id: str,
    gate: Mapping[str, object],
    entry: Mapping[str, object],
    adapter: ValidationAdapter,
    log_directory: Path,
    ordinal: int,
    cancellation: threading.Event,
) -> dict[str, object]:
    prefix = f"{ordinal:04d}-{gate_id}"
    stdout_path = log_directory / f"{prefix}.stdout"
    stderr_path = log_directory / f"{prefix}.stderr"
    stdout_path.touch()
    stderr_path.touch()
    context = ExecutionContext(
        gate_id=gate_id,
        timeout_seconds=int(gate["timeout_seconds"]),
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        cancellation=cancellation,
    )
    started = time.monotonic()
    exit_code = 0
    child_gates: tuple[str, ...] = ()
    reason = "completed"
    status = "PASS"
    try:
        adapter_result = adapter.run(context)
        if not isinstance(adapter_result, AdapterResult):
            raise TypeError("adapter must return AdapterResult")
        exit_code = adapter_result.exit_code
        child_gates = adapter_result.child_gates
        if exit_code < 0:
            raise ChildProcessError(f"process terminated by signal {-exit_code}")
        if exit_code:
            reason = "nonzero_exit"
            status = _failure_status(str(gate["severity"]))
    except ExecutionCancelled:
        cancellation.set()
        exit_code = 130
        reason = "cancelled_during_execution"
        status = "BLOCKED_CONFIGURATION"
    except TimeoutError:
        exit_code = 124
        reason = "timeout"
        status = _failure_status(str(gate["severity"]))
    except ChildProcessError as error:
        exit_code = 70
        reason = "child_process_crash"
        status = _failure_status(str(gate["severity"]))
        with stderr_path.open("ab") as stderr:
            stderr.write(f"executor captured {type(error).__name__}: {error}\n".encode("utf-8"))
    except (OSError, TypeError, ValueError) as error:
        exit_code = 2
        reason = "adapter_configuration_error"
        status = "BLOCKED_CONFIGURATION"
        with stderr_path.open("ab") as stderr:
            stderr.write(f"executor captured {type(error).__name__}: {error}\n".encode("utf-8"))
    return {
        "gate_id": gate_id,
        "status": status,
        "severity": gate["severity"],
        "reason": reason,
        "exit_code": exit_code,
        "duration_seconds": round(time.monotonic() - started, 6),
        "stdout_bytes": _file_size(stdout_path),
        "stderr_bytes": _file_size(stderr_path),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "child_gates": list(child_gates),
        "dependencies": sorted(str(value) for value in gate["prerequisites"]),
        "satisfied_obligations": (
            sorted(str(value) for value in gate["satisfies_obligations"])
            if status == "PASS"
            else []
        ),
        "plan_reasons": list(entry["reasons"]),
    }


def _skipped_gate(
    gate_id: str,
    gate: Mapping[str, object],
    entry: Mapping[str, object],
    reason: str,
) -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "status": "SKIP_NOT_APPLICABLE",
        "severity": gate["severity"],
        "reason": reason,
        "exit_code": 0,
        "duration_seconds": 0.0,
        "stdout_bytes": 0,
        "stderr_bytes": 0,
        "stdout_path": None,
        "stderr_path": None,
        "child_gates": [],
        "dependencies": sorted(str(value) for value in gate["prerequisites"]),
        "satisfied_obligations": [],
        "plan_reasons": list(entry["reasons"]),
    }


def _run_status(results: Sequence[Mapping[str, object]], cancelled: bool) -> tuple[str, int]:
    if cancelled or any(result["status"] == "BLOCKED_CONFIGURATION" for result in results):
        return "BLOCKED_CONFIGURATION", 2
    if any(result["status"] == "FAIL" for result in results):
        return "FAIL", 1
    if any(result["status"] == "WARN" for result in results):
        return "WARN", 0
    return "PASS", 0


def _atomic_write(receipt: Mapping[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
            json.dump(receipt, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def execute_plan(
    plan: ValidationPlan,
    manifest: Mapping[str, object],
    adapters: Mapping[str, ValidationAdapter],
    *,
    receipt_root: Path,
    max_workers: int = 4,
    cancellation: threading.Event | None = None,
    run_id: str | None = None,
) -> ExecutionOutcome:
    """Validate and execute one read-only shadow plan, then atomically receipt it."""

    if not isinstance(max_workers, int) or isinstance(max_workers, bool) or max_workers < 1:
        raise ExecutorError("max_workers must be a positive integer")
    gates, entries = _validate_read_only_plan(plan, manifest, adapters)
    cancellation = cancellation or threading.Event()
    plan_hash = hashlib.sha256(plan.canonical_json().encode("utf-8")).hexdigest()
    if run_id is None:
        nonce = f"{plan_hash}:{time.time_ns()}".encode("utf-8")
        run_id = f"RUN-{hashlib.sha256(nonce).hexdigest()[:16]}"
    if not isinstance(run_id, str) or not re.fullmatch(r"RUN-[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id):
        raise ExecutorError("run_id must be a path-safe RUN-prefixed identity")

    run_directory = Path(receipt_root) / plan.manifest_hash / run_id
    log_directory = run_directory / "gates"
    try:
        log_directory.mkdir(parents=True, exist_ok=False)
    except OSError as error:
        raise ExecutorError(f"receipt directory creation failed: {error}") from error

    order = list(plan.ordered_gate_ids)
    position = {gate_id: index for index, gate_id in enumerate(order)}
    pending = set(order)
    completed: set[str] = set()
    results: dict[str, dict[str, object]] = {}
    fail_fast = False
    while pending and not fail_fast and not cancellation.is_set():
        ready = [
            gate_id
            for gate_id in order
            if gate_id in pending
            and set(str(value) for value in gates[gate_id]["prerequisites"]) <= completed
        ]
        if not ready:
            raise ExecutorError("selected plan cannot make dependency progress")
        priority = min(
            (
                0 if gates[gate_id]["severity"] == "blocking" and gates[gate_id]["cost_class"] == "fast"
                else 1 + _COST_PRIORITY[str(gates[gate_id]["cost_class"])]
            )
            for gate_id in ready
        )
        tier = [
            gate_id
            for gate_id in ready
            if (
                0 if gates[gate_id]["severity"] == "blocking" and gates[gate_id]["cost_class"] == "fast"
                else 1 + _COST_PRIORITY[str(gates[gate_id]["cost_class"])]
            ) == priority
        ]
        parallel_group = gates[tier[0]]["parallel_group"]
        batch = [gate_id for gate_id in tier if gates[gate_id]["parallel_group"] == parallel_group]
        with ThreadPoolExecutor(max_workers=min(max_workers, len(batch))) as pool:
            futures = {
                gate_id: pool.submit(
                    _run_gate,
                    gate_id,
                    gates[gate_id],
                    entries[gate_id],
                    adapters[str(gates[gate_id]["adapter"])],
                    log_directory,
                    position[gate_id],
                    cancellation,
                )
                for gate_id in batch
            }
            for gate_id in batch:
                results[gate_id] = futures[gate_id].result()
                pending.remove(gate_id)
                completed.add(gate_id)
        fail_fast = any(
            results[gate_id]["status"] in {"FAIL", "BLOCKED_CONFIGURATION"}
            and gates[gate_id]["severity"] == "blocking"
            for gate_id in batch
        )

    skip_reason = "cancelled_before_start" if cancellation.is_set() else "fail_fast"
    for gate_id in order:
        if gate_id in pending:
            results[gate_id] = _skipped_gate(gate_id, gates[gate_id], entries[gate_id], skip_reason)
    ordered_results = [results[gate_id] for gate_id in order]
    cancelled = cancellation.is_set()
    status, exit_code = _run_status(ordered_results, cancelled)
    counts = {
        "gate_count": len(ordered_results),
        "pass_count": sum(result["status"] == "PASS" for result in ordered_results),
        "fail_count": sum(result["status"] == "FAIL" for result in ordered_results),
        "warn_count": sum(result["status"] == "WARN" for result in ordered_results),
        "blocked_count": sum(result["status"] == "BLOCKED_CONFIGURATION" for result in ordered_results),
        "skipped_count": sum(str(result["status"]).startswith("SKIP_") for result in ordered_results),
    }
    receipt: dict[str, object] = {
        "schema_id": "validation_execution_receipt_v1",
        "schema_version": 1,
        "run_id": run_id,
        "plan_hash": plan_hash,
        "manifest_hash": plan.manifest_hash,
        "execution_authority": "legacy",
        "migration_epoch": "shadow_planner",
        "status": status,
        "exit_code": exit_code,
        "cancelled": cancelled,
        "counts": counts,
        "gate_results": ordered_results,
        "authority": {
            "operational_validation_only": True,
            "legacy_result_authoritative": True,
            "source_authoritative": False,
            "physics_claim_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "proof_authority": False,
            "gate_chair_authority": False,
        },
    }
    receipt_path = run_directory / "receipt.json"
    try:
        _atomic_write(receipt, receipt_path)
    except OSError as error:
        failed_receipt = dict(receipt)
        failed_receipt["status"] = "BLOCKED_CONFIGURATION"
        failed_receipt["exit_code"] = 2
        failed_receipt["error"] = f"receipt_write_failed: {error}"
        return ExecutionOutcome(
            "BLOCKED_CONFIGURATION",
            2,
            failed_receipt,
            None,
            f"receipt_write_failed: {error}",
        )
    return ExecutionOutcome(status, exit_code, receipt, receipt_path)
