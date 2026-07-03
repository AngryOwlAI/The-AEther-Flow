#!/usr/bin/env python3
"""Validate v15 P9-T01 Distance-to-GR delta effect enforcement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]

EFFECT_VALUES = [
    "no_distance_delta",
    "scoped_evidence_precondition",
    "scoped_source_only_object",
    "scoped_source_extension_object",
    "conditional_theorem_candidate",
    "obstruction_recorded",
    "frozen_negative",
    "milestone_discharge",
    "protected_gate_pending",
]

TEST_NAMES = [
    "test_p9_future_physics_completion_requires_distance_delta_effect",
    "test_p9_future_physics_completion_rejects_unknown_distance_delta_effect",
    "test_p9_future_physics_completion_accepts_allowed_distance_delta_effect",
    "test_p9_distance_delta_effect_does_not_authorize_downstream_unlock",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def build_report() -> dict[str, Any]:
    validator_text = read_text("scripts/research_control/validate_research_control.py")
    template_text = read_text("research_control/templates/COMPLETION_TEMPLATE.yaml")
    test_text = read_text("tests/test_research_control.py")

    checks = [
        {
            "id": "effect_policy_activation_constant_present",
            "passed": 'DISTANCE_TO_GR_DELTA_EFFECT_ACTIVE_AFTER = "2026-07-03T11:24:00Z"' in validator_text,
            "detail": "Validator declares the P9-T01 prospective activation timestamp.",
        },
        {
            "id": "effect_vocabulary_complete",
            "passed": all(f'"{value}"' in validator_text for value in EFFECT_VALUES),
            "detail": "Validator contains every P9-T01 Distance-to-GR effect value.",
        },
        {
            "id": "future_physics_hook_present",
            "passed": "validate_distance_to_gr_delta_effect(report, job_row, completion, path_text)" in validator_text
            and "def validate_distance_to_gr_delta_effect(" in validator_text,
            "detail": "Future physics completion validation calls the Distance-to-GR effect validator.",
        },
        {
            "id": "missing_and_invalid_effects_hard_fail",
            "passed": "future physics completion missing distance_to_gr_delta.effect" in validator_text
            and "distance_to_gr_delta.effect is not allowed" in validator_text,
            "detail": "Validator hard-fails missing and unsupported effect values.",
        },
        {
            "id": "effect_does_not_authorize_downstream_unlock",
            "passed": "distance_to_gr_delta.effect does not authorize" in validator_text
            and "UNAUTHORIZED_DOWNSTREAM_GR_UNLOCKS" in validator_text,
            "detail": "Effect labels cannot unlock downstream GR objects without human-gated promotion authority.",
        },
        {
            "id": "completion_template_exposes_effect_field",
            "passed": 'distance_to_gr_delta:\n  effect: "no_distance_delta"' in template_text,
            "detail": "Completion template now asks completions to state the actual effect field.",
        },
        {
            "id": "focused_tests_present",
            "passed": all(name in test_text for name in TEST_NAMES),
            "detail": "Focused tests cover missing, invalid, allowed, and no-promotion cases.",
        },
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260703-014",
        "plan_task_id": "P9-T01",
        "checks": checks,
        "effect_values": EFFECT_VALUES,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_coupling_authorized": False,
            "stress_energy_authorized": False,
            "matter_action_authorized": False,
            "variation_principle_authorized": False,
            "einstein_equations_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "proof_authority": False,
        },
    }


def write_receipt(report: dict[str, Any]) -> None:
    if report["status"] != "PASS":
        return
    receipt_path = (
        REPO_ROOT
        / "research_control/tasks/RT-20260703-014/artifacts/p9_t01_distance_to_gr_delta_enforcement_receipt.md"
    )
    receipt_path.write_text(
        "\n".join(
            [
                "<!-- authority: control -->",
                "",
                "# P9-T01 Distance-To-GR Delta Enforcement Receipt",
                "",
                "## Status",
                "",
                "PASS.",
                "",
                "## Scope",
                "",
                "This receipt validates future-physics completion enforcement for `distance_to_gr_delta.effect`. It does not authorize source-law adoption, matter semantics, detector semantics, coupling-law adoption, matter coupling, stress-energy semantics, a stress-energy tensor, a matter action, a variation principle, Einstein equations, benchmark promotion, or completed derivation.",
                "",
                "## Enforced Effect Values",
                "",
                *[f"- `{value}`" for value in EFFECT_VALUES],
                "",
                "## No-Promotion Boundary",
                "",
                "The effect field is a reporting classification only. The validator separately rejects downstream GR unlocks unless human-gated physics promotion authority is present.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_receipt(report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
