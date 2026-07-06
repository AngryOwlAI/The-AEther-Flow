#!/usr/bin/env python3
"""Validate the v17 P4-T01 detector-semantics replacement problem artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_PATH = REPO_ROOT / "research_control/tasks/RT-20260706-001/artifacts/detector_semantics_replacement_problem_statement_v1.md"
REPORT_PATH = REPO_ROOT / "research_control/tasks/RT-20260706-001/artifacts/p4_t01_detector_semantics_replacement_problem_report.json"

REQUIRED_MARKERS = [
    "What Detector Semantics Would Normally Contribute",
    "Forbidden Target Or Empirical Imports",
    "Source-Side Replacement Burden",
    "Interaction With `DetPlaceholder(E)`",
    "Constructive Witness Floor",
    "Scoped Obstruction Floor",
    "Ontology-Law Selector Condition",
    'selected_route_class: "constructive_replacement"',
    'selected_next_plan_task_id: "P4-T02"',
    "detector-semantics adoption",
    "does not adopt detector semantics",
    "does not derive or adopt matter coupling",
]

FORBIDDEN_PROMOTIONS = [
    "this artifact adopts detector semantics",
    "detector semantics are adopted",
    "matter coupling is derived",
    "coupling law is adopted",
    "einstein equations are derived",
    "benchmark is promoted",
    "completed derivation",
]


def validate() -> dict[str, object]:
    text = ARTIFACT_PATH.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
    lowered = text.lower()
    forbidden_hits = [
        phrase for phrase in FORBIDDEN_PROMOTIONS if phrase in lowered and phrase != "completed derivation"
    ]
    if "completed derivation;" not in lowered and "- completed derivation" not in lowered:
        forbidden_hits.append("completed derivation boundary missing")
    status = "PASS" if not missing and not forbidden_hits else "FAIL"
    return {
        "status": status,
        "artifact_path": ARTIFACT_PATH.relative_to(REPO_ROOT).as_posix(),
        "required_marker_count": len(REQUIRED_MARKERS),
        "missing_required_markers": missing,
        "forbidden_promotion_hits": forbidden_hits,
        "selected_next_route": "P4-T02",
        "detector_semantics_adopted": False,
        "matter_coupling_derived": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
