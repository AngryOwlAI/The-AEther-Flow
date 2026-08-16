#!/usr/bin/env python3
"""Validate the bounded RT001 handoff-1044 blank-EOF checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260816-002"
JOB_ID = "AJ-RT-20260816-002-001"
SOURCE_TASK_ID = "RT-20260816-001"
SOURCE_JOB_ID = "AJ-RT-20260816-001-001"
SOURCE_HEAD = "50f4d83d130d402b9633ffc6232540aaefb0804e"
SOURCE_TREE = "0256dd3fd5fb8ab6668c8c8b7efdbb29cde16880"
HANDOFF_PATH = ROOT / "research_control/handoffs/handoff-1044.yaml"
HANDOFF_SHA256 = "3a73c8804ff6568c28296bfaa81ad256a02d79952675046a4c58cac505e13abc"
HANDOFF_MD_PATH = ROOT / "research_control/handoffs/handoff-1044.md"
HANDOFF_MD_SHA256 = "81e55004cfb7b1c7c0e46adc6eb2769e3162902c82fc47d04b3f83166387f29d"
SOURCE_TASK_PATH = ROOT / "research_control/tasks/RT-20260816-001/00_TASK.yaml"
SOURCE_TASK_SHA256 = "5ada4ce169251f04b5b7352ae1a01c3e4a5add751f7ee0c1a00107a00403158c"
SOURCE_JOB_PATH = ROOT / "research_control/tasks/RT-20260816-001/jobs/AJ-RT-20260816-001-001.yaml"
SOURCE_JOB_SHA256 = "1336e18fe55f165402a308743386c0058ac4abc4c8184a43931249c7e1943d62"
SOURCE_COMPLETION_PATH = ROOT / "research_control/tasks/RT-20260816-001/jobs/completions/AJC-AJ-RT-20260816-001-001.yaml"
SOURCE_COMPLETION_SHA256 = "1d077a50e2b9b96e2c28d0d8c3cb0ae2c94625354a7b3fc314199af41938bf6e"
SOURCE_ROLE_PATH = ROOT / "research_control/tasks/RT-20260816-001/roles/ontology-formalizer@0.2.0--RT-20260816-001.yaml"
SOURCE_ROLE_SHA256 = "2c32956dee23071bc4da0b6784777598419c17fbf3f416ec58fbf923df811523"
BLOCKER_PATH = ROOT / "research_control/tasks/RT-20260816-001/artifacts/checkpoint_blocker_rt001_handoff_1044_blank_eof_v1.yaml"
BLOCKER_SHA256 = "67f06ea6a0c0bf3c490093526cbfb24ea7bac47ffc06906fc5ff8200823a4e15"
FAILED_BLOB_SHA1 = "4728b015bb142ffc4303e109390767a43763920d"
FAILED_BLOB_SHA256 = "b4a587695f806289ed4cf2b1d50a984123516bb7361878848a6466f71b310a4c"
FAILED_STAGED_TREE = "66c671b23b03f502bfcf72ca21466c403846b3cf"
OPERATIONAL_RECEIPT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-05eb814de8cf8411/receipt.json"
OPERATIONAL_RECEIPT_SHA256 = "7bc292e6e5927d8cf907e10897efb71a5d437de296541529a9d753d1deff8a42"
SUCCESSOR_PACKET_ID = "PKT-V22-P4T02-B2-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1"
REPORT_PATH = ROOT / "research_control/tasks/RT-20260816-002/artifacts/rt001_handoff_1044_blank_eof_checkpoint_recovery_receipt.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping: {path}")
    return payload


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    governed = {
        "handoff_yaml": (HANDOFF_PATH, HANDOFF_SHA256),
        "handoff_markdown": (HANDOFF_MD_PATH, HANDOFF_MD_SHA256),
        "source_task": (SOURCE_TASK_PATH, SOURCE_TASK_SHA256),
        "source_job": (SOURCE_JOB_PATH, SOURCE_JOB_SHA256),
        "source_completion": (SOURCE_COMPLETION_PATH, SOURCE_COMPLETION_SHA256),
        "source_role": (SOURCE_ROLE_PATH, SOURCE_ROLE_SHA256),
        "checkpoint_blocker": (BLOCKER_PATH, BLOCKER_SHA256),
    }
    observed_hashes: dict[str, str] = {}
    for label, (path, expected) in governed.items():
        if not path.is_file():
            errors.append(f"missing governed source: {path.relative_to(ROOT)}")
            continue
        observed = sha256(path)
        observed_hashes[label] = observed
        if observed != expected:
            errors.append(f"governed source hash mismatch: {label}")

    markdown = HANDOFF_MD_PATH.read_bytes()
    if not markdown.endswith(b"\n") or markdown.endswith(b"\n\n"):
        errors.append("handoff-1044 Markdown does not end with exactly one newline")

    failed_blob = git("cat-file", "blob", FAILED_BLOB_SHA1)
    failed_blob_bytes = failed_blob.stdout.encode("utf-8")
    if failed_blob.returncode != 0:
        errors.append("failed staged blob is not available in the object database")
    if sha256_bytes(failed_blob_bytes) != FAILED_BLOB_SHA256:
        errors.append("failed staged blob SHA-256 mismatch")
    if not failed_blob_bytes.endswith(b"\n\n"):
        errors.append("failed staged blob does not retain the proven blank EOF")

    blocker = load_yaml(BLOCKER_PATH)
    if blocker.get("status") != "BLOCKED_CHECKPOINT_STAGED_GIT_DIFF_HANDOFF_1044_BLANK_EOF_REPAIRED_FRESH_CHECKPOINT_REQUIRED":
        errors.append("checkpoint blocker status mismatch")
    if blocker.get("checkpoint_invocation_count") != 1:
        errors.append("prior checkpoint invocation count is not exactly one")
    if blocker.get("checkpoint_retry_in_this_job_authorized") is not False:
        errors.append("prior same-AgentJob retry is not prohibited")
    if blocker.get("failed_staged_artifact", {}).get("git_blob_sha1") != FAILED_BLOB_SHA1:
        errors.append("blocker failed blob SHA-1 mismatch")
    if blocker.get("staged_acceptance", {}).get("tree_sha1") != FAILED_STAGED_TREE:
        errors.append("blocker failed staged tree mismatch")
    if blocker.get("index_restoration", {}).get("restored") is not True:
        errors.append("blocker does not record restored index")

    operational_receipt_hash = "missing"
    if OPERATIONAL_RECEIPT_PATH.is_file():
        operational_receipt_hash = sha256(OPERATIONAL_RECEIPT_PATH)
        if operational_receipt_hash != OPERATIONAL_RECEIPT_SHA256:
            errors.append("operational checkpoint receipt hash mismatch")
        receipt = json.loads(OPERATIONAL_RECEIPT_PATH.read_text(encoding="utf-8"))
        if receipt.get("status") != "FAIL":
            errors.append("operational checkpoint receipt no longer records FAIL")
    else:
        errors.append("operational checkpoint receipt is missing")

    handoff = load_yaml(HANDOFF_PATH)
    completion_text = SOURCE_COMPLETION_PATH.read_text(encoding="utf-8")
    handoff_text = HANDOFF_PATH.read_text(encoding="utf-8")
    if handoff.get("handoff_id") != "handoff-1044":
        errors.append("source handoff identity mismatch")
    if handoff.get("completion_sha256") != SOURCE_COMPLETION_SHA256:
        errors.append("source handoff completion binding mismatch")
    if SUCCESSOR_PACKET_ID not in completion_text or SUCCESSOR_PACKET_ID not in handoff_text:
        errors.append("selected Smuggling Auditor packet identity is not preserved")
    if "selected_packet_executed: false" not in completion_text or "selected_packet_executed: false" not in handoff_text:
        errors.append("selected Smuggling Auditor remains-unexecuted boundary missing")

    diff_check = git("diff", "--check")
    if diff_check.returncode != 0:
        errors.append("working-tree git diff --check failed")
    staged = git("diff", "--cached", "--name-only")
    staged_paths = [line for line in staged.stdout.splitlines() if line]
    if staged.returncode != 0 or staged_paths:
        errors.append("index is not restored and empty before the fresh recovery checkpoint")
    head = git("rev-parse", "HEAD").stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.strip()
    if head != SOURCE_HEAD or tree != SOURCE_TREE:
        errors.append("pre-recovery source HEAD/tree changed")

    return {
        "schema_id": "rt001_handoff_1044_blank_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "source_handoff_id": "handoff-1044",
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "strategy_id": "recover_rt001_handoff_1044_blank_eof_checkpoint_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": {
            "governing_source_hashes": observed_hashes,
            "governing_source_count": len(governed),
            "handoff_markdown_ends_with_exactly_one_newline": markdown.endswith(b"\n") and not markdown.endswith(b"\n\n"),
            "failed_staged_blob_sha1": FAILED_BLOB_SHA1,
            "failed_staged_blob_sha256": sha256_bytes(failed_blob_bytes),
            "failed_staged_blob_ends_with_blank_line": failed_blob_bytes.endswith(b"\n\n"),
            "failed_staged_tree": FAILED_STAGED_TREE,
            "operational_receipt_sha256": operational_receipt_hash,
            "prior_checkpoint_invocation_count": blocker.get("checkpoint_invocation_count"),
            "prior_same_agentjob_retry_authorized": blocker.get("checkpoint_retry_in_this_job_authorized"),
            "index_restored_before_fresh_checkpoint": not staged_paths,
            "working_tree_diff_check": "PASS" if diff_check.returncode == 0 else "FAIL",
            "rt001_science_reexecuted": False,
            "smuggling_auditor_executed": False,
            "consumed_checkpoint_replayed": False,
            "semantic_science_payload_modified": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "source_law_adopted": False,
            "physical_probability_claimed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authorized": False,
            "push_authorized": False,
            "external_action_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif not args.write_report:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
