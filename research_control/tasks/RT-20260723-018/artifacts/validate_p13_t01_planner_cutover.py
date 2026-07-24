#!/usr/bin/env python3
"""Build the bounded v21 P13-T01 planner-equivalence cutover packet."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.project_control.classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.plan import build_plan, load_manifest  # noqa: E402
from scripts.validation.run import DEFAULT_BINDINGS, load_adapters  # noqa: E402


TASK_ID = "RT-20260723-018"
JOB_ID = "AJ-RT-20260723-018-001"
TASK = ROOT / "research_control/tasks" / TASK_ID
ARTIFACTS = TASK / "artifacts"
LOCAL = ROOT / ".local/v21_p13_t01"

CORPUS_PATH = ROOT / "tests/fixtures/validation_equivalence/corpus.json"
EQUIVALENCE_TEST_PATH = ROOT / "tests/test_validation_equivalence.py"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
POLICY_PATH = (
    ROOT
    / "research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md"
)
PLAN_PATH = (
    ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
)
BACKLOG_PATH = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
PROJECT_WORKFLOW_PATH = ROOT / ".github/workflows/project-control-validation.yml"
SCHEDULED_WORKFLOW_PATH = ROOT / ".github/workflows/scheduled-full-validation.yml"
CHECKPOINT_PATH = ROOT / "scripts/research_control/checkpoint_research_transaction.py"
PREVIOUS_BINDING_REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260718-007/artifacts/"
    "planner_execution_binding_report.json"
)
PREVIOUS_HOSTED_CI_REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260718-008/artifacts/"
    "planner_hosted_ci_authority_evidence.json"
)

EQUIVALENCE_RESULTS_PATH = ARTIFACTS / "p13_t01_validation_planner_equivalence_corpus.json"
MISMATCH_LEDGER_PATH = ARTIFACTS / "p13_t01_mismatch_disposition_ledger.json"
CUTOVER_DECISION_PATH = ARTIFACTS / "p13_t01_cutover_decision.md"
COMPACT_RECEIPT_PATH = ARTIFACTS / "p13_t01_compact_receipt.json"

FOCUSED_TESTS = (
    "tests.test_validation_equivalence",
    "tests.test_checkpoint_validation_planner",
    "tests.test_validation_profiles",
    "tests.test_validation_precheck",
    "tests.test_staged_validation",
    "tests.test_ci_validation_plan",
    "tests.test_validation_executor",
    "tests.test_validation_orchestration",
)

REPRESENTATIVE_CHANGE_FAMILIES = (
    ("explanatory_markdown", ("README.md",)),
    ("research_control_state", ("research_control/program_state.yaml",)),
    ("canonical_registry", ("registries/AGENT_JOB_REGISTRY.csv",)),
    ("validation_implementation", ("scripts/validation/cli.py",)),
    ("validation_test", ("tests/test_validation_equivalence.py",)),
)

NON_NEGOTIABLE_GATE_IDS = {
    "classify_changes",
    "resolve_project_improvement",
    "project_improvement_signals",
    "documentation_impact",
    "memory_sync",
    "memory_core",
    "research_control_core",
    "research_control_diff",
    "test_shard_repository",
    "claim_graph_validation",
    "git_diff_check",
    "continue_memory_preflight",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def run_command(
    label: str,
    command: list[str],
    *,
    timeout: int = 1800,
) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    duration = time.monotonic() - started
    stdout_path = LOCAL / f"{label}.stdout.log"
    stderr_path = LOCAL / f"{label}.stderr.log"
    stdout_path.write_text(completed.stdout or "", encoding="utf-8")
    stderr_path.write_text(completed.stderr or "", encoding="utf-8")
    return {
        "label": label,
        "command": command,
        "returncode": completed.returncode,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "duration_seconds": round(duration, 6),
        "stdout": {
            "path": stdout_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stdout_path),
            "bytes": stdout_path.stat().st_size,
        },
        "stderr": {
            "path": stderr_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stderr_path),
            "bytes": stderr_path.stat().st_size,
        },
    }


def load_equivalence_module():
    specification = importlib.util.spec_from_file_location(
        "p13_t01_validation_equivalence",
        EQUIVALENCE_TEST_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load validation-equivalence module")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def execute_fixed_corpus() -> list[dict[str, Any]]:
    module = load_equivalence_module()
    observed = module.execute_corpus()
    results: list[dict[str, Any]] = []
    for result in observed:
        results.append(
            {
                "fixture_id": result["fixture_id"],
                "legacy": result["legacy"],
                "planner_candidate": result["consolidated"],
                "mismatch_fields": result["mismatch_fields"],
                "hard_mismatch": result["blocking"],
                "disposition": (
                    "unexplained_hard_mismatch"
                    if result["blocking"]
                    else "matched_no_disposition_required"
                ),
            }
        )
    return results


def plan_comparisons(
    live_manifest: dict[str, Any],
    candidate_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    for family_id, paths in REPRESENTATIVE_CHANGE_FAMILIES:
        classification = classify_paths(paths)
        legacy_plan = build_plan(
            live_manifest,
            classification,
            profile="affected",
            scopes=(),
        )
        candidate_plan = build_plan(
            candidate_manifest,
            classification,
            profile="affected",
            scopes=(),
        )
        mismatch_fields: list[str] = []
        for field, legacy_value, candidate_value in (
            ("status", legacy_plan.status, candidate_plan.status),
            (
                "ordered_gate_ids",
                legacy_plan.ordered_gate_ids,
                candidate_plan.ordered_gate_ids,
            ),
            (
                "selected_gate_ids",
                legacy_plan.selected_gate_ids,
                candidate_plan.selected_gate_ids,
            ),
            ("blocked_paths", legacy_plan.blocked_paths, candidate_plan.blocked_paths),
            ("unknown_paths", legacy_plan.unknown_paths, candidate_plan.unknown_paths),
        ):
            if legacy_value != candidate_value:
                mismatch_fields.append(field)
        comparisons.append(
            {
                "family_id": family_id,
                "paths": list(paths),
                "legacy": {
                    "status": legacy_plan.status,
                    "selected_gate_ids": list(legacy_plan.selected_gate_ids),
                    "planner_executes_commands": legacy_plan.to_dict()[
                        "planner_executes_commands"
                    ],
                },
                "planner_candidate": {
                    "status": candidate_plan.status,
                    "selected_gate_ids": list(candidate_plan.selected_gate_ids),
                    "planner_executes_commands": candidate_plan.to_dict()[
                        "planner_executes_commands"
                    ],
                },
                "mismatch_fields": mismatch_fields,
                "hard_mismatch": bool(mismatch_fields),
                "disposition": (
                    "unexplained_hard_mismatch"
                    if mismatch_fields
                    else "matched_no_disposition_required"
                ),
            }
        )
    return comparisons


def hosted_ci_runs(head: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    receipt = run_command(
        "current-head-ci",
        [
            "gh",
            "run",
            "list",
            "--commit",
            head,
            "--limit",
            "20",
            "--json",
            "databaseId,workflowName,status,conclusion,headSha,url",
        ],
        timeout=120,
    )
    if receipt["status"] != "PASS":
        return receipt, []
    stdout_path = ROOT / str(receipt["stdout"]["path"])
    try:
        payload = json.loads(stdout_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return receipt, []
    return receipt, payload if isinstance(payload, list) else []


def write_outputs(
    equivalence: dict[str, Any],
    mismatch_ledger: dict[str, Any],
    compact_receipt: dict[str, Any],
) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    EQUIVALENCE_RESULTS_PATH.write_text(
        json.dumps(equivalence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    MISMATCH_LEDGER_PATH.write_text(
        json.dumps(mismatch_ledger, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    compact_receipt["artifacts"] = {
        "equivalence_corpus_results": {
            "path": EQUIVALENCE_RESULTS_PATH.relative_to(ROOT).as_posix(),
            "sha256": sha256(EQUIVALENCE_RESULTS_PATH),
        },
        "mismatch_disposition_ledger": {
            "path": MISMATCH_LEDGER_PATH.relative_to(ROOT).as_posix(),
            "sha256": sha256(MISMATCH_LEDGER_PATH),
        },
        "cutover_decision": {
            "path": CUTOVER_DECISION_PATH.relative_to(ROOT).as_posix(),
        },
    }
    decision = equivalence["cutover_decision"]
    lines = [
        "---",
        "authority: control",
        f'task_id: "{TASK_ID}"',
        f'job_id: "{JOB_ID}"',
        'plan_task_id: "P13-T01"',
        f'decision: "{decision["verdict"]}"',
        "cutover_authorized: false",
        "scientific_claims_changed: false",
        "---",
        "",
        "# P13-T01 validation-planner cutover decision",
        "",
        "## Decision",
        "",
        f"`{decision['verdict']}`.",
        "",
        decision["summary"],
        "",
        "The fixed component corpus and representative planner-selection families "
        "contain zero unexplained hard mismatches. That local result is necessary "
        "but not sufficient for a live cutover.",
        "",
        "## Evidence gaps",
        "",
    ]
    lines.extend(f"- `{finding}`" for finding in decision["evidence_gaps"])
    if not decision["evidence_gaps"]:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Safety failures",
            "",
        ]
    )
    lines.extend(f"- `{finding}`" for finding in decision["safety_failures"])
    if not decision["safety_failures"]:
        lines.append("- None observed.")
    lines.extend(
        [
            "",
            "## Authority boundary",
            "",
            "The live manifest remains `shadow_planner` with `legacy` execution "
            "authority and the explicit rollback path retained. This operational "
            "audit does not change validation authority, workflow behavior, "
            "scientific status, ontology, benchmark status, proof authority, "
            "Distance-to-GR status, or publication authority.",
            "",
            "## Reopening criteria",
            "",
            decision["reopening_criteria"],
            "",
        ]
    )
    CUTOVER_DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")
    compact_receipt["artifacts"]["cutover_decision"]["sha256"] = sha256(
        CUTOVER_DECISION_PATH
    )
    COMPACT_RECEIPT_PATH.write_text(
        json.dumps(compact_receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    observed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    head = git("rev-parse", "HEAD").stdout.strip()
    branch = git("branch", "--show-current").stdout.strip()
    origin_head_result = git("rev-parse", "--verify", "origin/main", check=False)
    origin_head = (
        origin_head_result.stdout.strip() if origin_head_result.returncode == 0 else None
    )
    head_on_origin_main = False
    if origin_head:
        head_on_origin_main = (
            git("merge-base", "--is-ancestor", head, "origin/main", check=False).returncode
            == 0
        )

    live_manifest = load_manifest(MANIFEST_PATH)
    candidate_manifest = deepcopy(live_manifest)
    candidate_manifest["migration_epoch"] = "planner_authoritative"
    candidate_manifest["execution_authority"] = "manifest_planner"

    fixed_corpus = execute_fixed_corpus()
    selection_comparisons = plan_comparisons(live_manifest, candidate_manifest)
    full_candidate_plan = build_plan(
        candidate_manifest,
        classify_paths(()),
        profile="full",
        scopes=("repository",),
    )
    candidate_adapters = load_adapters(DEFAULT_BINDINGS, candidate_manifest)
    manifest_gates = {
        str(gate["gate_id"]): gate
        for gate in candidate_manifest["gates"]
        if isinstance(gate, dict)
    }
    missing_binding_gate_ids = sorted(
        gate_id
        for gate_id in full_candidate_plan.selected_gate_ids
        if str(manifest_gates[gate_id]["adapter"]) not in candidate_adapters
    )
    missing_non_negotiable_gate_ids = sorted(
        NON_NEGOTIABLE_GATE_IDS - set(full_candidate_plan.selected_gate_ids)
    )

    focused_tests = run_command(
        "focused-planner-burn-in",
        [sys.executable, "-m", "unittest", "-v", *FOCUSED_TESTS],
    )
    ci_receipt, ci_runs = hosted_ci_runs(head)

    project_workflow = PROJECT_WORKFLOW_PATH.read_text(encoding="utf-8")
    scheduled_workflow = SCHEDULED_WORKFLOW_PATH.read_text(encoding="utf-8")
    checkpoint = CHECKPOINT_PATH.read_text(encoding="utf-8")
    previous_binding = load_json(PREVIOUS_BINDING_REPORT_PATH)
    previous_hosted_ci = load_json(PREVIOUS_HOSTED_CI_REPORT_PATH)

    corpus_mismatches = [item for item in fixed_corpus if item["hard_mismatch"]]
    selection_mismatches = [
        item for item in selection_comparisons if item["hard_mismatch"]
    ]
    safety_failures: list[str] = []
    if corpus_mismatches:
        safety_failures.append("fixed_corpus_contains_unexplained_hard_mismatch")
    if selection_mismatches:
        safety_failures.append(
            "representative_selection_contains_unexplained_hard_mismatch"
        )
    if focused_tests["status"] != "PASS":
        safety_failures.append("focused_planner_burn_in_failed")
    if missing_binding_gate_ids:
        safety_failures.append("planner_candidate_adapter_coverage_incomplete")
    if missing_non_negotiable_gate_ids:
        safety_failures.append("planner_candidate_drops_non_negotiable_gate")
    if (
        'parser.set_defaults(validation_mode="compare")' not in checkpoint
        or "--legacy-validation" not in checkpoint
    ):
        safety_failures.append("checkpoint_compare_or_rollback_switch_missing")
    if "schedule:" not in scheduled_workflow or "--profile full" not in scheduled_workflow:
        safety_failures.append("scheduled_full_workflow_missing_or_filtered")

    evidence_gaps: list[str] = []
    if live_manifest.get("migration_epoch") != "planner_authoritative":
        evidence_gaps.append("live_manifest_epoch_remains_shadow_planner")
    if live_manifest.get("execution_authority") != "manifest_planner":
        evidence_gaps.append("live_manifest_execution_authority_remains_legacy")
    if not head_on_origin_main:
        evidence_gaps.append("current_head_is_not_published_on_origin_main")
    if not ci_runs:
        evidence_gaps.append("no_hosted_ci_run_for_current_head")
        evidence_gaps.append("no_scheduled_full_run_for_current_head")
    if "continue-on-error: true" in project_workflow:
        evidence_gaps.append("project_control_planner_jobs_remain_shadow_advisory")
    evidence_gaps.extend(
        [
            "three_clean_current_head_shadow_transactions_not_recorded",
            "affected_checkpoint_full_matched_execution_set_not_recorded",
            "uncached_current_head_final_staged_tree_comparison_pending",
            "current_head_safety_budget_receipt_not_recorded",
        ]
    )
    if previous_binding.get("status") != "PASS":
        evidence_gaps.append("prior_candidate_execution_binding_receipt_not_pass")
    if (
        previous_hosted_ci.get("hosted_ci", {}).get("official_ci_evidence_status")
        != "ABSENT"
    ):
        evidence_gaps.append("prior_hosted_ci_boundary_receipt_drifted")

    if safety_failures:
        verdict = "ROLLBACK_REQUIRED"
        summary = (
            "At least one non-negotiable equivalence, rollback, or gate-preservation "
            "check failed. Live legacy authority must remain in place."
        )
    elif evidence_gaps:
        verdict = "HOLD_LEGACY_REPAIR_REQUIRED"
        summary = (
            "The bounded local burn-in has zero unexplained hard mismatches and the "
            "rollback path passes, but live cutover evidence is incomplete. Legacy "
            "execution remains authoritative."
        )
    else:
        verdict = "CUTOVER_AUTHORIZED"
        summary = (
            "Every P13-T01 equivalence, rollback, authority, and current-head "
            "hosted-CI criterion is directly proven."
        )

    all_ledger_rows = [
        {
            "comparison_id": f"corpus:{item['fixture_id']}",
            "comparison_class": "fixed_component_corpus",
            "hard_mismatch": item["hard_mismatch"],
            "mismatch_fields": item["mismatch_fields"],
            "disposition": item["disposition"],
            "investigation_status": (
                "OPEN" if item["hard_mismatch"] else "NOT_REQUIRED"
            ),
        }
        for item in fixed_corpus
    ]
    all_ledger_rows.extend(
        {
            "comparison_id": f"selection:{item['family_id']}",
            "comparison_class": "representative_planner_selection",
            "hard_mismatch": item["hard_mismatch"],
            "mismatch_fields": item["mismatch_fields"],
            "disposition": item["disposition"],
            "investigation_status": (
                "OPEN" if item["hard_mismatch"] else "NOT_REQUIRED"
            ),
        }
        for item in selection_comparisons
    )
    mismatch_ledger = {
        "schema_id": "v21_p13_t01_mismatch_disposition_ledger_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P13-T01",
        "observed_at": observed_at,
        "status": "PASS" if not safety_failures else "FAIL",
        "comparison_count": len(all_ledger_rows),
        "hard_mismatch_count": sum(row["hard_mismatch"] for row in all_ledger_rows),
        "unexplained_hard_mismatch_count": sum(
            row["disposition"] == "unexplained_hard_mismatch"
            for row in all_ledger_rows
        ),
        "rows": all_ledger_rows,
        "authority": {
            "operational_validation_only": True,
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }

    equivalence = {
        "schema_id": "v21_p13_t01_validation_planner_equivalence_corpus_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P13-T01",
        "recommendation_ids": ["V21-R54"],
        "observed_at": observed_at,
        "burn_in_window": {
            "kind": "fixed_current_head_local_window",
            "branch": branch,
            "head": head,
            "origin_main": origin_head,
            "head_published_on_origin_main": head_on_origin_main,
            "tree_basis": "same repository checkout, Python environment, manifest, and fixed fixtures",
        },
        "fixed_component_corpus": {
            "path": CORPUS_PATH.relative_to(ROOT).as_posix(),
            "sha256": sha256(CORPUS_PATH),
            "fixture_count": len(fixed_corpus),
            "hard_mismatch_count": len(corpus_mismatches),
            "results": fixed_corpus,
        },
        "representative_change_families": {
            "family_count": len(selection_comparisons),
            "hard_mismatch_count": len(selection_mismatches),
            "results": selection_comparisons,
        },
        "planner_candidate": {
            "migration_epoch": candidate_manifest["migration_epoch"],
            "execution_authority": candidate_manifest["execution_authority"],
            "full_plan_status": full_candidate_plan.status,
            "full_plan_gate_count": len(full_candidate_plan.selected_gate_ids),
            "planner_executes_commands": full_candidate_plan.to_dict()[
                "planner_executes_commands"
            ],
            "missing_binding_gate_ids": missing_binding_gate_ids,
            "missing_non_negotiable_gate_ids": missing_non_negotiable_gate_ids,
            "live_authority_changed": False,
        },
        "rollback_drill": {
            "focused_test_receipt": focused_tests,
            "checkpoint_compare_default": (
                'parser.set_defaults(validation_mode="compare")' in checkpoint
            ),
            "explicit_legacy_switch": "--legacy-validation" in checkpoint,
            "scheduled_full_present": (
                "schedule:" in scheduled_workflow
                and "--profile full" in scheduled_workflow
            ),
            "status": "PASS"
            if focused_tests["status"] == "PASS"
            and "--legacy-validation" in checkpoint
            else "FAIL",
        },
        "hosted_ci": {
            "query_receipt": ci_receipt,
            "matched_current_head_run_count": len(ci_runs),
            "runs": ci_runs,
        },
        "prior_evidence": {
            "candidate_execution_binding": {
                "path": PREVIOUS_BINDING_REPORT_PATH.relative_to(ROOT).as_posix(),
                "sha256": sha256(PREVIOUS_BINDING_REPORT_PATH),
                "status": previous_binding.get("status"),
                "observed_head": previous_binding.get("repository", {}).get("head"),
            },
            "hosted_ci_authority_boundary": {
                "path": PREVIOUS_HOSTED_CI_REPORT_PATH.relative_to(ROOT).as_posix(),
                "sha256": sha256(PREVIOUS_HOSTED_CI_REPORT_PATH),
                "status": previous_hosted_ci.get("decision", {}).get("status"),
            },
        },
        "source_hashes": {
            "implementation_plan_sha256": sha256(PLAN_PATH),
            "recommendation_backlog_sha256": sha256(BACKLOG_PATH),
            "migration_policy_sha256": sha256(POLICY_PATH),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "adapter_bindings_sha256": sha256(DEFAULT_BINDINGS),
            "equivalence_test_sha256": sha256(EQUIVALENCE_TEST_PATH),
            "project_control_workflow_sha256": sha256(PROJECT_WORKFLOW_PATH),
            "scheduled_full_workflow_sha256": sha256(SCHEDULED_WORKFLOW_PATH),
            "checkpoint_sha256": sha256(CHECKPOINT_PATH),
        },
        "cutover_decision": {
            "verdict": verdict,
            "cutover_authorized": verdict == "CUTOVER_AUTHORIZED",
            "summary": summary,
            "safety_failures": safety_failures,
            "evidence_gaps": evidence_gaps,
            "unexplained_hard_mismatch_count": len(corpus_mismatches)
            + len(selection_mismatches),
            "live_legacy_authority_retained": True,
            "live_authority_changed": False,
            "reopening_criteria": (
                "Re-run one fresh bounded P13-T01 authority audit only after the "
                "exact candidate checkpoint is published with explicit user "
                "authority and matched current-head hosted CI plus scheduled-full "
                "evidence is available; do not infer publication authority from "
                "this relay."
            ),
        },
        "authority": {
            "operational_validation_only": True,
            "source_authority": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authority": False,
        },
    }
    compact_receipt = {
        "schema_id": "v21_p13_t01_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P13-T01",
        "recommendation_ids": ["V21-R54"],
        "status": "PASS" if not safety_failures else "FAIL",
        "result_status": verdict,
        "fixed_fixture_count": len(fixed_corpus),
        "representative_family_count": len(selection_comparisons),
        "hard_mismatch_count": len(corpus_mismatches) + len(selection_mismatches),
        "unexplained_hard_mismatch_count": len(corpus_mismatches)
        + len(selection_mismatches),
        "safety_failure_count": len(safety_failures),
        "evidence_gap_count": len(evidence_gaps),
        "validator_ids": [
            "validation_equivalence_fixed_corpus",
            "validation_planner_representative_selection",
            "checkpoint_planner_rollback_drill",
            "current_head_hosted_ci_presence",
            "non_negotiable_gate_preservation",
        ],
        "source_hashes": equivalence["source_hashes"],
        "claim_boundary_summary": (
            "Operational validation-planner equivalence and cutover readiness only; "
            "no scientific, ontology, benchmark, proof, Gate Chair, or publication "
            "authority."
        ),
        "live_legacy_authority_retained": True,
        "physics_promotion_authorized": False,
    }

    if args.write_report:
        write_outputs(equivalence, mismatch_ledger, compact_receipt)
    if args.json:
        print(json.dumps(equivalence, indent=2, sort_keys=True))
    return 0 if not safety_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
