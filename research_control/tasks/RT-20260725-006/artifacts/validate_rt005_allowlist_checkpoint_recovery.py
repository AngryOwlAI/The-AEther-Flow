#!/usr/bin/env python3
"""Validate the exact RT-005 allowlist-order and protected-byte recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260725-006"
JOB_ID = "AJ-RT-20260725-006-001"
SOURCE_JOB_ID = "AJ-RT-20260725-005-001"
SOURCE_ROLE_REF = "validator-engineer@0.2.0--RT-20260725-005"
REPORT_PATH = ROOT / "research_control/tasks/RT-20260725-006/artifacts/rt005_allowlist_checkpoint_recovery_receipt.json"

SOURCE_JOB_PATH = ROOT / "research_control/tasks/RT-20260725-005/jobs/AJ-RT-20260725-005-001.yaml"
SOURCE_ROLE_PATH = ROOT / "research_control/tasks/RT-20260725-005/roles/validator-engineer@0.2.0--RT-20260725-005.yaml"

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260725-005/jobs/AJ-RT-20260725-005-001.yaml": "8b505634e9b7cbff6b047c4b153159a8dbea4c8aac17cb523f6257ffd4f6a1c0",
    "research_control/tasks/RT-20260725-005/jobs/completions/AJC-AJ-RT-20260725-005-001.yaml": "63788998ba3c4fb6af7325bea18c84e409248f5e2474ee56cf19aadd2aef6ae8",
    "research_control/handoffs/handoff-0865.yaml": "4c502b303a3e69d498fa216bc6109e49211a2142a96846c1e1371751b8bd0c83",
    "research_control/handoffs/handoff-0865.md": "df9b498a936a0d992996173113c47f61ba5468f537f4ca76f11d298664c8ad4c",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "7bb5c01a9f893c192cc98408f22176ec8d1e8162c6b645b483c6053200ed136d",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_object_v1.tex": "2520f82e54edcb2668446579ceed7a7dfc7a8abf995572aa9889a3d9a3a4467c",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_spec_v1.yaml": "a381549ac6eb37346c1469f1157bdfa8417fbc010a19c087cf099b1368ab1b9c",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_type_dependency_v1.yaml": "559d6fd77f5f4fc93e97e3429cbc87a09acf91b39099f56ef7ba00fbf3c3dd2f",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_validation_receipt_v1.json": "838a0fb827e2912d4452bd19556b3c96a7ea5a6a814e23defa3401ff649b9432",
    "research_control/tasks/RT-20260725-003/artifacts/child_phys_math_p5_t01_source_theory.yaml": "037d479f8b5285bf4180f956ad99c8158ddfc57adbcef00adc754085520bb50e",
    "research_control/tasks/RT-20260725-003/artifacts/child_phys_phil_p5_t01_source_theory.yaml": "18e24c5fcefbc5981cba7ccd6e613be32d7d33534c4f39acf4ee131bf909ce92",
    "research_control/tasks/RT-20260725-003/artifacts/parent_conflict_review_p5_t01_source_theory.yaml": "6bcec4104d73d0190850b36abd9c9604816af3d1adb3b82f7bdb503215bf8778",
    "research_control/tasks/RT-20260725-003/artifacts/parent_fusion_notes_p5_t01_source_theory.md": "75b6fec9d87070dc66b0e342aa2b191593c9869146bc3809a7dbbec28945f779",
    "research_control/tasks/RT-20260725-004/artifacts/p5_t01_dependent_contract_recovery_receipt.json": "45f6e7687b08c95ef5c74cacc845a6ecf1533bf55225179a08db459caf7949bc",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def registry_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    raise ValueError(f"missing registry row {value} in {path.relative_to(ROOT)}")


def build_report() -> dict[str, Any]:
    source_job = yaml.safe_load(SOURCE_JOB_PATH.read_text(encoding="utf-8"))
    source_role = yaml.safe_load(SOURCE_ROLE_PATH.read_text(encoding="utf-8"))
    job_row = registry_row(ROOT / "registries/AGENT_JOB_REGISTRY.csv", "job_id", SOURCE_JOB_ID)
    role_row = registry_row(
        ROOT / "registries/ROLE_EXECUTION_REGISTRY.csv",
        "execution_role_ref",
        SOURCE_ROLE_REF,
    )

    representations = {
        "agent_job": list(source_job["allowed_write_paths"]),
        "execution_role": list(source_role["allowed_write_paths"]),
        "agent_job_registry": job_row["allowed_write_paths"].split(";"),
        "role_execution_registry": role_row["allowed_write_paths"].split(";"),
    }
    canonical = representations["agent_job"]
    protected = {}
    errors: list[str] = []
    for relative, expected in PROTECTED_HASHES.items():
        observed = sha256(ROOT / relative)
        match = observed == expected
        protected[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"protected hash mismatch: {relative}")

    for name, paths in representations.items():
        if paths != canonical:
            errors.append(f"{name} allowed_write_paths differ from AgentJob order")

    if len(canonical) != 37:
        errors.append(f"expected 37 source allowed_write_paths, observed {len(canonical)}")
    if len(set(canonical)) != len(canonical):
        errors.append("source AgentJob allowed_write_paths contain duplicates")

    report = {
        "schema_id": "rt005_allowlist_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_job_id": SOURCE_JOB_ID,
        "strategy_id": "repair_p5_t01_rt005_allowlist_order_and_interrupted_checkpoint_v1",
        "checks": {
            "allowed_write_path_counts": {name: len(paths) for name, paths in representations.items()},
            "allowed_write_paths_equal": not any(
                paths != canonical for paths in representations.values()
            ),
            "ordered_representation_count": len(representations),
            "source_job_byte_preserved": protected[
                "research_control/tasks/RT-20260725-005/jobs/AJ-RT-20260725-005-001.yaml"
            ]["match"],
            "protected_hashes": protected,
            "p5_t01_reexecuted": False,
            "p5_t02_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p5_t02_executed": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }
    return report


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
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
