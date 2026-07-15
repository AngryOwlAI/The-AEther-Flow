#!/usr/bin/env python3
"""Write-only memory-system operations and deterministic mutation receipts."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable


TRACKED_MEMORY_SURFACES = (Path("FOLDER_MAP.md"), Path("registries"), Path("wiki"))
LOCAL_RETRIEVAL_SURFACES = (
    Path(".local/content_semantics"),
    Path(".local/obsidian"),
    Path(".local/memory_index"),
)


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
