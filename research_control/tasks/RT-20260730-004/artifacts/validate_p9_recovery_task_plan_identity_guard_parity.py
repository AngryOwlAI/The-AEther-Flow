#!/usr/bin/env python3
"""Validate the exact P9 recovery-task plan-identity and route-guard repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.ordinary_route_guard import (  # noqa: E402
    evaluate_research_handoff_guard,
)


REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260730-004/artifacts/"
    "p9_recovery_task_plan_identity_guard_parity_receipt.json"
)
TARGETS = {
    "research_control/tasks/RT-20260730-002/00_TASK.yaml": {
        "before": "28f794fa1b42daa976af4478b2006e23247f0c86f07b5982903b8b07b13124a0",
        "after": "6c06056bca781c7d197c2d7469cb9f3db88a366bba645448c2efc1749615221e",
    },
    "research_control/tasks/RT-20260730-003/00_TASK.yaml": {
        "before": "6de25c65f7009cd0566eefabd52ba8eb67270584f9cccabc2d5ab130afa491ec",
        "after": "4356cafade0ab6a868e04c6df560b2dd0dee9d5ae49049e93b09c2a46c444cfe",
    },
}
OLD_PAIR = (
    b'  plan_task_id: "P9-T02"\n'
    b'  recovery_for_plan_task_id: "P9-T01"\n'
)
NEW_PAIR = (
    b'  plan_task_id: "P9-T01"\n'
    b'  recovery_for_plan_task_id: "P9-T01"\n'
)
PROTECTED_HASHES = {
    "research_control/tasks/RT-20260729-012/jobs/"
    "AJ-RT-20260729-012-001.yaml":
        "c1444fb0cd15f4248c1f3886daab4fdfbe7f6f80dc4a42ead25af3e32a24848a",
    "research_control/tasks/RT-20260729-012/jobs/completions/"
    "AJC-AJ-RT-20260729-012-001.yaml":
        "645d5934a58ded9cafbbbd3af59ad9d3aa91efd5ec9bfe51ab231fd7488c07c4",
    "research_control/tasks/RT-20260729-012/artifacts/"
    "source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/tasks/RT-20260730-001/00_TASK.yaml":
        "1708e6eaf58dc98552ba83af7456be1afaf69f3c7e77168c874e1dead452ccdb",
    "research_control/tasks/RT-20260730-001/jobs/completions/"
    "AJC-AJ-RT-20260730-001-001.yaml":
        "fcc1f5d90ee5b4c70293b1cf98e4fef92db542721bee847c14b7ec169978248a",
    "research_control/tasks/RT-20260730-002/jobs/"
    "AJ-RT-20260730-002-001.yaml":
        "f00501e2277cb8f8df7efc3e3bfa3c7d5de7a29759176db3b478cf55dd498bb5",
    "research_control/tasks/RT-20260730-002/jobs/completions/"
    "AJC-AJ-RT-20260730-002-001.yaml":
        "13c0096045d19668b13abe1a4ca9c72ab042fb4f0fca7429ddfc8a3958815b8a",
    "research_control/tasks/RT-20260730-003/jobs/"
    "AJ-RT-20260730-003-001.yaml":
        "097d5923fce79627182e70a3fea6df59cf99d8cd889b324e9ce8162666a6653e",
    "research_control/tasks/RT-20260730-003/jobs/completions/"
    "AJC-AJ-RT-20260730-003-001.yaml":
        "e8560bb3be2696c4acd41c138741e320a557fe84b0a6e7d813bd86336ddcb6aa",
    "research_control/tasks/RT-20260730-003/artifacts/"
    "p9_t01_immutable_agentjob_status_parity_recovery_receipt.json":
        "8424a10dbac57f6d789d60b0dbdb16627d7d4e0bf905b1794dc36560771c2e9e",
    "research_control/tasks/RT-20260730-003/artifacts/"
    "validate_p9_t01_immutable_agentjob_status_parity_recovery.py":
        "6d39cd1d26407538243c219cebe3912650b866e3f9972ea7d72dbf6cab94fa3f",
    "research_control/tasks/RT-20260730-003/artifacts/"
    "validation_blocker_precheckpoint_recovery_task_plan_identity_guard_parity_v1.yaml":
        "94ae594123b13cd4a0bd9b2fc4804d8b0db7814a405cb9342e5832aad79b4637",
    "research_control/handoffs/handoff-0908.yaml":
        "6b690aa475ae901cb981eb2a444145db21c098d34ed88b77d78142835a40ff58",
    "research_control/handoffs/handoff-0908.md":
        "d2edce09694674ffb5d716f89705b086613b3a3cc4b6dbb7d9962254f637c058",
    "research_control/handoffs/handoff-0909.yaml":
        "9168059352723b2d6d36b920e48d054c506563cac134aabf9050510ffe0b4a35",
    "research_control/handoffs/handoff-0909.md":
        "9ec6f581009f9113e7ce397aade276a583583a2c3e477a0db21a45cf6aa88bbe",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def add_check(
    checks: list[dict[str, object]], name: str, ok: bool, detail: object
) -> None:
    checks.append(
        {
            "name": name,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, object]:
    checks: list[dict[str, object]] = []
    target_results: list[dict[str, object]] = []
    for relative, expected in TARGETS.items():
        current = (REPO_ROOT / relative).read_bytes()
        current_hash = sha256_bytes(current)
        reconstructed = current.replace(NEW_PAIR, OLD_PAIR, 1)
        reconstructed_hash = sha256_bytes(reconstructed)
        pair_count = current.count(NEW_PAIR)
        parsed = yaml.safe_load(current)
        plan = parsed.get("implementation_plan", {}) if isinstance(parsed, dict) else {}
        target_ok = (
            current_hash == expected["after"]
            and reconstructed_hash == expected["before"]
            and pair_count == 1
            and plan.get("plan_task_id") == "P9-T01"
            and plan.get("recovery_for_plan_task_id") == "P9-T01"
            and plan.get("next_plan_task_id") == "P9-T02"
        )
        add_check(
            checks,
            f"target_{Path(relative).parts[-2]}_{Path(relative).parts[-1]}",
            target_ok,
            {
                "path": relative,
                "after_sha256": current_hash,
                "reconstructed_before_sha256": reconstructed_hash,
                "new_pair_count": pair_count,
            },
        )
        target_results.append(
            {
                "path": relative,
                "sha256_before": expected["before"],
                "sha256_after": current_hash,
                "reconstructed_preimage_sha256": reconstructed_hash,
                "changed_field": "implementation_plan.plan_task_id",
                "value_before": "P9-T02",
                "value_after": "P9-T01",
            }
        )

    protected_mismatches: list[str] = []
    for relative, expected in PROTECTED_HASHES.items():
        actual = sha256_file(REPO_ROOT / relative)
        if actual != expected:
            protected_mismatches.append(f"{relative}:{actual}")
    add_check(
        checks,
        "protected_hashes",
        not protected_mismatches,
        "all exact" if not protected_mismatches else protected_mismatches,
    )

    handoff_path = REPO_ROOT / "research_control/handoffs/handoff-0911.yaml"
    handoff = yaml.safe_load(handoff_path.read_text(encoding="utf-8"))
    guard = evaluate_research_handoff_guard(handoff, REPO_ROOT)
    guard_ok = (
        guard.get("status") in {"PASS", "WARN"}
        and not guard.get("errors")
        and guard.get("observed_run_length") == 2
        and guard.get("ready_science_plan_task_ids") == ["P9-T02", "P14-T04"]
        and guard.get("selected_plan_task_id") == "P9-T02"
        and guard.get("expected_outcome") == "below_threshold"
    )
    add_check(checks, "handoff_0911_ordinary_route_guard", guard_ok, guard)

    status_repair_hash = sha256_file(
        REPO_ROOT
        / "research_control/tasks/RT-20260729-012/jobs/"
        "AJ-RT-20260729-012-001.yaml"
    )
    add_check(
        checks,
        "predecessor_status_repair_preserved",
        status_repair_hash
        == "c1444fb0cd15f4248c1f3886daab4fdfbe7f6f80dc4a42ead25af3e32a24848a",
        status_repair_hash,
    )

    state_text = (REPO_ROOT / "research_control/program_state.yaml").read_text(
        encoding="utf-8"
    )
    p9_t02_unexecuted = (
        "p9_t02_executed: true" not in state_text
        and "benchmark_case_executed: true" not in state_text
        and "executed_case_count: 1" not in state_text
    )
    add_check(
        checks,
        "p9_t02_unexecuted",
        p9_t02_unexecuted,
        "no P9-T02 or benchmark execution token is present",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p9_recovery_task_plan_identity_guard_parity_receipt_v1",
        "task_id": "RT-20260730-004",
        "job_id": "AJ-RT-20260730-004-001",
        "strategy_id": "repair_p9_recovery_task_plan_identity_and_ordinary_guard_parity_v1",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "error_count": len(failures),
        "target_path_count": len(TARGETS),
        "target_field_count": len(TARGETS),
        "targets": target_results,
        "protected_hash_count": len(PROTECTED_HASHES),
        "protected_hash_mismatch_count": len(protected_mismatches),
        "handoff_0911_sha256": sha256_file(handoff_path),
        "ready_science_plan_task_ids": guard.get(
            "ready_science_plan_task_ids", []
        ),
        "selected_plan_task_id": guard.get("selected_plan_task_id", ""),
        "p9_t01_reexecuted": False,
        "p9_t02_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.write_report == args.check:
        parser.error("choose exactly one of --write-report or --check")

    report = build_report()
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    elif not REPORT_PATH.exists():
        report["status"] = "FAIL"
        report["error_count"] = int(report["error_count"]) + 1
        report["checks"].append(
            {
                "name": "receipt_exists",
                "status": "FAIL",
                "detail": str(REPORT_PATH),
            }
        )
    else:
        expected = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if REPORT_PATH.read_text(encoding="utf-8") != expected:
            report["status"] = "FAIL"
            report["error_count"] = int(report["error_count"]) + 1
            report["checks"].append(
                {
                    "name": "receipt_fresh",
                    "status": "FAIL",
                    "detail": str(REPORT_PATH),
                }
            )

    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
