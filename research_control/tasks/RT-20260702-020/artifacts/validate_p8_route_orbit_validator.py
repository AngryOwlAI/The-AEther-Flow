#!/usr/bin/env python3
"""Validate the P8-T03 route-orbit validator receipt."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, path: Path):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


extractor = load_module("extract_route_history", SCRIPT_DIR / "extract_route_history.py")
validator = load_module("validate_route_orbits", SCRIPT_DIR / "validate_route_orbits.py")


def synthetic_signature(task_id: str) -> dict:
    signature = {
        "signature_schema_id": "route_signature_definition_v1",
        "signature_id": f"route-sig-{task_id}",
        "source_task_id": task_id,
        "source_job_id": f"AJ-{task_id}-001",
        "source_completion_path": "",
        "implementation_plan_id": "recommendations_implementation_plan_continue_task-v14",
        "plan_task_id": "synthetic",
        "target_derivation_milestone": "matter_coupling",
        "milestone_burden": "missing_source_law",
        "object_family": "matter_coupling",
        "object_name": "SyntheticLaw_v1",
        "task_type": "ontology_formalization",
        "role_id": "ontology-formalizer",
        "execution_role_ref": "",
        "source_extension_category": "source_extension_candidate",
        "selected_route": "ontology_law_research_packet",
        "missing_primitive": "SyntheticLaw_v1",
        "payload_type": "none",
        "obstruction_label": "none",
        "freeze_candidate": "none",
        "boundary_synchronization_state": "pending",
        "gate_chair_state": "not_requested",
        "previous_task_ids": [],
        "new_mathematical_payload_exists": False,
        "exact_repair_attempted": False,
        "freeze_criteria_evaluated": False,
        "new_source_evidence_exists": False,
        "source_created_at": f"2026-07-02T00:00:{task_id[-2:]}Z",
        "route_cycle_control_present": False,
        "source_evidence": {},
    }
    signature["signature_hash"] = extractor.compute_signature_hash(signature)
    return signature


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    route_history = extractor.build_route_history(REPO_ROOT, sample="recent-matter-rr-e")
    sample_report = validator.validate_route_history(route_history)
    require(route_history["extraction_errors"] == [], "recent sample extraction errors must be empty")
    require(sample_report["schema_id"] == "route_orbit_validator_v1", "unexpected validator schema")
    require(sample_report["status"] == "PASS", "recent sample must pass route-orbit validation")
    require(sample_report["hard_failure_count"] == 0, "recent sample must not emit hard failures")
    warning_codes = {warning["code"] for warning in sample_report["warnings"]}
    require(
        "scoped_gate_followed_by_construction_before_boundary_sync" not in warning_codes,
        "recent sample must recognize boundary synchronization before later construction",
    )

    hard_report = validator.validate_route_history(
        {
            "schema_id": "route_history_extractor_v1",
            "sample": "synthetic-hard-fail",
            "task_count": 2,
            "signatures": [synthetic_signature("RT-SYNTH-01"), synthetic_signature("RT-SYNTH-02")],
            "extraction_errors": [],
        }
    )
    require(hard_report["status"] == "FAIL", "synthetic repeated orbit must fail")
    require(hard_report["hard_failure_count"] == 1, "synthetic repeated orbit must produce one hard failure")
    print("P8-T03 route-orbit validator receipt PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
