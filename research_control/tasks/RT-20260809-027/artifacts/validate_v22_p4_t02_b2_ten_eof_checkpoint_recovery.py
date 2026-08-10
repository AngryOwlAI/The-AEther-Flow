#!/usr/bin/env python3
"""Validate the exact RT026 ten-EOF checkpoint recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = ROOT / "research_control/tasks/RT-20260809-027"
MANIFEST = TASK_ROOT / "artifacts/inherited_dirty_manifest_v22_p4_t02_b2_ten_eof_checkpoint_recovery.json"
BLOCKER = TASK_ROOT / "artifacts/v22_p4_t02_b2_ten_eof_checkpoint_blocker.yaml"
BOUNDARY_RECEIPT = TASK_ROOT / "artifacts/v22_p4_t02_b2_ten_eof_repair_boundary_receipt.json"
REPORT = TASK_ROOT / "artifacts/v22_p4_t02_b2_ten_eof_checkpoint_recovery_validation.json"
CHECKPOINT_RECEIPT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-7742e8345c578971/receipt.json"
FAILED_OUTPUT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-7742e8345c578971/gates/0006-git_diff_check.stdout"

SOURCE_HEAD = "8348a5412c1defd80e028c9efbb5efc2e7498913"
SOURCE_TREE = "d466c8e253e112293f3d5e9dc4fa0c485899bf61"
MANIFEST_SHA256 = "4e400c87485b4b843218e3ed7a67057fbe86f3c8c14582bc89ece8c21e945806"
BLOCKER_SHA256 = "76138b25d3fde9453766e11d7c4031425c31e2a7240fd9dcd71c247bcaf988ef"
CHECKPOINT_RECEIPT_SHA256 = "b1cd97fd2f327ed1ee63b1526b7a26a1b0db0baf5af40394128cee6ad3a0df39"
FAILED_OUTPUT_SHA256 = "d3815fc6bf218213c7e39c1a9346bff2c48207f51ee7e5e79eaeab9a98e37fc5"
BOUNDARY_RECEIPT_SHA256 = "6707f7dede7424eb82f7a0e43ce964d0806723cc9daf93e7ffd10f4debddce84"
STRATEGY_ID = "repair_v22_p4_t02_b2_ten_eof_blank_lines_and_checkpoint_v1"
ROUTE_SHA256 = "30a238248dba89c595f528b25ca302a862a78fa4fd3c45c0f42113c1c7474412"

TARGETS = {
    "research_control/handoffs/handoff-0996.md": (3238, "ea718c8e6c8c841ad1b0dbf929a986db0fcb52c844f5cafbfbbc630942a9733e", 3237, "7be8e4455a5d9ef6ece4560e5427a23c78ad3fa19980c6e831cb42656ffa98b9", "markdown"),
    "research_control/tasks/RT-20260809-026/artifacts/child_phys_math_p4_t02_b2_populated_instance_audit.yaml": (2160, "37b944c10d6787bfcce4a052a23115ba4fe2ed4d021b4eafbaea6269ad453da3", 2159, "d5f73b165dab2573c28534d149108952cd4e59dbadfffe39e786afeffa179609", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/child_phys_phil_p4_t02_b2_populated_instance_audit.yaml": (1899, "aa1d92f45b7535d630c6316088893f6cd22145f133d2eaf7ca51d73b46dd3db6", 1898, "a5e359bd83aa271c5f41b440f3036ed8e6e2ec0f2cc9cce84e8c97c4d5864840", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/parent_conflict_review_p4_t02_b2_populated_instance_audit.yaml": (1629, "e9690cd5a012111cb27cb73b53ebc983ac11b1c09526549ce5836c8b77f7f833", 1628, "d4ca64c691fafb2e979e7f7abc548b52570bcec1232d478deaeb6481fe52a624", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/parent_fusion_notes_p4_t02_b2_populated_instance_audit.md": (1957, "5fb075ba9d67bf1d1e4abbe794acb8839101b1ac5d9de4a4cb0dfc43d74de85c", 1956, "b6dba96db8f14e17e56753504653b96707400d5e39ffe24c70ef7c12b3b1cbee", "markdown"),
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_operational_interface_obstruction_v1.yaml": (1533, "5334e01aaacfde9839ef5ccf16654155ab8ad0eca0fc2ee2f306b861dbc9b008", 1532, "332d44f0b067c09a9a579c467bfeb8e36583e35d14a4f7aae10c023ac9c35642", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_disposition_v1.yaml": (3417, "5bc10f3bb42506a7e17a356152af1b66685fcb36a694d3a014a1c53aeab9b8b4", 3416, "5e9c2e48c5744f9c764c26b949cd09f4ecab6154d257e9551b1a6a0065dbde89", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_matrix_v1.yaml": (5209, "c15224b8bbb7adbdd9f8841990481fcd371e31fec61a6872d94d8a12aa448a08", 5208, "220cf896fbc8fe976c3a2fec357a420247bcf1042808c820683ea6a1161ee95c", "yaml"),
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_model.py": (4747, "27c12967db0b553174a2e1b29a5f43eb06bafb0dee83e4ae414ac4b367c18146", 4746, "1d6d73df17185b4f2b9b271031f03112533cc4c72e4410cc69e9fe1a3c80e1dd", "python"),
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_sector_split_and_presentation_countermodels_v1.yaml": (2721, "118fed7897bf2650df14546e902aaa185f9cb27720ccd7e6ecb975263aab7dff", 2720, "c432cb666385de776e438a09a027ef168f58ebc94bdd992e44f473ae191dd051", "yaml"),
}

PROTECTED = {
    "research_control/tasks/RT-20260809-026/00_TASK.yaml": "4ae68095712daa222f0b73ad024458aa834614efa2371bc79a2440ca914bdb34",
    "research_control/tasks/RT-20260809-026/DDR-20260809-026.md": "216dfc3c2d2664b0c3af5843791ebf74e840ee2a43ec85c1fb53c4570fd6addb",
    "research_control/tasks/RT-20260809-026/jobs/AJ-RT-20260809-026-001.yaml": "d6a52a21630348c8a6e85b479541e1f05ba4be0e4dfaf49a4baf23cec4c69381",
    "research_control/tasks/RT-20260809-026/jobs/completions/AJC-AJ-RT-20260809-026-001.yaml": "0277ebaecf44e169adc43c1de26d4dc2e6da7cccc9bbf3a2081c888d4d58ad4e",
    "research_control/tasks/RT-20260809-026/roles/smuggling-auditor@0.2.0--RT-20260809-026.yaml": "8e6992890626a8c39661884db6060bd3c64f930f5f9bba91dcfe36d2fa0e6bc2",
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_smuggling_audit_v1.tex": "8404fc7bd3586c353155cdce00bbede9e107ed4b38231b69953f4242bc5d90f0",
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_latex_compile_receipt.json": "c1e6d65e8458fb392cc9a39c6d23361aab7df7805a985f9f348cb2e52a7d85d9",
    "research_control/tasks/RT-20260809-026/artifacts/validate_v22_p4_t02_b2_populated_instance_audit.py": "a0e5757d775f8a6965f0c3e241dd749bd50c130593c7cb87f66c10ec58ea145c",
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_validation.json": "cc47831ffa49fb7ed0fca35a7937d3ef3af3fa4fe59b3740fb1d812f11a6b26f",
    "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_audit_compact_receipt.json": "15612099504dbe40bb632085a7307ca650fbbfb8db8042d808f952d170a3772c",
    "research_control/handoffs/handoff-0996.yaml": "1d92ae1b5e42630069dd04af7c72cb0eeb0d5cb8bf4884f17f4cdd0b0ce2a674",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return run("git", *args).stdout.decode().strip()


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_by_type(path: Path, kind: str) -> bool:
    try:
        if kind == "yaml":
            yaml.safe_load(path.read_text())
        elif kind == "python":
            compile(path.read_text(), str(path), "exec")
        else:
            path.read_text()
        return True
    except Exception:
        return False


def checkpoint_checks(errors: list[str]) -> dict:
    add(errors, sha(CHECKPOINT_RECEIPT) == CHECKPOINT_RECEIPT_SHA256, "checkpoint receipt hash mismatch")
    add(errors, sha(FAILED_OUTPUT) == FAILED_OUTPUT_SHA256, "failed-gate output hash mismatch")
    receipt = json.loads(CHECKPOINT_RECEIPT.read_text())
    failed = next(g for g in receipt["gate_results"] if g["status"] == "FAIL")
    add(errors, receipt["run_id"] == "RUN-CHECKPOINT-7742e8345c578971", "checkpoint run mismatch")
    add(errors, receipt["counts"] == {"blocked_count": 0, "cache_hit_count": 0, "executed_pass_count": 2, "fail_count": 1, "gate_count": 7, "pass_count": 2, "skipped_count": 4, "warn_count": 0}, "checkpoint counts mismatch")
    add(errors, receipt["final_plan_hash"] == "cd44288ec34993f5fa94d31e713143ed51273f21c837b0399c3fa3d41a1d3e7a", "checkpoint plan hash mismatch")
    add(errors, failed["gate_id"] == "git_diff_check" and failed["exit_code"] == 2, "failed gate mismatch")
    return {"run_id": receipt["run_id"], "counts": receipt["counts"], "failed_gate": failed, "receipt_sha256": sha(CHECKPOINT_RECEIPT), "failed_output_sha256": sha(FAILED_OUTPUT), "final_plan_hash": receipt["final_plan_hash"], "finding_count": 10}


def target_checks(errors: list[str], manifest: dict) -> dict:
    by_path = {item["path"]: item for item in manifest["paths"]}
    checks = {}
    for rel, (pre_bytes, pre_sha, post_bytes, post_sha, kind) in TARGETS.items():
        source = by_path.get(rel, {})
        data = (ROOT / rel).read_bytes()
        ok = len(data) == post_bytes and sha(ROOT / rel) == post_sha
        add(errors, source.get("working_bytes") == pre_bytes and source.get("working_sha256") == pre_sha, f"manifest preimage mismatch: {rel}")
        add(errors, ok, f"postimage mismatch: {rel}")
        add(errors, data.endswith(b"\n") and not data.endswith(b"\n\n"), f"terminal newline mismatch: {rel}")
        add(errors, parse_by_type(ROOT / rel, kind), f"parse failure: {rel}")
        checks[rel] = {"preimage_sha256": pre_sha, "postimage_sha256": sha(ROOT / rel), "byte_delta": pre_bytes - len(data), "exact_one_final_newline_removed": ok, "ends_with_exactly_one_newline": data.endswith(b"\n") and not data.endswith(b"\n\n"), "document_parses": parse_by_type(ROOT / rel, kind)}
    return checks


def protected_checks(errors: list[str]) -> dict:
    checks = {}
    for rel, expected in PROTECTED.items():
        observed = sha(ROOT / rel)
        add(errors, observed == expected, f"protected hash mismatch: {rel}")
        checks[rel] = {"expected_sha256": expected, "observed_sha256": observed, "match": observed == expected}
    return checks


def boundary_payload() -> dict:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text())
    add(errors, sha(MANIFEST) == MANIFEST_SHA256, "manifest hash mismatch")
    add(errors, sha(BLOCKER) == BLOCKER_SHA256, "blocker hash mismatch")
    add(errors, manifest["path_count"] == 63 and manifest["error_count"] == 0, "manifest count or errors mismatch")
    add(errors, manifest["source_head"] == SOURCE_HEAD and manifest["source_tree"] == SOURCE_TREE and manifest["entry_index_tree"] == SOURCE_TREE, "manifest source identity mismatch")
    add(errors, git_text("rev-parse", "HEAD") == SOURCE_HEAD, "working HEAD drifted")
    add(errors, git_text("write-tree") == SOURCE_TREE, "entry index tree drifted")
    add(errors, run("git", "diff", "--cached", "--quiet", check=False).returncode == 0, "entry index is dirty")
    target = target_checks(errors, manifest)
    non_target_mismatches = []
    for item in manifest["paths"]:
        if item["path"] in TARGETS:
            continue
        current = sha(ROOT / item["path"])
        if current != item["working_sha256"]:
            non_target_mismatches.append({"path": item["path"], "expected": item["working_sha256"], "observed": current})
    add(errors, not non_target_mismatches, "non-target inherited paths changed before repair boundary")
    payload = {
        "schema_id": "v22_p4_t02_b2_ten_eof_repair_boundary_receipt_v1",
        "authority": "operational_validation_only",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260809-027",
        "job_id": "AJ-RT-20260809-027-001",
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "inherited_manifest": {"path": str(MANIFEST.relative_to(ROOT)), "sha256": sha(MANIFEST), "path_count": manifest["path_count"], "target_path_count": len(TARGETS), "non_target_path_count": manifest["path_count"] - len(TARGETS)},
        "repair_boundary": {"git_head": git_text("rev-parse", "HEAD"), "git_tree": git_text("write-tree"), "git_index_clean": run("git", "diff", "--cached", "--quiet", check=False).returncode == 0, "checkpoint_evidence": checkpoint_checks(errors), "target_checks": target, "non_target_hash_mismatch_count": len(non_target_mismatches), "non_target_hash_mismatches": non_target_mismatches, "protected_science_and_control": protected_checks(errors)},
        "authority_limits": {"semantic_science_changed": False, "prior_job_replayed": False, "source_intrinsic_interface_repair_executed": False, "p4_t03_executed": False, "distance_to_gr_changed": False, "physics_promotion_authorized": False, "publication_or_push_authorized": False, "external_action_authorized": False},
        "error_count": len(errors),
        "errors": errors,
    }
    payload["status"] = "PASS" if not errors else "FAIL"
    return payload


def registry_has(path: str, field: str, value: str) -> bool:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return any(row.get(field) == value for row in csv.DictReader(handle))


def final_payload() -> dict:
    errors: list[str] = []
    add(errors, BOUNDARY_RECEIPT_SHA256 != "REPLACE_AFTER_BOUNDARY_CAPTURE", "boundary hash constant is unset")
    add(errors, BOUNDARY_RECEIPT.exists() and sha(BOUNDARY_RECEIPT) == BOUNDARY_RECEIPT_SHA256, "boundary receipt hash mismatch")
    if BOUNDARY_RECEIPT.exists():
        boundary = json.loads(BOUNDARY_RECEIPT.read_text())
        add(errors, boundary.get("status") == "PASS" and boundary.get("error_count") == 0, "repair boundary did not pass")
    manifest = json.loads(MANIFEST.read_text())
    targets = target_checks(errors, manifest)
    protected = protected_checks(errors)
    checkpoint = checkpoint_checks(errors)
    required_files = [
        "research_control/tasks/RT-20260809-027/00_TASK.yaml",
        "research_control/tasks/RT-20260809-027/DDR-20260809-027.md",
        "research_control/tasks/RT-20260809-027/jobs/AJ-RT-20260809-027-001.yaml",
        "research_control/tasks/RT-20260809-027/jobs/completions/AJC-AJ-RT-20260809-027-001.yaml",
        "research_control/tasks/RT-20260809-027/roles/process-integrity-auditor@0.1.0--RT-20260809-027.yaml",
        "research_control/tasks/RT-20260809-027/documentation_impact.yaml",
        "research_control/handoffs/handoff-0997.yaml",
        "research_control/handoffs/handoff-0997.md",
    ]
    for rel in required_files:
        add(errors, (ROOT / rel).is_file(), f"required output missing: {rel}")
        if (ROOT / rel).is_file():
            data = (ROOT / rel).read_bytes()
            add(errors, data.endswith(b"\n") and not data.endswith(b"\n\n"), f"required output terminal newline mismatch: {rel}")
    if all((ROOT / rel).is_file() for rel in required_files):
        task = yaml.safe_load((TASK_ROOT / "00_TASK.yaml").read_text())
        job = yaml.safe_load((TASK_ROOT / "jobs/AJ-RT-20260809-027-001.yaml").read_text())
        completion = yaml.safe_load((TASK_ROOT / "jobs/completions/AJC-AJ-RT-20260809-027-001.yaml").read_text())
        role = yaml.safe_load((TASK_ROOT / "roles/process-integrity-auditor@0.1.0--RT-20260809-027.yaml").read_text())
        handoff = yaml.safe_load((ROOT / "research_control/handoffs/handoff-0997.yaml").read_text())
        program = yaml.safe_load((ROOT / "research_control/program_state.yaml").read_text())
        add(errors, task["status"] == "completed" and task["route_strategy_id"] == STRATEGY_ID, "task state mismatch")
        add(errors, job["status"] == "completed" and job["checkpoint_invocation_count"] == 0 and not job["prior_failed_checkpoint_replayed"], "job state mismatch")
        add(errors, job["checkpoint_recovery"]["source_handoff_sha256"] == "1d92ae1b5e42630069dd04af7c72cb0eeb0d5cb8bf4884f17f4cdd0b0ce2a674", "checkpoint recovery handoff mismatch")
        add(errors, completion["status"] == "completed" and completion["result_status"] == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "completion state mismatch")
        add(errors, role["status"] == "completed" and role["expires_after"] == "AJ-RT-20260809-027-001", "role state mismatch")
        add(errors, handoff["handoff_id"] == "handoff-0997" and handoff["task_id"] == "RT-20260809-027", "handoff identity mismatch")
        add(errors, handoff["selected_next_route"]["strategy_id"] == "repair_v22_p4_t02_b2_populated_descriptor_source_intrinsic_interfaces_v1", "scientific route was not preserved")
        add(errors, not handoff["selected_next_route"]["executed"] and not handoff["claim_boundary"]["source_intrinsic_interface_repair_executed"], "scientific repair executed inside recovery")
        add(errors, program.get("active_task_id") == "RT-20260809-027" and program.get("latest_handoff_id") == "handoff-0997", "program active state mismatch")
    registry_checks = {
        "agent_job": registry_has("registries/AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260809-027-001"),
        "claim_boundary": registry_has("registries/CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-PS-V22-P4-T02-B2-TEN-EOF-CHECKPOINT-RECOVERY-001"),
        "director_decision": registry_has("registries/DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260809-027"),
        "research_task": registry_has("registries/RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260809-027"),
        "role_execution": registry_has("registries/ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", "process-integrity-auditor@0.1.0--RT-20260809-027"),
    }
    add(errors, all(registry_checks.values()), "one or more registry rows are missing")
    tracked_check = run("git", "diff", "--check", check=False)
    add(errors, tracked_check.returncode == 0, "tracked git diff whitespace check failed")
    payload = {
        "schema_id": "v22_p4_t02_b2_ten_eof_checkpoint_recovery_validation_v1",
        "authority": "operational_validation_only",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260809-027",
        "job_id": "AJ-RT-20260809-027-001",
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "boundary_receipt_sha256": sha(BOUNDARY_RECEIPT) if BOUNDARY_RECEIPT.exists() else None,
        "checkpoint_evidence": checkpoint,
        "target_checks": targets,
        "protected_science_and_control": protected,
        "registry_checks": registry_checks,
        "authority_limits": {"semantic_payload_changed": False, "prior_job_replayed": False, "source_intrinsic_interface_repair_executed": False, "p4_t03_executed": False, "distance_to_gr_changed": False, "physics_promotion_authorized": False, "proof_authority": False, "publication_authorized": False, "push_authorized": False, "external_action_authorized": False},
        "error_count": len(errors),
        "errors": errors,
    }
    payload["status"] = "PASS" if not errors else "FAIL"
    return payload


def write(payload: dict, path: Path) -> int:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"], "path": str(path.relative_to(ROOT)), "error_count": payload["error_count"], "errors": payload["errors"]}))
    return 1 if payload["errors"] else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write-boundary-receipt", action="store_true")
    group.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    return write(boundary_payload(), BOUNDARY_RECEIPT) if args.write_boundary_receipt else write(final_payload(), REPORT)


if __name__ == "__main__":
    raise SystemExit(main())
