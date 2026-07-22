#!/usr/bin/env python3
"""Validate the P12-T02 family-freeze seed and route fixture matrix."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.family_freeze_admission import (  # noqa: E402
    REOPENING_CLASSES,
    family_freeze_policy,
    evaluate_family_freeze_admission,
)

ARTIFACT_DIR = Path(__file__).resolve().parent
SEED_PATH = ARTIFACT_DIR / "family_freeze_historical_seed.json"
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "family_freeze_route_cases.json"
REPORT_PATH = ARTIFACT_DIR / "family_freeze_validation_report.json"
RECEIPT_PATH = ARTIFACT_DIR / "family_freeze_compact_receipt.json"
P10_SEED_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260721-005"
    / "artifacts"
    / "v21_candidate_lineage_historical_seed.json"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def rendered(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _fixture_evidence_verifier(path_text: str, expected_sha256: str) -> str:
    if not path_text.startswith("fixtures/"):
        return "fixture evidence path must remain under fixtures/"
    if not SHA256_RE.fullmatch(expected_sha256):
        return "fixture evidence hash must be a lowercase SHA-256 digest"
    return ""


def _validate_seed(seed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if seed.get("schema_id") != "family_freeze_registry_v1":
        errors.append("seed schema_id mismatch")
    if seed.get("status") != "draft/control":
        errors.append("seed status must be draft/control")
    for path_text, expected_sha in seed.get("source_hashes", {}).items():
        path = REPO_ROOT / path_text
        if not path.is_file():
            errors.append(f"missing source {path_text}")
            continue
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != expected_sha:
            errors.append(f"source hash drift {path_text}")

    p10 = json.loads(P10_SEED_PATH.read_text(encoding="utf-8"))
    p10_families = {item["family_id"]: item for item in p10["families"]}
    p10_candidates = {item["immutable_candidate_id"]: item for item in p10["candidates"]}
    freeze_ids: set[str] = set()
    family_ids: set[str] = set()
    for freeze in seed.get("freezes", []):
        freeze_id = str(freeze.get("freeze_id", ""))
        family_id = str(freeze.get("family_id", ""))
        if not freeze_id or freeze_id in freeze_ids:
            errors.append(f"duplicate or blank freeze_id {freeze_id}")
        freeze_ids.add(freeze_id)
        if not family_id or family_id in family_ids:
            errors.append(f"duplicate or blank family_id {family_id}")
        family_ids.add(family_id)
        source_family = p10_families.get(family_id)
        if not source_family:
            errors.append(f"family absent from P10 seed {family_id}")
            continue
        if freeze.get("family_identity_sha256") != source_family.get(
            "family_identity_sha256"
        ):
            errors.append(f"family identity drift {family_id}")
        candidate_ids = freeze.get("candidate_ids", [])
        if candidate_ids != source_family.get("member_candidate_ids"):
            errors.append(f"candidate membership drift {family_id}")
            continue
        expected_candidate_hashes = [
            p10_candidates[item]["candidate_identity_sha256"] for item in candidate_ids
        ]
        expected_assumption_hashes = [
            p10_candidates[item]["assumption_sha256"] for item in candidate_ids
        ]
        if freeze.get("candidate_identity_sha256es") != expected_candidate_hashes:
            errors.append(f"candidate identity hash drift {family_id}")
        if freeze.get("assumption_sha256es") != expected_assumption_hashes:
            errors.append(f"assumption hash drift {family_id}")
        if freeze.get("disposition") != (
            "family_locally_frozen_no_adoption_no_global_no_go"
        ):
            errors.append(f"invalid freeze disposition {family_id}")

    if set(seed.get("reopening_classes", [])) != set(REOPENING_CLASSES):
        errors.append("reopening class set mismatch")
    if seed.get("barred_route_kinds") != ["rename_or_repackage"]:
        errors.append("barred route set mismatch")
    expected_flags = {
        "historical_records_mutated": False,
        "global_no_go_inferred": False,
        "candidate_adoption_authorized": False,
        "ontology_edit_authorized": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "publication_authority": False,
    }
    if seed.get("authority_flags") != expected_flags:
        errors.append("seed authority flags mismatch")
    return errors


def build_report() -> dict[str, object]:
    seed_bytes = SEED_PATH.read_bytes()
    fixture_bytes = FIXTURE_PATH.read_bytes()
    seed = json.loads(seed_bytes)
    fixture = json.loads(fixture_bytes)
    seed_errors = _validate_seed(seed)
    results: list[dict[str, object]] = []
    for case in fixture["cases"]:
        job = _merge(fixture["base_job"], case.get("job_patch", {}))
        observed = evaluate_family_freeze_admission(
            job,
            expected_admission_path=fixture["expected_admission_path"],
            created_at=fixture["created_at"],
            registry=seed,
            evidence_verifier=_fixture_evidence_verifier,
        )
        results.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "observed_status": observed["status"],
                "passed": observed["status"] == case["expected_status"],
                "match_reasons": observed["match_reasons"],
                "error_count": len(observed["errors"]),
                "theorem_truth_evaluated": observed["theorem_truth_evaluated"],
            }
        )
    passed = sum(1 for item in results if item["passed"])
    report: dict[str, object] = {
        "schema_id": "family_freeze_validation_report_v1",
        "task_id": "RT-20260722-013",
        "plan_task_id": "P12-T02",
        "policy": family_freeze_policy(),
        "seed_path": str(SEED_PATH.relative_to(REPO_ROOT)),
        "seed_sha256": hashlib.sha256(seed_bytes).hexdigest(),
        "fixture_path": str(FIXTURE_PATH.relative_to(REPO_ROOT)),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "source_hashes": seed["source_hashes"],
        "seed_error_count": len(seed_errors),
        "seed_errors": seed_errors,
        "freeze_count": len(seed["freezes"]),
        "case_count": len(results),
        "passed_case_count": passed,
        "failed_case_count": len(results) - passed,
        "results": results,
        "historical_sources_unchanged": not seed_errors,
        "fixture_evidence_is_production_authority": False,
        "local_family_freeze_preserved": True,
        "global_no_go_inferred": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }
    report["status"] = (
        "PASS" if not seed_errors and passed == len(results) else "FAIL"
    )
    return report


def receipt_for(report: dict[str, object]) -> dict[str, object]:
    return {
        "schema_id": "family_freeze_compact_receipt_v1",
        "task_id": report["task_id"],
        "plan_task_id": report["plan_task_id"],
        "status": report["status"],
        "source_hashes": report["source_hashes"],
        "seed_sha256": report["seed_sha256"],
        "fixture_sha256": report["fixture_sha256"],
        "report_sha256": hashlib.sha256(
            canonical_json(report).encode("utf-8")
        ).hexdigest(),
        "validator_ids": [
            "family_freeze_seed_source_hashes_v1",
            "family_identity_and_assumption_match_v1",
            "evidence_based_reopening_shape_v1",
            "distinct_branch_non_blocking_v1",
            "local_freeze_global_no_go_guard_v1",
        ],
        "freeze_count": report["freeze_count"],
        "case_count": report["case_count"],
        "passed_case_count": report["passed_case_count"],
        "failed_case_count": report["failed_case_count"],
        "historical_sources_unchanged": report["historical_sources_unchanged"],
        "claim_boundary_summary": (
            "Five EqSrc families remain locally frozen; repeated candidate cycles require "
            "tracked primitive theorem variation-class or protected-decision evidence; "
            "materially distinct investigations remain open; no global no-go or promotion."
        ),
        "local_family_freeze_preserved": True,
        "global_no_go_inferred": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    receipt = receipt_for(report)
    if args.write:
        REPORT_PATH.write_text(rendered(report), encoding="utf-8")
        RECEIPT_PATH.write_text(rendered(receipt), encoding="utf-8")
    else:
        expected = {REPORT_PATH: rendered(report), RECEIPT_PATH: rendered(receipt)}
        drift = [
            str(path.relative_to(REPO_ROOT))
            for path, value in expected.items()
            if not path.exists() or path.read_text(encoding="utf-8") != value
        ]
        if drift:
            report = {**report, "status": "FAIL", "drift_paths": drift}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
