"""Bounded read-only execution for validated v19 shadow plans.

The executor emits operational evidence only.  It does not make the manifest
planner authoritative and it never confers scientific, ontology, benchmark,
proof, or Gate Chair authority.
"""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import time
from typing import Callable, Mapping, Protocol, Sequence

from scripts.validation.cache import ValidationCache
from scripts.validation.mutators import (
    MutatorContractError,
    matches_any,
    mutation_delta,
    selected_mutators,
    snapshot_tree,
    validate_allowed_globs,
    validate_mutator_gate,
)
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
class GateCacheEvidence:
    """Complete decision-relevant closure for one potentially cacheable gate."""

    implementation_digest: str
    source_fingerprint_manifest: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_fingerprint_manifest",
            tuple(dict(item) for item in self.source_fingerprint_manifest),
        )


@dataclass(frozen=True, slots=True)
class ExecutionCacheContext:
    """Invocation-wide exact-state identity supplied by the execution owner."""

    cache: ValidationCache
    tree_state: str
    tree_hash: str
    base_ref_name: str
    base_ref_commit: str
    git_common_dir: Path
    environment_fingerprint: str
    dependency_lock_digest: str
    gate_evidence: Mapping[str, GateCacheEvidence]
    freshness_check: Callable[[], bool]
    mandatory_bypass_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.cache, ValidationCache):
            raise TypeError("cache must be a ValidationCache")
        if self.tree_state not in {"working", "staged", "commit"}:
            raise ValueError("tree_state must be working, staged, or commit")
        if not callable(self.freshness_check):
            raise TypeError("freshness_check must be callable")
        evidence = dict(self.gate_evidence)
        if any(
            not isinstance(gate_id, str)
            or not gate_id
            or not isinstance(value, GateCacheEvidence)
            for gate_id, value in evidence.items()
        ):
            raise TypeError("gate_evidence must map gate IDs to GateCacheEvidence")
        object.__setattr__(self, "gate_evidence", evidence)
        object.__setattr__(self, "git_common_dir", Path(self.git_common_dir).absolute())
        if self.mandatory_bypass_reason is not None and not self.mandatory_bypass_reason.strip():
            raise ValueError("mandatory_bypass_reason must be nonblank when present")


@dataclass(frozen=True, slots=True)
class _GateCachePlan:
    cache: ValidationCache | None
    key_material: dict[str, object] | None
    source_fingerprint_manifest: tuple[dict[str, object], ...]
    freshness_check: Callable[[], bool]
    gate_policy: str
    mandatory_bypass: bool
    initial_cache_status: str
    initial_reason: str


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
_UNCONDITIONALLY_UNCACHED_GATE_IDS = {"git_diff_check", "checkpoint_transaction"}


def _utc_timestamp(value: datetime | None = None) -> str:
    timestamp = value or datetime.now(timezone.utc)
    return timestamp.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: object) -> str:
    return f"sha256:{hashlib.sha256(_canonical_bytes(value)).hexdigest()}"


def _canonical_sources(
    values: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            (dict(value) for value in values),
            key=lambda value: (
                str(value.get("input_id", "")),
                str(value.get("input_type", "")),
            ),
        )
    )


def _safe_freshness(check: Callable[[], bool]) -> bool:
    try:
        return check() is True
    except Exception:
        # Cache evidence is optional; an unreliable freshness probe disables reuse.
        return False


