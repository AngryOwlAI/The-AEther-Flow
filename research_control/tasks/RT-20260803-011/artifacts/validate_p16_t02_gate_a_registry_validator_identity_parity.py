#!/usr/bin/env python3
"""Validate exact-object Gate A registry and source identity parity."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260803-011"
JOB_ID = "AJ-RT-20260803-011-001"
REPORT_PATH = Path(
    "research_control/tasks/RT-20260803-011/artifacts/"
    "p16_t02_gate_a_registry_validator_identity_parity_validation.json"
)
REGISTRY_PATH = Path("registries/TEX_SOURCE_REGISTRY.csv")

GATE_A_OBJECT_ID = "TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1"
GATE_A_SOURCE_PATH = (
    "research_control/tasks/RT-20260724-004/artifacts/"
    "ontology_regime_gate_chair_decision_v1.tex"
)
GATE_A_SOURCE_SHA256 = "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934"
FOUNDATIONS_OBJECT_ID = "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS"

SEALED_RT005_HASHES = {
    "research_control/tasks/RT-20260803-005/artifacts/validate_p16_t02_gate_status_layer_contract.py": (
        "9ba655982225774beef866ec43f0a8fd116182f8987088afab78736fec5ac5e7"
    ),
    "research_control/tasks/RT-20260803-005/artifacts/p16_t02_gate_status_layer_contract_validation.json": (
        "330c35edb94d153553f33e449bfa94b2a3e88c435cb6ce99e95f7a89d56fc401"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record_check(
    checks: dict[str, Any],
    errors: list[str],
    check_id: str,
    observed: Any,
    expected: Any,
) -> None:
    matches = observed == expected
    checks[check_id] = {
        "expected": expected,
        "observed": observed,
        "match": matches,
    }
    if not matches:
        errors.append(f"{check_id}_mismatch")


def read_registry(registry_path: Path) -> list[dict[str, str]]:
    with registry_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_report(repo_root: Path, registry_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}
    rows = read_registry(registry_path)

    exact_rows = [row for row in rows if row.get("object_id") == GATE_A_OBJECT_ID]
    foundations_rows = [
        row for row in rows if row.get("object_id") == FOUNDATIONS_OBJECT_ID
    ]
    _record_check(checks, errors, "exact_object_row_count", len(exact_rows), 1)
    _record_check(
        checks,
        errors,
        "foundations_reference_row_count",
        len(foundations_rows),
        1,
    )

    if exact_rows:
        exact = exact_rows[0]
        _record_check(
            checks, errors, "exact_object_id", exact.get("object_id"), GATE_A_OBJECT_ID
        )
        _record_check(
            checks, errors, "exact_object_path", exact.get("path"), GATE_A_SOURCE_PATH
        )
        _record_check(
            checks,
            errors,
            "exact_object_registry_sha256",
            exact.get("source_hash"),
            GATE_A_SOURCE_SHA256,
        )
        _record_check(
            checks,
            errors,
            "exact_object_validation_status",
            exact.get("validation_status"),
            "PASS",
        )

    source_path = repo_root / GATE_A_SOURCE_PATH
    source_is_regular = source_path.is_file() and not source_path.is_symlink()
    _record_check(checks, errors, "exact_source_regular_file", source_is_regular, True)
    source_hash = sha256(source_path) if source_is_regular else None
    _record_check(
        checks,
        errors,
        "exact_source_sha256",
        source_hash,
        GATE_A_SOURCE_SHA256,
    )

    sealed_results: dict[str, dict[str, Any]] = {}
    for relative_path, expected_hash in SEALED_RT005_HASHES.items():
        path = repo_root / relative_path
        observed_hash = sha256(path) if path.is_file() and not path.is_symlink() else None
        matches = observed_hash == expected_hash
        sealed_results[relative_path] = {
            "expected_sha256": expected_hash,
            "observed_sha256": observed_hash,
            "match": matches,
        }
        if not matches:
            errors.append(f"sealed_rt005_hash_mismatch:{relative_path}")
    checks["sealed_rt005_hashes"] = sealed_results

    foundations_status = foundations_rows[0].get("validation_status") if foundations_rows else None
    exact_status = exact_rows[0].get("validation_status") if exact_rows else None
    cross_object_rejected = exact_status == "PASS" and GATE_A_OBJECT_ID != FOUNDATIONS_OBJECT_ID
    checks["cross_object_substitution"] = {
        "claimed_object_id": GATE_A_OBJECT_ID,
        "claimed_object_status": exact_status,
        "non_substitutable_object_id": FOUNDATIONS_OBJECT_ID,
        "non_substitutable_object_status": foundations_status,
        "rejected": cross_object_rejected,
    }
    if not cross_object_rejected:
        errors.append("cross_object_substitution_not_rejected")

    try:
        registry_display = registry_path.relative_to(repo_root).as_posix()
    except ValueError:
        registry_display = registry_path.as_posix()

    return {
        "schema_id": "p16_t02_gate_a_registry_validator_identity_parity_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "registry_path": registry_display,
        "exact_object_id": GATE_A_OBJECT_ID,
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "registry_validation_is_gate_verdict": False,
            "canonical_science_modified": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_external_action_or_push_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    registry_path = args.registry
    if not registry_path.is_absolute():
        registry_path = REPO_ROOT / registry_path
    report = build_report(REPO_ROOT, registry_path)
    destination = REPO_ROOT / REPORT_PATH

    if args.write_report:
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.check:
        if not destination.is_file():
            report["errors"].append("stored_report_missing")
        else:
            stored = json.loads(destination.read_text(encoding="utf-8"))
            if stored != report:
                report["errors"].append("stored_report_drift")
        report["error_count"] = len(report["errors"])
        report["validation_status"] = "PASS" if not report["errors"] else "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
