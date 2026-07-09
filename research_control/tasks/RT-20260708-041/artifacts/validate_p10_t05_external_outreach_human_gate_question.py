#!/usr/bin/env python3
"""Validate the v18 P10-T05 external-outreach human-gate setup artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT = ROOT / "research_control/tasks/RT-20260708-041/artifacts/external_outreach_human_gate_question_v1.yaml"
REPORT = ROOT / "research_control/tasks/RT-20260708-041/artifacts/p10_t05_external_outreach_human_gate_question_report.json"


REQUIRED_FORBIDDEN = {
    "external outreach",
    "reviewer naming",
    "outreach message sending or queueing",
    "external review completion claim",
    "external endorsement claim",
    "external feedback as proof authority",
    "benchmark promotion",
    "completed derivation",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("artifact root must be a mapping")
    return data


def validate(path: Path) -> dict[str, Any]:
    failures: list[str] = []
    data = _load_yaml(path)
    question = data.get("external_outreach_human_gate_question")
    if not isinstance(question, dict):
        failures.append("missing external_outreach_human_gate_question mapping")
        question = {}

    required_values = {
        "packet_path": "external_review_packets/eqsrc_family_closure_review_packet_v1.md",
        "proposed_outreach": "not_executed",
        "external_outreach_authorized_in_this_task": False,
        "human_gate_required_for_future_outreach": True,
        "external_feedback_as_proof_authority": False,
        "next_route": "P10-T06",
    }
    for key, expected in required_values.items():
        if question.get(key) != expected:
            failures.append(f"{key} must be {expected!r}")

    gate_question = question.get("gate_question")
    if not isinstance(gate_question, str) or not gate_question.strip():
        failures.append("gate_question must be nonblank")

    no_outreach = question.get("no_outreach_receipt")
    if not isinstance(no_outreach, dict):
        failures.append("missing no_outreach_receipt mapping")
        no_outreach = {}

    boolean_false_fields = [
        "external_message_sent",
        "external_message_queued",
        "outreach_message_created_for_delivery",
        "reviewer_named",
        "reviewer_identity_publication_allowed",
        "public_endorsement_claimed",
        "external_review_completed",
    ]
    for key in boolean_false_fields:
        if no_outreach.get(key) is not False:
            failures.append(f"no_outreach_receipt.{key} must be false")

    if no_outreach.get("proposed_reviewer_names") != []:
        failures.append("proposed_reviewer_names must be empty")

    future_scope = question.get("proposed_future_gate_scope")
    if not isinstance(future_scope, dict):
        failures.append("missing proposed_future_gate_scope mapping")
        future_scope = {}
    remains_forbidden = set(future_scope.get("remains_forbidden_without_later_gate") or [])
    missing_forbidden = sorted(REQUIRED_FORBIDDEN - remains_forbidden)
    if missing_forbidden:
        failures.append("missing forbidden future-gate entries: " + ", ".join(missing_forbidden))

    expectations = data.get("validation_expectations")
    if not isinstance(expectations, dict):
        failures.append("missing validation_expectations mapping")
        expectations = {}
    expected_true = [
        "human_gate_setup_exists",
        "no_external_message_sent",
        "no_reviewer_named",
        "next_route_is_p10_t06",
    ]
    for key in expected_true:
        if expectations.get(key) is not True:
            failures.append(f"validation_expectations.{key} must be true")
    if expectations.get("physics_promotion_authorized") is not False:
        failures.append("validation_expectations.physics_promotion_authorized must be false")

    status = "PASS" if not failures else "FAIL"
    return {
        "schema_id": "p10_t05_external_outreach_human_gate_question_validator_v1",
        "status": status,
        "artifact_path": str(path.relative_to(ROOT)),
        "packet_path": question.get("packet_path"),
        "proposed_outreach": question.get("proposed_outreach"),
        "external_outreach_authorized_in_this_task": question.get("external_outreach_authorized_in_this_task"),
        "human_gate_required_for_future_outreach": question.get("human_gate_required_for_future_outreach"),
        "external_feedback_as_proof_authority": question.get("external_feedback_as_proof_authority"),
        "no_external_message_sent": no_outreach.get("external_message_sent") is False,
        "no_reviewer_named": no_outreach.get("reviewer_named") is False and no_outreach.get("proposed_reviewer_names") == [],
        "next_route": question.get("next_route"),
        "physics_promotion_authorized": expectations.get("physics_promotion_authorized"),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", default=str(ARTIFACT))
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate(Path(args.artifact))
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
