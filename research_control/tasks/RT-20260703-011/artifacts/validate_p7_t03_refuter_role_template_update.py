#!/usr/bin/env python3
"""Validate the v15 P7-T03 Refuter role/template update."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
ROLE_PATH = REPO_ROOT / ".agents/roles/physics/refuter.v0.2.0.md"
TEMPLATE_PATH = REPO_ROOT / "research_control/templates/COMPLETION_TEMPLATE.yaml"
SCHEMA_PATH = "research_control/design/refuter_obstruction_schema_v1.md"
CATALOG_PATH = "research_control/design/refuter_countermodel_fixture_catalog_v1.md"

REQUIRED_RECORD_FIELDS = [
    "refuter_obstruction_record",
    "obstruction_id",
    "target_claim",
    "target_milestone",
    "failed_premise",
    "minimal_countermodel_available",
    "countermodel_path",
    "countermodel_scope",
    "certificate_gap",
    "source_extension_repair_possible",
    "global_no_go_claim_authorized",
    "future_source_extension_impossibility_authorized",
    "freeze_criteria_status",
    "route_cycle_control",
    "forbidden_conclusions",
]

ROLE_REQUIRED_SNIPPETS = [
    "Formal Obstruction Records",
    "refuter_obstruction_record",
    SCHEMA_PATH,
    CATALOG_PATH,
    "failed_premise",
    "needs more work",
    "must not be treated as PASS",
    "minimal_countermodel_available: true",
    "countermodel_path",
    "global_no_go_claim_authorized",
    "future_source_extension_impossibility_authorized",
]

TEMPLATE_REQUIRED_SNIPPETS = [
    "refuter_obstruction_record:",
    "required_when_refuter_obstruction: true",
    "pass_requires_actual_failed_premise: true",
    "vague_failure_language_sufficient_for_pass: false",
    f'schema_path: "{SCHEMA_PATH}"',
    f'fixture_catalog_path: "{CATALOG_PATH}"',
    "failed_premise:",
    "minimal_countermodel_available: false",
    "global_no_go_claim_authorized: false",
    "future_source_extension_impossibility_authorized: false",
]


def contains_all(text: str, snippets: list[str]) -> tuple[bool, list[str]]:
    missing = [snippet for snippet in snippets if snippet not in text]
    return not missing, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    role_text = ROLE_PATH.read_text(encoding="utf-8")
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    checks = []

    role_ok, role_missing = contains_all(role_text, ROLE_REQUIRED_SNIPPETS)
    checks.append(
        {
            "check_id": "role_contract_refuter_obstruction_record_guidance",
            "status": "PASS" if role_ok else "FAIL",
            "missing": role_missing,
            "path": str(ROLE_PATH.relative_to(REPO_ROOT)),
        }
    )

    template_ok, template_missing = contains_all(
        template_text, TEMPLATE_REQUIRED_SNIPPETS
    )
    checks.append(
        {
            "check_id": "completion_template_refuter_obstruction_record_shape",
            "status": "PASS" if template_ok else "FAIL",
            "missing": template_missing,
            "path": str(TEMPLATE_PATH.relative_to(REPO_ROOT)),
        }
    )

    field_missing = [
        field for field in REQUIRED_RECORD_FIELDS if field not in template_text
    ]
    checks.append(
        {
            "check_id": "template_contains_required_schema_fields",
            "status": "PASS" if not field_missing else "FAIL",
            "missing": field_missing,
            "schema_path": SCHEMA_PATH,
        }
    )

    vague_blockers = [
        "needs more work",
        "future work remains",
        "generalization was not attempted",
        "insufficient time",
    ]
    role_blocks_vague_pass = all(phrase in role_text for phrase in vague_blockers)
    role_blocks_vague_pass = role_blocks_vague_pass and (
        "not a sufficient failed premise" in role_text
    )
    template_blocks_vague_pass = (
        "vague_failure_language_sufficient_for_pass: false" in template_text
    )
    checks.append(
        {
            "check_id": "vague_failure_language_not_pass_sufficient",
            "status": "PASS"
            if role_blocks_vague_pass and template_blocks_vague_pass
            else "FAIL",
            "role_blocks_vague_pass": role_blocks_vague_pass,
            "template_blocks_vague_pass": template_blocks_vague_pass,
        }
    )

    protected_flags_default_false = all(
        snippet in template_text
        for snippet in [
            "global_no_go_claim_authorized: false",
            "future_source_extension_impossibility_authorized: false",
        ]
    )
    checks.append(
        {
            "check_id": "protected_refuter_conclusion_flags_default_false",
            "status": "PASS" if protected_flags_default_false else "FAIL",
            "global_no_go_default_false": "global_no_go_claim_authorized: false"
            in template_text,
            "future_source_extension_impossibility_default_false": (
                "future_source_extension_impossibility_authorized: false"
                in template_text
            ),
        }
    )

    failed = [check for check in checks if check["status"] != "PASS"]
    report = {
        "status": "PASS" if not failed else "FAIL",
        "task_id": "RT-20260703-011",
        "plan_task_id": "P7-T03",
        "role_path": str(ROLE_PATH.relative_to(REPO_ROOT)),
        "template_path": str(TEMPLATE_PATH.relative_to(REPO_ROOT)),
        "schema_path": SCHEMA_PATH,
        "fixture_catalog_path": CATALOG_PATH,
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "claim_boundary": {
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "source_law_adopted": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "benchmark_promoted": False,
            "global_no_go_claim_authorized": False,
            "future_source_extension_impossibility_authorized": False,
        },
    }

    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"status={report['status']} failed_check_count={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
