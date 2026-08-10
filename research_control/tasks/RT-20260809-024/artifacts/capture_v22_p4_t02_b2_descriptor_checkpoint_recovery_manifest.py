#!/usr/bin/env python3
"""Capture the inherited RT-023 transaction before its bounded recovery."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research_control/tasks/RT-20260809-024/artifacts/inherited_dirty_manifest_v22_p4_t02_b2_descriptor_checkpoint_recovery.json"
EXCLUDED_PREFIX = "research_control/tasks/RT-20260809-024/"
RECEIPT_ROOT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844"
RUN_IDS = [
    "RUN-CHECKPOINT-98526e01392211f5",
    "RUN-CHECKPOINT-bc05e07710ffd3ae",
    "RUN-CHECKPOINT-29f02e278335a022",
    "RUN-CHECKPOINT-0e238274095c768c",
]


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

    checkpoints = []
    for position, run_id in enumerate(RUN_IDS):
        run_dir = RECEIPT_ROOT / run_id
        receipt = run_dir / "receipt.json"
        receipt_data = receipt.read_bytes()
        payload = json.loads(receipt_data)
        gates = payload["gate_results"]
        failed_gate = next(g for g in gates if g["status"] == "FAIL")
        output_path = Path(failed_gate["stdout_path"])
        output_data = output_path.read_bytes()
        checkpoints.append(
            {
                "run_id": run_id,
                "canonical_consumed": position == 0,
                "redundant_unintended_receipt": position != 0,
                "receipt_path": str(receipt.relative_to(ROOT)),
                "receipt_sha256": digest(receipt_data),
                "status": payload["status"],
                "exit_code": payload["exit_code"],
                "gate_count": len(gates),
                "pass_count": sum(g["status"] == "PASS" for g in gates),
                "failure_count": sum(g["status"] == "FAIL" for g in gates),
                "failed_gate_id": failed_gate["gate_id"],
                "failed_gate_output_path": str(output_path.relative_to(ROOT)),
                "failed_gate_output_sha256": digest(output_data),
                "final_plan_hash": payload["final_plan_hash"],
            }
        )

    manifest = {
        "authority": "operational_validation_only",
        "job_id": "AJ-RT-20260809-024-001",
        "source_head": run("git", "rev-parse", "HEAD"),
        "entry_index_tree": run("git", "write-tree"),
        "path_count": len(paths),
        "paths": paths,
        "checkpoint_evidence": {
            "consumed": True,
            "replayed": False,
            "canonical_run_id": RUN_IDS[0],
            "finding_count": 23,
            "runs": checkpoints,
        },
        "error_count": 0,
        "errors": [],
    }
    if len(paths) != 52:
        manifest["errors"].append(f"expected 52 inherited paths, found {len(paths)}")
    output_hashes = {item["failed_gate_output_sha256"] for item in checkpoints}
    if output_hashes != {"50c4b8988edce9b5d4172db9921206f45443401132d45886b64f8e3181454e80"}:
        manifest["errors"].append("failed-gate output hashes do not match the sealed blocker")
    manifest["error_count"] = len(manifest["errors"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), "path_count": len(paths), "errors": manifest["errors"]}))
    return 1 if manifest["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
