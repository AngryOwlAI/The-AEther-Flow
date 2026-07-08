from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "physics_payload_ratio"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PhysicsPayloadRatioPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module(
            "validate_research_control_payload_ratio",
            "validate_research_control.py",
        )

    def test_required_fixtures_match_expected_statuses(self) -> None:
        fixture_results = [
            self.validator.evaluate_physics_payload_ratio_policy_fixture(path)
            for path in sorted(FIXTURE_DIR.glob("*.yaml"))
        ]

        self.assertEqual(len(fixture_results), 5)
        for result in fixture_results:
            self.assertTrue(result["matches_expected"], result)

    def test_threshold_warning_stays_separate_from_hard_failures(self) -> None:
        report = self.validator.evaluate_physics_payload_ratio_policy_fixture(
            FIXTURE_DIR / "warn_project_system_threshold.yaml"
        )

        self.assertEqual(report["status"], "WARN")
        self.assertEqual(report["hard_failure_count"], 0)
        warning_codes = {item["code"] for item in report["warnings"]}
        self.assertIn("project_system_run_exceeds_threshold", warning_codes)
        self.assertIn("physics_payload_missing_after_threshold", warning_codes)

    def test_exempt_security_or_integrity_repair_does_not_warn(self) -> None:
        report = self.validator.evaluate_physics_payload_ratio_policy_fixture(
            FIXTURE_DIR / "good_security_repair_exception.yaml"
        )

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["warning_count"], 0)
        self.assertEqual(report["hard_failure_count"], 0)

    def test_exception_without_evidence_warns_without_blocking(self) -> None:
        report = self.validator.evaluate_physics_payload_ratio_policy_fixture(
            FIXTURE_DIR / "warn_exception_missing_evidence.yaml"
        )

        self.assertEqual(report["status"], "WARN")
        self.assertEqual(report["hard_failure_count"], 0)
        warning_codes = {item["code"] for item in report["warnings"]}
        self.assertEqual(warning_codes, {"exception_declared_without_evidence"})

    def test_process_task_physics_delta_claim_is_hard_failure(self) -> None:
        report = self.validator.evaluate_physics_payload_ratio_policy_fixture(
            FIXTURE_DIR / "bad_process_task_claims_physics_delta.yaml"
        )

        self.assertEqual(report["status"], "HARD_FAIL")
        hard_failure_codes = {item["code"] for item in report["hard_failures"]}
        self.assertEqual(hard_failure_codes, {"process_task_claims_physics_delta"})
        self.assertFalse(report["authority_boundary"]["physics_claim_authority_created"])


if __name__ == "__main__":
    unittest.main()
