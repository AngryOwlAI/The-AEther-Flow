#!/usr/bin/env python3
"""Validate the sealed ten-file V22 P3-T01 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-011"
JOB_ID = "AJ-RT-20260809-011-001"
STRATEGY_ID = "repair_v22_p3_t01_ten_eof_blank_lines_and_checkpoint_v1"
ROUTE_SHA256 = "28f579c56ace1669d4a808f30ed8fd57ad325f6565281ce08a2732b106a74abd"
BLOCKER_FINGERPRINT = "ecb02644dcb9611d61f89853eff2bce3497679bed4afdda4b5131f16d2c50a6c"
MANIFEST_SHA256 = "1b894544f1d4a47925c6a9cd2976661ff4ba6134e8e2b1befaeea34b4ddf70ab"
SOURCE_HEAD = "f97ecc4c4889df82d688b5892b88f8f0a171fd84"
SOURCE_TREE = "59a045a5750d85ab0dd566fd22b8534027af24a0"
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-011"
MANIFEST_PATH = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p3_t01_ten_eof_checkpoint.txt"
REPORT_PATH = TASK_DIR / "artifacts/v22_p3_t01_ten_eof_checkpoint_recovery_receipt.json"
VALIDATION_PATH = TASK_DIR / "artifacts/v22_p3_t01_ten_eof_checkpoint_recovery_validation.json"
CHECKPOINT_RECEIPT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-4340d0e85f29ac8f/receipt.json"
FAILED_OUTPUT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-4340d0e85f29ac8f/gates/0006-git_diff_check.stdout"
CHECKPOINT_RECEIPT_SHA256 = "a0293bc18ca70fc87d9d3428bfa2d60210858a941a969b0b40da987c54b23b93"
FAILED_OUTPUT_SHA256 = "6e9274c3191ebb082e54db91ee1aac45e982494f01e232bcb31dae43f3973af4"

TARGETS = {
    "research_control/handoffs/handoff-0980.md": (
        "fcd35813f683190c3c35418d663e03ace743bb67bf2ca2b752c05943ed0aa6b7",
        "d1ef8e4a6016624ff53ceb768e72eae108240b255edacc7c8fa8a5badf966181",
        False,
    ),
    "research_control/tasks/RT-20260809-010/00_TASK.yaml": (
        "423ffa40e9a20637cf42e9165863b2cd768fa379daa5080c0a9f417cddeda69b",
        "57f8963614d4a023e7b6e9c1105ffed4a3c734211c889a1396960ef15ec5614a",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/child_phys_math_p3_t01_local_state.yaml": (
        "3f74b646320882ad1aa539dd3da6729657db24df675808d0ee73362bd8fb4da9",
        "e0826b28bc563534c9c9d26b6284cb342ada3898f8ba5948aed1166e6b26dc40",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/child_phys_phil_p3_t01_source_target_audit.yaml": (
        "c7276d5ce51fb036b30b91314eb5cf6066f3267797b423159612f7796a301928",
        "dc0c34ff71d1c5298ddaccc045370ec14ce27b9616c4aff76af6800226ec2e96",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/fixtures/v22_p3_t01_local_state_cases.yaml": (
        "d4ae48a735ecf97e94dcc72615f44606120d966c2cbe970f9fbc9e0d493b2d3c",
        "9906c1cb2657f5dcdfce51fd253cb399129f77da9491166e225c42687f638fba",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/parent_conflict_review_p3_t01_local_state.yaml": (
        "dfaf379b53c43721f653cbc2edb42ace0c425214ec2c8a01aa7260ad96bf05bb",
        "e0311b8bcd95496cb79e3e7fd90c4c5715674b44066d2efae68be26d82b23e6c",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/parent_fusion_notes_p3_t01_local_state.md": (
        "e512a4db19a108223ed2b55a0de5dea6ade6a2b49015da1654b0d9708275c034",
        "faee0f28e891ff85b09aca811f7a889e7cb79a96cad615af260415c665d192c6",
        False,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_assumption_cost_ledger_v1.yaml": (
        "ab7039f9ca859a7aea0f1e7b03220fe37d69a544b8c7047e04b31cf8e375d436",
        "a67a007421866fd4b7676a35193bcf48636e7b530b1fda34d378c9bfdc379b08",
        True,
    ),
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_p7_refinement_interface_v1.yaml": (
        "81982c5caaecdf6a014aa9c6e162808368f28238eafc2d326968f26223bf8a73",
        "cfda8abd1905d04d3ec806c4178ad7c2f620f82a736ed6316e0768c17c143baa",
        True,
    ),
    "research_control/tasks/RT-20260809-010/documentation_impact.yaml": (
        "bbfb3e5afea82e3c99080f0ac7e8620e9a25e185cc1260e4ea53f2a7825b9768",
        "528ed0ced32d32f815268dca0423f95e65ee816977b1e3728aefd0d82afbaeed",
        True,
    ),
}

CUMULATIVE_DOCUMENTATION_PATH = "research_control/tasks/RT-20260809-010/documentation_impact.yaml"
REQUIRED_RECOVERY_DOCUMENTATION_PATHS = {
    "research_control/handoffs/handoff-0981.md",
    "research_control/handoffs/handoff-0981.yaml",
    "research_control/tasks/RT-20260809-011/00_TASK.yaml",
    "research_control/tasks/RT-20260809-011/DDR-20260809-011.md",
    "research_control/tasks/RT-20260809-011/artifacts/inherited_dirty_manifest_v22_p3_t01_ten_eof_checkpoint.txt",
    "research_control/tasks/RT-20260809-011/artifacts/p3_t01_ten_eof_checkpoint_blocker.yaml",
    "research_control/tasks/RT-20260809-011/artifacts/v22_p3_t01_ten_eof_checkpoint_recovery_receipt.json",
    "research_control/tasks/RT-20260809-011/artifacts/v22_p3_t01_ten_eof_checkpoint_recovery_validation.json",
    "research_control/tasks/RT-20260809-011/artifacts/validate_v22_p3_t01_ten_eof_checkpoint_recovery.py",
    "research_control/tasks/RT-20260809-011/documentation_impact.yaml",
    "research_control/tasks/RT-20260809-011/jobs/AJ-RT-20260809-011-001.yaml",
    "research_control/tasks/RT-20260809-011/jobs/completions/AJC-AJ-RT-20260809-011-001.yaml",
    "research_control/tasks/RT-20260809-011/roles/process-integrity-auditor@0.1.0--RT-20260809-011.yaml",
}

PROTECTED_LIVE_PATHS = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/design/v22_recommendation_backlog.yaml": "9ab9161e6ffb90c971e0cca5dafb1dec140376a91307850e125702d5bcfe3e7c",
    "research_control/handoffs/handoff-0979.yaml": "8cf1a9a5f17ba985c7200ad13223752ac7d7ff1e140f41c747d7ae808ed91957",
    "research_control/handoffs/handoff-0980.yaml": "6a372a42b26d4538f5ed995099fd66e3c7dd11a4f174bc4fc81df99d98b47e8f",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_primary_local_multifield_candidate_v1.yaml": "5d8a332c6aa05d85260a14af777a1d3f43015ba48980493acfa4c584bec75132",
    "research_control/tasks/RT-20260809-009/jobs/completions/AJC-AJ-RT-20260809-009-001.yaml": "7be3d3930f24aa6ba35f0131bf792fbdb386a5475e843883df999c1fc1845fae",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_local_multifield_source_state_v1.tex": "ce1b852b7ea178dd5d42a204e9cc63fb2c11e9987e8ac0fc733267eb04dbb6db",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_local_state_specification_v1.yaml": "961636349d8bfe73f5f13d33953f92d2a07d7d567f836e8f217dfeef7bb30813",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_local_state_validation.json": "4ed4ddc5f3cf0b6d441fd1001ca3e7c79af12bd09731b8e6f0ed7d282624c7bc",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_compact_receipt.json": "0e04dbfcb76b3af3e581397de474940f9461b0c74a6b84a5a5a6f48aa82fd07e",
    "research_control/tasks/RT-20260809-010/artifacts/validate_v22_p3_t01_local_state.py": "cf6cf0a88de923a2b6e5ebf536f3418ef2782763272151e1e53fa3b94d9ceb61",
    "research_control/tasks/RT-20260809-010/jobs/AJ-RT-20260809-010-001.yaml": "e3c7202bcfa1b52b686d395c3e2e28a570efb743d5a32b934c8cf018210acba3",
    "research_control/tasks/RT-20260809-010/jobs/completions/AJC-AJ-RT-20260809-010-001.yaml": "c28457f2bfb37f1e19a681d3e0084b5c9d76d4c4963ec8fd0f5d3cd1e609abe0",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def load_yaml(relative: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


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
    counts = receipt.get("counts", {})
    if receipt.get("status") != "FAIL" or receipt.get("exit_code") != 1:
        errors.append("checkpoint receipt does not record the expected failure")
    if failed_gate.get("status") != "FAIL" or failed_gate.get("exit_code") != 2:
        errors.append("git_diff_check gate does not record the expected return code")
    expected_counts = {"gate_count": 7, "pass_count": 2, "fail_count": 1, "skipped_count": 4}
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            errors.append(f"checkpoint count mismatch for {key}")
    output_lines = [line for line in FAILED_OUTPUT_PATH.read_text(encoding="utf-8").splitlines() if line]
    if len(output_lines) != len(TARGETS):
        errors.append(f"expected ten git-diff findings, observed {len(output_lines)}")
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
        "counts": counts,
    }


def build_boundary_receipt() -> dict[str, Any]:
    errors: list[str] = []
    manifest_lines, manifest = load_manifest()
    manifest_hash = sha256_path(MANIFEST_PATH)
    if manifest_hash != MANIFEST_SHA256:
        errors.append("inherited dirty manifest hash mismatch")
    if len(manifest_lines) != 62 or len(manifest) != 62:
        errors.append(f"expected 62 unique manifest paths, observed {len(manifest)}")
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
            declared_before, expected_after, parse_yaml = TARGETS[relative]
            parses = True
            try:
                text = data.decode("utf-8")
                if parse_yaml:
                    parses = yaml.safe_load(text) is not None
            except Exception:
                parses = False
            exact_one_newline_removed = (
                expected_before == declared_before
                and observed == expected_after
                and data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected_before
            )
            target_checks[relative] = {
                "before_sha256": expected_before,
                "after_sha256": observed,
                "byte_delta": 1,
                "document_parses": parses,
                "ends_with_exactly_one_newline": data.endswith(b"\n") and not data.endswith(b"\n\n"),
                "exact_one_final_newline_removed": exact_one_newline_removed,
            }
            if not exact_one_newline_removed or not parses:
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
            errors.append(f"protected P3-T01 hash mismatch: {relative}")

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
        "schema_id": "v22_p3_t01_ten_eof_checkpoint_recovery_receipt_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "route_blocker_fingerprint": BLOCKER_FINGERPRINT,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "source_task_id": "RT-20260809-010",
        "source_job_id": "AJ-RT-20260809-010-001",
        "source_handoff_id": "handoff-0980",
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
        "plan_state": {
            "p3_t01_executed": True,
            "p3_t01_replayed": False,
            "p3_t02_selected": True,
            "p3_t02_executed": False,
            "p2_t02_external_review_completed": False,
        },
        "authority_limits": {
            "semantic_payload_changed": False,
            "p3_t01_replayed": False,
            "p3_t02_executed": False,
            "p2_t02_external_action_taken": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "external_action_authorized": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def control_record_errors() -> list[str]:
    errors: list[str] = []
    expected = {
        "research_control/tasks/RT-20260809-011/00_TASK.yaml": ("task_id", TASK_ID, "status", "completed"),
        "research_control/tasks/RT-20260809-011/jobs/AJ-RT-20260809-011-001.yaml": ("job_id", JOB_ID, "status", "completed"),
        "research_control/tasks/RT-20260809-011/jobs/completions/AJC-AJ-RT-20260809-011-001.yaml": ("job_id", JOB_ID, "status", "completed"),
        "research_control/handoffs/handoff-0981.yaml": ("handoff_id", "handoff-0981", "status", "ready_for_v22_p3_t02_after_fresh_checkpoint"),
    }
    for relative, (key1, value1, key2, value2) in expected.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"required recovery control record missing: {relative}")
            continue
        data = load_yaml(relative)
        if data.get(key1) != value1 or data.get(key2) != value2:
            errors.append(f"recovery control record state mismatch: {relative}")
    completion_path = ROOT / "research_control/tasks/RT-20260809-011/jobs/completions/AJC-AJ-RT-20260809-011-001.yaml"
    if completion_path.is_file():
        completion = load_yaml(str(completion_path.relative_to(ROOT)))
        checkpoint = completion.get("checkpoint_commit", {})
        if checkpoint.get("status") != "PENDING" or completion.get("checkpoint_invocation_count") != 0:
            errors.append("recovery completion does not preserve one fresh pending checkpoint")
        prior = completion.get("prior_checkpoint", {})
        if prior.get("consumed") is not True or prior.get("replayed") is not False:
            errors.append("recovery completion does not preserve consumed-checkpoint non-replay")
    state_path = ROOT / "research_control/program_state.yaml"
    if state_path.is_file():
        state = load_yaml("research_control/program_state.yaml")
        if state.get("active_task_id") != TASK_ID or state.get("active_agent_job_id") != JOB_ID or state.get("latest_handoff_id") != "handoff-0981":
            errors.append("program state does not point to the recovery transaction")
    return errors


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
    if inherited.get("sha256") != MANIFEST_SHA256 or inherited.get("path_count") != 62:
        errors.append("sealed receipt inherited-manifest binding mismatch")
    repair = report.get("repair_boundary", {})
    if repair.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed receipt records non-target repair-boundary drift")

    target_checks: dict[str, Any] = {}
    sealed_targets = repair.get("target_checks", {})
    for relative, (_, expected_after, parse_yaml) in TARGETS.items():
        data = (ROOT / relative).read_bytes()
        observed = sha256_bytes(data)
        sealed_after = sealed_targets.get(relative, {}).get("after_sha256")
        parses = True
        missing_documentation_paths: list[str] = []
        try:
            text = data.decode("utf-8")
            if parse_yaml:
                parsed = yaml.safe_load(text)
                parses = parsed is not None
                if relative == CUMULATIVE_DOCUMENTATION_PATH:
                    changed_paths = set(parsed.get("changed_paths", [])) if isinstance(parsed, dict) else set()
                    missing_documentation_paths = sorted(REQUIRED_RECOVERY_DOCUMENTATION_PATHS - changed_paths)
        except Exception:
            parses = False
        if relative == CUMULATIVE_DOCUMENTATION_PATH:
            match = (
                sealed_after == expected_after
                and data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and parses
                and not missing_documentation_paths
            )
        else:
            match = observed == expected_after and sealed_after == expected_after and data.endswith(b"\n") and not data.endswith(b"\n\n") and parses
        target_checks[relative] = {
            "expected_repair_boundary_sha256": expected_after,
            "sealed_after_sha256": sealed_after,
            "observed_sha256": observed,
            "document_parses": parses,
            "post_boundary_cumulative_documentation_coverage": relative == CUMULATIVE_DOCUMENTATION_PATH,
            "missing_recovery_documentation_paths": missing_documentation_paths,
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
            errors.append(f"live protected P3-T01 hash mismatch: {relative}")

    head = git("rev-parse", "HEAD").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD:
        errors.append("source HEAD changed before fresh recovery checkpoint")
    if not index_clean:
        errors.append("Git index is not clean before fresh recovery checkpoint")
    errors.extend(control_record_errors())

    return {
        "schema_id": "v22_p3_t01_ten_eof_checkpoint_recovery_validation_v1",
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
            "job_id": "AJ-RT-20260809-010-001",
            "run_id": "RUN-CHECKPOINT-4340d0e85f29ac8f",
            "consumed": True,
            "replayed": False,
            "sole_failure_gate": "git_diff_check",
            "finding_count": 10,
        },
        "plan_state": report.get("plan_state", {}),
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
