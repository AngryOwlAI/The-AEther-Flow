#!/usr/bin/env python3
"""Validate the bounded P4-T01 matter-coupling DAG schema artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCHEMA_PATH = Path("research_control/design/matter_coupling_dependency_dag_schema_v1.md")

REQUIRED_NODE_KINDS = {
    "evidence_precondition",
    "adopted_object",
    "theorem",
    "law",
    "obstruction",
    "physical_target",
}

REQUIRED_NODE_IDS = {
    "mc_source_matter_semantics_objects",
    "mc_source_matter_semantics_equivalence_theorem",
    "mc_rr_e_certificate_boundary",
    "mc_detector_semantics_target",
    "mc_coupling_law_target",
    "mc_stress_energy_semantics_target",
    "mc_stress_energy_tensor_target",
    "mc_matter_action_target",
    "mc_universal_matter_coupling_derivation",
    "mc_einstein_equation_dependency",
    "mc_benchmark_promotion_dependency",
}

REQUIRED_GUARDS = {
    "no_source_law_adoption",
    "no_RR_ETransportCompletenessOrInvarianceLaw_v1_adoption",
    "no_unrestricted_RR_E_theorem",
    "no_matter_semantics_adoption",
    "no_detector_semantics",
    "no_coupling_law_adoption",
    "no_matter_coupling_derivation",
    "no_matter_coupling_adoption",
    "no_stress_energy_semantics",
    "no_stress_energy_tensor",
    "no_matter_action",
    "no_einstein_equations",
    "no_benchmark_promotion",
    "no_completed_derivation",
}

FORBIDDEN_OVERREAD_TEXT = [
    "not the populated DAG",
    "not a matter-coupling derivation",
    "not a source-law adoption",
    "not detector semantics",
    "not stress-energy semantics",
    "not a matter action",
    "not Einstein equations",
    "not benchmark promotion",
    "not a completed derivation",
]


def build_report() -> dict:
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    checks = []

    def add_check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"id": check_id, "passed": bool(passed), "detail": detail})

    for node_kind in sorted(REQUIRED_NODE_KINDS):
        add_check(
            f"node_kind_{node_kind}",
            f"`{node_kind}`" in text,
            f"Required node kind `{node_kind}` is declared.",
        )

    for node_id in sorted(REQUIRED_NODE_IDS):
        node_present = f"`{node_id}`" in text
        line = next((candidate for candidate in text.splitlines() if f"`{node_id}`" in candidate), "")
        has_guard = "no_" in line and (node_id.startswith("mc_source_") or "blocked" in line or "fail_closed" in line or "human_gated" in line)
        add_check(
            f"required_node_{node_id}",
            node_present and has_guard,
            f"Required node `{node_id}` is present with forbidden-overread guard text.",
        )

    for guard in sorted(REQUIRED_GUARDS):
        add_check(
            f"guard_{guard}",
            guard in text,
            f"Required forbidden-overread guard `{guard}` appears in schema.",
        )

    for phrase in FORBIDDEN_OVERREAD_TEXT:
        add_check(
            f"authority_boundary_{phrase.replace(' ', '_').replace('-', '_')}",
            phrase in text,
            f"Authority boundary phrase `{phrase}` appears in schema.",
        )

    add_check(
        "p4_t02_population_deferred",
        "P4-T02 may populate" in text and "not the populated DAG" in text,
        "Schema explicitly defers DAG population to P4-T02.",
    )

    passed = all(check["passed"] for check in checks)
    return {
        "status": "PASS" if passed else "FAIL",
        "schema_path": str(SCHEMA_PATH),
        "check_count": len(checks),
        "failed_check_count": sum(1 for check in checks if not check["passed"]),
        "checks": checks,
        "claim_boundary": {
            "physics_claim_authority": False,
            "matter_coupling_derived": False,
            "coupling_law_adopted": False,
            "stress_energy_semantics_adopted": False,
            "einstein_equations_derived": False,
            "benchmark_promoted": False,
            "completed_derivation_claimed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
