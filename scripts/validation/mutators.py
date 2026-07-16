"""Deterministic mutation observation for v19 shadow validation barriers.

This module observes injected project-system writers.  It does not select
commands, restore Git state, or replace the legacy checkpoint transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable, Mapping, Sequence


class MutatorContractError(ValueError):
    """A selected mutator lacks a complete fail-closed manifest contract."""


@dataclass(frozen=True, slots=True)
class MutationDelta:
    before_tree_hash: str
    after_tree_hash: str
    before_paths: tuple[str, ...]
    after_paths: tuple[str, ...]
    changes: tuple[dict[str, str | None], ...]

    @property
    def changed_paths(self) -> tuple[str, ...]:
        return tuple(str(change["path"]) for change in self.changes)

    def to_dict(self) -> dict[str, object]:
        return {
            "before_tree_hash": self.before_tree_hash,
            "after_tree_hash": self.after_tree_hash,
            "before_paths": list(self.before_paths),
            "after_paths": list(self.after_paths),
            "changes": [dict(change) for change in self.changes],
        }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return digest.hexdigest()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_exclusions(root: Path, excluded: Iterable[Path]) -> tuple[str, ...]:
    root_resolved = root.resolve()
    values: list[str] = [".git"]
    for path in excluded:
        try:
            relative = Path(path).resolve().relative_to(root_resolved).as_posix()
        except ValueError:
            continue
        if relative not in {"", "."}:
            values.append(relative.rstrip("/"))
    return tuple(sorted(set(values)))


def snapshot_tree(root: Path, *, excluded: Iterable[Path] = ()) -> dict[str, str]:
    """Hash every file below root except Git internals and explicit receipt roots."""

    root = Path(root)
    if not root.is_dir():
        raise MutatorContractError("mutation_root must be an existing directory")
    exclusions = _relative_exclusions(root, excluded)
    snapshot: dict[str, str] = {}
    for candidate in sorted(root.rglob("*")):
        relative = candidate.relative_to(root).as_posix()
        if any(relative == prefix or relative.startswith(f"{prefix}/") for prefix in exclusions):
            continue
        if candidate.is_file() or candidate.is_symlink():
            snapshot[relative] = _sha256(candidate)
    return snapshot


def tree_hash(snapshot: Mapping[str, str]) -> str:
    payload = json.dumps(
        dict(sorted(snapshot.items())),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def mutation_delta(before: Mapping[str, str], after: Mapping[str, str]) -> MutationDelta:
    paths = sorted(set(before) | set(after))
    changes: list[dict[str, str | None]] = []
    for path in paths:
        before_hash = before.get(path)
        after_hash = after.get(path)
        if before_hash == after_hash:
            continue
        change_kind = "created" if before_hash is None else "deleted" if after_hash is None else "modified"
        changes.append(
            {
                "path": path,
                "change": change_kind,
                "before_sha256": before_hash,
                "after_sha256": after_hash,
            }
        )
    return MutationDelta(
        before_tree_hash=tree_hash(before),
        after_tree_hash=tree_hash(after),
        before_paths=tuple(sorted(before)),
        after_paths=tuple(sorted(after)),
        changes=tuple(changes),
    )


def matches_any(path: str, globs: Sequence[str]) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in globs)


def validate_allowed_globs(globs: Sequence[str], *, context: str) -> tuple[str, ...]:
    values = tuple(globs)
    if not values or any(
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or "\\" in value
        or "\x00" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
        for value in values
    ):
        raise MutatorContractError(f"{context} must contain normalized repository-relative globs")
    return values


def validate_mutator_gate(gate: Mapping[str, object]) -> tuple[str, ...]:
    gate_id = gate.get("gate_id")
    if not isinstance(gate_id, str) or not gate_id:
        raise MutatorContractError("mutator gate_id must be nonblank")
    if gate.get("mutating") is not True:
        raise MutatorContractError(f"gate is not classified as a mutator: {gate_id}")
    if gate.get("cache_policy") != "ineligible":
        raise MutatorContractError(f"mutator may not be cached: {gate_id}")
    output_globs = gate.get("output_globs")
    if not isinstance(output_globs, list):
        raise MutatorContractError(f"mutator output_globs must be an array: {gate_id}")
    return validate_allowed_globs(output_globs, context=f"{gate_id}.output_globs")


def selected_mutators(
    ordered_gate_ids: Sequence[str],
    gates: Mapping[str, Mapping[str, object]],
) -> tuple[str, ...]:
    selected: list[str] = []
    for gate_id in ordered_gate_ids:
        gate = gates[gate_id]
        if gate.get("mutating") is True:
            validate_mutator_gate(gate)
            selected.append(gate_id)
    return tuple(selected)
