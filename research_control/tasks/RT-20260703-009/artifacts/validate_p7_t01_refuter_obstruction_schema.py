#!/usr/bin/env python3
"""Validate v15 P7-T01 Refuter obstruction schema artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control/design/refuter_obstruction_schema_v1.md"

REQUIRED_FIELDS = [
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

REQUIRED_CLAIM_BOUNDARY_TOKENS = [
    "project-control contract",
    "not a physics theorem",
    "not a source-law adoption",
    "not a Gate Chair verdict",
    "not proof authority",
    "global_no_go_claim_authorized: false",
    "future_source_extension_impossibility_authorized: false",
    "No program-wide no-go conclusion follows.",
    "No future source-extension impossibility follows.",
]

REQUIRED_DISTINCTION_TOKENS = [
    "Scoped obstruction",
    "Finite countermodel",
    "Global no-go",
    "Freeze",
    "minimal_countermodel_available: true",
    "countermodel_path",
    "freeze_decision",
    "orbit_avoidance_reason",
]

FORBIDDEN_OVERREAD_TOKENS = [
    "source-law adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "coupling-law adoption",
    "matter-coupling derivation",
    "MetricData(E) adoption",
    "g_eff",
    "Einstein equations",
    "benchmark promotion",
    "Gate Chair verdict",
    "completed derivation",
    "program-wide no-go conclusion",
    "future source-extension impossibility",
]


def make_check(check_id: str, passed: bool, detail: str) -> dict[str, object]:
    return {"id": check_id, "passed": passed, "detail": detail}


def build_report() -> dict[str, object]:
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    checks = [
        make_check(
            "schema_file_exists",
            SCHEMA_PATH.exists(),
            f"Schema path is present: {SCHEMA_PATH.relative_to(REPO_ROOT)}.",
        ),
        make_check(
            "all_required_fields_present",
            all(f"{field}:" in text or f"`{field}`" in text for field in REQUIRED_FIELDS),
            "All P7-T01 required schema field names are present.",
        ),
        make_check(
            "protected_authorization_defaults_false",
            "global_no_go_claim_authorized: false" in text
            and "future_source_extension_impossibility_authorized: false" in text,
            "Global no-go and future-source-extension impossibility flags default to false.",
        ),
        make_check(
            "claim_boundary_tokens_present",
            all(token in text for token in REQUIRED_CLAIM_BOUNDARY_TOKENS),
            "The schema records the support-only project-control boundary and protected overread blocks.",
        ),
        make_check(
            "case_distinctions_present",
            all(token in text for token in REQUIRED_DISTINCTION_TOKENS),
            "The schema distinguishes scoped obstruction, finite countermodel, global no-go, and freeze.",
        ),
        make_check(
            "forbidden_overread_coverage_present",
            all(token in text for token in FORBIDDEN_OVERREAD_TOKENS),
            "Forbidden conclusion coverage includes downstream GR and global-overread blocks.",
        ),
        make_check(
            "next_route_is_p7_t02",
            "P7-T02" in text and "minimal countermodel fixture library" in text,
            "The schema routes the next bounded packet to P7-T02 fixture-library work.",
        ),
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260703-009",
        "schema_path": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "check_count": len(checks),
        "failed_check_count": sum(1 for check in checks if not check["passed"]),
        "checks": checks,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_coupling_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "global_no_go_claim_authorized": False,
            "future_source_extension_impossibility_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Optional JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
