#!/usr/bin/env python3
"""Validate the bounded P11-T01 CI shard design without executing CI shards."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.project_control.classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.plan import load_manifest  # noqa: E402
from scripts.validation.profiles import build_membership_audit, resolve_profile  # noqa: E402


MANIFEST_PATH = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
POLICY_PATH = REPO_ROOT / "research_control/design/ci_validation_shard_policy_v1.md"
WORKFLOW_PATH = REPO_ROOT / ".github/workflows/project-control-validation.yml"
ARTIFACT_DIR = REPO_ROOT / "research_control/tasks/RT-20260718-003/artifacts"
COVERAGE_PATH = ARTIFACT_DIR / "ci_shard_coverage_report.json"
SCENARIOS_PATH = ARTIFACT_DIR / "ci_shard_plan_scenarios.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_workflow() -> dict[str, object]:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    require(yaml.compose(text) is not None, "workflow YAML did not produce a document")
    for fragment in (
        "validation_plan_shadow:",
        "continue-on-error: true",
        "fetch-depth: 0",
        "scripts.validation.cli plan",
        "--profile affected",
        "actions/upload-artifact@v4",
        "validate_project_control:",
        "validate_memory_read_only:",
        "cancel-in-progress: true",
        "timeout-minutes: 45",
        "timeout-minutes: 20",
    ):
        require(fragment in text, f"workflow missing required fragment: {fragment}")
    for deferred_job in (
        "policy_fast:",
        "research_control_integration:",
        "dependency_graph:",
        "memory_core:",
        "publication:",
        "scientific_support:",
        "local_retrieval:",
        "orchestration_equivalence:",
    ):
        require(deferred_job not in text, f"P11-T02 job implemented early: {deferred_job}")
    return {
        "syntax": "PASS",
        "shadow_job_present": True,
        "legacy_jobs_preserved": True,
        "execution_shards_absent": True,
    }


def validate_ownership(manifest: dict[str, object]) -> dict[str, object]:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    gates = manifest["gates"]
    require(isinstance(gates, list), "manifest gates must be an array")
    gate_ids = {str(gate["gate_id"]) for gate in gates}
    owners = coverage["primary_owners"]
    require(isinstance(owners, dict), "primary_owners must be an object")
    flattened = [
        str(gate_id)
        for owner_gate_ids in owners.values()
        for gate_id in owner_gate_ids
    ]
    counts = Counter(flattened)
    duplicate = sorted(gate_id for gate_id, count in counts.items() if count != 1)
    missing = sorted(gate_ids - set(flattened))
    unknown = sorted(set(flattened) - gate_ids)
    require(not duplicate, f"duplicate primary ownership: {duplicate}")
    require(not missing, f"missing primary ownership: {missing}")
    require(not unknown, f"unknown primary ownership: {unknown}")
    require(len(flattened) == 37 == len(gate_ids), "expected 37 exactly owned gates")
    test_shards = [str(gate["test_shard"]) for gate in gates]
    require(
        set(test_shards)
        == {"tests/fixtures/validation_manifest/legacy_gate_coverage_v1.json"},
        "live manifest test_shard inventory changed",
    )
    require(
        coverage["test_shard_contract"]["hidden_command_lists_allowed"] is False,
        "hidden command lists must remain forbidden",
    )
    return {
        "manifest_gate_count": len(gate_ids),
        "owned_gate_count": len(flattened),
        "missing_gate_ids": missing,
        "duplicate_primary_owner_gate_ids": duplicate,
        "unknown_gate_ids": unknown,
        "manifest_test_shard_count": len(test_shards),
    }


def validate_profiles(manifest: dict[str, object]) -> dict[str, object]:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    audit = build_membership_audit(manifest)
    full = audit["representative_scenarios"]["repository_full"]
    expected = coverage["full_profile"]["selected_gate_ids"]
    require(full["selected_gate_ids"] == expected, "full-profile union drifted")
    shadow = audit["affected_blocking_shadow_comparison"]
    require(shadow["status"] == "PASS", "legacy/planner shadow comparison failed")
    require(
        shadow["unexplained_mismatch_gate_ids"] == [],
        "legacy/planner shadow comparison has unexplained mismatch",
    )
    require(
        audit["full_nontransactional_blocking_missing_gate_ids"] == [],
        "full profile omits a nontransactional blocking gate",
    )
    return {
        "full_selected_gate_count": len(full["selected_gate_ids"]),
        "full_nontransactional_blocking_missing_gate_ids": [],
        "legacy_planner_shadow_status": shadow["status"],
        "unexplained_mismatch_gate_ids": [],
    }


def validate_scenarios(manifest: dict[str, object]) -> dict[str, object]:
    fixture = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    checked: list[str] = []
    for name, expected in fixture["scenarios"].items():
        classification = classify_paths(expected["paths"])
        resolution = resolve_profile(
            manifest,
            classification,
            requested_profile=expected["requested_profile"],
            scopes=expected.get("scopes", []),
            shadow=True,
        )
        plan = resolution.plan.to_dict()
        require(plan["schema_id"] == "validation_plan_v1", f"{name}: wrong plan schema")
        require(plan["status"] == expected["status"], f"{name}: status drift")
        require(
            plan["effective_profile"] == expected["effective_profile"],
            f"{name}: effective profile drift",
        )
        require(
            plan["selected_gate_ids"] == expected["selected_gate_ids"],
            f"{name}: selected gate drift",
        )
        require(plan["unknown_paths"] == expected["unknown_paths"], f"{name}: unknown drift")
        require(plan["planner_executes_commands"] is False, f"{name}: planner executed")
        require(
            plan["authority"]["physics_claim_authority"] is False,
            f"{name}: invalid physics authority",
        )
        checked.append(name)
    return {"scenario_count": len(checked), "checked_scenarios": sorted(checked)}


def validate_policy(manifest: dict[str, object]) -> dict[str, object]:
    text = POLICY_PATH.read_text(encoding="utf-8")
    gates = manifest["gates"]
    for gate in gates:
        gate_id = str(gate["gate_id"])
        require(gate_id in text, f"policy omits live gate: {gate_id}")
    for shard in (
        "validation-plan",
        "policy-fast",
        "research-control-integration",
        "dependency-graph",
        "memory-core",
        "publication",
        "scientific-support",
        "local-retrieval",
        "orchestration-equivalence",
        "scheduled-full",
    ):
        require(shard in text, f"policy omits topology shard: {shard}")
    for boundary in (
        "continue-on-error: true",
        "SKIP_NOT_APPLICABLE",
        "cancel-in-progress: true",
        "branch-protection",
        "legacy",
        "P11-T02",
    ):
        require(boundary in text, f"policy omits boundary: {boundary}")
    return {"gate_mentions": len(gates), "topology_job_count": 10}


def main() -> int:
    try:
        manifest = load_manifest(MANIFEST_PATH)
        result = {
            "schema_id": "v19_ci_shard_design_validator_result_v1",
            "status": "PASS",
            "workflow": validate_workflow(),
            "ownership": validate_ownership(manifest),
            "profiles": validate_profiles(manifest),
            "scenarios": validate_scenarios(manifest),
            "policy": validate_policy(manifest),
            "authority": {
                "operational_validation_only": True,
                "legacy_ci_authoritative": True,
                "execution_shards_implemented": False,
                "physics_claim_authority": False,
                "proof_authority": False,
            },
        }
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
