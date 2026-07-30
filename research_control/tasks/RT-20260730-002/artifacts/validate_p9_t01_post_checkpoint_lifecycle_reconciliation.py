#!/usr/bin/env python3
"""Validate the evidence-unique P9-T01 post-checkpoint lifecycle repair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260730-002/artifacts/"
    "p9_t01_post_checkpoint_lifecycle_reconciliation_receipt.json"
)
CHECKPOINT = "14a82f7be9762567359300c9082d3c5bc3d2ee3e"
CHECKPOINT_TREE = "add8aa8abc4ea37bb3f3871626a2ac32e2975c40"
CHECKPOINT_PARENT = "c65c2d40cff97ecd96de1c59bd220a9f1274dfc6"
OLD_COMPLETION = (
    "research_control/tasks/RT-20260730-001/jobs/completions/"
    "AJC-AJ-RT-20260730-001-001.yaml"
)
OLD_COMPLETION_SHA = "fcc1f5d90ee5b4c70293b1cf98e4fef92db542721bee847c14b7ec169978248a"
PROTOCOL = (
    "research_control/tasks/RT-20260729-012/artifacts/"
    "source_derived_benchmark_protocol_v1.tex"
)
PROTOCOL_SHA = "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007"
HANDOFF_0908_YAML_SHA = "6b690aa475ae901cb981eb2a444145db21c098d34ed88b77d78142835a40ff58"
HANDOFF_0908_MD_SHA = "d2edce09694674ffb5d716f89705b086613b3a3cc4b6dbb7d9962254f637c058"
HANDOFF_0909_YAML_SHA = "9168059352723b2d6d36b920e48d054c506563cac134aabf9050510ffe0b4a35"
HANDOFF_0909_MD_SHA = "9ec6f581009f9113e7ce397aade276a583583a2c3e477a0db21a45cf6aa88bbe"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: str) -> str:
    return sha256_bytes((ROOT / path).read_bytes())


def run(*args: str) -> str:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.strip()


def load_yaml(path: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def csv_row(path: str, key: str, value: str) -> dict[str, str]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"{path} expected one {key}={value} row, found {len(rows)}")
    return rows[0]


def status_paths() -> list[str]:
    lines = run("git", "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted(line[3:] for line in lines if len(line) >= 4)


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def expect(check_id: str, condition: bool, evidence: Any) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "evidence": evidence,
            }
        )

    resolved_checkpoint = run("git", "rev-parse", CHECKPOINT)
    checkpoint_tree = run("git", "rev-parse", f"{CHECKPOINT}^{{tree}}")
    checkpoint_parent = run("git", "rev-parse", f"{CHECKPOINT}^1")
    expect("checkpoint_identity", resolved_checkpoint == CHECKPOINT, resolved_checkpoint)
    expect("checkpoint_tree", checkpoint_tree == CHECKPOINT_TREE, checkpoint_tree)
    expect("checkpoint_parent", checkpoint_parent == CHECKPOINT_PARENT, checkpoint_parent)
    expect(
        "checkpoint_is_ancestor",
        run("git", "merge-base", "--is-ancestor", CHECKPOINT, "HEAD") == "",
        CHECKPOINT,
    )

    committed_completion = subprocess.run(
        ["git", "show", f"{CHECKPOINT}:{OLD_COMPLETION}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    expect(
        "checkpoint_contains_completion",
        sha256_bytes(committed_completion) == OLD_COMPLETION_SHA,
        sha256_bytes(committed_completion),
    )

    immutable_hashes = {
        OLD_COMPLETION: sha256_path(OLD_COMPLETION),
        PROTOCOL: sha256_path(PROTOCOL),
        "research_control/handoffs/handoff-0908.yaml": sha256_path(
            "research_control/handoffs/handoff-0908.yaml"
        ),
        "research_control/handoffs/handoff-0908.md": sha256_path(
            "research_control/handoffs/handoff-0908.md"
        ),
        "research_control/handoffs/handoff-0909.yaml": sha256_path(
            "research_control/handoffs/handoff-0909.yaml"
        ),
        "research_control/handoffs/handoff-0909.md": sha256_path(
            "research_control/handoffs/handoff-0909.md"
        ),
    }
    expected_immutable_hashes = {
        OLD_COMPLETION: OLD_COMPLETION_SHA,
        PROTOCOL: PROTOCOL_SHA,
        "research_control/handoffs/handoff-0908.yaml": HANDOFF_0908_YAML_SHA,
        "research_control/handoffs/handoff-0908.md": HANDOFF_0908_MD_SHA,
        "research_control/handoffs/handoff-0909.yaml": HANDOFF_0909_YAML_SHA,
        "research_control/handoffs/handoff-0909.md": HANDOFF_0909_MD_SHA,
    }
    expect(
        "immutable_predecessor_hashes",
        immutable_hashes == expected_immutable_hashes,
        immutable_hashes,
    )

    old_job = load_yaml(
        "research_control/tasks/RT-20260729-012/jobs/AJ-RT-20260729-012-001.yaml"
    )
    old_completion = load_yaml(
        "research_control/tasks/RT-20260729-012/jobs/completions/"
        "AJC-AJ-RT-20260729-012-001.yaml"
    )
    expect(
        "immutable_p9_t01_records_preserved",
        old_job.get("status") == "active"
        and old_completion.get("status") == "completed"
        and old_completion.get("validation_status") == "PASS",
        {
            "job_status": old_job.get("status"),
            "completion_status": old_completion.get("status"),
            "validation_status": old_completion.get("validation_status"),
        },
    )

    stale_row = csv_row(
        "registries/AGENT_JOB_REGISTRY.csv",
        "job_id",
        "AJ-RT-20260729-012-001",
    )
    new_job_row = csv_row(
        "registries/AGENT_JOB_REGISTRY.csv",
        "job_id",
        "AJ-RT-20260730-002-001",
    )
    new_task_row = csv_row(
        "registries/RESEARCH_TASK_REGISTRY.csv",
        "task_id",
        "RT-20260730-002",
    )
    expect(
        "registry_lifecycle_reconciled",
        stale_row.get("status") == "completed"
        and new_job_row.get("status") == "completed"
        and new_task_row.get("status") == "completed",
        {
            "stale_job_status": stale_row.get("status"),
            "new_job_status": new_job_row.get("status"),
            "new_task_status": new_task_row.get("status"),
        },
    )

    program = load_yaml("research_control/program_state.yaml")
    lifecycle = program.get("p9_t01_post_checkpoint_lifecycle_reconciliation", {})
    prior_recovery = program.get("p9_t01_handoff_identity_checkpoint_recovery", {})
    protocol_state = program.get("p9_t01_source_derived_benchmark_protocol", {})
    expect(
        "program_state_active_pointer",
        program.get("active_task_id") == "RT-20260730-002"
        and program.get("latest_handoff_id") == "handoff-0910"
        and program.get("next_plan_task_id") == "P9-T02",
        {
            "active_task_id": program.get("active_task_id"),
            "latest_handoff_id": program.get("latest_handoff_id"),
            "next_plan_task_id": program.get("next_plan_task_id"),
        },
    )
    expect(
        "program_state_checkpoint_truth",
        isinstance(lifecycle, dict)
        and lifecycle.get("reconciled_checkpoint_commit") == CHECKPOINT
        and lifecycle.get("p9_t02_executed") is False
        and isinstance(prior_recovery, dict)
        and prior_recovery.get("checkpoint_committed") is True
        and prior_recovery.get("checkpoint_commit_sha") == CHECKPOINT
        and isinstance(protocol_state, dict)
        and protocol_state.get("checkpoint_completed") is True
        and protocol_state.get("checkpoint_commit") == CHECKPOINT,
        {
            "lifecycle_checkpoint": lifecycle.get("reconciled_checkpoint_commit")
            if isinstance(lifecycle, dict)
            else None,
            "prior_checkpoint": prior_recovery.get("checkpoint_commit_sha")
            if isinstance(prior_recovery, dict)
            else None,
            "protocol_checkpoint": protocol_state.get("checkpoint_commit")
            if isinstance(protocol_state, dict)
            else None,
        },
    )

    handoff = load_yaml("research_control/handoffs/handoff-0910.yaml")
    expect(
        "handoff_0910_lifecycle",
        handoff.get("handoff_id") == "handoff-0910"
        and handoff.get("parent_handoff_id") == "handoff-0909"
        and handoff.get("reconciled_checkpoint_commit") == CHECKPOINT
        and handoff.get("plan_task_id") == "P9-T02"
        and handoff.get("p9_t02_executed") is False,
        {
            "handoff_id": handoff.get("handoff_id"),
            "parent_handoff_id": handoff.get("parent_handoff_id"),
            "reconciled_checkpoint_commit": handoff.get(
                "reconciled_checkpoint_commit"
            ),
            "p9_t02_executed": handoff.get("p9_t02_executed"),
        },
    )

    with (ROOT / "registries/AGENT_JOB_REGISTRY.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        pending_or_active_jobs = [
            row.get("job_id", "")
            for row in csv.DictReader(handle)
            if row.get("status") in {"pending", "active"}
        ]
    expect(
        "continuation_boundary_inputs",
        not pending_or_active_jobs
        and program.get("active_task_id") == "RT-20260730-002"
        and program.get("latest_handoff_id") == "handoff-0910",
        {
            "expected_boundary": "director_decision_required",
            "pending_or_active_job_ids": pending_or_active_jobs,
            "active_task_id": program.get("active_task_id"),
            "latest_handoff_id": program.get("latest_handoff_id"),
        },
    )

    changed = status_paths()
    forbidden_prefixes = (
        ".agents/roles/",
        ".codex/skills/",
        "implementations_plans/",
        "legacy_ontology/",
        "manuscripts/",
        "ontology/",
        "research_control/tasks/RT-20260729-012/",
        "research_control/tasks/RT-20260730-001/",
        "scripts/",
        "tests/",
    )
    forbidden_exact = {
        "research_control/handoffs/handoff-0908.md",
        "research_control/handoffs/handoff-0908.yaml",
        "research_control/handoffs/handoff-0909.md",
        "research_control/handoffs/handoff-0909.yaml",
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "registries/METRIC_USE_LEDGER.csv",
    }
    forbidden_changed = [
        path
        for path in changed
        if path in forbidden_exact or path.startswith(forbidden_prefixes)
    ]
    expect(
        "forbidden_paths_unchanged",
        not forbidden_changed,
        {"forbidden_changed": forbidden_changed},
    )

    errors = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "p9_t01_post_checkpoint_lifecycle_reconciliation_receipt_v1",
        "status": "PASS" if not errors else "FAIL",
        "strategy_id": "repair_p9_t01_post_checkpoint_lifecycle_and_activate_p9_t02_v1",
        "route_sha256": "0c3e04e946add84e44b6655cbe4091da99481b2041e219a0cf3dbae5e74ebeda",
        "checkpoint_commit": CHECKPOINT,
        "checkpoint_tree": CHECKPOINT_TREE,
        "checkpoint_parent": CHECKPOINT_PARENT,
        "immutable_predecessor_hashes": immutable_hashes,
        "check_count": len(checks),
        "error_count": len(errors),
        "checks": checks,
        "authority_limits": {
            "p9_t01_reexecuted": False,
            "p9_t02_executed": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authorized": False,
            "push_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def canonical_bytes(report: dict[str, Any]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    rendered = canonical_bytes(report)

    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_bytes(rendered)
    if args.check:
        if not REPORT_PATH.exists():
            report["status"] = "FAIL"
            report["error_count"] = int(report.get("error_count", 0)) + 1
            report["receipt_error"] = "receipt_missing"
        elif REPORT_PATH.read_bytes() != rendered:
            report["status"] = "FAIL"
            report["error_count"] = int(report.get("error_count", 0)) + 1
            report["receipt_error"] = "receipt_drift"

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
