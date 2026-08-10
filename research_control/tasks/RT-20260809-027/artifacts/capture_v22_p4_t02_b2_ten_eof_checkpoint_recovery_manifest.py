#!/usr/bin/env python3
"""Seal the inherited RT-026 transaction before its exact EOF recovery."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research_control/tasks/RT-20260809-027/artifacts/inherited_dirty_manifest_v22_p4_t02_b2_ten_eof_checkpoint_recovery.json"
EXCLUDED_PREFIX = "research_control/tasks/RT-20260809-027/"
RECEIPT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-7742e8345c578971/receipt.json"
FAILED_OUTPUT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-7742e8345c578971/gates/0006-git_diff_check.stdout"


def run(*args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode().strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def status_entries() -> list[tuple[str, str]]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all", binary=True)
    assert isinstance(raw, bytes)
    fields = raw.split(b"\0")
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(fields) and fields[i]:
        record = fields[i]
        status = record[:2].decode()
        path = record[3:].decode()
        i += 1
        if "R" in status or "C" in status:
            i += 1
        if not path.startswith(EXCLUDED_PREFIX):
            entries.append((status, path))
    return sorted(entries, key=lambda item: item[1])


def index_bytes(path: str) -> bytes | None:
    result = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True)
    return result.stdout if result.returncode == 0 else None


def main() -> int:
    paths = []
    for status, path in status_entries():
        working = (ROOT / path).read_bytes()
        indexed = index_bytes(path)
        paths.append(
            {
                "path": path,
                "status": status,
                "working_bytes": len(working),
                "working_sha256": digest(working),
                "index_bytes": None if indexed is None else len(indexed),
                "index_sha256": None if indexed is None else digest(indexed),
            }
        )

    receipt_data = RECEIPT.read_bytes()
    receipt = json.loads(receipt_data)
    gates = receipt["gate_results"]
    failed_gate = next(gate for gate in gates if gate["status"] == "FAIL")
    failed_output_data = FAILED_OUTPUT.read_bytes()
    manifest = {
        "authority": "operational_validation_only",
        "job_id": "AJ-RT-20260809-027-001",
        "source_head": run("git", "rev-parse", "HEAD"),
        "source_tree": run("git", "rev-parse", "HEAD^{tree}"),
        "entry_index_tree": run("git", "write-tree"),
        "path_count": len(paths),
        "paths": paths,
        "checkpoint_evidence": {
            "consumed": True,
            "replayed": False,
            "run_id": "RUN-CHECKPOINT-7742e8345c578971",
            "receipt_path": str(RECEIPT.relative_to(ROOT)),
            "receipt_sha256": digest(receipt_data),
            "failed_gate_output_path": str(FAILED_OUTPUT.relative_to(ROOT)),
            "failed_gate_output_sha256": digest(failed_output_data),
            "status": receipt["status"],
            "exit_code": receipt["exit_code"],
            "gate_count": len(gates),
            "pass_count": sum(gate["status"] == "PASS" for gate in gates),
            "failure_count": sum(gate["status"] == "FAIL" for gate in gates),
            "skipped_count": receipt["counts"]["skipped_count"],
            "failed_gate_id": failed_gate["gate_id"],
            "failed_gate_returncode": failed_gate["exit_code"],
            "final_plan_hash": receipt["final_plan_hash"],
            "finding_count": 10,
        },
        "error_count": 0,
        "errors": [],
    }
    if len(paths) != 63:
        manifest["errors"].append(f"expected 63 inherited paths, found {len(paths)}")
    if manifest["source_head"] != "8348a5412c1defd80e028c9efbb5efc2e7498913":
        manifest["errors"].append("source HEAD differs from the consumed RT026 checkpoint preimage")
    if manifest["source_tree"] != "d466c8e253e112293f3d5e9dc4fa0c485899bf61":
        manifest["errors"].append("source tree differs from the consumed RT026 checkpoint preimage")
    if manifest["entry_index_tree"] != manifest["source_tree"]:
        manifest["errors"].append("entry index is not clean at the consumed checkpoint tree")
    if manifest["checkpoint_evidence"]["receipt_sha256"] != "b1cd97fd2f327ed1ee63b1526b7a26a1b0db0baf5af40394128cee6ad3a0df39":
        manifest["errors"].append("checkpoint receipt hash differs from the sealed blocker")
    if manifest["checkpoint_evidence"]["failed_gate_output_sha256"] != "d3815fc6bf218213c7e39c1a9346bff2c48207f51ee7e5e79eaeab9a98e37fc5":
        manifest["errors"].append("failed-gate output hash differs from the sealed blocker")
    manifest["error_count"] = len(manifest["errors"])
    OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), "path_count": len(paths), "errors": manifest["errors"]}))
    return 1 if manifest["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
