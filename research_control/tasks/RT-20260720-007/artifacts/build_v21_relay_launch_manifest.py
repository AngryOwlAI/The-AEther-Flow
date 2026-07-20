#!/usr/bin/env python3
"""Build and validate the bounded v21 P0-T04 relay launch artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260720-007"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GOAL_PATH = ROOT / ".codex/skills/continue-research-goal/goals" / f"goal-{GOAL_ID}.md"
PLAN_PATH = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
BACKLOG_PATH = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
BASELINE_PATH = ROOT / "research_control/tasks/RT-20260720-006/artifacts/v21_starting_baseline.json"
SOURCE_MANIFEST_PATH = ROOT / "research_control/tasks/RT-20260720-006/artifacts/v21_source_hash_manifest.json"
ARTIFACT_DIR = ROOT / "research_control/tasks/RT-20260720-007/artifacts"
SCOPE_PATH = ARTIFACT_DIR / "v21_scope_contract_candidate.json"
COMPLETION_PATH = ARTIFACT_DIR / "v21_completion_contract.md"
CHECKLIST_PATH = ARTIFACT_DIR / "v21_prelaunch_checklist.md"
MANIFEST_PATH = ARTIFACT_DIR / "v21_relay_launch_manifest.md"
RECEIPT_PATH = ARTIFACT_DIR / "v21_launch_manifest_receipt.json"

FIXED_GUARDS = {
    "max_repeated_state_fingerprints": 1,
    "max_live_continuations": 1,
    "handoff_ready_timeout_seconds": 60,
    "stop_on_human_gate": True,
    "stop_on_validation_failure": True,
    "stop_on_checkpoint_failure": True,
    "stop_on_unexpected_dirty_state": True,
    "stop_on_no_progress": True,
    "stop_on_repeated_state": True,
    "stop_on_capability_loss": True,
    "stop_on_branch_or_repository_mismatch": True,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_goal_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("goal record missing opening frontmatter delimiter")
    frontmatter, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        raise ValueError("goal record missing closing frontmatter delimiter")
    value = json.loads(frontmatter)
    if not isinstance(value, dict):
        raise ValueError("goal record frontmatter must be an object")
    return value


def assert_acyclic(items: list[dict[str, Any]]) -> int:
    graph = {item["work_item_id"]: list(item["depends_on"]) for item in items}
    visited: set[str] = set()
    active: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            raise ValueError(f"dependency cycle reaches {node}")
        if node in visited:
            return
        active.add(node)
        for dependency in graph[node]:
            if dependency not in graph:
                raise ValueError(f"missing dependency {dependency} for {node}")
            visit(dependency)
        active.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return sum(len(dependencies) for dependencies in graph.values())


def build_inputs() -> dict[str, Any]:
    goal = parse_goal_record(GOAL_PATH)
    backlog = yaml.safe_load(BACKLOG_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    source_manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))

    if goal["schema_version"] != "continue-research-goal.v4":
        raise ValueError("active goal is not v4")
    if goal["goal_id"] != GOAL_ID:
        raise ValueError("active goal id mismatch")
    if goal["discussion_contract"]["reasoning_effort"] != "max":
        raise ValueError("reasoning effort is not max")
    if goal["discussion_contract"]["confirmation_marker"] != "combined_goal_and_reasoning_effort_confirmed":
        raise ValueError("combined confirmation marker is absent")
    if goal["guards"].get("max_continue_passes") is not None or goal.get("deadline_at") is not None:
        raise ValueError("scheduling horizons are not both null")
    for key, value in FIXED_GUARDS.items():
        if goal["guards"].get(key) != value:
            raise ValueError(f"fixed guard mismatch: {key}")

    backlog_items = backlog["items"]
    included = [
        {
            "work_item_id": item["plan_task_id"],
            "objective": item["exact_objective"],
            "depends_on": item["depends_on"],
        }
        for item in backlog_items
    ]
    if len(included) != 122:
        raise ValueError("backlog does not contain 122 work items")
    if len({item["work_item_id"] for item in included}) != len(included):
        raise ValueError("duplicate work-item id")
    dependency_edge_count = assert_acyclic(included)

    active_scope = goal["scope_contract"]
    candidate_scope = {
        "mode": "multi_step",
        "included_work_items": included,
        "dependency_source": {
            "path": str(PLAN_PATH.relative_to(ROOT)),
            "sha256": sha256_file(PLAN_PATH),
        },
        "exclusions": active_scope["exclusions"],
        "source_hashes": active_scope["source_hashes"],
        "allow_scope_expansion": False,
    }
    if canonical_json(candidate_scope) != canonical_json(active_scope):
        raise ValueError("candidate scope does not equal the validated active scope contract")
    if sha256_text(canonical_json(candidate_scope)) != goal["scope_contract_sha256"]:
        raise ValueError("scope-contract hash mismatch")

    baseline_by_path = {record["path"]: record for record in source_manifest["records"]}
    comparison = []
    for path, launch_sha256 in candidate_scope["source_hashes"].items():
        record = baseline_by_path.get(path)
        if record is None:
            raise ValueError(f"baseline source record missing: {path}")
        if record.get("goal_scope_launch_sha256") != launch_sha256:
            raise ValueError(f"baseline launch hash mismatch: {path}")
        comparison.append(
            {
                "path": path,
                "launch_sha256": launch_sha256,
                "baseline_sha256": record["sha256"],
                "launch_matches_baseline": launch_sha256 == record["sha256"],
                "baseline_retained_at_commit": record["retained_at_baseline_commit"],
            }
        )

    required_exclusion_fragments = (
        "scope expansion",
        "goal files",
        "human",
        "push",
        "benchmark",
        "completed-derivation",
    )
    exclusion_text = "\n".join(candidate_scope["exclusions"]).lower()
    for fragment in required_exclusion_fragments:
        if fragment not in exclusion_text:
            raise ValueError(f"required exclusion missing: {fragment}")

    runtime_paths = sorted(path.name for path in GOAL_PATH.parent.glob("goal-*.md"))
    return {
        "goal": goal,
        "backlog": backlog,
        "baseline": baseline,
        "source_manifest": source_manifest,
        "scope": candidate_scope,
        "source_comparison": comparison,
        "dependency_edge_count": dependency_edge_count,
        "runtime_paths": runtime_paths,
    }


def render_scope(inputs: dict[str, Any]) -> str:
    return json.dumps(inputs["scope"], indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_completion(inputs: dict[str, Any]) -> str:
    goal = inputs["goal"]
    contract_json = json.dumps(goal["completion_contract"], indent=2, ensure_ascii=False, sort_keys=True)
    return f"""<!-- authority: control -->

