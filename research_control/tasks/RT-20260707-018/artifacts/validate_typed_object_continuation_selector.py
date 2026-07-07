#!/usr/bin/env python3
"""Task-local validation for RT-20260707-018 selector artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SELECTOR = ROOT / "typed_object_continuation_selector_v1.md"
RECEIPT = ROOT / "typed_object_continuation_selector_receipt.md"

REQUIRED = [
    "P3_T01_family_closure_theorem_or_countermodel_setup",
    'selected_next_packet_type: "bounded_theoretical_calculation"',
    'preserves_claim_blocks: true',
    'requires_human_gate: false',
    'general EqSrc discharge',
    'RetainH adoption',
    'GenH adoption',
    'source-law adoption',
    'no_distance_delta',
    'payload_type: "packet_selection"',
]

FORBIDDEN = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "source law is adopted",
    "matter coupling is derived",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "claims completed derivation",
]


def main() -> int:
    failures: list[str] = []
    selector_text = SELECTOR.read_text(encoding="utf-8")
    receipt_text = RECEIPT.read_text(encoding="utf-8")
    combined = selector_text + "\n" + receipt_text

    for token in REQUIRED:
        if token not in combined:
            failures.append(f"missing required token: {token}")

    for token in FORBIDDEN:
        if token in combined:
            failures.append(f"forbidden promoted wording: {token}")

    if combined.count("selected_route: \"P3_T01_family_closure_theorem_or_countermodel_setup\"") != 1:
        failures.append("expected exactly one YAML selected_route for P3_T01")

    result = {
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260707-018",
        "plan_task_id": "P2-T06",
        "selected_route": "P3_T01_family_closure_theorem_or_countermodel_setup",
        "next_packet_type": "bounded_theoretical_calculation",
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
