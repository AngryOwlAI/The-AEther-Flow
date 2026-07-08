#!/usr/bin/env python3
"""Validate the v18 P9-T01 status-card v2 schema packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import load as load_yaml  # noqa: E402


SCHEMA_PATH = REPO_ROOT / "research_control" / "design" / "status_card_v2_schema.md"
CALIBRATION_PATH = REPO_ROOT / "research_control" / "design" / "accepted_status_calibration_v2.yaml"
ALIAS_PATH = REPO_ROOT / "research_control" / "design" / "distance_to_gr_status_aliases.yaml"
REPORT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-032"
    / "artifacts"
    / "p9_t01_status_card_v2_schema_report.json"
)

REQUIRED_OBJECTS = (
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
)
REQUIRED_FIELDS = (
    "object_id",
    "positive_status",
    "exact_scope",
    "allowed_use",
    "blocked_overread",
    "next_burden",
    "next_lawful_route",
    "public_summary",
    "full_control_non_conclusions",
)
LIST_FIELDS = ("blocked_overread", "full_control_non_conclusions")


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def fail(report: dict[str, Any], message: str) -> None:
    report.setdefault("errors", []).append(message)


def text_positions(text: str, tokens: tuple[str, ...]) -> dict[str, int]:
    return {token: text.find(token) for token in tokens}


def validate_positive_first_order(calibration_text: str, object_id: str, report: dict[str, Any]) -> None:
    marker = f"    {object_id}:"
    start = calibration_text.find(marker)
    if start < 0:
        fail(report, f"{object_id}: cannot locate object block for field-order check")
        return
    next_start = len(calibration_text)
    for other_id in REQUIRED_OBJECTS:
        other_marker = f"    {other_id}:"
        other_start = calibration_text.find(other_marker, start + len(marker))
        if 0 < other_start < next_start:
            next_start = other_start
    block = calibration_text[start:next_start]
    positions = text_positions(
        block,
        (
            "positive_status:",
            "exact_scope:",
            "allowed_use:",
            "blocked_overread:",
            "next_burden:",
            "next_lawful_route:",
            "public_summary:",
            "full_control_non_conclusions:",
        ),
    )
    missing = [token for token, pos in positions.items() if pos < 0]
    if missing:
        fail(report, f"{object_id}: missing tokens for order check {missing}")
        return
    ordered = list(positions.values()) == sorted(positions.values())
    if not ordered:
        fail(report, f"{object_id}: status_card_v2 fields do not preserve positive-first order")


def validate_card(
    report: dict[str, Any],
    object_id: str,
    card: dict[str, Any],
    alias_card: dict[str, Any],
) -> None:
    if not card:
        fail(report, f"{object_id}: missing status_card_v2")
        return
    if card.get("object_id") != object_id:
        fail(report, f"{object_id}: card object_id does not match key")
    for field in REQUIRED_FIELDS:
        if field not in card:
            fail(report, f"{object_id}: missing card field {field}")
            continue
        if field in LIST_FIELDS:
            if not as_list(card.get(field)):
                fail(report, f"{object_id}: {field} must be a nonempty list")
        elif not isinstance(card.get(field), str) or not card.get(field, "").strip():
            fail(report, f"{object_id}: {field} must be a nonempty string")
    if card.get("positive_status", "").strip().lower() == "accepted":
        fail(report, f"{object_id}: positive_status renders bare accepted")
    if "accepted." in card.get("public_summary", "").lower():
        fail(report, f"{object_id}: public_summary uses bare accepted")
    if "next_burden" not in card or not card.get("next_burden", "").strip():
        fail(report, f"{object_id}: next_burden required for high-risk row")
    if not alias_card:
        fail(report, f"{object_id}: alias map missing status_card_v2")
        return
    for field in REQUIRED_FIELDS:
        if alias_card.get(field) != card.get(field):
            fail(report, f"{object_id}: alias status_card_v2 field {field} does not match calibration")


def validate() -> dict[str, Any]:
    report: dict[str, Any] = {
        "status": "PASS",
        "errors": [],
        "schema_path": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "calibration_path": str(CALIBRATION_PATH.relative_to(REPO_ROOT)),
        "alias_path": str(ALIAS_PATH.relative_to(REPO_ROOT)),
        "required_objects": list(REQUIRED_OBJECTS),
        "required_fields": list(REQUIRED_FIELDS),
    }

    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
    calibration_text = CALIBRATION_PATH.read_text(encoding="utf-8")
    for term in REQUIRED_FIELDS:
        if term not in schema_text:
            fail(report, f"schema missing field term: {term}")
    for object_id in REQUIRED_OBJECTS:
        if object_id not in schema_text:
            fail(report, f"schema missing required object term: {object_id}")
    for required_phrase in (
        "does not override",
        "does not decide the next research route",
        "does not create proof authority",
        "preserves positive-first order",
    ):
        if required_phrase not in schema_text:
            fail(report, f"schema missing authority phrase: {required_phrase}")

    calibration = load_yaml(CALIBRATION_PATH)
    alias_map = load_yaml(ALIAS_PATH)

    if calibration.get("schema_id") != "accepted_status_calibration_v2":
        fail(report, "calibration schema_id mismatch")
    rules = as_dict(calibration.get("authority_rules"))
    required_rule_values = {
        "calibration_is_physics_proof": False,
        "calibration_is_routing_authority": False,
        "calibration_overrides_ledger": False,
        "no_physics_delta": True,
        "status_card_v2_required_for_high_risk_rows": True,
        "positive_first_order_required": True,
        "next_burden_required": True,
        "public_summary_is_compression_only": True,
        "full_control_non_conclusions_required": True,
    }
    for key, expected in required_rule_values.items():
        if rules.get(key) is not expected:
            fail(report, f"calibration authority rule {key} must be {expected!r}")
    if rules.get("renderer_integration_deferred_to_plan_task_id") != "P9-T02":
        fail(report, "renderer integration must be deferred to P9-T02")
    if rules.get("linter_tests_deferred_to_plan_task_id") != "P9-T04":
        fail(report, "linter tests must be deferred to P9-T04")
    if calibration.get("status_card_v2_field_order") != list(REQUIRED_FIELDS):
        fail(report, "status_card_v2_field_order mismatch")

    alias_rules = as_dict(alias_map.get("authority_rules"))
    if alias_rules.get("status_card_v2_next_burden_required_for_high_risk_rows") is not True:
        fail(report, "alias map does not require status-card v2 next_burden")
    if alias_rules.get("accepted_status_calibration_v2_path") != str(CALIBRATION_PATH.relative_to(REPO_ROOT)):
        fail(report, "alias map does not name accepted_status_calibration_v2 path")
    if alias_rules.get("status_card_v2_renderer_integration_deferred_to_plan_task_id") != "P9-T02":
        fail(report, "alias map renderer integration must be deferred to P9-T02")

    high_risk = as_dict(
        as_dict(calibration.get("accepted_status_calibration_v2")).get("high_risk_objects")
    )
    aliases = as_dict(alias_map.get("row_aliases"))
    for object_id in REQUIRED_OBJECTS:
        row = as_dict(high_risk.get(object_id))
        if row.get("object_id") != object_id:
            fail(report, f"{object_id}: calibration object_id does not match key")
        if row.get("ledger_burden_id") != object_id:
            fail(report, f"{object_id}: ledger_burden_id does not match key")
        card = as_dict(row.get("status_card_v2"))
        alias_card = as_dict(as_dict(aliases.get(object_id)).get("status_card_v2"))
        validate_card(report, object_id, card, alias_card)
        validate_positive_first_order(calibration_text, object_id, report)

    if report["errors"]:
        report["status"] = "FAIL"
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report-path", default=str(REPORT_PATH))
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        report_path = Path(args.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"status={report['status']} errors={len(report.get('errors', []))}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
