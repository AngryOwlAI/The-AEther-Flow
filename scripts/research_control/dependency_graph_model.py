"""Immutable input snapshots for the research dependency graph."""

from __future__ import annotations

import csv
import hashlib
import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping

try:
    from strict_yaml import StrictYamlError, loads as load_yaml_text
except ModuleNotFoundError:  # Package import during tests and library use.
    from .strict_yaml import StrictYamlError, loads as load_yaml_text


PROGRAM_STATE_PATH = "research_control/program_state.yaml"
AGENT_JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass
class GraphInstrumentation:
    """Operational counters for one snapshot/build/render transaction."""

    source_loads: int = 0
    graph_builds: int = 0
    render_calls: int = 0
    source_loads_by_path: dict[str, int] = field(default_factory=dict)
    renders_by_format: dict[str, int] = field(default_factory=dict)

    def record_source_load(self, path_text: str) -> None:
        self.source_loads += 1
        self.source_loads_by_path[path_text] = self.source_loads_by_path.get(path_text, 0) + 1

    def record_graph_build(self) -> None:
        self.graph_builds += 1

    def record_render(self, format_name: str) -> None:
        self.render_calls += 1
        self.renders_by_format[format_name] = self.renders_by_format.get(format_name, 0) + 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_loads": self.source_loads,
            "graph_builds": self.graph_builds,
            "render_calls": self.render_calls,
            "source_loads_by_path": dict(sorted(self.source_loads_by_path.items())),
            "renders_by_format": dict(sorted(self.renders_by_format.items())),
        }


@dataclass(frozen=True)
class SnapshotSource:
    path: str
    source_hash: str
    payload: Any
    parse_error: str = ""


@dataclass(frozen=True)
class GraphInputSnapshot:
    """One tree-bound, deeply immutable graph extraction."""

    repo_root: Path
    registry_paths: tuple[str, ...]
    handoff_paths: tuple[str, ...]
    sources: Mapping[str, SnapshotSource]

    def source_hash(self, path_text: str) -> str:
        source = self.sources.get(path_text)
        return source.source_hash if source else ""

    def csv_rows(self, path_text: str) -> list[dict[str, str]]:
        source = self.sources.get(path_text)
        if not source or source.parse_error:
            return []
        rows = _thaw(source.payload)
        return rows if isinstance(rows, list) else []

    def yaml_payload(self, path_text: str) -> dict[str, Any]:
        source = self.sources.get(path_text)
        if not source or source.parse_error:
            return {}
        payload = _thaw(source.payload)
        return payload if isinstance(payload, dict) else {}

    def parse_error(self, path_text: str) -> str:
        source = self.sources.get(path_text)
        return source.parse_error if source else "source not captured"

    @property
    def source_hashes(self) -> Mapping[str, str]:
        return MappingProxyType(
            {path_text: source.source_hash for path_text, source in self.sources.items()}
        )


def _csv_payload(text: str) -> list[dict[str, str]]:
    return [
        {key: value or "" for key, value in row.items()}
        for row in csv.DictReader(io.StringIO(text, newline=""))
    ]


def _handoff_number(path: Path) -> int:
    match = re.fullmatch(r"handoff-(\d{4})\.yaml", path.name)
    return int(match.group(1)) if match else -1


def load_graph_input_snapshot(
    repo_root: Path,
    *,
    registry_paths: Iterable[str],
    instrumentation: GraphInstrumentation | None = None,
) -> GraphInputSnapshot:
    """Read every graph input at most once and return an immutable snapshot."""

    root = repo_root.resolve()
    ordered_registry_paths = tuple(dict.fromkeys(registry_paths))
    loaded: dict[str, SnapshotSource] = {}

    def load_source(path_text: str, source_type: str) -> SnapshotSource:
        existing = loaded.get(path_text)
        if existing is not None:
            return existing
        if instrumentation is not None:
            instrumentation.record_source_load(path_text)
        path = root / path_text
        if not path.exists() or not path.is_file():
            source = SnapshotSource(path_text, "", _freeze({}), "source missing")
            loaded[path_text] = source
            return source
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            if source_type == "csv":
                payload: Any = _csv_payload(text)
            else:
                payload = load_yaml_text(text)
            source = SnapshotSource(
                path=path_text,
                source_hash=hashlib.sha256(raw).hexdigest(),
                payload=_freeze(payload),
            )
        except (OSError, UnicodeDecodeError, StrictYamlError, csv.Error) as exc:
            source = SnapshotSource(path_text, "", _freeze({}), str(exc))
        loaded[path_text] = source
        return source

    for registry_path in ordered_registry_paths:
        load_source(registry_path, "csv")
    load_source(PROGRAM_STATE_PATH, "yaml")

    job_source = loaded.get(AGENT_JOB_REGISTRY_PATH)
    job_rows = _thaw(job_source.payload) if job_source and not job_source.parse_error else []
    completion_paths = sorted(
        {
            str(row.get("completion_path", "")).strip()
            for row in job_rows
            if isinstance(row, dict) and str(row.get("completion_path", "")).strip()
        }
    )
    for completion_path in completion_paths:
        load_source(completion_path, "yaml")

    handoff_dir = root / "research_control" / "handoffs"
    handoff_paths = tuple(
        path.relative_to(root).as_posix()
        for path in sorted(handoff_dir.glob("handoff-*.yaml"), key=_handoff_number)
    )
    for handoff_path in handoff_paths:
        load_source(handoff_path, "yaml")

    return GraphInputSnapshot(
        repo_root=root,
        registry_paths=ordered_registry_paths,
        handoff_paths=handoff_paths,
        sources=MappingProxyType(dict(loaded)),
    )
