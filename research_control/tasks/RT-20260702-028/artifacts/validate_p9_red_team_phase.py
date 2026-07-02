#!/usr/bin/env python3
"""Validate v14 P9 external red-team phase integration."""

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
    "p9_t01_report": "research_control/tasks/RT-20260702-024/artifacts/p9_t01_external_red_team_role_contract_report.json",
    "p9_t02_report": "research_control/tasks/RT-20260702-025/artifacts/p9_t02_red_team_review_template_report.json",
    "p9_t03_report": "research_control/tasks/RT-20260702-026/artifacts/p9_t03_external_red_team_review_report.json",
    "p9_t04_report": "research_control/tasks/RT-20260702-027/artifacts/p9_t04_red_team_findings_selector_report.json",
    "p9_t04_selector": "research_control/tasks/RT-20260702-027/artifacts/p9_t04_red_team_findings_selector_v1.yaml",
    "handoff_0480": "research_control/handoffs/handoff-0480.yaml",
}


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def check_status(label: str, data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    if data.get("status") != "PASS":
        issues.append({"field": label, "message": "status must be PASS"})


def validate() -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    p9_t01 = read_json(PATHS["p9_t01_report"])
    p9_t02 = read_json(PATHS["p9_t02_report"])
    p9_t03 = read_json(PATHS["p9_t03_report"])
    p9_t04 = read_json(PATHS["p9_t04_report"])
    selector = strict_yaml.load(REPO_ROOT / PATHS["p9_t04_selector"])
    handoff = strict_yaml.load(REPO_ROOT / PATHS["handoff_0480"])

    for label, data in (
        ("p9_t01_report", p9_t01),
        ("p9_t02_report", p9_t02),
        ("p9_t03_report", p9_t03),
        ("p9_t04_report", p9_t04),
    ):
        check_status(label, data, issues)

    t01_boundary = p9_t01.get("claim_boundary", {})
    if t01_boundary.get("may_promote_claims") is not False:
        issues.append({"field": "p9_t01.claim_boundary.may_promote_claims", "message": "must be false"})
    role_row = next((item for item in p9_t01.get("checks", []) if item.get("label") == "agent_role_registry"), {})
    row = role_row.get("row", {})
    if row.get("requires_human_gate") != "false" or row.get("may_promote_claims") != "false":
        issues.append({"field": "p9_t01.agent_role_registry", "message": "role registry must keep non-promotional ordinary execution"})

    if p9_t02.get("issues") != []:
        issues.append({"field": "p9_t02.issues", "message": "template validator must have no issues"})
    if len(p9_t02.get("v14_required_sections", [])) < 14:
        issues.append({"field": "p9_t02.v14_required_sections", "message": "must contain all v14 review sections"})
    if "selector" not in p9_t02.get("v14_allowed_recommendations", []):
        issues.append({"field": "p9_t02.v14_allowed_recommendations", "message": "must include selector route"})

    if p9_t03.get("checked_object_count") != 7:
        issues.append({"field": "p9_t03.checked_object_count", "message": "must validate seven core frontier objects"})
    if p9_t03.get("physics_promotion_authorized") is not False:
        issues.append({"field": "p9_t03.physics_promotion_authorized", "message": "must be false"})
    if p9_t03.get("recommended_next_route") != "v14_p9_t04_external_red_team_findings_selector":
        issues.append({"field": "p9_t03.recommended_next_route", "message": "must route to P9-T04"})

    if p9_t04.get("checked_object_count") != 7:
        issues.append({"field": "p9_t04.checked_object_count", "message": "must validate seven route classifications"})
    if p9_t04.get("selected_route") != "no_action_record_findings_then_phase_validation":
        issues.append({"field": "p9_t04.selected_route", "message": "must record findings and route to phase validation"})
    if p9_t04.get("selected_next_packet_type") != "phase_validation_packet":
        issues.append({"field": "p9_t04.selected_next_packet_type", "message": "must route to phase validation"})

    selector_boundary = selector.get("claim_boundary", {})
    for flag in (
        "proof_authority",
        "ontology_edit_authorized",
        "source_law_adoption_authorized",
        "downstream_physics_promotion_authorized",
        "benchmark_promotion_authorized",
        "completed_derivation_authorized",
    ):
        if selector_boundary.get(flag) is not False:
            issues.append({"field": f"selector.claim_boundary.{flag}", "message": "must be false"})

    required = handoff.get("required_next_packet", {})
    if required.get("role_id") != "validator-engineer":
        issues.append({"field": "handoff_0480.required_next_packet.role_id", "message": "must require validator-engineer"})
    if "P9-T05" not in handoff.get("next_action", ""):
        issues.append({"field": "handoff_0480.next_action", "message": "must require P9-T05"})

    status = "PASS" if not issues else "FAIL"
    return {
        "schema_id": "p9_red_team_phase_validation_v1",
        "status": status,
        "task_id": "RT-20260702-028",
        "validated_plan_phase": "P9",
        "validated_tasks": ["P9-T01", "P9-T02", "P9-T03", "P9-T04", "P9-T05"],
        "checked_paths": PATHS,
        "checks": {
            "role_contract": "PASS" if not any(i["field"].startswith("p9_t01") for i in issues) else "FAIL",
            "review_template": "PASS" if not any(i["field"].startswith("p9_t02") for i in issues) else "FAIL",
            "red_team_pilot": "PASS" if not any(i["field"].startswith("p9_t03") for i in issues) else "FAIL",
            "findings_selector": "PASS" if not any(i["field"].startswith(("p9_t04", "selector")) for i in issues) else "FAIL",
            "handoff_boundary": "PASS" if not any(i["field"].startswith("handoff_0480") for i in issues) else "FAIL",
        },
        "issues": issues,
        "claim_boundary": {
            "phase_validation_is_physics_evidence": False,
            "physics_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
        "next_route": "P10-T01 literature-comparison scope selector",
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
        print(f"{report['status']}: P9 phase validation")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
