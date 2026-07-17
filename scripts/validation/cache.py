"""Conservative exact-tree validation-cache storage.

This module implements the standalone storage boundary defined by
``validation_cache_contract_v1.md``.  It deliberately does not integrate with
the validation executor or make any manifest gate cache-eligible.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
from typing import Callable, Mapping, Sequence


CONTRACT_ID = "validation-cache-contract-v1"
KEY_SCHEMA_ID = "validation_cache_key_v1"
ENTRY_SCHEMA_ID = "validation_cache_entry_v1"
DEFAULT_CACHE_ROOT = Path(".local/validation-cache/v1")
DEFAULT_MAX_ENTRY_BYTES = 16 * 1024 * 1024
DEFAULT_MAX_ENTRIES = 2_048
DEFAULT_MAX_TOTAL_BYTES = 512 * 1024 * 1024
CACHE_MODES = ("off", "read_only", "read_write")
CACHE_POLICIES = ("exact_tree", "scheduled_bypass")

_HEX_64 = re.compile(r"[0-9a-f]{64}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_QUALIFIED_DIGEST = re.compile(r"[a-z][a-z0-9_-]*:[0-9a-f]{40,128}\Z")
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_FINDING_ID = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\Z")
_UTC_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z"
)
_ENTRY_FIELDS = {
    "schema_id",
    "schema_version",
    "contract_id",
    "key_material",
    "cache_key",
    "gate_id",
    "original_result",
    "result_hash",
    "created_at",
    "writer",
    "source_fingerprint_manifest",
    "source_fingerprint_hash",
    "full_receipt",
    "byte_size",
    "authority",
}
_RESULT_FIELDS = {
    "schema_id",
    "gate_id",
    "severity",
    "status",
    "cache_status",
    "input_fingerprint",
    "implementation_fingerprint",
    "started_at",
    "finished_at",
    "duration_ms",
    "error_count",
    "warning_count",
    "finding_count",
    "shown_finding_count",
    "findings_truncated",
    "shown_findings",
    "full_receipt",
    "satisfied_obligation_ids",
    "child_gate_ids",
    "mutated_paths",
    "artifact_refs",
}
_FINDING_FIELDS = {
    "schema_id",
    "finding_id",
    "level",
    "code",
    "message",
    "artifact_ref",
}
_FULL_RECEIPT_FIELDS = {
    "artifact_id",
    "path",
    "content_hash",
    "local_only",
    "authoritative",
}
_SOURCE_FIELDS = {"input_id", "input_type", "digest"}
_AUTHORITY = {
    "operational_validation_only": True,
    "source_authoritative": False,
    "full_receipts_authoritative": False,
    "physics_claim_authority": False,
    "ontology_authority": False,
    "proof_authority": False,
    "benchmark_authority": False,
    "gate_chair_authority": False,
}


class CacheValidationError(ValueError):
    """Raised when cache material cannot satisfy the v1 contract."""


class CacheIntegrityError(CacheValidationError):
    """Raised when stored cache material is corrupt or unsafe."""


class CacheMismatchError(CacheIntegrityError):
    """Raised when an explicitly offered entry belongs to another exact key."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True, slots=True)
class CacheLookup:
    """Bounded outcome of one exact-key lookup."""

    status: str
    reason: str
    cache_key: str | None = None
    entry_path: Path | None = None
    original_result: dict[str, object] | None = None
    result_hash: str | None = None

    @property
    def hit(self) -> bool:
        return self.status == "HIT"

    def as_hit_result(
        self,
        *,
        started_at: str,
        finished_at: str,
        duration_ms: int,
    ) -> dict[str, object]:
        """Create a current ``CACHE_HIT`` result without mutating the original."""

        if not self.hit or self.original_result is None:
            raise CacheValidationError("only a cache hit can emit a CACHE_HIT result")
        _validate_time_window(started_at, finished_at, duration_ms)
        result = deepcopy(self.original_result)
        result["status"] = "CACHE_HIT"
        result["cache_status"] = "HIT"
        result["started_at"] = started_at
        result["finished_at"] = finished_at
        result["duration_ms"] = duration_ms
        return result


@dataclass(frozen=True, slots=True)
class CacheWrite:
    """Bounded outcome of one optional cache publication."""

    status: str
    reason: str
    cache_key: str | None = None
    entry_path: Path | None = None


@dataclass(frozen=True, slots=True)
class CacheInspection:
    """Read-only cache inventory summary."""

    entry_count: int
    total_bytes: int
    valid_count: int
    invalid_count: int
    reads_disabled: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": "validation_cache_inspection_v1",
            "entry_count": self.entry_count,
            "total_bytes": self.total_bytes,
            "valid_count": self.valid_count,
            "invalid_count": self.invalid_count,
            "reads_disabled": self.reads_disabled,
            "authority": "operational_validation_only",
        }


