#!/usr/bin/env python3
"""Validate the sealed two-file RT-20260810-003 EOF-only recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260810-004"
JOB_ID = "AJ-RT-20260810-004-001"
SOURCE_TASK_ID = "RT-20260810-003"
SOURCE_JOB_ID = "AJ-RT-20260810-003-001"
SOURCE_HANDOFF_ID = "handoff-1000"
SOURCE_HEAD = "cdab63ae17afd842bb432e4d85cb4cad54630b9f"
MANIFEST_PATH = (
    ROOT
    / "research_control/tasks/RT-20260810-004/artifacts/"
    "rt003_failed_checkpoint_dirty_state_manifest.yaml"
)
MANIFEST_SHA256 = "5dd7772603884bec19f80cfa90270c512db94e4afc96c4cd18a08828898462c0"
FAILURE_EVIDENCE_PATH = (
    ROOT
    / "research_control/tasks/RT-20260810-004/artifacts/"
    "rt003_failed_checkpoint_evidence.yaml"
)
FAILURE_EVIDENCE_SHA256 = (
    "4ff32356fe5fe389adda6d166a60d964e2f766f1520144971a11c18959c8f807"
)
BLOCKER_PATH = (
    ROOT
    / "research_control/tasks/RT-20260810-004/artifacts/"
    "rt003_checkpoint_whitespace_blocker.yaml"
)
BLOCKER_SHA256 = "19f3dafb6a4cb86ac5b4d7daa15a084bdf6d7032dee1d5508a4a4cb372e67bb3"
CHECKPOINT_RECEIPT_PATH = (
    ROOT
    / ".local/validation-receipts/"
    "8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/"
    "RUN-CHECKPOINT-50382a6d69ea35dc/receipt.json"
)
CHECKPOINT_RECEIPT_SHA256 = (
    "2d82fdc56e66ce892698bb83ff3616b433302fa3268ab3d26e72af549c5f781b"
)
FAILED_GATE_STDOUT_PATH = CHECKPOINT_RECEIPT_PATH.parent / "gates/0006-git_diff_check.stdout"
FAILED_GATE_STDOUT_SHA256 = (
    "79f4e23915a5a0dc519d3f1c1ea37d77080c67af4370170d42296b94901207ba"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260810-004/artifacts/"
    "rt003_two_eof_checkpoint_recovery_receipt.json"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_manifest() -> tuple[dict[str, dict[str, Any]], set[str], dict[str, Any]]:
    payload = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("dirty-state manifest is not a mapping")
    entries: dict[str, dict[str, Any]] = {}
    for raw in payload.get("entries", []):
        if not isinstance(raw, str):
            raise ValueError("manifest entry is not a string")
        path, git_status, digest, byte_count = raw.rsplit("|", 3)
        entries[path] = {
            "git_status": git_status,
            "sha256": digest,
            "byte_count": int(byte_count),
        }
    targets = {str(item) for item in payload.get("targets", [])}
    return entries, targets, payload


def structured_valid(relative: str, data: bytes) -> bool:
    try:
        text = data.decode("utf-8")
        if relative.endswith(".yaml"):
            return isinstance(yaml.safe_load(text), dict)
        if relative.endswith(".md") and text.startswith("---\n"):
            marker = text.find("\n---\n", 4)
            if marker < 0:
                return False
            return isinstance(yaml.safe_load(text[4:marker]), dict)
    except (UnicodeDecodeError, yaml.YAMLError):
        return False
    return False


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    entries, targets, manifest = parse_manifest()

    if sha256(MANIFEST_PATH) != MANIFEST_SHA256:
        errors.append("sealed dirty-state manifest hash mismatch")
    if sha256(FAILURE_EVIDENCE_PATH) != FAILURE_EVIDENCE_SHA256:
        errors.append("tracked failed-checkpoint evidence hash mismatch")
    if sha256(BLOCKER_PATH) != BLOCKER_SHA256:
        errors.append("tracked checkpoint blocker hash mismatch")
    if len(entries) != 76:
        errors.append(f"expected 76 manifest paths, observed {len(entries)}")
    if len(targets) != 2:
        errors.append(f"expected 2 targets, observed {len(targets)}")
    if targets - set(entries):
        errors.append("one or more targets are absent from the manifest")
    if manifest.get("head") != SOURCE_HEAD:
        errors.append("manifest source HEAD mismatch")
    if manifest.get("index_entry_count") != 0:
        errors.append("manifest did not capture an empty index")

    target_checks: dict[str, Any] = {}
    non_target_mismatches: list[str] = []
    for relative, expected in entries.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"manifest path missing: {relative}")
            continue
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if relative in targets:
            exact_one_newline_removed = (
                data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected["sha256"]
                and len(data) + 1 == expected["byte_count"]
            )
            valid_structure = structured_valid(relative, data)
            target_checks[relative] = {
                "before_sha256": expected["sha256"],
                "after_sha256": observed,
                "before_byte_count": expected["byte_count"],
                "after_byte_count": len(data),
                "exact_one_final_newline_removed": exact_one_newline_removed,
                "ends_with_exactly_one_newline": data.endswith(b"\n")
                and not data.endswith(b"\n\n"),
                "structured_valid": valid_structure,
            }
            if not exact_one_newline_removed:
                errors.append(f"target is not an exact one-newline deletion: {relative}")
            if not valid_structure:
                errors.append(f"target structure is invalid: {relative}")
        elif observed != expected["sha256"] or len(data) != expected["byte_count"]:
            non_target_mismatches.append(relative)

    if non_target_mismatches:
        errors.append(
            f"{len(non_target_mismatches)} non-target dirty-manifest paths changed"
        )

    checkpoint_receipt_hash = sha256(CHECKPOINT_RECEIPT_PATH)
    if checkpoint_receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("failed checkpoint receipt hash mismatch")
    checkpoint_receipt = json.loads(CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8"))
    if checkpoint_receipt.get("status") != "FAIL":
        errors.append("source checkpoint receipt no longer records FAIL")
    counts = checkpoint_receipt.get("counts", {})
    if counts.get("gate_count") != 7 or counts.get("executed_pass_count") != 2:
        errors.append("source checkpoint receipt gate counts differ from sealed failure")

    failed_gate_stdout = FAILED_GATE_STDOUT_PATH.read_bytes()
    failed_gate_stdout_hash = sha256_bytes(failed_gate_stdout)
    if failed_gate_stdout_hash != FAILED_GATE_STDOUT_SHA256:
        errors.append("failed git-diff gate output hash mismatch")
    decoded_gate_stdout = failed_gate_stdout.decode("utf-8")
    for relative in sorted(targets):
        if relative not in decoded_gate_stdout:
            errors.append(f"failed gate output does not name target: {relative}")

    return {
        "schema_id": "rt003_two_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "source_handoff_id": SOURCE_HANDOFF_ID,
        "source_head": SOURCE_HEAD,
        "strategy_id": "repair_rt003_two_eof_blanks_and_checkpoint_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": {
            "manifest_path": str(MANIFEST_PATH.relative_to(ROOT)),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "manifest_path_count": len(entries),
            "target_path_count": len(targets),
            "non_target_path_count": len(entries) - len(targets),
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "targets": target_checks,
            "failed_checkpoint_receipt_sha256": checkpoint_receipt_hash,
            "failed_gate_stdout_sha256": failed_gate_stdout_hash,
            "failed_gate_target_count": sum(
                relative in decoded_gate_stdout for relative in targets
            ),
            "rt003_science_reexecuted": False,
            "candidate_construction_executed": False,
            "semantic_science_payload_modified": False,
            "consumed_checkpoint_replayed": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "candidate_construction_authorized": False,
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
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif not args.write_report:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
