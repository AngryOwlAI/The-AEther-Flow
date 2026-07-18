#!/usr/bin/env python3
"""Deterministic file-backed state for the continue-research goal relay.

This module owns local orchestration state only.  It deliberately has no Codex
task API, research-routing, Git mutation, checkpoint, or scientific-completion
authority.  JSON is used inside YAML frontmatter because JSON is a YAML 1.2
subset and preserves the exact goal string without an additional dependency.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Iterator, Mapping, MutableMapping, Optional


LEGACY_SCHEMA_VERSION = "continue-research-goal.v1"
RETAINED_SCHEMA_VERSION = "continue-research-goal.v2"
SCHEMA_VERSION = "continue-research-goal.v3"
SUPPORTED_SCHEMA_VERSIONS = {
    LEGACY_SCHEMA_VERSION,
    RETAINED_SCHEMA_VERSION,
    SCHEMA_VERSION,
}
LEASE_SCHEMA_VERSION = "continue-research-goal-worktree-lease.v1"
EXECUTION_PROFILES = {"acceptance_test", "production_profile"}
WORKER_SKILLS = {"continue-research", "improve-project-system"}
SCOPE_MODES = {"single_objective", "multi_step"}
WORK_ITEM_STATUSES = {
    "completed",
    "in_progress",
    "deferred_human_gate",
    "blocked",
    "repair_completed",
    "no_job",
}

NONTERMINAL_PHASES = {
    "initialized",
    "successor_intent",
    "successor_created",
    "step_active",
    "step_verifying",
    "step_verified",
    "continuation_required",
    "recovery_required",
    "recovery_pending",
}
TERMINAL_PHASES = {
    "terminal_complete",
    "terminal_awaiting_human",
    "terminal_capability_blocked",
    "terminal_guard_exhausted",
    "terminal_no_progress",
    "terminal_validation_failed",
    "terminal_handoff_ambiguous",
    "terminal_handoff_timeout",
    "terminal_duplicate_detected",
    "terminal_corrupt_state",
    "terminal_failed",
    "terminal_cancelled",
}
PHASES = NONTERMINAL_PHASES | TERMINAL_PHASES
RECOVERABLE_TERMINALS = {
    "terminal_awaiting_human",
    "terminal_capability_blocked",
    "terminal_guard_exhausted",
    "terminal_no_progress",
    "terminal_validation_failed",
    "terminal_handoff_ambiguous",
    "terminal_handoff_timeout",
    "terminal_failed",
}
ABSORBING_TERMINALS = TERMINAL_PHASES - RECOVERABLE_TERMINALS
INVOCATION_STATES = {"not_authorized", "authorized", "returned", "unknown"}
HOLDER_KINDS = {"launcher", "continuation", "successor_reserved"}

STOP_PHASES = {
    "goal_met": "terminal_complete",
    "human_gate": "terminal_awaiting_human",
    "indeterminate": "terminal_awaiting_human",
    "capability": "terminal_capability_blocked",
    "pass_limit": "terminal_guard_exhausted",
    "elapsed_limit": "terminal_guard_exhausted",
    "budget_limit": "terminal_guard_exhausted",
    "no_action": "terminal_no_progress",
    "no_progress": "terminal_no_progress",
    "repeated_state": "terminal_no_progress",
    "validation": "terminal_validation_failed",
    "checkpoint": "terminal_validation_failed",
    "dirty_state": "terminal_validation_failed",
    "ambiguous_dispatch": "terminal_handoff_ambiguous",
    "handoff_timeout": "terminal_handoff_timeout",
    "duplicate": "terminal_duplicate_detected",
    "schema": "terminal_corrupt_state",
    "hash": "terminal_corrupt_state",
    "journal": "terminal_corrupt_state",
    "path": "terminal_corrupt_state",
    "symlink": "terminal_corrupt_state",
    "branch": "terminal_failed",
    "repository": "terminal_failed",
    "interrupted": "terminal_failed",
    "execution": "terminal_failed",
    "dispatch_failed": "terminal_failed",
    "cancelled": "terminal_cancelled",
}

GOAL_ID_RE = re.compile(r"^crg-\d{8}T\d{6}Z-[a-f0-9]{8,64}$")
SECRET_PATTERNS = (
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|client[_ -]?secret)\s*[:=]\s*\S+"),
)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


class GoalStateError(RuntimeError):
    """Base class for fail-closed relay-state errors."""


class ValidationError(GoalStateError):
    """The goal record, path, hash, journal, or lease is invalid."""


class StateConflict(GoalStateError):
    """The expected revision, phase, generation, token, or lease is stale."""


class GuardStop(GoalStateError):
    """A fixed execution guard prevents consumption."""


class ActiveRelayError(GoalStateError):
    """Another conforming relay already owns the worktree lease."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValidationError(f"invalid UTC timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"timestamp lacks timezone: {value!r}")
    return parsed.astimezone(dt.timezone.utc)


def canonical_utc(value: str) -> str:
    parsed = parse_utc(value)
    timespec = "microseconds" if parsed.microsecond else "seconds"
    return parsed.isoformat(timespec=timespec).replace("+00:00", "Z")


