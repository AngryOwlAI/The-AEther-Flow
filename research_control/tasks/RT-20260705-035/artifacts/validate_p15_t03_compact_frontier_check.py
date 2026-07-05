#!/usr/bin/env python3
"""Validate the P15-T03 compact frontier check integration receipt."""

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

import validate_compact_current_frontier_v16 as compact_validator  # noqa: E402


INVENTORY_PATH = REPO_ROOT / "research_control" / "design" / "validation_command_inventory_v16.md"
FULL_VALIDATOR_PATH = REPO_ROOT / "scripts" / "research_control" / "run_full_research_control_validation.py"
RESEARCH_CONTROL_VALIDATOR_PATH = REPO_ROOT / "scripts" / "research_control" / "validate_research_control.py"
COMMAND = ".venv/bin/python scripts/research_control/validate_compact_current_frontier_v16.py --json"


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    compact_report = compact_validator.build_report(REPO_ROOT)
    if compact_report["status"] != "PASS":
        errors.append("compact_current_frontier_v16_validator_failed")

    inventory_text = INVENTORY_PATH.read_text(encoding="utf-8") if INVENTORY_PATH.exists() else ""
    if COMMAND not in inventory_text:
        errors.append("validation_command_inventory_missing_compact_check_command")
    if "No validator PASS is proof authority" not in inventory_text:
        errors.append("validation_command_inventory_missing_non_authority_warning")

    full_validator_text = FULL_VALIDATOR_PATH.read_text(encoding="utf-8")
    if "compact_current_frontier_check" not in full_validator_text:
        errors.append("run_full_research_control_validation_missing_compact_label")

    research_validator_text = RESEARCH_CONTROL_VALIDATOR_PATH.read_text(encoding="utf-8")
    if "validate_compact_current_frontier_sync" not in research_validator_text:
        errors.append("validate_research_control_missing_compact_sync_hook")

    return {
        "schema_id": "p15_t03_compact_frontier_check_integration_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "compact_validator_status": compact_report["status"],
        "checked_command": COMMAND,
        "inventory_path": INVENTORY_PATH.relative_to(REPO_ROOT).as_posix(),
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
