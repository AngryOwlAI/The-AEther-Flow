#!/usr/bin/env python3
"""Validate the v14 P9-T04 red-team findings selector artifact."""

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


ARTIFACT_PATH = REPO_ROOT / "research_control/tasks/RT-20260702-027/artifacts/p9_t04_red_team_findings_selector_v1.yaml"
REQUIRED_OBJECTS = {
    "M_src",
    "g_eff",
    "MSStableMatterSemanticsBridge_v1",
    "SourceMatterSemanticsAdoptionReadinessLaw_v1",
    "PositiveMSProfile_v1",
    "RR_E_underdetermination_obstruction",
    "RR_ETransportCompletenessOrInvarianceLaw_v1",
}


def issue(field: str, message: str) -> dict[str, str]:
    return {"field": field, "message": message}


def validate(data: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if data.get("selected_route") != "no_action_record_findings_then_phase_validation":
        issues.append(issue("selected_route", "must select no_action_record_findings_then_phase_validation"))
    if data.get("selected_next_packet_type") != "phase_validation_packet":
        issues.append(issue("selected_next_packet_type", "must route to phase_validation_packet"))

    tdo = data.get("theoretical_decision_output")
    if not isinstance(tdo, dict):
        issues.append(issue("theoretical_decision_output", "must be a map"))
    else:
        required_fields = (
            "selected_next_packet_type",
            "decision_basis",
            "theoretical_method",
            "preserves_claim_blocks",
            "requires_human_gate",
            "human_gate_reason",
        )
        for field in required_fields:
            if field not in tdo:
                issues.append(issue(f"theoretical_decision_output.{field}", "missing required field"))
        if tdo.get("preserves_claim_blocks") is not True:
            issues.append(issue("theoretical_decision_output.preserves_claim_blocks", "must be true"))
        if tdo.get("requires_human_gate") is not False:
            issues.append(issue("theoretical_decision_output.requires_human_gate", "must be false"))

    classifications = data.get("route_classifications")
    if not isinstance(classifications, list):
        issues.append(issue("route_classifications", "must be a list"))
    else:
        seen = set()
        for index, item in enumerate(classifications):
            if not isinstance(item, dict):
                issues.append(issue(f"route_classifications[{index}]", "must be a map"))
                continue
            object_id = item.get("object_id")
            if object_id in REQUIRED_OBJECTS:
                seen.add(object_id)
            else:
                issues.append(issue(f"route_classifications[{index}].object_id", "unexpected object id"))
            route = item.get("selected_p9_route")
            if route not in {"no_action_record_finding", "record_guard_finding", "record_scoped_obstruction_finding"}:
                issues.append(issue(f"route_classifications[{index}].selected_p9_route", "invalid P9 route"))
        missing = sorted(REQUIRED_OBJECTS - seen)
        if missing:
            issues.append(issue("route_classifications", f"missing objects: {', '.join(missing)}"))

    auth = data.get("claim_boundary")
    if not isinstance(auth, dict):
        issues.append(issue("claim_boundary", "must be a map"))
    else:
        for flag in (
            "proof_authority",
            "ontology_edit_authorized",
            "source_law_adoption_authorized",
            "downstream_physics_promotion_authorized",
            "benchmark_promotion_authorized",
            "completed_derivation_authorized",
        ):
            if auth.get(flag) is not False:
                issues.append(issue(f"claim_boundary.{flag}", "must be false"))
    return issues


def build_report(path: Path) -> dict[str, Any]:
    data = strict_yaml.load(path)
    issues = validate(data)
    if issues:
        return {
            "schema_id": "p9_t04_red_team_findings_selector_validator",
            "status": "FAIL",
            "artifact_path": path.as_posix(),
            "issues": issues,
            "physics_promotion_authorized": False,
        }
    return {
        "schema_id": "p9_t04_red_team_findings_selector_validator",
        "status": "PASS",
        "artifact_path": path.as_posix(),
        "checked_object_count": len(REQUIRED_OBJECTS),
        "selected_route": data["selected_route"],
        "selected_next_packet_type": data["selected_next_packet_type"],
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", default=ARTIFACT_PATH.as_posix())
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(Path(args.artifact))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {output_path}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