def add_minutes(value: str, minutes: int) -> str:
    return (parse_utc(value) + dt.timedelta(minutes=minutes)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_goal_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValidationError("goal_text must be a string")
    return value.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def goal_text_sha256(value: str) -> str:
    return sha256_bytes(canonical_goal_text(value).encode("utf-8"))


def canonical_fingerprint(payload: Mapping[str, Any]) -> str:
    """Hash a timestamp-free canonical repository evidence object."""
    if not isinstance(payload, Mapping):
        raise ValidationError("fingerprint payload must be an object")
    return sha256_json(payload)


def fingerprint_status(history: Iterable[str], candidate: str) -> str:
    values = list(history)
    if values and values[-1] == candidate:
        return "unchanged"
    if candidate in values:
        return "repeated"
    return "new"


def map_stop(reason: str) -> str:
    try:
        return STOP_PHASES[reason]
    except KeyError as exc:
        raise ValidationError(f"unregistered stop reason: {reason!r}") from exc


def contains_secret(value: str) -> bool:
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def repository_identity_hash(binding: Mapping[str, Any]) -> str:
    return sha256_json({"root": binding.get("root"), "git_common_dir": binding.get("git_common_dir")})


def _require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ValidationError(f"{field} must be a lowercase SHA-256")
    return value


def _scope_item_map(scope_contract: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    return {
        item["work_item_id"]: item
        for item in scope_contract["included_work_items"]
    }


def validate_scope_contract(scope_contract: Mapping[str, Any]) -> None:
    required = {
        "mode",
        "included_work_items",
        "dependency_source",
        "exclusions",
        "source_hashes",
        "allow_scope_expansion",
    }
    if not isinstance(scope_contract, Mapping) or set(scope_contract) != required:
        raise ValidationError("scope_contract fields are incomplete or unexpected")
    if scope_contract["mode"] not in SCOPE_MODES:
        raise ValidationError("scope_contract mode is invalid")
    if scope_contract["allow_scope_expansion"] is not False:
        raise ValidationError("scope_contract must prohibit scope expansion")
    exclusions = scope_contract["exclusions"]
    if (
        not isinstance(exclusions, list)
        or not exclusions
        or any(not isinstance(item, str) or not item for item in exclusions)
    ):
        raise ValidationError("scope_contract exclusions must be a nonempty string list")
    source_hashes = scope_contract["source_hashes"]
    if (
        not isinstance(source_hashes, Mapping)
        or not source_hashes
        or any(not isinstance(path, str) or not path for path in source_hashes)
    ):
        raise ValidationError("scope_contract source_hashes must be a nonempty path-to-hash object")
    for path, digest in source_hashes.items():
        _require_sha256(digest, f"scope_contract source hash for {path}")

    items = scope_contract["included_work_items"]
    if not isinstance(items, list) or not items:
        raise ValidationError("scope_contract must include at least one work item")
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, Mapping) or set(item) != {"work_item_id", "objective", "depends_on"}:
            raise ValidationError("scope work items require work_item_id, objective, and depends_on")
        work_item_id = item["work_item_id"]
        if not isinstance(work_item_id, str) or not work_item_id or work_item_id in seen:
            raise ValidationError("scope work-item IDs must be unique nonblank strings")
        seen.add(work_item_id)
        if not isinstance(item["objective"], str) or not item["objective"]:
            raise ValidationError("scope work-item objectives must be nonblank")
        dependencies = item["depends_on"]
        if (
            not isinstance(dependencies, list)
            or len(dependencies) != len(set(dependencies))
            or any(not isinstance(value, str) or not value for value in dependencies)
        ):
            raise ValidationError("scope work-item dependencies must be unique string lists")
    item_map = _scope_item_map(scope_contract)
    for work_item_id, item in item_map.items():
        for dependency in item["depends_on"]:
            if dependency not in item_map or dependency == work_item_id:
                raise ValidationError("scope work-item dependency is dangling or self-referential")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(work_item_id: str) -> None:
        if work_item_id in visiting:
            raise ValidationError("scope work-item dependency graph is cyclic")
        if work_item_id in visited:
            return
        visiting.add(work_item_id)
        for dependency in item_map[work_item_id]["depends_on"]:
            visit(dependency)
        visiting.remove(work_item_id)
        visited.add(work_item_id)

    for work_item_id in item_map:
        visit(work_item_id)

    dependency_source = scope_contract["dependency_source"]
    if scope_contract["mode"] == "single_objective":
        if len(items) != 1 or items[0]["depends_on"]:
            raise ValidationError("single_objective scope requires exactly one dependency-free item")
        if dependency_source is not None:
            raise ValidationError("single_objective scope must use a null dependency_source")
    else:
        if not isinstance(dependency_source, Mapping) or set(dependency_source) != {"path", "sha256"}:
            raise ValidationError("multi_step scope requires an exact dependency source")
        if not isinstance(dependency_source["path"], str) or not dependency_source["path"]:
            raise ValidationError("scope dependency-source path must be nonblank")
        _require_sha256(dependency_source["sha256"], "scope dependency-source hash")
        if source_hashes.get(dependency_source["path"]) != dependency_source["sha256"]:
            raise ValidationError("scope dependency source must match source_hashes")


def validate_dirty_state_manifest(manifest: Mapping[str, Any]) -> None:
    required = {
        "owning_task_id",
        "owning_agent_job_id",
        "head",
        "porcelain",
        "changed_paths",
        "failed_gates",
    }
    if not isinstance(manifest, Mapping) or set(manifest) != required:
        raise ValidationError("dirty-state manifest fields are incomplete or unexpected")
    for field in ("owning_task_id", "owning_agent_job_id", "head"):
        if not isinstance(manifest[field], str) or not manifest[field]:
            raise ValidationError(f"dirty-state manifest {field} must be nonblank")
    if not isinstance(manifest["porcelain"], str):
        raise ValidationError("dirty-state manifest porcelain must be a string")
    changed_paths = manifest["changed_paths"]
    if not isinstance(changed_paths, list):
        raise ValidationError("dirty-state manifest changed_paths must be a list")
    seen_paths: set[str] = set()
    for item in changed_paths:
        if not isinstance(item, Mapping) or set(item) != {"path", "sha256"}:
            raise ValidationError("dirty-state changed paths require path and sha256")
        if not isinstance(item["path"], str) or not item["path"] or item["path"] in seen_paths:
            raise ValidationError("dirty-state changed paths must be unique and nonblank")
        seen_paths.add(item["path"])
        _require_sha256(item["sha256"], f"dirty-state hash for {item['path']}")
    failed_gates = manifest["failed_gates"]
    if not isinstance(failed_gates, list) or not failed_gates:
        raise ValidationError("dirty-state manifest requires at least one failed gate")
    seen_gates: set[str] = set()
    for item in failed_gates:
        if not isinstance(item, Mapping) or set(item) != {"gate_id", "status", "evidence_sha256"}:
            raise ValidationError("dirty-state failed gates require gate_id, status, and evidence_sha256")
        if (
            not isinstance(item["gate_id"], str)
            or not item["gate_id"]
            or item["gate_id"] in seen_gates
            or not isinstance(item["status"], str)
            or not item["status"]
        ):
            raise ValidationError("dirty-state failed gates must be unique and nonblank")
        seen_gates.add(item["gate_id"])
        _require_sha256(item["evidence_sha256"], f"dirty-state evidence for {item['gate_id']}")


def validate_route(route: Mapping[str, Any], scope_contract: Mapping[str, Any]) -> None:
    required = {
        "worker_skill",
        "reason_id",
        "strategy_id",
        "source_generation",
        "work_item_id",
        "blocker_fingerprint",
        "evidence_hashes",
        "dirty_state_manifest",
    }
    if not isinstance(route, Mapping) or set(route) != required:
        raise ValidationError("generation route fields are incomplete or unexpected")
    if route["worker_skill"] not in WORKER_SKILLS:
        raise ValidationError("generation route worker_skill is invalid")
    for field in ("reason_id", "strategy_id", "work_item_id"):
        if not isinstance(route[field], str) or not route[field]:
            raise ValidationError(f"generation route {field} must be nonblank")
    if route["work_item_id"] not in _scope_item_map(scope_contract):
        raise ValidationError("generation route broadens beyond scope_contract")
    if (
        isinstance(route["source_generation"], bool)
        or not isinstance(route["source_generation"], int)
        or route["source_generation"] < 0
    ):
        raise ValidationError("generation route source_generation must be nonnegative")
    _require_sha256(route["blocker_fingerprint"], "generation route blocker_fingerprint")
    evidence_hashes = route["evidence_hashes"]
    if (
        not isinstance(evidence_hashes, list)
        or not evidence_hashes
        or len(evidence_hashes) != len(set(evidence_hashes))
    ):
        raise ValidationError("generation route evidence_hashes must be a unique nonempty list")
    for digest in evidence_hashes:
        _require_sha256(digest, "generation route evidence hash")
    manifest = route["dirty_state_manifest"]
    if route["worker_skill"] == "improve-project-system":
        if not isinstance(manifest, Mapping):
            raise ValidationError("project-system repair route requires a dirty-state manifest")
        validate_dirty_state_manifest(manifest)
    elif manifest is not None:
        raise ValidationError("continue-research route cannot carry a dirty-state manifest")


def build_route(
    *,
    worker_skill: str,
    reason_id: str,
    strategy_id: str,
    source_generation: int,
    work_item_id: str,
    blocker_fingerprint: str,
    evidence_hashes: Iterable[str],
    dirty_state_manifest: Optional[Mapping[str, Any]] = None,
    scope_contract: Mapping[str, Any],
) -> Dict[str, Any]:
    route = {
        "worker_skill": worker_skill,
        "reason_id": reason_id,
        "strategy_id": strategy_id,
        "source_generation": source_generation,
        "work_item_id": work_item_id,
        "blocker_fingerprint": blocker_fingerprint,
        "evidence_hashes": sorted(set(evidence_hashes)),
        "dirty_state_manifest": (
            copy.deepcopy(dict(dirty_state_manifest))
            if dirty_state_manifest is not None
            else None
        ),
    }
    validate_route(route, scope_contract)
    return route


def validate_human_intervention(value: Mapping[str, Any], recovery_ledger: Iterable[Mapping[str, Any]]) -> None:
    required = {
        "required_action",
        "reason",
        "blocking_evidence_hashes",
        "safe_authorized_strategies_exhausted",
        "attempted_strategy_ids",
        "remaining_safe_authorized_strategy_ids",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValidationError("human-intervention fields are incomplete or unexpected")
    for field in ("required_action", "reason"):
        if not isinstance(value[field], str) or not value[field]:
            raise ValidationError(f"human-intervention {field} must be nonblank")
    hashes = value["blocking_evidence_hashes"]
    if not isinstance(hashes, list) or not hashes or len(hashes) != len(set(hashes)):
        raise ValidationError("human-intervention evidence hashes must be unique and nonempty")
    for digest in hashes:
        _require_sha256(digest, "human-intervention evidence hash")
    if value["safe_authorized_strategies_exhausted"] is not True:
        raise ValidationError("non-success terminal requires exhausted safe authorized strategies")
    attempted = value["attempted_strategy_ids"]
    remaining = value["remaining_safe_authorized_strategy_ids"]
    if (
        not isinstance(attempted, list)
        or len(attempted) != len(set(attempted))
        or any(not isinstance(item, str) or not item for item in attempted)
        or remaining != []
    ):
        raise ValidationError("human intervention must name attempted strategies and no safe remaining strategy")
    ledger_ids = [entry["strategy_id"] for entry in recovery_ledger]
    if set(attempted) != set(ledger_ids):
        raise ValidationError("human-intervention attempted strategies do not match the recovery ledger")


def validate_work_result(value: Mapping[str, Any], scope_contract: Mapping[str, Any]) -> None:
    required = {
        "work_item_id",
        "work_item_status",
        "task_id",
        "agent_job_id",
        "completion_path",
        "completion_sha256",
        "checkpoint_commit",
        "validator_results",
        "progress_summary",
        "zero_job_reason",
        "out_of_scope_remaining_work",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValidationError("v3 work_result fields are incomplete or unexpected")
    if value["work_item_id"] not in _scope_item_map(scope_contract):
        raise ValidationError("work_result references an out-of-scope work item")
    if value["work_item_status"] not in WORK_ITEM_STATUSES:
        raise ValidationError("work_result status is invalid")
    if not isinstance(value["progress_summary"], str) or not value["progress_summary"]:
        raise ValidationError("work_result progress_summary must be nonblank")
    if not isinstance(value["validator_results"], list):
        raise ValidationError("work_result validator_results must be a list")
    if (
        not isinstance(value["out_of_scope_remaining_work"], list)
        or any(not isinstance(item, str) or not item for item in value["out_of_scope_remaining_work"])
    ):
        raise ValidationError("work_result out_of_scope_remaining_work must be a string list")
    agent_job_id = value["agent_job_id"]
    if agent_job_id is None:
        if not isinstance(value["zero_job_reason"], str) or not value["zero_job_reason"]:
            raise ValidationError("work_result without an AgentJob requires zero_job_reason")
        for field in ("completion_path", "completion_sha256"):
            if value[field] is not None:
                raise ValidationError("zero-AgentJob work_result cannot name a completion")
    else:
        for field in ("task_id", "agent_job_id", "completion_path"):
            if not isinstance(value[field], str) or not value[field]:
                raise ValidationError(f"AgentJob work_result {field} must be nonblank")
        _require_sha256(value["completion_sha256"], "work_result completion hash")
        if value["zero_job_reason"] is not None:
            raise ValidationError("AgentJob work_result cannot use zero_job_reason")
    if value["checkpoint_commit"] is not None and (
        not isinstance(value["checkpoint_commit"], str) or not value["checkpoint_commit"]
    ):
        raise ValidationError("work_result checkpoint_commit must be null or nonblank")


def _finalized_receipts(record: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        entry["payload"]
        for entry in record.get("journal", [])
        if entry.get("kind") == "step_receipt"
    ]


def _completion_summary(record: Mapping[str, Any]) -> Dict[str, Any]:
    receipts = copy.deepcopy(_finalized_receipts(record))
    work_results = [receipt["work_result"] for receipt in receipts]
    final_work = work_results[-1] if work_results else None
    evidence = {
        "task_ids": sorted({item["task_id"] for item in work_results if item["task_id"]}),
        "agent_job_ids": sorted({item["agent_job_id"] for item in work_results if item["agent_job_id"]}),
        "completions": sorted(
            [
                {"path": item["completion_path"], "sha256": item["completion_sha256"]}
                for item in work_results
                if item["completion_path"]
            ],
            key=lambda item: (item["path"], item["sha256"]),
        ),
        "checkpoint_commits": sorted(
            {item["checkpoint_commit"] for item in work_results if item["checkpoint_commit"]}
        ),
        "validator_results": [
            item
            for work in work_results
            for item in work["validator_results"]
        ],
    }
    completed_lines = [
        f"Generation {receipt['generation']}: {receipt['work_result']['progress_summary']}"
        for receipt in receipts
    ]
    outside = final_work["out_of_scope_remaining_work"] if final_work else []
    report_lines = [
        "Goal reached.",
        f"Exact original goal: {json.dumps(record['goal_text'], ensure_ascii=False)}",
        "Completed across generations: " + ("; ".join(completed_lines) if completed_lines else "no worker frame"),
        "Supporting evidence: "
        + json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        "Outside the goal: " + ("; ".join(outside) if outside else "none"),
        "That goal was reached.",
    ]
    return {
        "status_line": "Goal reached.",
        "exact_original_goal": record["goal_text"],
        "effective_completion_contract": copy.deepcopy(effective_completion_contract(record)),
        "finalized_generation_receipts": receipts,
        "work_results": work_results,
        "supporting_evidence": evidence,
        "final_fingerprint": record["state"]["last_canonical_fingerprint"],
        "out_of_scope_remaining_work": outside,
        "closing_statement": "That goal was reached.",
        "reader_report": "\n".join(report_lines),
    }


def _human_intervention_summary(record: Mapping[str, Any]) -> Dict[str, Any]:
    receipts = copy.deepcopy(_finalized_receipts(record))
    intervention = copy.deepcopy(record["state"]["human_intervention"])
    completed_lines = [
        f"Generation {receipt['generation']}: {receipt['work_result']['progress_summary']}"
        for receipt in receipts
    ]
    attempted = [entry["strategy_id"] for entry in record["recovery_ledger"]]
    report_lines = [
        "Goal not reached — human action required",
        f"Exact original goal: {json.dumps(record['goal_text'], ensure_ascii=False)}",
        "Completed work: " + ("; ".join(completed_lines) if completed_lines else "none"),
        "Attempted recovery strategies: " + (", ".join(attempted) if attempted else "none applicable"),
        f"Required human action: {intervention['required_action']}",
    ]
    return {
        "status_line": "Goal not reached — human action required",
        "exact_original_goal": record["goal_text"],
        "completed_work": [receipt["work_result"] for receipt in receipts],
        "attempted_recovery_strategies": attempted,
        "human_intervention": intervention,
        "reader_report": "\n".join(report_lines),
    }


def _journal_entry(kind: str, payload: Mapping[str, Any], prior_hash: Optional[str], sequence: int) -> Dict[str, Any]:
    core = {
        "kind": kind,
        "payload": copy.deepcopy(dict(payload)),
        "prior_hash": prior_hash,
        "sequence": sequence,
    }
    core["entry_hash"] = sha256_json(core)
    return core


def append_journal(record: MutableMapping[str, Any], kind: str, payload: Mapping[str, Any]) -> str:
    journal = record.setdefault("journal", [])
    prior = journal[-1]["entry_hash"] if journal else None
    entry = _journal_entry(kind, payload, prior, len(journal) + 1)
    journal.append(entry)
    return entry["entry_hash"]


def effective_completion_contract(record: Mapping[str, Any]) -> Mapping[str, Any]:
    value: Mapping[str, Any] = record["completion_contract"]
    for amendment in record.get("amendments", []):
        if amendment.get("kind") == "completion_contract":
            value = amendment["new_value"]
    return value


def _initial_effective_guards(record: Mapping[str, Any]) -> Dict[str, Any]:
    value = copy.deepcopy(record["guards"])
    if record.get("schema_version") in {RETAINED_SCHEMA_VERSION, SCHEMA_VERSION}:
        value["deadline_at"] = record["deadline_at"]
    return value


def effective_guards(record: Mapping[str, Any]) -> Dict[str, Any]:
    value = _initial_effective_guards(record)
    for amendment in record.get("amendments", []):
        if amendment.get("kind") == "guards":
            value.update(copy.deepcopy(amendment["new_value"]))
    return value


def _validate_v2_guard_extension(
    prior_value: Mapping[str, Any],
    new_value: Mapping[str, Any],
    *,
    created_at: str,
    require_canonical_deadline: bool,
) -> Dict[str, Any]:
    allowed = {"max_continue_passes", "deadline_at"}
    if not isinstance(new_value, Mapping) or not new_value or not set(new_value) <= allowed:
        raise ValidationError("guard amendment may change only max_continue_passes or deadline_at")

    normalized = copy.deepcopy(dict(new_value))
    if "max_continue_passes" in normalized:
        prior_passes = prior_value["max_continue_passes"]
        proposed_passes = normalized["max_continue_passes"]
        if proposed_passes is None:
            if prior_passes is None:
                raise ValidationError("unlimited max_continue_passes cannot be amended")
        elif isinstance(proposed_passes, bool) or not isinstance(proposed_passes, int) or proposed_passes <= 0:
            raise ValidationError("max_continue_passes must be a positive integer or null")
        elif prior_passes is None or proposed_passes <= prior_passes:
            raise ValidationError("max_continue_passes may only extend a finite limit or become unlimited")

    if "deadline_at" in normalized:
        prior_deadline = prior_value["deadline_at"]
        proposed_deadline = normalized["deadline_at"]
        if proposed_deadline is None:
            if prior_deadline is None:
                raise ValidationError("unlimited deadline_at cannot be amended")
        else:
            canonical_deadline = canonical_utc(proposed_deadline)
            if require_canonical_deadline and canonical_deadline != proposed_deadline:
                raise ValidationError("deadline_at must use canonical UTC Z form")
            if parse_utc(canonical_deadline) <= parse_utc(created_at):
                raise ValidationError("deadline_at must be in the future")
            if prior_deadline is None or parse_utc(canonical_deadline) <= parse_utc(prior_deadline):
                raise ValidationError("deadline_at may only extend a finite limit or become unlimited")
            normalized["deadline_at"] = canonical_deadline
    return normalized


def render_goal(record: Mapping[str, Any]) -> str:
    frontmatter = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2)
    contract = json.dumps(effective_completion_contract(record), ensure_ascii=False, sort_keys=True, indent=2)
    lines = [
        "---",
        frontmatter,
        "---",
        "",
        "# Goal relay record",
        "",
        "## Completion contract",
        "",
        "```json",
        contract,
        "```",
        "",
        "## Step journal",
        "",
    ]
    if not record.get("journal"):
        lines.append("_No journal entries._")
    else:
        for entry in record["journal"]:
            lines.extend(
                [
                    f"### {entry['sequence']}. {entry['kind']}",
                    "",
                    f"- Prior hash: `{entry['prior_hash'] or 'GENESIS'}`",
                    f"- Entry hash: `{entry['entry_hash']}`",
                    "",
                    "```json",
                    json.dumps(entry["payload"], ensure_ascii=False, sort_keys=True, indent=2),
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def parse_goal_text(text: str) -> tuple[Dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValidationError("goal file lacks YAML frontmatter opener")
    frontmatter, separator, body = text[4:].partition("\n---\n")
    if not separator:
        raise ValidationError("goal file lacks YAML frontmatter closer")
    try:
        record = json.loads(frontmatter)
    except json.JSONDecodeError as exc:
        raise ValidationError("goal frontmatter is not valid JSON/YAML") from exc
    if not isinstance(record, dict):
        raise ValidationError("goal frontmatter must be an object")
    return record, body


def validate_record(record: Mapping[str, Any], expected_path: Optional[Path] = None, rendered_text: Optional[str] = None) -> None:
    required = {
        "schema_version",
        "goal_id",
        "goal_text",
        "goal_sha256",
        "completion_contract",
        "completion_contract_sha256",
        "amendments",
        "created_at",
        "deadline_at",
        "guards",
        "repository_binding",
        "authorization",
        "state",
        "generations",
        "handoff",
        "journal",
        "updated_at",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ValidationError(f"goal record missing fields: {', '.join(missing)}")
    schema_version = record["schema_version"]
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValidationError("unsupported goal schema version")
    if schema_version == SCHEMA_VERSION:
        v3_required = {
            "scope_contract",
            "scope_contract_sha256",
            "recovery_ledger",
            "completion_summary",
            "completion_summary_sha256",
            "human_intervention_summary",
            "human_intervention_summary_sha256",
        }
        v3_missing = sorted(v3_required - set(record))
        if v3_missing:
            raise ValidationError(f"v3 goal record missing fields: {', '.join(v3_missing)}")
        validate_scope_contract(record["scope_contract"])
        if sha256_json(record["scope_contract"]) != record["scope_contract_sha256"]:
            raise ValidationError("scope-contract hash mismatch")
    if not GOAL_ID_RE.fullmatch(str(record["goal_id"])):
        raise ValidationError("invalid goal_id")
    if expected_path is not None and expected_path.name != f"goal-{record['goal_id']}.md":
        raise ValidationError("goal filename does not match embedded goal_id")
    if record["goal_text"] != canonical_goal_text(record["goal_text"]):
        raise ValidationError("goal text contains noncanonical line endings")
    if goal_text_sha256(record["goal_text"]) != record["goal_sha256"]:
        raise ValidationError("goal text hash mismatch")
    if sha256_json(record["completion_contract"]) != record["completion_contract_sha256"]:
        raise ValidationError("original completion-contract hash mismatch")
    created_at = parse_utc(record["created_at"])
    parse_utc(record["updated_at"])
    deadline_at = record["deadline_at"]
    if schema_version == LEGACY_SCHEMA_VERSION:
        if parse_utc(deadline_at) <= created_at:
            raise ValidationError("deadline must be after creation")
    elif deadline_at is not None:
        if canonical_utc(deadline_at) != deadline_at:
            raise ValidationError("deadline_at must use canonical UTC Z form")
        if parse_utc(deadline_at) <= created_at:
            raise ValidationError("deadline must be after creation")

    guards = record["guards"]
    max_continue_passes = guards.get("max_continue_passes")
    if schema_version == LEGACY_SCHEMA_VERSION:
        if not isinstance(max_continue_passes, int) or max_continue_passes <= 0:
            raise ValidationError("guard max_continue_passes must be a positive integer")
    elif max_continue_passes is not None and (
        isinstance(max_continue_passes, bool)
        or not isinstance(max_continue_passes, int)
        or max_continue_passes <= 0
    ):
        raise ValidationError("guard max_continue_passes must be a positive integer or null")
    for key in ("max_repeated_state_fingerprints", "max_live_continuations", "handoff_ready_timeout_seconds"):
        if not isinstance(guards.get(key), int) or guards[key] <= 0:
            raise ValidationError(f"guard {key} must be a positive integer")
    if schema_version == SCHEMA_VERSION:
        for key in (
            "stop_on_human_gate",
            "stop_on_validation_failure",
            "stop_on_checkpoint_failure",
            "stop_on_unexpected_dirty_state",
            "stop_on_no_progress",
            "stop_on_repeated_state",
            "stop_on_capability_loss",
            "stop_on_branch_or_repository_mismatch",
        ):
            if guards.get(key) is not True:
                raise ValidationError(f"v3 fixed guard {key} must remain true")
    binding = record["repository_binding"]
    for key in ("execution_profile", "root", "branch", "environment_mode", "git_common_dir", "starting_head"):
        if not isinstance(binding.get(key), str) or not binding[key]:
            raise ValidationError(f"repository binding field {key} must be nonblank")
    if binding["execution_profile"] not in EXECUTION_PROFILES:
        raise ValidationError("unsupported repository execution profile")
    if binding["environment_mode"] != "local":
        raise ValidationError("only local environment mode is supported")
    if binding["branch"] == "main":
        raise ValidationError("main is not an authorized relay branch")

    if schema_version == SCHEMA_VERSION:
        ledger = record["recovery_ledger"]
        if not isinstance(ledger, list):
            raise ValidationError("recovery_ledger must be a list")
        seen_strategy_pairs: set[tuple[str, str]] = set()
        for index, recovery in enumerate(ledger, start=1):
            required_recovery = {
                "sequence",
                "strategy_id",
                "blocker_fingerprint",
                "route",
                "route_sha256",
                "approved_for_generation",
                "approved_at",
            }
            if not isinstance(recovery, Mapping) or set(recovery) != required_recovery:
                raise ValidationError("recovery-ledger entry fields are incomplete or unexpected")
            if recovery["sequence"] != index:
                raise ValidationError("recovery-ledger sequence is invalid")
            validate_route(recovery["route"], record["scope_contract"])
            if sha256_json(recovery["route"]) != recovery["route_sha256"]:
                raise ValidationError("recovery-ledger route hash mismatch")
            if (
                recovery["strategy_id"] != recovery["route"]["strategy_id"]
                or recovery["blocker_fingerprint"] != recovery["route"]["blocker_fingerprint"]
            ):
                raise ValidationError("recovery-ledger route identity mismatch")
            pair = (recovery["blocker_fingerprint"], recovery["strategy_id"])
            if pair in seen_strategy_pairs:
                raise ValidationError("recovery strategy repeats for the same blocker fingerprint")
            seen_strategy_pairs.add(pair)
            if (
                isinstance(recovery["approved_for_generation"], bool)
                or not isinstance(recovery["approved_for_generation"], int)
                or recovery["approved_for_generation"] <= recovery["route"]["source_generation"]
            ):
                raise ValidationError("recovery-ledger target generation is invalid")
            parse_utc(recovery["approved_at"])

    state = record["state"]
    if state.get("phase") not in PHASES:
        raise ValidationError("invalid phase")
    if not isinstance(state.get("revision"), int) or state["revision"] < 1:
        raise ValidationError("revision must be a positive integer")
    if not isinstance(state.get("current_generation"), int) or state["current_generation"] < 0:
        raise ValidationError("current_generation must be nonnegative")
    if not isinstance(state.get("passes_consumed"), int) or state["passes_consumed"] < 0:
        raise ValidationError("passes_consumed must be nonnegative")
    if state.get("goal_evaluation") not in {"unmet", "met", "indeterminate"}:
        raise ValidationError("invalid goal evaluation")
    if state["phase"] in ABSORBING_TERMINALS and state.get("active_lease") is not None:
        raise ValidationError("absorbing terminal phase cannot retain a lease")
    if schema_version == SCHEMA_VERSION:
        for key in ("approved_route", "approved_route_sha256", "human_intervention"):
            if key not in state:
                raise ValidationError(f"v3 state missing {key}")
        approved_route = state["approved_route"]
        approved_route_sha256 = state["approved_route_sha256"]
        if approved_route is None:
            if approved_route_sha256 is not None:
                raise ValidationError("null approved route cannot retain a hash")
        else:
            validate_route(approved_route, record["scope_contract"])
            if sha256_json(approved_route) != approved_route_sha256:
                raise ValidationError("approved-route hash mismatch")
        if state["phase"] == "terminal_complete":
            if state["human_intervention"] is not None:
                raise ValidationError("successful terminal cannot require human intervention")
        elif state["phase"] in TERMINAL_PHASES:
            validate_human_intervention(state["human_intervention"], record["recovery_ledger"])
        elif state["human_intervention"] is not None:
            raise ValidationError("nonterminal v3 state cannot retain human intervention")

    expected_prior = None
    seen_receipts: Dict[int, str] = {}
    recovery_events: Dict[int, Mapping[str, Any]] = {}
    for index, entry in enumerate(record["journal"], start=1):
        if entry.get("sequence") != index or entry.get("prior_hash") != expected_prior:
            raise ValidationError("journal sequence or prior hash mismatch")
        core = {key: entry[key] for key in ("kind", "payload", "prior_hash", "sequence")}
        expected_hash = sha256_json(core)
        if entry.get("entry_hash") != expected_hash:
            raise ValidationError("journal entry hash mismatch")
        expected_prior = expected_hash
        if entry["kind"] == "step_receipt":
            generation = entry["payload"].get("generation")
            if not isinstance(generation, int) or generation in seen_receipts:
                raise ValidationError("generation has duplicate or invalid finalized receipt")
            if schema_version == SCHEMA_VERSION:
                validate_work_result(entry["payload"].get("work_result"), record["scope_contract"])
            seen_receipts[generation] = expected_hash
        if entry["kind"] in {"recovery_required", "dispatch_recovery_required"}:
            recovery_sequence = entry["payload"].get("recovery_sequence")
            if not isinstance(recovery_sequence, int) or recovery_sequence in recovery_events:
                raise ValidationError("recovery journal sequence is duplicate or invalid")
            recovery_events[recovery_sequence] = entry["payload"]

    if schema_version == SCHEMA_VERSION:
        if set(recovery_events) != set(range(1, len(record["recovery_ledger"]) + 1)):
            raise ValidationError("recovery ledger is not fully linked to the journal")
        for recovery in record["recovery_ledger"]:
            event = recovery_events[recovery["sequence"]]
            if event.get("approved_route_sha256") != recovery["route_sha256"]:
                raise ValidationError("recovery ledger route differs from journal authority")
            if "strategy_id" in event and event["strategy_id"] != recovery["strategy_id"]:
                raise ValidationError("recovery ledger strategy differs from journal authority")
            if (
                "blocker_fingerprint" in event
                and event["blocker_fingerprint"] != recovery["blocker_fingerprint"]
            ):
                raise ValidationError("recovery ledger blocker differs from journal authority")

    generations = record["generations"]
    if not isinstance(generations, dict):
        raise ValidationError("generations must be an object")
    for key, generation in generations.items():
        try:
            number = int(key)
        except ValueError as exc:
            raise ValidationError("generation keys must be decimal integers") from exc
        if number <= 0 or generation.get("generation") != number:
            raise ValidationError("generation key and payload mismatch")
        if generation.get("invocation_state") not in INVOCATION_STATES:
            raise ValidationError("invalid invocation state")
        if not isinstance(generation.get("invocation_consumed"), bool):
            raise ValidationError("invocation_consumed must be Boolean")
        receipt_hash = generation.get("finalized_receipt_hash")
        if receipt_hash is not None and seen_receipts.get(number) != receipt_hash:
            raise ValidationError("finalized receipt hash does not match journal")
        if receipt_hash is None and number in seen_receipts:
            raise ValidationError("journal receipt is not linked from its generation")
        if schema_version == SCHEMA_VERSION:
            route = generation.get("route")
            route_sha256 = generation.get("route_sha256")
            validate_route(route, record["scope_contract"])
            if sha256_json(route) != route_sha256:
                raise ValidationError("generation route hash mismatch")
            if route["source_generation"] >= number:
                raise ValidationError("generation route source must precede its generation")

    if schema_version == SCHEMA_VERSION:
        for recovery in record["recovery_ledger"]:
            target = str(recovery["approved_for_generation"])
            if target in generations:
                if generations[target]["route_sha256"] != recovery["route_sha256"]:
                    raise ValidationError("reserved recovery generation differs from approved ledger route")
            elif state.get("approved_route_sha256") != recovery["route_sha256"]:
                raise ValidationError("unreserved recovery route is not the active approved route")

    effective_contract = record["completion_contract"]
    effective_guard_values = _initial_effective_guards(record)
    for amendment in record["amendments"]:
        if amendment.get("kind") == "completion_contract":
            prior = sha256_json(effective_contract)
            effective_contract = amendment.get("new_value")
        elif amendment.get("kind") == "guards":
            prior = sha256_json(effective_guard_values)
            new_guard_values = amendment.get("new_value", {})
            if schema_version in {RETAINED_SCHEMA_VERSION, SCHEMA_VERSION}:
                new_guard_values = _validate_v2_guard_extension(
                    effective_guard_values,
                    new_guard_values,
                    created_at=amendment.get("created_at"),
                    require_canonical_deadline=True,
                )
            effective_guard_values.update(new_guard_values)
        else:
            raise ValidationError("invalid amendment kind")
        if amendment.get("prior_effective_sha256") != prior:
            raise ValidationError("amendment prior hash mismatch")
        if amendment.get("new_sha256") != sha256_json(effective_contract if amendment["kind"] == "completion_contract" else effective_guard_values):
            raise ValidationError("amendment new hash mismatch")
        if not amendment.get("user_authorization"):
            raise ValidationError("amendment lacks exact user authorization")
        parse_utc(amendment.get("created_at"))

    if schema_version == SCHEMA_VERSION:
        completion_summary = record["completion_summary"]
        completion_summary_sha256 = record["completion_summary_sha256"]
        human_summary = record["human_intervention_summary"]
        human_summary_sha256 = record["human_intervention_summary_sha256"]
        if state["phase"] == "terminal_complete":
            expected_summary = _completion_summary(record)
            if completion_summary != expected_summary:
                raise ValidationError("terminal completion summary is absent or nondeterministic")
            if completion_summary_sha256 != sha256_json(completion_summary):
                raise ValidationError("terminal completion-summary hash mismatch")
            if human_summary is not None or human_summary_sha256 is not None:
                raise ValidationError("successful terminal cannot retain a human-intervention summary")
        elif state["phase"] in TERMINAL_PHASES:
            expected_human_summary = _human_intervention_summary(record)
            if human_summary != expected_human_summary:
                raise ValidationError("human-intervention summary is absent or nondeterministic")
            if human_summary_sha256 != sha256_json(human_summary):
                raise ValidationError("human-intervention-summary hash mismatch")
            if completion_summary is not None or completion_summary_sha256 is not None:
                raise ValidationError("non-success terminal cannot retain a completion summary")
        elif any(
            value is not None
            for value in (
                completion_summary,
                completion_summary_sha256,
                human_summary,
                human_summary_sha256,
            )
        ):
            raise ValidationError("nonterminal v3 record cannot retain a terminal summary")

    if rendered_text is not None and render_goal(record) != rendered_text:
        raise ValidationError("Markdown body or serialization drift detected")


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _exclusive_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
    _fsync_dir(path.parent)


def _atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(f"{path.name}.{secrets.token_hex(8)}.tmp")
    _exclusive_write(tmp, data)
    os.replace(tmp, path)
    _fsync_dir(path.parent)


@contextmanager
def _file_lock(path: Path) -> Iterator[None]:
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


class GoalStore:
    """Atomic state-machine operations for one goals directory."""

    def __init__(self, goals_dir: os.PathLike[str] | str):
        self.goals_dir = Path(goals_dir).absolute()
        self.goals_dir.mkdir(parents=True, exist_ok=True)
        if self.goals_dir.is_symlink():
            raise ValidationError("goals directory may not be a symlink")
        self.goals_dir_resolved = self.goals_dir.resolve()
        self.global_lease_path = self.goals_dir / ".relay-lease.json"
        self.global_lock_path = self.goals_dir / ".relay-lease.lock"

    def _validate_path(self, value: os.PathLike[str] | str, must_exist: bool = True) -> Path:
        path = Path(value).absolute()
        if path.parent.resolve() != self.goals_dir_resolved:
            raise ValidationError("goal path escapes the configured goals directory")
        if not path.name.startswith("goal-") or path.suffix != ".md":
            raise ValidationError("goal path must match goal-*.md")
        if must_exist:
            try:
                stat = path.lstat()
            except FileNotFoundError as exc:
                raise ValidationError("goal file does not exist") from exc
            if path.is_symlink() or not os.path.isfile(path):
                raise ValidationError("goal path must be a regular non-symlink file")
            if stat.st_nlink != 1:
                raise ValidationError("goal file must have exactly one hard link")
        return path

    def _goal_lock_path(self, goal_path: Path) -> Path:
        return goal_path.with_suffix(".lock")

    @contextmanager
    def _locks(self, goal_path: Optional[Path] = None) -> Iterator[None]:
        with _file_lock(self.global_lock_path):
            if goal_path is None:
                yield
            else:
                with _file_lock(self._goal_lock_path(goal_path)):
                    yield

    def _read_global(self) -> Optional[Dict[str, Any]]:
        if not self.global_lease_path.exists():
            return None
        if self.global_lease_path.is_symlink():
            raise ValidationError("global lease may not be a symlink")
        try:
            value = json.loads(self.global_lease_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValidationError("global lease is unreadable or corrupt") from exc
        required = {
            "schema_version",
            "repository_fingerprint",
            "goal_id",
            "generation",
            "holder_kind",
            "holder_token",
            "transaction_id",
            "acquired_at",
            "heartbeat_at",
            "expires_at",
        }
        if not isinstance(value, dict) or not required <= set(value):
            raise ValidationError("global lease schema is incomplete")
        if value["schema_version"] != LEASE_SCHEMA_VERSION or value["holder_kind"] not in HOLDER_KINDS:
            raise ValidationError("global lease schema or holder kind is invalid")
        for key in ("acquired_at", "heartbeat_at", "expires_at"):
            parse_utc(value[key])
        return value

    def _write_global(self, lease: Mapping[str, Any]) -> None:
        _atomic_write(self.global_lease_path, canonical_json_bytes(lease) + b"\n")

    def _remove_global(self) -> None:
        try:
            self.global_lease_path.unlink()
        except FileNotFoundError:
            return
        _fsync_dir(self.goals_dir)

    def read(self, goal_path: os.PathLike[str] | str, require_lease_parity: bool = False) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        text = path.read_text(encoding="utf-8")
        record, _ = parse_goal_text(text)
        validate_record(record, path, text)
        if require_lease_parity:
            self._validate_lease_parity(record, self._read_global())
        return record

    def summarize(self, goal_path: os.PathLike[str] | str) -> Dict[str, Any]:
        record = self.read(goal_path)
        if record["state"].get("active_lease") is not None:
            self._validate_lease_parity(record, self._read_global())
        receipts = copy.deepcopy(_finalized_receipts(record))
        work_results = [
            receipt["work_result"]
            for receipt in receipts
            if isinstance(receipt.get("work_result"), Mapping)
        ]
        if record["schema_version"] == SCHEMA_VERSION:
            terminal_summary = (
                record["completion_summary"]
                if record["completion_summary"] is not None
                else record["human_intervention_summary"]
            )
            reader_report = terminal_summary["reader_report"] if terminal_summary else ""
            scope_contract = copy.deepcopy(record["scope_contract"])
            recovery_ledger = copy.deepcopy(record["recovery_ledger"])
        else:
            reader_report = (
                f"Retained {record['schema_version']} record; validation and summary only. "
                "Automatic resumption is disabled."
            )
            scope_contract = None
            recovery_ledger = []
        return {
            "schema_version": record["schema_version"],
            "goal_id": record["goal_id"],
            "goal_sha256": record["goal_sha256"],
            "exact_goal": record["goal_text"],
            "phase": record["state"]["phase"],
            "revision": record["state"]["revision"],
            "current_generation": record["state"]["current_generation"],
            "passes_consumed": record["state"]["passes_consumed"],
            "effective_completion_contract": copy.deepcopy(effective_completion_contract(record)),
            "effective_guards": effective_guards(record),
            "scope_contract": scope_contract,
            "finalized_receipt_count": len(receipts),
            "finalized_receipts": receipts,
            "work_results": work_results,
            "recovery_ledger": recovery_ledger,
            "completion_summary": copy.deepcopy(record.get("completion_summary")),
            "human_intervention_summary": copy.deepcopy(
                record.get("human_intervention_summary")
            ),
            "reader_report": reader_report,
        }

    def _write_record(self, path: Path, record: Mapping[str, Any]) -> None:
        validate_record(record, path)
        _atomic_write(path, render_goal(record).encode("utf-8"))

    def _validate_lease_parity(self, record: Mapping[str, Any], global_lease: Optional[Mapping[str, Any]]) -> None:
        active = record["state"].get("active_lease")
        if active is None:
            if global_lease is not None:
                raise ValidationError("goal/global lease mismatch: goal released but global lease remains")
            return
        if global_lease is None:
            raise ValidationError("goal/global lease mismatch: goal lease exists without global lease")
        keys = ("goal_id", "generation", "holder_kind", "holder_token", "transaction_id")
        if any(active.get(key) != global_lease.get(key) for key in keys):
            raise ValidationError("goal/global lease transaction mismatch")
        expected_repo = repository_identity_hash(record["repository_binding"])
        if global_lease.get("repository_fingerprint") != expected_repo:
            raise ValidationError("global lease repository identity mismatch")

    def _load_locked(self, path: Path, expected_revision: Optional[int] = None, require_parity: bool = True) -> Dict[str, Any]:
        record = self.read(path)
        if record["schema_version"] != SCHEMA_VERSION:
            raise StateConflict("retained v1/v2 records are validation-only and cannot be resumed or mutated")
        if expected_revision is not None and record["state"]["revision"] != expected_revision:
            raise StateConflict(
                f"stale revision: expected {expected_revision}, found {record['state']['revision']}"
            )
        if require_parity:
            self._validate_lease_parity(record, self._read_global())
        return record

    def _make_lease(
        self,
        record: Mapping[str, Any],
        generation: int,
        holder_kind: str,
        holder_token: str,
        transaction_id: str,
        timestamp: str,
        *,
        acquired_at: Optional[str] = None,
        quarantined: bool = False,
    ) -> Dict[str, Any]:
        if holder_kind not in HOLDER_KINDS:
            raise ValidationError("invalid lease holder kind")
        lease = {
            "schema_version": LEASE_SCHEMA_VERSION,
            "repository_fingerprint": repository_identity_hash(record["repository_binding"]),
            "goal_id": record["goal_id"],
            "generation": generation,
            "holder_kind": holder_kind,
            "holder_token": holder_token,
            "transaction_id": transaction_id,
            "acquired_at": acquired_at or timestamp,
            "heartbeat_at": timestamp,
            "expires_at": add_minutes(timestamp, 5),
        }
        if quarantined:
            lease["quarantined"] = True
        return lease

    def _commit(
        self,
        path: Path,
        record: MutableMapping[str, Any],
        *,
        timestamp: Optional[str] = None,
        release: bool = False,
        holder_kind: Optional[str] = None,
        holder_token: Optional[str] = None,
        generation: Optional[int] = None,
        quarantined: bool = False,
    ) -> Dict[str, Any]:
        now = timestamp or utc_now()
        record["state"]["revision"] += 1
        record["updated_at"] = now
        if release:
            record["state"]["active_lease"] = None
            self._write_record(path, record)
            self._remove_global()
        else:
            if holder_kind is None or holder_token is None or generation is None:
                raise ValidationError("lease holder details are required for a retained transaction")
            transaction_id = secrets.token_hex(16)
            prior_active = record["state"].get("active_lease") or {}
            lease = self._make_lease(
                record,
                generation,
                holder_kind,
                holder_token,
                transaction_id,
                now,
                acquired_at=prior_active.get("acquired_at"),
                quarantined=quarantined,
            )
            record["state"]["active_lease"] = copy.deepcopy(lease)
            self._write_record(path, record)
            self._write_global(lease)
        loaded = self.read(path)
        self._validate_lease_parity(loaded, self._read_global())
        return loaded

    def _assert_no_active_relay(self) -> None:
        global_lease = self._read_global()
        if global_lease is not None:
            raise ActiveRelayError(f"worktree relay lease is owned by {global_lease.get('goal_id')}")
        for path in sorted(self.goals_dir.glob("goal-*.md")):
            record = self.read(path)
            if record["state"].get("active_lease") is not None:
                raise ActiveRelayError(f"unreconciled per-goal lease exists in {path.name}")

    def initialize(
        self,
        *,
        goal_text: str,
        completion_contract: Mapping[str, Any],
        scope_contract: Mapping[str, Any],
        max_continue_passes: Optional[int] = None,
        deadline_at: Optional[str] = None,
        max_elapsed_minutes: Optional[int] = None,
        repository_binding: Mapping[str, Any],
        initial_fingerprint: str,
        goal_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        launcher_token: Optional[str] = None,
    ) -> tuple[Path, Dict[str, Any]]:
        exact_goal = canonical_goal_text(goal_text)
        if not exact_goal:
            raise ValidationError("goal_text must be nonblank")
        if contains_secret(exact_goal):
            raise ValidationError("goal text appears to contain a secret; redact it before persistence")
        if max_continue_passes is not None and (
            isinstance(max_continue_passes, bool)
            or not isinstance(max_continue_passes, int)
            or max_continue_passes <= 0
        ):
            raise ValidationError("max_continue_passes must be a positive integer or null")
        if deadline_at is not None and max_elapsed_minutes is not None:
            raise ValidationError("deadline_at and max_elapsed_minutes are mutually exclusive")
        if max_elapsed_minutes is not None and (
            isinstance(max_elapsed_minutes, bool)
            or not isinstance(max_elapsed_minutes, int)
            or max_elapsed_minutes <= 0
        ):
            raise ValidationError("max_elapsed_minutes must be a positive integer")
        if not isinstance(completion_contract, Mapping) or not completion_contract.get("required_evidence"):
            raise ValidationError("completion contract must name required canonical evidence")
        validate_scope_contract(scope_contract)
        now = timestamp or utc_now()
        parsed_now = parse_utc(now)
        if deadline_at is not None:
            effective_deadline = canonical_utc(deadline_at)
            if parse_utc(effective_deadline) <= parsed_now:
                raise ValidationError("deadline_at must be in the future")
        elif max_elapsed_minutes is not None:
            effective_deadline = add_minutes(now, max_elapsed_minutes)
        else:
            effective_deadline = None
        binding = copy.deepcopy(dict(repository_binding))
        if binding.get("execution_profile") not in EXECUTION_PROFILES:
            raise ValidationError("unsupported repository execution profile")
        if binding.get("branch") == "main":
            raise ValidationError("main is disabled for relay initialization")
        if binding.get("environment_mode") != "local":
            raise ValidationError("relay initialization requires local environment mode")
        token = launcher_token or secrets.token_hex(16)

        with self._locks():
            self._assert_no_active_relay()
            for _ in range(128):
                candidate_id = goal_id or f"crg-{parse_utc(now).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(8)}"
                if not GOAL_ID_RE.fullmatch(candidate_id):
                    raise ValidationError("invalid requested goal_id")
                path = self.goals_dir / f"goal-{candidate_id}.md"
                if not path.exists():
                    break
                if goal_id is not None:
                    raise StateConflict("requested goal_id already exists")
            else:
                raise GoalStateError("unable to allocate a collision-safe goal file")

            transaction_id = secrets.token_hex(16)
            exact_scope_contract = copy.deepcopy(dict(scope_contract))
            scope_contract_sha256 = sha256_json(exact_scope_contract)
            completion_contract_sha256 = sha256_json(completion_contract)
            initial_work_item_id = exact_scope_contract["included_work_items"][0]["work_item_id"]
            initial_route = build_route(
                worker_skill="continue-research",
                reason_id="initial_goal_execution",
                strategy_id="initial_continue_research",
                source_generation=0,
                work_item_id=initial_work_item_id,
                blocker_fingerprint=initial_fingerprint,
                evidence_hashes=[completion_contract_sha256, scope_contract_sha256],
                scope_contract=exact_scope_contract,
            )
            record: Dict[str, Any] = {
                "schema_version": SCHEMA_VERSION,
                "goal_id": candidate_id,
                "goal_text": exact_goal,
                "goal_sha256": goal_text_sha256(exact_goal),
                "completion_contract": copy.deepcopy(dict(completion_contract)),
                "completion_contract_sha256": completion_contract_sha256,
                "scope_contract": exact_scope_contract,
                "scope_contract_sha256": scope_contract_sha256,
                "amendments": [],
                "created_at": now,
                "deadline_at": effective_deadline,
                "guards": {
                    "max_continue_passes": max_continue_passes,
                    "max_repeated_state_fingerprints": 1,
                    "max_live_continuations": 1,
                    "handoff_ready_timeout_seconds": 60,
                    "stop_on_human_gate": True,
                    "stop_on_validation_failure": True,
                    "stop_on_checkpoint_failure": True,
                    "stop_on_unexpected_dirty_state": True,
                    "stop_on_no_progress": True,
                    "stop_on_repeated_state": True,
                    "stop_on_capability_loss": True,
                    "stop_on_branch_or_repository_mismatch": True,
                },
                "repository_binding": binding,
                "authorization": {"fresh_recursive_threads_explicitly_requested": True},
                "state": {
                    "revision": 1,
                    "phase": "initialized",
                    "current_generation": 0,
                    "passes_consumed": 0,
                    "active_lease": None,
                    "goal_evaluation": "unmet",
                    "last_canonical_fingerprint": initial_fingerprint,
                    "canonical_fingerprint_history": [initial_fingerprint],
                    "terminal_reason": None,
                    "approved_route": initial_route,
                    "approved_route_sha256": sha256_json(initial_route),
                    "human_intervention": None,
                },
                "generations": {},
                "recovery_ledger": [],
                "handoff": {
                    "status": "none",
                    "generation": 1,
                    "token": None,
                    "idempotency_key": None,
                    "predecessor_thread_id": None,
                    "successor_thread_id": None,
                },
                "journal": [],
                "completion_summary": None,
                "completion_summary_sha256": None,
                "human_intervention_summary": None,
                "human_intervention_summary_sha256": None,
                "updated_at": now,
            }
            lease = self._make_lease(record, 0, "launcher", token, transaction_id, now)
            record["state"]["active_lease"] = copy.deepcopy(lease)
            append_journal(
                record,
                "initialized",
                {
                    "goal_id": candidate_id,
                    "goal_sha256": record["goal_sha256"],
                    "completion_contract_sha256": record["completion_contract_sha256"],
                    "scope_contract_sha256": record["scope_contract_sha256"],
                    "initial_route_sha256": record["state"]["approved_route_sha256"],
                    "repository_fingerprint": lease["repository_fingerprint"],
                    "timestamp": now,
                },
            )
            validate_record(record, path)
            _exclusive_write(path, render_goal(record).encode("utf-8"))
            self._write_global(lease)
            loaded = self.read(path)
            self._validate_lease_parity(loaded, self._read_global())
            return path, loaded

    def reserve_successor(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        predecessor_thread_id: Optional[str],
        handoff_token: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            phase = record["state"]["phase"]
            if phase not in {"initialized", "continuation_required", "recovery_required", "recovery_pending"}:
                raise StateConflict(f"cannot reserve successor from {phase}")
            generation = record["state"]["current_generation"] + 1
            key = str(generation)
            if key in record["generations"]:
                raise StateConflict("successor generation already exists")
            route = record["state"].get("approved_route")
            route_sha256 = record["state"].get("approved_route_sha256")
            if route is None or route_sha256 != sha256_json(route):
                raise StateConflict("successor has no already-approved immutable route")
            validate_route(route, record["scope_contract"])
            if route["source_generation"] >= generation:
                raise StateConflict("approved route source generation is not prior to successor")
            token = handoff_token or secrets.token_hex(24)
            idempotency_key = f"{record['goal_id']}:{generation}"
            now = timestamp or utc_now()
            record["generations"][key] = {
                "generation": generation,
                "handoff_token": token,
                "idempotency_key": idempotency_key,
                "phase": "successor_intent",
                "lease_token": token,
                "invocation_consumed": False,
                "invocation_state": "not_authorized",
                "consumed_at": None,
                "returned_at": None,
                "before_fingerprint": record["state"]["last_canonical_fingerprint"],
                "after_fingerprint": None,
                "pending_step_result": None,
                "finalized_receipt_hash": None,
                "terminal_or_successor_outcome": None,
                "claimed_at": None,
                "successor_thread_id": None,
                "route": copy.deepcopy(route),
                "route_sha256": route_sha256,
            }
            record["state"]["phase"] = "successor_intent"
            record["state"]["current_generation"] = generation
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["handoff"] = {
                "status": "intent",
                "generation": generation,
                "token": token,
                "idempotency_key": idempotency_key,
                "predecessor_thread_id": predecessor_thread_id,
                "successor_thread_id": None,
            }
            append_journal(
                record,
                "successor_intent",
                {
                    "generation": generation,
                    "handoff_token": token,
                    "idempotency_key": idempotency_key,
                    "predecessor_thread_id": predecessor_thread_id,
                    "route_sha256": route_sha256,
                    "worker_skill": route["worker_skill"],
                    "strategy_id": route["strategy_id"],
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="successor_reserved",
                holder_token=token,
                generation=generation,
            )

    def record_successor(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        handoff_token: str,
        successor_thread_id: str,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not successor_thread_id:
            raise ValidationError("successor_thread_id must be nonblank")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, require_parity=True)
            handoff = record["handoff"]
            if (
                record["state"]["phase"] == "successor_created"
                and handoff.get("generation") == generation
                and handoff.get("token") == handoff_token
                and handoff.get("successor_thread_id") == successor_thread_id
            ):
                return record
            if record["state"]["revision"] != expected_revision:
                raise StateConflict("stale revision while recording successor")
            if record["state"]["phase"] != "successor_intent":
                raise StateConflict("successor can be recorded only from successor_intent")
            if handoff.get("generation") != generation or handoff.get("token") != handoff_token:
                raise StateConflict("successor handoff identity mismatch")
            entry = record["generations"][str(generation)]
            if entry.get("successor_thread_id") not in (None, successor_thread_id):
                raise StateConflict("a different successor is already recorded")
            now = timestamp or utc_now()
            entry["phase"] = "successor_created"
            entry["successor_thread_id"] = successor_thread_id
            entry["terminal_or_successor_outcome"] = "successor_created"
            handoff["status"] = "created"
            handoff["successor_thread_id"] = successor_thread_id
            record["state"]["phase"] = "successor_created"

            prior_generation = generation - 1
            if prior_generation > 0:
                prior = record["generations"][str(prior_generation)]
                if prior.get("pending_step_result") is not None and prior.get("finalized_receipt_hash") is None:
                    self._finalize_receipt(
                        record,
                        prior_generation,
                        decision="successor_created",
                        successor_thread_id=successor_thread_id,
                        timestamp=now,
                    )
            append_journal(
                record,
                "successor_created",
                {
                    "generation": generation,
                    "handoff_token": handoff_token,
                    "idempotency_key": handoff["idempotency_key"],
                    "successor_thread_id": successor_thread_id,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="successor_reserved",
                holder_token=handoff_token,
                generation=generation,
            )

    def handoff_ready(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        generation: int,
        handoff_token: str,
        idempotency_key: str,
    ) -> bool:
        record = self.read(goal_path)
        handoff = record["handoff"]
        return bool(
            record["state"]["phase"] == "successor_created"
            and handoff.get("status") == "created"
            and handoff.get("generation") == generation
            and handoff.get("token") == handoff_token
            and handoff.get("idempotency_key") == idempotency_key
            and handoff.get("successor_thread_id")
        )

    def claim_generation(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        handoff_token: str,
        idempotency_key: str,
        claim_token: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            handoff = record["handoff"]
            if record["state"]["phase"] != "successor_created":
                raise StateConflict("generation is not claimable")
            if (
                generation != record["state"]["current_generation"]
                or handoff.get("generation") != generation
                or handoff.get("token") != handoff_token
                or handoff.get("idempotency_key") != idempotency_key
                or not handoff.get("successor_thread_id")
            ):
                raise StateConflict("claim identity is stale or mismatched")
            entry = record["generations"][str(generation)]
            if entry["invocation_consumed"] or entry["phase"] != "successor_created":
                raise StateConflict("generation is already claimed or consumed")
            token = claim_token or secrets.token_hex(24)
            now = timestamp or utc_now()
            entry["phase"] = "step_active"
            entry["lease_token"] = token
            entry["claimed_at"] = now
            record["state"]["phase"] = "step_active"
            handoff["status"] = "claimed"
            append_journal(
                record,
                "generation_claimed",
                {
                    "generation": generation,
                    "handoff_token": handoff_token,
                    "idempotency_key": idempotency_key,
                    "claim_token": token,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=token,
                generation=generation,
            )

    def check_guards(self, record: Mapping[str, Any], *, timestamp: Optional[str] = None) -> list[str]:
        now = parse_utc(timestamp or utc_now())
        guards = effective_guards(record)
        stops = []
        pass_limit = guards["max_continue_passes"]
        if pass_limit is not None and record["state"]["passes_consumed"] >= pass_limit:
            stops.append("pass_limit")
        deadline = guards.get("deadline_at", record["deadline_at"])
        if deadline is not None and now >= parse_utc(deadline):
            stops.append("elapsed_limit")
        return stops

    def _validate_worker_route(
        self,
        entry: Mapping[str, Any],
        *,
        worker_skill: str,
        observed_dirty_state_manifest: Optional[Mapping[str, Any]],
    ) -> None:
        route = entry["route"]
        if worker_skill not in WORKER_SKILLS or worker_skill != route["worker_skill"]:
            raise StateConflict("worker skill does not match the immutable generation route")
        expected_manifest = route["dirty_state_manifest"]
        if worker_skill == "improve-project-system":
            if observed_dirty_state_manifest is None:
                raise ValidationError("repair frame requires the observed dirty-state manifest")
            validate_dirty_state_manifest(observed_dirty_state_manifest)
            if canonical_json_bytes(observed_dirty_state_manifest) != canonical_json_bytes(expected_manifest):
                raise StateConflict("dirty state no longer matches the approved repair manifest")
        elif observed_dirty_state_manifest is not None:
            raise ValidationError("research frame cannot supply a repair dirty-state manifest")

    def consume_invocation(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        worker_skill: str,
        observed_dirty_state_manifest: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "step_active":
                raise StateConflict("invocation can be consumed only from step_active")
            entry = record["generations"].get(str(generation))
            active = record["state"]["active_lease"]
            if entry is None or entry.get("lease_token") != claim_token or active.get("holder_token") != claim_token:
                raise StateConflict("claim token or generation mismatch")
            if entry["invocation_consumed"]:
                raise StateConflict("generation invocation was already consumed")
            self._validate_worker_route(
                entry,
                worker_skill=worker_skill,
                observed_dirty_state_manifest=observed_dirty_state_manifest,
            )
            stops = self.check_guards(record, timestamp=timestamp)
            if stops:
                raise GuardStop(",".join(stops))
            now = timestamp or utc_now()
            entry["invocation_consumed"] = True
            entry["invocation_state"] = "authorized"
            entry["consumed_at"] = now
            record["state"]["passes_consumed"] += 1
            append_journal(
                record,
                "invocation_consumed",
                {
                    "generation": generation,
                    "claim_token": claim_token,
                    "worker_skill": worker_skill,
                    "route_sha256": entry["route_sha256"],
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=claim_token,
                generation=generation,
            )

    def _receipt_base(
        self,
        record: Mapping[str, Any],
        generation: int,
        *,
        invocation_count: int | str,
        decision: str,
        timestamp: str,
        evidence: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        entry = record["generations"][str(generation)]
        handoff = record["handoff"]
        supplied = copy.deepcopy(dict(evidence or {}))
        repository = record["repository_binding"]
        route = entry["route"]
        predecessor_thread_id = supplied.pop(
            "predecessor_thread_id", handoff.get("predecessor_thread_id")
        )
        successor_thread_id = supplied.pop("successor_thread_id", None)
        started_at = supplied.pop("started_at", entry.get("claimed_at"))
        repository_root = supplied.pop("repository_root", repository["root"])
        branch = supplied.pop("branch", repository["branch"])
        before_head = supplied.pop("before_head", repository["starting_head"])
        after_head = supplied.pop("after_head", repository["starting_head"])
        agent_job_id = supplied.pop("agent_job_id", None)
        zero_agent_job_reason = supplied.pop("zero_agent_job_reason", None)
        active_task_id = supplied.pop("active_task_id", None)
        latest_handoff_id = supplied.pop("latest_handoff_id", None)
        checkpoint_commit = supplied.pop("checkpoint_commit", None)
        validator_results = supplied.pop("validator_results", [])
        goal_evaluation = supplied.pop("goal_evaluation", record["state"]["goal_evaluation"])
        progress_summary = supplied.pop("progress_summary", "")
        remaining_work = supplied.pop("remaining_work", "")
        completion_path = supplied.pop("completion_path", None)
        completion_sha256 = supplied.pop("completion_sha256", None)
        out_of_scope_remaining_work = supplied.pop("out_of_scope_remaining_work", [])
        work_result = supplied.pop("work_result", None)
        if work_result is None:
            work_result = {
                "work_item_id": route["work_item_id"],
                "work_item_status": (
                    "completed"
                    if goal_evaluation == "met"
                    else ("no_job" if agent_job_id is None else "in_progress")
                ),
                "task_id": active_task_id,
                "agent_job_id": agent_job_id,
                "completion_path": completion_path,
                "completion_sha256": completion_sha256,
                "checkpoint_commit": checkpoint_commit,
                "validator_results": validator_results,
                "progress_summary": progress_summary,
                "zero_job_reason": zero_agent_job_reason,
                "out_of_scope_remaining_work": out_of_scope_remaining_work,
            }
        else:
            work_result = copy.deepcopy(dict(work_result))
        validate_work_result(work_result, record["scope_contract"])
        continue_research_count: int | str = 0
        if route["worker_skill"] == "continue-research":
            continue_research_count = invocation_count
        receipt = {
            "goal_id": record["goal_id"],
            "generation": generation,
            "handoff_token": entry["handoff_token"],
            "idempotency_key": entry["idempotency_key"],
            "predecessor_thread_id": predecessor_thread_id,
            "successor_thread_id": successor_thread_id,
            "started_at": started_at,
            "finished_at": timestamp,
            "repository_root": repository_root,
            "branch": branch,
            "before_head": before_head,
            "after_head": after_head,
            "before_fingerprint": entry.get("before_fingerprint"),
            "after_fingerprint": entry.get("after_fingerprint"),
            "worker_skill": route["worker_skill"],
            "route_sha256": entry["route_sha256"],
            "worker_invocation_count": invocation_count,
            "continue_research_invocation_count": continue_research_count,
            "agent_job_id": agent_job_id,
            "zero_agent_job_reason": zero_agent_job_reason,
            "active_task_id": active_task_id,
            "latest_handoff_id": latest_handoff_id,
            "checkpoint_commit": checkpoint_commit,
            "validator_results": validator_results,
            "goal_evaluation": goal_evaluation,
            "progress_summary": progress_summary,
            "remaining_work": remaining_work,
            "work_result": work_result,
            "decision": decision,
        }
        receipt.update(supplied)
        return receipt

    def _finalize_receipt(
        self,
        record: MutableMapping[str, Any],
        generation: int,
        *,
        decision: str,
        successor_thread_id: Optional[str],
        timestamp: str,
        invocation_count: Optional[int | str] = None,
        evidence: Optional[Mapping[str, Any]] = None,
    ) -> str:
        entry = record["generations"][str(generation)]
        if entry.get("finalized_receipt_hash") is not None:
            raise StateConflict("generation receipt is already finalized")
        pending = copy.deepcopy(entry.get("pending_step_result") or {})
        pending.update(copy.deepcopy(dict(evidence or {})))
        if invocation_count is None:
            invocation_count = 1 if entry.get("invocation_state") == "returned" else (
                "unknown" if entry.get("invocation_state") == "unknown" else 0
            )
        pending["successor_thread_id"] = successor_thread_id
        receipt = self._receipt_base(
            record,
            generation,
            invocation_count=invocation_count,
            decision=decision,
            timestamp=timestamp,
            evidence=pending,
        )
        receipt_hash = append_journal(record, "step_receipt", receipt)
        entry["finalized_receipt_hash"] = receipt_hash
        entry["pending_step_result"] = None
        entry["terminal_or_successor_outcome"] = decision
        return receipt_hash

    def pre_execution_stop(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        stop_reason: str,
        evidence: Optional[Mapping[str, Any]] = None,
        human_intervention: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        terminal = map_stop(stop_reason)
        if terminal == "terminal_complete":
            raise ValidationError("goal completion is not a pre-execution stop")
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_active" or entry is None:
                raise StateConflict("pre-execution stop requires an active generation")
            if entry["invocation_consumed"] or entry.get("lease_token") != claim_token:
                raise StateConflict("pre-execution stop cannot follow consumption or a stale claim")
            validate_human_intervention(human_intervention, record["recovery_ledger"])
            now = timestamp or utc_now()
            entry["phase"] = terminal
            record["state"]["phase"] = terminal
            record["state"]["terminal_reason"] = stop_reason
            record["state"]["human_intervention"] = copy.deepcopy(dict(human_intervention))
            self._finalize_receipt(
                record,
                generation,
                decision=terminal,
                successor_thread_id=None,
                timestamp=now,
                invocation_count=0,
                evidence=evidence,
            )
            record["human_intervention_summary"] = _human_intervention_summary(record)
            record["human_intervention_summary_sha256"] = sha256_json(
                record["human_intervention_summary"]
            )
            return self._commit(path, record, timestamp=now, release=True)

    def record_invocation_returned(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        worker_skill: str,
        execution_evidence: Mapping[str, Any],
        observed_dirty_state_manifest: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not execution_evidence:
            raise ValidationError("direct execution evidence is required")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_active" or entry is None:
                raise StateConflict("returned invocation requires step_active")
            if not entry["invocation_consumed"] or entry["invocation_state"] != "authorized":
                raise StateConflict("invocation was not authorized and consumed")
            if entry.get("lease_token") != claim_token:
                raise StateConflict("claim token mismatch")
            self._validate_worker_route(
                entry,
                worker_skill=worker_skill,
                observed_dirty_state_manifest=observed_dirty_state_manifest,
            )
            now = timestamp or utc_now()
            entry["invocation_state"] = "returned"
            entry["returned_at"] = now
            entry["execution_evidence"] = copy.deepcopy(dict(execution_evidence))
            entry["phase"] = "step_verifying"
            record["state"]["phase"] = "step_verifying"
            append_journal(
                record,
                "invocation_returned",
                {
                    "generation": generation,
                    "worker_skill": worker_skill,
                    "route_sha256": entry["route_sha256"],
                    "execution_evidence": execution_evidence,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=claim_token,
                generation=generation,
            )

    def record_invocation_uncertain(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        worker_skill: str,
        diagnostic: Mapping[str, Any],
        human_intervention: Mapping[str, Any],
        observed_dirty_state_manifest: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_active" or entry is None:
                raise StateConflict("uncertain invocation requires step_active")
            if not entry["invocation_consumed"] or entry.get("lease_token") != claim_token:
                raise StateConflict("uncertain invocation lacks consumed matching claim")
            self._validate_worker_route(
                entry,
                worker_skill=worker_skill,
                observed_dirty_state_manifest=observed_dirty_state_manifest,
            )
            validate_human_intervention(human_intervention, record["recovery_ledger"])
            now = timestamp or utc_now()
            recovery_token = secrets.token_hex(24)
            entry["invocation_state"] = "unknown"
            entry["pending_step_result"] = copy.deepcopy(dict(diagnostic))
            entry["phase"] = "terminal_awaiting_human"
            record["state"]["phase"] = "terminal_awaiting_human"
            record["state"]["terminal_reason"] = "invocation_outcome_uncertain"
            record["state"]["human_intervention"] = copy.deepcopy(dict(human_intervention))
            append_journal(
                record,
                "invocation_uncertain",
                {
                    "generation": generation,
                    "worker_skill": worker_skill,
                    "diagnostic": diagnostic,
                    "recovery_token": recovery_token,
                    "timestamp": now,
                },
            )
            record["human_intervention_summary"] = _human_intervention_summary(record)
            record["human_intervention_summary_sha256"] = sha256_json(
                record["human_intervention_summary"]
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=recovery_token,
                generation=generation,
                quarantined=True,
            )

    def verify_step(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        after_fingerprint: str,
        goal_evaluation: str,
        evidence: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if goal_evaluation not in {"unmet", "met", "indeterminate"}:
            raise ValidationError("invalid goal evaluation")
        if "work_result" not in evidence:
            raise ValidationError("v3 verification evidence requires a standardized work_result")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_verifying" or entry is None:
                raise StateConflict("verification requires step_verifying")
            if entry["invocation_state"] != "returned" or entry.get("lease_token") != claim_token:
                raise StateConflict("verification lacks returned matching invocation")
            validate_work_result(evidence["work_result"], record["scope_contract"])
            if evidence["work_result"]["work_item_id"] != entry["route"]["work_item_id"]:
                raise StateConflict("work_result item does not match the immutable generation route")
            now = timestamp or utc_now()
            status = fingerprint_status(record["state"]["canonical_fingerprint_history"], after_fingerprint)
            entry["after_fingerprint"] = after_fingerprint
            entry["fingerprint_status"] = status
            entry["pending_step_result"] = copy.deepcopy(dict(evidence))
            entry["pending_step_result"].update(
                {"goal_evaluation": goal_evaluation, "fingerprint_status": status}
            )
            entry["phase"] = "step_verified"
            record["state"]["phase"] = "step_verified"
            record["state"]["goal_evaluation"] = goal_evaluation
            record["state"]["last_canonical_fingerprint"] = after_fingerprint
            record["state"]["canonical_fingerprint_history"].append(after_fingerprint)
            append_journal(
                record,
                "step_verified",
                {
                    "generation": generation,
                    "after_fingerprint": after_fingerprint,
                    "fingerprint_status": status,
                    "goal_evaluation": goal_evaluation,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=claim_token,
                generation=generation,
            )

    def decide_step(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        decision: str,
        stop_reason: Optional[str] = None,
        next_work_item_id: Optional[str] = None,
        human_intervention: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_verified" or entry is None:
                raise StateConflict("decision requires step_verified")
            if entry.get("lease_token") != claim_token:
                raise StateConflict("decision claim token mismatch")
            now = timestamp or utc_now()
            if decision == "continuation_required":
                if record["state"]["goal_evaluation"] != "unmet":
                    raise StateConflict("only an unmet goal may recurse")
                if entry.get("fingerprint_status") != "new":
                    raise StateConflict("unchanged or repeated fingerprints may not recurse")
                selected_work_item = next_work_item_id or entry["route"]["work_item_id"]
                scope_items = _scope_item_map(record["scope_contract"])
                if selected_work_item not in scope_items:
                    raise StateConflict("next work item would broaden the immutable goal scope")
                completed_work_items = {
                    receipt["work_result"]["work_item_id"]
                    for receipt in _finalized_receipts(record)
                    if receipt["work_result"]["work_item_status"] == "completed"
                }
                pending_work_result = entry["pending_step_result"]["work_result"]
                if pending_work_result["work_item_status"] == "completed":
                    completed_work_items.add(pending_work_result["work_item_id"])
                missing_dependencies = sorted(
                    set(scope_items[selected_work_item]["depends_on"]) - completed_work_items
                )
                if missing_dependencies:
                    raise StateConflict(
                        "next work item has unmet dependencies: " + ", ".join(missing_dependencies)
                    )
                next_reason = (
                    "resume_research_after_project_system_repair"
                    if entry["route"]["worker_skill"] == "improve-project-system"
                    else "dependency_ready_in_scope"
                )
                next_route = build_route(
                    worker_skill="continue-research",
                    reason_id=next_reason,
                    strategy_id=f"continue_in_scope_generation_{generation + 1}",
                    source_generation=generation,
                    work_item_id=selected_work_item,
                    blocker_fingerprint=entry["after_fingerprint"],
                    evidence_hashes=[
                        entry["after_fingerprint"],
                        sha256_json(entry["pending_step_result"]),
                    ],
                    scope_contract=record["scope_contract"],
                )
                entry["phase"] = decision
                entry["pending_step_result"]["decision"] = decision
                record["state"]["phase"] = decision
                record["state"]["approved_route"] = next_route
                record["state"]["approved_route_sha256"] = sha256_json(next_route)
                append_journal(
                    record,
                    "continuation_required",
                    {
                        "generation": generation,
                        "next_work_item_id": selected_work_item,
                        "approved_route_sha256": record["state"]["approved_route_sha256"],
                        "timestamp": now,
                    },
                )
                return self._commit(
                    path,
                    record,
                    timestamp=now,
                    holder_kind="continuation",
                    holder_token=claim_token,
                    generation=generation,
                )

            terminal = decision
            if stop_reason is not None:
                terminal = map_stop(stop_reason)
            if terminal not in TERMINAL_PHASES:
                raise ValidationError("decision must be continuation_required or a terminal phase")
            if terminal == "terminal_complete" and record["state"]["goal_evaluation"] != "met":
                raise StateConflict("terminal_complete requires goal_evaluation=met")
            if terminal != "terminal_complete" and record["state"]["goal_evaluation"] == "met":
                raise StateConflict("a met goal must use terminal_complete")
            if terminal != "terminal_complete":
                validate_human_intervention(human_intervention, record["recovery_ledger"])
            entry["phase"] = terminal
            record["state"]["phase"] = terminal
            record["state"]["terminal_reason"] = stop_reason or terminal
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["state"]["human_intervention"] = (
                None
                if terminal == "terminal_complete"
                else copy.deepcopy(dict(human_intervention))
            )
            self._finalize_receipt(
                record,
                generation,
                decision=terminal,
                successor_thread_id=None,
                timestamp=now,
            )
            if terminal == "terminal_complete":
                record["completion_summary"] = _completion_summary(record)
                record["completion_summary_sha256"] = sha256_json(
                    record["completion_summary"]
                )
            else:
                record["human_intervention_summary"] = _human_intervention_summary(record)
                record["human_intervention_summary_sha256"] = sha256_json(
                    record["human_intervention_summary"]
                )
            return self._commit(path, record, timestamp=now, release=True)

    def record_recovery_required(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        recovery_plan: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        required = {
            "worker_skill",
            "reason_id",
            "strategy_id",
            "work_item_id",
            "blocker_fingerprint",
            "evidence_hashes",
            "dirty_state_manifest",
            "work_result",
        }
        if not isinstance(recovery_plan, Mapping) or set(recovery_plan) != required:
            raise ValidationError("recovery plan fields are incomplete or unexpected")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if entry is None or entry.get("lease_token") != claim_token:
                raise StateConflict("recovery plan requires the matching active generation")
            phase = record["state"]["phase"]
            if phase == "step_active":
                if entry["invocation_consumed"]:
                    raise StateConflict("pre-consumption recovery cannot follow invocation consumption")
                expected_blocker = record["state"]["last_canonical_fingerprint"]
            elif phase == "step_verified":
                if entry["invocation_state"] != "returned":
                    raise StateConflict("post-return recovery requires a verified returned invocation")
                expected_blocker = entry["after_fingerprint"]
            else:
                raise StateConflict(
                    "record-recovery-required is valid only before consumption or after verified return"
                )
            if recovery_plan["blocker_fingerprint"] != expected_blocker:
                raise StateConflict("recovery plan blocker fingerprint does not match canonical state")
            validate_work_result(recovery_plan["work_result"], record["scope_contract"])
            if phase == "step_active":
                if (
                    recovery_plan["work_result"]["work_item_id"]
                    != entry["route"]["work_item_id"]
                    or recovery_plan["work_result"]["agent_job_id"] is not None
                ):
                    raise ValidationError(
                        "pre-consumption recovery requires a zero-AgentJob result for the current work item"
                    )
            elif recovery_plan["work_result"] != entry["pending_step_result"]["work_result"]:
                raise StateConflict("post-return recovery work result differs from verified evidence")

            route = build_route(
                worker_skill=recovery_plan["worker_skill"],
                reason_id=recovery_plan["reason_id"],
                strategy_id=recovery_plan["strategy_id"],
                source_generation=generation,
                work_item_id=recovery_plan["work_item_id"],
                blocker_fingerprint=recovery_plan["blocker_fingerprint"],
                evidence_hashes=recovery_plan["evidence_hashes"],
                dirty_state_manifest=recovery_plan["dirty_state_manifest"],
                scope_contract=record["scope_contract"],
            )
            pair = (route["blocker_fingerprint"], route["strategy_id"])
            existing_pairs = {
                (item["blocker_fingerprint"], item["strategy_id"])
                for item in record["recovery_ledger"]
            }
            if pair in existing_pairs:
                raise StateConflict("the same recovery strategy already ran or was approved for this blocker")

            scope_items = _scope_item_map(record["scope_contract"])
            completed_work_items = {
                receipt["work_result"]["work_item_id"]
                for receipt in _finalized_receipts(record)
                if receipt["work_result"]["work_item_status"] == "completed"
            }
            if phase == "step_verified":
                pending_work_result = entry["pending_step_result"]["work_result"]
                if pending_work_result["work_item_status"] == "completed":
                    completed_work_items.add(pending_work_result["work_item_id"])
            missing_dependencies = sorted(
                set(scope_items[route["work_item_id"]]["depends_on"]) - completed_work_items
            )
            if missing_dependencies:
                raise StateConflict(
                    "recovery route targets work with unmet dependencies: "
                    + ", ".join(missing_dependencies)
                )

            now = timestamp or utc_now()
            route_sha256 = sha256_json(route)
            recovery_entry = {
                "sequence": len(record["recovery_ledger"]) + 1,
                "strategy_id": route["strategy_id"],
                "blocker_fingerprint": route["blocker_fingerprint"],
                "route": copy.deepcopy(route),
                "route_sha256": route_sha256,
                "approved_for_generation": generation + 1,
                "approved_at": now,
            }
            record["recovery_ledger"].append(recovery_entry)
            if phase == "step_active":
                entry["pending_step_result"] = {
                    "goal_evaluation": "unmet",
                    "fingerprint_status": "not_evaluated",
                    "work_result": copy.deepcopy(recovery_plan["work_result"]),
                    "progress_summary": recovery_plan["work_result"]["progress_summary"],
                    "remaining_work": "approved distinct recovery strategy",
                }
            entry["phase"] = "recovery_required"
            entry["pending_step_result"]["decision"] = "recovery_required"
            record["state"]["phase"] = "recovery_required"
            record["state"]["goal_evaluation"] = "unmet"
            record["state"]["approved_route"] = route
            record["state"]["approved_route_sha256"] = route_sha256
            append_journal(
                record,
                "recovery_required",
                {
                    "generation": generation,
                    "recovery_sequence": recovery_entry["sequence"],
                    "strategy_id": route["strategy_id"],
                    "worker_skill": route["worker_skill"],
                    "blocker_fingerprint": route["blocker_fingerprint"],
                    "approved_route_sha256": route_sha256,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=claim_token,
                generation=generation,
            )

    def reconcile_dispatch(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        handoff_token: str,
        recovery_evidence: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        required = {
            "prior_holder_terminal",
            "matching_unclaimed_successor_ids",
            "capability_available",
            "inspection_evidence_hashes",
        }
        if not isinstance(recovery_evidence, Mapping) or set(recovery_evidence) != required:
            raise ValidationError("dispatch-recovery evidence fields are incomplete or unexpected")
        if recovery_evidence["prior_holder_terminal"] is not True:
            raise ValidationError("dispatch recovery requires terminal-holder proof")
        matching = recovery_evidence["matching_unclaimed_successor_ids"]
        if (
            not isinstance(matching, list)
            or len(matching) != len(set(matching))
            or any(not isinstance(item, str) or not item for item in matching)
        ):
            raise ValidationError("matching successor IDs must be a unique string list")
        evidence_hashes = recovery_evidence["inspection_evidence_hashes"]
        if not isinstance(evidence_hashes, list) or not evidence_hashes:
            raise ValidationError("dispatch recovery requires inspection evidence hashes")
        for digest in evidence_hashes:
            _require_sha256(digest, "dispatch-recovery evidence hash")
        if len(matching) > 1:
            raise StateConflict("dispatch recovery found duplicate matching children")

        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "successor_intent":
                raise StateConflict("dispatch reconciliation requires successor_intent")
            if (
                record["handoff"].get("generation") != generation
                or record["handoff"].get("token") != handoff_token
            ):
                raise StateConflict("dispatch reconciliation handoff identity mismatch")
            entry = record["generations"][str(generation)]
            now = timestamp or utc_now()
            if matching:
                successor_thread_id = matching[0]
                entry["phase"] = "successor_created"
                entry["successor_thread_id"] = successor_thread_id
                entry["terminal_or_successor_outcome"] = "successor_created_reconciled"
                record["handoff"]["status"] = "created"
                record["handoff"]["successor_thread_id"] = successor_thread_id
                record["state"]["phase"] = "successor_created"
                prior_generation = generation - 1
                if prior_generation > 0:
                    prior = record["generations"][str(prior_generation)]
                    if (
                        prior.get("pending_step_result") is not None
                        and prior.get("finalized_receipt_hash") is None
                    ):
                        self._finalize_receipt(
                            record,
                            prior_generation,
                            decision="successor_created_reconciled",
                            successor_thread_id=successor_thread_id,
                            timestamp=now,
                        )
                append_journal(
                    record,
                    "dispatch_reconciled_successor",
                    {
                        "generation": generation,
                        "successor_thread_id": successor_thread_id,
                        "recovery_evidence": recovery_evidence,
                        "timestamp": now,
                    },
                )
                return self._commit(
                    path,
                    record,
                    timestamp=now,
                    holder_kind="successor_reserved",
                    holder_token=handoff_token,
                    generation=generation,
                )

            if recovery_evidence["capability_available"] is not True:
                raise StateConflict("no child exists but task creation capability is unavailable")
            prior_route = entry["route"]
            retry_route = build_route(
                worker_skill=prior_route["worker_skill"],
                reason_id="dispatch_retry_after_proven_no_child",
                strategy_id=f"dispatch_retry_generation_{generation + 1}",
                source_generation=generation,
                work_item_id=prior_route["work_item_id"],
                blocker_fingerprint=record["state"]["last_canonical_fingerprint"],
                evidence_hashes=evidence_hashes,
                dirty_state_manifest=prior_route["dirty_state_manifest"],
                scope_contract=record["scope_contract"],
            )
            route_sha256 = sha256_json(retry_route)
            recovery_entry = {
                "sequence": len(record["recovery_ledger"]) + 1,
                "strategy_id": retry_route["strategy_id"],
                "blocker_fingerprint": retry_route["blocker_fingerprint"],
                "route": copy.deepcopy(retry_route),
                "route_sha256": route_sha256,
                "approved_for_generation": generation + 1,
                "approved_at": now,
            }
            record["recovery_ledger"].append(recovery_entry)
            entry["phase"] = "recovery_required"
            entry["terminal_or_successor_outcome"] = "dispatch_retry_no_child"
            record["handoff"]["status"] = "reconciled_no_child"
            record["state"]["phase"] = "recovery_required"
            record["state"]["approved_route"] = retry_route
            record["state"]["approved_route_sha256"] = route_sha256
            append_journal(
                record,
                "dispatch_recovery_required",
                {
                    "generation": generation,
                    "recovery_sequence": recovery_entry["sequence"],
                    "approved_route_sha256": route_sha256,
                    "recovery_evidence": recovery_evidence,
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=handoff_token,
                generation=generation,
            )

    def dispatch_failure(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        handoff_token: str,
        outcome: str,
        diagnostic: Mapping[str, Any],
        human_intervention: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        outcome_to_reason = {
            "definitive": "dispatch_failed",
            "ambiguous": "ambiguous_dispatch",
            "duplicate": "duplicate",
            "timeout": "handoff_timeout",
        }
        if outcome not in outcome_to_reason:
            raise ValidationError("invalid dispatch failure outcome")
        reason = outcome_to_reason[outcome]
        terminal = map_stop(reason)
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "successor_intent":
                raise StateConflict("dispatch failure requires successor_intent")
            if record["handoff"].get("generation") != generation or record["handoff"].get("token") != handoff_token:
                raise StateConflict("dispatch failure handoff identity mismatch")
            validate_human_intervention(human_intervention, record["recovery_ledger"])
            now = timestamp or utc_now()
            prior_generation = generation - 1
            if prior_generation > 0:
                prior = record["generations"][str(prior_generation)]
                if prior.get("pending_step_result") is not None and prior.get("finalized_receipt_hash") is None:
                    self._finalize_receipt(
                        record,
                        prior_generation,
                        decision=terminal,
                        successor_thread_id=None,
                        timestamp=now,
                        evidence={"dispatch_diagnostic": diagnostic},
                    )
            record["generations"][str(generation)]["phase"] = terminal
            record["generations"][str(generation)]["terminal_or_successor_outcome"] = terminal
            record["state"]["phase"] = terminal
            record["state"]["terminal_reason"] = reason
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["state"]["human_intervention"] = copy.deepcopy(dict(human_intervention))
            append_journal(
                record,
                "dispatch_failure",
                {"generation": generation, "outcome": outcome, "diagnostic": diagnostic, "timestamp": now},
            )
            record["human_intervention_summary"] = _human_intervention_summary(record)
            record["human_intervention_summary_sha256"] = sha256_json(
                record["human_intervention_summary"]
            )
            if outcome == "ambiguous":
                recovery_token = secrets.token_hex(24)
                return self._commit(
                    path,
                    record,
                    timestamp=now,
                    holder_kind="successor_reserved",
                    holder_token=recovery_token,
                    generation=generation,
                    quarantined=True,
                )
            return self._commit(path, record, timestamp=now, release=True)

    def begin_recovery(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        canonical_reconciliation: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not user_authorization:
            raise ValidationError("recovery requires exact user authorization")
        if not canonical_reconciliation:
            raise ValidationError("recovery requires canonical reconciliation evidence")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            prior_phase = record["state"]["phase"]
            if prior_phase not in RECOVERABLE_TERMINALS:
                raise StateConflict(f"phase {prior_phase} is not recoverable")
            if record["state"].get("active_lease") is None and self._read_global() is not None:
                raise ValidationError("cannot recover a released goal while another global lease exists")
            now = timestamp or utc_now()
            token = secrets.token_hex(24)
            current_generation = record["state"]["current_generation"]
            current_route = record["generations"][str(current_generation)]["route"]
            approved_route = build_route(
                worker_skill=current_route["worker_skill"],
                reason_id="explicit_human_authorized_recovery",
                strategy_id=f"human_authorized_recovery_generation_{current_generation + 1}",
                source_generation=current_generation,
                work_item_id=current_route["work_item_id"],
                blocker_fingerprint=record["state"]["last_canonical_fingerprint"],
                evidence_hashes=[sha256_json(canonical_reconciliation)],
                dirty_state_manifest=current_route["dirty_state_manifest"],
                scope_contract=record["scope_contract"],
            )
            record["state"]["phase"] = "recovery_pending"
            record["state"]["terminal_reason"] = None
            record["state"]["human_intervention"] = None
            record["state"]["approved_route"] = approved_route
            record["state"]["approved_route_sha256"] = sha256_json(approved_route)
            record["completion_summary"] = None
            record["completion_summary_sha256"] = None
            record["human_intervention_summary"] = None
            record["human_intervention_summary_sha256"] = None
            append_journal(
                record,
                "recovery_pending",
                {
                    "prior_terminal_phase": prior_phase,
                    "user_authorization": user_authorization,
                    "canonical_reconciliation": canonical_reconciliation,
                    "old_revision": expected_revision,
                    "new_revision": expected_revision + 1,
                    "selected_edge": "terminal_to_recovery_pending",
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="continuation",
                holder_token=token,
                generation=current_generation,
            )

    def adopt_successor(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        successor_thread_id: str,
        unique_live_successor_proof: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Adopt one uniquely proven live, unclaimed successor during recovery."""
        if not successor_thread_id or not unique_live_successor_proof:
            raise ValidationError("successor adoption requires one ID and uniqueness proof")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "recovery_pending" or entry is None:
                raise StateConflict("successor adoption requires recovery_pending and an existing intent")
            if entry["invocation_consumed"] or entry.get("claimed_at") is not None:
                raise StateConflict("a claimed or consumed generation cannot be adopted")
            prior_id = entry.get("successor_thread_id")
            if prior_id not in (None, successor_thread_id):
                raise StateConflict("a different successor is already recorded")
            token = entry["handoff_token"]
            now = timestamp or utc_now()
            entry["phase"] = "successor_created"
            entry["successor_thread_id"] = successor_thread_id
            entry["terminal_or_successor_outcome"] = "successor_created_recovery_adoption"
            record["state"]["phase"] = "successor_created"
            record["state"]["current_generation"] = generation
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["handoff"] = {
                "status": "created",
                "generation": generation,
                "token": token,
                "idempotency_key": entry["idempotency_key"],
                "predecessor_thread_id": record["handoff"].get("predecessor_thread_id"),
                "successor_thread_id": successor_thread_id,
            }
            append_journal(
                record,
                "successor_adopted",
                {
                    "generation": generation,
                    "successor_thread_id": successor_thread_id,
                    "unique_live_successor_proof": unique_live_successor_proof,
                    "selected_edge": "recovery_pending_to_successor_created",
                    "timestamp": now,
                },
            )
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind="successor_reserved",
                holder_token=token,
                generation=generation,
            )

    def write_dispatch_recovery_sidecar(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        generation: int,
        handoff_token: str,
        idempotency_key: str,
        returned_thread_id: str,
        expected_revision: int,
        error: str,
        timestamp: Optional[str] = None,
    ) -> Path:
        """Persist ignored evidence after a concrete task ID cannot be recorded."""
        path = self._validate_path(goal_path)
        record = self.read(path)
        if not returned_thread_id or not error:
            raise ValidationError("dispatch recovery sidecar requires returned ID and error")
        if generation != record["state"]["current_generation"]:
            raise StateConflict("sidecar generation does not match current goal generation")
        if handoff_token != record["handoff"].get("token") or idempotency_key != record["handoff"].get("idempotency_key"):
            raise StateConflict("sidecar handoff identity mismatch")
        payload = {
            "schema_version": "continue-research-goal-dispatch-recovery.v1",
            "goal_id": record["goal_id"],
            "generation": generation,
            "handoff_token": handoff_token,
            "idempotency_key": idempotency_key,
            "returned_thread_id": returned_thread_id,
            "expected_revision": expected_revision,
            "error": error,
            "timestamp": timestamp or utc_now(),
        }
        sidecar = path.with_name(f"{path.stem}.dispatch-recovery.json")
        _atomic_write(sidecar, canonical_json_bytes(payload) + b"\n")
        return sidecar

    def amend_completion_contract(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        new_contract: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not new_contract.get("required_evidence"):
            raise ValidationError("amended contract must name required evidence")
        return self._append_amendment(
            goal_path,
            expected_revision=expected_revision,
            user_authorization=user_authorization,
            kind="completion_contract",
            new_value=dict(new_contract),
            timestamp=timestamp,
        )

    def amend_guards(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        new_guards: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        allowed = {"max_continue_passes", "deadline_at"}
        if not new_guards or not set(new_guards) <= allowed:
            raise ValidationError("guard amendment may change only max_continue_passes or deadline_at")
        return self._append_amendment(
            goal_path,
            expected_revision=expected_revision,
            user_authorization=user_authorization,
            kind="guards",
            new_value=dict(new_guards),
            timestamp=timestamp,
        )

    def _append_amendment(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        kind: str,
        new_value: Mapping[str, Any],
        timestamp: Optional[str],
    ) -> Dict[str, Any]:
        if not user_authorization:
            raise ValidationError("amendment requires exact user authorization")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "recovery_pending":
                raise StateConflict("amendments require recovery_pending")
            now = timestamp or utc_now()
            if kind == "completion_contract":
                prior_value = effective_completion_contract(record)
                effective_new = copy.deepcopy(dict(new_value))
            else:
                prior_value = effective_guards(record)
                effective_new = copy.deepcopy(prior_value)
                if record["schema_version"] == SCHEMA_VERSION:
                    new_value = _validate_v2_guard_extension(
                        prior_value,
                        new_value,
                        created_at=now,
                        require_canonical_deadline=False,
                    )
                else:
                    if "max_continue_passes" in new_value:
                        proposed = new_value["max_continue_passes"]
                        if not isinstance(proposed, int) or proposed <= prior_value["max_continue_passes"]:
                            raise ValidationError("max_continue_passes may only be extended")
                    if "deadline_at" in new_value and parse_utc(new_value["deadline_at"]) <= parse_utc(
                        prior_value.get("deadline_at", record["deadline_at"])
                    ):
                        raise ValidationError("deadline_at may only be extended")
                effective_new.update(copy.deepcopy(dict(new_value)))
            amendment = {
                "kind": kind,
                "user_authorization": user_authorization,
                "created_at": now,
                "prior_effective_sha256": sha256_json(prior_value),
                "new_value": copy.deepcopy(dict(new_value)),
                "new_sha256": sha256_json(effective_new),
            }
            record["amendments"].append(amendment)
            append_journal(record, "amendment", amendment)
            active = record["state"]["active_lease"]
            return self._commit(
                path,
                record,
                timestamp=now,
                holder_kind=active["holder_kind"],
                holder_token=active["holder_token"],
                generation=active["generation"],
            )

    def abandon_unconsumed(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        user_authorization: str,
        terminal_holder_proof: Mapping[str, Any],
        human_intervention: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not user_authorization or not terminal_holder_proof:
            raise ValidationError("abandonment requires authorization and terminal-holder proof")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_active" or entry is None or entry["invocation_consumed"]:
                raise StateConflict("only an unconsumed active generation may be abandoned")
            validate_human_intervention(human_intervention, record["recovery_ledger"])
            now = timestamp or utc_now()
            append_journal(
                record,
                "abandoned_unconsumed",
                {
                    "generation": generation,
                    "user_authorization": user_authorization,
                    "terminal_holder_proof": terminal_holder_proof,
                    "timestamp": now,
                },
            )
            record["state"]["phase"] = "terminal_failed"
            record["state"]["terminal_reason"] = "abandoned_unconsumed"
            record["state"]["human_intervention"] = copy.deepcopy(dict(human_intervention))
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            entry["phase"] = "terminal_failed"
            self._finalize_receipt(
                record,
                generation,
                decision="terminal_failed",
                successor_thread_id=None,
                timestamp=now,
                invocation_count=0,
                evidence={
                    "zero_agent_job_reason": "abandoned before invocation consumption",
                    "progress_summary": "active generation was abandoned before worker invocation",
                    "out_of_scope_remaining_work": [],
                },
            )
            record["human_intervention_summary"] = _human_intervention_summary(record)
            record["human_intervention_summary_sha256"] = sha256_json(
                record["human_intervention_summary"]
            )
            return self._commit(path, record, timestamp=now, release=True)

    def reconcile_consumed(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        returned_proven: bool,
        terminal_holder_proof: Mapping[str, Any],
        canonical_evidence: Mapping[str, Any],
        decision: str,
        human_intervention: Optional[Mapping[str, Any]] = None,
        next_work_item_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not terminal_holder_proof or not canonical_evidence:
            raise ValidationError("consumed reconciliation requires terminal-holder and canonical evidence")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "recovery_pending" or entry is None or not entry["invocation_consumed"]:
                raise StateConflict("consumed reconciliation requires recovery_pending consumed generation")
            if entry.get("finalized_receipt_hash") is not None:
                raise StateConflict("consumed generation receipt is already finalized")
            if decision not in TERMINAL_PHASES | {"continuation_required"}:
                raise ValidationError("invalid reconciliation decision")
            if decision == "continuation_required" and not returned_proven:
                raise StateConflict("unknown invocation count cannot authorize automatic continuation")
            if "work_result" not in canonical_evidence:
                raise ValidationError("consumed reconciliation requires a standardized work_result")
            validate_work_result(canonical_evidence["work_result"], record["scope_contract"])
            now = timestamp or utc_now()
            entry["invocation_state"] = "returned" if returned_proven else "unknown"
            entry["pending_step_result"] = copy.deepcopy(dict(canonical_evidence))
            append_journal(
                record,
                "consumed_reconciliation",
                {
                    "generation": generation,
                    "returned_proven": returned_proven,
                    "terminal_holder_proof": terminal_holder_proof,
                    "canonical_evidence": canonical_evidence,
                    "decision": decision,
                    "timestamp": now,
                },
            )
            if decision == "continuation_required":
                selected_work_item = next_work_item_id or entry["route"]["work_item_id"]
                route = build_route(
                    worker_skill="continue-research",
                    reason_id="resume_after_consumed_reconciliation",
                    strategy_id=f"reconciled_continuation_generation_{generation + 1}",
                    source_generation=generation,
                    work_item_id=selected_work_item,
                    blocker_fingerprint=record["state"]["last_canonical_fingerprint"],
                    evidence_hashes=[sha256_json(canonical_evidence)],
                    scope_contract=record["scope_contract"],
                )
                entry["phase"] = decision
                entry["pending_step_result"]["decision"] = decision
                record["state"]["phase"] = decision
                record["state"]["approved_route"] = route
                record["state"]["approved_route_sha256"] = sha256_json(route)
                active = record["state"]["active_lease"]
                return self._commit(
                    path,
                    record,
                    timestamp=now,
                    holder_kind=active["holder_kind"],
                    holder_token=active["holder_token"],
                    generation=active["generation"],
                )
            if decision == "terminal_complete":
                if canonical_evidence.get("goal_evaluation") != "met":
                    raise StateConflict("terminal_complete reconciliation requires goal_evaluation=met")
                record["state"]["goal_evaluation"] = "met"
            else:
                validate_human_intervention(human_intervention, record["recovery_ledger"])
            entry["phase"] = decision
            record["state"]["phase"] = decision
            record["state"]["terminal_reason"] = "reconciled_consumed_generation"
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["state"]["human_intervention"] = (
                None
                if decision == "terminal_complete"
                else copy.deepcopy(dict(human_intervention))
            )
            self._finalize_receipt(
                record,
                generation,
                decision=decision,
                successor_thread_id=None,
                timestamp=now,
                invocation_count=1 if returned_proven else "unknown",
            )
            if decision == "terminal_complete":
                record["completion_summary"] = _completion_summary(record)
                record["completion_summary_sha256"] = sha256_json(
                    record["completion_summary"]
                )
            else:
                record["human_intervention_summary"] = _human_intervention_summary(record)
                record["human_intervention_summary_sha256"] = sha256_json(
                    record["human_intervention_summary"]
                )
            return self._commit(path, record, timestamp=now, release=True)

    def cancel_recovery(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        human_intervention: Mapping[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not user_authorization:
            raise ValidationError("cancellation requires exact user authorization")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "recovery_pending":
                raise StateConflict("cancellation requires recovery_pending")
            validate_human_intervention(human_intervention, record["recovery_ledger"])
            now = timestamp or utc_now()
            append_journal(
                record,
                "cancelled",
                {"user_authorization": user_authorization, "timestamp": now},
            )
            record["state"]["phase"] = "terminal_cancelled"
            record["state"]["terminal_reason"] = "cancelled"
            record["state"]["approved_route"] = None
            record["state"]["approved_route_sha256"] = None
            record["state"]["human_intervention"] = copy.deepcopy(dict(human_intervention))
            record["human_intervention_summary"] = _human_intervention_summary(record)
            record["human_intervention_summary_sha256"] = sha256_json(
                record["human_intervention_summary"]
            )
            return self._commit(path, record, timestamp=now, release=True)


def _json_arg(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _print_result(record_or_pair: Any) -> None:
    if isinstance(record_or_pair, tuple):
        path, record = record_or_pair
        payload = {"goal_file": str(path), "record": record}
    else:
        payload = record_or_pair
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--goals-dir", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--goal-file", type=Path, required=True)
    validate.add_argument("--require-lease-parity", action="store_true")

    summarize = sub.add_parser("summarize")
    summarize.add_argument("--goal-file", type=Path, required=True)

    init = sub.add_parser("initialize")
    init.add_argument("--goal-text", required=True)
    init.add_argument("--completion-contract-json", type=_json_arg, required=True)
    init.add_argument("--scope-contract-json", type=_json_arg, required=True)
    init.add_argument("--max-continue-passes", type=int)
    deadline = init.add_mutually_exclusive_group()
    deadline.add_argument("--deadline-at")
    deadline.add_argument("--max-elapsed-minutes", type=int)
    init.add_argument("--repository-binding-json", type=_json_arg, required=True)
    init.add_argument("--initial-fingerprint", required=True)

    for name in (
        "reserve-successor",
        "record-successor",
        "claim",
        "pre-execution-stop",
        "consume",
        "returned",
        "uncertain",
        "verify-step",
        "decide-step",
        "record-recovery-required",
        "reconcile-dispatch",
        "dispatch-failure",
        "dispatch-recovery-sidecar",
        "begin-recovery",
        "adopt-successor",
        "amend-contract",
        "amend-guards",
        "abandon-unconsumed",
        "reconcile-consumed",
        "cancel",
    ):
        command = sub.add_parser(name)
        command.add_argument("--goal-file", type=Path, required=True)
        command.add_argument("--expected-revision", type=int, required=True)
        if name == "reserve-successor":
            command.add_argument("--predecessor-thread-id")
        elif name == "record-successor":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--successor-thread-id", required=True)
        elif name == "claim":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--idempotency-key", required=True)
        elif name == "pre-execution-stop":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--stop-reason", required=True)
            command.add_argument("--evidence-json", type=_json_arg, default={})
            command.add_argument("--human-intervention-json", type=_json_arg, required=True)
        elif name == "consume":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--worker-skill", choices=sorted(WORKER_SKILLS), required=True)
            command.add_argument("--observed-dirty-state-manifest-json", type=_json_arg)
        elif name == "returned":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--worker-skill", choices=sorted(WORKER_SKILLS), required=True)
            command.add_argument("--execution-evidence-json", type=_json_arg, required=True)
            command.add_argument("--observed-dirty-state-manifest-json", type=_json_arg)
        elif name == "uncertain":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--worker-skill", choices=sorted(WORKER_SKILLS), required=True)
            command.add_argument("--diagnostic-json", type=_json_arg, required=True)
            command.add_argument("--human-intervention-json", type=_json_arg, required=True)
            command.add_argument("--observed-dirty-state-manifest-json", type=_json_arg)
        elif name == "verify-step":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--after-fingerprint", required=True)
            command.add_argument("--goal-evaluation", choices=("unmet", "met", "indeterminate"), required=True)
            command.add_argument("--evidence-json", type=_json_arg, required=True)
        elif name == "decide-step":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--decision", required=True)
            command.add_argument("--stop-reason")
            command.add_argument("--next-work-item-id")
            command.add_argument("--human-intervention-json", type=_json_arg)
        elif name == "record-recovery-required":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--recovery-plan-json", type=_json_arg, required=True)
        elif name == "reconcile-dispatch":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--recovery-evidence-json", type=_json_arg, required=True)
        elif name == "dispatch-failure":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--outcome", choices=("definitive", "ambiguous", "duplicate", "timeout"), required=True)
            command.add_argument("--diagnostic-json", type=_json_arg, required=True)
            command.add_argument("--human-intervention-json", type=_json_arg, required=True)
        elif name == "dispatch-recovery-sidecar":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--idempotency-key", required=True)
            command.add_argument("--returned-thread-id", required=True)
            command.add_argument("--error", required=True)
        elif name == "begin-recovery":
            command.add_argument("--user-authorization", required=True)
            command.add_argument("--canonical-reconciliation-json", type=_json_arg, required=True)
        elif name == "adopt-successor":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--successor-thread-id", required=True)
            command.add_argument("--unique-live-successor-proof-json", type=_json_arg, required=True)
        elif name == "amend-contract":
            command.add_argument("--user-authorization", required=True)
            command.add_argument("--new-contract-json", type=_json_arg, required=True)
        elif name == "amend-guards":
            command.add_argument("--user-authorization", required=True)
            command.add_argument("--new-guards-json", type=_json_arg, required=True)
        elif name == "abandon-unconsumed":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--user-authorization", required=True)
            command.add_argument("--terminal-holder-proof-json", type=_json_arg, required=True)
            command.add_argument("--human-intervention-json", type=_json_arg, required=True)
        elif name == "reconcile-consumed":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--returned-proven", action="store_true")
            command.add_argument("--terminal-holder-proof-json", type=_json_arg, required=True)
            command.add_argument("--canonical-evidence-json", type=_json_arg, required=True)
            command.add_argument("--decision", required=True)
            command.add_argument("--next-work-item-id")
            command.add_argument("--human-intervention-json", type=_json_arg)
        elif name == "cancel":
            command.add_argument("--user-authorization", required=True)
            command.add_argument("--human-intervention-json", type=_json_arg, required=True)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    store = GoalStore(args.goals_dir)
    try:
        if args.command == "validate":
            result = store.read(args.goal_file, require_lease_parity=args.require_lease_parity)
        elif args.command == "summarize":
            result = store.summarize(args.goal_file)
        elif args.command == "initialize":
            result = store.initialize(
                goal_text=args.goal_text,
                completion_contract=args.completion_contract_json,
                scope_contract=args.scope_contract_json,
                max_continue_passes=args.max_continue_passes,
                deadline_at=args.deadline_at,
                max_elapsed_minutes=args.max_elapsed_minutes,
                repository_binding=args.repository_binding_json,
                initial_fingerprint=args.initial_fingerprint,
            )
        elif args.command == "reserve-successor":
            result = store.reserve_successor(
                args.goal_file,
                expected_revision=args.expected_revision,
                predecessor_thread_id=args.predecessor_thread_id,
            )
        elif args.command == "record-successor":
            result = store.record_successor(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                handoff_token=args.handoff_token,
                successor_thread_id=args.successor_thread_id,
            )
        elif args.command == "claim":
            result = store.claim_generation(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                handoff_token=args.handoff_token,
                idempotency_key=args.idempotency_key,
            )
        elif args.command == "pre-execution-stop":
            result = store.pre_execution_stop(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                stop_reason=args.stop_reason,
                evidence=args.evidence_json,
                human_intervention=args.human_intervention_json,
            )
        elif args.command == "consume":
            result = store.consume_invocation(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                worker_skill=args.worker_skill,
                observed_dirty_state_manifest=args.observed_dirty_state_manifest_json,
            )
        elif args.command == "returned":
            result = store.record_invocation_returned(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                worker_skill=args.worker_skill,
                execution_evidence=args.execution_evidence_json,
                observed_dirty_state_manifest=args.observed_dirty_state_manifest_json,
            )
        elif args.command == "uncertain":
            result = store.record_invocation_uncertain(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                worker_skill=args.worker_skill,
                diagnostic=args.diagnostic_json,
                human_intervention=args.human_intervention_json,
                observed_dirty_state_manifest=args.observed_dirty_state_manifest_json,
            )
        elif args.command == "verify-step":
            result = store.verify_step(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                after_fingerprint=args.after_fingerprint,
                goal_evaluation=args.goal_evaluation,
                evidence=args.evidence_json,
            )
        elif args.command == "decide-step":
            result = store.decide_step(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                decision=args.decision,
                stop_reason=args.stop_reason,
                next_work_item_id=args.next_work_item_id,
                human_intervention=args.human_intervention_json,
            )
        elif args.command == "record-recovery-required":
            result = store.record_recovery_required(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                recovery_plan=args.recovery_plan_json,
            )
        elif args.command == "reconcile-dispatch":
            result = store.reconcile_dispatch(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                handoff_token=args.handoff_token,
                recovery_evidence=args.recovery_evidence_json,
            )
        elif args.command == "dispatch-failure":
            result = store.dispatch_failure(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                handoff_token=args.handoff_token,
                outcome=args.outcome,
                diagnostic=args.diagnostic_json,
                human_intervention=args.human_intervention_json,
            )
        elif args.command == "dispatch-recovery-sidecar":
            sidecar = store.write_dispatch_recovery_sidecar(
                args.goal_file,
                generation=args.generation,
                handoff_token=args.handoff_token,
                idempotency_key=args.idempotency_key,
                returned_thread_id=args.returned_thread_id,
                expected_revision=args.expected_revision,
                error=args.error,
            )
            result = {"dispatch_recovery_sidecar": str(sidecar)}
        elif args.command == "begin-recovery":
            result = store.begin_recovery(
                args.goal_file,
                expected_revision=args.expected_revision,
                user_authorization=args.user_authorization,
                canonical_reconciliation=args.canonical_reconciliation_json,
            )
        elif args.command == "adopt-successor":
            result = store.adopt_successor(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                successor_thread_id=args.successor_thread_id,
                unique_live_successor_proof=args.unique_live_successor_proof_json,
            )
        elif args.command == "amend-contract":
            result = store.amend_completion_contract(
                args.goal_file,
                expected_revision=args.expected_revision,
                user_authorization=args.user_authorization,
                new_contract=args.new_contract_json,
            )
        elif args.command == "amend-guards":
            result = store.amend_guards(
                args.goal_file,
                expected_revision=args.expected_revision,
                user_authorization=args.user_authorization,
                new_guards=args.new_guards_json,
            )
        elif args.command == "abandon-unconsumed":
            result = store.abandon_unconsumed(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                user_authorization=args.user_authorization,
                terminal_holder_proof=args.terminal_holder_proof_json,
                human_intervention=args.human_intervention_json,
            )
        elif args.command == "reconcile-consumed":
            result = store.reconcile_consumed(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                returned_proven=args.returned_proven,
                terminal_holder_proof=args.terminal_holder_proof_json,
                canonical_evidence=args.canonical_evidence_json,
                decision=args.decision,
                human_intervention=args.human_intervention_json,
                next_work_item_id=args.next_work_item_id,
            )
        elif args.command == "cancel":
            result = store.cancel_recovery(
                args.goal_file,
                expected_revision=args.expected_revision,
                user_authorization=args.user_authorization,
                human_intervention=args.human_intervention_json,
            )
        else:  # pragma: no cover - argparse enforces the command set.
            raise AssertionError(args.command)
    except GoalStateError as exc:
        print(json.dumps({"status": "blocked", "error_type": type(exc).__name__, "error": str(exc)}))
        return 2
    _print_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
