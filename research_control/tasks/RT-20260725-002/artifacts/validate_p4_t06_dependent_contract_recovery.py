#!/usr/bin/env python3
"""Validate the bounded P4-T06 dependent contract recovery."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control import validate_research_control as control_validator  # noqa: E402
from scripts.research_control.strict_yaml import load as load_yaml  # noqa: E402


TASK_ID = "RT-20260725-002"
JOB_ID = "AJ-RT-20260725-002-001"
GENERATED_AT = "2026-07-25T03:41:05Z"
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260725-002/artifacts/"
    "p4_t06_dependent_contract_recovery_receipt.json"
)

PRESERVED_HASHES = {
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json": "8cf49a04b90d02f8439b54e138257cc5c56b2a72ba2b26c43c5b1b9a5dba78a0",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_validation.json": "9323760e532acf2560342eeb1c47bd558dc861ab6d05c8db1ed40cb117c3ef8d",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_compact_receipt.json": "92a0a538cd7a1bd8cd8b4b996976a9a5c0f23bb129ca49a322b1ef3f4d21825d",
    "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_architecture_contract.json": "d5fa22e7bbc1d92f29acd6c8418d06ce7d81a042589ade77c7ba4fdebb0eda44",
    "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_architecture_validation.json": "6358f829c9e07adc6095a471621664830b37e7797c10b321b562b3f894b68b23",
    "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_architecture_compact_receipt.json": "04cc34d38b1b0125fb77c38f639895bfc49e0864ad62bfc43aba78666bef72b3",
    "research_control/tasks/RT-20260721-009/artifacts/v21_burden_definitions_v1.yaml": "67b8053baa60db4b11ee20582633d6279523d40b2ee853a6c570e2fdc1d113f5",
    "ontology/tex/aether_flow_foundations.tex": "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_dynamics.tex": "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_geometry.tex": "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7",
    "ontology/pdfs/aether_flow_foundations.pdf": "d20d56e71f7c91230649219216fba45c3078ac4d59dd355ade6bf682923d657c",
    "ontology/pdfs/aether_flow_dynamics.pdf": "3af0e28bb55cee17ec820cbe5b7551c5b60e662bc53f8bb48dc7e23ea36763e0",
    "ontology/pdfs/aether_flow_geometry.pdf": "f71b08bead7217bd3606a5ddd2591871beaae183367fc001f9cac9f80cd513b9",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "69a513d1c737f7c6b49ec03bbcb51dfc8a5a6b4063c5f2d88bb663eea286dccf",
}

EXPECTED_TASK_METADATA = {
    "title": "Integrate the selected ontology regime and retire hybrid language",
    "task_taxonomy": {
        "schema_id": "v21_task_taxonomy_v1",
        "work_kind": "integration_or_selection",
        "milestone": "source_ontology",
        "candidate_family": "unknown",
        "result_kind": "completed_or_precisely_blocked",
        "authority": "science_draft",
        "scope": "scientific",
    },
}


def sha256(relative_path: str) -> str:
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check(check_id: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "evidence": evidence,
    }


def build_report() -> dict[str, Any]:
    observed = {path: sha256(path) for path in PRESERVED_HASHES}
    mismatches = {
        path: {"expected": expected, "observed": observed[path]}
        for path, expected in PRESERVED_HASHES.items()
        if observed[path] != expected
    }

    candidate = load_module(
        "p4_t06_recovery_candidate_lineage",
        "research_control/tasks/RT-20260721-005/artifacts/"
        "validate_v21_candidate_lineage.py",
    )
    candidate_validation, candidate_receipt = candidate.validate()

    event_store = load_module(
        "p4_t06_recovery_event_store",
        "research_control/tasks/RT-20260721-007/artifacts/"
        "validate_v21_event_store_architecture.py",
    )
    event_validation, event_receipt = event_store.build_outputs(
        event_store.load_contract()
    )
    current_ledger_valid, current_ledger_evidence = (
        event_store.validate_current_distance_to_gr_authority()
    )

    p10_audit = load_module(
        "p4_t06_recovery_p10_migration",
        "research_control/tasks/RT-20260722-003/artifacts/"
        "validate_v21_p10_migration_readiness.py",
    )
    p10_validation, p10_receipt = p10_audit.build_audit()

    task_path = ROOT / "research_control/tasks/RT-20260724-010/00_TASK.yaml"
    task = load_yaml(task_path)
    task_metadata_matches = isinstance(task, dict) and all(
        task.get(key) == value for key, value in EXPECTED_TASK_METADATA.items()
    )

    definitions_text = (
        ROOT
        / "research_control/tasks/RT-20260721-009/artifacts/"
        "v21_burden_definitions_v1.yaml"
    ).read_text(encoding="utf-8")
    fixture_text = (ROOT / "tests/test_current_burden_status.py").read_text(
        encoding="utf-8"
    )
    current_required_object = (
        'required_object: "selected primitive source arena and unresolved '
        'source-order or evolution slot"'
    )
    fixture_current = (
        current_required_object in definitions_text
        and current_required_object in fixture_text
        and 'current_status: "stale fixture"' in fixture_text
        and 'required_object: "primitive substrate data"' not in fixture_text
    )

    source_job_path = (
        ROOT
        / "research_control/tasks/RT-20260724-010/jobs/"
        "AJ-RT-20260724-010-001.yaml"
    )
    source_job = load_yaml(source_job_path)
    admission_report = control_validator.ValidationReport()
    admitted = control_validator.validate_protected_canonical_integration_admission(
        admission_report,
        {
            "job_id": "AJ-RT-20260724-010-001",
            "task_id": "RT-20260724-010",
            "role_id": "ontology-formalizer",
            "job_path": source_job_path.relative_to(ROOT).as_posix(),
        },
        source_job,
    )

    checks = [
        check(
            "historical_and_protected_bytes_preserved",
            not mismatches,
            {"path_count": len(PRESERVED_HASHES), "mismatches": mismatches},
        ),
        check(
            "candidate_lineage_current_authority_pass",
            candidate_validation.get("validation_status") == "PASS"
            and candidate_receipt.get("result_status") == "PASS",
            {
                "validation_status": candidate_validation.get("validation_status"),
                "failed_check_count": candidate_validation.get("failed_check_count"),
            },
        ),
        check(
            "event_store_historical_and_current_authority_pass",
            event_validation.get("status") == "PASS"
            and event_receipt.get("validation_status") == "PASS"
            and current_ledger_valid,
            {
                "validation_status": event_validation.get("status"),
                "failed_check_count": event_validation.get("failed_check_count"),
                "current_ledger": current_ledger_evidence,
            },
        ),
        check(
            "burden_status_fixture_targets_current_definition",
            fixture_current,
            {"current_required_object_present": fixture_current},
        ),
        check(
            "p4_t06_title_and_taxonomy_exact",
            task_metadata_matches,
            {
                "title": task.get("title") if isinstance(task, dict) else None,
                "task_taxonomy": (
                    task.get("task_taxonomy") if isinstance(task, dict) else None
                ),
            },
        ),
        check(
            "protected_admission_accepts_exact_metadata_repair",
            admitted and not admission_report.errors,
            {"errors": admission_report.errors},
        ),
        check(
            "p10_migration_readiness_restored",
            p10_validation.get("audit_status") == "PASS"
            and p10_receipt.get("result_status")
            == "PASS_AUDIT_FREEZE_BROADER_ROLLOUT",
            {
                "validation_status": p10_validation.get("audit_status"),
                "receipt_status": p10_receipt.get("result_status"),
            },
        ),
    ]
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p4_t06_dependent_contract_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": "RT-20260725-001",
        "source_job_id": "AJ-RT-20260725-001-001",
        "plan_task_id": "P4-T06",
        "generated_at": GENERATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "source_hashes": observed,
        "authority_boundary": {
            "operational_validation_only": True,
            "historical_observations_rewritten": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p4_t06_reexecuted": False,
            "p5_t01_executed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    expected = json.dumps(report, indent=2, sort_keys=True) + "\n"
    drift = False
    if args.write_report:
        REPORT_PATH.write_text(expected, encoding="utf-8")
    if args.check:
        drift = not REPORT_PATH.is_file() or REPORT_PATH.read_text(
            encoding="utf-8"
        ) != expected
    result = {
        "status": (
            "PASS" if report["status"] == "PASS" and not drift else "FAIL"
        ),
        "validation_status": report["status"],
        "drift": [REPORT_PATH.relative_to(ROOT).as_posix()] if drift else [],
        "check_count": report["check_count"],
        "fail_count": report["fail_count"],
    }
    if args.json or not args.write_report:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
