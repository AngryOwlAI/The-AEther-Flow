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


class RouteSignatureExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = load_module("extract_route_signatures", "extract_route_signatures.py")

    def test_recent_matter_coupling_report_uses_v15_schema_and_is_advisory(self) -> None:
        report = self.extractor.build_report(REPO_ROOT, sample="recent-matter-coupling")

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["schema_id"], "route_signature_pilot_report_v1")
        self.assertEqual(report["signature_schema_id"], "route_signature_schema_v1")
        self.assertFalse(report["pilot_blocks_research"])
        self.assertFalse(report["route_orbit_warning_should_emit"])
        self.assertEqual(report["task_count"], 23)
        self.assertEqual(report["route_signature_count"], 23)

        first_signature = report["route_signatures"][0]
        for field in self.extractor.REQUIRED_V15_FIELDS:
            self.assertIn(field, first_signature)

        no_payload_task_ids = {
            task["task_id"] for task in report["no_new_mathematical_payload_tasks"]
        }
        self.assertIn("RT-20260701-010", no_payload_task_ids)
        self.assertIn("RT-20260701-031", no_payload_task_ids)
        self.assertEqual(
            report["suggested_freeze_or_continuation_consequence"],
            "no_freeze_from_pilot_continue_to_p10_t03_freeze_threshold_policy",
        )

    def test_repeated_process_refresh_cycle_emits_advisory_warning(self) -> None:
        base = {
            "signature_schema_id": "route_signature_schema_v1",
            "source_task_id": "RT-SYN-001",
            "source_job_id": "AJ-RT-SYN-001-001",
            "source_completion_path": "",
            "target_derivation_milestone": "matter_coupling",
            "milestone_burden": "synthetic_burden",
            "object_or_claim_name": "SyntheticClaim_v1",
            "route_family": "selector",
            "role_family": "theoretical-continuation-selector",
            "mathematical_payload_class": "route_selector_only",
            "distance_to_gr_delta": {
                "effect": "no_distance_delta",
                "changed": False,
                "burden_id": "",
                "milestone": "",
            },
            "source_extension_classification": "none",
            "obstruction_id": "none",
            "freeze_criteria_status": {
                "evaluated": False,
                "triggered": False,
                "decision": "not_applicable",
                "freeze_scope": "none",
            },
            "next_route_selected": "selector",
            "new_mathematics_signature": False,
            "process_refresh_signature": True,
        }
        second = dict(base)
        second["source_task_id"] = "RT-SYN-002"
        analysis = self.extractor.summarize_route_orbits([base, second])

        self.assertEqual(analysis["repeated_burden_cycle_count"], 1)
        self.assertEqual(analysis["repeated_no_new_payload_cycle_count"], 1)
        self.assertTrue(analysis["route_orbit_warning_should_emit"])
        self.assertEqual(
            analysis["suggested_freeze_or_continuation_consequence"],
            "emit_advisory_route_orbit_warning_and_route_p10_t03_freeze_threshold_review",
        )


if __name__ == "__main__":
    unittest.main()
