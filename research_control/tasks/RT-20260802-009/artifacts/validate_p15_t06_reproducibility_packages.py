#!/usr/bin/env python3
"""Validate deterministic P15-T06 archives and clean-room reproduction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
BUILDER_PATH = ARTIFACT_DIR / "build_p15_t06_reproducibility_packages.py"
REPORT_PATH = ARTIFACT_DIR / "p15_t06_validation_v1.json"
RECEIPT_PATH = ARTIFACT_DIR / "p15_t06_compact_receipt_v1.json"
CREATED_AT = "2026-08-02T14:32:33Z"

FORBIDDEN_PATH_PARTS = (
    ".git",
    ".local",
    "__pycache__",
)
FORBIDDEN_PREFIXES = (
    ".codex/skills/continue-research-goal/goals/",
    ".codex/skills/continue-research-goal/leases/",
)


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("p15_t06_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load package builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_text(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return (
        bool(name)
        and not path.is_absolute()
        and ".." not in path.parts
        and not any(part in FORBIDDEN_PATH_PARTS for part in path.parts)
        and not any(name.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)
        and not name.endswith(".pyc")
    )


def run_reproduction(root: Path, commands: list[list[str]]) -> dict[str, object]:
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C", "LANG": "C"})
    command_results: list[dict[str, object]] = []
    for parts in commands:
        result = subprocess.run(
            (sys.executable, *parts),
            cwd=root,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
        )
        command_results.append(
            {
                "command": ["python", *parts],
                "returncode": result.returncode,
                "output_tail": result.stdout[-1000:],
            }
        )
        if result.returncode != 0:
            break
    return {
        "status": "PASS" if len(command_results) == len(commands) and all(item["returncode"] == 0 for item in command_results) else "FAIL",
        "commands": command_results,
    }


def validate() -> tuple[dict[str, object], dict[str, object]]:
    builder = load_builder()
    expected_outputs: dict[Path, bytes] = builder.build_outputs()
    checks: list[dict[str, object]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    for path, expected in sorted(expected_outputs.items(), key=lambda item: str(item[0])):
        present = path.is_file()
        exact = present and path.read_bytes() == expected
        check(f"deterministic_output::{path.name}", exact, "exact builder bytes")

    catalog_path = builder.OUTPUT_PATHS["catalog"]
    source_map_path = builder.OUTPUT_PATHS["source_map"]
    license_path = builder.OUTPUT_PATHS["license_audit"]
    environment_path = builder.OUTPUT_PATHS["environment"]
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    source_map = json.loads(source_map_path.read_text(encoding="utf-8"))
    license_audit = json.loads(license_path.read_text(encoding="utf-8"))
    environment_text = environment_path.read_text(encoding="utf-8")

    check("exact_candidate_set", [item["plan_task_id"] for item in catalog["packages"]] == ["P15-T01", "P15-T02", "P15-T03", "P15-T04"], "four direct dependency candidates")
    check("source_map_count", len(source_map["packages"]) == 4, "one source map per package")
    check("external_release_false", catalog["external_release_authorized"] is False and catalog["publication_authorized"] is False, "external action remains human-gated")
    check("environment_python_series", ">=3.12,<3.13" in environment_text and "requirements.lock" in environment_text, "Python and exact lock recipes present")
    check("license_status", license_audit["status"] == "PASS_SPLIT_LICENSE_AND_NOTICE_BOUND", "split-license mapping bound")
    check("license_external_material", license_audit["third_party_payloads_included"] is False and license_audit["external_primary_literature_copied"] is False, "no external payload copied")
    check("license_authority", license_audit["external_release_authorized"] is False and license_audit["scientific_status_changed"] is False, "license does not grant workflow or science authority")

    clean_results: list[dict[str, object]] = []
    total_manifest_entries = 0
    for package in catalog["packages"]:
        plan_task_id = package["plan_task_id"]
        archive_path = ROOT / package["archive_path"]
        archive_bytes = archive_path.read_bytes()
        check(f"archive_hash::{plan_task_id}", sha256_bytes(archive_bytes) == package["archive_sha256"], "outer catalog hash")
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
            members = archive.getmembers()
            names = [item.name for item in members]
            safe = all(item.isfile() and safe_member(item.name) for item in members)
            check(f"archive_safe::{plan_task_id}", safe, f"member_count={len(members)}")
            check(f"archive_unique::{plan_task_id}", len(names) == len(set(names)), "no duplicate member paths")
            check(f"archive_metadata::{plan_task_id}", all(item.mtime == 0 and item.uid == 0 and item.gid == 0 and item.mode == 0o644 for item in members), "fixed tar metadata")
            manifest_file = archive.extractfile("PACKAGE_MANIFEST.json")
            manifest = json.loads(manifest_file.read()) if manifest_file is not None else {}
            entries = manifest.get("entries", [])
            total_manifest_entries += len(entries)
            member_hashes: dict[str, str] = {}
            for item in entries:
                extracted = archive.extractfile(item["path"])
                member_hashes[item["path"]] = sha256_bytes(extracted.read()) if extracted is not None else "missing"
            exact_entries = all(member_hashes.get(item["path"]) == item["sha256"] for item in entries)
            check(f"manifest_hashes::{plan_task_id}", exact_entries, f"entry_count={len(entries)}")
            check(f"manifest_identity::{plan_task_id}", manifest.get("plan_task_id") == plan_task_id and manifest.get("package_id") == package["package_id"], "catalog and manifest identity")
            check(f"manifest_authority::{plan_task_id}", all(value is False for value in manifest.get("authority_limits", {}).values()), "all promotion and mutation flags false")

            with tempfile.TemporaryDirectory(prefix=f"p15-t06-{plan_task_id.lower()}-") as temp_dir:
                extraction_root = Path(temp_dir)
                archive.extractall(extraction_root, filter="data")
                reproduction = run_reproduction(extraction_root, manifest["reproduction_commands"])
        clean_results.append(
            {
                "plan_task_id": plan_task_id,
                "archive_sha256": package["archive_sha256"],
                "source_snapshot_commit": package["source_snapshot_commit"],
                "status": reproduction["status"],
                "commands": reproduction["commands"],
            }
        )
        check(f"clean_reproduction::{plan_task_id}", reproduction["status"] == "PASS", "all candidate commands exit zero in extracted archive")

    failed = [item["check_id"] for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "v21_p15_t06_reproducibility_package_validation_v1",
        "validator_id": "VAL-P15T06-REPRODUCIBILITY-PACKAGES-001",
        "created_at": CREATED_AT,
        "task_id": "RT-20260802-009",
        "plan_task_id": "P15-T06",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "failed_check_ids": failed,
        "package_count": len(catalog["packages"]),
        "manifest_entry_count": total_manifest_entries,
        "clean_reproduction_results": clean_results,
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_operational_evidence_only": True,
            "canonical_science_modified": False,
            "historical_evidence_rewritten": False,
            "external_release_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority_created": False,
        },
    }
    receipt_inputs = {
        str(path.relative_to(ROOT)): sha256_bytes(path.read_bytes())
        for path in sorted(expected_outputs, key=str)
    }
    receipt = {
        "schema_id": "v21_p15_t06_reproducibility_package_compact_receipt_v1",
        "receipt_id": "RECEIPT-P15T06-REPRODUCIBILITY-PACKAGES-001",
        "created_at": CREATED_AT,
        "task_id": "RT-20260802-009",
        "plan_task_id": "P15-T06",
        "result_status": "PASS_FOUR_SOURCE_BACKED_INTERNAL_RELEASE_CANDIDATES" if not failed else "FAIL_PRECISE_VALIDATION_BLOCKER",
        "package_count": len(catalog["packages"]),
        "manifest_entry_count": total_manifest_entries,
        "validator_id": report["validator_id"],
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "source_hashes": receipt_inputs,
        "clean_reproduction_pass_count": sum(item["status"] == "PASS" for item in clean_results),
        "license_and_notice_status": license_audit["status"],
        "claim_boundary_summary": "Four exact source-snapshot packages reproduce operational checks without changing canonical science, rewriting historical evidence, authorizing external release, or creating physics, proof, benchmark, or completed-derivation authority.",
        "recommendation_ids": ["V21-R39", "V21-R49", "V21-R57", "V21-R60", "V21-R66", "V21-R68"],
        "physics_promotion_authorized": False,
        "publication_authorized": False,
    }
    return report, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report, receipt = validate()
    report_text = json_text(report)
    receipt_text = json_text(receipt)
    stale: list[str] = []
    if args.write_report:
        REPORT_PATH.write_text(report_text, encoding="utf-8")
        RECEIPT_PATH.write_text(receipt_text, encoding="utf-8")
    else:
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report_text:
            stale.append(str(REPORT_PATH.relative_to(ROOT)))
        if not RECEIPT_PATH.is_file() or RECEIPT_PATH.read_text(encoding="utf-8") != receipt_text:
            stale.append(str(RECEIPT_PATH.relative_to(ROOT)))

    summary = {
        "schema_id": report["schema_id"],
        "status": "PASS" if report["status"] == "PASS" and not stale else "FAIL",
        "check_count": report["check_count"],
        "failed_check_ids": report["failed_check_ids"],
        "package_count": report["package_count"],
        "clean_reproduction_pass_count": receipt["clean_reproduction_pass_count"],
        "stale_outputs": stale,
        "authority": "operational_validation_only",
    }
    if args.json or True:
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
