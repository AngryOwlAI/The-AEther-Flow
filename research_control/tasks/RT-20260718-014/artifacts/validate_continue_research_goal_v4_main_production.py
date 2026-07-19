#!/usr/bin/env python3
"""Validate the bounded continue-research-goal.v4 main-production policy."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260718-014"
POLICY = TASK_DIR / "artifacts/continue_research_goal_v4_main_production_policy.md"
REPORT = TASK_DIR / "artifacts/continue_research_goal_v4_main_production_validation.json"
HELPER = ROOT / ".codex/skills/continue-research-goal/scripts/goal_state.py"
LAUNCHER = ROOT / ".codex/skills/continue-research-goal/SKILL.md"
WORKER = ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md"
SCHEMA = ROOT / ".codex/skills/continue-research-goal/references/goal-file-schema.md"
TESTS = ROOT / "tests/test_continue_research_goal_state.py"
V4_TASK = ROOT / "research_control/tasks/RT-20260718-013"

EXPECTED_V4_TREE_SHA256 = "db16a687e8f68ff7e8da4853ec75c38046c0f1ac455ac5dc561771bbc3fd4d2e"
EXPECTED_PRESERVED_FILES = {
    "research_control/program_state.yaml":
        "1a28fc71d3076347be4221e4d30b4bf962e5f752fd9d90f099d916dd89a4706c",
    "research_control/handoffs/handoff-0740.yaml":
        "5be1f16f476c1f03db0baf3dcfec8ffc1947ff61c5d5d3ff43012239ce5c0c1d",
    "research_control/handoffs/handoff-0740.md":
        "2d2bb5936181f7040357c1074c06e124904b28cd84fdb6b3138be59055d02402",
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
    spec = importlib.util.spec_from_file_location("goal_state_main_policy_validation", HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load goal_state helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def binding(profile: str, branch: str) -> dict[str, str]:
    return {
        "execution_profile": profile,
        "root": "/Volumes/P-SSD/AngryOwl/The-AEther-Flow",
        "branch": branch,
        "environment_mode": "local",
        "git_common_dir": "/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.git",
        "starting_head": "b" * 40,
    }


def initialize(helper: Any, profile: str, branch: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temp:
        store = helper.GoalStore(Path(temp) / "goals")
        path, record = store.initialize(
            goal_text="validate bounded main-production policy",
            completion_contract={
                "interpretation": "complete one bounded goal",
                "required_evidence": ["tracked transition", "validators pass"],
                "user_confirmed_when_ambiguous": False,
            },
            scope_contract={
                "mode": "single_objective",
                "included_work_items": [
                    {
                        "work_item_id": "objective-1",
                        "objective": "complete one bounded goal",
                        "depends_on": [],
                    }
                ],
                "dependency_source": None,
                "exclusions": ["all work outside the exact goal"],
                "source_hashes": {"goal-source.md": "c" * 64},
                "allow_scope_expansion": False,
            },
            reasoning_effort="max",
            max_continue_passes=2,
            max_elapsed_minutes=30,
            repository_binding=binding(profile, branch),
            initial_fingerprint="a" * 64,
            timestamp="2026-07-18T12:00:00Z",
        )
        if store.read(path) != record:
            raise RuntimeError(f"{profile} {branch} did not round-trip")
        return record


def retained_record(helper: Any, record: dict[str, Any], schema_version: str) -> dict[str, Any]:
    retained = copy.deepcopy(record)
    retained["schema_version"] = schema_version
    if schema_version == helper.AUTONOMOUS_SCHEMA_VERSION:
        retained.pop("discussion_contract")
        retained.pop("discussion_contract_sha256")
        return retained
    for key in (
        "discussion_contract",
        "discussion_contract_sha256",
        "scope_contract",
        "scope_contract_sha256",
        "recovery_ledger",
        "completion_summary",
        "completion_summary_sha256",
        "human_intervention_summary",
        "human_intervention_summary_sha256",
    ):
        retained.pop(key)
    for key in ("approved_route", "approved_route_sha256", "human_intervention"):
        retained["state"].pop(key)
    for key in (
        "stop_on_human_gate",
        "stop_on_validation_failure",
        "stop_on_checkpoint_failure",
        "stop_on_unexpected_dirty_state",
        "stop_on_no_progress",
        "stop_on_repeated_state",
        "stop_on_capability_loss",
        "stop_on_branch_or_repository_mismatch",
    ):
        retained["guards"].pop(key)
    return retained


def require_tokens(errors: list[str], label: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            errors.append(f"{label} missing token: {token}")


def validate() -> dict[str, Any]:
    errors: list[str] = []
    helper = load_helper()
    texts = {
        "launcher": LAUNCHER.read_text(encoding="utf-8"),
        "worker": WORKER.read_text(encoding="utf-8"),
        "schema": SCHEMA.read_text(encoding="utf-8"),
        "helper": HELPER.read_text(encoding="utf-8"),
        "tests": TESTS.read_text(encoding="utf-8"),
        "policy": POLICY.read_text(encoding="utf-8"),
    }

    production_main = None
    try:
        production_main = initialize(helper, "production_profile", "main")
        initialize(helper, "production_profile", "codex/validation-branch")
    except Exception as exc:
        errors.append(f"valid v4 production binding rejected: {exc}")

    try:
        initialize(helper, "acceptance_test", "main")
    except helper.ValidationError:
        pass
    else:
        errors.append("acceptance_test main binding was accepted")

    if production_main is not None:
        for version in sorted(helper.RETAINED_SCHEMA_VERSIONS):
            retained = retained_record(helper, production_main, version)
            try:
                helper.validate_record(retained)
            except helper.ValidationError as exc:
                if "main is authorized only for v4 production_profile records" not in str(exc):
                    errors.append(f"{version} failed for the wrong reason: {exc}")
            else:
                errors.append(f"{version} main binding was accepted")

    require_tokens(
        errors,
        "launcher",
        texts["launcher"],
        (
            "branch: the current main branch or a current branch whose name begins with codex/",
            "continue to reject `main`",
            "accept either `main` or a\nbranch under `codex/*`",
            "Never treat a production `main` binding as authority to bypass any other",
        ),
    )
    require_tokens(
        errors,
        "worker",
        texts["worker"],
        (
            "A v4 `production_profile` branch may be `main` or begin with",
            "an `acceptance_test` branch must remain the exact disposable",
            "treat a production `main` binding as a guard bypass",
        ),
    )
    require_tokens(
        errors,
        "schema",
        texts["schema"],
        (
            'branch: "<exact acceptance branch | main | codex/* production branch>"',
            "For new v4 records, `main` is valid only with `production_profile`",
            "Retained v1-v3 records bound to `main`",
        ),
    )
    require_tokens(
        errors,
        "helper",
        texts["helper"],
        (
            'schema_version == SCHEMA_VERSION',
            'binding["execution_profile"] == "production_profile"',
            "main initialization requires production_profile",
        ),
    )
    require_tokens(
        errors,
        "tests",
        texts["tests"],
        (
            "test_v4_production_profile_main_round_trips",
            "test_secret_goal_and_acceptance_main_binding_are_rejected",
            "test_retained_v1_v3_records_bound_to_main_remain_rejected",
            "test_main_branch_policy_is_production_v4_only",
        ),
    )
    require_tokens(
        errors,
        "policy",
        texts["policy"],
        (
            "## Binding matrix",
            "## Preserved relay safeguards",
            "## Compatibility",
            "## Research and claim boundary",
        ),
    )

    old_bans = (
        "The branch must not be `main`.",
        "Never target `main`",
        "main is disabled for relay initialization",
        "main is not an authorized relay branch",
    )
    for label in ("launcher", "worker", "helper"):
        for token in old_bans:
            if token in texts[label]:
                errors.append(f"{label} retains obsolete blanket main ban: {token}")

    v4_tree_hash = tree_sha256(V4_TASK)
    if v4_tree_hash != EXPECTED_V4_TREE_SHA256:
        errors.append("completed RT-20260718-013 task tree changed")
    preserved_hashes: dict[str, str] = {}
    for relative, expected in EXPECTED_PRESERVED_FILES.items():
        actual = sha256_file(ROOT / relative)
        preserved_hashes[relative] = actual
        if actual != expected:
            errors.append(f"preserved research-control file changed: {relative}")

    source_paths = (POLICY, HELPER, LAUNCHER, WORKER, SCHEMA, TESTS)
    source_hashes = {
        path.relative_to(ROOT).as_posix(): sha256_file(path)
        for path in source_paths
    }
    checks = {
        "v4_production_main_round_trip": production_main is not None,
        "production_codex_branch_retained": not any(
            "valid v4 production binding rejected" in error for error in errors
        ),
        "acceptance_main_rejected": "acceptance_test main binding was accepted" not in errors,
        "retained_v1_v3_main_rejected": not any(
            error.startswith("continue-research-goal.v") for error in errors
        ),
        "five_surface_contract_synchronized": not any(
            "missing token" in error or "obsolete blanket main ban" in error
            for error in errors
        ),
        "completed_v4_transaction_unchanged": v4_tree_hash == EXPECTED_V4_TREE_SHA256,
        "ordinary_research_state_unchanged": all(
            preserved_hashes[path] == expected
            for path, expected in EXPECTED_PRESERVED_FILES.items()
        ),
    }
    return {
        "schema_version": "continue-research-goal-v4-main-production-validation.v1",
        "task_id": "RT-20260718-014",
        "status": "PASS" if not errors else "FAIL",
        "runtime_schema": helper.SCHEMA_VERSION,
        "checks": checks,
        "check_count": len(checks),
        "source_hashes": source_hashes,
        "completed_v4_tree_sha256": v4_tree_hash,
        "preserved_research_control_hashes": preserved_hashes,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "errors": errors,
    }


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
        print(f"{report['status']}: {report['check_count']} main-production policy checks")
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
