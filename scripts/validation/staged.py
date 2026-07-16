#!/usr/bin/env python3
"""Rollback-safe final staged-tree acceptance for the v19 shadow epoch.

The caller supplies the already-authoritative legacy outcomes and a bounded
executor for the selected non-mutating checkpoint gates.  This module stages
one allowlisted transaction, binds every shadow result to the exact Git index
tree, rejects residue or comparison drift, and restores the entry index.  It
does not commit, run generators, or make planner output authoritative.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Callable, Iterable, Mapping, Sequence

from scripts.validation.plan import PlannerError, ValidationPlan
from scripts.validation.profiles import ProfileError, resolve_profile


TREE_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
PASS_STATUSES = {"PASS"}


class StagedAcceptanceError(RuntimeError):
    """An internal fail-closed staged-acceptance finding."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = dict(details or {})


@dataclass(frozen=True, slots=True)
class GateOutcome:
    gate_id: str
    status: str
    scope: str
    tree_hash: str

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value
            for value in (self.gate_id, self.status, self.scope, self.tree_hash)
        ):
            raise ValueError("gate outcomes require nonblank string fields")

    def to_dict(self) -> dict[str, str]:
        return {
            "gate_id": self.gate_id,
            "status": self.status,
            "scope": self.scope,
            "tree_hash": self.tree_hash,
        }


@dataclass(frozen=True, slots=True)
class StagedExecutionContext:
    repo_root: Path
    base_ref: str
    scope: str
    tree_hash: str
    staged_paths: tuple[str, ...]
    agent_job_id: str
    allowlist_digest: str


Classifier = Callable[..., dict[str, object]]
GateExecutor = Callable[
    [tuple[str, ...], StagedExecutionContext], Sequence[GateOutcome]
]
LegacyStatusProvider = Callable[[tuple[str, ...]], Mapping[str, str]]


