#!/usr/bin/env python3
"""Validate the v18 P4-T03 countermodel-obligation validator integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
RESEARCH_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
PROJECT_SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
for path in (RESEARCH_SCRIPT_DIR, PROJECT_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import validate_claim_language  # noqa: E402
import validate_research_control  # noqa: E402


REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260708-003/artifacts/"
    "p4_t03_countermodel_obligation_validator_report.json"
)


def build_report() -> dict[str, object]:
    registry_report = validate_research_control.ValidationReport()
    rows = validate_research_control.read_csv_rows("COUNTERMODEL_OBLIGATION_REGISTRY.csv")
    validate_research_control.validate_countermodel_obligation_registry(registry_report, rows)

    taxonomy = validate_claim_language.load_taxonomy()
    overread_report = validate_claim_language.report_dict(
        validate_claim_language.scan_text_map(
            {
                "research_control/current_frontier.md": (
                    "A local countermodel proves global no-go.\n"
                )
            },
            taxonomy=taxonomy,
            reviewed_contexts=[],
            active_handoffs=set(),
        ),
        scanned_paths=["research_control/current_frontier.md"],
    )
    scoped_report = validate_claim_language.report_dict(
        validate_claim_language.scan_text_map(
            {
                "research_control/current_frontier.md": (
                    "A local countermodel records scoped obstruction only; "
                    "it is not a global no-go and not future source-extension impossibility.\n"
                )
            },
            taxonomy=taxonomy,
            reviewed_contexts=[],
            active_handoffs=set(),
        ),
        scanned_paths=["research_control/current_frontier.md"],
    )

    hard_fail_classes = {
        str(finding.get("class_id", ""))
        for finding in overread_report.get("findings", [])
        if str(finding.get("severity", "")).startswith("hard_fail_")
    }
    missing_slot_warnings = [
        warning
        for warning in registry_report.warnings
        if "missing_countermodel_slot" in warning
    ]
    status = "PASS"
    errors: list[str] = []
    if registry_report.errors:
        status = "FAIL"
        errors.extend(registry_report.errors)
    if "countermodel_overread_as_global_no_go" not in hard_fail_classes:
        status = "FAIL"
        errors.append("countermodel overread phrase did not hard-fail")
    if scoped_report.get("status") != "PASS":
        status = "FAIL"
        errors.append("scoped countermodel denial wording did not pass")
    if not missing_slot_warnings:
        status = "FAIL"
        errors.append("live registry did not emit the expected advisory missing-slot warning")

    return {
        "schema_id": "p4_t03_countermodel_obligation_validator_report_v1",
        "status": status,
        "errors": errors,
        "registry_row_count": len(rows),
        "registry_error_count": len(registry_report.errors),
        "registry_warning_count": len(registry_report.warnings),
        "missing_slot_warning_count": len(missing_slot_warnings),
        "overread_report_status": overread_report.get("status"),
        "overread_hard_fail_classes": sorted(hard_fail_classes),
        "scoped_denial_report_status": scoped_report.get("status"),
        "initial_severity": {
            "missing_countermodel_slot": "warn_current_control",
            "countermodel_overread_as_global_no_go": "overclaim_hard_fail",
            "theorem_without_countermodel_justification": "warn_current_control",
            "countermodel_scope_missing": "warn_current_control",
        },
        "authority_boundary": {
            "validator_is_project_control_only": True,
            "physics_claim_authority_created": False,
            "missing_slots_are_advisory_first_cycle": True,
            "global_no_go_overread_is_hard_fail": True,
        },
    }


def main() -> int:
    report = build_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
