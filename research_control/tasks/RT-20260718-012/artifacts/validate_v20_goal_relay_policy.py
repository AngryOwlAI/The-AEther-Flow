#!/usr/bin/env python3
"""Validate the governed v20 P0-T03 autonomous goal-relay contract."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260718-012"
POLICY = TASK_DIR / "artifacts/v20_goal_relay_execution_policy.md"
SCENARIOS = TASK_DIR / "artifacts/v20_goal_relay_scenarios.json"
REPORT = TASK_DIR / "artifacts/v20_goal_relay_policy_validation.json"
BACKLOG = ROOT / "research_control/tasks/RT-20260718-011/artifacts/v20_recommendation_backlog.yaml"
P0_T02_DIR = ROOT / "research_control/tasks/RT-20260718-011"
HELPER = ROOT / ".codex/skills/continue-research-goal/scripts/goal_state.py"

EXPECTED_SCENARIOS = {
    "S01_MULTI_STEP_INCLUDED_TASKS",
    "S02_SINGLE_OBJECTIVE_SCOPE_PROTECTION",
    "S03_RESEARCH_REPAIR_RESUME",
    "S04_HUMAN_GATE_WITH_INDEPENDENT_WORK",
    "S05_STRATEGY_SWITCH_ON_REPEAT",
    "S06_STRATEGY_EXHAUSTION",
    "S07_EXPLICIT_GUARD_STOP",
    "S08_DIRTY_MANIFEST_MISMATCH",
    "S09_ZERO_CHILD_DISPATCH",
    "S10_ONE_CHILD_DISPATCH_ADOPTION",
    "S11_AMBIGUOUS_OR_DUPLICATE_DISPATCH",
    "S12_DUPLICATE_WORKER_OR_LEASE",
    "S13_UNCERTAIN_CONSUMED_INVOCATION",
    "S14_DETERMINISTIC_SUCCESS_REPORT",
    "S15_V1_V2_HISTORICAL_VALIDATION",
}

POLICY_TOKENS = {
    "continue-research-goal.v3",
    "single_objective",
    "multi_step",
    "recovery_required",
    "improve-project-system",
    "(blocker_fingerprint, strategy_id)",
    "Goal reached.",
    "That goal was reached.",
    "Goal not reached — human action required",
    "cross_task_relay_reuse: false",
    "worker prose is telemetry",
}

HELPER_TOKENS = {
    'SCHEMA_VERSION = "continue-research-goal.v3"',
    'RETAINED_SCHEMA_VERSION = "continue-research-goal.v2"',
    '"recovery_required"',
    "def record_recovery_required(",
    "def reconcile_dispatch(",
    "def summarize(",
    '"improve-project-system"',
    "--scope-contract-json",
    "--human-intervention-json",
}

TEST_TOKENS = {
    "test_explicit_multi_step_scope_crosses_included_task_boundary_and_summarizes",
    "test_single_objective_scope_rejects_unlisted_next_task",
    "test_research_to_project_system_repair_to_resumed_research_counts_every_frame",
    "test_human_gated_item_is_deferred_while_independent_scope_continues",
    "test_repeated_fingerprint_switches_distinct_strategies_then_stops_with_exact_human_action",
    "test_dispatch_reconciliation_retries_only_after_zero_children_or_adopts_one",
    "test_guard_deadline_and_pass_limit_stop_before_second_consumption",
    "test_scope_contract_hash_and_route_hash_fail_closed",
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
    spec = importlib.util.spec_from_file_location("goal_state_v3_policy_validation", HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load goal_state helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate() -> dict[str, Any]:
    errors: list[str] = []
    policy_text = POLICY.read_text(encoding="utf-8")
    helper_text = HELPER.read_text(encoding="utf-8")
    tests_path = ROOT / "tests/test_continue_research_goal_state.py"
    tests_text = tests_path.read_text(encoding="utf-8")
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    helper = load_helper()

    if data.get("schema_version") != "v20-goal-relay-scenarios.v3":
        fail(errors, "scenario schema_version must be v20-goal-relay-scenarios.v3")
    if data.get("runtime_schema") != helper.SCHEMA_VERSION:
        fail(errors, "scenario runtime_schema does not match helper SCHEMA_VERSION")
    if helper.RETAINED_SCHEMA_VERSION != "continue-research-goal.v2":
        fail(errors, "helper retained schema version changed")
    if helper.LEGACY_SCHEMA_VERSION != "continue-research-goal.v1":
        fail(errors, "helper legacy schema version changed")
    if helper.WORKER_SKILLS != {"continue-research", "improve-project-system"}:
        fail(errors, "worker skill allowlist is not the v3 contract")
    if helper.SCOPE_MODES != {"single_objective", "multi_step"}:
        fail(errors, "scope mode allowlist is not the v3 contract")
    if "recovery_required" not in helper.NONTERMINAL_PHASES:
        fail(errors, "recovery_required is not nonterminal")

    for token in sorted(POLICY_TOKENS):
        if token.lower() not in policy_text.lower():
            fail(errors, f"policy missing token: {token}")
    for token in sorted(HELPER_TOKENS):
        if token not in helper_text:
            fail(errors, f"helper missing token: {token}")
    for token in sorted(TEST_TOKENS):
        if token not in tests_text:
            fail(errors, f"focused tests missing coverage token: {token}")

    recorded_hashes = data.get("source_hashes", {})
    actual_hashes: dict[str, str] = {}
    for relative, expected_hash in recorded_hashes.items():
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"source hash path missing: {relative}")
            continue
        actual_hash = sha256_file(path)
        actual_hashes[relative] = actual_hash
        if actual_hash != expected_hash:
            fail(errors, f"source hash mismatch: {relative}")

    p0_t02_hash = tree_sha256(P0_T02_DIR)
    if p0_t02_hash != data.get("historical_p0_t02_tree_sha256"):
        fail(errors, "completed P0-T02 tree changed")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list):
        fail(errors, "scenarios must be a list")
        scenarios = []
    ids = [item.get("scenario_id") for item in scenarios if isinstance(item, dict)]
    if set(ids) != EXPECTED_SCENARIOS or len(ids) != len(set(ids)):
        fail(errors, "scenario IDs are missing, duplicated, or unexpected")

    legal_phases = helper.NONTERMINAL_PHASES | helper.TERMINAL_PHASES
    terminal_count = 0
    recursive_count = 0
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            fail(errors, "scenario entry must be an object")
            continue
        if scenario.get("scope_mode") not in helper.SCOPE_MODES:
            fail(errors, f"{scenario.get('scenario_id')}: invalid scope_mode")
        route_skills = scenario.get("route_skills")
        if not isinstance(route_skills, list) or any(skill not in helper.WORKER_SKILLS for skill in route_skills):
            fail(errors, f"{scenario.get('scenario_id')}: invalid route_skills")
        phases = scenario.get("expected_phases")
        if not isinstance(phases, list) or not phases:
            fail(errors, f"{scenario.get('scenario_id')}: expected_phases must be nonempty")
            continue
        unknown = sorted(set(phases) - legal_phases)
        if unknown:
            fail(errors, f"{scenario.get('scenario_id')}: illegal phases {unknown}")
        if phases[-1] in helper.TERMINAL_PHASES:
            terminal_count += 1
        else:
            recursive_count += 1
        if scenario.get("must_continue") and phases[-1] in helper.TERMINAL_PHASES:
            fail(errors, f"{scenario.get('scenario_id')}: must_continue maps to terminal phase")

    backlog_text = BACKLOG.read_text(encoding="utf-8")
    for token in (
        'plan_task_id: P0-T03',
        'goal_text_sha256: 3d3ad1c9aebd6a2a2db1964bda744149fe9009be21992250402337d82a2ad3c2',
        'cross_task_relay_reuse: false',
        '- P0-T02',
    ):
        if token not in backlog_text:
            fail(errors, f"P0-T03 backlog contract missing token: {token}")

    report = {
        "schema_version": "v20-goal-relay-policy-validation.v3",
        "task_id": "RT-20260718-012",
        "plan_task_id": "P0-T03",
        "status": "PASS" if not errors else "FAIL",
        "runtime_schema": helper.SCHEMA_VERSION,
        "retained_schema_versions": [helper.LEGACY_SCHEMA_VERSION, helper.RETAINED_SCHEMA_VERSION],
        "scope_modes": sorted(helper.SCOPE_MODES),
        "worker_skills": sorted(helper.WORKER_SKILLS),
        "recovery_required_is_nonterminal": "recovery_required" in helper.NONTERMINAL_PHASES,
        "scenario_count": len(scenarios),
        "terminal_scenario_count": terminal_count,
        "recursive_scenario_count": recursive_count,
        "scenario_ids": sorted(ids),
        "source_hashes": actual_hashes,
        "policy_sha256": sha256_file(POLICY),
        "scenarios_sha256": sha256_file(SCENARIOS),
        "historical_p0_t02_tree_sha256": p0_t02_hash,
        "historical_p0_t02_unchanged": p0_t02_hash == data.get("historical_p0_t02_tree_sha256"),
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "errors": errors,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the deterministic JSON receipt")
    parser.add_argument("--json", action="store_true", help="print the receipt as JSON")
    args = parser.parse_args()
    report = validate()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.json:
        print(rendered, end="")
    else:
        print(
            f"{report['status']}: {report['scenario_count']} scenarios; "
            f"{report['terminal_scenario_count']} terminal; "
            f"{report['recursive_scenario_count']} recursive"
        )
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
