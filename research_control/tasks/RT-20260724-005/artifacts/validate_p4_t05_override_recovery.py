#!/usr/bin/env python3
"""Validate the exact P4-T05 protected-route admission recovery."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control.ordinary_route_guard import (  # noqa: E402
    evaluate_agent_job_route_admission,
)


TASK_ROOT = ROOT / "research_control/tasks/RT-20260724-005"
REPORT_PATH = TASK_ROOT / "artifacts/p4_t05_override_recovery_receipt.json"
PROTECTED_JOB_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-004/jobs/AJ-RT-20260724-004-001.yaml"
)
RECOVERY_JOB_PATH = TASK_ROOT / "jobs/AJ-RT-20260724-005-001.yaml"
FIXED_ACTIVATED_PATHS = {
    "approval": (
        "research_control/approvals/approval-20260724-001.yaml",
        "37038157b5deb23a3ae8249dcf5562ac8e9be37f6fa4ae8704c47b0eeb24a412",
    ),
    "protected_ddr": (
        "research_control/tasks/RT-20260724-004/DDR-20260724-004.md",
        "5b262a37de7b37b2244bc112584d1321807ebb5d9ca46907d897e5e4689fb24e",
    ),
    "protected_job": (
        "research_control/tasks/RT-20260724-004/jobs/AJ-RT-20260724-004-001.yaml",
        "835b97cf022fb8ce5845467d6703b0d3e6dc167b0f7ffff5706c8c4a6bd2decd",
    ),
    "protected_completion": (
        "research_control/tasks/RT-20260724-004/jobs/completions/AJC-AJ-RT-20260724-004-001.yaml",
        "d248a2abfe6a2571b7ebb6a930c720f64af7f3d39cdf0e497a5e194308a055bf",
    ),
    "source_handoff": (
        "research_control/handoffs/handoff-0853.yaml",
        "c231cdfc621a809d95069e9889d87bfcb7c9c4807576ba0c6407b7c83cc8d0a4",
    ),
    "blocked_handoff": (
        "research_control/handoffs/handoff-0854.yaml",
        "19be01044894e6611cf11d8f7ce91cbff04a93e0bd88f8a6d353eca7fbf4acda",
    ),
    "blocker": (
        "research_control/tasks/RT-20260724-004/artifacts/validation_blocker_ordinary_route_human_override_admission_v1.yaml",
        "54f12b8a481253b2482f2525573c09213fbf72d121c75d04ef630abd22c3db4c",
    ),
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def check(checks: list[dict[str, Any]], check_id: str, condition: bool, detail: str) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, Any]:
    protected_job = load_mapping(PROTECTED_JOB_PATH)
    recovery_job = load_mapping(RECOVERY_JOB_PATH)
    protected_result = evaluate_agent_job_route_admission(
        protected_job,
        created_at=str(protected_job["created_at"]),
        repo_root=ROOT,
    )
    recovery_result = evaluate_agent_job_route_admission(
        recovery_job,
        created_at=str(recovery_job["created_at"]),
        repo_root=ROOT,
    )
    no_override_job = copy.deepcopy(protected_job)
    no_override_job["ordinary_route_guard_admission"].pop("override_authority")
    no_override_result = evaluate_agent_job_route_admission(
        no_override_job,
        created_at=str(no_override_job["created_at"]),
        repo_root=ROOT,
    )

    checks: list[dict[str, Any]] = []
    check(
        checks,
        "protected_execution_exact_chain",
        protected_result["status"] == "PASS" and not protected_result["errors"],
        json.dumps(protected_result, sort_keys=True),
    )
    check(
        checks,
        "checkpoint_recovery_exact_chain",
        recovery_result["status"] == "PASS" and not recovery_result["errors"],
        json.dumps(recovery_result, sort_keys=True),
    )
    check(
        checks,
        "ordinary_equality_without_override",
        "job_plan_task_id_not_selected_by_handoff" in no_override_result["errors"],
        json.dumps(no_override_result, sort_keys=True),
    )
    for label, (relative, expected) in FIXED_ACTIVATED_PATHS.items():
        observed = sha256_path(ROOT / relative)
        check(
            checks,
            f"fixed_activated_hash_{label}",
            observed == expected,
            f"{relative} expected={expected} observed={observed}",
        )

    source_hashes = {
        "evaluator": sha256_path(
            ROOT / "scripts/research_control/ordinary_route_guard.py"
        ),
        "focused_tests": sha256_path(ROOT / "tests/test_ordinary_route_guard.py"),
        "agent_job_schema": sha256_path(
            ROOT / ".agents/schemas/AGENT_JOB_SCHEMA.md"
        ),
        "ordinary_route_policy": sha256_path(
            ROOT
            / "research_control/tasks/RT-20260722-015/artifacts/"
            "ordinary_route_guard_policy_v1.md"
        ),
        "protected_execution_receipt": sha256_path(
            ROOT
            / "research_control/tasks/RT-20260724-004/artifacts/"
            "protected_human_route_override_admission_v1.yaml"
        ),
        "checkpoint_recovery_receipt": sha256_path(
            TASK_ROOT
            / "artifacts/protected_human_route_override_admission_v1.yaml"
        ),
    }
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p4_t05_protected_human_override_recovery_receipt_v1",
        "task_id": "RT-20260724-005",
        "job_id": "AJ-RT-20260724-005-001",
        "generated_at": "2026-07-24T16:09:13Z",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "source_hashes": source_hashes,
        "focused_regression_count": 20,
        "protected_job_mutated": False,
        "protected_completion_mutated": False,
        "approval_reused": False,
        "p4_t05_gate_reexecuted": False,
        "p4_t06_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def serialized(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    content = serialized(report)
    if args.write_report:
        REPORT_PATH.write_text(content, encoding="utf-8")
    matches = not args.check or (
        REPORT_PATH.is_file()
        and REPORT_PATH.read_text(encoding="utf-8") == content
    )
    output = {
        "status": report["status"] if matches else "FAIL",
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "failure_count": report["failure_count"],
        "report_matches": matches,
    }
    print(json.dumps(output, indent=2, sort_keys=True) if args.json else output["status"])
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
