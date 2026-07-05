from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "minimum_physics_payload"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MinimumPhysicsPayloadValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module(
            "validate_minimum_physics_payload",
            "validate_minimum_physics_payload.py",
        )

    def test_required_fixtures_match_expected_statuses(self) -> None:
        report = self.validator.evaluate_fixture_dir(FIXTURE_DIR)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["fixture_count"], 12)
        for result in report["fixture_results"]:
            self.assertTrue(result["matches_expected"], result)

    def test_three_same_burden_no_payload_hard_gates(self) -> None:
        fixture_id, expected, records = self.validator.load_fixture(
            FIXTURE_DIR / "bad_three_same_burden_selector_no_payload.yaml"
        )
        report = self.validator.evaluate_records(records, sample=fixture_id)

        self.assertEqual(expected, "HARD_GATE")
        self.assertEqual(report["status"], "HARD_GATE")
        codes = {item["code"] for item in report["hard_gates"]}
        self.assertIn("three_same_burden_no_payload_route_orbit", codes)

    def test_two_weak_same_burden_warns_without_hard_gate(self) -> None:
        fixture_id, expected, records = self.validator.load_fixture(
            FIXTURE_DIR / "warn_two_weak_same_burden.yaml"
        )
        report = self.validator.evaluate_records(records, sample=fixture_id)

        self.assertEqual(expected, "WARN")
        self.assertEqual(report["status"], "WARN")
        self.assertEqual(report["hard_gate_count"], 0)
        codes = {item["code"] for item in report["warnings"]}
        self.assertIn("two_same_burden_weak_payload", codes)

    def test_live_opt_in_scan_does_not_reclassify_historical_tasks(self) -> None:
        report = self.validator.evaluate_records(
            self.validator.live_opt_in_records(REPO_ROOT),
            sample="live-opt-in",
        )

        self.assertIn(report["status"], {"PASS", "WARN"})
        self.assertEqual(report["hard_gate_count"], 0)
        self.assertTrue(report["authority_boundary"]["validator_is_project_control_only"])
        self.assertFalse(report["authority_boundary"]["physics_claim_authority_created"])


if __name__ == "__main__":
    unittest.main()
