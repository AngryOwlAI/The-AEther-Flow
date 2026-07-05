from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "status_field_compatibility"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class StatusFieldCompatibilityValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module(
            "validate_status_field_compatibility",
            "validate_status_field_compatibility.py",
        )

    def test_required_fixtures_match_expected_statuses(self) -> None:
        report = self.validator.evaluate_fixture_dir(FIXTURE_DIR)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["fixture_count"], 7)
        for result in report["fixture_results"]:
            self.assertTrue(result["matches_expected"], result)

    def test_future_broad_promotion_without_layer_hard_gates(self) -> None:
        fixture_id, expected, records = self.validator.load_fixture(
            FIXTURE_DIR / "bad_future_physics_promotion_missing_layer.yaml"
        )
        report = self.validator.evaluate_records(records, sample=fixture_id)

        self.assertEqual(expected, "HARD_GATE")
        self.assertEqual(report["status"], "HARD_GATE")
        codes = {item["code"] for item in report["hard_gates"]}
        self.assertIn("future_physics_promotion_missing_layer", codes)

    def test_historical_scoped_context_warns_at_most(self) -> None:
        fixture_id, expected, records = self.validator.load_fixture(
            FIXTURE_DIR / "warn_historical_scoped_broad_field.yaml"
        )
        report = self.validator.evaluate_records(records, sample=fixture_id)

        self.assertEqual(expected, "WARN")
        self.assertEqual(report["status"], "WARN")
        self.assertEqual(report["hard_gate_count"], 0)
        codes = {item["code"] for item in report["warnings"]}
        self.assertIn("historical_physics_promotion_requires_context", codes)

    def test_good_future_scoped_record_passes_without_promotion(self) -> None:
        fixture_id, expected, records = self.validator.load_fixture(
            FIXTURE_DIR / "good_future_scoped_evidence.yaml"
        )
        report = self.validator.evaluate_records(records, sample=fixture_id)

        self.assertEqual(expected, "PASS")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["hard_gate_count"], 0)
        self.assertEqual(report["warning_count"], 0)
        self.assertTrue(report["authority_boundary"]["validator_is_project_control_only"])
        self.assertFalse(report["authority_boundary"]["physics_claim_authority_created"])


if __name__ == "__main__":
    unittest.main()
