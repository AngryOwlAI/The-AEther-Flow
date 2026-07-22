from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "research_control/tasks/RT-20260722-011/artifacts/validate_p11_scientific_qa_non_regression.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("p11_t08_non_regression", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load P11-T08 validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class P11ScientificQANonRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.matrix, cls.validation, cls.receipt = cls.validator.generated()

    def test_all_critical_cases_pass(self) -> None:
        self.assertEqual(self.matrix["status"], "PASS")
        self.assertEqual(self.matrix["failed_case_count"], 0)

    def test_two_exact_limitations_are_preserved(self) -> None:
        self.assertEqual(self.matrix["finding_ids"], ["P11-QA-F001", "P11-QA-F002"])
        self.assertEqual(self.matrix["limitation_count"], 2)

    def test_bounded_rollout_does_not_authorize_unattended_automation(self) -> None:
        self.assertEqual(self.matrix["rollout_disposition"], "BOUNDED_ROLLOUT_WITH_GUARDRAILS_UNATTENDED_AUTOMATION_FROZEN")
        self.assertEqual(len(self.matrix["mandatory_guardrails"]), 4)

    def test_authority_flags_remain_false(self) -> None:
        self.assertTrue(self.validation["authority_flags"])
        self.assertFalse(any(self.validation["authority_flags"].values()))

    def test_compact_receipt_matches_validation(self) -> None:
        self.assertEqual(self.receipt["status"], "PASS")
        self.assertEqual(self.receipt["repair_obligation_ids"], ["P11-QA-F001", "P11-QA-F002"])
        self.assertFalse(self.receipt["authority_flags"]["physics_promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
