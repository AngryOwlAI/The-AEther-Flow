#!/usr/bin/env python3
"""Validate the exact P4-T06 project-system recovery without scientific inference."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control import validate_research_control as validator  # noqa: E402
from scripts.research_control.strict_yaml import load as load_yaml  # noqa: E402


TASK_ID = "RT-20260725-001"
JOB_ID = "AJ-RT-20260725-001-001"
SOURCE_TASK_ID = "RT-20260724-010"
SOURCE_JOB_ID = "AJ-RT-20260724-010-001"
GENERATED_AT = "2026-07-25T02:15:00Z"
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260725-001/artifacts/"
    "p4_t06_protected_canonical_recovery_receipt.json"
)

PROTECTED_HASHES = {
    "ontology/tex/aether_flow_foundations.tex": "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_dynamics.tex": "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_geometry.tex": "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7",
    "ontology/pdfs/aether_flow_foundations.pdf": "d20d56e71f7c91230649219216fba45c3078ac4d59dd355ade6bf682923d657c",
    "ontology/pdfs/aether_flow_dynamics.pdf": "3af0e28bb55cee17ec820cbe5b7551c5b60e662bc53f8bb48dc7e23ea36763e0",
    "ontology/pdfs/aether_flow_geometry.pdf": "f71b08bead7217bd3606a5ddd2591871beaae183367fc001f9cac9f80cd513b9",
    "research_control/design/epistemic_category_glossary.md": "f61f6dd611b9b4999af779c4ee811b4339dff235abaa1e7236e2f36e9f5b8c50",
    "research_control/design/frontier_theorem_inventory.md": "fa7d97207315b49517e6e05bc3ae5b6bfcd0e335b669ba6a98371e55b4721600",
    "research_control/design/gr_derivation_burden_map.md": "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "research_control/tasks/RT-20260721-009/artifacts/v21_burden_definitions_v1.yaml": "67b8053baa60db4b11ee20582633d6279523d40b2ee853a6c570e2fdc1d113f5",
    "research_control/tasks/RT-20260724-010/00_TASK.yaml": "d105660a4fa96c961820f53a7904a5737c764de488a28e782a628cbdc67b46ed",
    "research_control/tasks/RT-20260724-010/DDR-20260724-010.md": "677649c6d617d5dce6221f204e6081903158ceef72a496196f7bc71ed3610e7e",
    "research_control/tasks/RT-20260724-010/artifacts/child_phys_math_p4_t06_ontology_integration.yaml": "db8d26111391e2f4e3fea8c3990fdbeab25b4c0cd5ed6aaf86f95c773cc98ab8",
    "research_control/tasks/RT-20260724-010/artifacts/child_phys_phil_p4_t06_ontology_integration.yaml": "a4c5bde1ca2bb0000bd22867a733c16f390cf75e094127c3699c8073cdfd2d60",
    "research_control/tasks/RT-20260724-010/artifacts/hybrid_ontology_language_deprecation_v1.yaml": "003443ebe517daf938bd3ccf54fdca04aa5e34cc552367f03c6c4ddffa83a155",
    "research_control/tasks/RT-20260724-010/artifacts/p4_t06_canonical_integration_validation_v1.json": "2de85c3c95adc7f64cda6ba58c7bec287e2c2cdc2db1f4d2fd1eaf5890f0a351",
    "research_control/tasks/RT-20260724-010/artifacts/parent_conflict_review_p4_t06_ontology_integration.yaml": "52406a817a3d7d720c14b465bec825f590aaf75406e4740dc9ca9bd06c06c243",
    "research_control/tasks/RT-20260724-010/artifacts/parent_fusion_notes_p4_t06_ontology_integration.md": "b72800e6676e02c9a3a53ae27676fde19018aa3892021f41eaacdabf6e66779d",
    "research_control/tasks/RT-20260724-010/artifacts/selected_ontology_regime_assumption_delta_v1.yaml": "588a861880fd804be62cd1215a6d1f4aa70aaed0e48a2363c9aaf84c14ae8139",
    "research_control/tasks/RT-20260724-010/artifacts/selected_ontology_regime_burden_dependency_v1.yaml": "bf8a149d803715357d3ad48c0e1c1f5ed938c0931e3028e820012fa6d2bb8703",
    "research_control/tasks/RT-20260724-010/artifacts/selected_ontology_regime_claim_vocabulary_v1.yaml": "a183bd59fa5e0a5e20bb23bfbb0d73b8153a724ff2059855ca2b060051d4607c",
    "research_control/tasks/RT-20260724-010/artifacts/selected_ontology_regime_integration_v1.tex": "02e624b1e79f0212c5c295ec2df9a9d4d42720708e724101194090175e5bc03e",
    "research_control/tasks/RT-20260724-010/artifacts/validate_p4_t06_canonical_integration.py": "028584dff969ab27a66ea30371d885d05a3ebe65185a2a5560c70052bf045be5",
    "research_control/tasks/RT-20260724-010/artifacts/validation_blocker_protected_canonical_integration_admission_v1.yaml": "a76b245296f3bafba30fc1343fffd1a9208675b9d4bad5c8839e1c6719c911e8",
    "research_control/tasks/RT-20260724-010/documentation_impact.yaml": "46b6c89a4ca91d217f87801bcfd73b9a1a25e05e21f3f658b3dba92ce7677979",
    "research_control/tasks/RT-20260724-010/jobs/AJ-RT-20260724-010-001.yaml": "ac923add390dee54363ff21bea39b340386de5910cbbe961caf7bb03afdb3194",
    "research_control/tasks/RT-20260724-010/jobs/completions/AJC-AJ-RT-20260724-010-001.yaml": "aadf750c91486d1085a1ec99294add8d26008e0382176ee17aa74da74591c402",
    "research_control/tasks/RT-20260724-010/roles/ontology-formalizer@0.2.0--RT-20260724-010.yaml": "538fbe58c53f07c8b32ee9d88fda57c751cee48c63ea99ac6b25deb649ad4535",
    "research_control/handoffs/handoff-0860.yaml": "3b219cbf2e4b8d0d7a9f5b5f4c3a7222e174f47a5b9b371db179f96f2befd160",
    "research_control/handoffs/handoff-0860.md": "934558dbf2d67d8628fa06dff7cd0bc115d9b8a8e45d75b42283f843fe685bbd",
}

HISTORICAL_MUTABLE_OBJECTS = {
    "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS",
    "TEX-ONTOLOGY-AETHER-FLOW-DYNAMICS",
    "TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY",
    "MD-RESEARCH-CONTROL-DESIGN-EPISTEMIC-CATEGORY-GLOSSARY",
}


def check(name: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "check_id": name,
        "status": "PASS" if passed else "FAIL",
        "evidence": evidence,
    }


def build_report() -> dict[str, Any]:
    observed_hashes = {
        path: validator.sha256_file(ROOT / path)
        for path in PROTECTED_HASHES
    }
    hash_mismatches = {
        path: {"expected": expected, "observed": observed_hashes[path]}
        for path, expected in PROTECTED_HASHES.items()
        if observed_hashes[path] != expected
    }

    source_job_path = (
        ROOT
        / "research_control/tasks/RT-20260724-010/jobs/"
        "AJ-RT-20260724-010-001.yaml"
    )
    source_job = load_yaml(source_job_path)
    admission_report = validator.ValidationReport()
    admitted = validator.validate_protected_canonical_integration_admission(
        admission_report,
        {
            "job_id": SOURCE_JOB_ID,
            "task_id": SOURCE_TASK_ID,
            "role_id": "ontology-formalizer",
            "job_path": source_job_path.relative_to(ROOT).as_posix(),
        },
        source_job,
    )

    ordinary_report = validator.ValidationReport()
    validator.validate_future_physics_job_authority(
        ordinary_report,
        {
            "job_id": "AJ-NEGATIVE-CONTROL",
            "task_id": "RT-NEGATIVE-CONTROL",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-NEGATIVE-CONTROL/jobs/AJ-NEGATIVE-CONTROL.yaml",
            "created_at": "2026-06-16T20:00:00Z",
            "started_at": "",
            "completed_at": "",
        },
        {
            "allowed_write_paths": ["ontology/tex/unrelated.tex"],
            "forbidden_source_classes": sorted(
                validator.PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES
            ),
        },
    )
    ordinary_rejected = any(
        "may not allow direct write path" in error
        for error in ordinary_report.errors
    )

    active_task_id = validator.active_program_task_id()
    active_current = all(
        validator.memory_preflight_hash_must_be_current(
            {"task_id": active_task_id},
            object_id,
        )
        for object_id in HISTORICAL_MUTABLE_OBJECTS
    )
    historical_preserved = all(
        not validator.memory_preflight_hash_must_be_current(
            {"task_id": SOURCE_TASK_ID},
            object_id,
        )
        for object_id in HISTORICAL_MUTABLE_OBJECTS
    )

    checks = [
        check(
            "protected_p4_t06_payload_hashes_preserved",
            not hash_mismatches,
            {
                "protected_path_count": len(PROTECTED_HASHES),
                "mismatches": hash_mismatches,
            },
        ),
        check(
            "exact_protected_canonical_integration_admitted",
            admitted and not admission_report.errors,
            {"errors": admission_report.errors},
        ),
        check(
            "exact_six_path_contract",
            set(validator.PROTECTED_CANONICAL_INTEGRATION_PATHS)
            == {
                "ontology/tex/aether_flow_foundations.tex",
                "ontology/tex/aether_flow_dynamics.tex",
                "ontology/tex/aether_flow_geometry.tex",
                "ontology/pdfs/aether_flow_foundations.pdf",
                "ontology/pdfs/aether_flow_dynamics.pdf",
                "ontology/pdfs/aether_flow_geometry.pdf",
            },
            sorted(validator.PROTECTED_CANONICAL_INTEGRATION_PATHS),
        ),
        check(
            "ordinary_direct_ontology_write_still_rejected",
            ordinary_rejected,
            {"errors": ordinary_report.errors},
        ),
        check(
            "four_changed_objects_use_history_preserving_rule",
            HISTORICAL_MUTABLE_OBJECTS.issubset(
                validator.MUTABLE_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS
            ),
            sorted(HISTORICAL_MUTABLE_OBJECTS),
        ),
        check(
            "active_current_and_historical_immutable_semantics",
            active_current and historical_preserved,
            {
                "active_task_requires_current_hash": active_current,
                "historical_task_preserves_observed_hash": historical_preserved,
            },
        ),
    ]
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p4_t06_protected_canonical_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "generated_at": GENERATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "authority_boundary": {
            "operational_validation_only": True,
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
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
