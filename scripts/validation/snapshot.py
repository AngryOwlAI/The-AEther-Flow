"""Lazy, immutable, exact-tree repository inputs for validation consumers.

The snapshot is deliberately a data boundary rather than a gate adapter.  A
caller declares the components it may use, captures one working or staged Git
state, and receives deeply immutable deterministic views.  Every access
rechecks the captured identity so cached parses cannot cross repository state.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import subprocess
import threading
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

from scripts.research_control.strict_yaml import StrictYamlError, loads as load_yaml_text


PROGRAM_STATE_PATH = "research_control/program_state.yaml"
AGENT_JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"
HANDOFF_PATTERN = re.compile(r"^research_control/handoffs/handoff-(\d{4})\.yaml$")
VALID_SCOPES = frozenset({"working", "staged"})


class RepositorySnapshotError(RuntimeError):
    """Base class for repository snapshot failures."""


class SnapshotGitError(RepositorySnapshotError):
    """Raised when Git cannot establish or inspect snapshot identity."""


class SnapshotParseError(RepositorySnapshotError):
    """Raised when a declared source is absent, malformed, or inaccessible."""


class UndeclaredComponentError(RepositorySnapshotError):
    """Raised when a caller asks for a component it did not declare."""


class StaleSnapshotError(RepositorySnapshotError):
    """Raised when repository state no longer matches the captured identity."""


def _normalize_path(path_text: str) -> str:
    text = str(path_text).strip().replace("\\", "/")
    candidate = PurePosixPath(text)
    if not text or candidate.is_absolute() or text == "." or ".." in candidate.parts:
        raise ValueError(f"repository path must be a non-empty relative path: {path_text!r}")
    return candidate.as_posix()


def _normalize_registry_path(path_text: str) -> str:
    normalized = _normalize_path(path_text)
    if "/" not in normalized:
        normalized = f"registries/{normalized}"
    return normalized


def _ordered_unique(paths: tuple[str, ...], *, registry: bool = False) -> tuple[str, ...]:
    normalize = _normalize_registry_path if registry else _normalize_path
    return tuple(sorted({normalize(path_text) for path_text in paths}))


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {
                str(key): _freeze(item)
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            }
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return tuple(sorted((_freeze(item) for item in value), key=repr))
    return value


def _configuration_fingerprint(
    request: "SnapshotRequest", configuration: Mapping[str, Any] | None
) -> str:
    payload = {
        "configuration": configuration or {},
        "request": {
            "registries": request.registries,
            "yaml_paths": request.yaml_paths,
            "include_program_state": request.include_program_state,
            "include_handoffs": request.include_handoffs,
            "include_job_completions": request.include_job_completions,
            "include_git_changed_paths": request.include_git_changed_paths,
            "source_hash_paths": request.source_hash_paths,
        },
    }
    try:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("snapshot configuration must be JSON-serializable") from exc
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class SnapshotRequest:
    """The complete component declaration for one snapshot."""

    registries: tuple[str, ...] = ()
    yaml_paths: tuple[str, ...] = ()
    include_program_state: bool = False
    include_handoffs: bool = False
    include_job_completions: bool = False
    include_git_changed_paths: bool = False
    source_hash_paths: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "registries",
            _ordered_unique(tuple(self.registries), registry=True),
        )
        object.__setattr__(self, "yaml_paths", _ordered_unique(tuple(self.yaml_paths)))
        object.__setattr__(
            self,
            "source_hash_paths",
            _ordered_unique(tuple(self.source_hash_paths)),
        )


@dataclass(frozen=True)
class TreeIdentity:
    """Stable identity of the tree and configuration captured by a snapshot."""

    repo_root: str
    git_common_dir: str
    scope: str
    base_ref: str
    base_commit: str
    head_commit: str
    tree_fingerprint: str
    configuration_fingerprint: str
    snapshot_id: str


@dataclass(frozen=True)
class SnapshotDocument:
    """One immutable YAML document and its source identity."""

    path: str
    payload: Mapping[str, Any]
    source_hash: str


@dataclass
class SnapshotInstrumentation:
    """Internal counters exposed only as an immutable point-in-time mapping."""

    file_reads: int = 0
    csv_parses: int = 0
    yaml_parses: int = 0
    hash_operations: int = 0
    git_commands: int = 0
    component_loads: int = 0
    cache_hits: int = 0
    identity_checks: int = 0
    directory_scans: int = 0
    file_reads_by_path: dict[str, int] = field(default_factory=dict)
    component_loads_by_name: dict[str, int] = field(default_factory=dict)

    def record_file_read(self, path_text: str) -> None:
        self.file_reads += 1
        self.file_reads_by_path[path_text] = self.file_reads_by_path.get(path_text, 0) + 1

    def record_component_load(self, name: str) -> None:
        self.component_loads += 1
        self.component_loads_by_name[name] = self.component_loads_by_name.get(name, 0) + 1

    def as_mapping(self) -> Mapping[str, Any]:
        return _freeze(
            {
                "cache_hits": self.cache_hits,
                "component_loads": self.component_loads,
                "component_loads_by_name": self.component_loads_by_name,
                "csv_parses": self.csv_parses,
                "directory_scans": self.directory_scans,
                "file_reads": self.file_reads,
                "file_reads_by_path": self.file_reads_by_path,
                "git_commands": self.git_commands,
                "hash_operations": self.hash_operations,
                "identity_checks": self.identity_checks,
                "yaml_parses": self.yaml_parses,
            }
        )


def _git(
    root: Path,
    instrumentation: SnapshotInstrumentation,
    *args: str,
    allowed_returncodes: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[bytes]:
    instrumentation.git_commands += 1
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode not in allowed_returncodes:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise SnapshotGitError(f"git {' '.join(args)} failed: {detail or result.returncode}")
    return result


def _git_text(
    root: Path,
    instrumentation: SnapshotInstrumentation,
    *args: str,
) -> str:
    return _git(root, instrumentation, *args).stdout.decode("utf-8").strip()


def _untracked_paths(root: Path, instrumentation: SnapshotInstrumentation) -> tuple[str, ...]:
    raw = _git(
        root,
        instrumentation,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
    ).stdout
    return tuple(
        sorted(
            {
                _normalize_path(os.fsdecode(item))
                for item in raw.split(b"\0")
                if item
            }
        )
    )


def _hash_untracked_file(root: Path, path_text: str, digest: Any) -> None:
    path = root / path_text
    digest.update(path_text.encode("utf-8", errors="surrogateescape"))
    digest.update(b"\0")
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return
    if not path.is_file():
        digest.update(b"non-file\0")
        return
    digest.update(b"file\0")
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)


def _tree_fingerprint(
    root: Path,
    instrumentation: SnapshotInstrumentation,
    *,
    scope: str,
    base_commit: str,
) -> str:
    digest = hashlib.sha256()
    digest.update(scope.encode("ascii"))
    digest.update(b"\0")
    digest.update(base_commit.encode("ascii"))
    digest.update(b"\0")
    if scope == "staged":
        tree = _git_text(root, instrumentation, "write-tree")
        digest.update(tree.encode("ascii"))
        return digest.hexdigest()

    diff = _git(
        root,
        instrumentation,
        "diff",
        "--no-ext-diff",
        "--binary",
        "--full-index",
        base_commit,
        "--",
    ).stdout
    digest.update(diff)
    for path_text in _untracked_paths(root, instrumentation):
        digest.update(b"\0")
        _hash_untracked_file(root, path_text, digest)
    return digest.hexdigest()


class RepositorySnapshot:
    """A lazy, parse-once snapshot tied to one exact Git state."""

    def __init__(
        self,
        *,
        root: Path,
        request: SnapshotRequest,
        identity: TreeIdentity,
        instrumentation: SnapshotInstrumentation,
    ) -> None:
        self._root = root
        self._request = request
        self._identity = identity
        self._instrumentation = instrumentation
        self._source_bytes: dict[str, bytes] = {}
        self._source_hashes: dict[str, str] = {}
        self._components: dict[str, Any] = {}
        self._lock = threading.RLock()

    @classmethod
    def capture(
        cls,
        repo_root: Path | str,
        request: SnapshotRequest,
        *,
        scope: str = "working",
        base_ref: str = "HEAD",
        configuration: Mapping[str, Any] | None = None,
    ) -> "RepositorySnapshot":
        """Capture identity without reading any declared source component."""

        if scope not in VALID_SCOPES:
            raise ValueError(f"scope must be one of {sorted(VALID_SCOPES)}")
        if not str(base_ref).strip():
            raise ValueError("base_ref must be non-empty")

        instrumentation = SnapshotInstrumentation()
        root = Path(repo_root).expanduser().resolve()
        top_level = Path(
            _git_text(root, instrumentation, "rev-parse", "--show-toplevel")
        ).resolve()
        if top_level != root:
            raise SnapshotGitError(
                f"repo_root must be the Git top level: expected {top_level}, got {root}"
            )

        common_text = _git_text(root, instrumentation, "rev-parse", "--git-common-dir")
        common_dir = Path(common_text)
        if not common_dir.is_absolute():
            common_dir = root / common_dir
        common_dir = common_dir.resolve()

        head_commit = _git_text(root, instrumentation, "rev-parse", "HEAD")
        base_commit = _git_text(root, instrumentation, "rev-parse", str(base_ref))
        tree_fingerprint = _tree_fingerprint(
            root,
            instrumentation,
            scope=scope,
            base_commit=base_commit,
        )
        config_fingerprint = _configuration_fingerprint(request, configuration)
        snapshot_material = "\0".join(
            (
                str(root),
                str(common_dir),
                scope,
                str(base_ref),
                base_commit,
                head_commit,
                tree_fingerprint,
                config_fingerprint,
            )
        ).encode("utf-8")
        snapshot_id = hashlib.sha256(snapshot_material).hexdigest()
        identity = TreeIdentity(
            repo_root=str(root),
            git_common_dir=str(common_dir),
            scope=scope,
            base_ref=str(base_ref),
            base_commit=base_commit,
            head_commit=head_commit,
            tree_fingerprint=tree_fingerprint,
            configuration_fingerprint=config_fingerprint,
            snapshot_id=snapshot_id,
        )
        return cls(
            root=root,
            request=request,
            identity=identity,
            instrumentation=instrumentation,
        )

    @property
    def identity(self) -> TreeIdentity:
        return self._identity

    @property
    def request(self) -> SnapshotRequest:
        return self._request

    @property
    def instrumentation(self) -> Mapping[str, Any]:
        with self._lock:
            return self._instrumentation.as_mapping()

    def assert_fresh(self) -> None:
        """Reject reuse after the Git root, base, HEAD, or captured tree changes."""

        with self._lock:
            self._instrumentation.identity_checks += 1
            top_level = Path(
                _git_text(
                    self._root,
                    self._instrumentation,
                    "rev-parse",
                    "--show-toplevel",
                )
            ).resolve()
            common_text = _git_text(
                self._root,
                self._instrumentation,
                "rev-parse",
                "--git-common-dir",
            )
            common_dir = Path(common_text)
            if not common_dir.is_absolute():
                common_dir = self._root / common_dir
            common_dir = common_dir.resolve()
            head_commit = _git_text(
                self._root,
                self._instrumentation,
                "rev-parse",
                "HEAD",
            )
            base_commit = _git_text(
                self._root,
                self._instrumentation,
                "rev-parse",
                self._identity.base_ref,
            )
            tree_fingerprint = _tree_fingerprint(
                self._root,
                self._instrumentation,
                scope=self._identity.scope,
                base_commit=base_commit,
            )
            observed = (
                str(top_level),
                str(common_dir),
                head_commit,
                base_commit,
                tree_fingerprint,
            )
            expected = (
                self._identity.repo_root,
                self._identity.git_common_dir,
                self._identity.head_commit,
                self._identity.base_commit,
                self._identity.tree_fingerprint,
            )
            if observed != expected:
                raise StaleSnapshotError(
                    "repository state changed after snapshot capture "
                    f"(snapshot_id={self._identity.snapshot_id})"
                )

    def _record_component(self, name: str) -> None:
        self._instrumentation.record_component_load(name)

    def _cached_component(self, name: str) -> Any | None:
        if name not in self._components:
            return None
        self.assert_fresh()
        self._instrumentation.cache_hits += 1
        return self._components[name]

    def _read_source(self, path_text: str) -> bytes:
        normalized = _normalize_path(path_text)
        cached = self._source_bytes.get(normalized)
        if cached is not None:
            self.assert_fresh()
            self._instrumentation.cache_hits += 1
            return cached

        self.assert_fresh()
        if self._identity.scope == "staged":
            result = _git(
                self._root,
                self._instrumentation,
                "show",
                f":{normalized}",
                allowed_returncodes=(0, 128),
            )
            if result.returncode != 0:
                raise SnapshotParseError(f"{normalized}: source is absent from staged tree")
            raw = result.stdout
        else:
            ignored = _git(
                self._root,
                self._instrumentation,
                "check-ignore",
                "-q",
                "--",
                normalized,
                allowed_returncodes=(0, 1),
            )
            if ignored.returncode == 0:
                raise SnapshotParseError(
                    f"{normalized}: ignored sources cannot participate in a working snapshot"
                )
            path = (self._root / normalized).resolve()
            try:
                path.relative_to(self._root)
            except ValueError as exc:
                raise SnapshotParseError(f"{normalized}: source resolves outside repository") from exc
            if not path.is_file():
                raise SnapshotParseError(f"{normalized}: source file is missing")
            try:
                raw = path.read_bytes()
            except OSError as exc:
                raise SnapshotParseError(f"{normalized}: cannot read source: {exc}") from exc

        self._instrumentation.record_file_read(normalized)
        self._instrumentation.hash_operations += 1
        source_hash = hashlib.sha256(raw).hexdigest()
        self.assert_fresh()
        self._source_bytes[normalized] = raw
        self._source_hashes[normalized] = source_hash
        return raw

    def _parse_csv(self, path_text: str) -> tuple[Mapping[str, str], ...]:
        raw = self._read_source(path_text)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SnapshotParseError(f"{path_text}: CSV is not UTF-8") from exc
        self._instrumentation.csv_parses += 1
        try:
            reader = csv.DictReader(io.StringIO(text, newline=""))
            headers = reader.fieldnames
            if not headers or any(not str(header).strip() for header in headers):
                raise SnapshotParseError(f"{path_text}: CSV header is missing or blank")
            if len(headers) != len(set(headers)):
                raise SnapshotParseError(f"{path_text}: CSV headers are duplicated")
            rows: list[Mapping[str, str]] = []
            for line_number, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    raise SnapshotParseError(
                        f"{path_text}:{line_number}: CSV row does not match header"
                    )
                rows.append(_freeze({str(key): str(value) for key, value in row.items()}))
        except csv.Error as exc:
            raise SnapshotParseError(f"{path_text}: malformed CSV: {exc}") from exc
        return tuple(rows)

    def _parse_yaml(self, path_text: str) -> Mapping[str, Any]:
        raw = self._read_source(path_text)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SnapshotParseError(f"{path_text}: YAML is not UTF-8") from exc
        self._instrumentation.yaml_parses += 1
        try:
            payload = load_yaml_text(text)
        except StrictYamlError as exc:
            raise SnapshotParseError(f"{path_text}: strict YAML parse failed: {exc}") from exc
        return _freeze(payload)

    def _registry_rows(
        self,
        path_text: str,
        *,
        require_declared: bool,
    ) -> tuple[Mapping[str, str], ...]:
        normalized = _normalize_registry_path(path_text)
        if require_declared and normalized not in self._request.registries:
            raise UndeclaredComponentError(f"registry was not declared: {normalized}")
        key = f"registry:{normalized}"
        cached = self._cached_component(key)
        if cached is not None:
            return cached
        self._record_component(key)
        rows = self._parse_csv(normalized)
        self._components[key] = rows
        return rows

    def registry_rows(self, path_text: str) -> tuple[Mapping[str, str], ...]:
        with self._lock:
            return self._registry_rows(path_text, require_declared=True)

    def yaml_document(self, path_text: str) -> Mapping[str, Any]:
        with self._lock:
            normalized = _normalize_path(path_text)
            if normalized not in self._request.yaml_paths:
                raise UndeclaredComponentError(f"YAML source was not declared: {normalized}")
            key = f"yaml:{normalized}"
            cached = self._cached_component(key)
            if cached is not None:
                return cached
            self._record_component(key)
            payload = self._parse_yaml(normalized)
            self._components[key] = payload
            return payload

    def program_state(self) -> Mapping[str, Any]:
        with self._lock:
            if not self._request.include_program_state:
                raise UndeclaredComponentError("program_state was not declared")
            key = "program_state"
            cached = self._cached_component(key)
            if cached is not None:
                return cached
            self._record_component(key)
            payload = self._parse_yaml(PROGRAM_STATE_PATH)
            self._components[key] = payload
            return payload

    def _scope_paths(self, prefix: str) -> tuple[str, ...]:
        self.assert_fresh()
        self._instrumentation.directory_scans += 1
        if self._identity.scope == "staged":
            raw = _git(
                self._root,
                self._instrumentation,
                "ls-files",
                "-z",
                "--",
                prefix,
            ).stdout
            candidates = (os.fsdecode(item) for item in raw.split(b"\0") if item)
        else:
            base = self._root / prefix
            candidates = (
                path.relative_to(self._root).as_posix()
                for path in base.glob("*.yaml")
                if path.is_file()
            )
        paths = tuple(sorted({_normalize_path(path_text) for path_text in candidates}))
        self.assert_fresh()
        return paths

    def handoffs(self) -> tuple[SnapshotDocument, ...]:
        with self._lock:
            if not self._request.include_handoffs:
                raise UndeclaredComponentError("handoffs were not declared")
            key = "handoffs"
            cached = self._cached_component(key)
            if cached is not None:
                return cached
            self._record_component(key)
            numbered_paths = [
                (int(match.group(1)), path_text)
                for path_text in self._scope_paths("research_control/handoffs")
                if (match := HANDOFF_PATTERN.fullmatch(path_text))
            ]
            documents = tuple(
                SnapshotDocument(
                    path=path_text,
                    payload=self._parse_yaml(path_text),
                    source_hash=self._source_hashes[path_text],
                )
                for _, path_text in sorted(numbered_paths)
            )
            self._components[key] = documents
            return documents

    def job_completions(self) -> tuple[SnapshotDocument, ...]:
        with self._lock:
            if not self._request.include_job_completions:
                raise UndeclaredComponentError("job_completions were not declared")
            key = "job_completions"
            cached = self._cached_component(key)
            if cached is not None:
                return cached
            self._record_component(key)
            rows = self._registry_rows(AGENT_JOB_REGISTRY_PATH, require_declared=False)
            paths = tuple(
                sorted(
                    {
                        _normalize_path(str(row["completion_path"]).strip())
                        for row in rows
                        if str(row.get("completion_path", "")).strip()
                    }
                )
            )
            documents = tuple(
                SnapshotDocument(
                    path=path_text,
                    payload=self._parse_yaml(path_text),
                    source_hash=self._source_hashes[path_text],
                )
                for path_text in paths
            )
            self._components[key] = documents
            return documents

    def changed_paths(self) -> tuple[str, ...]:
        with self._lock:
            if not self._request.include_git_changed_paths:
                raise UndeclaredComponentError("git_changed_paths were not declared")
            key = "git_changed_paths"
            cached = self._cached_component(key)
            if cached is not None:
                return cached
            self._record_component(key)
            self.assert_fresh()
            args = ["diff"]
            if self._identity.scope == "staged":
                args.append("--cached")
            args.extend(("--name-only", "-z", self._identity.base_commit, "--"))
            raw = _git(self._root, self._instrumentation, *args).stdout
            paths = {
                _normalize_path(os.fsdecode(item))
                for item in raw.split(b"\0")
                if item
            }
            if self._identity.scope == "working":
                paths.update(_untracked_paths(self._root, self._instrumentation))
            result = tuple(sorted(paths))
            self.assert_fresh()
            self._components[key] = result
            return result

    def source_hash(self, path_text: str) -> str:
        with self._lock:
            normalized = _normalize_path(path_text)
            directly_declared = (
                normalized in self._request.source_hash_paths
                or normalized in self._request.registries
                or normalized in self._request.yaml_paths
                or (
                    self._request.include_program_state
                    and normalized == PROGRAM_STATE_PATH
                )
            )
            if not directly_declared and normalized not in self._source_hashes:
                raise UndeclaredComponentError(f"source hash was not declared: {normalized}")
            if normalized not in self._source_hashes:
                self._read_source(normalized)
            else:
                self.assert_fresh()
                self._instrumentation.cache_hits += 1
            return self._source_hashes[normalized]

    def source_hashes(self) -> Mapping[str, str]:
        with self._lock:
            for path_text in self._request.source_hash_paths:
                if path_text not in self._source_hashes:
                    self._read_source(path_text)
            self.assert_fresh()
            return _freeze(dict(sorted(self._source_hashes.items())))
