#!/usr/bin/env python3
"""Validate the bounded continue-research-goal.v4 reasoning-effort contract."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260718-013"
POLICY = TASK_DIR / "artifacts/continue_research_goal_v4_reasoning_effort_policy.md"
REPORT = TASK_DIR / "artifacts/continue_research_goal_v4_policy_validation.json"
HELPER = ROOT / ".codex/skills/continue-research-goal/scripts/goal_state.py"
LAUNCHER = ROOT / ".codex/skills/continue-research-goal/SKILL.md"
WORKER = ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md"
SCHEMA = ROOT / ".codex/skills/continue-research-goal/references/goal-file-schema.md"
TESTS = ROOT / "tests/test_continue_research_goal_state.py"
V3_TASK = ROOT / "research_control/tasks/RT-20260718-012"

EXPECTED_REASONING_EFFORTS = {
    "none",
    "minimal",
    "low",
    "medium",
    "high",
    "xhigh",
    "max",
    "ultra",
}
EXPECTED_V3_TREE_SHA256 = "4a70356a7fbb89e32847fdaae111ad7a8ae33c1eb235f311c996070334baf526"
EXPECTED_V3_ARTIFACTS = {
    "artifacts/v20_goal_relay_execution_policy.md":
        "18c4cfe125883dc84da84156e0337a58720eab9c9c471d635fb5b01fc739e858",
    "artifacts/v20_goal_relay_scenarios.json":
        "73ebd5d03153a309533364de822c453de5fe06f06bb5735ca9930d1040446c65",
    "artifacts/v20_goal_relay_policy_validation.json":
        "dc08b90b0f13b04cfe572e1d52d88d70214126eff128b6b9e02ca2f14ef5ccd2",
    "artifacts/validate_v20_goal_relay_policy.py":
        "e6bec75ae452e108109b95d63d74d4635aab8cd7c26b705d2f60062765263296",
    "jobs/completions/AJC-AJ-RT-20260718-012-001.yaml":
        "82f772d5d02517150e24457b8d281adb635c53ebba7905268dac27a93e3933f6",
}
EXPECTED_PRESERVED_FILES = {
    "research_control/program_state.yaml":
        "1a28fc71d3076347be4221e4d30b4bf962e5f752fd9d90f099d916dd89a4706c",
    "research_control/handoffs/handoff-0740.yaml":
        "5be1f16f476c1f03db0baf3dcfec8ffc1947ff61c5d5d3ff43012239ce5c0c1d",
    "research_control/handoffs/handoff-0740.md":
        "2d2bb5936181f7040357c1074c06e124904b28cd84fdb6b3138be59055d02402",
}

LAUNCHER_TOKENS = {
    'reasoning_effort: "<value>"',
    "Omission of `reasoning_effort` selects `max`",
    "edits only the goal, preserve the previously selected",
    "edits only the effort, preserve the goal",
    "edits both simultaneously, replace both candidates",
    "ambiguous approval",
    "create no state",
    'nodeRepl.requestMeta["x-codex-turn-metadata"]',
    "current-task `reasoning_effort` exactly equals",
    "change the Codex UI reasoning setting",
    "create_thread(..., thinking=<persisted discussion_contract reasoning_effort>)",
    "omit the `model` argument",
    "rely on default inheritance",
    "silently downgrade",
}
WORKER_TOKENS = {
    'nodeRepl.requestMeta["x-codex-turn-metadata"]',
    "stops before generation claim",
    "rediscover the exact saved project and current `create_thread` contract",
    "before successor reservation",
    "create_thread(..., thinking=<persisted discussion_contract reasoning_effort>)",
    "omit the `model` argument",
    "inherit a default reasoning effort",
    "silently downgrade",
}
TEST_TOKENS = {
    "test_v4_default_effort_contract_and_omitted_scheduling_guards",
    "test_alternate_reasoning_effort_serializes_and_summarizes",
    "test_unsupported_reasoning_effort_is_rejected_without_state",
    "test_v3_record_is_validation_and_summary_only_without_migration",
    "test_rehashed_discussion_tamper_is_rejected_by_initialization_evidence",
    "test_launcher_acceptance_loop_covers_defaults_edits_and_ambiguous_approval",
    "test_launcher_metadata_mismatch_stops_before_initialization",
    "test_both_relay_skills_pin_thinking_and_omit_model",
    "test_recursive_effort_checks_precede_claim_and_successor_reservation",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(item).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_helper() -> Any:
    spec = importlib.util.spec_from_file_location("goal_state_v4_policy_validation", HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load goal_state helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_tokens(errors: list[str], label: str, text: str, tokens: set[str]) -> None:
    for token in sorted(tokens):
        if token not in text:
            errors.append(f"{label} missing token: {token}")


def validate() -> dict[str, Any]:
    errors: list[str] = []
    helper = load_helper()
    helper_text = HELPER.read_text(encoding="utf-8")
    launcher_text = LAUNCHER.read_text(encoding="utf-8")
    worker_text = WORKER.read_text(encoding="utf-8")
    schema_text = SCHEMA.read_text(encoding="utf-8")
    tests_text = TESTS.read_text(encoding="utf-8")
    policy_text = POLICY.read_text(encoding="utf-8")

    if helper.SCHEMA_VERSION != "continue-research-goal.v4":
        errors.append("current helper schema is not v4")
    expected_retained = {
        "continue-research-goal.v1",
        "continue-research-goal.v2",
        "continue-research-goal.v3",
    }
    if helper.RETAINED_SCHEMA_VERSIONS != expected_retained:
        errors.append("retained schema set is not exactly v1-v3")
    if helper.SUPPORTED_SCHEMA_VERSIONS != expected_retained | {helper.SCHEMA_VERSION}:
        errors.append("supported schema set does not preserve exactly v1-v4")
    if helper.REASONING_EFFORTS != EXPECTED_REASONING_EFFORTS:
        errors.append("reasoning effort enum differs from the task-tool contract")
    if (
        helper.DISCUSSION_CONFIRMATION_MARKER
        != "combined_goal_and_reasoning_effort_confirmed"
    ):
        errors.append("discussion confirmation marker changed")

    goal_hash = "a" * 64
    contract = helper.build_discussion_contract(
        accepted_goal_sha256=goal_hash,
        reasoning_effort="max",
    )
    try:
        helper.validate_discussion_contract(contract, goal_sha256=goal_hash)
    except helper.ValidationError as exc:
        errors.append(f"valid max discussion contract rejected: {exc}")
    if contract.get("reasoning_effort") != "max":
        errors.append("default policy effort is not representable as max")
    tampered = dict(contract)
    tampered["accepted_goal_sha256"] = "b" * 64
    try:
        helper.validate_discussion_contract(tampered, goal_sha256=goal_hash)
    except helper.ValidationError:
        pass
    else:
        errors.append("goal-mismatched discussion contract was accepted")

    require_tokens(errors, "launcher", launcher_text, LAUNCHER_TOKENS)
    require_tokens(errors, "worker", worker_text, WORKER_TOKENS)
    require_tokens(errors, "focused tests", tests_text, TEST_TOKENS)
    require_tokens(
        errors,
        "schema",
        schema_text,
        {
            "# Continue-Research Goal Record Schema v4",
            "Immutable Discussion Contract",
            "`--scope-contract-json`, `--reasoning-effort`",
            "retained v1-v3",
        },
    )
    require_tokens(
        errors,
        "policy",
        policy_text,
        {
            "Combined pre-launch acceptance",
            "Current-task verification",
            "Immutable discussion contract",
            "Recursive task pinning",
            "Compatibility and failure behavior",
            "Distance-to-GR",
        },
    )
    require_tokens(
        errors,
        "helper",
        helper_text,
        {
            'SCHEMA_VERSION = "continue-research-goal.v4"',
            "def validate_reasoning_effort(",
            "def validate_discussion_contract(",
            '"discussion_contract_sha256": record["discussion_contract_sha256"]',
            '"--reasoning-effort"',
        },
    )

    metadata_token = 'nodeRepl.requestMeta["x-codex-turn-metadata"]'
    initialize_token = "call helper `initialize` exactly once"
    if launcher_text.index(metadata_token) >= launcher_text.index(initialize_token):
        errors.append("launcher metadata verification does not precede initialization")
    claim_token = "Call helper `claim` exactly once"
    if worker_text.index(metadata_token) >= worker_text.index(claim_token):
        errors.append("worker metadata verification does not precede claim")
    rediscover_token = (
        "rediscover the exact saved project and current `create_thread` contract"
    )
    reserve_token = "call helper `reserve-successor` once"
    if worker_text.index(rediscover_token) >= worker_text.index(reserve_token):
        errors.append("create_thread rediscovery does not precede successor reservation")

    v3_tree_hash = tree_sha256(V3_TASK)
    if v3_tree_hash != EXPECTED_V3_TREE_SHA256:
        errors.append("completed RT-20260718-012 task tree changed")
    v3_artifact_hashes: dict[str, str] = {}
    for relative, expected in EXPECTED_V3_ARTIFACTS.items():
        actual = sha256_file(V3_TASK / relative)
        v3_artifact_hashes[relative] = actual
        if actual != expected:
            errors.append(f"completed v3 artifact changed: {relative}")

    preserved_hashes: dict[str, str] = {}
    for relative, expected in EXPECTED_PRESERVED_FILES.items():
        actual = sha256_file(ROOT / relative)
        preserved_hashes[relative] = actual
        if actual != expected:
            errors.append(f"preserved research-control file changed: {relative}")

    source_paths = [POLICY, HELPER, LAUNCHER, WORKER, SCHEMA, TESTS]
    source_hashes = {
        path.relative_to(ROOT).as_posix(): sha256_file(path)
        for path in source_paths
    }
    checks = {
        "v4_schema_and_v1_v3_retention": helper.SCHEMA_VERSION
        == "continue-research-goal.v4"
        and helper.RETAINED_SCHEMA_VERSIONS == expected_retained,
        "reasoning_enum_and_contract": helper.REASONING_EFFORTS
        == EXPECTED_REASONING_EFFORTS,
        "combined_acceptance_static_contract": all(
            token in launcher_text for token in LAUNCHER_TOKENS
        ),
        "worker_pinning_static_contract": all(
            token in worker_text for token in WORKER_TOKENS
        ),
        "focused_coverage_contract": all(token in tests_text for token in TEST_TOKENS),
        "completed_v3_tree_unchanged": v3_tree_hash == EXPECTED_V3_TREE_SHA256,
        "preserved_research_control_unchanged": all(
            preserved_hashes[path] == expected
            for path, expected in EXPECTED_PRESERVED_FILES.items()
        ),
    }
    report = {
        "schema_version": "continue-research-goal-v4-policy-validation.v1",
        "task_id": "RT-20260718-013",
        "status": "PASS" if not errors else "FAIL",
        "runtime_schema": helper.SCHEMA_VERSION,
        "retained_schema_versions": sorted(helper.RETAINED_SCHEMA_VERSIONS),
        "reasoning_efforts": sorted(helper.REASONING_EFFORTS),
        "discussion_confirmation_marker": helper.DISCUSSION_CONFIRMATION_MARKER,
        "checks": checks,
        "check_count": len(checks),
        "source_hashes": source_hashes,
        "completed_v3_tree_sha256": v3_tree_hash,
        "completed_v3_artifact_hashes": v3_artifact_hashes,
        "preserved_research_control_hashes": preserved_hashes,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "errors": errors,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.json:
        print(rendered, end="")
    else:
        print(f"{report['status']}: {report['check_count']} v4 policy checks")
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