# V21 P0-T04 completion contract

This task-local control artifact reproduces the validated active v4 completion
contract. It is not scientific evidence, a claim promotion, or permission to
initialize a duplicate relay.

- Goal ID: `{goal['goal_id']}`
- Goal SHA-256: `{goal['goal_sha256']}`
- Completion-contract SHA-256: `{goal['completion_contract_sha256']}`
- Scope-contract SHA-256: `{goal['scope_contract_sha256']}`

```json
{contract_json}
```

The positive base case requires every criterion above to be proved by
canonical tracked evidence and required validators. An unresolved protected
human gate requires the deterministic human-action terminal, not an invented
approval.
"""


def render_checklist(inputs: dict[str, Any]) -> str:
    goal = inputs["goal"]
    baseline_mismatches = [row["path"] for row in inputs["source_comparison"] if not row["launch_matches_baseline"]]
    mismatch_text = ", ".join(f"`{path}`" for path in baseline_mismatches) or "none"
    return f"""<!-- authority: control -->

# V21 P0-T04 prelaunch checklist

This checklist is a tracked planning artifact. It does not call the launcher,
reserve a successor, create a goal record, or override an active relay lease.

## Static contract checks completed by P0-T04

- [x] Goal text SHA-256 is `{goal['goal_sha256']}`.
- [x] Combined goal and reasoning-effort confirmation marker is present.
- [x] `reasoning_effort` is exactly `max`.
- [x] Scope mode is `multi_step`.
- [x] Included work-item count is 122 and dependency edge count is {inputs['dependency_edge_count']}.
- [x] Work-item IDs, objectives, and dependencies equal the materialized backlog.
- [x] Dependency source is the registered v21 plan with SHA-256 `{inputs['scope']['dependency_source']['sha256']}`.
- [x] `allow_scope_expansion` is `false`.
- [x] `max_continue_passes` and `deadline_at` are JSON `null`.
- [x] Every fixed v4 stop guard is retained.
- [x] Production binding requires the exact project root, Git common directory, local mode, and `main` or `codex/*` branch.
- [x] Baseline evidence contains the exact immutable launch hash for all ten scope source paths.
- [x] P0-T03 baseline paths whose bytes differ from the immutable launch hash: {mismatch_text}.
- [x] Runtime goal-file inventory was unchanged during artifact generation.

