#!/usr/bin/env python3
"""Validate the P15-T01 compact current-frontier schema artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = ROOT / "research_control/design/compact_current_frontier_schema_v16.md"

REQUIRED_SNIPPETS = [
    'schema_id: "compact_current_frontier_v16"',
    '  - "research_control/program_state.yaml"',
    '  - "latest_handoff"',
    '  - "registries/DISTANCE_TO_GR_LEDGER.csv"',
    '  - "research_control/current_frontier.md"',
    "active_state:",
    "next_route:",
    "claim_boundary:",
    "scoped_positive_objects:",
    "scoped_evidence_preconditions:",
    "blocked_physical_targets:",
    "distance_to_gr:",
    "validation:",
    "authority_warning:",
    "snapshot_only_not_authority: true",
    "Generated wiki notes",
    "Obsidian notes",
    "semantic extracts",
    "SQLite retrieval",
    "`m_src`",
    "`g_eff`",
    "`matter_coupling`",
    "`einstein_equations`",
    "`benchmark_promotion`",
    "source-law adoption",
    "matter-coupling derivation or adoption",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
]


def build_report() -> dict[str, object]:
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    missing = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in text]
    return {
        "status": "PASS" if not missing else "FAIL",
        "schema_path": str(SCHEMA_PATH.relative_to(ROOT)),
        "schema_id": "compact_current_frontier_v16",
        "check_count": len(REQUIRED_SNIPPETS),
        "missing_required_snippets": missing,
        "snapshot_only_not_authority_required": True,
        "physics_claim_authority": False,
        "proof_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.output:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
