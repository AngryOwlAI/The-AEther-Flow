#!/usr/bin/env python3
"""Validate the sealed P9-T08 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260731-002"
JOB_ID = "AJ-RT-20260731-002-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 186
ROUTE_SHA256 = "853cd2622d61fcb4b8ba3384d0c6613c9df49a9ca9a24e65377aafbb355d8e55"
DIRTY_MANIFEST_SHA256 = (
    "09e9a26758752e70a8cbd22cf16b8fcd7f0dc01e3ea0da103e51fcda7a4f46c2"
)
BLOCKER_SHA256 = (
    "26c0d92e777824d5ab2ce3100947a0a84da99d121b0f9065f4dea8fb8ca8b575"
)
SOURCE_HEAD = "536a7cf43a28923dea1a2ab4faed8822618326b3"
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
BLOCKER_PATH = (
    ROOT
    / "research_control/tasks/RT-20260731-001/artifacts/"
    "validation_blocker_checkpoint_p9_t08_blank_eof_v1.yaml"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260731-002/artifacts/"
    "p9_t08_eof_checkpoint_recovery_receipt.json"
)
COMPACT_RECEIPT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_benchmark_audit_compact_receipt_v1.json"
)
GATE_E_MATRIX_PATH = (
    ROOT
    / "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_gate_e_readiness_matrix_v1.yaml"
)
REPLICATION_PATH = (
    ROOT
    / "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_independent_replication_status_v1.yaml"
)

REPAIR_PATHS = (
    "research_control/tasks/RT-20260731-001/artifacts/"
    "child_phys_math_p9_t08_benchmark_audit.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "child_phys_phil_p9_t08_benchmark_audit.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_benchmark_audit_compact_receipt_v1.json",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_benchmark_audit_receipt.md",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_benchmark_smuggling_audit_v1.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_benchmark_suite_red_team_review_v1.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_cross_case_assumption_consistency_v1.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_gate_e_readiness_matrix_v1.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "p9_t08_independent_replication_status_v1.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "parent_conflict_review_p9_t08_benchmark_audit.yaml",
    "research_control/tasks/RT-20260731-001/artifacts/"
    "parent_fusion_notes_p9_t08_benchmark_audit.md",
)
ALREADY_NORMALIZED_PATHS = (
    "research_control/handoffs/handoff-0923.md",
    "research_control/tasks/RT-20260731-001/00_TASK.yaml",
    "research_control/tasks/RT-20260731-001/DDR-20260731-001.md",
    "research_control/tasks/RT-20260731-001/jobs/AJ-RT-20260731-001-001.yaml",
)
ORIGINAL_FINDING_PATHS = frozenset(REPAIR_PATHS + ALREADY_NORMALIZED_PATHS)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return payload


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def load_goal() -> dict[str, Any]:
    text = GOAL_PATH.read_text(encoding="utf-8")
    frontmatter, _ = text[4:].split("\n---\n", 1)
    payload = yaml.safe_load(frontmatter)
    if not isinstance(payload, dict):
        raise ValueError("goal frontmatter is not a mapping")
    return payload


def recovery_route(goal: dict[str, Any]) -> dict[str, Any]:
    for entry in goal.get("recovery_ledger", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("approved_for_generation") != GENERATION:
            continue
        route = entry.get("route")
        if isinstance(route, dict):
            return route
    raise ValueError("generation-186 recovery route is missing")


def ends_with_exactly_one_lf(data: bytes) -> bool:
    return data.endswith(b"\n") and not data.endswith(b"\n\n")


def blank_eof_check(relative: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "git",
            "diff",
            "--no-index",
            "--check",
            "--",
            "/dev/null",
            relative,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    clean = (
        completed.returncode in (0, 1)
        and "new blank line at EOF" not in output
        and "trailing whitespace" not in output
    )
    return {
        "returncode": completed.returncode,
        "blank_eof_clean": clean,
        "diagnostic": output.strip(),
    }


def science_boundary_checks() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    compact = load_json(COMPACT_RECEIPT_PATH)
    matrix = load_yaml(GATE_E_MATRIX_PATH)
    replication = load_yaml(REPLICATION_PATH)

    case_outcomes = matrix.get("case_outcomes", {})
    all_six_inconclusive = (
        isinstance(case_outcomes, dict)
        and set(case_outcomes) == {
            "P9-T02",
            "P9-T03",
            "P9-T04",
            "P9-T05",
            "P9-T06",
            "P9-T07",
        }
        and set(case_outcomes.values()) == {"INCONCLUSIVE"}
    )
    zero_benchmark_passes = (
        compact.get("benchmark_pass_count") == 0
        and compact.get("inconclusive_case_count") == 6
        and compact.get("executed_case_count") == 6
        and matrix.get("counts", {}).get("passed_case_count") == 0
    )
    no_qualifying_replication = (
        compact.get("qualifying_independent_replication_completed") is False
        and compact.get("independent_replication_count") == 0
        and replication.get("qualifying_independent_replication_completed") is False
        and replication.get("status") == "NOT_ACQUIRED"
    )
    gate_e_not_ready = (
        compact.get("gate_e_readiness")
        == "NOT_READY_NO_BENCHMARK_PASS_NO_QUALIFYING_INDEPENDENT_REPLICATION"
        and compact.get("gate_e_verdict_issued") is False
        and matrix.get("overall_readiness")
        == "NOT_READY_NO_BENCHMARK_PASS_NO_QUALIFYING_INDEPENDENT_REPLICATION"
        and matrix.get("authority_limits", {}).get("Gate_E_verdict_issued") is False
    )
    no_promotion = (
        compact.get("physics_promotion_authorized") is False
        and matrix.get("authority_limits", {}).get("benchmark_promotion_authorized")
        is False
        and matrix.get("authority_limits", {}).get("physics_promotion_authorized")
        is False
    )

    checks = {
        "all_six_cases_inconclusive": all_six_inconclusive,
        "zero_benchmark_passes": zero_benchmark_passes,
        "qualifying_independent_replication_absent": no_qualifying_replication,
        "gate_e_not_ready_and_no_verdict": gate_e_not_ready,
        "benchmark_and_physics_promotion_unauthorized": no_promotion,
    }
    for name, passed in checks.items():
        if not passed:
            errors.append(f"science boundary check failed: {name}")
    return checks, errors


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    route = recovery_route(load_goal())
    manifest = route.get("dirty_state_manifest", {})
    manifest_entries = manifest.get("changed_paths", [])
    manifest_by_path = {
        str(item["path"]): str(item["sha256"])
        for item in manifest_entries
        if isinstance(item, dict) and item.get("path") and item.get("sha256")
    }

    if canonical_sha256(route) != ROUTE_SHA256:
        errors.append("immutable route canonical hash mismatch")
    if canonical_sha256(manifest) != DIRTY_MANIFEST_SHA256:
        errors.append("dirty manifest canonical hash mismatch")
    if route.get("worker_skill") != "improve-project-system":
        errors.append("immutable route worker mismatch")
    if route.get("work_item_id") != "P9-T08":
        errors.append("immutable route work-item mismatch")
    if manifest.get("head") != SOURCE_HEAD:
        errors.append("sealed manifest head mismatch")
    if manifest.get("owning_task_id") != "RT-20260731-001":
        errors.append("sealed manifest task owner mismatch")
    if manifest.get("owning_agent_job_id") != "AJ-RT-20260731-001-001":
        errors.append("sealed manifest job owner mismatch")
    if len(manifest_by_path) != 62:
        errors.append(f"expected 62 manifest paths, observed {len(manifest_by_path)}")

    blocker = load_yaml(BLOCKER_PATH)
    blocker_findings = blocker.get("findings", [])
    blocker_by_path = {
        str(item["path"]): str(item["sha256"])
        for item in blocker_findings
        if isinstance(item, dict) and item.get("path") and item.get("sha256")
    }
    if sha256(BLOCKER_PATH) != BLOCKER_SHA256:
        errors.append("tracked blocker hash mismatch")
    if set(blocker_by_path) != ORIGINAL_FINDING_PATHS:
        errors.append("blocker finding path set mismatch")
    if any(
        item.get("finding") != "new blank line at EOF"
        for item in blocker_findings
        if isinstance(item, dict)
    ):
        errors.append("blocker contains a non-EOF finding")

    repair_checks: dict[str, Any] = {}
    for relative in REPAIR_PATHS:
        sealed_before = manifest_by_path.get(relative, "")
        blocker_before = blocker_by_path.get(relative, "")
        live_data = (ROOT / relative).read_bytes()
        live_after = sha256_bytes(live_data)
        exact = (
            sealed_before == blocker_before
            and ends_with_exactly_one_lf(live_data)
            and sha256_bytes(live_data + b"\n") == sealed_before
        )
        whitespace = blank_eof_check(relative)
        repair_checks[relative] = {
            "sealed_before_sha256": sealed_before,
            "blocker_before_sha256": blocker_before,
            "live_after_sha256": live_after,
            "exactly_one_final_lf_removed": exact,
            "ends_with_exactly_one_lf": ends_with_exactly_one_lf(live_data),
            "git_whitespace_check": whitespace,
        }
        if not exact:
            errors.append(f"not an exact one-LF deletion: {relative}")
        if not whitespace["blank_eof_clean"]:
            errors.append(f"Git EOF whitespace check failed: {relative}")

    normalized_checks: dict[str, Any] = {}
    for relative in ALREADY_NORMALIZED_PATHS:
        sealed = manifest_by_path.get(relative, "")
        blocker_before = blocker_by_path.get(relative, "")
        live_data = (ROOT / relative).read_bytes()
        live_hash = sha256_bytes(live_data)
        exact = (
            bool(sealed)
            and sealed != blocker_before
            and live_hash == sealed
            and ends_with_exactly_one_lf(live_data)
        )
        whitespace = blank_eof_check(relative)
        normalized_checks[relative] = {
            "blocker_before_sha256": blocker_before,
            "sealed_normalized_sha256": sealed,
            "live_sha256": live_hash,
            "preserved_from_sealed_manifest": exact,
            "ends_with_exactly_one_lf": ends_with_exactly_one_lf(live_data),
            "git_whitespace_check": whitespace,
        }
        if not exact:
            errors.append(f"already-normalized path drifted: {relative}")
        if not whitespace["blank_eof_clean"]:
            errors.append(f"Git EOF whitespace check failed: {relative}")

    non_finding_paths = sorted(set(manifest_by_path) - ORIGINAL_FINDING_PATHS)
    non_finding_mismatches: list[str] = []
    for relative in non_finding_paths:
        live_path = ROOT / relative
        if not live_path.is_file() or sha256(live_path) != manifest_by_path[relative]:
            non_finding_mismatches.append(relative)
    if len(non_finding_paths) != 47:
        errors.append(
            f"expected 47 non-finding manifest paths, observed {len(non_finding_paths)}"
        )
    if non_finding_mismatches:
        errors.append(
            f"{len(non_finding_mismatches)} non-finding manifest paths changed"
        )

    science_checks, science_errors = science_boundary_checks()
    errors.extend(science_errors)

    return {
        "schema_id": "p9_t08_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": "repair_rt_20260731_001_blank_eof_and_checkpoint_v1",
        "route_sha256": ROUTE_SHA256,
        "dirty_state_manifest_sha256": DIRTY_MANIFEST_SHA256,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260731-001",
        "source_job_id": "AJ-RT-20260731-001-001",
        "source_handoff_id": "handoff-0923",
        "checks": {
            "manifest_path_count": len(manifest_by_path),
            "original_finding_path_count": len(ORIGINAL_FINDING_PATHS),
            "remaining_repair_path_count": len(REPAIR_PATHS),
            "already_normalized_path_count": len(ALREADY_NORMALIZED_PATHS),
            "non_finding_manifest_path_count": len(non_finding_paths),
            "non_finding_hash_mismatch_count": len(non_finding_mismatches),
            "non_finding_hash_mismatches": non_finding_mismatches,
            "repair_paths": repair_checks,
            "already_normalized_paths": normalized_checks,
            "science_boundary": science_checks,
            "p9_t08_reexecuted": False,
            "p9_t09_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "scientific_audit_disposition_preserved": True,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "benchmark_or_physics_promotion_authorized_by_recovery": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p9_t09_executed": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def check_sealed_report() -> dict[str, Any]:
    errors: list[str] = []
    report = load_json(REPORT_PATH)
    checks = report.get("checks", {})
    if report.get("validation_status") != "PASS":
        errors.append("sealed recovery receipt is not PASS")
    if report.get("route_sha256") != ROUTE_SHA256:
        errors.append("sealed recovery receipt route hash mismatch")
    if checks.get("manifest_path_count") != 62:
        errors.append("sealed recovery receipt manifest count mismatch")
    if checks.get("original_finding_path_count") != 15:
        errors.append("sealed recovery receipt finding count mismatch")
    if checks.get("remaining_repair_path_count") != 11:
        errors.append("sealed recovery receipt repair count mismatch")
    if checks.get("already_normalized_path_count") != 4:
        errors.append("sealed recovery receipt normalized count mismatch")
    if checks.get("non_finding_manifest_path_count") != 47:
        errors.append("sealed recovery receipt non-finding count mismatch")
    if checks.get("non_finding_hash_mismatch_count") != 0:
        errors.append("sealed recovery receipt records non-finding drift")

    live_repair_checks: dict[str, Any] = {}
    sealed_repairs = checks.get("repair_paths", {})
    for relative in REPAIR_PATHS:
        expected_after = sealed_repairs.get(relative, {}).get("live_after_sha256")
        live_data = (ROOT / relative).read_bytes()
        live_hash = sha256_bytes(live_data)
        match = (
            bool(expected_after)
            and live_hash == expected_after
            and ends_with_exactly_one_lf(live_data)
        )
        whitespace = blank_eof_check(relative)
        live_repair_checks[relative] = {
            "expected_after_sha256": expected_after,
            "live_sha256": live_hash,
            "match": match,
            "git_whitespace_check": whitespace,
        }
        if not match:
            errors.append(f"live repaired path hash mismatch: {relative}")
        if not whitespace["blank_eof_clean"]:
            errors.append(f"live repaired path Git check failed: {relative}")

    live_normalized_checks: dict[str, Any] = {}
    sealed_normalized = checks.get("already_normalized_paths", {})
    for relative in ALREADY_NORMALIZED_PATHS:
        expected = sealed_normalized.get(relative, {}).get(
            "sealed_normalized_sha256"
        )
        live_data = (ROOT / relative).read_bytes()
        live_hash = sha256_bytes(live_data)
        match = bool(expected) and live_hash == expected
        whitespace = blank_eof_check(relative)
        live_normalized_checks[relative] = {
            "expected_sha256": expected,
            "live_sha256": live_hash,
            "match": match,
            "git_whitespace_check": whitespace,
        }
        if not match:
            errors.append(f"live already-normalized path drifted: {relative}")
        if not whitespace["blank_eof_clean"]:
            errors.append(f"live normalized path Git check failed: {relative}")

    science_checks, science_errors = science_boundary_checks()
    errors.extend(science_errors)

    return {
        "schema_id": "p9_t08_eof_checkpoint_recovery_check_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "sealed_receipt_sha256": sha256(REPORT_PATH),
        "live_repair_checks": live_repair_checks,
        "live_already_normalized_checks": live_normalized_checks,
        "science_boundary": science_checks,
        "p9_t08_reexecuted": False,
        "p9_t09_executed": False,
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = check_sealed_report() if args.check else build_report()
    if args.write_report and not args.check:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
