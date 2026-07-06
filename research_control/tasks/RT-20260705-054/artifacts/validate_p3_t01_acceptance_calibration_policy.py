#!/usr/bin/env python3
"""Validate the v17 P3-T01 accepted-status calibration policy artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_HEADINGS = [
    "## 1. Problem Statement",
    "## 2. Calibrated Acceptance Principle",
    "## 3. Positive-First Status-Card Model",
    "## 4. High-Risk Rows Covered",
    "## 5. Preferred Wording Patterns",
    "## 6. Forbidden Overclaim Patterns",
    "## 7. Forbidden Underclaim Patterns",
    "## 8. Public-Summary Compression Rule",
    "## 9. Full-Control Non-Conclusion Rule",
    "## 10. Renderer and Linter Implementation Requirements",
    "## 11. Examples",
]

REQUIRED_PHRASES = [
    "Positive status first",
    "Exact scope second",
    "Blocked overread third",
    "Scoped adoption/evidence/precondition is basically nothing.",
    "canonical ontology adoption",
    "source-law adoption",
    "coupling-law adoption",
    "matter-coupling derivation",
    "stress-energy tensor",
    "matter action",
    "Einstein equations",
    "benchmark promotion",
    "Gate Chair verdict",
    "completed derivation",
    "Future source-extension impossibility claim",
    "`positive_status`",
    "`exact_scope`",
    "`blocked_overread`",
    "`M_src`",
    "`g_eff`",
    "`matter_coupling`",
    "`Resp_lc`",
    "`NarrowMSCertEq_v1`",
    "Frozen-negative routes",
    "No-Physics-Delta Boundary",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--policy",
        default="research_control/design/accepted_status_calibration_policy_v1.md",
    )
    parser.add_argument(
        "--output",
        default=(
            "research_control/tasks/RT-20260705-054/artifacts/"
            "p3_t01_acceptance_calibration_policy_report.json"
        ),
    )
    args = parser.parse_args()

    policy_path = Path(args.policy)
    output_path = Path(args.output)
    text = policy_path.read_text(encoding="utf-8")

    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]

    lower_text = text.lower()
    order_terms = [
        "positive status first",
        "exact scope second",
        "blocked overread third",
    ]
    order_positions = [lower_text.find(term) for term in order_terms]
    ordered_status_rule = all(pos >= 0 for pos in order_positions) and order_positions == sorted(order_positions)

    report = {
        "status": "PASS"
        if not missing_headings and not missing_phrases and ordered_status_rule
        else "FAIL",
        "policy": str(policy_path),
        "missing_headings": missing_headings,
        "missing_phrases": missing_phrases,
        "ordered_status_rule": ordered_status_rule,
        "checks": {
            "required_sections_present": not missing_headings,
            "required_phrases_present": not missing_phrases,
            "positive_exact_blocked_order_present": ordered_status_rule,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
