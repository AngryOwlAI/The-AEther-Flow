#!/usr/bin/env python3
"""Validate v14 P12 no-target hygiene phase integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml


PATHS = {
    "p12_t01_report": "research_control/tasks/RT-20260702-039/artifacts/p12_t01_no_target_hygiene_doctrine_report.json",
    "p12_t02_report": "research_control/tasks/RT-20260702-040/artifacts/p12_t02_positive_semantics_requirement_report.json",
    "p12_t03_report": "research_control/tasks/RT-20260702-041/artifacts/p12_t03_no_target_linter_examples_report.json",
    "handoff_0494": "research_control/handoffs/handoff-0494.yaml",
    "doctrine": "research_control/design/no_target_certificate_hygiene_doctrine.md",
    "requirement_note": "research_control/design/positive_semantics_requirement_note.md",
    "taxonomy": "research_control/design/claim_language_linter_taxonomy.yaml",
    "examples": "research_control/design/scoped_claim_language_examples.md",
}


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def read_text(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def require(condition: bool, issues: list[dict[str, str]], field: str, message: str) -> None:
    if not condition:
        issues.append({"field": field, "message": message})


def validate() -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    t01 = read_json(PATHS["p12_t01_report"])
    t02 = read_json(PATHS["p12_t02_report"])
    t03 = read_json(PATHS["p12_t03_report"])
    handoff_0494 = strict_yaml.load(REPO_ROOT / PATHS["handoff_0494"])
    doctrine = read_text(PATHS["doctrine"])
    requirement_note = read_text(PATHS["requirement_note"])
    taxonomy = read_text(PATHS["taxonomy"])
    examples = read_text(PATHS["examples"])

    for label, data in (("p12_t01_report", t01), ("p12_t02_report", t02), ("p12_t03_report", t03)):
        require(data.get("status") == "PASS", issues, f"{label}.status", "must be PASS")

    require(t03.get("fixture_no_target_finding_count", 0) >= 5, issues, "p12_t03.fixture_no_target_finding_count", "must prove no-target overread coverage")
    require(not t03.get("public_no_target_hard_failures"), issues, "p12_t03.public_no_target_hard_failures", "public surfaces must have zero no-target hard failures")

    required_phrases = [
        "source_hygiene_certificate_only",
        "negative certificate",
        "positive source-side matter semantics",
        "PositiveMSProfile_v1",
        "RR_E",
        "no-target certificate proves positive matter semantics",
        "no-target certificate provides proof authority",
    ]
    combined = "\n".join([doctrine, requirement_note, taxonomy, examples])
    for phrase in required_phrases:
        require(phrase in combined, issues, f"required_phrase:{phrase}", "missing required P12 phrase")

    boundary_terms = [
        "source-law adoption",
        "matter-semantics adoption",
        "detector-semantics adoption",
        "stress-energy semantics",
        "matter action",
        "Einstein equations",
        "benchmark promotion",
        "completed derivation",
    ]
    for phrase in boundary_terms:
        require(phrase in combined, issues, f"claim_boundary:{phrase}", "missing claim-boundary phrase")

    required_next = handoff_0494.get("required_next_packet", {})
    require(
        required_next.get("task_type") == "v14_p12_t04_no_target_hygiene_phase_validation",
        issues,
        "handoff_0494.required_next_packet.task_type",
        "must require P12-T04 validation",
    )

    status = "PASS" if not issues else "FAIL"
    return {
        "schema_id": "p12_no_target_hygiene_phase_validation_v1",
        "status": status,
        "task_id": "RT-20260702-042",
        "validated_plan_phase": "P12",
        "validated_tasks": ["P12-T01", "P12-T02", "P12-T03", "P12-T04"],
        "checked_paths": PATHS,
        "checks": {
            "hygiene_doctrine": "PASS" if not any(i["field"].startswith("p12_t01") for i in issues) else "FAIL",
            "positive_semantics_requirement": "PASS" if not any(i["field"].startswith("p12_t02") for i in issues) else "FAIL",
            "linter_examples": "PASS" if not any(i["field"].startswith("p12_t03") for i in issues) else "FAIL",
            "claim_boundary": "PASS" if not any(i["field"].startswith(("required_phrase", "claim_boundary")) for i in issues) else "FAIL",
            "handoff_boundary": "PASS" if not any(i["field"].startswith("handoff_") for i in issues) else "FAIL",
        },
        "issues": issues,
        "claim_boundary": {
            "phase_validation_is_physics_evidence": False,
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_sector_adoption_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
        "next_route": "P13-T01 RR_E separation boundary control note",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: P12 no-target hygiene phase validation")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
