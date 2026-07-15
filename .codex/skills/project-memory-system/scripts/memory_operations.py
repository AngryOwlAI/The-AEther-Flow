#!/usr/bin/env python3
"""Write-only memory-system operations and deterministic mutation receipts."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable


TRACKED_MEMORY_SURFACES = (Path("FOLDER_MAP.md"), Path("registries"), Path("wiki"))
LOCAL_RETRIEVAL_SURFACES = (
    Path(".local/content_semantics"),
    Path(".local/obsidian"),
    Path(".local/memory_index"),
)


@dataclass(frozen=True)
class ValidationFinding:
    """Stable machine-readable identity for one validation finding."""

    finding_id: str
    severity: str
    message: str


@dataclass
class ValidationReport:
    """Compatibility report with stable gate and finding metadata."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    gate_id: str = ""
    findings: list[ValidationFinding] = field(default_factory=list)
    check_ids: list[str] = field(default_factory=list)

    def error(self, message: str, *, finding_id: str = "validation.error") -> None:
        self.errors.append(message)
        self.findings.append(ValidationFinding(finding_id, "error", message))

    def warning(self, message: str, *, finding_id: str = "validation.warning") -> None:
        self.warnings.append(message)
        self.findings.append(ValidationFinding(finding_id, "warning", message))

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def counts(self) -> dict[str, object]:
        by_finding_id: dict[str, int] = {}
        for finding in self.findings:
            by_finding_id[finding.finding_id] = by_finding_id.get(finding.finding_id, 0) + 1
        return {
            "checks": len(self.check_ids),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": len(self.findings),
            "by_finding_id": dict(sorted(by_finding_id.items())),
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "status": "PASS" if self.ok else "FAIL",
            "check_ids": list(self.check_ids),
            "counts": self.counts,
            "findings": [asdict(finding) for finding in self.findings],
        }

    def print(self) -> None:
        for message in self.errors:
            print(f"ERROR: {message}")
        for message in self.warnings:
            print(f"WARNING: {message}")
        if self.ok:
            print("Validation PASS")
        else:
            print(f"Validation FAIL: {len(self.errors)} error(s)")


@dataclass(frozen=True)
class MemoryCoreSnapshot:
    """Immutable registry snapshot shared by memory-core checks."""

    rows_by_registry: Mapping[str, tuple[Mapping[str, str], ...]]

    @classmethod
    def from_rows(
        cls,
        rows_by_registry: Mapping[str, Iterable[Mapping[str, str]]],
    ) -> "MemoryCoreSnapshot":
        frozen = {
            name: tuple(MappingProxyType(dict(row)) for row in rows)
            for name, rows in rows_by_registry.items()
        }
        return cls(MappingProxyType(frozen))


@dataclass(frozen=True)
class MemoryCoreCheck:
    finding_id: str
    validate: Callable[[ValidationReport, MemoryCoreSnapshot], None]


@dataclass(frozen=True)
class MemoryCoreValidationOperations:
    load_snapshot: Callable[[], MemoryCoreSnapshot]
    checks: tuple[MemoryCoreCheck, ...]


def memory_validate_core(
    operations: MemoryCoreValidationOperations,
    *,
    snapshot: MemoryCoreSnapshot | None = None,
) -> ValidationReport:
    """Run the side-effect-free memory-core gate over one immutable snapshot."""

    resolved_snapshot = snapshot if snapshot is not None else operations.load_snapshot()
    report = ValidationReport(gate_id="memory_core")
    report.check_ids.extend(check.finding_id for check in operations.checks)
    for check in operations.checks:
        staged = ValidationReport()
        check.validate(staged, resolved_snapshot)
        for message in staged.errors:
            report.error(message, finding_id=check.finding_id)
        for message in staged.warnings:
            report.warning(message, finding_id=check.finding_id)
    return report


@dataclass(frozen=True)
class MemoryMutationReceipt:
    """Deterministic path-level receipt for one synchronization mutation."""

    changed: tuple[str, ...]
    unchanged: tuple[str, ...]
    created: tuple[str, ...]
    pruned: tuple[str, ...]
    local_retrieval_enabled: bool

    @property
    def mutated(self) -> bool:
        return bool(self.changed or self.created or self.pruned)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["changed"] = list(self.changed)
        payload["unchanged"] = list(self.unchanged)
        payload["created"] = list(self.created)
        payload["pruned"] = list(self.pruned)
        payload["mutated"] = self.mutated
        payload["counts"] = {
            "changed": len(self.changed),
            "unchanged": len(self.unchanged),
            "created": len(self.created),
            "pruned": len(self.pruned),
        }
        return payload


