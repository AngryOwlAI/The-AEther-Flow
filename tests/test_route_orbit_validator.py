from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RouteOrbitValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = load_module("extract_route_history", "extract_route_history.py")
        cls.validator = load_module("validate_route_orbits", "validate_route_orbits.py")

    def signature(self, task_id: str, **updates):
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
        signature.update(updates)
        signature["signature_hash"] = self.extractor.compute_signature_hash(signature)
        return signature

    def test_hard_failure_detects_repeated_route_without_progress(self) -> None:
        signatures = [
            self.signature("RT-SYNTH-01"),
            self.signature("RT-SYNTH-02"),
        ]
        report = self.validator.validate_route_history(
            {
                "schema_id": "route_history_extractor_v1",
                "sample": "",
                "task_count": 2,
                "signatures": signatures,
                "extraction_errors": [],
            }
        )

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["hard_failure_count"], 1)
        self.assertEqual(report["hard_failures"][0]["code"], "hard_route_orbit_candidate")

    def test_repeated_new_payload_warns_without_route_cycle_control(self) -> None:
        signatures = [
            self.signature("RT-SYNTH-01", new_mathematical_payload_exists=True, payload_type="definition"),
            self.signature(
                "RT-SYNTH-02",
                new_mathematical_payload_exists=True,
                payload_type="definition",
                route_cycle_control_present=True,
            ),
        ]
        report = self.validator.validate_route_history(
            {
                "schema_id": "route_history_extractor_v1",
                "sample": "",
                "task_count": 2,
                "signatures": signatures,
                "extraction_errors": [],
            }
        )

        warning_codes = {warning["code"] for warning in report["warnings"]}
        self.assertIn("repeated_burden_new_payload_missing_route_cycle_control", warning_codes)
        self.assertEqual(report["hard_failure_count"], 0)

    def test_recent_matter_rr_e_sample_has_no_hard_failures_or_gate_sync_warning(self) -> None:
        route_history = self.extractor.build_route_history(REPO_ROOT, sample="recent-matter-rr-e")
        report = self.validator.validate_route_history(route_history)

        self.assertEqual(route_history["extraction_errors"], [])
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["hard_failure_count"], 0)
        warning_codes = {warning["code"] for warning in report["warnings"]}
        self.assertNotIn("scoped_gate_followed_by_construction_before_boundary_sync", warning_codes)


if __name__ == "__main__":
    unittest.main()
