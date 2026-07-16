#!/usr/bin/env python3
"""Validate route-history signatures for repeated route-orbit candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
for import_path in (REPO_ROOT, SCRIPT_DIR):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

from extract_route_history import (  # noqa: E402
    SIGNATURE_SCHEMA_ID,
    build_route_history,
    compact_text,
)
from scripts.validation.models import (  # noqa: E402
    ValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (  # noqa: E402
    DEFAULT_RECEIPT_ROOT,
    add_reporting_arguments,
    options_from_namespace,
    summary_dict,
    write_full_receipt,
)


VALIDATOR_SCHEMA_ID = "route_orbit_validator_v1"
MAX_SUMMARY_IDS = 5
SYNC_STATES = {"synchronized", "not_applicable"}
NON_PHYSICS_ROLES = {
    "documentation-curator",
    "process-integrity-auditor",
    "project-control-maintainer",
    "validator-engineer",
}


def truthy(value: Any) -> bool:
    return bool(value)


def normalized(value: Any, default: str = "none") -> str:
    text = compact_text(value)
    return text if text else default


def known(value: str) -> bool:
    return value not in {"", "none", "unknown", "not_applicable"}


def signature_sort_key(signature: dict[str, Any]) -> tuple[str, str]:
    return (
        normalized(signature.get("source_created_at", "")),
        normalized(signature.get("source_task_id", "")),
    )


def same_known_or_unknown_compatible(left: str, right: str) -> bool:
    if known(left) and known(right):
        return left == right
    return True


def same_route_type(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        normalized(left.get("selected_route"), "unknown") == normalized(right.get("selected_route"), "unknown")
        or normalized(left.get("task_type"), "unknown") == normalized(right.get("task_type"), "unknown")
    )


def hard_orbit_member(signature: dict[str, Any]) -> bool:
    return (
        normalized(signature.get("target_derivation_milestone")) != "none"
        and normalized(signature.get("milestone_burden")) != "none"
        and not truthy(signature.get("new_mathematical_payload_exists"))
        and not truthy(signature.get("exact_repair_attempted"))
        and normalized(signature.get("obstruction_label")) == "none"
        and not truthy(signature.get("freeze_criteria_evaluated"))
        and normalized(signature.get("boundary_synchronization_state"), "unknown") not in SYNC_STATES
        and not truthy(signature.get("new_source_evidence_exists"))
    )


def hard_orbit_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        hard_orbit_member(left)
        and hard_orbit_member(right)
        and normalized(left.get("target_derivation_milestone")) == normalized(right.get("target_derivation_milestone"))
        and normalized(left.get("milestone_burden")) == normalized(right.get("milestone_burden"))
        and normalized(left.get("missing_primitive")) == normalized(right.get("missing_primitive"))
        and same_route_type(left, right)
        and same_known_or_unknown_compatible(
            normalized(left.get("object_family")),
            normalized(right.get("object_family")),
        )
        and same_known_or_unknown_compatible(
            normalized(left.get("object_name")),
            normalized(right.get("object_name")),
        )
    )


def hard_failure_record(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {
        "code": "hard_route_orbit_candidate",
        "severity": "hard_fail",
        "task_ids": [left.get("source_task_id", "unknown"), right.get("source_task_id", "unknown")],
        "signature_ids": [left.get("signature_id", "unknown"), right.get("signature_id", "unknown")],
        "signature_hashes": [left.get("signature_hash", ""), right.get("signature_hash", "")],
        "comparison": {
            "target_derivation_milestone": normalized(left.get("target_derivation_milestone")),
            "milestone_burden": normalized(left.get("milestone_burden")),
            "missing_primitive": normalized(left.get("missing_primitive")),
            "selected_route_left": normalized(left.get("selected_route"), "unknown"),
            "selected_route_right": normalized(right.get("selected_route"), "unknown"),
            "task_type_left": normalized(left.get("task_type"), "unknown"),
            "task_type_right": normalized(right.get("task_type"), "unknown"),
            "object_family_left": normalized(left.get("object_family")),
            "object_family_right": normalized(right.get("object_family")),
            "object_name_left": normalized(left.get("object_name")),
            "object_name_right": normalized(right.get("object_name")),
        },
        "reason": "same milestone burden missing primitive and route shape with no new payload repair obstruction freeze evaluation boundary synchronization or new source evidence",
    }


def find_hard_failures(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(signatures, key=signature_sort_key)
    failures: list[dict[str, Any]] = []
    for left_index, left in enumerate(ordered):
        for right in ordered[left_index + 1 :]:
            if hard_orbit_pair(left, right):
                failures.append(hard_failure_record(left, right))
    return failures


def repeated_burden_key(signature: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        normalized(signature.get("target_derivation_milestone")),
        normalized(signature.get("milestone_burden")),
        normalized(signature.get("missing_primitive")),
        normalized(signature.get("object_family")),
        normalized(signature.get("object_name")),
    )


def find_repeated_payload_warnings(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = {}
    for signature in signatures:
        key = repeated_burden_key(signature)
        if key[0] == "none" or key[1] == "none":
            continue
        grouped.setdefault(key, []).append(signature)

    warnings: list[dict[str, Any]] = []
    for key, members in grouped.items():
        if len(members) < 2:
            continue
        for signature in sorted(members, key=signature_sort_key):
            if truthy(signature.get("new_mathematical_payload_exists")) and not truthy(
                signature.get("route_cycle_control_present")
            ):
                warnings.append(
                    {
                        "code": "repeated_burden_new_payload_missing_route_cycle_control",
                        "severity": "warning",
                        "task_ids": [member.get("source_task_id", "unknown") for member in members],
                        "focus_task_id": signature.get("source_task_id", "unknown"),
                        "signature_id": signature.get("signature_id", "unknown"),
                        "comparison": {
                            "target_derivation_milestone": key[0],
                            "milestone_burden": key[1],
                            "missing_primitive": key[2],
                            "object_family": key[3],
                            "object_name": key[4],
                        },
                        "reason": "same burden repeats with new payload but the focused completion lacks route_cycle_control",
                    }
                )
    return warnings


def is_physics_construction(signature: dict[str, Any]) -> bool:
    return (
        normalized(signature.get("target_derivation_milestone")) != "none"
        and truthy(signature.get("new_mathematical_payload_exists"))
        and normalized(signature.get("role_id"), "unknown") not in NON_PHYSICS_ROLES
    )


def gate_match_key(signature: dict[str, Any]) -> tuple[str, str, str]:
    return (
        normalized(signature.get("target_derivation_milestone")),
        normalized(signature.get("object_family")),
        normalized(signature.get("object_name")),
    )


def gate_matches(left_key: tuple[str, str, str], right_key: tuple[str, str, str]) -> bool:
    return left_key[0] == right_key[0] and (
        left_key[1] == right_key[1]
        or same_known_or_unknown_compatible(left_key[2], right_key[2])
    )


def find_boundary_sync_warnings(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pending_gates: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for signature in sorted(signatures, key=signature_sort_key):
        state = normalized(signature.get("gate_chair_state"), "unknown")
        boundary_state = normalized(signature.get("boundary_synchronization_state"), "unknown")
        current_key = gate_match_key(signature)
        if boundary_state == "synchronized":
            pending_gates = [
                gate for gate in pending_gates if not gate_matches(gate_match_key(gate), current_key)
            ]
            continue
        if state == "scoped_evidence_or_precondition_accepted":
            pending_gates.append(signature)
            continue
        if not is_physics_construction(signature):
            continue
        for gate in pending_gates:
            if gate_matches(gate_match_key(gate), current_key):
                warnings.append(
                    {
                        "code": "scoped_gate_followed_by_construction_before_boundary_sync",
                        "severity": "warning",
                        "task_ids": [
                            gate.get("source_task_id", "unknown"),
                            signature.get("source_task_id", "unknown"),
                        ],
                        "signature_ids": [
                            gate.get("signature_id", "unknown"),
                            signature.get("signature_id", "unknown"),
                        ],
                        "reason": "Gate Chair scoped evidence/precondition result is followed by physics construction before a matching boundary synchronization signature",
                    }
                )
    return warnings


def selector_same_shape(signature: dict[str, Any]) -> bool:
    text = f"{signature.get('role_id', '')} {signature.get('task_type', '')} {signature.get('selected_route', '')}".lower()
    return "selector" in text


def find_selector_same_shape_warnings(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(signatures, key=signature_sort_key)
    warnings: list[dict[str, Any]] = []
    for index, signature in enumerate(ordered):
        if not selector_same_shape(signature) or truthy(signature.get("route_cycle_control_present")):
            continue
        prior_same_burden = [
            prior
            for prior in ordered[:index]
            if normalized(prior.get("target_derivation_milestone")) == normalized(signature.get("target_derivation_milestone"))
            and normalized(prior.get("milestone_burden")) == normalized(signature.get("milestone_burden"))
            and same_known_or_unknown_compatible(
                normalized(prior.get("object_family")),
                normalized(signature.get("object_family")),
            )
        ]
        if not prior_same_burden:
            continue
        warnings.append(
            {
                "code": "selector_same_shape_chain_missing_route_cycle_control",
                "severity": "warning",
                "task_ids": [prior.get("source_task_id", "unknown") for prior in prior_same_burden]
                + [signature.get("source_task_id", "unknown")],
                "focus_task_id": signature.get("source_task_id", "unknown"),
                "signature_id": signature.get("signature_id", "unknown"),
                "reason": "selector appears in a same-burden chain without route_cycle_control explaining why the prior burden is not being replayed",
            }
        )
    return warnings


def find_warnings(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings = []
    warnings.extend(find_repeated_payload_warnings(signatures))
    warnings.extend(find_boundary_sync_warnings(signatures))
    warnings.extend(find_selector_same_shape_warnings(signatures))
    return warnings


def validate_route_history(route_history: dict[str, Any]) -> dict[str, Any]:
    signatures = list(route_history.get("signatures", []))
    hard_failures = find_hard_failures(signatures)
    warnings = find_warnings(signatures)
    return {
        "schema_id": VALIDATOR_SCHEMA_ID,
        "signature_schema_id": SIGNATURE_SCHEMA_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_route_history_schema_id": route_history.get("schema_id", ""),
        "source_sample": route_history.get("sample", ""),
        "source_task_count": route_history.get("task_count", 0),
        "signature_count": len(signatures),
        "extraction_errors": route_history.get("extraction_errors", []),
        "hard_failure_count": len(hard_failures),
        "warning_count": len(warnings),
        "status": "FAIL" if hard_failures or route_history.get("extraction_errors") else "PASS",
        "hard_failures": hard_failures,
        "warnings": warnings,
    }


def load_route_history(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def serialize_report(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def report_fingerprint(report: dict[str, Any]) -> str:
    """Return a stable content key suitable for a later report cache."""
    semantic_report = dict(report)
    semantic_report.pop("generated_at", None)
    payload = json.dumps(
        semantic_report,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def atomic_write_report(path: Path, report: dict[str, Any]) -> None:
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
            json.dump(report, handle, indent=2, sort_keys=True, ensure_ascii=False)
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


def write_diagnostic_receipts(
    report: dict[str, Any],
    run: ValidationRun,
    repo_root: Path,
    output: Path | None = None,
) -> tuple[Path, Path]:
    common_receipt = write_full_receipt(run, repo_root / DEFAULT_RECEIPT_ROOT)
    report_receipt = output or common_receipt.with_name("route-report.json")
    if not report_receipt.is_absolute():
        report_receipt = repo_root / report_receipt
    atomic_write_report(report_receipt, report)
    return common_receipt, report_receipt


def bounded_values(values: list[str]) -> tuple[list[str], int]:
    unique = list(dict.fromkeys(value for value in values if value))
    return unique[:MAX_SUMMARY_IDS], max(0, len(unique) - MAX_SUMMARY_IDS)


def issue_values(report: dict[str, Any], key: str, field: str) -> list[str]:
    values: list[str] = []
    for issue in report.get(key, []):
        value = issue.get(field)
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        elif value:
            values.append(str(value))
    return values


def build_compact_summary(
    run: ValidationRun,
    common_receipt: Path,
    report_receipt: Path,
    *,
    gate_id: str,
    counts: dict[str, int],
    hard_failure_ids: list[str],
    warning_ids: list[str],
    affected_task_ids: list[str],
    affected_task_ids_omitted: int,
    recommended_guard_action: str,
    advisory_only: bool,
) -> dict[str, Any]:
    summary = summary_dict(run, common_receipt, max_findings=MAX_SUMMARY_IDS)
    summary["diagnostic"] = {
        "gate_id": gate_id,
        "counts": counts,
        "hard_failure_ids": hard_failure_ids,
        "warning_ids": warning_ids,
        "affected_task_ids": affected_task_ids,
        "affected_task_ids_omitted": affected_task_ids_omitted,
        "recommended_guard_action": recommended_guard_action,
        "advisory_only": advisory_only,
        "full_report_receipt": str(report_receipt),
    }
    summary["authority_boundary"] = {
        "advisory_only": advisory_only,
        "route_freeze_authorized": False,
        "physics_promotion_authorized": False,
    }
    return summary


def render_compact_summary(summary: dict[str, Any]) -> str:
    diagnostic = summary["diagnostic"]
    counts = " ".join(f"{key}={value}" for key, value in sorted(diagnostic["counts"].items()))
    hard_ids = ",".join(diagnostic["hard_failure_ids"]) or "none"
    warning_ids = ",".join(diagnostic["warning_ids"]) or "none"
    task_ids = ",".join(diagnostic["affected_task_ids"]) or "none"
    return (
        f"{summary['status']} gate={diagnostic['gate_id']} {counts} "
        f"hard_ids={hard_ids} warning_ids={warning_ids} task_ids={task_ids} "
        f"more_task_ids={diagnostic['affected_task_ids_omitted']} "
        f"guard_action={diagnostic['recommended_guard_action']} "
        f"advisory_only={str(diagnostic['advisory_only']).lower()} "
        "route_freeze_authorized=false physics_promotion_authorized=false "
        f"report={diagnostic['full_report_receipt']} receipt={summary['full_receipt']}\n"
    )


def emit_diagnostic_output(
    args: argparse.Namespace,
    report: dict[str, Any],
    summary: dict[str, Any],
    report_receipt: Path,
) -> None:
    if args.json or args.full_json:
        print(serialize_report(report), end="")
        return
    common_mode_selected = any(
        getattr(args, name) for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.output is not None and not common_mode_selected:
        return
    mode = options_from_namespace(args).mode
    if mode == "summary":
        sys.stdout.write(render_compact_summary(summary))
    elif mode == "json-summary":
        print(json.dumps(summary, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    elif mode == "receipt":
        print(report_receipt)


def _issue_message(issue: Any) -> str:
    if not isinstance(issue, dict):
        return compact_text(issue)
    parts = [compact_text(issue.get("reason", ""))]
    task_ids = issue.get("task_ids", [])
    if task_ids:
        parts.append(f"task_ids={','.join(str(task_id) for task_id in task_ids)}")
    return " | ".join(part for part in parts if part) or json.dumps(issue, sort_keys=True)


def adapt_to_common_run(
    report: dict[str, Any],
    gate_id: str,
    issues: list[tuple[str, str, str]],
    advisory_only: bool = False,
) -> ValidationRun:
    fingerprint = report_fingerprint(report)
    exit_code = 0 if advisory_only or report["status"] == "PASS" else 1
    finding_prefix = gate_id.replace("_", "-").upper()
    findings = tuple(
        ValidationFinding(
            finding_id=f"{finding_prefix}-{index:03d}",
            level=level,
            code=code,
            message=message,
        )
        for index, (level, code, message) in enumerate(issues, start=1)
    )
    gate = ValidationGateResult(
        gate_id=gate_id,
        status=report["status"],
        severity="advisory",
        exit_code=exit_code,
        findings=findings,
    )
    return ValidationRun(
        run_id=f"{finding_prefix}-{fingerprint[:16].upper()}",
        tree_hash=f"working-sha256:{fingerprint}",
        status=report["status"],
        exit_code=exit_code,
        gate_results=(gate,),
        profile="shadow_planner",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_reporting_arguments(parser)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--input", type=Path, default=None, help="Existing route-history JSON to validate.")
    parser.add_argument("--task-id", action="append", default=[], help="Extract and validate a task ID; repeatable.")
    parser.add_argument("--sample", choices=["recent-matter-rr-e"], default="", help="Extract and validate a built-in sample.")
    parser.add_argument("--limit", type=int, default=0, help="Limit selected rows after filtering.")
    parser.add_argument("--output", type=Path, default=None, help="Full JSON receipt path; written atomically.")
    parser.add_argument("--json", action="store_true", help="Print the legacy full report.")
    parser.add_argument("--advisory-only", action="store_true", help="Exit zero even when hard failures are detected.")
    args = parser.parse_args(argv)
    common_mode_selected = any(
        getattr(args, name) for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.json and common_mode_selected:
        parser.error("--json cannot be combined with a common reporting mode")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    repo_root = args.repo_root.resolve()
    if args.input is not None:
        input_path = args.input if args.input.is_absolute() else repo_root / args.input
        route_history = load_route_history(input_path)
    else:
        route_history = build_route_history(
            repo_root=repo_root,
            task_ids=args.task_id,
            sample=args.sample,
            limit=args.limit,
        )
    report = validate_route_history(route_history)
    issues = [
        *(
            ("ERROR", "route_history_extraction_error", _issue_message(error))
            for error in report["extraction_errors"]
        ),
        *(
            ("ERROR", str(item.get("code", "hard_route_orbit_candidate")), _issue_message(item))
            for item in report["hard_failures"]
        ),
        *(
            ("WARN", str(item.get("code", "route_orbit_warning")), _issue_message(item))
            for item in report["warnings"]
        ),
    ]
    run = adapt_to_common_run(
        report,
        "route_orbit_diagnostic",
        issues,
        advisory_only=args.advisory_only,
    )
    try:
        common_receipt, report_receipt = write_diagnostic_receipts(
            report,
            run,
            repo_root,
            args.output,
        )
    except (OSError, ValueError) as error:
        print(f"BLOCKED_CONFIGURATION receipt_write_failed: {compact_text(error)}")
        return 2
    hard_ids, _ = bounded_values(issue_values(report, "hard_failures", "code"))
    warning_ids, _ = bounded_values(issue_values(report, "warnings", "code"))
    task_ids, omitted = bounded_values(
        issue_values(report, "hard_failures", "task_ids") + issue_values(report, "warnings", "task_ids")
    )
    action = (
        "repair_extraction_errors_or_hard_route_orbit_candidates"
        if report["status"] == "FAIL"
        else "review_advisory_route_orbit_warnings"
        if report["warning_count"]
        else "continue_no_route_orbit_action_required"
    )
    summary = build_compact_summary(
        run,
        common_receipt,
        report_receipt,
        gate_id="route_orbit_diagnostic",
        counts={
            "source_tasks": report["source_task_count"],
            "signatures": report["signature_count"],
            "extraction_errors": len(report["extraction_errors"]),
            "hard_failures": report["hard_failure_count"],
            "warnings": report["warning_count"],
        },
        hard_failure_ids=hard_ids,
        warning_ids=warning_ids,
        affected_task_ids=task_ids,
        affected_task_ids_omitted=omitted,
        recommended_guard_action=action,
        advisory_only=args.advisory_only,
    )
    emit_diagnostic_output(args, report, summary, report_receipt)
    return run.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