def _cache_plan_for_gate(
    plan: ValidationPlan,
    manifest: Mapping[str, object],
    gate_id: str,
    gate: Mapping[str, object],
    entry: Mapping[str, object],
    cache_context: ExecutionCacheContext | None,
    *,
    receipt_root: Path,
) -> _GateCachePlan:
    policy = str(gate["cache_policy"])
    if policy == "ineligible":
        return _GateCachePlan(
            None, None, (), lambda: False, policy, False, "NOT_ELIGIBLE", "gate_policy_ineligible"
        )
    if gate.get("mutating") is not False:
        return _GateCachePlan(
            None, None, (), lambda: False, policy, True, "NOT_ELIGIBLE", "mutating_gate"
        )
    if cache_context is None:
        return _GateCachePlan(
            None, None, (), lambda: False, policy, False, "NOT_ELIGIBLE", "cache_evidence_absent"
        )
    freshness_check = lambda: _safe_freshness(cache_context.freshness_check)
    evidence = cache_context.gate_evidence.get(gate_id)
    if evidence is None or not evidence.source_fingerprint_manifest:
        return _GateCachePlan(
            cache_context.cache,
            None,
            (),
            freshness_check,
            policy,
            False,
            "NOT_ELIGIBLE",
            "incomplete_evidence_identity",
        )
    try:
        Path(receipt_root).resolve().relative_to(cache_context.cache.repository_root)
    except ValueError:
        return _GateCachePlan(
            cache_context.cache,
            None,
            (),
            freshness_check,
            policy,
            False,
            "NOT_ELIGIBLE",
            "receipt_root_outside_repository",
        )

    declared_scopes = {str(value) for value in gate["scopes"]}
    if "repository" in plan.scopes and "repository" in declared_scopes:
        scope_kind = "repository"
    elif cache_context.tree_state in declared_scopes:
        scope_kind = cache_context.tree_state
    else:
        return _GateCachePlan(
            cache_context.cache,
            None,
            (),
            freshness_check,
            policy,
            False,
            "NOT_ELIGIBLE",
            "scope_evidence_incomplete",
        )

    mandatory_bypass = bool(cache_context.mandatory_bypass_reason) or (
        gate_id in _UNCONDITIONALLY_UNCACHED_GATE_IDS
    )
    bypass_reason = cache_context.mandatory_bypass_reason
    if gate_id in _UNCONDITIONALLY_UNCACHED_GATE_IDS:
        bypass_reason = "unconditionally_uncached_safeguard"
    sources = _canonical_sources(evidence.source_fingerprint_manifest)
    selection_material = {
        "ordered_gate_ids": list(plan.ordered_gate_ids),
        "selected_gate_ids": list(plan.selected_gate_ids),
        "changed_paths": list(plan.changed_paths),
        "blocked_paths": list(plan.blocked_paths),
        "path_tags": list(plan.path_tags),
        "scopes": list(plan.scopes),
        "role_obligations": list(plan.role_obligations),
    }
    config_material = {
        "gate": dict(gate),
        "plan_entry": dict(entry),
        "requested_profile": plan.requested_profile,
        "effective_profile": plan.effective_profile,
        "execution_authority": plan.execution_authority,
    }
    repository_identity = {
        "repository_root": str(cache_context.cache.repository_root.resolve()),
        "git_common_dir": str(cache_context.git_common_dir.resolve()),
    }
    key_material: dict[str, object] = {
        "schema_id": "validation_cache_key_v1",
        "schema_version": 1,
        "contract_id": "validation-cache-contract-v1",
        "gate_id": gate_id,
        "scope": {
            "scope_kind": scope_kind,
            "tree_state": cache_context.tree_state,
            "profile": plan.effective_profile,
            "mode": "legacy",
            "selection_digest": _sha256(selection_material),
            "repository_identity_digest": _sha256(repository_identity),
        },
        "tree_hash": cache_context.tree_hash,
        "base_ref": {
            "name": cache_context.base_ref_name,
            "commit": cache_context.base_ref_commit,
        },
        "implementation_digest": evidence.implementation_digest,
        "manifest_digest": _sha256(manifest),
        "config_digest": _sha256(config_material),
        "environment_fingerprint": cache_context.environment_fingerprint,
        "dependency_lock_digest": cache_context.dependency_lock_digest,
        "receipt_schema": {
            "gate_result_id": "validation_gate_result_v1",
            "gate_result_version": 1,
            "run_receipt_id": "validation_run_receipt_v1",
            "run_receipt_version": 1,
        },
    }
    return _GateCachePlan(
        cache_context.cache,
        key_material,
        sources,
        freshness_check,
        policy,
        mandatory_bypass,
        "BYPASSED" if mandatory_bypass else "MISS",
        bypass_reason
        or ("cache_mode_off" if cache_context.cache.mode == "off" else "lookup_required"),
    )


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


