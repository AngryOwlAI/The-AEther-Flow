#!/usr/bin/env python3
"""Validate compact_current_frontier_v16 outputs against tracked state.

The compact frontier is an operational snapshot only. This validator checks
freshness and overread boundaries; it does not create physics authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_compact_current_frontier_v16 as renderer  # noqa: E402
from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_SCHEMA_ID = "compact_current_frontier_v16_validation_report_v1"
CHECKED_FAILURE_MODES = [
    "active_task_mismatch",
    "latest_handoff_mismatch",
    "next_route_mismatch",
    "high_risk_row_missing",
    "high_risk_status_card_missing",
    "high_risk_status_card_incomplete",
    "metric_use_ledger_missing",
    "metric_use_ledger_path_mismatch",
    "metric_use_ledger_forbidden_import_count_missing",
    "blocked_claim_missing",
    "matter_coupling_overpromoted",
    "einstein_equations_overpromoted",
    "benchmark_promotion_overpromoted",
    "authority_warning_missing",
    "yaml_json_mismatch",
    "live_snapshot_mismatch",
]


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def error_record(error_id: str, message: str) -> dict[str, str]:
    return {"id": error_id, "message": message}


def append_error(errors: list[dict[str, str]], error_id: str, message: str) -> None:
    errors.append(error_record(error_id, message))


def load_json_payload(path: Path, errors: list[dict[str, str]], label: str) -> dict[str, Any] | None:
    if not path.exists():
        append_error(errors, f"{label}_missing", f"missing {label} output: {path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        append_error(errors, f"{label}_invalid_json", f"{path}: {exc}")
        return None
    if not isinstance(payload, dict):
        append_error(errors, f"{label}_not_mapping", f"{path}: top-level JSON value must be an object")
        return None
    return payload


def load_yaml_payload(path: Path, errors: list[dict[str, str]], label: str) -> dict[str, Any] | None:
    if not path.exists():
        append_error(errors, f"{label}_missing", f"missing {label} output: {path}")
        return None
    try:
        payload = load_yaml(path)
    except StrictYamlError as exc:
        append_error(errors, f"{label}_invalid_yaml", f"{path}: {exc}")
        return None
    if not isinstance(payload, dict):
        append_error(errors, f"{label}_not_mapping", f"{path}: top-level YAML value must be a map")
        return None
    return payload


def high_risk_rows(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload.get("distance_to_gr", {}).get("high_risk_rows", [])
    if not isinstance(rows, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict):
            burden_id = str(row.get("burden_id", "")).strip()
            if burden_id:
                output[burden_id] = row
    return output


def high_risk_status_cards(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload.get("high_risk_status_cards", [])
    if not isinstance(rows, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict):
            object_id = str(row.get("object_id", "")).strip()
            if object_id:
                output[object_id] = row
    return output


def blocked_targets(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload.get("blocked_physical_targets", [])
    if not isinstance(rows, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict):
            target_id = str(row.get("target_id", "")).strip()
            if target_id:
                output[target_id] = row
    return output


def text(value: Any) -> str:
    return str(value or "").strip()


def lower_text(value: Any) -> str:
    return text(value).lower()


def compare_active_state(
    payload: dict[str, Any],
    live_snapshot: dict[str, Any],
    errors: list[dict[str, str]],
) -> None:
    output_state = payload.get("active_state", {})
    live_state = live_snapshot.get("active_state", {})
    if not isinstance(output_state, dict) or not isinstance(live_state, dict):
        append_error(errors, "active_state_missing", "compact active_state must be a mapping")
        return
    field_error_ids = {
        "active_task_id": "active_task_mismatch",
        "latest_handoff_id": "latest_handoff_mismatch",
        "current_status": "current_status_mismatch",
    }
    for field, error_id in field_error_ids.items():
        output_value = output_state.get(field)
        live_value = live_state.get(field)
        if output_value != live_value:
            append_error(
                errors,
                error_id,
                f"active_state.{field} output={output_value!r} tracked={live_value!r}",
            )


def compare_next_route(
    payload: dict[str, Any],
    live_snapshot: dict[str, Any],
    errors: list[dict[str, str]],
) -> None:
    output_route = payload.get("next_route", {})
    live_route = live_snapshot.get("next_route", {})
    if not isinstance(output_route, dict) or not isinstance(live_route, dict):
        append_error(errors, "next_route_missing", "compact next_route must be a mapping")
        return
    for field in sorted(live_route):
        output_value = output_route.get(field)
        live_value = live_route.get(field)
        if output_value != live_value:
            append_error(
                errors,
                "next_route_mismatch",
                f"next_route.{field} output={output_value!r} latest_handoff={live_value!r}",
            )


def validate_required_claims(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    boundary = payload.get("claim_boundary", {})
    if not isinstance(boundary, dict):
        append_error(errors, "claim_boundary_missing", "compact claim_boundary must be a mapping")
        return
    if boundary.get("physics_claim_authority") is not False:
        append_error(errors, "claim_authority_enabled", "physics_claim_authority must remain false")
    if boundary.get("proof_authority") is not False:
        append_error(errors, "proof_authority_enabled", "proof_authority must remain false")
    blocked_claims = boundary.get("blocked_claims", [])
    if not isinstance(blocked_claims, list):
        append_error(errors, "blocked_claims_not_list", "claim_boundary.blocked_claims must be a list")
        return
    blocked_claim_set = {text(item) for item in blocked_claims}
    for claim in renderer.REQUIRED_BLOCKED_CLAIMS:
        if claim not in blocked_claim_set:
            append_error(errors, f"blocked_claim_missing:{claim}", f"missing blocked claim: {claim}")


def validate_high_risk_rows(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    rows = high_risk_rows(payload)
    for burden_id in renderer.HIGH_RISK_BURDEN_IDS:
        if burden_id not in rows:
            append_error(errors, f"high_risk_row_missing:{burden_id}", f"missing high-risk row: {burden_id}")


def validate_high_risk_status_cards(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    cards_value = payload.get("high_risk_status_cards")
    if not isinstance(cards_value, list):
        append_error(
            errors,
            "high_risk_status_card_missing",
            "high_risk_status_cards must be a list",
        )
        return
    cards = high_risk_status_cards(payload)
    rows = high_risk_rows(payload)
    for burden_id in renderer.HIGH_RISK_BURDEN_IDS:
        card = cards.get(burden_id)
        if not isinstance(card, dict):
            append_error(
                errors,
                f"high_risk_status_card_missing:{burden_id}",
                f"missing high-risk status card: {burden_id}",
            )
        else:
            for field in ["positive_status", "exact_scope", "allowed_use"]:
                if not text(card.get(field)):
                    append_error(
                        errors,
                        f"high_risk_status_card_incomplete:{burden_id}:{field}",
                        f"status card {burden_id} missing {field}",
                    )
            blocked = card.get("blocked_overread")
            if not isinstance(blocked, list) or not [item for item in blocked if text(item)]:
                append_error(
                    errors,
                    f"high_risk_status_card_incomplete:{burden_id}:blocked_overread",
                    f"status card {burden_id} missing blocked_overread list",
                )
            if lower_text(card.get("positive_status")) == "accepted":
                append_error(
                    errors,
                    f"high_risk_status_card_incomplete:{burden_id}:bare_accepted",
                    f"status card {burden_id} renders bare accepted",
                )
        nested = rows.get(burden_id, {}).get("high_risk_status_card")
        if not isinstance(nested, dict) or nested.get("object_id") != burden_id:
            append_error(
                errors,
                f"high_risk_status_card_missing:{burden_id}:nested",
                f"high-risk row {burden_id} missing nested high_risk_status_card",
            )


def validate_authority_warning(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    warning = payload.get("authority_warning", {})
    if not isinstance(warning, dict) or warning.get("snapshot_only_not_authority") is not True:
        append_error(
            errors,
            "authority_warning_missing",
            "authority_warning.snapshot_only_not_authority must be true",
        )


def validate_metric_use_ledger(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    summary = payload.get("metric_use_ledger")
    if not isinstance(summary, dict):
        append_error(errors, "metric_use_ledger_missing", "metric_use_ledger must be a mapping")
        return
    if text(summary.get("ledger_path")) != renderer.METRIC_USE_LEDGER_PATH:
        append_error(
            errors,
            "metric_use_ledger_path_mismatch",
            f"metric_use_ledger.ledger_path must be {renderer.METRIC_USE_LEDGER_PATH}",
        )
    if int(summary.get("forbidden_or_import_row_count", 0)) <= 0:
        append_error(
            errors,
            "metric_use_ledger_forbidden_import_count_missing",
            "metric_use_ledger.forbidden_or_import_row_count must be positive",
        )
    if int(summary.get("total_row_count", 0)) < int(summary.get("forbidden_or_import_row_count", 0)):
        append_error(
            errors,
            "metric_use_ledger_forbidden_import_count_missing",
            "metric_use_ledger.forbidden_or_import_row_count must not exceed total_row_count",
        )


def validate_overpromotion(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    rows = high_risk_rows(payload)
    targets = blocked_targets(payload)

    matter = rows.get("matter_coupling", {})
    matter_target = targets.get("matter_coupling", {})
    if matter:
        reader = lower_text(matter.get("reader_facing_status"))
        if "derived" in reader or "adopted" in reader:
            append_error(
                errors,
                "matter_coupling_overpromoted",
                "matter_coupling reader-facing status must not render as derived or adopted",
            )
        if text(matter.get("control_status")) != "accepted_as_scoped_evidence_precondition":
            append_error(
                errors,
                "matter_coupling_overpromoted",
                "matter_coupling control_status must remain accepted_as_scoped_evidence_precondition",
            )
        if text(matter.get("promotion_status")) != "scoped_source_evidence_only":
            append_error(
                errors,
                "matter_coupling_overpromoted",
                "matter_coupling promotion_status must remain scoped_source_evidence_only",
            )
        physical = text(matter.get("physical_status"))
        if not physical.startswith("not_matter_coupling"):
            append_error(
                errors,
                "matter_coupling_overpromoted",
                "matter_coupling physical_status must remain a not_matter_coupling guard",
            )
    if matter_target and text(matter_target.get("control_status")) != "accepted_as_scoped_evidence_precondition":
        append_error(
            errors,
            "matter_coupling_overpromoted",
            "blocked_physical_targets.matter_coupling control_status drifted from scoped evidence",
        )

    einstein = rows.get("einstein_equations", {})
    einstein_target = targets.get("einstein_equations", {})
    if einstein:
        reader = lower_text(einstein.get("reader_facing_status"))
        if "derived" in reader:
            append_error(
                errors,
                "einstein_equations_overpromoted",
                "Einstein equations reader-facing status must not render as derived",
            )
        if text(einstein.get("control_status")) != "not_started":
            append_error(
                errors,
                "einstein_equations_overpromoted",
                "Einstein equations control_status must remain not_started",
            )
        if text(einstein.get("physical_status")) != "no_field_equation_derivation":
            append_error(
                errors,
                "einstein_equations_overpromoted",
                "Einstein equations physical_status must remain no_field_equation_derivation",
            )
        if text(einstein.get("promotion_status")) != "none":
            append_error(
                errors,
                "einstein_equations_overpromoted",
                "Einstein equations promotion_status must remain none",
            )
    if einstein_target and text(einstein_target.get("control_status")) != "not_started":
        append_error(
            errors,
            "einstein_equations_overpromoted",
            "blocked_physical_targets.einstein_equations control_status drifted from not_started",
        )

    benchmark = rows.get("benchmark_promotion", {})
    benchmark_target = targets.get("benchmark_promotion", {})
    if benchmark:
        reader = lower_text(benchmark.get("reader_facing_status"))
        if "promoted" in reader:
            append_error(
                errors,
                "benchmark_promotion_overpromoted",
                "benchmark reader-facing status must not render as promoted",
            )
        if text(benchmark.get("control_status")) != "blocked":
            append_error(
                errors,
                "benchmark_promotion_overpromoted",
                "benchmark_promotion control_status must remain blocked",
            )
        if text(benchmark.get("physical_status")) != "no_exact_gr_benchmark_promotion":
            append_error(
                errors,
                "benchmark_promotion_overpromoted",
                "benchmark_promotion physical_status must remain no_exact_gr_benchmark_promotion",
            )
        if text(benchmark.get("promotion_status")) != "none":
            append_error(
                errors,
                "benchmark_promotion_overpromoted",
                "benchmark_promotion promotion_status must remain none",
            )
    if benchmark_target and text(benchmark_target.get("control_status")) != "blocked":
        append_error(
            errors,
            "benchmark_promotion_overpromoted",
            "blocked_physical_targets.benchmark_promotion control_status drifted from blocked",
        )


def build_report(
    repo_root: Path = REPO_ROOT,
    *,
    yaml_rel_path: str = renderer.DEFAULT_YAML_PATH,
    json_rel_path: str = renderer.DEFAULT_JSON_PATH,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    yaml_path = repo_path(repo_root, yaml_rel_path)
    json_path = repo_path(repo_root, json_rel_path)
    yaml_payload = load_yaml_payload(yaml_path, errors, "yaml")
    json_payload = load_json_payload(json_path, errors, "json")

    live_snapshot: dict[str, Any] | None = None
    try:
        live_snapshot = renderer.build_snapshot(repo_root)
    except renderer.CompactFrontierError as exc:
        append_error(errors, "live_snapshot_error", f"could not build live compact snapshot: {exc}")

    primary_payload = json_payload if json_payload is not None else yaml_payload

    if yaml_payload is not None and json_payload is not None and yaml_payload != json_payload:
        append_error(errors, "yaml_json_mismatch", "compact YAML and JSON outputs differ")

    if primary_payload is not None:
        for message in renderer.validate_snapshot(primary_payload):
            if message.startswith("missing blocked claim: "):
                claim = message.removeprefix("missing blocked claim: ")
                append_error(errors, f"blocked_claim_missing:{claim}", message)
            elif message.startswith("missing high-risk row: "):
                burden_id = message.removeprefix("missing high-risk row: ")
                append_error(errors, f"high_risk_row_missing:{burden_id}", message)
            elif message.startswith("bare accepted high-risk row: "):
                burden_id = message.removeprefix("bare accepted high-risk row: ")
                append_error(errors, f"bare_accepted_high_risk_row:{burden_id}", message)
            else:
                append_error(errors, "schema_boundary_error", message)
        validate_required_claims(primary_payload, errors)
        validate_high_risk_rows(primary_payload, errors)
        validate_high_risk_status_cards(primary_payload, errors)
        validate_metric_use_ledger(primary_payload, errors)
        validate_authority_warning(primary_payload, errors)
        validate_overpromotion(primary_payload, errors)

    if primary_payload is not None and live_snapshot is not None:
        compare_active_state(primary_payload, live_snapshot, errors)
        compare_next_route(primary_payload, live_snapshot, errors)
        expected_yaml, expected_json, _ = renderer.rendered_texts(live_snapshot)
        if yaml_path.exists() and yaml_path.read_text(encoding="utf-8") != expected_yaml:
            append_error(errors, "yaml_live_mismatch", "compact YAML output is stale relative to tracked state")
        if json_path.exists() and json_path.read_text(encoding="utf-8") != expected_json:
            append_error(errors, "json_live_mismatch", "compact JSON output is stale relative to tracked state")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": REPORT_SCHEMA_ID,
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "checked_failure_modes": CHECKED_FAILURE_MODES,
        "yaml_path": yaml_rel_path,
        "json_path": json_rel_path,
        "snapshot_only_not_authority": bool(
            primary_payload
            and isinstance(primary_payload.get("authority_warning"), dict)
            and primary_payload["authority_warning"].get("snapshot_only_not_authority") is True
        ),
        "active_task_id": (
            primary_payload.get("active_state", {}).get("active_task_id")
            if isinstance(primary_payload, dict)
            else ""
        ),
        "latest_handoff_id": (
            primary_payload.get("active_state", {}).get("latest_handoff_id")
            if isinstance(primary_payload, dict)
            else ""
        ),
        "next_route_id": (
            primary_payload.get("next_route", {}).get("route_id")
            if isinstance(primary_payload, dict)
            else ""
        ),
        "operational_receipt_only": True,
        "physics_proof_authority": False,
        "no_physics_delta": True,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    parser.add_argument("--yaml-path", default=renderer.DEFAULT_YAML_PATH)
    parser.add_argument("--json-path", default=renderer.DEFAULT_JSON_PATH)
    parser.add_argument("--output", help="Write the validation report JSON to this path.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation report.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(
        Path(args.repo_root),
        yaml_rel_path=args.yaml_path,
        json_rel_path=args.json_path,
    )
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path(args.repo_root) / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        if report["status"] == "PASS":
            print("Compact current-frontier v16 validation passed.")
        else:
            print("Compact current-frontier v16 validation failed:")
            for error in report["errors"]:
                print(f"- {error['id']}: {error['message']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
