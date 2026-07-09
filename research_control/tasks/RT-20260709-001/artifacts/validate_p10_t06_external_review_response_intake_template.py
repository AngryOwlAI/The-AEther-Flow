#!/usr/bin/env python3
"""Validate the v18 P10-T06 external-review response intake template."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
TEMPLATE_PATH = ROOT / "research_control/design/external_review_response_intake_template_v1.md"
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260709-001/artifacts/p10_t06_external_review_response_intake_template_report.json"
)

EXPECTED_ACTIONS = [
    "repair",
    "refuter_stress",
    "theorem_rewrite",
    "freeze_review",
    "no_action",
]


def _extract_template_yaml(text: str) -> dict:
    for match in re.finditer(r"```yaml\n(.*?)\n```", text, re.DOTALL):
        block = match.group(1)
        if "external_review_response_intake:" in block:
            loaded = yaml.safe_load(block)
            if not isinstance(loaded, dict):
                raise ValueError("Template YAML block does not parse to a mapping")
            return loaded
    raise ValueError("Missing fenced YAML block for external_review_response_intake")


def validate_template() -> dict:
    errors: list[str] = []
    text = TEMPLATE_PATH.read_text(encoding="utf-8")

    try:
        data = _extract_template_yaml(text)
    except Exception as exc:  # pragma: no cover - defensive diagnostic path
        return {"status": "FAIL", "errors": [str(exc)]}

    intake = data.get("external_review_response_intake")
    if not isinstance(intake, dict):
        errors.append("external_review_response_intake must be a mapping")
        intake = {}

    false_fields = [
        "reviewer_identity_publication_allowed",
        "proof_authority",
        "benchmark_authority",
        "endorsement_claim_authorized",
    ]
    for field in false_fields:
        if intake.get(field) is not False:
            errors.append(f"{field} must be exactly false")

    for field in ["response_received_at", "response_summary"]:
        if not isinstance(intake.get(field), str):
            errors.append(f"{field} must be a string placeholder")

    list_fields = [
        "theorem_issue_identified",
        "countermodel_issue_identified",
        "terminology_issue_identified",
        "overclaim_risk_identified",
    ]
    for field in list_fields:
        value = intake.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{field} must be list[string]")

    if intake.get("action_recommendation") != EXPECTED_ACTIONS:
        errors.append("action_recommendation must list exactly the v18 P10-T06 allowed actions")

    required_text = [
        "No outreach is performed by this template.",
        "No reviewer is named by this template.",
        "No external response is proof authority.",
        "No external response is benchmark authority.",
        "No external response is an endorsement claim.",
    ]
    for phrase in required_text:
        if phrase not in text:
            errors.append(f"missing boundary phrase: {phrase}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "template_path": str(TEMPLATE_PATH.relative_to(ROOT)),
        "required_false_fields": false_fields,
        "required_list_fields": list_fields,
        "expected_action_recommendation": EXPECTED_ACTIONS,
        "external_outreach_performed": False,
        "reviewer_named": False,
        "proof_authority": False,
        "benchmark_authority": False,
        "endorsement_claim_authorized": False,
        "next_route": "P11-T01",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate_template()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
