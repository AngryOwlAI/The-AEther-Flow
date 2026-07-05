#!/usr/bin/env python3
"""Validate the P16-T01 documentation-impact consolidation receipt."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260705-036"
    / "artifacts"
    / "v16_documentation_impact_consolidation.md"
)
REGISTRY_PATH = REPO_ROOT / "registries" / "MARKDOWN_SOURCE_REGISTRY.csv"
INVENTORY_PATH = REPO_ROOT / "research_control" / "design" / "validation_command_inventory_v16.md"

REQUIRED_REGISTERED_PATHS = [
    "research_control/design/minimum_physics_payload_schema_v1.md",
    "research_control/design/route_orbit_gating_policy_v16.md",
    "research_control/design/layered_status_field_schema_v16.md",
    "research_control/design/eqsrc_retainh_genh_trigger_list_v16.md",
    "research_control/design/source_model_zoo_schema_v1.md",
    "research_control/design/source_model_zoo_v1.md",
    "research_control/design/manuscript_split_boundary_checklist_v16.md",
    "research_control/design/one_question_red_team_packet_v16.md",
    "research_control/design/target_import_attack_taxonomy_v16.md",
    "research_control/design/target_import_attack_fixture_catalog_v16.md",
    "research_control/design/compact_current_frontier_schema_v16.md",
    "research_control/design/validation_command_inventory_v16.md",
]

REQUIRED_ARTIFACT_PHRASES = [
    "Every design schema has source registry status if required",
    "Every validator/script addition has maintainer note or command inventory update",
    "Every generated derivative is regenerated, not hand-edited",
    "Every public-facing change has publication brief or source spec when required",
    "No documentation change promotes physics claims",
    "No physics delta",
    "P16-T02 owns the complete v16 inventory update",
    "Generated outputs remain derivative",
    "No changed path is used as scientific proof",
]

FORBIDDEN_PROMOTION_PHRASES = [
    "matter coupling is derived",
    "Einstein equations are derived",
    "benchmark is promoted",
    "completed derivation is established",
]


def load_registry_by_path() -> dict[str, dict[str, str]]:
    with REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row["path"]: row for row in reader}


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    registry_rows = load_registry_by_path()
    artifact_text = ARTIFACT_PATH.read_text(encoding="utf-8") if ARTIFACT_PATH.exists() else ""
    inventory_text = INVENTORY_PATH.read_text(encoding="utf-8") if INVENTORY_PATH.exists() else ""

    for phrase in REQUIRED_ARTIFACT_PHRASES:
        if phrase not in artifact_text:
            errors.append(f"artifact_missing_phrase:{phrase}")

    lower_text = artifact_text.lower()
    for phrase in FORBIDDEN_PROMOTION_PHRASES:
        if phrase in lower_text:
            errors.append(f"artifact_contains_forbidden_promotion_phrase:{phrase}")

    registry_checks: list[dict[str, str]] = []
    for path in REQUIRED_REGISTERED_PATHS:
        row = registry_rows.get(path)
        if row is None:
            errors.append(f"missing_markdown_registry_row:{path}")
            registry_checks.append({"path": path, "status": "missing"})
            continue
        status = row.get("validation_status", "")
        authority = row.get("authority_status", "")
        registry_checks.append(
            {
                "path": path,
                "object_id": row.get("object_id", ""),
                "authority_status": authority,
                "validation_status": status,
            }
        )
        if status != "PASS":
            errors.append(f"registry_row_not_pass:{path}:{status}")
        if authority != "project_control":
            errors.append(f"registry_row_not_project_control:{path}:{authority}")

    if "No validator PASS is proof authority" not in inventory_text:
        errors.append("validation_inventory_missing_no_proof_authority_warning")
    if "P16-T02 owns the full v16 inventory update" not in inventory_text:
        errors.append("validation_inventory_missing_p16_t02_notice")

    return {
        "schema_id": "p16_t01_documentation_impact_consolidation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "artifact_path": ARTIFACT_PATH.relative_to(REPO_ROOT).as_posix(),
        "registry_checks": registry_checks,
        "required_artifact_phrases_checked": REQUIRED_ARTIFACT_PHRASES,
        "operational_receipt_only": True,
        "physics_proof_authority": False,
        "no_physics_delta": True,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
