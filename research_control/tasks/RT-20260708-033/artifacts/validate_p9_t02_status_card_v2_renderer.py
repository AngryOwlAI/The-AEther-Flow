#!/usr/bin/env python3
"""Validate v18 P9-T02 status-card v2 frontier renderer integration."""

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

import render_compact_current_frontier_v16 as compact_renderer  # noqa: E402
import render_current_frontier as current_renderer  # noqa: E402


REPORT_PATH = (
    "research_control/tasks/RT-20260708-033/artifacts/"
    "p9_t02_status_card_v2_renderer_report.json"
)
HIGH_RISK_OBJECT_IDS = {
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
}
REQUIRED_CARD_FIELDS = [
    "object_id",
    "positive_status",
    "exact_scope",
    "allowed_use",
    "blocked_overread",
    "next_burden",
    "next_lawful_route",
    "public_summary",
    "full_control_non_conclusions",
]


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def card_errors(card: dict[str, Any], object_id: str, prefix: str) -> list[str]:
    errors: list[str] = []
    if card.get("object_id") != object_id:
        errors.append(f"{prefix}:{object_id}: object_id mismatch")
    for field in REQUIRED_CARD_FIELDS:
        value = card.get(field)
        if field in {"blocked_overread", "full_control_non_conclusions"}:
            if not isinstance(value, list) or not [item for item in value if text(item)]:
                errors.append(f"{prefix}:{object_id}: missing nonempty {field}")
        elif not text(value):
            errors.append(f"{prefix}:{object_id}: missing {field}")
    if text(card.get("positive_status")).lower() == "accepted":
        errors.append(f"{prefix}:{object_id}: bare accepted positive_status")
    return errors


def cards_by_id(cards: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(cards, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for card in cards:
        if isinstance(card, dict) and text(card.get("object_id")):
            output[text(card.get("object_id"))] = card
    return output


def build_report(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []

    current_payload, current_markdown = current_renderer.render_payload(repo_root)
    compact_snapshot = compact_renderer.build_snapshot(repo_root)
    compact_yaml, compact_json, compact_markdown = compact_renderer.rendered_texts(compact_snapshot)

    if current_payload.get("accepted_status_calibration_path") != current_renderer.ACCEPTED_STATUS_CALIBRATION_V2_PATH:
        errors.append("current_frontier: accepted_status_calibration_v2 not selected")
    if current_payload.get("status_card_version") != "v2":
        errors.append("current_frontier: status_card_version is not v2")
    if current_markdown.count("**Next burden:**") < len(HIGH_RISK_OBJECT_IDS):
        errors.append("current_frontier: fewer next-burden lines than high-risk rows")

    current_cards = cards_by_id(current_renderer.build_state(repo_root).get("high_risk_status_cards", []))
    compact_cards = cards_by_id(compact_snapshot.get("high_risk_status_cards", []))
    compact_rows = compact_snapshot.get("distance_to_gr", {}).get("high_risk_rows", [])
    compact_nested = {
        text(row.get("burden_id")): row.get("high_risk_status_card")
        for row in compact_rows
        if isinstance(row, dict)
    }

    for object_id in sorted(HIGH_RISK_OBJECT_IDS):
        current_card = current_cards.get(object_id)
        if not isinstance(current_card, dict):
            errors.append(f"current_frontier:{object_id}: missing status_card_v2")
        else:
            errors.extend(card_errors(current_card, object_id, "current_frontier"))

        compact_card = compact_cards.get(object_id)
        if not isinstance(compact_card, dict):
            errors.append(f"compact_frontier:{object_id}: missing top-level status_card_v2")
        else:
            errors.extend(card_errors(compact_card, object_id, "compact_frontier"))

        nested_card = compact_nested.get(object_id)
        if not isinstance(nested_card, dict):
            errors.append(f"compact_frontier:{object_id}: missing nested status_card_v2")
        else:
            errors.extend(card_errors(nested_card, object_id, "compact_frontier_nested"))

    if "Next burden" not in compact_markdown:
        errors.append("compact_frontier_markdown: missing Next burden column")
    if compact_renderer.ACCEPTED_STATUS_CALIBRATION_V2_PATH not in compact_snapshot.get("generated_from", []):
        errors.append("compact_frontier: accepted_status_calibration_v2 not listed as generated_from")

    output_paths = {
        compact_renderer.DEFAULT_YAML_PATH: compact_yaml,
        compact_renderer.DEFAULT_JSON_PATH: compact_json,
        compact_renderer.DEFAULT_MARKDOWN_PATH: compact_markdown,
        current_renderer.DEFAULT_FRONTIER_PATH: current_markdown,
    }
    stale_paths = [
        rel_path
        for rel_path, expected_text in output_paths.items()
        if not (repo_root / rel_path).exists()
        or (repo_root / rel_path).read_text(encoding="utf-8") != expected_text
    ]
    if stale_paths:
        errors.append(f"stale renderer outputs: {', '.join(stale_paths)}")

    return {
        "schema_id": "p9_t02_status_card_v2_renderer_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checked_failure_modes": [
            "current_frontier_v2_calibration_selected",
            "current_frontier_next_burden_rendered",
            "compact_frontier_v2_calibration_selected",
            "compact_frontier_top_level_status_cards_complete",
            "compact_frontier_nested_status_cards_complete",
            "full_control_non_conclusions_available",
            "renderer_outputs_fresh",
        ],
        "current_frontier_path": current_renderer.DEFAULT_FRONTIER_PATH,
        "compact_yaml_path": compact_renderer.DEFAULT_YAML_PATH,
        "compact_json_path": compact_renderer.DEFAULT_JSON_PATH,
        "compact_markdown_path": compact_renderer.DEFAULT_MARKDOWN_PATH,
        "high_risk_object_ids": sorted(HIGH_RISK_OBJECT_IDS),
        "current_status_card_count": len(current_cards),
        "compact_status_card_count": len(compact_cards),
        "physics_proof_authority": False,
        "no_physics_delta": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    if args.write_report:
        output_path = repo_root / REPORT_PATH
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
