from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-007/artifacts/validate_positive_provenance_gate.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("p11_t05_positive_provenance_gate", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PositiveProvenanceOperationalGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.contract = cls.validator.extract_contract()
        cls.fixtures = cls.validator.load_fixtures()
        cls.result = cls.validator.run_fixture_suite(cls.contract, cls.fixtures)

    def test_contract_has_gate_b_and_gate_c_extensions(self) -> None:
        self.assertEqual(set(self.contract["gate_profiles"]), {"gate_b", "gate_c"})
        self.assertEqual(
            set(self.contract["review_surface_integration"]),
            {"effective_metric", "detector_semantics", "matter_coupling", "field_equations"},
        )

    def test_all_seven_positive_evidence_dimensions_are_required(self) -> None:
        self.assertEqual(
            set(self.contract["required_dimensions"]),
            {
                "source_derivation",
                "uniqueness_or_quotient",
                "naturality",
                "dynamics",
                "operational_systems",
                "robustness",
                "independent_review",
            },
        )

    def test_no_target_and_validator_pass_are_not_sufficient(self) -> None:
        flags = self.contract["policy_flags"]
        self.assertTrue(flags["no_target_purity_required_for_evidence_complete"])
        self.assertFalse(flags["no_target_purity_sufficient_for_evidence_complete"])
        self.assertFalse(flags["validator_pass_sufficient_for_evidence_complete"])
        rows = {row["fixture_id"]: row for row in self.result["rows"]}
        self.assertFalse(rows["NEG-NO-TARGET-ONLY-001"]["observed_evidence_complete"])
        self.assertFalse(rows["NEG-VALIDATOR-PASS-ONLY-001"]["observed_evidence_complete"])

    def test_target_and_validator_receipts_cannot_be_source_premises(self) -> None:
        rows = {row["fixture_id"]: row for row in self.result["rows"]}
        for fixture_id in (
            "NEG-TARGET-BENCHMARK-AS-PREMISE-001",
            "NEG-VALIDATOR-RECEIPT-AS-PREMISE-001",
        ):
            self.assertFalse(rows[fixture_id]["observed_valid"])
            self.assertIn(
                "positive_gate_source_premises_source_only",
                rows[fixture_id]["observed_rule_ids"],
            )

    def test_scoped_candidate_remains_valid_without_physical_readiness(self) -> None:
        row = next(
            row
            for row in self.result["rows"]
            if row["fixture_id"] == "POS-SCOPED-CANDIDATE-REPRESENTABLE-001"
        )
        self.assertTrue(row["observed_valid"])
        self.assertFalse(row["observed_evidence_complete"])
        self.assertIn("operational_systems", row["observed_blocker_ids"])

    def test_not_applicable_is_distinct_and_cannot_complete_a_core_dimension(self) -> None:
        rows = {row["fixture_id"]: row for row in self.result["rows"]}
        self.assertFalse(rows["NEG-NOT-APPLICABLE-WITHOUT-REASON-001"]["observed_valid"])
        self.assertTrue(rows["NEG-NOT-APPLICABLE-WITH-REASON-001"]["observed_valid"])
        self.assertFalse(rows["NEG-NOT-APPLICABLE-WITH-REASON-001"]["observed_evidence_complete"])

    def test_same_context_blind_and_different_model_are_not_independent(self) -> None:
        rows = {row["fixture_id"]: row for row in self.result["rows"]}
        self.assertFalse(rows["NEG-SAME-CONTEXT-REVIEW-001"]["observed_evidence_complete"])
        self.assertFalse(rows["NEG-DIFFERENT-MODEL-REVIEW-001"]["observed_evidence_complete"])

    def test_evidence_complete_records_still_cannot_authorize_promotion(self) -> None:
        rows = {row["fixture_id"]: row for row in self.result["rows"]}
        self.assertTrue(rows["POS-GATE-B-UNIQUE-001"]["observed_evidence_complete"])
        self.assertTrue(rows["POS-GATE-C-REPLICATION-001"]["observed_evidence_complete"])
        self.assertFalse(rows["NEG-PHYSICS-PROMOTION-TRUE-001"]["observed_valid"])

    def test_every_fixture_matches_its_expected_gate_result(self) -> None:
        self.assertEqual(self.result["unexpected"], [], json.dumps(self.result, sort_keys=True))
        self.assertGreaterEqual(len(self.result["rows"]), 24)

    def test_generated_outputs_are_byte_deterministic(self) -> None:
        first = self.validator.generated_outputs()
        second = self.validator.generated_outputs()
        self.assertEqual(first, second)

    def test_written_outputs_match_rebuild(self) -> None:
        result = self.validator.check_outputs()
        self.assertEqual(result["status"], "PASS", json.dumps(result, sort_keys=True))
        self.assertEqual(result["drift_paths"], [])


if __name__ == "__main__":
    unittest.main()
