#!/usr/bin/env python3
"""Validate the v18 P4-T01 countermodel-obligation policy artifact."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
POLICY = ROOT / "research_control/design/minimal_countermodel_obligation_policy_v1.md"
REPORT = ROOT / "research_control/tasks/RT-20260708-001/artifacts/p4_t01_countermodel_obligation_policy_report.json"

REQUIRED_HEADINGS = [
    "## 1. Why Theorem Attempts Require Countermodel Slots",
    "## 2. Countermodel, Obstruction, Freeze, And Program-Wide No-Go",
    "## 3. Required Countermodel Slots By Theorem Family",
    "## 4. EqSrc-Specific Slots",
    "## 5. Matter-Coupling-Specific Slots",
    "## 6. Detector/Readout-Specific Slots",
    "## 7. Toy-Model-Specific Slots",
    "## 8. Completion Receipt Requirements",
    "## 9. Validator Requirements",
    "## 10. Forbidden Conclusions",
]

REQUIRED_PHRASES = [
    "Every future theorem attempt must either fill the required countermodel slots",
    "waived by an explicit Director Decision Record",
    "missing_inverse_countermodel",
    "missing_composition_countermodel",
    "RetainH_needed_countermodel",
    "GenH_needed_countermodel",
    "source_matter_semantics_missing_countermodel",
    "detector_semantics_import_countermodel",
    "toy_model_countermodel_slots",
    "countermodel_obligations:",
    "countermodel_overread_as_program_wide_no_go",
    "local_countermodel_as_program_wide_no_go_forbidden: true",
    "next_plan_task_id: \"P4-T02\"",
]

FORBIDDEN_POSITIVE_PATTERNS = [
    "authorizes source-law adoption",
    "authorizes matter-coupling derivation",
    "authorizes Einstein equations",
    "authorizes benchmark promotion",
    "authorizes completed derivation",
    "program-wide no-go is established",
    "program-wide no-go conclusion is authorized",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    if not POLICY.exists():
        failures.append(f"missing policy path: {POLICY.relative_to(ROOT)}")
        text = ""
    else:
        text = POLICY.read_text(encoding="utf-8")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"missing heading: {heading}")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"missing required phrase: {phrase}")

    lowered = text.lower()
    for pattern in FORBIDDEN_POSITIVE_PATTERNS:
        if pattern in lowered:
            failures.append(f"forbidden positive pattern present: {pattern}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "policy_path": str(POLICY.relative_to(ROOT)),
        "policy_hash": sha256(POLICY) if POLICY.exists() else "",
        "required_heading_count": len(REQUIRED_HEADINGS),
        "required_phrase_count": len(REQUIRED_PHRASES),
        "failures": failures,
        "done_criteria": {
            "countermodel_slots_mandatory_unless_ddr_waived": "PASS" if "waived by an explicit Director Decision Record" in text else "FAIL",
            "local_countermodel_program_wide_no_go_forbidden": "PASS" if "local_countermodel_as_program_wide_no_go_forbidden: true" in text else "FAIL",
            "next_route_p4_t02": "PASS" if "next_plan_task_id: \"P4-T02\"" in text else "FAIL",
        },
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
