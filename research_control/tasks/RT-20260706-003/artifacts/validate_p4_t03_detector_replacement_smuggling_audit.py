#!/usr/bin/env python3
"""Validate the P4-T03 detector replacement smuggling-audit artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
ARTIFACT = TASK_DIR / "artifacts" / "detector_replacement_smuggling_audit_v1.tex"
REPORT = TASK_DIR / "artifacts" / "p4_t03_detector_replacement_smuggling_audit_report.json"

REQUIRED_STRINGS = [
    "Detector-Replacement Smuggling Audit v1",
    "SourceDetectorReplacementCandidate\\_EStar\\_v1",
    "\\AuditVerdict",
    "source\\_pure\\_as\\_written",
    "detector_replacement_smuggling_audit_result:",
    "result_type: \"source_pure_as_written\"",
    "empirical_detector_protocol_import: \"pass_absent\"",
    "proper_time_import: \"pass_absent\"",
    "target_metric_import: \"pass_absent\"",
    "target_atlas_or_topology_import: \"pass_absent\"",
    "benchmark_success_import: \"pass_absent\"",
    "stress_energy_or_matter_action_import: \"pass_absent\"",
    "role_registry_or_validator_authority_import: \"pass_absent\"",
    "placeholder_as_adoption: \"pass_absent\"",
    "detector_semantics_adopted: false",
    "source_law_adopted: false",
    "coupling_law_adopted: false",
    "matter_coupling_derived: false",
    "next_required_role: \"refuter\"",
    "The Distance-to-GR ledger is unchanged",
]

FORBIDDEN_SUCCESS_STRINGS = [
    "detector_semantics_adopted: true",
    "source_law_adopted: true",
    "coupling_law_adopted: true",
    "matter_coupling_derived: true",
    "matter_coupling_adopted: true",
    "benchmark_promoted: true",
    "completed_derivation_claimed: true",
]


def build_report() -> dict[str, object]:
    text = ARTIFACT.read_text(encoding="utf-8")
    missing = [needle for needle in REQUIRED_STRINGS if needle not in text]
    lowered = text.lower()
    forbidden_present = [
        needle for needle in FORBIDDEN_SUCCESS_STRINGS if needle in lowered
    ]
    status = "PASS" if not missing and not forbidden_present else "FAIL"
    return {
        "status": status,
        "artifact": str(ARTIFACT.relative_to(TASK_DIR.parents[1])),
        "audit_verdict": "source_pure_as_written",
        "selected_next_route": "P4-T04",
        "missing_required_strings": missing,
        "forbidden_success_strings_present": forbidden_present,
        "detector_semantics_adopted": False,
        "matter_coupling_derived": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