def _exact_keys(value: Mapping[str, object], expected: set[str], name: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise CacheValidationError(
            f"{name} fields do not match schema; missing={missing} unknown={unknown}"
        )


def _require_string(
    value: object,
    name: str,
    pattern: re.Pattern[str] | None = None,
    *,
    max_bytes: int = 4_096,
) -> str:
    if not isinstance(value, str) or not value:
        raise CacheValidationError(f"{name} must be a nonblank string")
    if len(value.encode("utf-8")) > max_bytes:
        raise CacheValidationError(f"{name} exceeds {max_bytes} UTF-8 bytes")
    if pattern is not None and not pattern.fullmatch(value):
        raise CacheValidationError(f"{name} has an unsupported format")
    return value


def _require_int(value: object, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise CacheValidationError(f"{name} must be an integer >= {minimum}")
    return value


def _canonical_bytes(value: object) -> bytes:
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise CacheValidationError(f"value is not canonical JSON: {error}") from error
    return rendered.encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def _strict_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CacheIntegrityError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json_loads(payload: bytes) -> dict[str, object]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_strict_object_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                CacheIntegrityError(f"non-finite JSON number: {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CacheIntegrityError(f"cache entry is not strict UTF-8 JSON: {error}") from error
    if not isinstance(value, dict):
        raise CacheIntegrityError("cache entry must be a JSON object")
    return value


def _normalized_relative_path(value: object, name: str) -> str:
    path = _require_string(value, name)
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts or "\\" in path:
        raise CacheValidationError(f"{name} must be a normalized relative path")
    if str(pure) != path:
        raise CacheValidationError(f"{name} must be normalized")
    return path


def _parse_utc(value: object, name: str) -> datetime:
    text = _require_string(value, name, _UTC_TIMESTAMP)
    try:
        return datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError as error:
        raise CacheValidationError(f"{name} is not a valid UTC timestamp") from error


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _validate_time_window(started_at: object, finished_at: object, duration_ms: object) -> None:
    started = _parse_utc(started_at, "started_at")
    finished = _parse_utc(finished_at, "finished_at")
    duration = _require_int(duration_ms, "duration_ms")
    if finished < started:
        raise CacheValidationError("finished_at precedes started_at")
    actual_ms = round((finished - started).total_seconds() * 1000)
    if abs(actual_ms - duration) > 1:
        raise CacheValidationError("duration_ms is inconsistent with result timestamps")


def validate_key_material(value: Mapping[str, object]) -> dict[str, object]:
    """Return a detached validated v1 key object."""

    if not isinstance(value, Mapping):
        raise CacheValidationError("key material must be an object")
    key = deepcopy(dict(value))
    _exact_keys(
        key,
        {
            "schema_id",
            "schema_version",
            "contract_id",
            "gate_id",
            "scope",
            "tree_hash",
            "base_ref",
            "implementation_digest",
            "manifest_digest",
            "config_digest",
            "environment_fingerprint",
            "dependency_lock_digest",
            "receipt_schema",
        },
        "key material",
    )
    if key["schema_id"] != KEY_SCHEMA_ID or key["schema_version"] != 1:
        raise CacheValidationError("unsupported cache-key schema")
    if key["contract_id"] != CONTRACT_ID:
        raise CacheValidationError("unsupported cache contract")
    _require_string(key["gate_id"], "gate_id", _SAFE_ID)
    _require_string(key["tree_hash"], "tree_hash", _QUALIFIED_DIGEST)
    for field in (
        "implementation_digest",
        "manifest_digest",
        "config_digest",
        "environment_fingerprint",
        "dependency_lock_digest",
    ):
        _require_string(key[field], field, _SHA256)

    scope = key["scope"]
    if not isinstance(scope, dict):
        raise CacheValidationError("scope must be an object")
    _exact_keys(
        scope,
        {
            "scope_kind",
            "tree_state",
            "profile",
            "mode",
            "selection_digest",
            "repository_identity_digest",
        },
        "scope",
    )
    _require_string(scope["scope_kind"], "scope.scope_kind", _SAFE_ID)
    if scope["tree_state"] not in {"working", "staged", "commit"}:
        raise CacheValidationError("scope.tree_state is unsupported")
    if (
        scope["scope_kind"] in {"working", "staged", "commit"}
        and scope["scope_kind"] != scope["tree_state"]
    ):
        raise CacheValidationError("scope_kind and concrete tree_state are inconsistent")
    _require_string(scope["profile"], "scope.profile", _SAFE_ID)
    if scope["mode"] not in {"legacy", "shadow", "planner"}:
        raise CacheValidationError("scope.mode is unsupported")
    _require_string(scope["selection_digest"], "scope.selection_digest", _SHA256)
    _require_string(
        scope["repository_identity_digest"],
        "scope.repository_identity_digest",
        _SHA256,
    )

    base_ref = key["base_ref"]
    if not isinstance(base_ref, dict):
        raise CacheValidationError("base_ref must be an object")
    _exact_keys(base_ref, {"name", "commit"}, "base_ref")
    name = _require_string(base_ref["name"], "base_ref.name")
    commit = _require_string(base_ref["commit"], "base_ref.commit")
    if (name == "none") != (commit == "none"):
        raise CacheValidationError("base_ref name and commit must use none together")
    if commit != "none" and not _QUALIFIED_DIGEST.fullmatch(commit):
        raise CacheValidationError("base_ref.commit must be algorithm-qualified")

    receipt_schema = key["receipt_schema"]
    if not isinstance(receipt_schema, dict):
        raise CacheValidationError("receipt_schema must be an object")
    _exact_keys(
        receipt_schema,
        {
            "gate_result_id",
            "gate_result_version",
            "run_receipt_id",
            "run_receipt_version",
        },
        "receipt_schema",
    )
    expected_receipt = {
        "gate_result_id": "validation_gate_result_v1",
        "gate_result_version": 1,
        "run_receipt_id": "validation_run_receipt_v1",
        "run_receipt_version": 1,
    }
    if receipt_schema != expected_receipt:
        raise CacheValidationError("receipt_schema is not the supported v1 pair")
    _canonical_bytes(key)
    return key


def cache_key_for(value: Mapping[str, object]) -> str:
    """Return the raw hexadecimal content-addressed key."""

    key = validate_key_material(value)
    return hashlib.sha256(_canonical_bytes(key)).hexdigest()


def _validate_string_set(value: object, name: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise CacheValidationError(f"{name} must be an array of nonblank strings")
    if len(value) != len(set(value)):
        raise CacheValidationError(f"{name} must contain unique values")
    for item in value:
        _require_string(item, f"{name} item", max_bytes=512)
    return value


def _validate_full_receipt(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise CacheValidationError("full_receipt must be an object")
    _exact_keys(value, _FULL_RECEIPT_FIELDS, "full_receipt")
    _require_string(value["artifact_id"], "full_receipt.artifact_id", _SAFE_ID)
    _normalized_relative_path(value["path"], "full_receipt.path")
    _require_string(value["content_hash"], "full_receipt.content_hash", _SHA256)
    if value["local_only"] is not True or value["authoritative"] is not False:
        raise CacheValidationError("full_receipt must be local-only and non-authoritative")
    return value


def _validate_finding(value: object) -> None:
    if not isinstance(value, dict):
        raise CacheValidationError("shown finding must be an object")
    _exact_keys(value, _FINDING_FIELDS, "shown finding")
    if value["schema_id"] != "validation_finding_v1":
        raise CacheValidationError("shown finding has unsupported schema")
    _require_string(value["finding_id"], "finding_id", _FINDING_ID)
    if value["level"] not in {"ERROR", "WARN", "INFO"}:
        raise CacheValidationError("shown finding has unsupported level")
    _require_string(value["code"], "finding.code", _SAFE_ID)
    _require_string(value["message"], "finding.message", max_bytes=1_024)
    if value["artifact_ref"] is not None:
        _require_string(value["artifact_ref"], "finding.artifact_ref", _SAFE_ID)


def _validate_original_result(
    value: Mapping[str, object],
    *,
    key_material: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise CacheValidationError("original_result must be an object")
    result = deepcopy(dict(value))
    _exact_keys(result, _RESULT_FIELDS, "original_result")
    if result["schema_id"] != "validation_gate_result_v1":
        raise CacheValidationError("original_result has unsupported schema")
    if result["gate_id"] != key_material["gate_id"]:
        raise CacheValidationError("result gate_id does not match key material")
    if result["severity"] not in {"blocking", "advisory", "diagnostic"}:
        raise CacheValidationError("result severity is unsupported")
    if result["status"] != "PASS":
        raise CacheValidationError("only an original PASS may be stored")
    if result["cache_status"] not in {"MISS", "BYPASSED"}:
        raise CacheValidationError("stored PASS must be an uncached execution")
    _require_string(result["input_fingerprint"], "input_fingerprint", _SHA256)
    if result["implementation_fingerprint"] != key_material["implementation_digest"]:
        raise CacheValidationError("implementation fingerprint does not match key")
    _validate_time_window(
        result["started_at"],
        result["finished_at"],
        result["duration_ms"],
    )
    error_count = _require_int(result["error_count"], "error_count")
    warning_count = _require_int(result["warning_count"], "warning_count")
    finding_count = _require_int(result["finding_count"], "finding_count")
    shown_count = _require_int(result["shown_finding_count"], "shown_finding_count")
    if error_count or warning_count:
        raise CacheValidationError("only zero-error zero-warning PASS may be stored")
    if not isinstance(result["findings_truncated"], bool):
        raise CacheValidationError("findings_truncated must be boolean")
    if not isinstance(result["shown_findings"], list):
        raise CacheValidationError("shown_findings must be an array")
    for finding in result["shown_findings"]:
        _validate_finding(finding)
    if shown_count != len(result["shown_findings"]):
        raise CacheValidationError("shown_finding_count is inconsistent")
    if finding_count < shown_count:
        raise CacheValidationError("finding_count is smaller than shown evidence")
    if result["findings_truncated"] != (finding_count > shown_count):
        raise CacheValidationError("findings_truncated is inconsistent")
    if result["findings_truncated"]:
        raise CacheValidationError("truncated PASS evidence is not cacheable")
    shown_errors = sum(
        finding["level"] == "ERROR" for finding in result["shown_findings"]
    )
    shown_warnings = sum(
        finding["level"] == "WARN" for finding in result["shown_findings"]
    )
    if shown_errors != error_count or shown_warnings != warning_count:
        raise CacheValidationError("finding levels do not match result counts")
    if finding_count != shown_count:
        raise CacheValidationError("complete PASS finding count is inconsistent")
    _validate_full_receipt(result["full_receipt"])
    _validate_string_set(result["satisfied_obligation_ids"], "satisfied_obligation_ids")
    _validate_string_set(result["child_gate_ids"], "child_gate_ids")
    mutated = _validate_string_set(result["mutated_paths"], "mutated_paths")
    if mutated:
        raise CacheValidationError("a mutating result is not cacheable")
    _validate_string_set(result["artifact_refs"], "artifact_refs")
    return result


def _normalize_sources(values: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise CacheValidationError("source_fingerprint_manifest must be nonempty")
    normalized: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, raw in enumerate(values):
        if not isinstance(raw, Mapping):
            raise CacheValidationError(f"source fingerprint {index} must be an object")
        item = deepcopy(dict(raw))
        _exact_keys(item, _SOURCE_FIELDS, f"source fingerprint {index}")
        input_id = _require_string(item["input_id"], f"source fingerprint {index} input_id")
        _require_string(item["input_type"], f"source fingerprint {index} input_type", _SAFE_ID)
        _require_string(item["digest"], f"source fingerprint {index} digest", _QUALIFIED_DIGEST)
        if input_id in seen:
            raise CacheValidationError(f"duplicate source input_id: {input_id}")
        seen.add(input_id)
        normalized.append(item)
    normalized.sort(key=lambda item: (str(item["input_id"]), str(item["input_type"])))
    return normalized


def _entry_bytes(payload: dict[str, object]) -> bytes:
    payload["byte_size"] = 0
    for _ in range(12):
        rendered = _canonical_bytes(payload)
        measured = len(rendered)
        if payload["byte_size"] == measured:
            return rendered
        payload["byte_size"] = measured
    raise CacheValidationError("entry byte_size did not reach a stable encoding")


class ValidationCache:
    """One invocation-scoped exact-tree cache handle."""

    def __init__(
        self,
        *,
        root: Path = DEFAULT_CACHE_ROOT,
        repository_root: Path = Path("."),
        mode: str = "off",
        writer_name: str = "validation-cache",
        writer_version: str = "1",
        max_entry_bytes: int = DEFAULT_MAX_ENTRY_BYTES,
        max_entries: int = DEFAULT_MAX_ENTRIES,
        max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
        max_age_seconds: int | None = None,
        now: Callable[[], str] = _utc_now,
    ) -> None:
        if mode not in CACHE_MODES:
            raise CacheValidationError(f"unsupported cache mode: {mode}")
        _require_string(writer_name, "writer_name", _SAFE_ID)
        _require_string(writer_version, "writer_version", _SAFE_ID)
        for value, name in (
            (max_entry_bytes, "max_entry_bytes"),
            (max_entries, "max_entries"),
            (max_total_bytes, "max_total_bytes"),
        ):
            _require_int(value, name, minimum=1)
        if max_age_seconds is not None:
            _require_int(max_age_seconds, "max_age_seconds", minimum=1)
        self.root = Path(root).absolute()
        self.repository_root = Path(repository_root).absolute()
        self.mode = mode
        self.writer_name = writer_name
        self.writer_version = writer_version
        self.max_entry_bytes = max_entry_bytes
        self.max_entries = max_entries
        self.max_total_bytes = max_total_bytes
        self.max_age_seconds = max_age_seconds
        self.now = now
        self.reads_disabled = False
        self.diagnostics: list[str] = []
        if os.path.commonpath((str(self.repository_root), str(self.root))) != str(
            self.repository_root
        ):
            raise CacheValidationError("cache root must remain below the repository root")
        relative_root = self.root.relative_to(self.repository_root)
        if not relative_root.parts or relative_root.parts[0] != ".local":
            raise CacheValidationError("cache root must remain below repository .local")

    @property
    def objects_root(self) -> Path:
        return self.root / "objects"

    @property
    def locks_root(self) -> Path:
        return self.root / "locks"

    def _record_corruption(self, reason: str) -> None:
        self.reads_disabled = True
        self.diagnostics.append(reason[:240])

    def _check_owned_directory(self, path: Path, *, create: bool) -> None:
        if create:
            path.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            raise CacheIntegrityError(f"cache directory does not exist: {path}")
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise CacheIntegrityError(f"cache component is not a real directory: {path}")
        if hasattr(os, "geteuid") and metadata.st_uid != os.geteuid():
            raise CacheIntegrityError(f"cache component has unexpected owner: {path}")

    def _prepare_root(self, *, create: bool) -> None:
        relative = self.root.relative_to(self.repository_root)
        paths = [self.repository_root]
        current = self.repository_root
        for component in relative.parts:
            current = current / component
            paths.append(current)
        for path in paths:
            self._check_owned_directory(path, create=create)
        if create:
            self._check_owned_directory(self.objects_root, create=True)
            self._check_owned_directory(self.locks_root, create=True)

    def _root_exists_safely(self) -> bool:
        relative = self.root.relative_to(self.repository_root)
        current = self.repository_root
        self._check_owned_directory(current, create=False)
        for component in relative.parts:
            current = current / component
            if not os.path.lexists(current):
                return False
            self._check_owned_directory(current, create=False)
        return True

    def _entry_path(self, cache_key: str, *, create_parent: bool) -> Path:
        _require_string(cache_key, "cache_key", _HEX_64)
        path = self.objects_root / cache_key[:2] / f"{cache_key}.json"
        if os.path.commonpath((str(self.root), str(path))) != str(self.root):
            raise CacheIntegrityError("cache entry path escapes configured root")
        self._prepare_root(create=create_parent)
        if create_parent:
            self._check_owned_directory(path.parent, create=True)
        elif path.parent.exists():
            self._check_owned_directory(path.parent, create=False)
        return path

    def _lock_path(self, cache_key: str) -> Path:
        path = self.locks_root / cache_key[:2] / f"{cache_key}.lock"
        if os.path.commonpath((str(self.root), str(path))) != str(self.root):
            raise CacheIntegrityError("cache lock path escapes configured root")
        self._prepare_root(create=True)
        self._check_owned_directory(path.parent, create=True)
        return path

    def _open_lock(self, cache_key: str) -> int:
        path = self._lock_path(cache_key)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags, 0o600)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            os.close(descriptor)
            raise CacheIntegrityError("cache lock is not a regular file")
        if hasattr(os, "geteuid") and metadata.st_uid != os.geteuid():
            os.close(descriptor)
            raise CacheIntegrityError("cache lock has unexpected owner")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        return descriptor

    def _safe_file_bytes(self, path: Path, *, maximum: int) -> bytes:
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise CacheIntegrityError(f"cache reference is not a regular file: {path}")
        if hasattr(os, "geteuid") and metadata.st_uid != os.geteuid():
            raise CacheIntegrityError(f"cache reference has unexpected owner: {path}")
        if metadata.st_size > maximum:
            raise CacheIntegrityError(f"cache reference exceeds size limit: {path}")
        payload = path.read_bytes()
        if len(payload) != metadata.st_size:
            raise CacheIntegrityError(f"cache reference changed while reading: {path}")
        return payload

    def _receipt_bytes(self, receipt: Mapping[str, object]) -> bytes:
        relative = _normalized_relative_path(receipt["path"], "full_receipt.path")
        path = self.repository_root / relative
        if os.path.commonpath((str(self.repository_root), str(path))) != str(
            self.repository_root
        ):
            raise CacheIntegrityError("full receipt path escapes repository root")
        payload = self._safe_file_bytes(path, maximum=self.max_entry_bytes)
        if _sha256_bytes(payload) != receipt["content_hash"]:
            raise CacheIntegrityError("full receipt content hash does not match")
        return payload

    def _validate_entry(
        self,
        payload: bytes,
        *,
        expected_key: str | None = None,
        expected_material: Mapping[str, object] | None = None,
        expected_path: Path | None = None,
    ) -> dict[str, object]:
        if len(payload) > self.max_entry_bytes:
            raise CacheIntegrityError("cache entry exceeds the per-entry size limit")
        entry = _strict_json_loads(payload)
        _exact_keys(entry, _ENTRY_FIELDS, "cache entry")
        if entry["schema_id"] != ENTRY_SCHEMA_ID or entry["schema_version"] != 1:
            raise CacheIntegrityError("cache entry schema is unsupported")
        if entry["contract_id"] != CONTRACT_ID:
            raise CacheIntegrityError("cache entry contract is unsupported")
        material = validate_key_material(entry["key_material"])  # type: ignore[arg-type]
        computed_key = cache_key_for(material)
        cache_key = _require_string(entry["cache_key"], "cache_key", _HEX_64)
        if cache_key != computed_key:
            raise CacheIntegrityError("cache key does not match canonical key material")
        if expected_material is not None:
            requested = validate_key_material(expected_material)
            if material != requested:
                if material["tree_hash"] != requested["tree_hash"]:
                    raise CacheMismatchError("wrong_tree")
                if material["scope"] != requested["scope"]:
                    raise CacheMismatchError("wrong_scope")
                if (
                    material["implementation_digest"]
                    != requested["implementation_digest"]
                ):
                    raise CacheMismatchError("wrong_implementation")
                raise CacheMismatchError("wrong_key")
        if expected_key is not None and cache_key != expected_key:
            raise CacheMismatchError("wrong_key")
        if expected_path is not None and (
            expected_path.name != f"{cache_key}.json"
            or expected_path.parent.name != cache_key[:2]
        ):
            raise CacheIntegrityError("cache entry path does not match key")
        if entry["gate_id"] != material["gate_id"]:
            raise CacheIntegrityError("cache entry gate_id does not match key material")
        result = _validate_original_result(
            entry["original_result"],  # type: ignore[arg-type]
            key_material=material,
        )
        result_hash = _require_string(entry["result_hash"], "result_hash", _SHA256)
        if result_hash != _sha256_bytes(_canonical_bytes(result)):
            raise CacheIntegrityError("cache result hash does not match original result")
        _parse_utc(entry["created_at"], "created_at")
        writer = entry["writer"]
        if not isinstance(writer, dict):
            raise CacheIntegrityError("writer must be an object")
        _exact_keys(writer, {"name", "version"}, "writer")
        _require_string(writer["name"], "writer.name", _SAFE_ID)
        _require_string(writer["version"], "writer.version", _SAFE_ID)
        if writer != {"name": self.writer_name, "version": self.writer_version}:
            raise CacheIntegrityError("cache writer version does not match this implementation")
        sources = _normalize_sources(entry["source_fingerprint_manifest"])  # type: ignore[arg-type]
        if sources != entry["source_fingerprint_manifest"]:
            raise CacheIntegrityError("source fingerprint manifest is not canonical")
        source_hash = _require_string(
            entry["source_fingerprint_hash"],
            "source_fingerprint_hash",
            _SHA256,
        )
        if source_hash != _sha256_bytes(_canonical_bytes(sources)):
            raise CacheIntegrityError("source fingerprint hash does not match manifest")
        if result["input_fingerprint"] != source_hash:
            raise CacheIntegrityError("result input fingerprint does not match source manifest")
        receipt = entry["full_receipt"]
        _validate_full_receipt(receipt)
        if receipt != result["full_receipt"]:
            raise CacheIntegrityError("entry and result full-receipt references differ")
        self._receipt_bytes(receipt)  # type: ignore[arg-type]
        byte_size = _require_int(entry["byte_size"], "byte_size", minimum=1)
        if byte_size != len(payload):
            raise CacheIntegrityError("cache entry byte_size does not match file")
        if entry["authority"] != _AUTHORITY:
            raise CacheIntegrityError("cache authority object is not the exact v1 object")
        return entry

    def _is_expired(self, entry: Mapping[str, object]) -> bool:
        if self.max_age_seconds is None:
            return False
        created = _parse_utc(entry["created_at"], "created_at")
        current = _parse_utc(self.now(), "current time")
        return (current - created).total_seconds() > self.max_age_seconds

    def lookup(
        self,
        key_material: Mapping[str, object],
        *,
        gate_policy: str,
        mandatory_bypass: bool,
        freshness_check: Callable[[], bool],
    ) -> CacheLookup:
        """Perform one exact-key lookup and fail closed to a bounded miss."""

        if self.mode == "off":
            return CacheLookup("DISABLED", "cache_mode_off")
        if self.reads_disabled:
            return CacheLookup("DISABLED", "reads_disabled_after_corruption")
        if gate_policy not in CACHE_POLICIES:
            return CacheLookup("MISS", "gate_policy_ineligible")
        if mandatory_bypass:
            return CacheLookup("MISS", "mandatory_bypass")
        if not freshness_check():
            return CacheLookup("MISS", "snapshot_stale_before_lookup")
        try:
            material = validate_key_material(key_material)
            cache_key = cache_key_for(material)
        except CacheValidationError:
            return CacheLookup("MISS", "key_unresolved")
        try:
            if not self._root_exists_safely():
                path = self.objects_root / cache_key[:2] / f"{cache_key}.json"
                return CacheLookup("MISS", "absent", cache_key, path)
            path = self._entry_path(cache_key, create_parent=False)
            if not path.exists():
                return CacheLookup("MISS", "absent", cache_key, path)
            payload = self._safe_file_bytes(path, maximum=self.max_entry_bytes)
            entry = self._validate_entry(
                payload,
                expected_key=cache_key,
                expected_material=material,
                expected_path=path,
            )
            if self._is_expired(entry):
                return CacheLookup("MISS", "expired", cache_key, path)
            if not freshness_check():
                return CacheLookup("MISS", "snapshot_stale_before_accept", cache_key, path)
            return CacheLookup(
                "HIT",
                "exact_match",
                cache_key,
                path,
                deepcopy(entry["original_result"]),  # type: ignore[arg-type]
                str(entry["result_hash"]),
            )
        except CacheMismatchError as error:
            self._record_corruption(str(error))
            return CacheLookup("MISS", error.reason)
        except (OSError, CacheValidationError) as error:
            self._record_corruption(str(error))
            return CacheLookup("MISS", "corrupt")

    def store(
        self,
        key_material: Mapping[str, object],
        original_result: Mapping[str, object],
        *,
        source_fingerprint_manifest: Sequence[Mapping[str, object]],
        gate_policy: str,
        mandatory_bypass: bool = False,
        created_at: str | None = None,
    ) -> CacheWrite:
        """Atomically publish one clean original PASS when writes are enabled."""

        if self.mode != "read_write":
            return CacheWrite("SKIPPED", "cache_not_writable")
        if gate_policy not in CACHE_POLICIES:
            return CacheWrite("SKIPPED", "gate_policy_ineligible")
        if mandatory_bypass:
            return CacheWrite("SKIPPED", "mandatory_bypass")
        try:
            material = validate_key_material(key_material)
            result = _validate_original_result(original_result, key_material=material)
            sources = _normalize_sources(source_fingerprint_manifest)
            source_hash = _sha256_bytes(_canonical_bytes(sources))
            if result["input_fingerprint"] != source_hash:
                raise CacheValidationError(
                    "result input fingerprint does not match source manifest"
                )
            receipt = _validate_full_receipt(result["full_receipt"])
            self._receipt_bytes(receipt)
            cache_key = cache_key_for(material)
            timestamp = created_at or self.now()
            _parse_utc(timestamp, "created_at")
            entry: dict[str, object] = {
                "schema_id": ENTRY_SCHEMA_ID,
                "schema_version": 1,
                "contract_id": CONTRACT_ID,
                "key_material": material,
                "cache_key": cache_key,
                "gate_id": material["gate_id"],
                "original_result": result,
                "result_hash": _sha256_bytes(_canonical_bytes(result)),
                "created_at": timestamp,
                "writer": {"name": self.writer_name, "version": self.writer_version},
                "source_fingerprint_manifest": sources,
                "source_fingerprint_hash": source_hash,
                "full_receipt": receipt,
                "byte_size": 0,
                "authority": deepcopy(_AUTHORITY),
            }
            payload = _entry_bytes(entry)
            if len(payload) > self.max_entry_bytes:
                return CacheWrite("SKIPPED", "entry_too_large", cache_key)
            path = self._entry_path(cache_key, create_parent=True)
            lock_descriptor = self._open_lock(cache_key)
            temporary: Path | None = None
            try:
                if path.exists():
                    existing = self._safe_file_bytes(path, maximum=self.max_entry_bytes)
                    if existing == payload:
                        return CacheWrite("EXISTS", "identical_entry", cache_key, path)
                    self._record_corruption("cache-key collision with different entry bytes")
                    return CacheWrite("REJECTED", "collision", cache_key, path)
                with tempfile.NamedTemporaryFile(
                    mode="wb",
                    dir=path.parent,
                    prefix=f".{path.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as handle:
                    temporary = Path(handle.name)
                    handle.write(payload)
                    handle.flush()
                    os.fsync(handle.fileno())
                written = self._safe_file_bytes(temporary, maximum=self.max_entry_bytes)
                if written != payload:
                    raise CacheIntegrityError("temporary cache entry verification failed")
                os.replace(temporary, path)
                temporary = None
                directory_fd = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
                fcntl.flock(lock_descriptor, fcntl.LOCK_UN)
                os.close(lock_descriptor)
            try:
                self.evict()
            except (OSError, CacheValidationError) as error:
                if path.exists() and self._safe_file_bytes(
                    path, maximum=self.max_entry_bytes
                ) == payload:
                    path.unlink()
                return CacheWrite("SKIPPED", f"maintenance_failed:{error}", cache_key)
            if not path.exists():
                return CacheWrite("SKIPPED", "evicted_by_policy", cache_key, path)
            return CacheWrite("STORED", "published", cache_key, path)
        except CacheIntegrityError as error:
            self._record_corruption(str(error))
            return CacheWrite("SKIPPED", f"invalid:{error}")
        except (OSError, CacheValidationError) as error:
            return CacheWrite("SKIPPED", f"invalid:{error}")

    def _entry_files(self) -> list[Path]:
        if not self._root_exists_safely():
            return []
        if not os.path.lexists(self.objects_root):
            return []
        self._prepare_root(create=False)
        self._check_owned_directory(self.objects_root, create=False)
        files: list[Path] = []
        for shard in sorted(self.objects_root.iterdir(), key=lambda item: item.name):
            self._check_owned_directory(shard, create=False)
            for path in sorted(shard.iterdir(), key=lambda item: item.name):
                if path.suffix == ".json":
                    files.append(path)
        return files

    def evict(self) -> tuple[str, ...]:
        """Remove invalid, expired, and oldest entries until limits hold."""

        if self.mode != "read_write":
            return ()
        removed: list[str] = []
        valid: list[tuple[datetime, str, int, Path]] = []
        for path in self._entry_files():
            try:
                payload = self._safe_file_bytes(path, maximum=self.max_entry_bytes)
                entry = self._validate_entry(payload, expected_path=path)
                if self._is_expired(entry):
                    path.unlink()
                    removed.append(path.name)
                    continue
                valid.append(
                    (
                        _parse_utc(entry["created_at"], "created_at"),
                        str(entry["cache_key"]),
                        len(payload),
                        path,
                    )
                )
            except (OSError, CacheValidationError) as error:
                self._record_corruption(str(error))
                path.unlink(missing_ok=True)
                removed.append(path.name)
        valid.sort(key=lambda item: (item[0], item[1]))
        count = len(valid)
        total = sum(item[2] for item in valid)
        for _, _, size, path in valid:
            if count <= self.max_entries and total <= self.max_total_bytes:
                break
            path.unlink()
            removed.append(path.name)
            count -= 1
            total -= size
        return tuple(removed)

    def clear(self) -> int:
        """Safely remove cache entries, locks, and empty cache directories."""

        removed = 0
        if not self._root_exists_safely():
            return removed
        self._prepare_root(create=False)
        for branch in (self.objects_root, self.locks_root):
            if not branch.exists():
                continue
            self._check_owned_directory(branch, create=False)
            for shard in list(branch.iterdir()):
                self._check_owned_directory(shard, create=False)
                for path in list(shard.iterdir()):
                    file_metadata = path.lstat()
                    if stat.S_ISLNK(file_metadata.st_mode) or not stat.S_ISREG(
                        file_metadata.st_mode
                    ):
                        raise CacheIntegrityError(f"unsafe cache file: {path}")
                    path.unlink()
                    removed += 1
                shard.rmdir()
            branch.rmdir()
        self.reads_disabled = False
        self.diagnostics.clear()
        return removed

    def inspect(self) -> CacheInspection:
        """Read cache metadata without mutating entries or access times."""

        valid_count = 0
        invalid_count = 0
        total_bytes = 0
        files = self._entry_files()
        for path in files:
            try:
                payload = self._safe_file_bytes(path, maximum=self.max_entry_bytes)
                total_bytes += len(payload)
                self._validate_entry(payload, expected_path=path)
                valid_count += 1
            except (OSError, CacheValidationError):
                invalid_count += 1
        return CacheInspection(
            entry_count=len(files),
            total_bytes=total_bytes,
            valid_count=valid_count,
            invalid_count=invalid_count,
            reads_disabled=self.reads_disabled,
        )


def add_cache_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the sole v1 command-line control surface; default mode remains off."""

    parser.add_argument(
        "--cache-mode",
        choices=CACHE_MODES,
        default="off",
        help="select off, read_only, or read_write cache behavior (default: off)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="force cache mode off even when another caller selected a mode",
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--clear-cache",
        action="store_true",
        help="safely delete ignored local validation-cache state",
    )
    actions.add_argument(
        "--inspect-cache",
        action="store_true",
        help="emit a read-only bounded cache inventory",
    )


def cache_mode_from_namespace(namespace: argparse.Namespace) -> str:
    if getattr(namespace, "no_cache", False):
        return "off"
    mode = getattr(namespace, "cache_mode", "off")
    if mode not in CACHE_MODES:
        raise CacheValidationError(f"unsupported cache mode: {mode}")
    return mode


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    add_cache_arguments(parser)
    arguments = parser.parse_args(argv)
    try:
        cache = ValidationCache(
            root=arguments.cache_root,
            mode=cache_mode_from_namespace(arguments),
        )
        if arguments.clear_cache:
            payload: dict[str, object] = {
                "schema_id": "validation_cache_clear_v1",
                "removed_file_count": cache.clear(),
                "authority": "operational_validation_only",
            }
        elif arguments.inspect_cache:
            payload = cache.inspect().to_dict()
        else:
            payload = {
                "schema_id": "validation_cache_control_v1",
                "cache_mode": cache.mode,
                "default_off": cache.mode == "off",
                "authority": "operational_validation_only",
            }
    except (OSError, CacheValidationError) as error:
        payload = {
            "schema_id": "validation_cache_control_v1",
            "status": "BLOCKED_CONFIGURATION",
            "reason": str(error)[:240],
            "authority": "operational_validation_only",
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return 2
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
