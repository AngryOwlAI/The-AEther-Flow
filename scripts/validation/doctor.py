#!/usr/bin/env python3
"""Run bounded, non-authoritative local-retrieval health diagnostics."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_SCRIPT_DIR = (
    REPO_ROOT / ".codex" / "skills" / "project-memory-system" / "scripts"
)
for import_path in (REPO_ROOT, MEMORY_SCRIPT_DIR):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

import obsidian_wiki_lib as memory  # noqa: E402
from scripts.project_control.classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.plan import load_manifest  # noqa: E402
from scripts.validation.profiles import (  # noqa: E402
    build_membership_audit,
    resolve_profile,
)


SCHEMA_ID = "validation_doctor_receipt_v1"
SUPPORTED_SCOPES = ("local_retrieval",)
DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_RECEIPT_ROOT = Path(".local/validation-receipts/doctor")
DEFAULT_SEARCH_QUERY = "Lorentzian metric"
RUN_ID_PATTERN = re.compile(r"RUN-DOCTOR-[A-Za-z0-9][A-Za-z0-9._-]{0,96}")
STATUS_PRIORITY = {"SKIPPED": 0, "PASS": 1, "WARN": 2, "FAIL": 3}
AdvisoryRunner = Callable[[Sequence[str], Path, int], Mapping[str, object]]


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def diagnostic(
    gate_id: str,
    status: str,
    summary: str,
    *,
    details: object | None = None,
) -> dict[str, object]:
    if status not in STATUS_PRIORITY:
        raise ValueError(f"unsupported doctor status: {status}")
    return {
        "gate_id": gate_id,
        "status": status,
        "summary": summary,
        "details": {} if details is None else details,
        "authority": "local_only_non_authoritative",
    }


def default_advisory_runner(
    command: Sequence[str],
    cwd: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "command": list(command),
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "command": list(command),
            "exit_code": None,
            "stdout": error.stdout or "",
            "stderr": error.stderr or "",
            "timed_out": True,
        }
    except OSError as error:
        return {
            "command": list(command),
            "exit_code": None,
            "stdout": "",
            "stderr": str(error),
            "timed_out": False,
        }


def command_diagnostic(
    gate_id: str,
    command: Sequence[str],
    *,
    cwd: Path,
    runner: AdvisoryRunner,
    timeout_seconds: int = 300,
) -> dict[str, object]:
    raw = dict(runner(command, cwd, timeout_seconds))
    exit_code = raw.get("exit_code")
    timed_out = raw.get("timed_out") is True
    status = "PASS" if exit_code == 0 and not timed_out else "WARN"
    summary = (
        "advisory command completed"
        if status == "PASS"
        else "advisory command reported an operational finding"
    )
    return diagnostic(gate_id, status, summary, details=raw)


def environment_diagnostic(runtime_root: Path) -> dict[str, object]:
    required = [
        runtime_root / ".codex/skills/project-memory-system/scripts/obsidian_wiki_lib.py",
        runtime_root / "scripts/validation/profiles.py",
        runtime_root / "research_control/design/validation_gate_manifest_v1.yaml",
    ]
    missing = [path.relative_to(runtime_root).as_posix() for path in required if not path.is_file()]
    fts5_available = True
    fts5_error = ""
    try:
        connection = sqlite3.connect(":memory:")
        try:
            connection.execute("CREATE VIRTUAL TABLE doctor_fts USING fts5(text)")
        finally:
            connection.close()
    except sqlite3.Error as error:
        fts5_available = False
        fts5_error = str(error)
    details = {
        "python_executable": sys.executable,
        "python_version": ".".join(str(value) for value in sys.version_info[:3]),
        "cpython": sys.implementation.name == "cpython",
        "sqlite_version": sqlite3.sqlite_version,
        "sqlite_fts5_available": fts5_available,
        "sqlite_fts5_error": fts5_error,
        "pymupdf_available": importlib.util.find_spec("fitz") is not None,
        "missing_runtime_paths": missing,
    }
    failed = bool(missing) or not fts5_available
    return diagnostic(
        "environment_health",
        "FAIL" if failed else "PASS",
        "doctor runtime is incomplete" if failed else "doctor runtime is available",
        details=details,
    )


def profile_diagnostic(
    manifest_path: Path,
    scope: str,
) -> tuple[dict[str, object], dict[str, object]]:
    try:
        manifest = load_manifest(manifest_path)
        resolution = resolve_profile(
            manifest,
            classify_paths([]),
            requested_profile="doctor",
            scopes=(scope,),
        )
        audit = build_membership_audit(manifest)
        selected = list(resolution.plan.selected_gate_ids)
        blocking = list(audit["doctor_blocking_gate_ids"])
        overlap = list(audit["doctor_checkpoint_obligation_overlap"])
        checkpoint_selected = "checkpoint_transaction" in selected
        failed = bool(blocking or overlap or checkpoint_selected)
        details = {
            "requested_profile": resolution.requested_profile,
            "effective_profile": resolution.effective_profile,
            "selected_gate_ids": selected,
            "ordered_gate_ids": list(resolution.plan.ordered_gate_ids),
            "doctor_blocking_gate_ids": blocking,
            "doctor_checkpoint_obligation_overlap": overlap,
            "checkpoint_transaction_selected": checkpoint_selected,
            "planner_executes_commands": False,
            "execution_authority": resolution.plan.execution_authority,
        }
        result = diagnostic(
            "doctor_profile_contract",
            "FAIL" if failed else "PASS",
            "doctor profile violates separation"
            if failed
            else "doctor profile remains advisory and checkpoint-separated",
            details=details,
        )
        return result, resolution.to_dict()
    except (OSError, RuntimeError, ValueError) as error:
        result = diagnostic(
            "doctor_profile_contract",
            "FAIL",
            "doctor profile could not be resolved",
            details={"error": str(error)},
        )
        return result, {}


def git_tracked_state_fingerprint(repo_root: Path) -> dict[str, object]:
    command_sets = (
        ("diff", "--binary"),
        ("diff", "--cached", "--binary"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
    )
    outputs: list[bytes] = []
    try:
        for arguments in command_sets:
            completed = subprocess.run(
                ["git", *arguments],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            outputs.append(completed.stdout)
    except (OSError, subprocess.CalledProcessError):
        return {"available": False, "sha256": ""}
    digest = hashlib.sha256()
    for output in outputs:
        digest.update(output)
        digest.update(b"\0")
    return {"available": True, "sha256": digest.hexdigest()}


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def refresh_local_retrieval(
    repo_root: Path,
    vault: Path,
    index_path: Path,
) -> dict[str, object]:
    rows_by_registry = memory.load_rows_by_registry(repo_root)
    semantic_rows = memory.generate_content_semantic_rows(
        repo_root,
        rows_by_registry,
        memory.utc_now(),
        write_text=True,
    )
    memory.ensure_vault(repo_root, vault)
    memory.write_vault(repo_root, vault, rows_by_registry)
    memory.build_memory_index(repo_root, index_path)
    return {
        "vault_path": vault.as_posix(),
        "index_path": index_path.as_posix(),
        "semantic_extract_count": len(semantic_rows),
        "mutation_scope": "ignored_local_retrieval_only",
    }


def refresh_diagnostic(
    repo_root: Path,
    vault: Path,
    index_path: Path,
    *,
    requested: bool,
) -> dict[str, object]:
    if not requested:
        return diagnostic(
            "local_retrieval_sync",
            "SKIPPED",
            "local refresh was not requested",
            details={"refresh_requested": False, "read_only_default": True},
        )
    local_root = repo_root / ".local"
    outside_local = [
        str(path)
        for path in (vault, index_path)
        if not is_within(path, local_root)
    ]
    if outside_local:
        return diagnostic(
            "local_retrieval_sync",
            "FAIL",
            "requested refresh targets escape the ignored local boundary",
            details={
                "refresh_requested": True,
                "allowed_root": str(local_root.resolve()),
                "rejected_targets": outside_local,
            },
        )
    before = git_tracked_state_fingerprint(repo_root)
    try:
        refresh_details = refresh_local_retrieval(repo_root, vault, index_path)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
        return diagnostic(
            "local_retrieval_sync",
            "FAIL",
            "requested local refresh could not complete",
            details={"refresh_requested": True, "error": str(error)},
        )
    after = git_tracked_state_fingerprint(repo_root)
    tracked_state_changed = (
        before.get("available") is True
        and after.get("available") is True
        and before.get("sha256") != after.get("sha256")
    )
    details = {
        "refresh_requested": True,
        "tracked_state_before": before,
        "tracked_state_after": after,
        "tracked_state_changed": tracked_state_changed,
        **refresh_details,
    }
    return diagnostic(
        "local_retrieval_sync",
        "FAIL" if tracked_state_changed else "PASS",
        "refresh changed tracked repository state"
        if tracked_state_changed
        else "requested local refresh completed without tracked mutation",
        details=details,
    )


def status_diagnostic(
    repo_root: Path,
    vault: Path,
    index_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    try:
        payload = memory.status(repo_root, vault, index_path)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
        result = diagnostic(
            "memory_status_diagnostic",
            "FAIL",
            "memory status could not be inspected",
            details={"error": str(error)},
        )
        return result, {}
    local_status = str(payload.get("local_retrieval_status", "WARN"))
    result = diagnostic(
        "memory_status_diagnostic",
        "PASS" if local_status == "PASS" else "WARN",
        "local retrieval is fresh"
        if local_status == "PASS"
        else "local retrieval has non-authoritative freshness findings",
        details=payload,
    )
    return result, payload


def lint_diagnostic(repo_root: Path, vault: Path) -> dict[str, object]:
    try:
        issues = memory.lint_vault(repo_root, vault, require_index=True)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
        return diagnostic(
            "local_retrieval_lint",
            "FAIL",
            "local vault lint could not run",
            details={"error": str(error)},
        )
    return diagnostic(
        "local_retrieval_lint",
        "WARN" if issues else "PASS",
        f"local vault lint reported {len(issues)} issue(s)"
        if issues
        else "local vault lint passed",
        details={"issue_count": len(issues), "issues": issues},
    )


def lookup_diagnostic(repo_root: Path) -> dict[str, object]:
    try:
        rows = memory.source_rows_with_registry(memory.load_rows_by_registry(repo_root))
        identifier = str(rows[0].get("object_id", "")) if rows else ""
        payload = memory.lookup_object(repo_root, identifier) if identifier else {}
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
        return diagnostic(
            "memory_lookup_diagnostic",
            "WARN",
            "memory lookup smoke could not complete",
            details={"error": str(error)},
        )
    match_count = int(payload.get("match_count", 0)) if payload else 0
    return diagnostic(
        "memory_lookup_diagnostic",
        "PASS" if match_count else "WARN",
        "memory lookup smoke returned a canonical row"
        if match_count
        else "memory lookup smoke returned no canonical row",
        details={"identifier": identifier, "match_count": match_count, "payload": payload},
    )


def search_diagnostic(
    repo_root: Path,
    index_path: Path,
    query: str,
) -> dict[str, object]:
    try:
        payload = memory.search_index(repo_root, query, None, 5, index_path)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
        return diagnostic(
            "memory_search_diagnostic",
            "WARN",
            "memory search smoke reported an operational failure",
            details={"query": query, "error": str(error)},
        )
    results = payload.get("results", [])
    degraded = bool(payload.get("error") or payload.get("fts_error") or not results)
    return diagnostic(
        "memory_search_diagnostic",
        "WARN" if degraded else "PASS",
        "memory search smoke reported an operational finding"
        if degraded
        else "memory search smoke returned results",
        details=payload,
    )


def aggregate_status(results: Sequence[Mapping[str, object]]) -> str:
    highest = max(
        (STATUS_PRIORITY.get(str(result.get("status")), STATUS_PRIORITY["FAIL"]) for result in results),
        default=STATUS_PRIORITY["FAIL"],
    )
    return next(status for status, priority in STATUS_PRIORITY.items() if priority == highest)


def status_counts(results: Sequence[Mapping[str, object]]) -> dict[str, int]:
    counts = {status.lower() + "_count": 0 for status in STATUS_PRIORITY}
    for result in results:
        key = str(result.get("status", "FAIL")).lower() + "_count"
        counts[key] = counts.get(key, 0) + 1
    counts["check_count"] = len(results)
    return counts


def normalized_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def write_receipt(
    receipt: Mapping[str, object],
    receipt_root: Path,
    run_id: str,
) -> tuple[Path, str]:
    receipt_root.mkdir(parents=True, exist_ok=True)
    path = receipt_root / f"{run_id}.json"
    payload = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=receipt_root,
            prefix=f".{run_id}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return path, hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_doctor(
    repo_root: Path,
    *,
    scope: str = "local_retrieval",
    refresh: bool = False,
    vault: Path | None = None,
    index_path: Path | None = None,
    search_query: str = DEFAULT_SEARCH_QUERY,
    manifest_path: Path = DEFAULT_MANIFEST,
    receipt_root: Path | None = None,
    run_id: str | None = None,
    advisory_runner: AdvisoryRunner = default_advisory_runner,
    runtime_root: Path = REPO_ROOT,
) -> tuple[dict[str, object], Path, str]:
    repo_root = repo_root.resolve()
    if scope not in SUPPORTED_SCOPES:
        raise ValueError(f"unsupported doctor scope: {scope}")
    if not search_query.strip():
        raise ValueError("search query must be nonblank")
    run_id = run_id or (
        "RUN-DOCTOR-"
        + hashlib.sha256(f"{os.getpid()}:{time.time_ns()}".encode("utf-8")).hexdigest()[:16]
    )
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run ID must be a path-safe RUN-DOCTOR identity")
    vault = (vault or memory.vault_root(repo_root)).resolve()
    index_path = (index_path or memory.memory_index_path(repo_root)).resolve()
    receipt_root = receipt_root or repo_root / DEFAULT_RECEIPT_ROOT
    if not receipt_root.is_absolute():
        receipt_root = repo_root / receipt_root

    results: list[dict[str, object]] = []
    profile_result, profile_payload = profile_diagnostic(manifest_path, scope)
    results.append(profile_result)
    results.append(environment_diagnostic(runtime_root))
    results.append(
        refresh_diagnostic(
            repo_root,
            vault,
            index_path,
            requested=refresh,
        )
    )
    status_result, status_payload = status_diagnostic(repo_root, vault, index_path)
    results.extend(
        [
            status_result,
            lint_diagnostic(repo_root, vault),
            lookup_diagnostic(repo_root),
            search_diagnostic(repo_root, index_path, search_query),
        ]
    )

    python = sys.executable
    results.extend(
        [
            command_diagnostic(
                "route_signature_diagnostic",
                (
                    python,
                    "scripts/research_control/render_route_diagnostics.py",
                    "--check",
                    "--repo-root",
                    str(repo_root),
                    "--summary",
                ),
                cwd=runtime_root,
                runner=advisory_runner,
            ),
            command_diagnostic(
                "route_orbit_diagnostic",
                (
                    python,
                    "scripts/research_control/validate_route_orbits.py",
                    "--advisory-only",
                    "--repo-root",
                    str(repo_root),
                    "--summary",
                ),
                cwd=runtime_root,
                runner=advisory_runner,
            ),
            command_diagnostic(
                "continue_context_resolution",
                (
                    python,
                    "scripts/research_control/continue_research.py",
                    "--summary",
                ),
                cwd=repo_root,
                runner=advisory_runner,
            ),
        ]
    )

    aggregate = aggregate_status(results)
    counts = status_counts(results)
    selected_gate_ids = (
        profile_payload.get("plan", {}).get("selected_gate_ids", [])
        if isinstance(profile_payload.get("plan"), dict)
        else []
    )
    compact = {
        "schema_id": "validation_doctor_compact_summary_v1",
        "status": aggregate,
        "scope": scope,
        "refresh_requested": refresh,
        "core_validation_status": status_payload.get("core_validation_status", "UNKNOWN"),
        "local_retrieval_status": status_payload.get("local_retrieval_status", "UNKNOWN"),
        "selected_gate_count": len(selected_gate_ids),
        **counts,
        "authority": "local_only_non_authoritative",
    }
    receipt = {
        "schema_id": SCHEMA_ID,
        "run_id": run_id,
        "status": aggregate,
        "scope": scope,
        "request": {
            "refresh": refresh,
            "search_query": search_query,
            "repo_root": str(repo_root),
            "vault": str(vault),
            "index_path": str(index_path),
        },
        "profile_resolution": profile_payload,
        "results": results,
        "counts": counts,
        "compact_summary": compact,
        "separation": {
            "read_only_default": not refresh,
            "refresh_is_explicit": True,
            "tracked_core_status": status_payload.get("core_validation_status", "UNKNOWN"),
            "local_retrieval_status": status_payload.get("local_retrieval_status", "UNKNOWN"),
            "doctor_blocking_gate_ids": profile_result.get("details", {}).get(
                "doctor_blocking_gate_ids", []
            ),
            "doctor_checkpoint_obligation_overlap": profile_result.get("details", {}).get(
                "doctor_checkpoint_obligation_overlap", []
            ),
            "checkpoint_transaction_selected": profile_result.get("details", {}).get(
                "checkpoint_transaction_selected", False
            ),
        },
        "authority": {
            "operational_diagnostics_only": True,
            "local_only": True,
            "repository_acceptance_authority": False,
            "checkpoint_authority": False,
            "scientific_claim_authority": False,
            "proof_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "gate_chair_authority": False,
        },
    }
    receipt_path, receipt_sha256 = write_receipt(receipt, receipt_root, run_id)
    compact["receipt_path"] = normalized_path(repo_root, receipt_path)
    compact["receipt_sha256"] = receipt_sha256
    return compact, receipt_path, receipt_sha256


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=SUPPORTED_SCOPES, default="local_retrieval")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Explicitly refresh ignored local retrieval state before diagnosis.",
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--vault", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--search-query", default=DEFAULT_SEARCH_QUERY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--run-id")
    parser.add_argument("--json", action="store_true", help="Emit compact JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        compact, receipt_path, _receipt_sha256 = run_doctor(
            args.repo_root,
            scope=args.scope,
            refresh=args.refresh,
            vault=args.vault,
            index_path=args.index,
            search_query=args.search_query,
            manifest_path=args.manifest,
            run_id=args.run_id,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL doctor configuration={error}", file=sys.stderr)
        return 2
    if args.json:
        print(canonical_json(compact))
    else:
        print(
            f"{compact['status']} doctor scope={compact['scope']} "
            f"checks={compact['check_count']} warn={compact['warn_count']} "
            f"fail={compact['fail_count']} receipt={receipt_path}"
        )
    return 1 if compact["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