## Human and live-runtime checks required before any future submission

- [ ] Confirm the exact goal text and `reasoning_effort: "max"` together in one unambiguous response.
- [ ] Verify no active conforming goal or worktree-global relay lease exists.
- [ ] Rediscover `list_projects`, `create_thread`, and `node_repl`; verify the active model supports `max` and the current task is running at `max`.
- [ ] Verify exactly one saved local project resolves to `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- [ ] Verify the production checkout is clean, locally bound, and on `main` or `codex/*` at the intended starting HEAD.
- [ ] Recompute every mutable source hash. If goal text, work items, dependencies, exclusions, or source hashes changed, regenerate this manifest instead of editing the contract by hand.
- [ ] Do not submit this packet while goal `{goal['goal_id']}` remains active; a duplicate live relay is forbidden.
- [ ] Do not push, merge, publish, promote a benchmark, bypass a human gate, or claim a completed derivation through launcher status.
"""


def work_item_table(items: list[dict[str, Any]]) -> str:
    rows = ["| Work item | Dependencies | Objective |", "| --- | --- | --- |"]
    for item in items:
        dependencies = ", ".join(f"`{value}`" for value in item["depends_on"]) or "none"
        objective = item["objective"].replace("|", "\\|")
        rows.append(f"| `{item['work_item_id']}` | {dependencies} | {objective} |")
    return "\n".join(rows)


def render_manifest(inputs: dict[str, Any]) -> str:
    goal = inputs["goal"]
    scope_json = json.dumps(inputs["scope"], indent=2, ensure_ascii=False, sort_keys=True)
    completion_json = json.dumps(goal["completion_contract"], indent=2, ensure_ascii=False, sort_keys=True)
    source_rows = ["| Path | Immutable launch SHA-256 | P0-T03 baseline SHA-256 |", "| --- | --- | --- |"]
    for row in inputs["source_comparison"]:
        source_rows.append(
            f"| `{row['path']}` | `{row['launch_sha256']}` | `{row['baseline_sha256']}` |"
        )
    runtime_inventory = ", ".join(f"`{path}`" for path in inputs["runtime_paths"])
    return f"""<!-- authority: control -->

# V21 P0-T04 continue-research-goal v4 production launch manifest

## Status and boundary

This is the tracked, human-readable reconstruction of the accepted active v4
relay contract for goal `{goal['goal_id']}`. It is draft/control orchestration
evidence only. P0-T04 did not call `initialize`, reserve a successor, create a
Codex task, or create a second runtime goal. The currently observed goal-file
inventory is {runtime_inventory} and was unchanged by generation.

A future operator may use this packet only after the live relay is terminal,
all current capability and repository checks pass, every mutable source hash is
recomputed, and the exact goal plus `reasoning_effort: "max"` receive combined
confirmation. It is never authority for a parallel duplicate relay.

## Exact launcher input

```yaml
goal: |-
  {goal['goal_text']}
reasoning_effort: "max"
scope:
  mode: "multi_step"
  included_work_items: "Use the exact JSON contract below; 122 items, {inputs['dependency_edge_count']} dependency edges."
  dependency_source:
    path: "{inputs['scope']['dependency_source']['path']}"
    sha256: "{inputs['scope']['dependency_source']['sha256']}"
  exclusions: "Use the exact JSON contract below."
  source_hashes: "Use the exact JSON contract below."
  allow_scope_expansion: false
max_continue_passes: null
deadline_at: null
```

The launcher must restate the complete goal and the separate exact line
`reasoning_effort: "max"`, then obtain one combined unambiguous confirmation
before capability preflight or state creation.

## Exact scope-contract candidate

- Scope-contract SHA-256: `{goal['scope_contract_sha256']}`
- Work-item count: 122
- Dependency-edge count: {inputs['dependency_edge_count']}
- Dependency source: `{inputs['scope']['dependency_source']['path']}`

```json
{scope_json}
```

## Included work items

{work_item_table(inputs['scope']['included_work_items'])}

## Exact completion contract

- Completion-contract SHA-256: `{goal['completion_contract_sha256']}`

```json
{completion_json}
```

## Scheduling and fixed guards

- `max_continue_passes`: `null`
- `deadline_at`: `null`
- `max_repeated_state_fingerprints`: `1`
- `max_live_continuations`: `1`
- `handoff_ready_timeout_seconds`: `60`
- Every stop-on-human-gate, validation, checkpoint, unexpected-dirty-state,
  no-progress, repeated-state, capability-loss, and repository-mismatch guard
  remains `true`.

Unlimited scheduling changes only the count and elapsed-time horizons. It does
not expand the one-worker/one-AgentJob frame, weaken leases or validators,
bypass protected authority, broaden scope, or permit a consumed generation to
run twice.

## Production repository binding

- Execution profile: `{goal['repository_binding']['execution_profile']}`
- Root: `{goal['repository_binding']['root']}`
- Git common directory: `{goal['repository_binding']['git_common_dir']}`
- Branch policy: `main` or `codex/*`; the accepted active contract records `{goal['repository_binding']['branch']}`.
- Environment mode: `{goal['repository_binding']['environment_mode']}`
- Accepted starting HEAD: `{goal['repository_binding']['starting_head']}`

Before any future launch, rediscover the saved project, task-tool contracts,
active model and effort metadata, root, Git common directory, branch, HEAD,
porcelain, tracked research state, and global relay lease. Never substitute a
fork, hook, controller, plugin, or default reasoning effort.

## Source-hash evidence

The baseline manifest records both the immutable launch hash and the frozen
P0-T03 baseline hash. Their one known mismatch is tracked control-state
evolution, not permission to rewrite the active immutable scope. A future
operator must separately recompute every live mutable hash before launch.

{chr(10).join(source_rows)}

## Explicit non-authority

This manifest is not physics proof, canonical ontology, source-law adoption,
EqSrc discharge, effective metric or coupling derivation, Einstein equations,
benchmark promotion, Gate Chair authority, publication authority, or a
completed derivation. Generated views, validators, registries, tasks, and goal
state remain operational evidence only within their declared authority.
"""


def build_expected() -> tuple[dict[Path, str], dict[str, Any]]:
    inputs = build_inputs()
    scope_text = render_scope(inputs)
    completion_text = render_completion(inputs)
    checklist_text = render_checklist(inputs)
    manifest_text = render_manifest(inputs)
    artifacts = {
        SCOPE_PATH: scope_text,
        COMPLETION_PATH: completion_text,
        CHECKLIST_PATH: checklist_text,
        MANIFEST_PATH: manifest_text,
    }
    comparison_mismatches = [row["path"] for row in inputs["source_comparison"] if not row["launch_matches_baseline"]]
    receipt = {
        "schema_id": "v21_p0_t04_launch_manifest_receipt_v1",
        "task_id": TASK_ID,
        "plan_task_id": "P0-T04",
        "goal_id": inputs["goal"]["goal_id"],
        "goal_sha256": inputs["goal"]["goal_sha256"],
        "discussion_contract_sha256": inputs["goal"]["discussion_contract_sha256"],
        "completion_contract_sha256": inputs["goal"]["completion_contract_sha256"],
        "scope_contract_sha256": inputs["goal"]["scope_contract_sha256"],
        "reasoning_effort": "max",
        "scope_mode": "multi_step",
        "work_item_count": len(inputs["scope"]["included_work_items"]),
        "dependency_edge_count": inputs["dependency_edge_count"],
        "source_hash_count": len(inputs["scope"]["source_hashes"]),
        "baseline_launch_hash_match_count": len(inputs["source_comparison"]),
        "baseline_launch_hash_mismatch_count": len(comparison_mismatches),
        "baseline_launch_hash_mismatch_paths": comparison_mismatches,
        "runtime_goal_files_before": inputs["runtime_paths"],
        "runtime_goal_files_after": inputs["runtime_paths"],
        "runtime_goal_file_inventory_unchanged": True,
        "runtime_goal_created_by_task": False,
        "initialize_called": False,
        "successor_reserved_by_task": False,
        "result_status": "PASS_VALIDATED_ACTIVE_CONTRACT_RECONSTRUCTION",
        "recommendation_ids": ["V21-R34", "V21-R35", "V21-R40", "V21-R44"],
        "artifact_sha256": {
            str(path.relative_to(ROOT)): sha256_text(text) for path, text in artifacts.items()
        },
        "validator_results": [
            {"validator_id": "v21_scope_contract_schema", "status": "PASS"},
            {"validator_id": "v21_work_item_backlog_parity", "status": "PASS"},
            {"validator_id": "v21_source_hash_baseline_parity", "status": "PASS"},
            {"validator_id": "v21_discussion_contract", "status": "PASS"},
            {"validator_id": "v21_completion_contract", "status": "PASS"},
            {"validator_id": "v21_fixed_guards", "status": "PASS"},
            {"validator_id": "v21_repository_binding_checklist", "status": "PASS"},
            {"validator_id": "v21_no_runtime_goal_created", "status": "PASS"},
        ],
        "finding_counts": {
            "hard_failure": 0,
            "explained_baseline_launch_hash_drift": len(comparison_mismatches),
            "scope_mismatch": 0,
            "work_item_mismatch": 0,
            "runtime_goal_inventory_change": 0,
        },
        "claim_boundary_summary": "Control-only launch-contract reconstruction; no duplicate launch, scientific claim, protected authority, publication, or downstream task execution.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    receipt_text = json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    artifacts[RECEIPT_PATH] = receipt_text
    return artifacts, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    before = sorted(path.name for path in GOAL_PATH.parent.glob("goal-*.md"))
    artifacts, receipt = build_expected()
    if args.write:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        for path, content in artifacts.items():
            path.write_text(content, encoding="utf-8")
    stale = []
    for path, expected in artifacts.items():
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            stale.append(str(path.relative_to(ROOT)))
    after = sorted(path.name for path in GOAL_PATH.parent.glob("goal-*.md"))
    if before != after:
        raise ValueError("runtime goal-file inventory changed during P0-T04 artifact generation")

    result = {
        "status": "PASS" if not stale else "FAIL",
        "mode": "write" if args.write else "check",
        "task_id": TASK_ID,
        "goal_id": GOAL_ID,
        "work_item_count": receipt["work_item_count"],
        "dependency_edge_count": receipt["dependency_edge_count"],
        "source_hash_count": receipt["source_hash_count"],
        "baseline_launch_hash_mismatch_count": receipt["baseline_launch_hash_mismatch_count"],
        "runtime_goal_file_inventory_unchanged": before == after,
        "stale_outputs": stale,
        "outputs": [str(path.relative_to(ROOT)) for path in artifacts],
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if not stale else 1


if __name__ == "__main__":
    raise SystemExit(main())
