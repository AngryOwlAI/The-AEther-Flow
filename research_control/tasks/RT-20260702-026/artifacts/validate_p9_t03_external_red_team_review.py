#!/usr/bin/env python3
"""Validate the v14 P9-T03 external red-team pilot artifact."""

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
from scripts.research_control.validate_red_team_review_artifact import validate_review_file


ARTIFACT_PATH = REPO_ROOT / "research_control/tasks/RT-20260702-026/artifacts/p9_t03_external_red_team_review_core_frontier.yaml"

REQUIRED_OBJECTS = {
    "M_src",
    "g_eff",
    "MSStableMatterSemanticsBridge_v1",
    "SourceMatterSemanticsAdoptionReadinessLaw_v1",
    "PositiveMSProfile_v1",
    "RR_E_underdetermination_obstruction",
    "RR_ETransportCompletenessOrInvarianceLaw_v1",
}

V14_VERDICTS = {
    "no_blocking_issue_found_within_scope",
    "repair_required",
    "scoped_obstruction_candidate",
    "freeze_candidate",
    "literature_review_required",
    "selector_required",
    "human_gate_required",
}

REQUIRED_FALSE_AUTHORITY_FLAGS = (
    "proof_authority",
    "ontology_edit_authorized",
    "source_law_adoption_authorized",
    "downstream_physics_promotion_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
)


def _issue(field: str, message: str) -> dict[str, str]:
    return {"field": field, "message": message}


def validate_v14_overlay(data: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    findings = data.get("per_object_findings")
    if not isinstance(findings, list):
        return [_issue("per_object_findings", "must be a list")]

    seen: set[str] = set()
    for index, item in enumerate(findings):
        if not isinstance(item, dict):
            issues.append(_issue(f"per_object_findings[{index}]", "must be a map"))
            continue
        object_id = item.get("object_id")
        verdict = item.get("v14_verdict")
        if object_id not in REQUIRED_OBJECTS:
            issues.append(_issue(f"per_object_findings[{index}].object_id", "unexpected or missing object id"))
        else:
            seen.add(object_id)
        if verdict not in V14_VERDICTS:
            issues.append(_issue(f"per_object_findings[{index}].v14_verdict", "invalid v14 verdict"))
        for required_text_field in ("finding", "route_pressure", "forbidden_overread"):
            value = item.get(required_text_field)
            if not isinstance(value, str) or not value.strip():
                issues.append(_issue(f"per_object_findings[{index}].{required_text_field}", "must be a nonempty string"))

    missing = sorted(REQUIRED_OBJECTS - seen)
    extra = sorted(seen - REQUIRED_OBJECTS)
    if missing:
        issues.append(_issue("per_object_findings", f"missing required objects: {', '.join(missing)}"))
    if extra:
        issues.append(_issue("per_object_findings", f"unexpected objects: {', '.join(extra)}"))
    if len(findings) != len(REQUIRED_OBJECTS):
        issues.append(_issue("per_object_findings", "must contain exactly seven findings"))

    recommendation = data.get("recommendation", {})
    if not isinstance(recommendation, dict) or recommendation.get("primary") != "selector_required":
        issues.append(_issue("recommendation.primary", "must route substantive findings to selector_required"))

    if data.get("recommended_next_route") != "v14_p9_t04_external_red_team_findings_selector":
        issues.append(_issue("recommended_next_route", "must route to P9-T04 selector"))

    if data.get("physics_promotion_authorized") is not False:
        issues.append(_issue("physics_promotion_authorized", "must be false"))

    auth = data.get("authorization_layers")
    if not isinstance(auth, dict):
        issues.append(_issue("authorization_layers", "must be a map"))
    else:
        for flag in REQUIRED_FALSE_AUTHORITY_FLAGS:
            if auth.get(flag) is not False:
                issues.append(_issue(f"authorization_layers.{flag}", "must be false"))

    if data.get("workflow_success_disregarded_as_evidence") is not True:
        issues.append(_issue("workflow_success_disregarded_as_evidence", "must be true"))
    if data.get("validator_success_disregarded_as_evidence") is not True:
        issues.append(_issue("validator_success_disregarded_as_evidence", "must be true"))
    if data.get("registry_status_disregarded_as_proof") is not True:
        issues.append(_issue("registry_status_disregarded_as_proof", "must be true"))

    return issues


def build_report(path: Path) -> dict[str, Any]:
    global_receipt = validate_review_file(path)
    data = strict_yaml.load(path)
    issues = validate_v14_overlay(data)
    if issues:
        return {
            "schema_id": "p9_t03_external_red_team_review_v14_overlay_validator",
            "status": "FAIL",
            "artifact_path": path.as_posix(),
            "issues": issues,
            "global_review_validator": global_receipt,
            "physics_promotion_authorized": False,
        }

    return {
        "schema_id": "p9_t03_external_red_team_review_v14_overlay_validator",
        "status": "PASS",
        "artifact_path": path.as_posix(),
        "checked_object_count": len(REQUIRED_OBJECTS),
        "v14_verdicts_seen": {
            item["object_id"]: item["v14_verdict"]
            for item in data["per_object_findings"]
        },
        "global_review_validator": global_receipt,
        "recommended_next_route": data["recommended_next_route"],
        "physics_promotion_authorized": False,
        "authority_boundary": "shape_and_coverage_validation_only_no_proof_authority_no_gate_chair_authority",
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