@dataclass(frozen=True)
class MemorySyncOperations:
    """Repository callbacks used by the write-only synchronization sequence."""

    now: Callable[[], str]
    ensure_directories: Callable[[], None]
    discover_markdown_rows: Callable[[str], list[dict[str, str]]]
    discover_tex_rows: Callable[[str], list[dict[str, str]]]
    merge_authored_registry: Callable[..., list[dict[str, str]]]
    generate_pdf_rows: Callable[..., list[dict[str, str]]]
    generate_html_rows: Callable[..., list[dict[str, str]]]
    generate_wiki: Callable[..., list[dict[str, str]]]
    generate_indexes: Callable[..., None]
    write_generated_registries: Callable[..., dict[str, list[dict[str, str]]]]
    prune_stale_generated_files: Callable[..., None]
    generate_file_object_registry: Callable[..., list[dict[str, str]]]
    generate_folder_map: Callable[..., None]
    markdown_columns: list[str]
    tex_columns: list[str]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _snapshot(repo_root: Path, include_local_retrieval: bool) -> dict[str, str]:
    surfaces = list(TRACKED_MEMORY_SURFACES)
    if include_local_retrieval:
        surfaces.extend(LOCAL_RETRIEVAL_SURFACES)
    snapshot: dict[str, str] = {}
    for relative in surfaces:
        path = repo_root / relative
        candidates = [path] if path.is_file() else sorted(path.rglob("*")) if path.exists() else []
        for candidate in candidates:
            if candidate.is_file():
                key = candidate.relative_to(repo_root).as_posix()
                snapshot[key] = _sha256(candidate)
    return snapshot


def _mutation_receipt(
    before: dict[str, str],
    after: dict[str, str],
    *,
    include_local_retrieval: bool,
) -> MemoryMutationReceipt:
    before_paths = set(before)
    after_paths = set(after)
    shared = before_paths & after_paths
    return MemoryMutationReceipt(
        changed=tuple(sorted(path for path in shared if before[path] != after[path])),
        unchanged=tuple(sorted(path for path in shared if before[path] == after[path])),
        created=tuple(sorted(after_paths - before_paths)),
        pruned=tuple(sorted(before_paths - after_paths)),
        local_retrieval_enabled=include_local_retrieval,
    )


def memory_sync(
    operations: MemorySyncOperations,
    *,
    repo_root: Path,
    refresh_existing: bool = False,
    rebuilt_pdf_paths: Iterable[str] | None = None,
    include_local_retrieval: bool = False,
) -> MemoryMutationReceipt:
    """Synchronize memory derivatives without running any validation gate."""

    before = _snapshot(repo_root, include_local_retrieval)
    operations.ensure_directories()
    now = operations.now()
    markdown_rows = operations.merge_authored_registry(
        "MARKDOWN_SOURCE_REGISTRY.csv",
        operations.markdown_columns,
        operations.discover_markdown_rows(now),
        refresh_existing,
    )
    tex_rows = operations.merge_authored_registry(
        "TEX_SOURCE_REGISTRY.csv",
        operations.tex_columns,
        operations.discover_tex_rows(now),
        refresh_existing,
    )
    pdf_rows = operations.generate_pdf_rows(
        tex_rows,
        now,
        rebuilt_pdf_paths=rebuilt_pdf_paths,
    )
    html_rows = operations.generate_html_rows(now, markdown_rows)
    rows_by_registry = {
        "MARKDOWN_SOURCE_REGISTRY.csv": markdown_rows,
        "TEX_SOURCE_REGISTRY.csv": tex_rows,
        "PDF_DERIVATIVE_REGISTRY.csv": pdf_rows,
        "HTML_EXPLAINER_REGISTRY.csv": html_rows,
    }
    wiki_rows = operations.generate_wiki(rows_by_registry, now)
    operations.generate_indexes(rows_by_registry)
    rows_by_registry["WIKI_ARTIFACT_REGISTRY.csv"] = wiki_rows
    generated_rows = operations.write_generated_registries(
        repo_root,
        rows_by_registry,
        now,
        write_semantic_text=include_local_retrieval,
    )
    rows_by_registry.update(generated_rows)
    operations.prune_stale_generated_files(
        rows_by_registry,
        include_local_retrieval=include_local_retrieval,
    )
    file_object_rows = operations.generate_file_object_registry(rows_by_registry, now)
    rows_by_registry["FILE_OBJECT_REGISTRY.csv"] = file_object_rows
    operations.generate_folder_map(rows_by_registry)
    after = _snapshot(repo_root, include_local_retrieval)
    return _mutation_receipt(
        before,
        after,
        include_local_retrieval=include_local_retrieval,
    )
