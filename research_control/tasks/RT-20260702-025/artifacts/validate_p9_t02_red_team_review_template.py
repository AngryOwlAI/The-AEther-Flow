#!/usr/bin/env python3
"""Validate the v14 P9-T02 red-team review template coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml  # noqa: E402
from scripts.research_control.validate_red_team_review_artifact import (  # noqa: E402
    REQUIRED_FIELDS as LEGACY_REQUIRED_FIELDS,
)


TEMPLATE_PATH = Path("research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml")

V14_REQUIRED_SECTIONS = (
    "object_under_attack",
    "source_files_reviewed",
    "status_being_tested",
    "definitions_attacked",
    "hidden_target_imports",
    "no_target_certificate_overread",
    "circularity_checks",
    "process_authority_checks",
    "evidence_as_adoption_checks",
    "rr_e_collapse_checks",
    "overclaim_checks",
    "finite_counterexamples",
    "comparison_to_known_constraints",
    "recommendation",
)

V14_ALLOWED_RECOMMENDATIONS = {
    "repair",
    "obstruction",
    "freeze",
    "literature_comparison",
    "selector",
    "no_action",
}

FALSE_AUTHORITY_FLAGS = (
    "physics_promotion_authorized",
    "gate_chair_authority_created",
    "source_law_adopted",
    "metric_data_adopted",
    "geff_adopted_or_expanded",
    "coupling_law_adopted",
    "matter_coupling_derived_or_adopted",
    "stress_energy_semantics_imported",
    "detector_semantics_imported",
    "matter_action_imported",
    "einstein_equations_derived",
    "benchmark_promoted",
    "completed_derivation_claimed",
)


def _get_nested(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = data
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def validate_template(path: Path) -> dict[str, Any]:
    data = strict_yaml.load(path)
    issues: list[dict[str, str]] = []

    for field in LEGACY_REQUIRED_FIELDS:
        if field not in data:
            issues.append({"field": field, "message": "missing legacy validator field"})

    for field in V14_REQUIRED_SECTIONS:
        if field not in data:
            issues.append({"field": field, "message": "missing v14 review section"})

    for list_field in (
        "source_files_reviewed",
        "definitions_attacked",
        "reviewed_source_paths",
        "assumptions_read",
        "definitions_read",
        "proof_steps_checked",
    ):
        if list_field in data and not isinstance(data[list_field], list):
            issues.append({"field": list_field, "message": "must be a list"})

    for map_field in (
        "object_under_attack",
        "status_being_tested",
        "hidden_target_imports",
        "no_target_certificate_overread",
        "circularity_checks",
        "process_authority_checks",
        "evidence_as_adoption_checks",
        "rr_e_collapse_checks",
        "overclaim_checks",
        "finite_counterexamples",
        "comparison_to_known_constraints",
        "recommendation",
    ):
        if map_field in data and not isinstance(data[map_field], dict):
            issues.append({"field": map_field, "message": "must be a map"})

    process_workflow_flag = _get_nested(
        data, ("process_authority_checks", "workflow_success_disregarded_as_evidence")
    )
    if process_workflow_flag is not True:
        issues.append(
            {
                "field": "process_authority_checks.workflow_success_disregarded_as_evidence",
                "message": "must be exactly true",
            }
        )

    process_validator_flag = _get_nested(
        data, ("process_authority_checks", "validator_success_disregarded_as_evidence")
    )
    if process_validator_flag is not True:
        issues.append(
            {
                "field": "process_authority_checks.validator_success_disregarded_as_evidence",
                "message": "must be exactly true",
            }
        )

    allowed = _get_nested(data, ("recommendation", "allowed_recommendations"))
    if not isinstance(allowed, list) or set(allowed) != V14_ALLOWED_RECOMMENDATIONS:
        issues.append(
            {
                "field": "recommendation.allowed_recommendations",
                "message": "must contain the exact v14 recommendation vocabulary",
            }
        )

    for field in FALSE_AUTHORITY_FLAGS:
        if data.get(field) is not False:
            issues.append({"field": field, "message": "must be exactly false"})

    non_authority = str(data.get("non_authority_statement", ""))
    for required_text in (
        "not proof authority",
        "source-law adoption",
        "benchmark promotion",
        "completed derivation",
    ):
        if required_text not in non_authority:
            issues.append(
                {
                    "field": "non_authority_statement",
                    "message": f"missing required boundary phrase: {required_text}",
                }
            )

    return {
        "status": "PASS" if not issues else "FAIL",
        "template_path": path.as_posix(),
        "legacy_required_fields": list(LEGACY_REQUIRED_FIELDS),
        "v14_required_sections": list(V14_REQUIRED_SECTIONS),
        "v14_allowed_recommendations": sorted(V14_ALLOWED_RECOMMENDATIONS),
        "authority_flags_checked": list(FALSE_AUTHORITY_FLAGS),
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", default=TEMPLATE_PATH.as_posix())
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_template(Path(args.template))
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    if args.json:
        print(payload)
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
