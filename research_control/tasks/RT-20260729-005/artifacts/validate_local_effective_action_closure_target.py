#!/usr/bin/env python3
"""Validate the bounded v21 P8-T02 local effective-action closure target."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "local_effective_action_closure_target_validation_v1.json"

TARGET_PATH = ARTIFACT_DIR / "local_effective_action_closure_target_v1.tex"
ENVELOPE_PATH = ARTIFACT_DIR / "local_effective_action_assumption_envelope_v1.yaml"
SHORTCUTS_PATH = ARTIFACT_DIR / "local_effective_action_forbidden_shortcuts_v1.yaml"
MATH_CHILD_PATH = ARTIFACT_DIR / "child_phys_math_p8_t02_local_effective_action_closure_target.yaml"
PHIL_CHILD_PATH = ARTIFACT_DIR / "child_phys_phil_p8_t02_local_effective_action_closure_target.yaml"
REVIEW_PATH = ARTIFACT_DIR / "parent_conflict_review_p8_t02_local_effective_action_closure_target.yaml"
FUSION_PATH = ARTIFACT_DIR / "parent_fusion_notes_p8_t02_local_effective_action_closure_target.md"
RECEIPT_PATH = ARTIFACT_DIR / "local_effective_action_closure_target_receipt.md"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex":
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260726-001/artifacts/p6_geometry_input_contract_v1.yaml":
        "7b0eee4ea249a3acf99d38d312bd14619dedea79977d7b802062e9410f5b8557",
    "research_control/tasks/RT-20260726-011/artifacts/metric_object_naming_decision_v1.yaml":
        "4d67563b2444cfed2bd430e9d027337f26656701624d532f7cb2e357cbac2452",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml":
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml":
        "e11f5e4ae886932cad618caa3ee97e973bbd38d363db25776fe1fbd2c27451dc",
    "research_control/tasks/RT-20260729-003/artifacts/gravitational_closure_route_decision_v1.yaml":
        "49af80465727038a7022371bac9dbe8fc4442b01a37fe14e9442873b1d8fa82f",
    "research_control/tasks/RT-20260729-003/artifacts/gravitational_closure_hypothesis_comparison_v1.yaml":
        "c337169583c60d1e4889e820ac0388c17ead67b190875268788805dae72b63d2",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_consistency.tex":
        "d965519639ee8764a5c5a63798d15e8a9a380d7e208dffc43a0be02b6f245ba1",
}

REQUIRED_ASSUMPTIONS = {f"A{index}" for index in range(10)}
FORBIDDEN_TARGET_TERM_VARIANTS = {
    "target atlas": ("target atlas",),
    "target metric": ("target metric",),
    "Einstein-Hilbert action": (
        "Einstein-Hilbert action",
        "Einstein--Hilbert action",
        "Einstein\u2013Hilbert action",
    ),
    "Einstein equations": ("Einstein equations",),
    "benchmark success": ("benchmark success",),
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

    required_paths = [
        TARGET_PATH,
        ENVELOPE_PATH,
        SHORTCUTS_PATH,
        MATH_CHILD_PATH,
        PHIL_CHILD_PATH,
        REVIEW_PATH,
        FUSION_PATH,
        RECEIPT_PATH,
    ]
    for artifact_path in required_paths:
        check(
            f"exists:{artifact_path.name}",
            artifact_path.is_file(),
            str(artifact_path.relative_to(ROOT)),
        )

    try:
        envelope = load_yaml(ENVELOPE_PATH)
        shortcuts = load_yaml(SHORTCUTS_PATH)
        math_child = load_yaml(MATH_CHILD_PATH)
        phil_child = load_yaml(PHIL_CHILD_PATH)
        review = load_yaml(REVIEW_PATH)
    except Exception as exc:
        check("yaml_load", False, str(exc))
        envelope = shortcuts = math_child = phil_child = review = {}
    else:
        check("yaml_load", True, "All five YAML artifacts parsed.")

    assumptions = envelope.get("assumptions", [])
    assumption_ids = {
        item.get("assumption_id")
        for item in assumptions
        if isinstance(item, dict)
    }
    assumption_statuses = [
        item.get("overall_status")
        for item in assumptions
        if isinstance(item, dict)
    ]
    check("assumption_set", assumption_ids == REQUIRED_ASSUMPTIONS, ",".join(sorted(str(value) for value in assumption_ids)))
    check("assumption_count", len(assumptions) == 10, str(len(assumptions)))
    check("satisfied_guard_count", assumption_statuses.count("satisfied_as_provenance_guard") == 1, str(assumption_statuses.count("satisfied_as_provenance_guard")))
    check("partial_count", assumption_statuses.count("partial_but_missing_bridge") == 2, str(assumption_statuses.count("partial_but_missing_bridge")))
    check("missing_count", assumption_statuses.count("missing") == 7, str(assumption_statuses.count("missing")))

    typed_objects = envelope.get("typed_objects", {})
    expected_typed_objects = {
        "source_datum",
        "effective_site",
        "locality_cover",
        "measure",
        "gravitational_carrier",
        "matter_carrier",
        "configuration_space",
        "source_to_gravity_map",
        "source_to_matter_map",
        "symmetry",
        "response_operator",
        "boundary_data",
        "inverse_variational_data",
        "correction_remainder",
    }
    check("typed_object_set", set(typed_objects) == expected_typed_objects, ",".join(sorted(typed_objects)))

    result = envelope.get("result", {})
    check("target_formalized", result.get("target_formalized") is True, str(result.get("target_formalized")))
    check("all_symbols_typed", result.get("all_symbols_typed") is True, str(result.get("all_symbols_typed")))
    check("next_plan_task", result.get("next_plan_task_id") == "P8-T03", str(result.get("next_plan_task_id")))
    check("next_role", result.get("next_role_family") == "candidate-constructor@0.2.0", str(result.get("next_role_family")))

    limits = envelope.get("authority_limits", {})
    barred_true_flags = [
        "canonical_ontology_modified",
        "source_law_adopted",
        "source_law_rejected",
        "theorem_truth_inferred",
        "local_effective_action_constructed",
        "target_metric_assumed",
        "Einstein_Hilbert_action_assumed",
        "Einstein_equations_assumed",
        "benchmark_success_assumed",
        "physics_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
    ]
    check("authority_flags_false", all(limits.get(flag) is False for flag in barred_true_flags), ",".join(barred_true_flags))

    shortcut_items = shortcuts.get("shortcuts", [])
    check("shortcut_count", len(shortcut_items) == 12, str(len(shortcut_items)))
    check(
        "all_shortcuts_fail_closed",
        all(str(item.get("failure_status", "")).startswith("fail_closed") for item in shortcut_items if isinstance(item, dict)),
        ",".join(str(item.get("failure_status")) for item in shortcut_items if isinstance(item, dict)),
    )

    check("math_child_complete", math_child.get("status") == "completed", str(math_child.get("status")))
    check("phil_child_complete", phil_child.get("status") == "completed", str(phil_child.get("status")))
    check("parent_conflicts_resolved", review.get("status") == "resolved" and review.get("unresolved_conflicts") == [], json.dumps(review.get("unresolved_conflicts")))
    check("no_child_agentjobs", review.get("fusion_result", {}).get("child_agentjob_count") == 0, str(review.get("fusion_result", {}).get("child_agentjob_count")))
    check("no_child_subagents", review.get("fusion_result", {}).get("child_subagent_count") == 0, str(review.get("fusion_result", {}).get("child_subagent_count")))

    target_text = TARGET_PATH.read_text(encoding="utf-8") if TARGET_PATH.is_file() else ""
    receipt_text = RECEIPT_PATH.read_text(encoding="utf-8") if RECEIPT_PATH.is_file() else ""
    combined_text = target_text + "\n" + receipt_text
    for term, variants in FORBIDDEN_TARGET_TERM_VARIANTS.items():
        check(
            f"forbidden_premise_named:{term}",
            any(variant in combined_text for variant in variants),
            term,
        )
    check("inverse_variational_burden", "Helmholtz" in target_text and "Global gluing" in target_text, "Local and global variational burdens are explicit.")
    check(
        "current_non_derivation",
        "does not presently derive" in target_text
        and "not a theorem that no such extension" in target_text,
        "Scoped non-derivation language is present.",
    )
    check("obstruction_identity", "OBST-P8T02-LOCAL-EFFECTIVE-ACTION-CLOSURE-DATA-ABSENT-001" in combined_text, "Exact obstruction identity is present.")
    check("no_distance_delta", "remains `not_started`" in receipt_text, "Einstein-equations burden remains not started.")

    for relative_path, expected_hash in SOURCE_HASHES.items():
        source_path = ROOT / relative_path
        actual_hash = sha256(source_path) if source_path.is_file() else ""
        check(f"source_hash:{relative_path}", actual_hash == expected_hash, actual_hash)

    failures = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "local_effective_action_closure_target_validation_v1",
        "task_id": "RT-20260729-005",
        "plan_task_id": "P8-T02",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "target_id": "LocalEffectiveActionClosureTarget_v1",
        "obstruction_id": "OBST-P8T02-LOCAL-EFFECTIVE-ACTION-CLOSURE-DATA-ABSENT-001",
        "next_plan_task_id": "P8-T03",
        "distance_to_gr_changed": False,
        "checks": checks,
    }

    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.json or not args.check:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
