#!/usr/bin/env python3
"""Validate and exercise the bounded P11-T04 execution-binding repair."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.project_control.classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.executor import execute_plan  # noqa: E402
from scripts.validation.plan import build_plan, load_manifest  # noqa: E402
from scripts.validation.run import DEFAULT_BINDINGS, load_adapters  # noqa: E402


TASK = ROOT / "research_control/tasks/RT-20260718-007"
REPORT_PATH = TASK / "artifacts/planner_execution_binding_report.json"
RECEIPT_PATH = TASK / "artifacts/planner_execution_binding_validation_receipt.json"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
RUNNER_PATH = ROOT / "scripts/validation/run.py"
PLAN_PATH = ROOT / "scripts/validation/plan.py"
PROFILES_PATH = ROOT / "scripts/validation/profiles.py"
EXECUTOR_PATH = ROOT / "scripts/validation/executor.py"
CHECKPOINT_PATH = ROOT / "scripts/research_control/checkpoint_research_transaction.py"
MAKEFILE_PATH = ROOT / "Makefile"
RECEIPT_ROOT = ROOT / ".local/v19_p11_t04_binding"
ALLOWED_MUTATION_GLOBS = (
    "FOLDER_MAP.md",
    "registries/**",
    "research_control/tasks/TASK_INDEX.csv",
    "research_control/tasks/TASK_INDEX.md",
    "output/research_dependency_graph.json",
    "output/research_dependency_graph.dot",
    "wiki/**",
    ".local/obsidian-vault/**",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*arguments: str, text: bool = True) -> str | bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return completed.stdout


def working_identity() -> str:
    digest = hashlib.sha256()
    digest.update(git("rev-parse", "HEAD").strip().encode("ascii"))
    digest.update(git("diff", "--binary", "HEAD", "--", text=False))
    raw_untracked = git("ls-files", "--others", "--exclude-standard", "-z", text=False)
    assert isinstance(raw_untracked, bytes)
    for raw_path in sorted(value for value in raw_untracked.split(b"\0") if value):
        path = ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        digest.update(raw_path)
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def changed_paths() -> list[str]:
    output = git("status", "--porcelain=v1")
    assert isinstance(output, str)
    paths: list[str] = []
    for line in output.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return sorted(paths)


def main() -> int:
    args = parse_args()
    live_manifest = load_manifest(MANIFEST_PATH)
    if (
        live_manifest.get("migration_epoch") != "shadow_planner"
        or live_manifest.get("execution_authority") != "legacy"
    ):
        raise SystemExit("live manifest authority changed outside this repair")

    live_plan = build_plan(
        live_manifest,
        classify_paths([]),
        profile="full",
        scopes=("repository",),
    )
    candidate_manifest = deepcopy(live_manifest)
    candidate_manifest["migration_epoch"] = "planner_authoritative"
    candidate_manifest["execution_authority"] = "manifest_planner"
    candidate_plan = build_plan(
        candidate_manifest,
        classify_paths([]),
        profile="full",
        scopes=("repository",),
    )
    adapters = load_adapters(DEFAULT_BINDINGS, candidate_manifest)
    gates = {
        str(gate["gate_id"]): gate
        for gate in candidate_manifest["gates"]
        if isinstance(gate, dict)
    }
    missing_bindings = [
        gate_id
        for gate_id in candidate_plan.selected_gate_ids
        if str(gates[gate_id]["adapter"]) not in adapters
    ]
    runner_text = RUNNER_PATH.read_text(encoding="utf-8")
    checkpoint_text = CHECKPOINT_PATH.read_text(encoding="utf-8")
    makefile_text = MAKEFILE_PATH.read_text(encoding="utf-8")
    static_checks = {
        "live_manifest_legacy": True,
        "candidate_plan_ready": candidate_plan.status == "READY",
        "candidate_planner_executes_commands": (
            candidate_plan.to_dict()["planner_executes_commands"] is True
        ),
        "candidate_legacy_result_not_authoritative": (
            candidate_plan.to_dict()["authority"]["legacy_result_authoritative"] is False
        ),
        "candidate_selection_matches_live": (
            candidate_plan.ordered_gate_ids == live_plan.ordered_gate_ids
        ),
        "binding_coverage_complete": not missing_bindings,
        "external_adapter_command_map_removed": "--adapter-commands" not in runner_text,
        "legacy_only_executor_rejection_removed": (
            "shadow executor requires legacy execution authority" not in runner_text
        ),
        "checkpoint_compare_default_retained": (
            'parser.set_defaults(validation_mode="compare")' in checkpoint_text
        ),
        "checkpoint_legacy_fallback_retained": "--legacy-validation" in checkpoint_text,
        "make_legacy_fallback_retained": "validate-project-control-legacy:" in makefile_text,
    }
    if not all(static_checks.values()):
        raise SystemExit(
            "static execution-binding checks failed: "
            + ", ".join(key for key, value in static_checks.items() if not value)
        )

    identity = working_identity()
    outcome = None
    if args.write_report:
        outcome = execute_plan(
            candidate_plan,
            candidate_manifest,
            adapters,
            receipt_root=RECEIPT_ROOT,
            max_workers=1,
            run_id=f"RUN-P11T04-{identity[:16]}",
            mutation_root=ROOT,
            allowed_mutation_globs=ALLOWED_MUTATION_GLOBS,
        )

    execution: dict[str, Any]
    if outcome is None:
        execution = {"status": "NOT_RUN", "exit_code": None}
    else:
        execution = {
            "status": outcome.status,
            "exit_code": outcome.exit_code,
            "receipt_path": (
                outcome.receipt_path.relative_to(ROOT).as_posix()
                if outcome.receipt_path is not None
                else None
            ),
            "receipt_sha256": (
                sha256(outcome.receipt_path)
                if outcome.receipt_path is not None
                else None
            ),
            "counts": outcome.receipt["counts"],
            "execution_authority": outcome.receipt["execution_authority"],
            "migration_epoch": outcome.receipt["migration_epoch"],
            "legacy_result_authoritative": outcome.receipt["authority"][
                "legacy_result_authoritative"
            ],
            "planner_result_authoritative": outcome.receipt["authority"][
                "planner_result_authoritative"
            ],
            "error": outcome.error,
        }

    status = (
        "PASS"
        if all(static_checks.values())
        and not missing_bindings
        and outcome is not None
        and outcome.status == "PASS"
        and outcome.exit_code == 0
        else "FAIL" if outcome is not None else "READY"
    )
    report: dict[str, Any] = {
        "schema_id": "v19_p11_t04_execution_binding_report_v1",
        "task_id": "RT-20260718-007",
        "job_id": "AJ-RT-20260718-007-001",
        "plan_task_id": "P11-T04",
        "status": status,
        "repository": {
            "root": ROOT.as_posix(),
            "head": git("rev-parse", "HEAD").strip(),
            "branch": git("branch", "--show-current").strip(),
            "working_identity_sha256": identity,
            "changed_paths": changed_paths(),
        },
        "source_hashes": {
            "live_manifest_sha256": sha256(MANIFEST_PATH),
            "adapter_bindings_sha256": sha256(DEFAULT_BINDINGS),
            "plan_sha256": sha256(PLAN_PATH),
            "profiles_sha256": sha256(PROFILES_PATH),
            "runner_sha256": sha256(RUNNER_PATH),
            "executor_sha256": sha256(EXECUTOR_PATH),
        },
        "live_state": {
            "migration_epoch": live_manifest["migration_epoch"],
            "execution_authority": live_manifest["execution_authority"],
            "planner_executes_commands": live_plan.to_dict()[
                "planner_executes_commands"
            ],
            "selected_gate_count": len(live_plan.selected_gate_ids),
        },
        "candidate_state": {
            "migration_epoch": candidate_manifest["migration_epoch"],
            "execution_authority": candidate_manifest["execution_authority"],
            "planner_executes_commands": candidate_plan.to_dict()[
                "planner_executes_commands"
            ],
            "selected_gate_count": len(candidate_plan.selected_gate_ids),
            "selected_gate_ids": list(candidate_plan.selected_gate_ids),
            "missing_binding_gate_ids": missing_bindings,
            "in_memory_only": True,
        },
        "static_checks": static_checks,
        "execution": execution,
        "remaining_cutover_evidence": {
            "live_manifest_cutover": "NOT_AUTHORIZED_IN_THIS_PACKET",
            "make_checkpoint_skill_ci_default_cutover": "NOT_AUTHORIZED_IN_THIS_PACKET",
            "hosted_ci_current_checkpoint": "PENDING_SEPARATE_PACKET",
            "p11_t05": "BLOCKED",
        },
        "authority": {
            "operational_validation_only": True,
            "live_legacy_execution_authoritative": True,
            "candidate_planner_execution_only": True,
            "legacy_fallback_retained": True,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_claim_authority": False,
            "proof_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "gate_chair_authority": False,
        },
        "next_route": (
            "After governed checkpoint PASS route one separately bounded P11-T04 "
            "hosted-CI and default-cutover evidence packet; P11-T05 remains blocked."
        ),
    }
    receipt = {
        "schema_id": "v19_p11_t04_execution_binding_validation_receipt_v1",
        "task_id": "RT-20260718-007",
        "job_id": "AJ-RT-20260718-007-001",
        "status": status,
        "static_check_count": len(static_checks),
        "static_check_pass_count": sum(static_checks.values()),
        "selected_gate_count": len(candidate_plan.selected_gate_ids),
        "missing_binding_count": len(missing_bindings),
        "candidate_execution_status": execution["status"],
        "live_authority_changed": False,
        "legacy_fallback_retained": True,
        "scientific_claims_changed": False,
    }
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        receipt["report_path"] = REPORT_PATH.relative_to(ROOT).as_posix()
        receipt["report_sha256"] = sha256(REPORT_PATH)
        RECEIPT_PATH.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status in {"PASS", "READY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
