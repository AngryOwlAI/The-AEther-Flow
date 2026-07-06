#!/usr/bin/env python3
"""Validate the P3-T04 positive-first status-card renderer contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260705-057"
JOB_ID = "AJ-RT-20260705-057-001"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260705-057/artifacts/"
    / "p3_t04_positive_first_status_card_renderer_report.json"
)
HIGH_RISK_IDS = {
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
}
REQUIRED_CARD_FIELDS = {
    "object_id",
    "positive_status",
    "exact_scope",
    "allowed_use",
    "blocked_overread",
}


def load_yaml(path: str) -> dict[str, Any]:
    with (REPO_ROOT / path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path} did not parse as a mapping")
    return data


def load_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def status_card_errors(card: dict[str, Any], object_id: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CARD_FIELDS.difference(card))
    if missing:
        errors.append(f"{object_id}: missing fields {','.join(missing)}")
    if card.get("object_id") != object_id:
        errors.append(f"{object_id}: object_id mismatch")
    for field in ("positive_status", "exact_scope", "allowed_use"):
        value = card.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{object_id}: empty {field}")
    blocked = card.get("blocked_overread")
    if not isinstance(blocked, list) or not blocked:
        errors.append(f"{object_id}: blocked_overread must be a nonempty list")
    elif any(not isinstance(item, str) or not item.strip() for item in blocked):
        errors.append(f"{object_id}: blocked_overread contains empty item")
    if str(card.get("positive_status", "")).strip().lower() == "accepted":
        errors.append(f"{object_id}: bare accepted positive_status")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    current_frontier = load_text("research_control/current_frontier.md")
    compact_yaml = load_yaml("output/compact_current_frontier_v16.yaml")
    compact_index = load_text("wiki/indexes/compact_current_frontier_v16.md")

    errors: list[str] = []
    checks: list[str] = []

    if "## Positive-First Status Cards" not in current_frontier:
        errors.append("current_frontier.md missing Positive-First Status Cards section")
    else:
        checks.append("current_frontier_has_status_card_section")

    if "## Positive-First Status Cards" not in compact_index:
        errors.append("compact frontier Markdown missing Positive-First Status Cards section")
    else:
        checks.append("compact_markdown_has_status_card_section")

    cards_value = compact_yaml.get("high_risk_status_cards")
    if not isinstance(cards_value, list):
        errors.append("compact YAML high_risk_status_cards is not a list")
        cards: dict[str, dict[str, Any]] = {}
    else:
        cards = {
            card.get("object_id"): card
            for card in cards_value
            if isinstance(card, dict) and isinstance(card.get("object_id"), str)
        }

    for object_id in sorted(HIGH_RISK_IDS):
        card = cards.get(object_id)
        if card is None:
            errors.append(f"{object_id}: missing top-level compact status card")
            continue
        errors.extend(status_card_errors(card, object_id))

        expected_heading = f"### `{object_id}`"
        if expected_heading not in current_frontier:
            errors.append(f"{object_id}: current frontier missing card heading")
        for label in ("Positive status", "Scope", "Allowed use", "Blocked overread"):
            if f"**{label}:**" not in current_frontier:
                errors.append(f"current frontier missing {label} label")

    distance_to_gr = compact_yaml.get("distance_to_gr", {})
    if not isinstance(distance_to_gr, dict):
        errors.append("compact YAML distance_to_gr is not a mapping")
        distance_to_gr = {}
    rows = distance_to_gr.get("high_risk_rows", [])
    if not isinstance(rows, list):
        errors.append("compact YAML high_risk_rows is not a list")
        rows = []
    nested_ids = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        burden_id = row.get("burden_id")
        if burden_id not in HIGH_RISK_IDS:
            continue
        nested = row.get("high_risk_status_card")
        if not isinstance(nested, dict):
            errors.append(f"{burden_id}: missing nested high_risk_status_card")
            continue
        nested_ids.add(burden_id)
        if nested.get("object_id") != burden_id:
            errors.append(f"{burden_id}: nested card object_id mismatch")

    missing_nested = sorted(HIGH_RISK_IDS.difference(nested_ids))
    if missing_nested:
        errors.append("missing nested compact cards: " + ",".join(missing_nested))
    else:
        checks.append("compact_rows_have_nested_status_cards")

    if HIGH_RISK_IDS.issubset(cards):
        checks.append("compact_top_level_cards_cover_high_risk_ids")

    report = {
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": checks,
        "high_risk_status_card_object_ids": sorted(cards),
        "required_high_risk_ids": sorted(HIGH_RISK_IDS),
        "source_paths": [
            "research_control/current_frontier.md",
            "output/compact_current_frontier_v16.yaml",
            "output/compact_current_frontier_v16.json",
            "wiki/indexes/compact_current_frontier_v16.md",
        ],
    }

    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