def _git(repo_root: Path, *arguments: str) -> bytes:
    try:
        result = subprocess.run(
            ("git", *arguments),
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise StagedAcceptanceError("git_execution_failed", str(error)) from error
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise StagedAcceptanceError(
            "git_command_failed",
            message or f"git {' '.join(arguments)} failed",
            details={"command": ["git", *arguments], "exit_code": result.returncode},
        )
    return result.stdout


def _write_tree(repo_root: Path) -> str:
    tree = _git(repo_root, "write-tree").decode("ascii", errors="strict").strip()
    if not TREE_RE.fullmatch(tree):
        raise StagedAcceptanceError(
            "invalid_index_tree", "git write-tree returned an invalid object ID"
        )
    return tree


def _tree_identity(tree: str) -> str:
    algorithm = "sha1" if len(tree) == 40 else "sha256"
    return f"git-{algorithm}:{tree}"


def _normalize_paths(paths: Iterable[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for raw in paths:
        path = str(raw)
        pure = PurePosixPath(path)
        if (
            not path
            or path.startswith("/")
            or "\\" in path
            or "\0" in path
            or any(part in {"", ".", ".."} for part in pure.parts)
            or pure.as_posix() != path
        ):
            raise StagedAcceptanceError(
                "invalid_transaction_path",
                "transaction paths must be normalized repository-relative paths",
                details={"path": path},
            )
        normalized.add(path)
    if not normalized:
        raise StagedAcceptanceError(
            "empty_transaction", "staged acceptance requires at least one path"
        )
    return tuple(sorted(normalized))


def _normalize_globs(globs: Iterable[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for raw in globs:
        pattern = str(raw)
        parts = PurePosixPath(pattern).parts
        if (
            not pattern
            or pattern.startswith("/")
            or "\\" in pattern
            or "\0" in pattern
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise StagedAcceptanceError(
                "invalid_agentjob_allowlist",
                "allowlist globs must be normalized and repository-relative",
                details={"pattern": pattern},
            )
        normalized.add(pattern)
    if not normalized:
        raise StagedAcceptanceError(
            "empty_agentjob_allowlist", "the active AgentJob allowlist is required"
        )
    return tuple(sorted(normalized))


def _allowed(path: str, globs: Sequence[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatchcase(path, pattern) for pattern in globs)


def _parse_name_status(payload: bytes) -> list[dict[str, object]]:
    fields = payload.split(b"\0")
    changes: list[dict[str, object]] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index].decode("ascii", errors="strict")
        index += 1
        path_count = 2 if status.startswith(("R", "C")) else 1
        if index + path_count > len(fields):
            raise StagedAcceptanceError(
                "truncated_git_diff", "git name-status output was truncated"
            )
        paths = tuple(
            value.decode("utf-8", errors="surrogateescape")
            for value in fields[index : index + path_count]
            if value
        )
        if len(paths) != path_count:
            raise StagedAcceptanceError(
                "truncated_git_diff", "git name-status output omitted a path"
            )
        changes.append({"status": status, "paths": list(paths)})
        index += path_count
    return changes


def _changed_paths(changes: Sequence[Mapping[str, object]]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                str(path)
                for change in changes
                for path in change.get("paths", [])  # type: ignore[union-attr]
            }
        )
    )


def _staged_changes(repo_root: Path, base_ref: str) -> list[dict[str, object]]:
    return _parse_name_status(
        _git(
            repo_root,
            "diff",
            "--cached",
            "--name-status",
            "-z",
            "--find-renames",
            base_ref,
            "--",
        )
    )


def _unstaged_paths(repo_root: Path) -> tuple[str, ...]:
    tracked = _changed_paths(
        _parse_name_status(
            _git(repo_root, "diff", "--name-status", "-z", "--find-renames", "--")
        )
    )
    untracked = tuple(
        value.decode("utf-8", errors="surrogateescape")
        for value in _git(
            repo_root, "ls-files", "--others", "--exclude-standard", "-z"
        ).split(b"\0")
        if value
    )
    return tuple(sorted(set(tracked) | set(untracked)))


def _working_plan_record(
    working_plan: ValidationPlan | Mapping[str, object] | None,
) -> dict[str, object]:
    if working_plan is None:
        return {
            "recorded": False,
            "scope": "working",
            "selected_gate_ids": [],
            "tree_hash": "",
            "staged_reusable": False,
        }
    document = working_plan.to_dict() if isinstance(working_plan, ValidationPlan) else dict(working_plan)
    scopes = document.get("scopes")
    scope = document.get("scope")
    if isinstance(scopes, list):
        scope = scopes[0] if scopes == ["working"] else ""
    if scope != "working":
        raise StagedAcceptanceError(
            "working_plan_scope_invalid",
            "working and staged plans must remain separate",
        )
    return {
        "recorded": True,
        "scope": "working",
        "selected_gate_ids": sorted(
            str(value) for value in document.get("selected_gate_ids", [])
        ),
        "tree_hash": str(document.get("tree_hash", "")),
        "staged_reusable": False,
    }


def _required_staged_gates(
    plan: ValidationPlan, manifest: Mapping[str, object]
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    raw_gates = manifest.get("gates")
    if not isinstance(raw_gates, list):
        raise StagedAcceptanceError("invalid_manifest", "manifest gates are unavailable")
    gates = {
        str(gate.get("gate_id")): gate
        for gate in raw_gates
        if isinstance(gate, dict)
    }
    required: list[str] = []
    legacy_owned_mutators: list[str] = []
    for gate_id in plan.ordered_gate_ids:
        gate = gates.get(gate_id)
        if gate is None:
            raise StagedAcceptanceError(
                "invalid_manifest", f"selected gate {gate_id} is undeclared"
            )
        if bool(gate.get("mutating")):
            legacy_owned_mutators.append(gate_id)
        elif gate.get("severity") == "blocking":
            required.append(gate_id)
    if not required:
        raise StagedAcceptanceError(
            "empty_staged_plan", "checkpoint plan selected no staged blocking gates"
        )
    return tuple(required), tuple(legacy_owned_mutators)


def _evidence_reuse_audit(
    evidence: Iterable[Mapping[str, object]], context: StagedExecutionContext
) -> dict[str, object]:
    rejections: list[dict[str, str]] = []
    for item in evidence:
        scope = str(item.get("scope", ""))
        tree_hash = str(item.get("tree_hash", ""))
        if scope == "working" or "tree_state=working" in scope:
            reason = "working_scope_cannot_satisfy_staged"
        elif scope != context.scope:
            reason = "scope_mismatch"
        elif tree_hash != context.tree_hash:
            reason = "tree_identity_mismatch"
        else:
            reason = "shadow_epoch_reuse_disabled"
        rejections.append(
            {
                "gate_id": str(item.get("gate_id", "")),
                "reason": reason,
                "scope": scope,
                "tree_hash": tree_hash,
            }
        )
    return {
        "accepted_gate_ids": [],
        "rejections": rejections,
        "policy": "execute_each_selected_staged_gate_once_in_shadow_epoch",
    }


def _base_receipt(base_ref: str, agent_job_id: str) -> dict[str, object]:
    return {
        "schema_id": "validation_staged_acceptance_receipt_v1",
        "status": "BLOCKED_CONFIGURATION",
        "exit_code": 2,
        "run_id": "",
        "scope": "staged",
        "evidence_scope": f"tree_state=index;base_ref={base_ref}",
        "base_ref": base_ref,
        "tree_hash": "",
        "agent_job_id": agent_job_id,
        "allowlist_digest": "",
        "staged_paths": [],
        "staged_changes": [],
        "plans": {
            "working": {
                "recorded": False,
                "scope": "working",
                "selected_gate_ids": [],
                "tree_hash": "",
                "staged_reusable": False,
            },
            "staged": {},
        },
        "execution": {
            "call_count": 0,
            "required_gate_ids": [],
            "legacy_owned_mutating_gate_ids": [],
            "gate_results": [],
        },
        "residue": {"before_execution": [], "after_execution": []},
        "shadow_comparison": {
            "status": "NOT_RUN",
            "compared_gate_ids": [],
            "mismatches": {},
        },
        "evidence_reuse": {"accepted_gate_ids": [], "rejections": []},
        "index": {
            "entry_tree": "",
            "final_staged_tree": "",
            "post_execution_tree": "",
            "restored_tree": "",
            "restored": False,
        },
        "checks": {
            "agentjob_allowlist": "NOT_RUN",
            "unstaged_residue": "NOT_RUN",
            "staged_tree_integrity": "NOT_RUN",
            "entry_index_restoration": "NOT_RUN",
        },
        "finding": {},
        "authority": {
            "operational_validation_only": True,
            "legacy_result_authoritative": True,
            "planner_result_authoritative": False,
            "repository_acceptance": False,
            "commit_performed": False,
            "physics_claim_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "proof_authority": False,
            "gate_chair_authority": False,
        },
    }


def _record_finding(receipt: dict[str, object], error: StagedAcceptanceError) -> None:
    receipt["status"] = "BLOCKED_CONFIGURATION"
    receipt["exit_code"] = 2
    receipt["finding"] = {
        "code": error.code,
        "message": " ".join(str(error).split()),
        "details": error.details,
    }


def run_staged_acceptance(
    repo_root: Path,
    *,
    transaction_paths: Iterable[str],
    allowed_path_globs: Iterable[str],
    manifest: Mapping[str, object],
    classifier: Classifier,
    gate_executor: GateExecutor,
    legacy_status_provider: LegacyStatusProvider,
    prior_evidence: Iterable[Mapping[str, object]] = (),
    working_plan: ValidationPlan | Mapping[str, object] | None = None,
    base_ref: str = "HEAD",
    agent_job_id: str = "",
) -> dict[str, object]:
    """Run one rollback-safe shadow acceptance against an exact staged tree."""

    repo_root = Path(repo_root).resolve()
    receipt = _base_receipt(base_ref, agent_job_id)
    entry_tree = ""
    error: StagedAcceptanceError | None = None

    try:
        if (
            not base_ref
            or base_ref.startswith("-")
            or any(character.isspace() for character in base_ref)
            or "\0" in base_ref
        ):
            raise StagedAcceptanceError("invalid_base_ref", "base_ref is invalid")
        paths = _normalize_paths(transaction_paths)
        globs = _normalize_globs(allowed_path_globs)
        receipt["allowlist_digest"] = "sha256:" + hashlib.sha256(
            json.dumps(globs, ensure_ascii=False, separators=(",", ":")).encode()
        ).hexdigest()
        outside = [path for path in paths if not _allowed(path, globs)]
        if outside:
            raise StagedAcceptanceError(
                "path_outside_agentjob_allowlist",
                "transaction paths exceed the active AgentJob allowlist",
                details={"paths": outside},
            )
        receipt["checks"]["agentjob_allowlist"] = "PASS"  # type: ignore[index]

        entry_tree = _write_tree(repo_root)
        receipt["index"]["entry_tree"] = entry_tree  # type: ignore[index]
        _git(repo_root, "add", "-A", "--", *paths)

        changes = _staged_changes(repo_root, base_ref)
        staged_paths = _changed_paths(changes)
        receipt["staged_changes"] = changes
        receipt["staged_paths"] = list(staged_paths)
        if not staged_paths:
            raise StagedAcceptanceError(
                "empty_staged_tree_delta", "the staged transaction has no changes"
            )
        outside_transaction = [path for path in staged_paths if path not in paths]
        if outside_transaction:
            raise StagedAcceptanceError(
                "staged_path_outside_transaction",
                "the Git index contains paths outside the exact transaction set",
                details={"paths": outside_transaction},
            )
        outside = [path for path in staged_paths if not _allowed(path, globs)]
        if outside:
            receipt["checks"]["agentjob_allowlist"] = "FAIL"  # type: ignore[index]
            raise StagedAcceptanceError(
                "path_outside_agentjob_allowlist",
                "the final staged tree exceeds the active AgentJob allowlist",
                details={"paths": outside},
            )

        residue = _unstaged_paths(repo_root)
        receipt["residue"]["before_execution"] = list(residue)  # type: ignore[index]
        if residue:
            receipt["checks"]["unstaged_residue"] = "FAIL"  # type: ignore[index]
            raise StagedAcceptanceError(
                "unstaged_transaction_residue",
                "unstaged or untracked transaction residue remains after staging",
                details={"paths": list(residue)},
            )
        receipt["checks"]["unstaged_residue"] = "PASS"  # type: ignore[index]

        final_tree = _write_tree(repo_root)
        tree_hash = _tree_identity(final_tree)
        scope = f"tree_state=index;base_ref={base_ref}"
        receipt["tree_hash"] = tree_hash
        receipt["run_id"] = f"STAGED-{final_tree[:16]}"
        receipt["index"]["final_staged_tree"] = final_tree  # type: ignore[index]
        context = StagedExecutionContext(
            repo_root=repo_root,
            base_ref=base_ref,
            scope=scope,
            tree_hash=tree_hash,
            staged_paths=staged_paths,
            agent_job_id=agent_job_id,
            allowlist_digest=str(receipt["allowlist_digest"]),
        )

        try:
            classification = classifier(staged_paths, registry_root=repo_root)
        except Exception as classifier_error:
            raise StagedAcceptanceError(
                "classification_failed", str(classifier_error)
            ) from classifier_error
        if not isinstance(classification, dict):
            raise StagedAcceptanceError(
                "classification_failed", "classifier did not return an object"
            )
        resolution = resolve_profile(
            manifest,
            classification,
            requested_profile="checkpoint",
            scopes=("staged",),
            shadow=True,
        )
        plan = resolution.plan
        if (
            plan.status != "READY"
            or plan.scopes != ("staged",)
            or plan.blocked_paths
            or plan.unknown_paths
        ):
            raise StagedAcceptanceError(
                "unknown_or_blocked_path",
                "the staged checkpoint plan is not safely executable",
                details={
                    "status": plan.status,
                    "blocked_paths": list(plan.blocked_paths),
                    "unknown_paths": list(plan.unknown_paths),
                },
            )
        if plan.execution_authority != "legacy" or not resolution.comparison_required:
            raise StagedAcceptanceError(
                "shadow_authority_changed",
                "P6-T04 requires legacy authority and planner comparison",
            )
        required, legacy_owned_mutators = _required_staged_gates(plan, manifest)
        receipt["plans"] = {
            "working": _working_plan_record(working_plan),
            "staged": plan.to_dict(),
        }
        receipt["execution"]["required_gate_ids"] = list(required)  # type: ignore[index]
        receipt["execution"]["legacy_owned_mutating_gate_ids"] = list(  # type: ignore[index]
            legacy_owned_mutators
        )
        receipt["evidence_reuse"] = _evidence_reuse_audit(prior_evidence, context)

        try:
            outcomes = tuple(gate_executor(required, context))
        except Exception as executor_error:
            raise StagedAcceptanceError(
                "gate_executor_failed", str(executor_error)
            ) from executor_error
        receipt["execution"]["call_count"] = 1  # type: ignore[index]
        if any(not isinstance(outcome, GateOutcome) for outcome in outcomes):
            raise StagedAcceptanceError(
                "invalid_gate_outcome", "gate executor returned an invalid outcome"
            )
        counts = Counter(outcome.gate_id for outcome in outcomes)
        if (
            set(counts) != set(required)
            or any(count != 1 for count in counts.values())
            or len(outcomes) != len(required)
        ):
            raise StagedAcceptanceError(
                "gate_execution_cardinality",
                "each selected staged gate must execute exactly once per identity",
                details={
                    "required_gate_ids": list(required),
                    "observed_counts": dict(sorted(counts.items())),
                },
            )
        for outcome in outcomes:
            if outcome.scope != scope or outcome.tree_hash != tree_hash:
                raise StagedAcceptanceError(
                    "gate_evidence_identity_mismatch",
                    "gate outcome is not bound to the final staged identity",
                    details={"gate_id": outcome.gate_id},
                )
        receipt["execution"]["gate_results"] = [  # type: ignore[index]
            outcome.to_dict() for outcome in outcomes
        ]

        post_tree = _write_tree(repo_root)
        receipt["index"]["post_execution_tree"] = post_tree  # type: ignore[index]
        if post_tree != final_tree:
            receipt["checks"]["staged_tree_integrity"] = "FAIL"  # type: ignore[index]
            raise StagedAcceptanceError(
                "staged_tree_changed",
                "a staged gate changed the exact index tree",
                details={"expected": final_tree, "observed": post_tree},
            )
        receipt["checks"]["staged_tree_integrity"] = "PASS"  # type: ignore[index]

        after_residue = _unstaged_paths(repo_root)
        receipt["residue"]["after_execution"] = list(after_residue)  # type: ignore[index]
        if after_residue:
            receipt["checks"]["unstaged_residue"] = "FAIL"  # type: ignore[index]
            raise StagedAcceptanceError(
                "unstaged_transaction_residue_after_execution",
                "staged gates left working-tree residue",
                details={"paths": list(after_residue)},
            )

        try:
            legacy_statuses = dict(legacy_status_provider(required))
        except Exception as comparison_error:
            raise StagedAcceptanceError(
                "legacy_shadow_comparison_failed", str(comparison_error)
            ) from comparison_error
        planner_statuses = {outcome.gate_id: outcome.status for outcome in outcomes}
        missing = sorted(set(required) - set(legacy_statuses))
        extras = sorted(set(legacy_statuses) - set(required))
        if missing or extras:
            raise StagedAcceptanceError(
                "legacy_shadow_incomplete",
                "legacy comparison does not cover the affected blocking gates exactly",
                details={"missing": missing, "extras": extras},
            )
        mismatches = {
            gate_id: {
                "legacy": legacy_statuses[gate_id],
                "planner": planner_statuses[gate_id],
            }
            for gate_id in required
            if legacy_statuses[gate_id] != planner_statuses[gate_id]
        }
        receipt["shadow_comparison"] = {
            "status": "FAIL" if mismatches else "PASS",
            "compared_gate_ids": list(required),
            "mismatches": mismatches,
        }
        if mismatches:
            raise StagedAcceptanceError(
                "legacy_shadow_mismatch",
                "legacy and planner outcomes differ for affected blocking gates",
                details={"gate_ids": sorted(mismatches)},
            )
        if any(outcome.status not in PASS_STATUSES for outcome in outcomes):
            receipt["status"] = "FAIL"
            receipt["exit_code"] = 1
        else:
            receipt["status"] = "PASS"
            receipt["exit_code"] = 0
    except (PlannerError, ProfileError, StagedAcceptanceError, TypeError, ValueError) as caught:
        error = (
            caught
            if isinstance(caught, StagedAcceptanceError)
            else StagedAcceptanceError("staged_acceptance_error", str(caught))
        )
    finally:
        if entry_tree:
            try:
                _git(repo_root, "read-tree", entry_tree)
                restored_tree = _write_tree(repo_root)
                receipt["index"]["restored_tree"] = restored_tree  # type: ignore[index]
                restored = restored_tree == entry_tree
                receipt["index"]["restored"] = restored  # type: ignore[index]
                receipt["checks"]["entry_index_restoration"] = (  # type: ignore[index]
                    "PASS" if restored else "FAIL"
                )
                if not restored:
                    error = StagedAcceptanceError(
                        "index_restore_failed",
                        "the entry Git index tree was not restored exactly",
                        details={"expected": entry_tree, "observed": restored_tree},
                    )
            except StagedAcceptanceError as restore_error:
                error = StagedAcceptanceError(
                    "index_restore_failed",
                    str(restore_error),
                    details=restore_error.details,
                )
                receipt["checks"]["entry_index_restoration"] = "FAIL"  # type: ignore[index]

    if error is not None:
        _record_finding(receipt, error)
    return receipt
