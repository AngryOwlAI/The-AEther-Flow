#!/usr/bin/env python3
"""Render and inspect a compact support-only route-diagnostic cache."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


SCHEMA_ID = "route_diagnostic_cache_v1"
SCHEMA_VERSION = 1
DEFAULT_CACHE_PATH = Path(".local/route_diagnostics/route_diagnostic_cache_v1.json")
REFRESH_COMMAND = (
    ".venv/bin/python scripts/research_control/render_route_diagnostics.py "
    "--refresh --summary"
)
REGISTRY_PATHS = (
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/AGENT_ROLE_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
)
ROUTING_PATHS = (
    "research_control/program_state.yaml",
    "research_control/current_frontier.md",
)
POLICY_PATHS = (
    "research_control/design/ai_research_agent_metrics_taxonomy_v1.md",
    "research_control/design/physics_payload_ratio_policy_v1.md",
    "research_control/design/route_orbit_freeze_threshold_policy_v1.md",
    "research_control/design/route_orbit_gating_policy_v16.md",
    "research_control/design/route_signature_definition.md",
    "research_control/design/route_signature_schema_v1.md",
    "research_control/design/route_diagnostic_cache_schema_v1.md",
)
IMPLEMENTATION_PATHS = (
    "scripts/research_control/extract_route_history.py",
    "scripts/research_control/extract_route_signatures.py",
    "scripts/research_control/validate_route_orbits.py",
    "scripts/research_control/report_physics_progress_metrics.py",
    "scripts/research_control/report_scientific_payload_density.py",
    "scripts/research_control/continue_research.py",
    "scripts/research_control/render_route_diagnostics.py",
)
AUTHORITY_BOUNDARY = {
    "support_only": True,
    "advisory_only": True,
    "hard_gate_created": False,
    "route_freeze_authorized": False,
    "checkpoint_authority": False,
    "physics_claim_authority": False,
    "physics_promotion_authorized": False,
    "source_records_remain_authority": True,
}
WARNING_FIELDS = (
    "payload_density_warning",
    "route_orbit_warning",
    "same_burden_repetition_warning",
    "gate_ready_without_gate_warning",
)


class RouteDiagnosticCacheError(RuntimeError):
    """Raised when a fresh cache cannot be generated safely."""


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def read_csv_rows(repo_root: Path, relative_path: str) -> list[dict[str, str]]:
    path = repo_root / relative_path
    if not path.is_file():
        return []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return [
                {key: value or "" for key, value in row.items()}
                for row in csv.DictReader(handle)
            ]
    except (OSError, csv.Error):
        return []


def normalized_relative_path(value: str) -> str:
    candidate = Path(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts:
        return ""
    return candidate.as_posix()


def collect_source_paths(repo_root: Path) -> tuple[str, ...]:
    """Return every tracked input class that may alter cached findings."""

    paths = set((*REGISTRY_PATHS, *ROUTING_PATHS, *POLICY_PATHS, *IMPLEMENTATION_PATHS))
    task_rows = read_csv_rows(
        repo_root,
        "registries/RESEARCH_TASK_REGISTRY.csv",
    )
    for row in task_rows:
        task_path = normalized_relative_path(row.get("task_path", ""))
        if task_path:
            paths.add(f"{task_path}/00_TASK.yaml")

    job_rows = read_csv_rows(repo_root, "registries/AGENT_JOB_REGISTRY.csv")
    for row in job_rows:
        for field_name in ("job_path", "completion_path"):
            relative_path = normalized_relative_path(row.get(field_name, ""))
            if relative_path:
                paths.add(relative_path)

    decision_rows = read_csv_rows(
        repo_root,
        "registries/DIRECTOR_DECISION_REGISTRY.csv",
    )
    for row in decision_rows:
        relative_path = normalized_relative_path(row.get("decision_path", ""))
        if relative_path:
            paths.add(relative_path)

    for pattern in (
        "research_control/handoffs/handoff-*.yaml",
        "research_control/handoffs/handoff-*.md",
        "research_control/tasks/*/artifacts/*checker_report.json",
    ):
        for path in repo_root.glob(pattern):
            if path.is_file():
                paths.add(path.relative_to(repo_root).as_posix())
    return tuple(sorted(paths))


def source_snapshot(repo_root: Path) -> dict[str, object]:
    entries: list[dict[str, str]] = []
    missing = 0
    for relative_path in collect_source_paths(repo_root):
        path = repo_root / relative_path
        if path.is_file():
            status = "present"
            digest = sha256_file(path)
        else:
            status = "missing"
            digest = ""
            missing += 1
        entries.append(
            {
                "path": relative_path,
                "status": status,
                "sha256": digest,
            }
        )
    fingerprint = sha256_bytes(canonical_json(entries).encode("utf-8"))
    return {
        "source_fingerprint": fingerprint,
        "source_file_count": len(entries),
        "missing_source_count": missing,
        "entries": entries,
    }


def _warning_ids(items: object, key: str) -> list[str]:
    if not isinstance(items, list):
        return []
    return sorted(
        {
            str(item.get(key, "")).strip()
            for item in items
            if isinstance(item, dict) and str(item.get(key, "")).strip()
        }
    )


def _affected_task_ids(items: object, limit: int = 20) -> tuple[list[str], int]:
    if not isinstance(items, list):
        return [], 0
    values: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_ids = item.get("task_ids", [])
        if isinstance(raw_ids, str):
            raw_ids = [raw_ids]
        if not isinstance(raw_ids, list):
            continue
        for value in raw_ids:
            task_id = str(value).strip()
            if task_id and task_id not in seen:
                seen.add(task_id)
                values.append(task_id)
    return values[:limit], max(0, len(values) - limit)


def default_diagnostics_builder(repo_root: Path) -> dict[str, object]:
    from continue_research import route_orbit_diagnostic_context

    return route_orbit_diagnostic_context(repo_root)


def default_route_orbit_builder(repo_root: Path) -> dict[str, object]:
    from extract_route_history import build_route_history
    from validate_route_orbits import validate_route_history

    route_history = build_route_history(repo_root)
    report = validate_route_history(route_history)
    affected, omitted = _affected_task_ids(
        [*report.get("hard_failures", []), *report.get("warnings", [])]
    )
    return {
        "status": str(report.get("status", "")),
        "source_task_count": int(report.get("source_task_count", 0)),
        "signature_count": int(report.get("signature_count", 0)),
        "extraction_error_count": len(report.get("extraction_errors", [])),
        "legacy_hard_candidate_count": int(report.get("hard_failure_count", 0)),
        "warning_count": int(report.get("warning_count", 0)),
        "legacy_hard_candidate_ids": _warning_ids(
            report.get("hard_failures", []),
            "code",
        ),
        "warning_ids": _warning_ids(report.get("warnings", []), "code"),
        "affected_task_ids": affected,
        "affected_task_ids_omitted": omitted,
        "advisory_only": True,
        "hard_gate": False,
        "route_freeze_authorized": False,
        "physics_claim_authority": False,
    }


def default_route_signature_builder(repo_root: Path) -> dict[str, object]:
    from extract_route_signatures import build_report

    report = build_report(repo_root)
    legacy = report.get("legacy_route_orbit_validation", {})
    if not isinstance(legacy, dict):
        legacy = {}
    return {
        "status": str(report.get("status", "")),
        "source_task_count": int(report.get("task_count", 0)),
        "signature_count": int(report.get("route_signature_count", 0)),
        "extraction_error_count": len(report.get("extraction_errors", [])),
        "legacy_hard_candidate_count": int(legacy.get("hard_failure_count", 0)),
        "warning_count": int(legacy.get("warning_count", 0)),
        "repeated_burden_cycle_count": int(
            report.get("repeated_burden_cycle_count", 0)
        ),
        "repeated_no_new_payload_cycle_count": int(
            report.get("repeated_no_new_payload_cycle_count", 0)
        ),
        "route_orbit_warning_should_emit": bool(
            report.get("route_orbit_warning_should_emit", False)
        ),
        "advisory_only": True,
        "hard_gate": False,
        "route_freeze_authorized": False,
        "physics_claim_authority": False,
    }


def _validate_warning_record(record: object) -> bool:
    return (
        isinstance(record, dict)
        and isinstance(record.get("triggered"), bool)
        and isinstance(record.get("warning_ids"), list)
        and all(isinstance(value, str) for value in record["warning_ids"])
        and record.get("hard_gate") is False
        and record.get("physics_claim_authority") is False
        and record.get("advisory_only") is True
    )


def validate_diagnostics_context(diagnostics: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(diagnostics, dict):
        return ["diagnostics must be an object"]
    for field_name in WARNING_FIELDS:
        if not _validate_warning_record(diagnostics.get(field_name)):
            errors.append(
                f"diagnostics.{field_name} must preserve the advisory warning boundary"
            )
    if diagnostics.get("warning_hard_gates_created") is not False:
        errors.append("diagnostics.warning_hard_gates_created must be false")
    if diagnostics.get("physics_claim_authority_created") is not False:
        errors.append("diagnostics.physics_claim_authority_created must be false")
    if not isinstance(diagnostics.get("recommended_guard_action"), str):
        errors.append("diagnostics.recommended_guard_action must be a string")
    if not isinstance(diagnostics.get("diagnostic_warning_ids"), list):
        errors.append("diagnostics.diagnostic_warning_ids must be a list")
    return errors


def validate_cache(cache: object) -> list[str]:
    if not isinstance(cache, dict):
        return ["cache must be an object"]
    errors: list[str] = []
    required_fields = {
        "schema_id",
        "schema_version",
        "generated_at",
        "source_fingerprint",
        "source_file_count",
        "missing_source_count",
        "warning_count",
        "warning_ids",
        "counts",
        "diagnostics",
        "route_signature_summary",
        "route_orbit_summary",
        "authority_boundary",
    }
    if set(cache) != required_fields:
        errors.append("cache fields differ from route_diagnostic_cache_v1")
    if cache.get("schema_id") != SCHEMA_ID:
        errors.append(f"schema_id must be {SCHEMA_ID}")
    if cache.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    fingerprint = cache.get("source_fingerprint")
    if (
        not isinstance(fingerprint, str)
        or len(fingerprint) != 64
        or any(character not in "0123456789abcdef" for character in fingerprint)
    ):
        errors.append("source_fingerprint must be lowercase SHA-256")
    for field_name in (
        "source_file_count",
        "missing_source_count",
        "warning_count",
    ):
        if not isinstance(cache.get(field_name), int) or cache[field_name] < 0:
            errors.append(f"{field_name} must be a nonnegative integer")
    warning_ids = cache.get("warning_ids")
    if (
        not isinstance(warning_ids, list)
        or any(not isinstance(value, str) or not value for value in warning_ids)
        or warning_ids != sorted(set(warning_ids))
    ):
        errors.append("warning_ids must be sorted unique nonblank strings")
    counts = cache.get("counts")
    if (
        not isinstance(counts, dict)
        or any(not isinstance(value, int) or value < 0 for value in counts.values())
    ):
        errors.append("counts must contain nonnegative integers")
    errors.extend(validate_diagnostics_context(cache.get("diagnostics")))
    for summary_name in ("route_signature_summary", "route_orbit_summary"):
        summary = cache.get(summary_name)
        if not isinstance(summary, dict):
            errors.append(f"{summary_name} must be an object")
            continue
        for field_name, expected in (
            ("advisory_only", True),
            ("hard_gate", False),
            ("route_freeze_authorized", False),
            ("physics_claim_authority", False),
        ):
            if summary.get(field_name) is not expected:
                errors.append(f"{summary_name}.{field_name} must be {expected}")
    if cache.get("authority_boundary") != AUTHORITY_BOUNDARY:
        errors.append("authority_boundary differs from the support-only contract")
    return errors


def build_cache(
    repo_root: Path = REPO_ROOT,
    *,
    diagnostics_builder: Callable[[Path], dict[str, object]] = default_diagnostics_builder,
    route_signature_builder: Callable[[Path], dict[str, object]] = default_route_signature_builder,
    route_orbit_builder: Callable[[Path], dict[str, object]] = default_route_orbit_builder,
) -> dict[str, object]:
    repo_root = Path(repo_root).resolve()
    snapshot = source_snapshot(repo_root)
    diagnostics = diagnostics_builder(repo_root)
    diagnostic_errors = validate_diagnostics_context(diagnostics)
    if diagnostic_errors:
        raise RouteDiagnosticCacheError("; ".join(diagnostic_errors))
    if diagnostics.get("status") == "unavailable":
        raise RouteDiagnosticCacheError(
            str(diagnostics.get("error", "direct diagnostic computation unavailable"))
        )
    route_signature = route_signature_builder(repo_root)
    route_orbit = route_orbit_builder(repo_root)
    metric_warning_ids = [
        str(value)
        for value in diagnostics.get("diagnostic_warning_ids", [])
        if str(value)
    ]
    route_orbit_warning_ids = [
        str(value)
        for value in route_orbit.get("warning_ids", [])
        if str(value)
    ]
    warning_ids = sorted(set(metric_warning_ids + route_orbit_warning_ids))
    counts = {
        "metrics_warning_count": int(
            diagnostics.get("diagnostic_warning_count", 0)
        ),
        "route_signature_warning_count": int(
            route_signature.get("warning_count", 0)
        ),
        "route_orbit_warning_count": int(route_orbit.get("warning_count", 0)),
        "route_signature_extraction_error_count": int(
            route_signature.get("extraction_error_count", 0)
        ),
        "route_orbit_extraction_error_count": int(
            route_orbit.get("extraction_error_count", 0)
        ),
        "legacy_hard_candidate_count": int(
            route_signature.get("legacy_hard_candidate_count", 0)
        )
        + int(route_orbit.get("legacy_hard_candidate_count", 0)),
    }
    cache: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_fingerprint": snapshot["source_fingerprint"],
        "source_file_count": snapshot["source_file_count"],
        "missing_source_count": snapshot["missing_source_count"],
        "warning_count": sum(
            counts[field_name]
            for field_name in (
                "metrics_warning_count",
                "route_signature_warning_count",
                "route_orbit_warning_count",
            )
        ),
        "warning_ids": warning_ids,
        "counts": counts,
        "diagnostics": diagnostics,
        "route_signature_summary": route_signature,
        "route_orbit_summary": route_orbit,
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }
    errors = validate_cache(cache)
    if errors:
        raise RouteDiagnosticCacheError("; ".join(errors))
    return cache


def resolve_cache_path(repo_root: Path, cache_path: Path | None = None) -> Path:
    selected = cache_path or DEFAULT_CACHE_PATH
    return selected if selected.is_absolute() else repo_root / selected


def atomic_write_cache(path: Path, cache: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(cache, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        assert temporary_path is not None
        os.replace(temporary_path, path)
        temporary_path = None
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def inspect_cache(
    repo_root: Path = REPO_ROOT,
    cache_path: Path | None = None,
) -> dict[str, object]:
    repo_root = Path(repo_root).resolve()
    path = resolve_cache_path(repo_root, cache_path)
    snapshot = source_snapshot(repo_root)
    relative_path = (
        path.relative_to(repo_root).as_posix()
        if path.is_relative_to(repo_root)
        else str(path)
    )
    base: dict[str, object] = {
        "schema_id": "route_diagnostic_cache_status_v1",
        "cache_status": "missing",
        "cache_path": relative_path,
        "cache_exists": path.is_file(),
        "current_source_fingerprint": snapshot["source_fingerprint"],
        "cached_source_fingerprint": "",
        "generated_at": "",
        "errors": [],
        "cache": None,
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }
    if not path.is_file():
        return base
    try:
        cache = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        base["cache_status"] = "parse_error"
        base["errors"] = [str(error)]
        return base
    errors = validate_cache(cache)
    if errors:
        base["cache_status"] = "invalid"
        base["errors"] = errors
        return base
    assert isinstance(cache, dict)
    base.update(
        {
            "cached_source_fingerprint": cache["source_fingerprint"],
            "generated_at": cache["generated_at"],
            "cache": cache,
            "cache_status": (
                "fresh"
                if cache["source_fingerprint"] == snapshot["source_fingerprint"]
                else "stale"
            ),
        }
    )
    return base


def advisory_freshness_context(
    status: str,
    *,
    cache_path: str,
    current_source_fingerprint: str,
    cached_source_fingerprint: str = "",
    generated_at: str = "",
    errors: list[str] | None = None,
) -> dict[str, object]:
    action = (
        f"Route diagnostics cache is {status}; run {REFRESH_COMMAND}. "
        "Routing may continue because this diagnostic is advisory only."
    )
    warning = {
        "triggered": False,
        "severity": "none",
        "warning_ids": [],
        "recommended_guard_action": action,
        "hard_gate": False,
        "physics_claim_authority": False,
        "advisory_only": True,
        "evidence": {},
    }
    return {
        "status": f"{status}_cache",
        "source": cache_path,
        "cache_status": status,
        "cache_path": cache_path,
        "source_fingerprint": current_source_fingerprint,
        "cached_source_fingerprint": cached_source_fingerprint,
        "generated_at": generated_at,
        "freshness_notice": {
            "status": status,
            "advisory_only": True,
            "hard_gate": False,
            "errors": list(errors or []),
        },
        "warnings_are_advisory_only": True,
        "warning_hard_gates_created": False,
        "physics_claim_authority_created": False,
        "payload_density_warning": dict(warning),
        "route_orbit_warning": dict(warning),
        "same_burden_repetition_warning": dict(warning),
        "gate_ready_without_gate_warning": dict(warning),
        "recommended_guard_action": action,
        "diagnostic_warning_count": 0,
        "diagnostic_warning_ids": [],
        "payload_density_metrics": {},
        "route_orbit_risk_metrics": {},
    }


def routing_diagnostics_from_cache(
    repo_root: Path = REPO_ROOT,
    cache_path: Path | None = None,
) -> dict[str, object]:
    inspection = inspect_cache(repo_root, cache_path)
    status = str(inspection["cache_status"])
    if status != "fresh":
        return advisory_freshness_context(
            status,
            cache_path=str(inspection["cache_path"]),
            current_source_fingerprint=str(
                inspection["current_source_fingerprint"]
            ),
            cached_source_fingerprint=str(
                inspection["cached_source_fingerprint"]
            ),
            generated_at=str(inspection["generated_at"]),
            errors=[
                str(value)
                for value in inspection.get("errors", [])
                if str(value)
            ],
        )
    cache = inspection["cache"]
    assert isinstance(cache, dict)
    diagnostics = json.loads(canonical_json(cache["diagnostics"]))
    assert isinstance(diagnostics, dict)
    diagnostics.update(
        {
            "status": "fresh_cache",
            "source": str(inspection["cache_path"]),
            "cache_status": "fresh",
            "cache_path": str(inspection["cache_path"]),
            "source_fingerprint": str(cache["source_fingerprint"]),
            "cached_source_fingerprint": str(cache["source_fingerprint"]),
            "generated_at": str(cache["generated_at"]),
            "freshness_notice": {
                "status": "fresh",
                "advisory_only": True,
                "hard_gate": False,
                "errors": [],
            },
        }
    )
    return diagnostics


def render_summary(status: dict[str, object]) -> str:
    cache = status.get("cache")
    warning_count = (
        int(cache.get("warning_count", 0))
        if isinstance(cache, dict)
        else 0
    )
    warning_ids = (
        ",".join(str(value) for value in cache.get("warning_ids", []))
        if isinstance(cache, dict)
        else "none"
    )
    return (
        f"PASS cache={status['cache_status']} warnings={warning_count} "
        f"warning_ids={warning_ids or 'none'} "
        f"source_fingerprint={status['current_source_fingerprint']} "
        "advisory_only=true hard_gate=false physics_claim_authority=false"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--refresh",
        action="store_true",
        help="Recompute direct diagnostics and atomically replace the local cache.",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Inspect freshness without writing. This is the default.",
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_CACHE_PATH)
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="Emit JSON status.")
    output.add_argument(
        "--summary",
        action="store_true",
        help="Emit one compact support-only status line.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    repo_root = args.repo_root.resolve()
    cache_path = resolve_cache_path(repo_root, args.output)
    if args.refresh:
        try:
            atomic_write_cache(cache_path, build_cache(repo_root))
        except (OSError, RouteDiagnosticCacheError) as error:
            print(f"FAIL cache=not_written error={error}", file=sys.stderr)
            return 2
    status = inspect_cache(repo_root, cache_path)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_summary(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
