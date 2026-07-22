from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "research_control/tasks/RT-20260722-008/artifacts/build_reviewer_agreement_report.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("p11_t06_reviewer_agreement_metrics", GENERATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReviewerAgreementMetricTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.suite = cls.generator.load_suite()
        cls.report = cls.generator.build_report(cls.suite)

    def test_fixture_suite_is_valid(self) -> None:
        self.assertEqual(self.report["status"], "PASS", json.dumps(self.report["errors"], sort_keys=True))
        self.assertEqual(self.report["errors"], [])

    def test_all_five_review_axes_are_present(self) -> None:
        self.assertEqual(
            self.report["review_axes"],
            ["theorem_validity", "assumptions", "countermodels", "physical_interpretation", "claim_scope"],
        )

    def test_sources_are_lineage_linked_and_hash_checked(self) -> None:
        for review in self.suite["reviews"]:
            path = ROOT / review["source_object_path"]
            self.assertTrue(path.is_file())
            self.assertEqual(self.generator.sha256(path), review["source_object_sha256"])

    def test_disagreement_and_unresolved_conflicts_remain_visible(self) -> None:
        metrics = self.report["metrics"]
        self.assertEqual(metrics["assessment_disagreement_count"], 13)
        self.assertEqual(metrics["unresolved_conflict_count"], 13)
        self.assertEqual(len(self.report["unresolved_conflicts"]), 13)

    def test_same_context_unanimity_is_flagged_as_false_consensus_risk(self) -> None:
        risks = self.report["false_consensus_risks"]
        self.assertEqual(len(risks), 5)
        self.assertTrue(all(risk["scientific_status_effect"] == "none" for risk in risks))
        self.assertTrue(all("same_context_role_review" in risk["review_context_classes"] for risk in risks))

    def test_human_class_in_calibration_does_not_claim_human_review(self) -> None:
        human = next(review for review in self.suite["reviews"] if review["review_context"]["classification"] == "human_expert_review")
        self.assertFalse(human["review_context"]["review_executed"])
        self.assertFalse(human["review_context"]["claims"]["human_expert_review_completed"])
        self.assertEqual(self.report["metrics"]["review_execution_count"], 0)

    def test_unknown_independence_remains_explicit(self) -> None:
        self.assertEqual(self.report["metrics"]["unknown_independence_record_count"], 1)
        unknown = next(review for review in self.suite["reviews"] if review["review_context"]["classification"] == "unknown")
        self.assertTrue(all(value["relationship"] == "unknown" for value in unknown["review_context"]["dimensions"].values()))

    def test_not_assessed_is_excluded_but_counted_as_coverage_gap(self) -> None:
        metrics = self.report["metrics"]
        self.assertGreater(metrics["coverage_gap_pair_axis_count"], 0)
        self.assertEqual(metrics["eligible_pair_axis_comparison_count"], 27)

    def test_blinded_configuration_report_has_no_winner(self) -> None:
        comparison = self.report["blinded_configuration_comparison"]
        self.assertTrue(comparison["ranking_forbidden"])
        self.assertTrue(comparison["agreement_optimization_forbidden"])
        self.assertIsNone(comparison["winner"])
        self.assertEqual(len(comparison["configuration_summaries"]), 4)

    def test_consensus_and_metrics_cannot_set_scientific_status(self) -> None:
        boundary = self.report["authority_boundary"]
        self.assertFalse(boundary["consensus_sets_scientific_status"])
        self.assertFalse(boundary["metric_threshold_sets_scientific_status"])
        self.assertFalse(boundary["physics_promotion_authorized"])
        self.assertFalse(boundary["proof_authority"])

    def test_generated_outputs_are_byte_deterministic(self) -> None:
        first = self.generator.generated_outputs()
        second = self.generator.generated_outputs()
        self.assertEqual(first, second)

    def test_written_outputs_match_rebuild(self) -> None:
        result = self.generator.check_outputs()
        self.assertEqual(result["status"], "PASS", json.dumps(result, sort_keys=True))
        self.assertEqual(result["drift_paths"], [])


if __name__ == "__main__":
    unittest.main()
