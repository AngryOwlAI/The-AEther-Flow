#!/usr/bin/env python3
"""Validate the v17 P3-T02 accepted-status calibration schema packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import load as load_yaml  # noqa: E402


SCHEMA_PATH = REPO_ROOT / "research_control" / "design" / "accepted_status_calibration_schema_v1.md"
CALIBRATION_PATH = REPO_ROOT / "research_control" / "design" / "accepted_status_calibration_v1.yaml"
ALIAS_PATH = REPO_ROOT / "research_control" / "design" / "distance_to_gr_status_aliases.yaml"
REPORT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260705-055"
    / "artifacts"
    / "p3_t02_acceptance_calibration_schema_report.json"
)

REQUIRED_OBJECTS = ("m_src", "g_eff", "matter_coupling")
REQUIRED_FIELDS = (
    "object_id",
    "ledger_burden_id",
    "status_family",
    "positive_status_sentence",
    "exact_scope_sentence",
    "allowed_use_sentence",
    "blocked_overread_sentence",
    "underclaim_guard",
    "overclaim_guard",
    "public_summary_max_blocked_items",
    "full_control_blocked_items",
    "evidence_source",
    "no_physics_delta",
)
MIRRORED_FIELDS = (
    "status_family",
    "positive_status_sentence",
    "exact_scope_sentence",
    "allowed_use_sentence",
    "blocked_overread_sentence",
)
VALID_STATUS_FAMILIES = {
    "scoped_source_object",
    "scoped_source_extension_object",
    "scoped_evidence_precondition",
    "draft_control",
    "blocked",
    "frozen_negative",
    "not_started",
}


def fail(report: dict[str, Any], message: str) -> None:
    report.setdefault("errors", []).append(message)


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def positive_int_value(value: Any) -> bool:
    if isinstance(value, int):
        return value > 0
    if isinstance(value, str) and value.isdigit():
        return int(value) > 0
    return False


def validate() -> dict[str, Any]:
    report: dict[str, Any] = {
        "status": "PASS",
        "errors": [],
        "schema_path": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "calibration_path": str(CALIBRATION_PATH.relative_to(REPO_ROOT)),
        "alias_path": str(ALIAS_PATH.relative_to(REPO_ROOT)),
        "required_objects": list(REQUIRED_OBJECTS),
    }

    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
    for term in REQUIRED_FIELDS:
        if term not in schema_text:
            fail(report, f"schema missing field term: {term}")
    for object_id in REQUIRED_OBJECTS:
        if object_id not in schema_text:
            fail(report, f"schema missing required object term: {object_id}")

    calibration = load_yaml(CALIBRATION_PATH)
    alias_map = load_yaml(ALIAS_PATH)

    if calibration.get("schema_id") != "accepted_status_calibration_v1":
        fail(report, "calibration schema_id mismatch")
    if calibration.get("authority_rules", {}).get("no_physics_delta") is not True:
        fail(report, "calibration authority rule no_physics_delta must be true")

    high_risk = as_dict(
        as_dict(calibration.get("accepted_status_calibration_v1")).get("high_risk_objects")
    )
    aliases = as_dict(alias_map.get("row_aliases"))
    rules = as_dict(alias_map.get("authority_rules"))
    if rules.get("acceptance_calibration_fields_required_for_p3_t02_rows") is not True:
        fail(report, "alias map does not require P3-T02 calibration fields")
    if rules.get("acceptance_calibration_path") != str(CALIBRATION_PATH.relative_to(REPO_ROOT)):
        fail(report, "alias map does not name the calibration source path")

    for object_id in REQUIRED_OBJECTS:
        row = as_dict(high_risk.get(object_id))
        alias = as_dict(aliases.get(object_id))
        mirrored = as_dict(alias.get("acceptance_calibration"))
        if not row:
            fail(report, f"missing calibration object: {object_id}")
            continue
        for field in REQUIRED_FIELDS:
            if field not in row:
                fail(report, f"{object_id}: missing field {field}")
        if row.get("object_id") != object_id:
            fail(report, f"{object_id}: object_id does not match key")
        if row.get("ledger_burden_id") != object_id:
            fail(report, f"{object_id}: ledger_burden_id does not match key")
        if row.get("status_family") not in VALID_STATUS_FAMILIES:
            fail(report, f"{object_id}: invalid status_family {row.get('status_family')}")
        if row.get("no_physics_delta") is not True:
            fail(report, f"{object_id}: no_physics_delta must be true")
        if not positive_int_value(row.get("public_summary_max_blocked_items")):
            fail(report, f"{object_id}: public_summary_max_blocked_items must be positive")
        if not as_list(row.get("full_control_blocked_items")):
            fail(report, f"{object_id}: full_control_blocked_items must be nonempty")
        if alias.get("display_status") == "accepted":
            fail(report, f"{object_id}: alias display_status renders bare accepted")
        if not mirrored:
            fail(report, f"{object_id}: alias map missing acceptance_calibration block")
            continue
        for field in MIRRORED_FIELDS:
            if mirrored.get(field) != row.get(field):
                fail(report, f"{object_id}: alias field {field} does not match calibration YAML")

    if report["errors"]:
        report["status"] = "FAIL"
    return report


def main() -> int:
    report = validate()
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
