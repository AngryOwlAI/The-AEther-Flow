#!/usr/bin/env python3
"""Validate the P14-T03 current-frontier final refresh."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
FRONTIER = ROOT / "research_control/current_frontier.md"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0503.yaml"
LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
REPORT = ROOT / "research_control/tasks/RT-20260702-050/artifacts/p14_t03_current_frontier_final_refresh_report.md"


REQUIRED_FRONTIER_PHRASES = [
    "`RT-20260702-050`",
    "`handoff-0503`",
    "Run one bounded v14 P14-T04 final validation packet.",
    "## Three-Tier Claim Summary Pilot",
    "## Scoped-Positive Alias Pilot",
    "## Validation And Authorization Layers",
    "## Distance-To-GR Table",
    "## Exact Blocked Claims",
    "accepted only as scoped source-extension evidence/precondition",
    "[ ] matter-coupling derivation",
    "[ ] Einstein equations",
    "[ ] exact-GR benchmark promotion",
    "[ ] completed derivation",
    "[ ] this snapshot as independent authority",
]

REQUIRED_REPORT_PHRASES = [
    "Matches `program_state.yaml` and latest handoff",
    "Matches Distance-to-GR ledger",
    "Includes scoped-positive language",
    "Includes three-tier claim summary",
    "Includes validation-layer status when implemented",
    "Blocks overclaims",
    "P14-T04 final validation",
]

FORBIDDEN_FRONTIER_PHRASES = [
    "Downstream promotion authorized | true",
    "benchmark promotion is complete",
    "completed derivation is established",
    "Einstein equations are derived",
    "matter coupling is derived",
    "this file is independent routing authority",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    frontier = FRONTIER.read_text()
    program_state = PROGRAM_STATE.read_text()
    handoff = HANDOFF.read_text()
    ledger = LEDGER.read_text()
    report_text = REPORT.read_text()

    for phrase in REQUIRED_FRONTIER_PHRASES:
        if phrase not in frontier:
            failures.append(f"frontier missing required phrase: {phrase}")

    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase not in report_text:
            failures.append(f"report missing required phrase: {phrase}")

    for phrase in FORBIDDEN_FRONTIER_PHRASES:
        if phrase in frontier:
            failures.append(f"frontier contains forbidden overclaim phrase: {phrase}")

    state_checks = {
        "program_state_active_task": 'active_task_id: "RT-20260702-050"' in program_state,
        "program_state_latest_handoff": 'latest_handoff_id: "handoff-0503"' in program_state,
        "program_state_next_p14_t04": "P14-T04 final validation" in program_state,
        "handoff_next_p14_t04": "Run one bounded v14 P14-T04 final validation packet." in handoff,
        "ledger_matter_coupling_guard": "no_matter_coupling_derivation" in ledger,
        "ledger_einstein_guard": "no_einstein_equations" in ledger,
        "ledger_benchmark_guard": "no_benchmark_promotion" in ledger,
    }
    for key, passed in state_checks.items():
        if not passed:
            failures.append(f"state check failed: {key}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "state_checks": state_checks,
        "source_hashes": {
            "current_frontier": sha256(FRONTIER),
            "program_state": sha256(PROGRAM_STATE),
            "handoff": sha256(HANDOFF),
            "distance_to_gr_ledger": sha256(LEDGER),
            "refresh_report": sha256(REPORT),
        },
        "claim_boundary": {
            "frontier_snapshot_only": True,
            "physics_claim_promotion_authorized": False,
        },
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
