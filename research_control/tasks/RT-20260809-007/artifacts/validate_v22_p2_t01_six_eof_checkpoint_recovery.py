#!/usr/bin/env python3
"""Validate the sealed six-file V22 P2-T01 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-007"
JOB_ID = "AJ-RT-20260809-007-001"
STRATEGY_ID = "repair_v22_p2_t01_six_eof_blank_lines_and_checkpoint_v1"
ROUTE_SHA256 = "bab376964ce0d88d4470a384804b0928a509a54037d87123cbbb604ef5265423"
BLOCKER_FINGERPRINT = "6a1aa4e2017c9234336df5ee89f3c54ffbde4935c21747ab93415300b2ce81c0"
MANIFEST_SHA256 = "1eba401f33257fca514ba9d656a63e87c816d9d6bbbf0eeda0fe87cbca17880b"
SOURCE_HEAD = "b1dd6195bb963ab02780e24c089d545cb8319cee"
SOURCE_TREE = "a01412cb5aee3a6ddc36948085393887caf1560d"
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-007"
MANIFEST_PATH = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p2_t01_six_eof_checkpoint.txt"
REPORT_PATH = TASK_DIR / "artifacts/v22_p2_t01_six_eof_checkpoint_recovery_receipt.json"
VALIDATION_PATH = TASK_DIR / "artifacts/v22_p2_t01_six_eof_checkpoint_recovery_validation.json"
CHECKPOINT_RECEIPT_PATH = ROOT / ".local/validation-receipts/901a09745e55e09d87397b94e710070f3d3bb2ed04e40d1e6379ff0963f36640/RUN-CHECKPOINT-35d67803fd0a382a/receipt.json"
FAILED_OUTPUT_PATH = ROOT / ".local/validation-receipts/901a09745e55e09d87397b94e710070f3d3bb2ed04e40d1e6379ff0963f36640/RUN-CHECKPOINT-35d67803fd0a382a/gates/0007-git_diff_check.stdout"
CHECKPOINT_RECEIPT_SHA256 = "d13ac85c59e86740ddda449c8b2115400a19262b797b647fe45b894aecba8224"
FAILED_OUTPUT_SHA256 = "cc46688a30de7d7565c6461c5a7cbe6165a15e9db4976cbf766adbe026cb9147"

TARGETS = {
    "research_control/tasks/RT-20260809-005/artifacts/child_phys_math_p2_t01_capacity_theorem.yaml": (
        "424bee951281caf3eb0d1b5a05de5039050e1c73b90c02e3f799327cd9e6bace",
        "992561f9d7ea96cd099d57113cb529bbaa01b68cf1fb4a6576ef189a43bb0c6e",
    ),
    "research_control/tasks/RT-20260809-005/artifacts/child_refuter_p2_t01_scope_audit.yaml": (
        "09a4e6243ca09a8bfe6c4347cd117ac4daba2a4778236554d5570ea95a68d073",
        "f1efdcc0d37900fdf736df20603dd0423d3b30c799ddaac05e6b6e5b8b7cec12",
    ),
    "research_control/tasks/RT-20260809-005/artifacts/parent_conflict_review_p2_t01_capacity.yaml": (
        "2827d9141f8299c9c7278c515622d3e86369227b485de877ee86bb759859f332",
        "64fade66b2c5716e9f5fdab2420448f198c470918ed0116731458d3263a3cf24",
    ),
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_local_state_quotient_definitions_v1.yaml": (
        "eaa545786e17f0b143e29d9c4c29e1d72e0874ac6441734d1cf5b9634ccea668",
        "27678adff2559c2a94725531944110e4cbb4496b94337860516b8dcac4e9c5d5",
    ),
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_proof_countermodel_archive_v1.yaml": (
        "0e1c4c809177dd7e0818cdc1652e4ae2d566eaf6292a663c4e32df99ea052bcb",
        "28967cd57a833c83ad0855787a6313a07c5bcee68cc95b4d864220fc9fc05c21",
    ),
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_source_adequacy_checklist_v1.yaml": (
        "9b64aee79729c6a7ca83fc94f38cd6ff2fc4eedf93b32d7ee3a345a09b0fb4a0",
        "a9b59df7b5b2d1203fef53cf23817400c6d1511836e97ff1ae21b819dc064e68",
    ),
}

PROTECTED_LIVE_PATHS = {
    "research_control/design/validation_obligation_resolution_policy_v1.md": "baea9d8b4b67c4c8bceb73da34dfbc562fe285c087992198295a177058c4cfc2",
    "research_control/design/v22_recommendation_backlog.yaml": "d7d33ad808cded6cb429d6bc4ead72c4e1593550f24eb4ff67d11f1f539f6d58",
    "research_control/handoffs/handoff-0975.yaml": "5d0a708da483f567d7329a9f0c4623192ab3095663062a8f47cb2f8726fa595d",
    "research_control/handoffs/handoff-0976.yaml": "b93b803dd98303f658aad29bdde9410aacaa75dc2a1bea3a8031160ffe45670d",
    "research_control/tasks/RT-20260804-001/00_TASK.yaml": "4e86172a58d0d82676ef5a94612402938c04a0e7927a43fb09501b13f526a88d",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_local_source_information_capacity_theorem_v1.tex": "2ba813e4e961b9ea2709a31c6e06152b1cb4d50ebd90185c2ed93d7aeb132439",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_capacity_validation.json": "0f5400de250218eca95d5c78ff2b4a8e062bd41f08eee93f581156ae9c708d4f",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_compact_receipt.json": "330d1f1982b4cd6e1d3861c20cfdbbc858baaadff642ec586a45552902dd9663",
    "research_control/tasks/RT-20260809-005/jobs/completions/AJC-AJ-RT-20260809-005-001.yaml": "087086ab7b5840209601794e9b66d0c29d466bbc65e05b22490a786760ea0d5d",
    "research_control/tasks/RT-20260809-006/jobs/completions/AJC-AJ-RT-20260809-006-001.yaml": "1716a7c978a5cf685266ca2899cf4459ae9d767583c832b858d82ad72e0c9907",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def load_manifest() -> tuple[list[str], dict[str, str]]:
    lines = [line for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines() if line]
    rows: dict[str, str] = {}
    for line in lines:
        relative, digest = line.rsplit("=", 1)
        rows[relative] = digest
    return lines, rows


def checkpoint_evidence_errors() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    receipt_hash = sha256_path(CHECKPOINT_RECEIPT_PATH)
    output_hash = sha256_path(FAILED_OUTPUT_PATH)
    if receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("checkpoint receipt hash mismatch")
    if output_hash != FAILED_OUTPUT_SHA256:
        errors.append("failed git-diff output hash mismatch")
    receipt = json.loads(CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8"))
    failed_gate = next(
        (item for item in receipt.get("gate_results", []) if item.get("gate_id") == "git_diff_check"),
        {},
    )
    if receipt.get("status") != "FAIL" or receipt.get("exit_code") != 1:
        errors.append("checkpoint receipt does not record the expected failure")
    if failed_gate.get("status") != "FAIL" or failed_gate.get("exit_code") != 2:
        errors.append("git_diff_check gate does not record the expected return code")
    output_lines = [line for line in FAILED_OUTPUT_PATH.read_text(encoding="utf-8").splitlines() if line]
    if len(output_lines) != len(TARGETS):
        errors.append(f"expected six git-diff findings, observed {len(output_lines)}")
    for relative in TARGETS:
        matches = [line for line in output_lines if line.startswith(f"{relative}:") and line.endswith("new blank line at EOF.")]
        if len(matches) != 1:
            errors.append(f"checkpoint output does not name exactly one EOF finding for {relative}")
    return errors, {
        "receipt_sha256": receipt_hash,
        "failed_output_sha256": output_hash,
        "failed_gate_status": failed_gate.get("status"),
        "failed_gate_exit_code": failed_gate.get("exit_code"),
        "finding_count": len(output_lines),
    }


def build_boundary_receipt() -> dict[str, Any]:
    errors: list[str] = []
    manifest_lines, manifest = load_manifest()
    manifest_hash = sha256_path(MANIFEST_PATH)
    if manifest_hash != MANIFEST_SHA256:
        errors.append("inherited dirty manifest hash mismatch")
    if len(manifest_lines) != 76 or len(manifest) != 76:
        errors.append(f"expected 76 unique manifest paths, observed {len(manifest)}")
    if manifest_lines != sorted(manifest_lines):
        errors.append("inherited dirty manifest is not sorted")
    if set(TARGETS) - set(manifest):
        errors.append("one or more EOF targets are absent from the inherited manifest")

    target_checks: dict[str, Any] = {}
    non_target_mismatches: list[str] = []
    for relative, expected_before in manifest.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"manifest path missing: {relative}")
            continue
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if relative in TARGETS:
            declared_before, expected_after = TARGETS[relative]
            exact_one_newline_removed = (
                expected_before == declared_before
                and observed == expected_after
                and data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected_before
            )
            parsed = yaml.safe_load(data.decode("utf-8"))
            target_checks[relative] = {
                "before_sha256": expected_before,
                "after_sha256": observed,
                "byte_delta": 1,
                "yaml_parses": parsed is not None,
                "ends_with_exactly_one_newline": data.endswith(b"\n") and not data.endswith(b"\n\n"),
                "exact_one_final_newline_removed": exact_one_newline_removed,
            }
            if not exact_one_newline_removed:
                errors.append(f"target is not the exact required one-newline deletion: {relative}")
        elif observed != expected_before:
            non_target_mismatches.append(relative)
    if non_target_mismatches:
        errors.append(f"{len(non_target_mismatches)} non-target inherited paths changed before sealing")

    evidence_errors, checkpoint_evidence = checkpoint_evidence_errors()
    errors.extend(evidence_errors)
    protected_checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256_path(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": match}
        if not match:
            errors.append(f"protected P2-T01 hash mismatch: {relative}")

    head = git("rev-parse", "HEAD").stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD:
        errors.append("source HEAD changed before recovery checkpoint")
    if tree != SOURCE_TREE:
        errors.append("source tree changed before recovery checkpoint")
    if not index_clean:
        errors.append("Git index is not clean at the repair boundary")

    return {
        "schema_id": "v22_p2_t01_six_eof_checkpoint_recovery_receipt_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "route_blocker_fingerprint": BLOCKER_FINGERPRINT,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "source_task_id": "RT-20260809-006",
        "source_job_id": "AJ-RT-20260809-006-001",
        "source_handoff_id": "handoff-0976",
        "inherited_manifest": {
            "path": str(MANIFEST_PATH.relative_to(ROOT)),
            "sha256": manifest_hash,
            "path_count": len(manifest),
            "target_path_count": len(TARGETS),
            "non_target_path_count": len(manifest) - len(TARGETS),
        },
        "repair_boundary": {
            "target_checks": target_checks,
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "protected_live_paths": protected_checks,
            "checkpoint_evidence": checkpoint_evidence,
            "git_head": head,
            "git_tree": tree,
            "git_index_clean": index_clean,
        },
        "authority_limits": {
            "semantic_payload_changed": False,
            "p2_t01_replayed": False,
            "p2_t03_executed": False,
            "p2_t02_external_action_taken": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def check_sealed_receipt() -> dict[str, Any]:
    errors: list[str] = []
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    if report.get("validation_status") != "PASS":
        errors.append("sealed repair-boundary receipt is not PASS")
    if report.get("immutable_route_sha256") != ROUTE_SHA256:
        errors.append("sealed receipt route hash mismatch")
    if report.get("route_blocker_fingerprint") != BLOCKER_FINGERPRINT:
        errors.append("sealed receipt blocker fingerprint mismatch")
    inherited = report.get("inherited_manifest", {})
    if inherited.get("sha256") != MANIFEST_SHA256 or inherited.get("path_count") != 76:
        errors.append("sealed receipt inherited-manifest binding mismatch")
    repair = report.get("repair_boundary", {})
    if repair.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed receipt records non-target repair-boundary drift")

    target_checks: dict[str, Any] = {}
    sealed_targets = repair.get("target_checks", {})
    for relative, (_, expected_after) in TARGETS.items():
        data = (ROOT / relative).read_bytes()
        observed = sha256_bytes(data)
        sealed_after = sealed_targets.get(relative, {}).get("after_sha256")
        match = (
            observed == expected_after
            and sealed_after == expected_after
            and data.endswith(b"\n")
            and not data.endswith(b"\n\n")
        )
        target_checks[relative] = {
            "expected_after_sha256": expected_after,
            "sealed_after_sha256": sealed_after,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"live recovered target mismatch: {relative}")

    protected_checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256_path(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": match}
        if not match:
            errors.append(f"live protected P2-T01 hash mismatch: {relative}")

    head = git("rev-parse", "HEAD").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD:
        errors.append("source HEAD changed before fresh recovery checkpoint")
    if not index_clean:
        errors.append("Git index is not clean before fresh recovery checkpoint")

    return {
        "schema_id": "v22_p2_t01_six_eof_checkpoint_recovery_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "status": "PASS" if not errors else "FAIL",
        "sealed_receipt_sha256": sha256_path(REPORT_PATH),
        "inherited_manifest_sha256": sha256_path(MANIFEST_PATH),
        "target_check_count": len(target_checks),
        "target_checks": target_checks,
        "protected_check_count": len(protected_checks),
        "protected_checks": protected_checks,
        "source_head": head,
        "git_index_clean": index_clean,
        "prior_checkpoint": {
            "job_id": "AJ-RT-20260809-006-001",
            "run_id": "RUN-CHECKPOINT-35d67803fd0a382a",
            "consumed": True,
            "replayed": False,
            "sole_failure_gate": "git_diff_check",
            "finding_count": 6,
        },
        "authority_limits": report.get("authority_limits", {}),
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-boundary", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.write_boundary:
        result = build_boundary_receipt()
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        result = check_sealed_receipt()
        if args.write:
            VALIDATION_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not (args.write_boundary or args.write):
        print(json.dumps(result, indent=2, sort_keys=True))
    status = result.get("validation_status", result.get("status"))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
