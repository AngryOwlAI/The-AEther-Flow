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


class RouteHistoryExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = load_module("extract_route_history", "extract_route_history.py")

    def test_recent_route_signature_matches_schema_and_hash(self) -> None:
        report = self.extractor.build_route_history(
            REPO_ROOT,
            task_ids=["RT-20260702-018"],
        )
        self.assertEqual(report["extraction_errors"], [])
        self.assertEqual(report["signature_count"], 1)
        signature = report["signatures"][0]

        self.assertEqual(signature["signature_schema_id"], "route_signature_definition_v1")
        self.assertEqual(signature["source_task_id"], "RT-20260702-018")
        self.assertEqual(signature["implementation_plan_id"], "recommendations_implementation_plan_continue_task-v14")
        self.assertEqual(signature["plan_task_id"], "P8-T01")
        self.assertEqual(signature["object_name"], "route_signature_definition_v1")
        self.assertEqual(signature["signature_hash"], self.extractor.compute_signature_hash(signature))

    def test_recent_matter_rr_e_sample_covers_gate_and_boundary_sync(self) -> None:
        report = self.extractor.build_route_history(
            REPO_ROOT,
            sample="recent-matter-rr-e",
        )
        self.assertEqual(report["extraction_errors"], [])
        signatures = {signature["source_task_id"]: signature for signature in report["signatures"]}

        self.assertEqual(
            signatures["RT-20260701-030"]["gate_chair_state"],
            "scoped_evidence_or_precondition_accepted",
        )
        self.assertEqual(
            signatures["RT-20260701-031"]["boundary_synchronization_state"],
            "synchronized",
        )
        self.assertIn("RT-20260701-030", signatures["RT-20260701-031"]["previous_task_ids"])
        self.assertEqual(signatures["RT-20260701-031"]["object_family"], "rr_e")


if __name__ == "__main__":
    unittest.main()
