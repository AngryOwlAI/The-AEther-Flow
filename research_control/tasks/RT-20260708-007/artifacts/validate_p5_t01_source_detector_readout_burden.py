#!/usr/bin/env python3
"""Validate the v18 P5-T01 source detector/readout burden packet."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
DESIGN = ROOT / "research_control/design/source_detector_readout_semantics_burden_v1.md"
RECEIPT = ROOT / "research_control/tasks/RT-20260708-007/artifacts/source_detector_readout_burden_receipt.md"
COMPLETION = ROOT / "research_control/tasks/RT-20260708-007/jobs/completions/AJC-AJ-RT-20260708-007-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0700.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
REPORT = ROOT / "research_control/tasks/RT-20260708-007/artifacts/p5_t01_source_detector_readout_burden_report.json"


REQUIRED_DESIGN_SNIPPETS = [
    'burden_id: "source_detector_readout_semantics"',
    'milestone: "matter_coupling"',
    'required_object: "Det_src or Readout_src"',
    'current_status: "proposal_burden_only"',
    "no empirical detector protocol import",
    "no proper-time import",
    "no target metric import",
    "compatibility with SourceCouplingLawCandidate_EStar_v1",
    "This definition is a burden target. It is not a constructed candidate and not",
    "This note requests no ledger row and performs no ledger status update.",
]

FORBIDDEN_PROMOTION_SNIPPETS = [
    "Det_src adopted",
    "Readout_src adopted",
    "detector semantics adopted",
    "matter coupling derived",
    "Einstein equations derived",
    "benchmark promoted",
    "completed derivation achieved",
]


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required path: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    try:
        design_text = read(DESIGN)
    except AssertionError as exc:
        failures.append(str(exc))
        design_text = ""

    try:
        receipt_text = read(RECEIPT)
    except AssertionError as exc:
        failures.append(str(exc))
        receipt_text = ""

    try:
        completion_text = read(COMPLETION)
    except AssertionError as exc:
        failures.append(str(exc))
        completion_text = ""

    try:
        handoff_text = read(HANDOFF)
    except AssertionError as exc:
        failures.append(str(exc))
        handoff_text = ""

    try:
        program_state_text = read(PROGRAM_STATE)
    except AssertionError as exc:
        failures.append(str(exc))
        program_state_text = ""

    for snippet in REQUIRED_DESIGN_SNIPPETS:
        if snippet not in design_text:
            failures.append(f"design missing snippet: {snippet}")

    for snippet in FORBIDDEN_PROMOTION_SNIPPETS:
        for label, text in {
            "design": design_text,
            "receipt": receipt_text,
            "completion": completion_text,
            "handoff": handoff_text,
        }.items():
            if snippet in text:
                failures.append(f"{label} contains forbidden promotion snippet: {snippet}")

    required_completion = [
        'plan_task_id: "P5-T01"',
        'selected_next_plan_task_id: "P5-T02"',
        'changed: false',
        'ledger_row_updated: false',
        "MP-P5T01-SOURCE-DETECTOR-READOUT-BURDEN-DEFINITION",
        "source_detector_readout_semantics",
    ]
    for snippet in required_completion:
        if snippet not in completion_text:
            failures.append(f"completion missing snippet: {snippet}")

    if 'latest_handoff_id: "handoff-0700"' not in program_state_text:
        failures.append("program_state does not point to handoff-0700")
    if "P5-T02" not in handoff_text:
        failures.append("handoff does not route to P5-T02")

    report = {
        "status": "FAIL" if failures else "PASS",
        "failures": failures,
        "checked_paths": [
            str(DESIGN.relative_to(ROOT)),
            str(RECEIPT.relative_to(ROOT)),
            str(COMPLETION.relative_to(ROOT)),
            str(HANDOFF.relative_to(ROOT)),
            str(PROGRAM_STATE.relative_to(ROOT)),
        ],
        "burden_id": "source_detector_readout_semantics",
        "plan_task_id": "P5-T01",
        "selected_next_plan_task_id": "P5-T02",
        "ledger_row_updated": False,
        "physics_promotion_authorized": False,
    }
    if "--write-report" in sys.argv:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
