from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.research_control import scientific_quality_metrics as metrics


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260723-004"
    / "artifacts"
    / "fixtures"
    / "scientific_quality_metric_cases.json"
)


class ScientificQualityMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_suite = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_exact_eight_nonaggregated_metric_families(self) -> None:
        self.assertEqual(len(metrics.REQUIRED_METRIC_IDS), 8)
        self.assertEqual(
            set(metrics.REQUIRED_METRIC_IDS),
            set(metrics.METRIC_SPECS),
        )
        report = metrics.build_repository_report(REPO_ROOT)
        self.assertEqual(report["metric_count"], 8)
        self.assertIsNone(report["aggregate_metric"])
        self.assertFalse(
            report["authority_boundary"][
                "aggregate_scientific_truth_score_created"
            ]
        )

    def test_calibration_fixture_suite(self) -> None:
        covered: set[str] = set()
        for case in self.fixture_suite["cases"]:
            with self.subTest(case_id=case["case_id"]):
                result = metrics.evaluate_metric(
                    case["metric_id"],
                    case["evidence"],
                )
                warning_codes = sorted(
                    warning["code"] for warning in result["warnings"]
                )
                self.assertEqual(result["status"], case["expected_status"])
                self.assertEqual(result["value"], case["expected_value"])
                self.assertEqual(
                    warning_codes,
                    sorted(case["expected_warning_codes"]),
                )
                self.assertFalse(
                    result["authority_boundary"][
                        "physics_promotion_authorized"
                    ]
                )
                covered.add(case["metric_id"])
        self.assertEqual(covered, set(metrics.REQUIRED_METRIC_IDS))

    def test_unknown_denominator_is_not_measured_not_zero(self) -> None:
        result = metrics.evaluate_metric(
            "assumption_reduction_rate",
            metrics.unknown_metric_evidence("missing corpus", ["fixture/source"]),
        )
        self.assertEqual(result["status"], "not_measured")
        self.assertIsNone(result["value"])
        self.assertIsNone(result["denominator"]["value"])
        self.assertIn(
            "unknown_denominator",
            {warning["code"] for warning in result["warnings"]},
        )

    def test_alias_binding_fails_anti_splitting_guard(self) -> None:
        binding = "a" * 64
        result = metrics.evaluate_metric(
            "theorem_generality_rate",
            {
                "denominator_status": "known",
                "eligible_items": [
                    {
                        "identity": "APP-1",
                        "identity_sha256": binding,
                        "identity_kind": "declared_theorem_application",
                        "source_path": "fixture/one",
                    },
                    {
                        "identity": "APP-2",
                        "identity_sha256": binding,
                        "identity_kind": "declared_theorem_application",
                        "source_path": "fixture/two",
                    },
                ],
                "qualifying_ids": [],
            },
        )
        self.assertEqual(result["status"], "invalid")
        self.assertIn(
            "artifact_splitting_or_alias",
            {warning["code"] for warning in result["warnings"]},
        )

    def test_obstruction_population_excludes_prose_and_composite_lists(self) -> None:
        records = [
            {
                "obstruction_id": "No new obstruction is recorded.",
                "completion_path": "fixture/prose",
                "text": "",
            },
            {
                "obstruction_id": "OB-A | OB-B",
                "completion_path": "fixture/composite",
                "text": "",
            },
            {
                "obstruction_id": "OB-VALID-001",
                "completion_path": "fixture/valid",
                "text": "",
            },
            {
                "obstruction_id": "",
                "completion_path": "fixture/reuse",
                "text": "Later result explicitly reuses OB-VALID-001.",
            },
        ]
        evidence = metrics._obstruction_reuse_evidence(REPO_ROOT, records)
        result = metrics.evaluate_metric(
            "obstruction_unification_and_reuse_rate",
            evidence,
        )
        self.assertEqual(result["status"], "measured")
        self.assertEqual(result["denominator"]["eligible_ids"], ["OB-VALID-001"])
        self.assertEqual(result["numerator"]["qualifying_ids"], ["OB-VALID-001"])
        self.assertEqual(result["value"], 1.0)

    def test_live_ledger_metrics_are_identity_bound(self) -> None:
        report = metrics.build_repository_report(REPO_ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["raw_volume_is_primary_quality"])
        for metric_id in (
            "retraction_repair_visibility_rate",
            "ledger_durability_rate",
        ):
            record = report["metrics"][metric_id]
            self.assertEqual(record["status"], "measured")
            self.assertGreater(record["denominator"]["value"], 0)
            for item in record["denominator"]["eligible_items"]:
                self.assertRegex(item["identity_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
