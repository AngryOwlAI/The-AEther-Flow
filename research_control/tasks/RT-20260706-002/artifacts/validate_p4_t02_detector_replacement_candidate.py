#!/usr/bin/env python3
"""Validate the P4-T02 detector replacement candidate artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
ARTIFACT = TASK_DIR / "artifacts" / "detector_semantics_replacement_candidate_v1.tex"
REPORT = TASK_DIR / "artifacts" / "p4_t02_detector_replacement_candidate_report.json"

REQUIRED_STRINGS = [
    "SourceDetectorReplacementCandidate\\_EStar\\_v1",
    "supplied\\_source\\_placeholder",
    "detector_replacement_candidate:",
    "source_domain:",
    "readout_interface:",
    "certificate:",
    "no_empirical_protocol_import: true",
    "no_proper_time_import: true",
    "no_target_metric_import: true",
    "finite_local_witness:",
    "obstruction_recorded: false",
    "detector_semantics_adopted: false",
    "next_required_role: \"smuggling-auditor\"",
    "This candidate is not detector semantics",
    "The Distance-to-GR ledger is unchanged",
]

FORBIDDEN_SUCCESS_STRINGS = [
    "detector semantics are adopted",
    "source law is adopted",
    "coupling law is adopted",
    "matter coupling is derived",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
]


def build_report() -> dict[str, object]:
    text = ARTIFACT.read_text(encoding="utf-8")
    missing = [needle for needle in REQUIRED_STRINGS if needle not in text]
    forbidden_present = [
        needle for needle in FORBIDDEN_SUCCESS_STRINGS if needle in text.lower()
    ]
    status = "PASS" if not missing and not forbidden_present else "FAIL"
    return {
        "status": status,
        "artifact": str(ARTIFACT.relative_to(TASK_DIR.parents[1])),
        "candidate_constructed": status == "PASS",
        "candidate_status": "supplied_source_placeholder",
        "selected_next_route": "P4-T03",
        "missing_required_strings": missing,
        "forbidden_success_strings_present": forbidden_present,
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