def _validate_plan(
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
        if gate.get("mutating") is True:
            try:
                validate_mutator_gate(gate)
            except MutatorContractError as error:
                raise ExecutorError(f"mutating gate contract invalid: {error}") from error
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
    attempt: int | None = None,
) -> dict[str, object]:
    attempt_suffix = f"-pass-{attempt:02d}" if attempt is not None else ""
    prefix = f"{ordinal:04d}-{gate_id}{attempt_suffix}"
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
    started_at = datetime.now(timezone.utc)
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
    finished_at = datetime.now(timezone.utc)
    duration_seconds = round(time.monotonic() - started, 6)
    return {
        "gate_id": gate_id,
        "status": status,
        "severity": gate["severity"],
        "reason": reason,
        "exit_code": exit_code,
        "started_at": _utc_timestamp(started_at),
        "finished_at": _utc_timestamp(finished_at),
        "duration_ms": round((finished_at - started_at).total_seconds() * 1000),
        "duration_seconds": duration_seconds,
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


def _write_gate_full_receipt(
    result: Mapping[str, object],
    *,
    log_directory: Path,
    repository_root: Path,
) -> dict[str, object]:
    gate_id = str(result["gate_id"])
    artifact_id = f"ART-{hashlib.sha256(gate_id.encode('utf-8')).hexdigest()[:24]}"
    path = log_directory / f"{gate_id}.full-receipt.json"
    evidence = {
        "schema_id": "validation_executor_gate_evidence_v1",
        "gate_id": gate_id,
        "result": dict(result),
        "authority": "operational_validation_only",
    }
    _atomic_write(evidence, path)
    payload = path.read_bytes()
    return {
        "artifact_id": artifact_id,
        "path": path.resolve().relative_to(repository_root).as_posix(),
        "content_hash": f"sha256:{hashlib.sha256(payload).hexdigest()}",
        "local_only": True,
        "authoritative": False,
    }


def _cache_original_result(
    result: Mapping[str, object],
    cache_plan: _GateCachePlan,
    full_receipt: Mapping[str, object],
) -> dict[str, object]:
    assert cache_plan.key_material is not None
    implementation_digest = str(cache_plan.key_material["implementation_digest"])
    severity = str(result["severity"])
    if severity == "local_only":
        severity = "diagnostic"
    return {
        "schema_id": "validation_gate_result_v1",
        "gate_id": result["gate_id"],
        "severity": severity,
        "status": result["status"],
        "cache_status": "MISS",
        "input_fingerprint": _sha256(cache_plan.source_fingerprint_manifest),
        "implementation_fingerprint": implementation_digest,
        "started_at": result["started_at"],
        "finished_at": result["finished_at"],
        "duration_ms": result["duration_ms"],
        "error_count": 0,
        "warning_count": 0,
        "finding_count": 0,
        "shown_finding_count": 0,
        "findings_truncated": False,
        "shown_findings": [],
        "full_receipt": dict(full_receipt),
        "satisfied_obligation_ids": list(result["satisfied_obligations"]),
        "child_gate_ids": list(result["child_gates"]),
        "mutated_paths": [],
        "artifact_refs": [],
    }


def _cache_hit_result(
    gate_id: str,
    gate: Mapping[str, object],
    entry: Mapping[str, object],
    original: Mapping[str, object],
    *,
    result_hash: str | None,
    started_at: datetime,
    finished_at: datetime,
) -> dict[str, object]:
    duration_ms = round((finished_at - started_at).total_seconds() * 1000)
    original_duration_ms = int(original["duration_ms"])
    full_receipt = dict(original["full_receipt"])  # type: ignore[arg-type]
    return {
        "gate_id": gate_id,
        "status": "CACHE_HIT",
        "severity": gate["severity"],
        "reason": "cache_hit",
        "cache_status": "HIT",
        "cache_reason": "exact_match",
        "cache_write_status": "NOT_ATTEMPTED",
        "cache_write_reason": "cache_hit",
        "exit_code": 0,
        "started_at": _utc_timestamp(started_at),
        "finished_at": _utc_timestamp(finished_at),
        "duration_ms": duration_ms,
        "duration_seconds": round(duration_ms / 1000, 6),
        "duration_saved_seconds": round(original_duration_ms / 1000, 6),
        "original_status": original["status"],
        "original_receipt_hash": full_receipt["content_hash"],
        "result_hash": result_hash,
        "input_fingerprint": original["input_fingerprint"],
        "implementation_fingerprint": original["implementation_fingerprint"],
        "full_receipt": full_receipt,
        "stdout_bytes": 0,
        "stderr_bytes": 0,
        "stdout_path": None,
        "stderr_path": None,
        "child_gates": list(original["child_gate_ids"]),
        "dependencies": sorted(str(value) for value in gate["prerequisites"]),
        "satisfied_obligations": list(original["satisfied_obligation_ids"]),
        "plan_reasons": list(entry["reasons"]),
    }


def _run_gate_cached(
    gate_id: str,
    gate: Mapping[str, object],
    entry: Mapping[str, object],
    adapter: ValidationAdapter,
    log_directory: Path,
    ordinal: int,
    cancellation: threading.Event,
    cache_plan: _GateCachePlan,
    cache_lock: threading.Lock,
) -> dict[str, object]:
    if cache_plan.cache is None or cache_plan.key_material is None:
        result = _run_gate(
            gate_id, gate, entry, adapter, log_directory, ordinal, cancellation
        )
        result.update(
            {
                "cache_status": cache_plan.initial_cache_status,
                "cache_reason": cache_plan.initial_reason,
                "cache_write_status": "NOT_ATTEMPTED",
                "cache_write_reason": cache_plan.initial_reason,
                "duration_saved_seconds": 0.0,
            }
        )
        return result

    lookup_started = datetime.now(timezone.utc)
    with cache_lock:
        lookup = cache_plan.cache.lookup(
            cache_plan.key_material,
            gate_policy=cache_plan.gate_policy,
            mandatory_bypass=cache_plan.mandatory_bypass,
            freshness_check=cache_plan.freshness_check,
        )
    lookup_finished = datetime.now(timezone.utc)
    if lookup.hit and lookup.original_result is not None:
        return _cache_hit_result(
            gate_id,
            gate,
            entry,
            lookup.original_result,
            result_hash=lookup.result_hash,
            started_at=lookup_started,
            finished_at=lookup_finished,
        )

    if cache_plan.mandatory_bypass or lookup.status == "DISABLED":
        cache_status = "BYPASSED"
    else:
        cache_status = "MISS"
    result = _run_gate(
        gate_id, gate, entry, adapter, log_directory, ordinal, cancellation
    )
    result.update(
        {
            "cache_status": cache_status,
            "cache_reason": lookup.reason,
            "cache_key": lookup.cache_key,
            "cache_write_status": "NOT_ATTEMPTED",
            "cache_write_reason": "result_not_cacheable",
            "duration_saved_seconds": 0.0,
        }
    )
    if result["status"] != "PASS" or cache_status != "MISS":
        return result
    if lookup.reason not in {"absent", "expired"}:
        result["cache_write_status"] = "SKIPPED"
        result["cache_write_reason"] = f"lookup_not_publishable:{lookup.reason}"
        return result
    if not cache_plan.freshness_check():
        result["cache_write_status"] = "SKIPPED"
        result["cache_write_reason"] = "snapshot_stale_after_execution"
        return result

    try:
        full_receipt = _write_gate_full_receipt(
            result,
            log_directory=log_directory,
            repository_root=cache_plan.cache.repository_root,
        )
        original = _cache_original_result(result, cache_plan, full_receipt)
        with cache_lock:
            if lookup.reason == "expired":
                cache_plan.cache.evict()
            if cache_plan.cache.reads_disabled:
                result["cache_write_status"] = "SKIPPED"
                result["cache_write_reason"] = "reads_disabled_after_maintenance"
                return result
            write = cache_plan.cache.store(
                cache_plan.key_material,
                original,
                source_fingerprint_manifest=cache_plan.source_fingerprint_manifest,
                gate_policy=cache_plan.gate_policy,
                mandatory_bypass=cache_plan.mandatory_bypass,
            )
        result.update(
            {
                "input_fingerprint": original["input_fingerprint"],
                "implementation_fingerprint": original["implementation_fingerprint"],
                "full_receipt": full_receipt,
                "cache_write_status": write.status,
                "cache_write_reason": write.reason,
                "cache_key": write.cache_key or lookup.cache_key,
            }
        )
    except (OSError, ValueError) as error:
        result["cache_write_status"] = "SKIPPED"
        result["cache_write_reason"] = f"full_receipt_unavailable:{type(error).__name__}"
    return result


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
        "cache_status": "NOT_ELIGIBLE",
        "cache_reason": reason,
        "cache_write_status": "NOT_ATTEMPTED",
        "cache_write_reason": reason,
        "duration_saved_seconds": 0.0,
        "started_at": None,
        "finished_at": None,
        "duration_ms": 0,
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
    mutation_root: Path | None = None,
    allowed_mutation_globs: Sequence[str] = (),
    max_stabilization_passes: int = 3,
    replan_if_new_tags: Callable[[tuple[str, ...]], ValidationPlan | None] | None = None,
    cache_context: ExecutionCacheContext | None = None,
) -> ExecutionOutcome:
    """Execute one validated shadow plan with a bounded pre-validation barrier."""

    if not isinstance(max_workers, int) or isinstance(max_workers, bool) or max_workers < 1:
        raise ExecutorError("max_workers must be a positive integer")
    if (
        not isinstance(max_stabilization_passes, int)
        or isinstance(max_stabilization_passes, bool)
        or max_stabilization_passes < 1
    ):
        raise ExecutorError("max_stabilization_passes must be a positive integer")
    if replan_if_new_tags is not None and not callable(replan_if_new_tags):
        raise ExecutorError("replan_if_new_tags must be callable")
    gates, entries = _validate_plan(plan, manifest, adapters)
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

    active_plan = plan
    mutator_ids = selected_mutators(active_plan.ordered_gate_ids, gates)
    mutator_results: dict[str, dict[str, object]] = {}
    barrier_passes: list[dict[str, object]] = []
    mutation_sequence: list[str] = []
    cumulative_changed_paths: set[str] = set()
    paths_considered_for_replan: set[str] = set()
    replan_count = 0
    replan_events: list[dict[str, object]] = []
    barrier_status = "NOT_APPLICABLE"
    barrier_finding_id: str | None = None

    if mutator_ids:
        if mutation_root is None:
            raise ExecutorError("mutation_root is required when the plan selects mutators")
        try:
            allowed_globs = validate_allowed_globs(
                allowed_mutation_globs,
                context="allowed_mutation_globs",
            )
        except MutatorContractError as error:
            raise ExecutorError(str(error)) from error
        mutation_root = Path(mutation_root)
        barrier_status = "RUNNING"
        for pass_number in range(1, max_stabilization_passes + 1):
            pass_before = snapshot_tree(mutation_root, excluded=(receipt_root,))
            pass_results: list[dict[str, object]] = []
            stop_this_pass = False
            for ordinal, gate_id in enumerate(mutator_ids):
                gate = gates[gate_id]
                before = snapshot_tree(mutation_root, excluded=(receipt_root,))
                result = _run_gate(
                    gate_id,
                    gate,
                    entries[gate_id],
                    adapters[str(gate["adapter"])],
                    log_directory,
                    ordinal,
                    cancellation,
                    attempt=pass_number,
                )
                after = snapshot_tree(mutation_root, excluded=(receipt_root,))
                delta = mutation_delta(before, after)
                declared_globs = validate_mutator_gate(gate)
                disallowed_paths = [
                    path
                    for path in delta.changed_paths
                    if not matches_any(path, declared_globs)
                    or not matches_any(path, allowed_globs)
                ]
                result = dict(result)
                result.update(
                    {
                        "barrier_pass": pass_number,
                        "mutation": delta.to_dict(),
                        "declared_output_globs": list(declared_globs),
                        "job_allowed_output_globs": list(allowed_globs),
                        "disallowed_paths": disallowed_paths,
                        "cache_eligible": False,
                        "cache_status": "NOT_ELIGIBLE",
                        "cache_reason": "mutating_gate",
                        "cache_write_status": "NOT_ATTEMPTED",
                        "cache_write_reason": "mutating_gate",
                        "duration_saved_seconds": 0.0,
                        "rollback": {
                            "required": bool(disallowed_paths) or result["status"] != "PASS",
                            "performed": False,
                            "authority": "legacy_checkpoint_index_owner",
                            "before_tree_hash": delta.before_tree_hash,
                            "after_tree_hash": delta.after_tree_hash,
                            "changed_paths": list(delta.changed_paths),
                        },
                    }
                )
                if disallowed_paths:
                    result["status"] = "BLOCKED_CONFIGURATION"
                    result["exit_code"] = 2
                    result["reason"] = "disallowed_mutation_output"
                    result["satisfied_obligations"] = []
                    barrier_status = "DISALLOWED_OUTPUT"
                    barrier_finding_id = "V19-MUTATOR-DISALLOWED-OUTPUT"
                elif result["status"] != "PASS":
                    barrier_status = "MUTATOR_FAILED"
                    barrier_finding_id = "V19-MUTATOR-EXECUTION-FAILED"
                pass_results.append(result)
                mutator_results[gate_id] = result
                mutation_sequence.append(gate_id)
                cumulative_changed_paths.update(delta.changed_paths)
                if result["status"] != "PASS":
                    stop_this_pass = True
                    break

            pass_after = snapshot_tree(mutation_root, excluded=(receipt_root,))
            pass_delta = mutation_delta(pass_before, pass_after)
            barrier_passes.append(
                {
                    "pass": pass_number,
                    "before_tree_hash": pass_delta.before_tree_hash,
                    "after_tree_hash": pass_delta.after_tree_hash,
                    "before_paths": list(pass_delta.before_paths),
                    "after_paths": list(pass_delta.after_paths),
                    "changed_paths": list(pass_delta.changed_paths),
                    "gate_results": pass_results,
                }
            )
            cumulative_changed_paths.update(pass_delta.changed_paths)
            if stop_this_pass:
                break

            new_paths = tuple(
                sorted(set(pass_delta.changed_paths) - paths_considered_for_replan)
            )
            if new_paths and replan_if_new_tags is not None:
                paths_considered_for_replan.update(new_paths)
                replanned = replan_if_new_tags(new_paths)
                if replanned is not None and replanned.canonical_json() != active_plan.canonical_json():
                    added_tags = sorted(set(replanned.path_tags) - set(active_plan.path_tags))
                    if not added_tags:
                        raise ExecutorError(
                            "mutation replan changed the plan without new affected tags"
                        )
                    gates, entries = _validate_plan(replanned, manifest, adapters)
                    replan_events.append(
                        {
                            "trigger_paths": list(new_paths),
                            "new_affected_tags": added_tags,
                        }
                    )
                    active_plan = replanned
                    mutator_ids = selected_mutators(active_plan.ordered_gate_ids, gates)
                    replan_count += 1

            if not pass_delta.changes:
                barrier_status = "STABLE"
                break
        else:
            barrier_status = "NON_CONVERGING"
            barrier_finding_id = "V19-MUTATOR-NON-CONVERGENCE"
            if mutator_ids:
                failing_gate_id = mutator_ids[-1]
                failed = mutator_results[failing_gate_id]
                failed["status"] = "FAIL"
                failed["exit_code"] = 1
                failed["reason"] = "stabilization_limit_exceeded"
                failed["satisfied_obligations"] = []
                rollback = dict(failed["rollback"])
                rollback["required"] = True
                failed["rollback"] = rollback
                mutator_results[failing_gate_id] = failed

    first_pdf = next(
        (index for index, gate_id in enumerate(mutation_sequence) if gate_id == "targeted_pdf_build"),
        None,
    )
    targeted_pdf_second_sync_observed = bool(
        first_pdf is not None
        and any(
            gate_id == "memory_sync"
            for gate_id in mutation_sequence[first_pdf + 1 :]
        )
    )
    barrier_receipt: dict[str, object] = {
        "schema_id": "validation_mutator_barrier_v1",
        "status": barrier_status,
        "finding_id": barrier_finding_id,
        "pass_count": len(barrier_passes),
        "max_stabilization_passes": max_stabilization_passes,
        "selected_mutator_ids": list(mutator_ids),
        "execution_sequence": mutation_sequence,
        "changed_paths": sorted(cumulative_changed_paths),
        "replan_count": replan_count,
        "replan_events": replan_events,
        "targeted_pdf_second_sync_observed": targeted_pdf_second_sync_observed,
        "legacy_checkpoint_authoritative": True,
        "rollback_performed": False,
        "passes": barrier_passes,
    }

    order = [
        gate_id
        for gate_id in active_plan.ordered_gate_ids
        if gates[gate_id]["mutating"] is False
    ]
    position = {gate_id: index for index, gate_id in enumerate(order)}
    cache_plans = {
        gate_id: _cache_plan_for_gate(
            active_plan,
            manifest,
            gate_id,
            gates[gate_id],
            entries[gate_id],
            cache_context,
            receipt_root=Path(receipt_root),
        )
        for gate_id in order
    }
    cache_lock = threading.Lock()
    pending = set(order)
    completed: set[str] = set(mutator_ids) if barrier_status in {"STABLE", "NOT_APPLICABLE"} else set()
    results: dict[str, dict[str, object]] = {}
    fail_fast = barrier_status not in {"STABLE", "NOT_APPLICABLE"}
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
                    _run_gate_cached,
                    gate_id,
                    gates[gate_id],
                    entries[gate_id],
                    adapters[str(gates[gate_id]["adapter"])],
                    log_directory,
                    position[gate_id],
                    cancellation,
                    cache_plans[gate_id],
                    cache_lock,
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
    if barrier_status not in {"STABLE", "NOT_APPLICABLE"}:
        skip_reason = "mutator_barrier_failed"
    for gate_id in order:
        if gate_id in pending:
            results[gate_id] = _skipped_gate(gate_id, gates[gate_id], entries[gate_id], skip_reason)
    ordered_results: list[dict[str, object]] = []
    for gate_id in active_plan.ordered_gate_ids:
        if gates[gate_id]["mutating"] is True:
            result = mutator_results.get(gate_id)
            if result is None:
                result = _skipped_gate(
                    gate_id,
                    gates[gate_id],
                    entries[gate_id],
                    "mutator_barrier_failed",
                )
            ordered_results.append(result)
        else:
            ordered_results.append(results[gate_id])
    cancelled = cancellation.is_set()
    status, exit_code = _run_status(ordered_results, cancelled)
    counts = {
        "gate_count": len(ordered_results),
        "pass_count": sum(result["status"] in {"PASS", "CACHE_HIT"} for result in ordered_results),
        "executed_pass_count": sum(result["status"] == "PASS" for result in ordered_results),
        "cache_hit_count": sum(result["status"] == "CACHE_HIT" for result in ordered_results),
        "fail_count": sum(result["status"] == "FAIL" for result in ordered_results),
        "warn_count": sum(result["status"] == "WARN" for result in ordered_results),
        "blocked_count": sum(result["status"] == "BLOCKED_CONFIGURATION" for result in ordered_results),
        "skipped_count": sum(str(result["status"]).startswith("SKIP_") for result in ordered_results),
    }
    cache_status_counts = Counter(
        str(result.get("cache_status", "NOT_ELIGIBLE")) for result in ordered_results
    )
    cache_reason_counts = Counter(
        str(result.get("cache_reason", "unspecified")) for result in ordered_results
    )
    cache_write_counts = Counter(
        str(result.get("cache_write_status", "NOT_ATTEMPTED"))
        for result in ordered_results
    )
    cache_summary: dict[str, object] = {
        "mode": cache_context.cache.mode if cache_context is not None else "unconfigured",
        "status_counts": dict(sorted(cache_status_counts.items())),
        "reason_counts": dict(sorted(cache_reason_counts.items())),
        "write_status_counts": dict(sorted(cache_write_counts.items())),
        "adapter_execution_count": sum(
            not str(result["status"]).startswith("SKIP_") and result["status"] != "CACHE_HIT"
            for result in ordered_results
        ),
        "duration_saved_seconds": round(
            sum(float(result.get("duration_saved_seconds", 0.0)) for result in ordered_results),
            6,
        ),
        "reads_disabled": bool(cache_context and cache_context.cache.reads_disabled),
        "diagnostics": (
            list(cache_context.cache.diagnostics[:8]) if cache_context is not None else []
        ),
    }
    receipt: dict[str, object] = {
        "schema_id": "validation_execution_receipt_v1",
        "schema_version": 1,
        "run_id": run_id,
        "plan_hash": plan_hash,
        "final_plan_hash": hashlib.sha256(
            active_plan.canonical_json().encode("utf-8")
        ).hexdigest(),
        "manifest_hash": plan.manifest_hash,
        "execution_authority": "legacy",
        "migration_epoch": "shadow_planner",
        "status": status,
        "exit_code": exit_code,
        "cancelled": cancelled,
        "counts": counts,
        "cache": cache_summary,
        "gate_results": ordered_results,
        "mutator_barrier": barrier_receipt,
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
