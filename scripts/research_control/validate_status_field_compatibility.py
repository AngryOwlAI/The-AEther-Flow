#!/usr/bin/env python3
"""Validate v16 status-field compatibility records.

This validator is project-control evidence only. A PASS, WARN, or HARD_GATE
result does not prove or refute a physics claim, promote ontology, authorize
matter coupling, promote a benchmark, or complete a derivation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


VALIDATOR_SCHEMA_ID = "status_field_compatibility_validator_v16"
LAYERED_SCHEMA_ID = "layered_status_field_schema_v16"

AUTHORIZATION_FIELDS = [
    "scoped_evidence_status_change_authorized",
    "source_object_status_change_authorized",
    "source_extension_object_status_change_authorized",
    "source_law_adoption_authorized",
    "matter_semantics_adoption_authorized",
    "detector_semantics_adoption_authorized",
    "coupling_law_adoption_authorized",
    "matter_coupling_derivation_authorized",
    "matter_coupling_adoption_authorized",
    "stress_energy_semantics_authorized",
    "matter_action_authorized",
    "einstein_equation_derivation_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
    "downstream_physics_promotion_authorized",
]

DOWNSTREAM_PROMOTION_FIELDS = {
    "source_law_adoption_authorized",
    "matter_semantics_adoption_authorized",
    "detector_semantics_adoption_authorized",
    "coupling_law_adoption_authorized",
    "matter_coupling_derivation_authorized",
    "matter_coupling_adoption_authorized",
    "stress_energy_semantics_authorized",
    "matter_action_authorized",
    "einstein_equation_derivation_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
    "downstream_physics_promotion_authorized",
}

AUTHORITY_KEYS = {"authority_scope", "authority_source_path", "blocked_downstream_claims"}
BARE_ACCEPTED_FIELDS = ("rendered_status", "status_label", "reader_facing_status", "summary")
SAFE_ACCEPTED_CONTEXT = re.compile(r"\b(scoped|only as|precondition|evidence-status|evidence status)\b", re.I)


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return bool(value)


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    result = str(value).strip()
    return result if result else default


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def record_id(record: dict[str, Any]) -> str:
    return text(record.get("record_id") or record.get("task_id"), "unknown")


def is_future(record: dict[str, Any]) -> bool:
    if truthy(record.get("future_record")):
        return True
    return text(record.get("record_scope")).lower() == "future"


def is_high_risk(record: dict[str, Any]) -> bool:
    if truthy(record.get("high_risk_status_row")):
        return True
    if truthy(record.get("physics_promotion_authorized")):
        return True
    if truthy(record.get("scientific_claims_changed")):
        return True
    layers = dict_value(record.get("authorization_layers"))
    return any(truthy(layers.get(field)) for field in AUTHORIZATION_FIELDS)


def event(code: str, severity: str, record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "record_id": record_id(record),
        "reason": reason,
        "physics_claim_authority_created": False,
    }


def true_authorization_fields(record: dict[str, Any]) -> list[str]:
    layers = dict_value(record.get("authorization_layers"))
    return [field for field in AUTHORIZATION_FIELDS if truthy(layers.get(field))]


def has_authority_context(record: dict[str, Any]) -> bool:
    layers = dict_value(record.get("authorization_layers"))
    scope = text(layers.get("authority_scope") or record.get("authorized_scope"))
    source = text(layers.get("authority_source_path") or record.get("promotion_authority_path"))
    blocked = list_value(layers.get("blocked_downstream_claims")) or list_value(
        record.get("blocked_downstream_claims")
    )
    return bool(scope and source and blocked)


def bare_accepted_text(record: dict[str, Any]) -> str:
    for field in BARE_ACCEPTED_FIELDS:
        value = text(record.get(field))
        if re.search(r"\baccepted\b", value, re.I) and not SAFE_ACCEPTED_CONTEXT.search(value):
            return value
    return ""


def gate_chair_scoped_acceptance_text(record: dict[str, Any]) -> str:
    combined = " ".join(text(record.get(field)) for field in ("summary", "rendered_status", "status_label"))
    if re.search(r"\bGate Chair\b", combined, re.I) and re.search(r"\baccepted\b", combined, re.I):
        if SAFE_ACCEPTED_CONTEXT.search(combined):
            return combined
    return ""


def evaluate_record(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    hard_gates: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    passes: list[dict[str, Any]] = []
    layers = dict_value(record.get("authorization_layers"))
    future = is_future(record)

    if truthy(record.get("physics_promotion_authorized")):
        true_layers = true_authorization_fields(record)
        if future and (not true_layers or not has_authority_context(record)):
            hard_gates.append(
                event(
                    "future_physics_promotion_missing_layer",
                    "HARD_GATE",
                    record,
                    "future physics_promotion_authorized=true lacks exact layer and authority context",
                )
            )
        elif not future:
            severity = "WARN" if has_authority_context(record) else "HARD_GATE"
            target = warnings if severity == "WARN" else hard_gates
            target.append(
                event(
                    "historical_physics_promotion_requires_context",
                    severity,
                    record,
                    "historical broad promotion field must be read through scope and authority context",
                )
            )

    if truthy(layers.get("scoped_evidence_status_change_authorized")):
        downstream_true = sorted(field for field in DOWNSTREAM_PROMOTION_FIELDS if truthy(layers.get(field)))
        if downstream_true:
            hard_gates.append(
                event(
                    "scoped_evidence_sets_downstream_promotion",
                    "HARD_GATE",
                    record,
                    f"scoped evidence status also set downstream fields {downstream_true}",
                )
            )

    gate_text = gate_chair_scoped_acceptance_text(record)
    if gate_text and truthy(layers.get("source_law_adoption_authorized")):
        hard_gates.append(
            event(
                "gate_chair_scoped_acceptance_implies_source_law_adoption",
                "HARD_GATE",
                record,
                "Gate Chair scoped evidence acceptance must not imply source-law adoption",
            )
        )

    accepted = bare_accepted_text(record)
    if accepted and is_high_risk(record):
        severity = "HARD_GATE" if future else "WARN"
        target = hard_gates if severity == "HARD_GATE" else warnings
        target.append(
            event(
                "bare_accepted_high_risk_status",
                severity,
                record,
                f"bare accepted rendering lacks scoped layer context: {accepted}",
            )
        )

    if truthy(record.get("scientific_claims_changed")):
        if not true_authorization_fields(record) and not text(record.get("scientific_claim_layer")):
            severity = "HARD_GATE" if future else "WARN"
            target = hard_gates if severity == "HARD_GATE" else warnings
            target.append(
                event(
                    "scientific_claims_changed_missing_layer",
                    severity,
                    record,
                    "scientific_claims_changed=true must state the exact layer changed",
                )
            )

    if not hard_gates and not warnings:
        passes.append(
            {
                "record_id": record_id(record),
                "future_record": future,
                "true_authorization_fields": true_authorization_fields(record),
            }
        )
    return hard_gates, warnings, passes


def evaluate_records(records: list[dict[str, Any]], sample: str = "") -> dict[str, Any]:
    hard_gates: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    passes: list[dict[str, Any]] = []
    for record in records:
        record_hard, record_warn, record_pass = evaluate_record(record)
        hard_gates.extend(record_hard)
        warnings.extend(record_warn)
        passes.extend(record_pass)
    status = "HARD_GATE" if hard_gates else "WARN" if warnings else "PASS"
    return {
        "schema_id": VALIDATOR_SCHEMA_ID,
        "layered_schema_id": LAYERED_SCHEMA_ID,
        "sample": sample,
        "status": status,
        "record_count": len(records),
        "hard_gate_count": len(hard_gates),
        "warning_count": len(warnings),
        "hard_gates": hard_gates,
        "warnings": warnings,
        "passes": passes,
        "authority_boundary": {
            "validator_is_project_control_only": True,
            "physics_claim_authority_created": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def load_yaml_file(path: Path) -> dict[str, Any]:
    try:
        payload = load_yaml(path)
    except StrictYamlError as exc:
        raise SystemExit(f"{path}: YAML parse error: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{path}: expected YAML mapping")
    return payload


def load_fixture(path: Path) -> tuple[str, str, list[dict[str, Any]]]:
    payload = load_yaml_file(path)
    records = list_value(payload.get("records"))
    if not records:
        records = [dict_value(payload.get("record"))]
    normalized_records = [dict(record) for record in records if isinstance(record, dict)]
    return text(payload.get("fixture_id"), path.stem), text(payload.get("expected_status"), "PASS"), normalized_records


def evaluate_fixture_dir(path: Path) -> dict[str, Any]:
    fixture_results: list[dict[str, Any]] = []
    all_match = True
    for fixture_path in sorted(path.glob("*.yaml")):
        fixture_id, expected_status, records = load_fixture(fixture_path)
        report = evaluate_records(records, sample=fixture_id)
        actual_status = report["status"]
        matches = actual_status == expected_status
        all_match = all_match and matches
        fixture_results.append(
            {
                "fixture_id": fixture_id,
                "path": str(fixture_path),
                "expected_status": expected_status,
                "actual_status": actual_status,
                "matches_expected": matches,
                "hard_gate_count": report["hard_gate_count"],
                "warning_count": report["warning_count"],
                "hard_gate_codes": [item["code"] for item in report["hard_gates"]],
                "warning_codes": [item["code"] for item in report["warnings"]],
            }
        )
    return {
        "schema_id": VALIDATOR_SCHEMA_ID,
        "sample": str(path),
        "status": "PASS" if all_match else "FAIL",
        "fixture_count": len(fixture_results),
        "fixture_results": fixture_results,
        "authority_boundary": {
            "validator_is_project_control_only": True,
            "physics_claim_authority_created": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-dir", type=Path, help="Evaluate fixture files and expected statuses.")
    parser.add_argument("--record", type=Path, help="Evaluate one YAML record file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a compact text summary.")
    parser.add_argument("--write-json", type=Path, help="Write the JSON report to this path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.fixture_dir:
        report = evaluate_fixture_dir(args.fixture_dir)
        exit_status = 0 if report["status"] == "PASS" else 1
    elif args.record:
        fixture_id, _expected, records = load_fixture(args.record)
        report = evaluate_records(records, sample=fixture_id)
        exit_status = 0 if report["status"] in {"PASS", "WARN"} else 1
    else:
        report = evaluate_records([], sample="empty")
        exit_status = 0

    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"status field compatibility validation: {report['status']}")
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
