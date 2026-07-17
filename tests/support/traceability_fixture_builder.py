"""Minimal filesystem fixtures for support-traceability validator tests."""

from __future__ import annotations

import copy
import csv
import io
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from scripts.research_control import strict_yaml


V1_REGISTRY_PATH = (
    "research_control/design/support_formalization_traceability_registry_v1.yaml"
)
V18_REGISTRY_PATH = (
    "research_control/design/support_formalization_traceability_registry_v18.yaml"
)
PNF_REGISTRY_PATH = "registries/PROOF_NORMAL_FORM_REGISTRY.csv"


def dump_fixture_yaml(data: dict[str, Any]) -> str:
    """Render strict-YAML list maps in the parser's accepted inline-key form."""

    source_lines = strict_yaml.dumps(data).splitlines()
    output: list[str] = []
    index = 0
    while index < len(source_lines):
        line = source_lines[index]
        indent = len(line) - len(line.lstrip(" "))
        if (
            line.strip() == "-"
            and index + 1 < len(source_lines)
            and len(source_lines[index + 1])
            - len(source_lines[index + 1].lstrip(" "))
            == indent + 2
            and ":" in source_lines[index + 1].strip()
        ):
            output.append(
                f"{' ' * indent}- {source_lines[index + 1].strip()}"
            )
            index += 2
            continue
        output.append(line)
        index += 1
    return "\n".join(output) + "\n"


@dataclass(frozen=True)
class FixtureBuild:
    registry_path: str
    entry_ids: tuple[str, ...]
    files: tuple[str, ...]
    file_count: int
    byte_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "byte_count": self.byte_count,
            "entry_ids": list(self.entry_ids),
            "file_count": self.file_count,
            "files": list(self.files),
            "registry_path": self.registry_path,
        }


class TraceabilityFixtureBuilder:
    """Materialize only registry and selected-entry dependencies."""

    def __init__(self, source_root: Path, fixture_root: Path) -> None:
        self.source_root = source_root
        self.fixture_root = fixture_root
        self._written: set[str] = set()

    @staticmethod
    def _safe_path(rel_path: str) -> PurePosixPath:
        path = PurePosixPath(rel_path)
        if path.is_absolute() or ".." in path.parts or rel_path == "":
            raise ValueError(f"fixture path must be repository-relative: {rel_path}")
        return path

    def _write(self, rel_path: str, payload: bytes) -> None:
        path = self._safe_path(rel_path)
        destination = self.fixture_root.joinpath(*path.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        self._written.add(rel_path)

    def _copy(self, rel_path: str) -> None:
        if rel_path in self._written:
            return
        path = self._safe_path(rel_path)
        source = self.source_root.joinpath(*path.parts)
        if not source.is_file():
            raise FileNotFoundError(f"fixture source is not a file: {rel_path}")
        self._write(rel_path, source.read_bytes())

    @staticmethod
    def _select_entries(
        registry: dict[str, Any], entry_ids: Iterable[str] | None
    ) -> list[dict[str, Any]]:
        entries = registry.get("entries")
        if not isinstance(entries, list):
            raise ValueError("traceability registry entries must be a list")
        requested = None if entry_ids is None else tuple(entry_ids)
        if requested is None:
            return copy.deepcopy(entries)
        by_id = {
            str(entry.get("entry_id", "")): entry
            for entry in entries
            if isinstance(entry, dict)
        }
        missing = [entry_id for entry_id in requested if entry_id not in by_id]
        if missing:
            raise ValueError(f"unknown traceability fixture entries: {missing}")
        return [copy.deepcopy(by_id[entry_id]) for entry_id in requested]

    def _finish(
        self, registry_path: str, entries: list[dict[str, Any]]
    ) -> FixtureBuild:
        files = tuple(sorted(self._written))
        return FixtureBuild(
            registry_path=registry_path,
            entry_ids=tuple(str(entry["entry_id"]) for entry in entries),
            files=files,
            file_count=len(files),
            byte_count=sum((self.fixture_root / path).stat().st_size for path in files),
        )

    def build_v1(
        self,
        entry_ids: Iterable[str] | None = None,
        *,
        registry_path: str = V1_REGISTRY_PATH,
    ) -> FixtureBuild:
        registry = strict_yaml.load(self.source_root / registry_path)
        entries = self._select_entries(registry, entry_ids)
        for entry in entries:
            for path in entry.get("formalization_files", []):
                self._copy(str(path))
            self._copy(str(entry["report_path"]))
            self._copy(str(entry["traceability_path"]))
            for field in (
                "canonical_source_artifacts",
                "support_dependency_artifacts",
            ):
                for artifact in entry.get(field, []):
                    self._copy(str(artifact["path"]))
        minimal_registry = copy.deepcopy(registry)
        minimal_registry["entries"] = entries
        self._write(
            registry_path,
            dump_fixture_yaml(minimal_registry).encode("utf-8"),
        )
        return self._finish(registry_path, entries)

    def build_v18(
        self,
        entry_ids: Iterable[str] | None = None,
        *,
        registry_path: str = V18_REGISTRY_PATH,
        pnf_registry_path: str = PNF_REGISTRY_PATH,
    ) -> FixtureBuild:
        registry = strict_yaml.load(self.source_root / registry_path)
        entries = self._select_entries(registry, entry_ids)
        for entry in entries:
            for field in ("source_artifacts", "tool_artifacts"):
                for artifact in entry.get(field, []):
                    self._copy(str(artifact["path"]))
            self._copy(str(entry["report_path"]))

        minimal_registry = copy.deepcopy(registry)
        minimal_registry["entries"] = entries
        self._write(
            registry_path,
            dump_fixture_yaml(minimal_registry).encode("utf-8"),
        )
        self._write_pnf_rows(
            pnf_registry_path,
            {
                str(entry["proof_normal_form_row_id"])
                for entry in entries
            },
        )
        return self._finish(registry_path, entries)

    def _write_pnf_rows(self, rel_path: str, row_ids: set[str]) -> None:
        source = self.source_root / rel_path
        with source.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames
            rows = [
                row
                for row in reader
                if row.get("proof_normal_form_row_id") in row_ids
            ]
        if fieldnames is None:
            raise ValueError("proof-normal-form registry has no header")
        found = {str(row["proof_normal_form_row_id"]) for row in rows}
        missing = sorted(row_ids - found)
        if missing:
            raise ValueError(f"missing proof-normal-form fixture rows: {missing}")
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        self._write(rel_path, output.getvalue().encode("utf-8"))
