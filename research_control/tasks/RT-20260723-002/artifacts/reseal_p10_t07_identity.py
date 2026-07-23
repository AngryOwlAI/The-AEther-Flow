#!/usr/bin/env python3
"""Reseal only the three authorized P10-T07 identity outputs."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
IDENTITY_TOOL_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py"
)
SOURCE_CONTRACT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_contract.json"
)
EXPECTED_SOURCE_SHA256 = (
    "cc7d678328f2242cd49a83ce9a3eaa47e30e830d48a8b70a6a29434bb4a6477d"
)
PREDECESSOR_COPY_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-002/artifacts/ca/"
    "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51.json"
)
EXPECTED_PREDECESSOR_SHA256 = (
    "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51"
)
AUTHORIZED_DRIFT_PATHS = (
    "research_control/tasks/RT-20260722-002/artifacts/artifact_refs.json",
    "research_control/tasks/RT-20260722-002/artifacts/ca/"
    "cc7d678328f2242cd49a83ce9a3eaa47e30e830d48a8b70a6a29434bb4a6477d.json",
    "research_control/tasks/RT-20260722-002/artifacts/compact_receipt.json",
)


def load_identity_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "p10_t07_artifact_identity", IDENTITY_TOOL_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {IDENTITY_TOOL_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path_hash(module: ModuleType, path: Path) -> str:
    return module.file_sha256(path) if path.is_file() else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    tool = load_identity_tool()
    outputs, validation = tool.expected_outputs()
    drift_before = tuple(tool.drift_paths(outputs))
    predecessor_before = path_hash(tool, PREDECESSOR_COPY_PATH)
    source_sha256 = path_hash(tool, SOURCE_CONTRACT_PATH)

    preconditions: dict[str, bool] = {
        "semantic_validation_pass": validation["status"] == "PASS",
        "source_contract_hash_matches": source_sha256 == EXPECTED_SOURCE_SHA256,
        "predecessor_copy_hash_matches": (
            predecessor_before == EXPECTED_PREDECESSOR_SHA256
        ),
        "drift_is_exact_authorized_set": (
            drift_before == AUTHORIZED_DRIFT_PATHS if args.write else not drift_before
        ),
    }

    written_paths: list[str] = []
    if all(preconditions.values()) and args.write:
        for path_text in AUTHORIZED_DRIFT_PATHS:
            tool.atomic_write(REPO_ROOT / path_text, outputs[path_text])
            written_paths.append(path_text)

    drift_after = tuple(tool.drift_paths(outputs))
    predecessor_after = path_hash(tool, PREDECESSOR_COPY_PATH)
    output_hashes = {
        path_text: path_hash(tool, REPO_ROOT / path_text)
        for path_text in AUTHORIZED_DRIFT_PATHS
    }
    postconditions = {
        "all_expected_outputs_current": not drift_after,
        "predecessor_copy_preserved": (
            predecessor_before
            == predecessor_after
            == EXPECTED_PREDECESSOR_SHA256
        ),
        "written_path_set_exact": (
            tuple(written_paths) == AUTHORIZED_DRIFT_PATHS
            if args.write
            else not written_paths
        ),
    }
    status = (
        "PASS"
        if all(preconditions.values()) and all(postconditions.values())
        else "FAIL"
    )
    payload: dict[str, Any] = {
        "authorized_drift_paths": list(AUTHORIZED_DRIFT_PATHS),
        "check_count": validation["check_count"],
        "drift_after": list(drift_after),
        "drift_before": list(drift_before),
        "failed_check_count": validation["failed_check_count"],
        "identity_tool_path": IDENTITY_TOOL_PATH.relative_to(REPO_ROOT).as_posix(),
        "identity_tool_sha256": path_hash(tool, IDENTITY_TOOL_PATH),
        "mode": "write" if args.write else "check",
        "output_hashes": output_hashes,
        "preconditions": preconditions,
        "predecessor_copy_path": PREDECESSOR_COPY_PATH.relative_to(
            REPO_ROOT
        ).as_posix(),
        "predecessor_sha256_after": predecessor_after,
        "predecessor_sha256_before": predecessor_before,
        "reference_count": validation["reference_count"],
        "schema_id": "p10_t07_identity_reseal_receipt_v1",
        "source_contract_path": SOURCE_CONTRACT_PATH.relative_to(
            REPO_ROOT
        ).as_posix(),
        "source_contract_sha256": source_sha256,
        "status": status,
        "written_paths": written_paths,
        "postconditions": postconditions,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
