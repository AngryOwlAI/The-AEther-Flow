#!/usr/bin/env python3
"""Validate v14 P11 matter-coupling moratorium phase integration."""

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
    "p11_t01_report": "research_control/tasks/RT-20260702-034/artifacts/p11_t01_matter_coupling_moratorium_report.json",
    "p11_t02_report": "research_control/tasks/RT-20260702-035/artifacts/p11_t02_pre_adoption_checklist_report.json",
    "p11_t03_report": "research_control/tasks/RT-20260702-036/artifacts/p11_t03_narrow_theorem_selector_report.json",
    "p11_t03_selector": "research_control/tasks/RT-20260702-036/artifacts/p11_t03_narrow_theorem_target_selector_v1.yaml",
    "p11_t04_report": "research_control/tasks/RT-20260702-037/artifacts/p11_t04_narrow_theorem_template_report.json",
    "handoff_0490": "research_control/handoffs/handoff-0490.yaml",
    "handoff_0491": "research_control/handoffs/handoff-0491.yaml",
    "moratorium_note": "research_control/design/matter_coupling_derivation_moratorium.md",
    "pre_adoption_checklist": "research_control/design/matter_coupling_pre_adoption_checklist.md",
    "narrow_template": "research_control/design/narrow_theorem_task_template.md",
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
    t01 = read_json(PATHS["p11_t01_report"])
    t02 = read_json(PATHS["p11_t02_report"])
    t03 = read_json(PATHS["p11_t03_report"])
    t04 = read_json(PATHS["p11_t04_report"])
    selector = strict_yaml.load(REPO_ROOT / PATHS["p11_t03_selector"])
    handoff_0490 = strict_yaml.load(REPO_ROOT / PATHS["handoff_0490"])
    handoff_0491 = strict_yaml.load(REPO_ROOT / PATHS["handoff_0491"])
    moratorium = read_text(PATHS["moratorium_note"])
    checklist = read_text(PATHS["pre_adoption_checklist"])
    template = read_text(PATHS["narrow_template"])

    for label, data in (
        ("p11_t01_report", t01),
        ("p11_t02_report", t02),
        ("p11_t03_report", t03),
        ("p11_t04_report", t04),
    ):
        require(data.get("status") == "PASS", issues, f"{label}.status", "must be PASS")

    require(t01.get("forbidden_overread_count", 0) >= 16, issues, "p11_t01.forbidden_overread_count", "must cover v14 forbidden overreads")
    require(t02.get("required_section_count", 0) >= 12, issues, "p11_t02.required_section_count", "must cover v14 checklist sections")
    require(
        selector.get("selected_route") == "no_target_certificate_hygiene_theorem_first",
        issues,
        "selector.selected_route",
        "must select no-target certificate hygiene first",
    )
    require(
        selector.get("selected_next_plan_task_id") == "P11-T04",
        issues,
        "selector.selected_next_plan_task_id",
        "must route to P11-T04 before P12",
    )
    require(
        any(check.get("name") == "handoff_routes_to_p11_t05" and check.get("status") == "PASS" for check in t04.get("checks", [])),
        issues,
        "p11_t04.handoff_routes_to_p11_t05",
        "must prove P11-T04 routed to P11-T05",
    )

    required_0490 = handoff_0490.get("required_next_packet", {})
    require(
        required_0490.get("task_type") == "v14_p11_t05_matter_coupling_moratorium_validation",
        issues,
        "handoff_0490.required_next_packet.task_type",
        "must require P11-T05 validation",
    )
    required_0491 = handoff_0491.get("required_next_packet", {})
    require(required_0491.get("task_type") == "v14_p12_t01_no_target_certificate_hygiene_doctrine", issues, "handoff_0491.required_next_packet.task_type", "must route to P12-T01 doctrine")
    require(required_0491.get("role_id") in {"project-control-maintainer", "documentation-curator"}, issues, "handoff_0491.required_next_packet.role_id", "must use a lawful P12-T01 project-control role")

    required_phrases = [
        "Direct universal matter-coupling derivation is blocked",
        "not a claim that matter coupling is impossible",
        "no-target certificate hygiene",
        "matter_coupling_pre_adoption_checklist",
        "negative hygiene, positive evidence",
        "forbidden_downstream_overreads_required: true",
    ]
    combined = "\n".join([moratorium, checklist, template])
    for phrase in required_phrases:
        require(phrase in combined, issues, f"required_phrase:{phrase}", "missing required P11 control phrase")

    forbidden_overreads = [
        "matter-semantics adoption",
        "detector-semantics adoption",
        "coupling-law adoption",
        "matter-coupling derivation or adoption",
        "stress-energy semantics",
        "matter action",
        "Einstein equations",
        "benchmark promotion",
        "completed derivation",
    ]
    for phrase in forbidden_overreads:
        require(phrase in combined, issues, f"forbidden_boundary:{phrase}", "missing forbidden overread boundary")

    status = "PASS" if not issues else "FAIL"
    return {
        "schema_id": "p11_matter_coupling_moratorium_phase_validation_v1",
        "status": status,
        "task_id": "RT-20260702-038",
        "validated_plan_phase": "P11",
        "validated_tasks": ["P11-T01", "P11-T02", "P11-T03", "P11-T04", "P11-T05"],
        "checked_paths": PATHS,
        "checks": {
            "moratorium_note": "PASS" if not any(i["field"].startswith("p11_t01") for i in issues) else "FAIL",
            "pre_adoption_checklist": "PASS" if not any(i["field"].startswith("p11_t02") for i in issues) else "FAIL",
            "narrow_theorem_selector": "PASS" if not any(i["field"].startswith(("p11_t03", "selector")) for i in issues) else "FAIL",
            "narrow_theorem_template": "PASS" if not any(i["field"].startswith("p11_t04") for i in issues) else "FAIL",
            "handoff_boundary": "PASS" if not any(i["field"].startswith("handoff_") for i in issues) else "FAIL",
            "claim_boundary": "PASS" if not any(i["field"].startswith(("required_phrase", "forbidden_boundary")) for i in issues) else "FAIL",
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
        "next_route": "P12-T01 no-target certificate hygiene doctrine",
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
        print(f"{report['status']}: P11 matter-coupling moratorium phase validation")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
