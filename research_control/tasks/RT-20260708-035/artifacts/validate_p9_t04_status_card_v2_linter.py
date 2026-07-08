#!/usr/bin/env python3
"""Validate the v18 P9-T04 status-card v2 linter-test packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260708-035/artifacts/p9_t04_status_card_v2_linter_report.json"
)


def load_linter() -> Any:
    spec = importlib.util.spec_from_file_location("validate_claim_language", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fixture_text(name: str) -> str:
    return (
        REPO_ROOT / "tests/fixtures/claim_language" / name
    ).read_text(encoding="utf-8")


def scan_one(linter: Any, taxonomy: dict[str, Any], path: str, text: str) -> dict[str, Any]:
    return linter.report_dict(
        linter.scan_text_map(
            {path: text},
            taxonomy=taxonomy,
            reviewed_contexts=[],
            active_handoffs={"research_control/handoffs/handoff-active.yaml"},
        ),
        scanned_paths=[path],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="Write the JSON report.")
    parser.add_argument("--json", action="store_true", help="Emit the JSON report.")
    args = parser.parse_args()

    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    class_ids = {item.get("class_id") for item in taxonomy.get("phrase_classes", [])}

    valid = scan_one(
        linter,
        taxonomy,
        "research_control/current_frontier.md",
        fixture_text("status_card_v2_valid.md"),
    )
    missing_next = scan_one(
        linter,
        taxonomy,
        "research_control/current_frontier.md",
        fixture_text("status_card_v2_missing_next_burden.md"),
    )
    caveat_wall = scan_one(
        linter,
        taxonomy,
        "research_control/current_frontier.md",
        fixture_text("status_card_v2_caveat_wall.md"),
    )
    overclaim = scan_one(
        linter,
        taxonomy,
        "research_control/current_frontier.md",
        (
            "Status-card v2: matter_coupling. Positive status: accepted scoped "
            "evidence/precondition only for continuation. Exact scope: scoped "
            "source-side support. Blocked overread: no benchmark promotion. "
            "Next burden: derive lawful source-side coupling before promotion.\n"
            "GR derived.\n"
        ),
    )

    missing_next_classes = {finding["class_id"] for finding in missing_next["findings"]}
    caveat_wall_classes = {finding["class_id"] for finding in caveat_wall["findings"]}
    overclaim_classes = {finding["class_id"] for finding in overclaim["findings"]}

    checks = {
        "taxonomy_has_status_card_v2_missing_next_burden_class": (
            "status_card_v2_missing_next_burden" in class_ids
        ),
        "valid_status_card_v2_fixture_passes_without_findings": (
            valid["status"] == "PASS" and valid["finding_count"] == 0
        ),
        "missing_next_burden_warns_without_hard_fail": (
            missing_next["status"] == "PASS"
            and missing_next["hard_fail_count"] == 0
            and "status_card_v2_missing_next_burden" in missing_next_classes
        ),
        "caveat_wall_warns_without_hard_fail": (
            caveat_wall["status"] == "PASS"
            and caveat_wall["hard_fail_count"] == 0
            and "caveat_wall_public_summary" in caveat_wall_classes
        ),
        "overclaim_still_hard_fails": (
            overclaim["status"] == "FAIL"
            and overclaim["hard_fail_count"] >= 1
            and "einstein_equation_overclaim" in overclaim_classes
        ),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "task_id": "RT-20260708-035",
        "job_id": "AJ-RT-20260708-035-001",
        "plan_task_id": "P9-T04",
        "status": status,
        "checks": checks,
        "case_reports": {
            "valid": valid,
            "missing_next_burden": missing_next,
            "caveat_wall": caveat_wall,
            "overclaim": overclaim,
        },
        "claim_boundary": {
            "validator_only": True,
            "physics_claims_changed": False,
            "physics_promotion_authorized": False,
        },
    }

    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    elif status == "PASS":
        print("P9-T04 status-card v2 linter validation passed.")
    else:
        print(json.dumps(report, indent=2), file=sys.stderr)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
