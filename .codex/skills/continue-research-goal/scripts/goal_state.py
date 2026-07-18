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
SCHEMA_VERSION = "continue-research-goal.v2"
SUPPORTED_SCHEMA_VERSIONS = {LEGACY_SCHEMA_VERSION, SCHEMA_VERSION}
LEASE_SCHEMA_VERSION = "continue-research-goal-worktree-lease.v1"
EXECUTION_PROFILES = {"acceptance_test", "production_profile"}

NONTERMINAL_PHASES = {
    "initialized",
    "successor_intent",
    "successor_created",
    "step_active",
    "step_verifying",
    "step_verified",
    "continuation_required",
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
    "repetition_limit": "terminal_guard_exhausted",
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
    if record.get("schema_version") == SCHEMA_VERSION:
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

    expected_prior = None
    seen_receipts: Dict[int, str] = {}
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
            seen_receipts[generation] = expected_hash

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

    effective_contract = record["completion_contract"]
    effective_guard_values = _initial_effective_guards(record)
    for amendment in record["amendments"]:
        if amendment.get("kind") == "completion_contract":
            prior = sha256_json(effective_contract)
            effective_contract = amendment.get("new_value")
        elif amendment.get("kind") == "guards":
            prior = sha256_json(effective_guard_values)
            new_guard_values = amendment.get("new_value", {})
            if schema_version == SCHEMA_VERSION:
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
            record: Dict[str, Any] = {
                "schema_version": SCHEMA_VERSION,
                "goal_id": candidate_id,
                "goal_text": exact_goal,
                "goal_sha256": goal_text_sha256(exact_goal),
                "completion_contract": copy.deepcopy(dict(completion_contract)),
                "completion_contract_sha256": sha256_json(completion_contract),
                "amendments": [],
                "created_at": now,
                "deadline_at": effective_deadline,
                "guards": {
                    "max_continue_passes": max_continue_passes,
                    "max_repeated_state_fingerprints": 1,
                    "max_live_continuations": 1,
                    "handoff_ready_timeout_seconds": 60,
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
                },
                "generations": {},
                "handoff": {
                    "status": "none",
                    "generation": 1,
                    "token": None,
                    "idempotency_key": None,
                    "predecessor_thread_id": None,
                    "successor_thread_id": None,
                },
                "journal": [],
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
            if phase not in {"initialized", "continuation_required", "recovery_pending"}:
                raise StateConflict(f"cannot reserve successor from {phase}")
            generation = record["state"]["current_generation"] + 1
            key = str(generation)
            if key in record["generations"]:
                raise StateConflict("successor generation already exists")
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
            }
            record["state"]["phase"] = "successor_intent"
            record["state"]["current_generation"] = generation
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

    def consume_invocation(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
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
                {"generation": generation, "claim_token": claim_token, "timestamp": now},
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
        receipt = {
            "goal_id": record["goal_id"],
            "generation": generation,
            "handoff_token": entry["handoff_token"],
            "idempotency_key": entry["idempotency_key"],
            "predecessor_thread_id": supplied.pop("predecessor_thread_id", handoff.get("predecessor_thread_id")),
            "successor_thread_id": supplied.pop("successor_thread_id", None),
            "started_at": supplied.pop("started_at", entry.get("claimed_at")),
            "finished_at": timestamp,
            "repository_root": supplied.pop("repository_root", repository["root"]),
            "branch": supplied.pop("branch", repository["branch"]),
            "before_head": supplied.pop("before_head", repository["starting_head"]),
            "after_head": supplied.pop("after_head", repository["starting_head"]),
            "before_fingerprint": entry.get("before_fingerprint"),
            "after_fingerprint": entry.get("after_fingerprint"),
            "continue_research_invocation_count": invocation_count,
            "agent_job_id": supplied.pop("agent_job_id", None),
            "zero_agent_job_reason": supplied.pop("zero_agent_job_reason", None),
            "active_task_id": supplied.pop("active_task_id", None),
            "latest_handoff_id": supplied.pop("latest_handoff_id", None),
            "checkpoint_commit": supplied.pop("checkpoint_commit", None),
            "validator_results": supplied.pop("validator_results", []),
            "goal_evaluation": supplied.pop("goal_evaluation", record["state"]["goal_evaluation"]),
            "progress_summary": supplied.pop("progress_summary", ""),
            "remaining_work": supplied.pop("remaining_work", ""),
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
            now = timestamp or utc_now()
            entry["phase"] = terminal
            record["state"]["phase"] = terminal
            record["state"]["terminal_reason"] = stop_reason
            self._finalize_receipt(
                record,
                generation,
                decision=terminal,
                successor_thread_id=None,
                timestamp=now,
                invocation_count=0,
                evidence=evidence,
            )
            return self._commit(path, record, timestamp=now, release=True)

    def record_invocation_returned(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        claim_token: str,
        execution_evidence: Mapping[str, Any],
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
            now = timestamp or utc_now()
            entry["invocation_state"] = "returned"
            entry["returned_at"] = now
            entry["execution_evidence"] = copy.deepcopy(dict(execution_evidence))
            entry["phase"] = "step_verifying"
            record["state"]["phase"] = "step_verifying"
            append_journal(
                record,
                "invocation_returned",
                {"generation": generation, "execution_evidence": execution_evidence, "timestamp": now},
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
        diagnostic: Mapping[str, Any],
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
            now = timestamp or utc_now()
            recovery_token = secrets.token_hex(24)
            entry["invocation_state"] = "unknown"
            entry["pending_step_result"] = copy.deepcopy(dict(diagnostic))
            entry["phase"] = "terminal_awaiting_human"
            record["state"]["phase"] = "terminal_awaiting_human"
            record["state"]["terminal_reason"] = "invocation_outcome_uncertain"
            append_journal(
                record,
                "invocation_uncertain",
                {"generation": generation, "diagnostic": diagnostic, "recovery_token": recovery_token, "timestamp": now},
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
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            entry = record["generations"].get(str(generation))
            if record["state"]["phase"] != "step_verifying" or entry is None:
                raise StateConflict("verification requires step_verifying")
            if entry["invocation_state"] != "returned" or entry.get("lease_token") != claim_token:
                raise StateConflict("verification lacks returned matching invocation")
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
                entry["phase"] = decision
                entry["pending_step_result"]["decision"] = decision
                record["state"]["phase"] = decision
                append_journal(
                    record,
                    "continuation_required",
                    {"generation": generation, "timestamp": now},
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
            entry["phase"] = terminal
            record["state"]["phase"] = terminal
            record["state"]["terminal_reason"] = stop_reason or terminal
            self._finalize_receipt(
                record,
                generation,
                decision=terminal,
                successor_thread_id=None,
                timestamp=now,
            )
            return self._commit(path, record, timestamp=now, release=True)

    def dispatch_failure(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        generation: int,
        handoff_token: str,
        outcome: str,
        diagnostic: Mapping[str, Any],
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
            append_journal(
                record,
                "dispatch_failure",
                {"generation": generation, "outcome": outcome, "diagnostic": diagnostic, "timestamp": now},
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
            record["state"]["phase"] = "recovery_pending"
            record["state"]["terminal_reason"] = None
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
                generation=record["state"]["current_generation"],
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
            entry["phase"] = "terminal_failed"
            self._finalize_receipt(
                record,
                generation,
                decision="terminal_failed",
                successor_thread_id=None,
                timestamp=now,
                invocation_count=0,
                evidence={"zero_agent_job_reason": "abandoned before invocation consumption"},
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
                entry["phase"] = decision
                entry["pending_step_result"]["decision"] = decision
                record["state"]["phase"] = decision
                active = record["state"]["active_lease"]
                return self._commit(
                    path,
                    record,
                    timestamp=now,
                    holder_kind=active["holder_kind"],
                    holder_token=active["holder_token"],
                    generation=active["generation"],
                )
            entry["phase"] = decision
            record["state"]["phase"] = decision
            record["state"]["terminal_reason"] = "reconciled_consumed_generation"
            self._finalize_receipt(
                record,
                generation,
                decision=decision,
                successor_thread_id=None,
                timestamp=now,
                invocation_count=1 if returned_proven else "unknown",
            )
            return self._commit(path, record, timestamp=now, release=True)

    def cancel_recovery(
        self,
        goal_path: os.PathLike[str] | str,
        *,
        expected_revision: int,
        user_authorization: str,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not user_authorization:
            raise ValidationError("cancellation requires exact user authorization")
        path = self._validate_path(goal_path)
        with self._locks(path):
            record = self._load_locked(path, expected_revision)
            if record["state"]["phase"] != "recovery_pending":
                raise StateConflict("cancellation requires recovery_pending")
            now = timestamp or utc_now()
            append_journal(
                record,
                "cancelled",
                {"user_authorization": user_authorization, "timestamp": now},
            )
            record["state"]["phase"] = "terminal_cancelled"
            record["state"]["terminal_reason"] = "cancelled"
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

    init = sub.add_parser("initialize")
    init.add_argument("--goal-text", required=True)
    init.add_argument("--completion-contract-json", type=_json_arg, required=True)
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
        elif name == "consume":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
        elif name == "returned":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--execution-evidence-json", type=_json_arg, required=True)
        elif name == "uncertain":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--claim-token", required=True)
            command.add_argument("--diagnostic-json", type=_json_arg, required=True)
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
        elif name == "dispatch-failure":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--handoff-token", required=True)
            command.add_argument("--outcome", choices=("definitive", "ambiguous", "duplicate", "timeout"), required=True)
            command.add_argument("--diagnostic-json", type=_json_arg, required=True)
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
        elif name == "reconcile-consumed":
            command.add_argument("--generation", type=int, required=True)
            command.add_argument("--returned-proven", action="store_true")
            command.add_argument("--terminal-holder-proof-json", type=_json_arg, required=True)
            command.add_argument("--canonical-evidence-json", type=_json_arg, required=True)
            command.add_argument("--decision", required=True)
        elif name == "cancel":
            command.add_argument("--user-authorization", required=True)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    store = GoalStore(args.goals_dir)
    try:
        if args.command == "validate":
            result = store.read(args.goal_file, require_lease_parity=args.require_lease_parity)
        elif args.command == "initialize":
            result = store.initialize(
                goal_text=args.goal_text,
                completion_contract=args.completion_contract_json,
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
            )
        elif args.command == "consume":
            result = store.consume_invocation(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
            )
        elif args.command == "returned":
            result = store.record_invocation_returned(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                execution_evidence=args.execution_evidence_json,
            )
        elif args.command == "uncertain":
            result = store.record_invocation_uncertain(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                claim_token=args.claim_token,
                diagnostic=args.diagnostic_json,
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
            )
        elif args.command == "dispatch-failure":
            result = store.dispatch_failure(
                args.goal_file,
                expected_revision=args.expected_revision,
                generation=args.generation,
                handoff_token=args.handoff_token,
                outcome=args.outcome,
                diagnostic=args.diagnostic_json,
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
            )
        elif args.command == "cancel":
            result = store.cancel_recovery(
                args.goal_file,
                expected_revision=args.expected_revision,
                user_authorization=args.user_authorization,
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
