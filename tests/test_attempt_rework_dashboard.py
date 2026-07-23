from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260723-011/artifacts/"
    "build_attempt_rework_dashboard.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "build_attempt_rework_dashboard", MODULE_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AttemptReworkDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_dashboard_matches_sealed_ledger_and_contextualizes_pass(self):
        dashboard, _ = self.module.build_dashboard()
        ledger = json.loads(self.module.LEDGER_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            dashboard["bounded_scope"]["event_count"], len(ledger["events"])
        )
        self.assertEqual(dashboard["headline_counts"]["repair_event_count"], 2)
        self.assertEqual(
            dashboard["pass_saturation_context"]["numerator"], 4
        )
        self.assertEqual(
            dashboard["pass_saturation_context"]["denominator"], 8
        )
        self.assertIn(
            "Operational saturation context only",
            dashboard["pass_saturation_context"]["interpretation"],
        )

    def test_failure_classes_are_typed_and_never_overread_as_physics(self):
        dashboard, _ = self.module.build_dashboard()
        failures = dashboard["failure_categories"]
        self.assertEqual(failures["syntax"], 0)
        self.assertEqual(failures["validation"], 1)
        self.assertEqual(failures["proof"], 0)
        self.assertEqual(failures["interpretation"], 1)
        self.assertEqual(failures["physics"], 0)
        self.assertFalse(
            dashboard["authority_boundary"][
                "process_failures_are_physics_refutations"
            ]
        )

    def test_abandonment_is_not_measured_without_denominator(self):
        dashboard, _ = self.module.build_dashboard()
        metric = dashboard["abandonment_metric"]
        self.assertEqual(metric["status"], "not_measured")
        self.assertEqual(metric["numerator"], 0)
        self.assertIsNone(metric["denominator"])
        self.assertIsNone(metric["value"])

    def test_private_field_and_credential_patterns_are_rejected(self):
        self.assertTrue(
            self.module.private_material_findings({"prompt_text": "do not expose"})
        )
        self.assertTrue(
            self.module.private_material_findings(
                {"safe_field": "sk-examplecredential123456"}
            )
        )
        dashboard, _ = self.module.build_dashboard()
        self.assertEqual(self.module.private_material_findings(dashboard), [])

    def test_freshness_rejects_stale_source_hash(self):
        expected = self.module.build_expected_artifacts()
        freshness = json.loads(
            expected[self.module.FRESHNESS_PATH].decode("utf-8")
        )
        observed = {
            row["path"]: row["sha256"] for row in freshness["source_bindings"]
        }
        self.assertTrue(self.module.freshness_matches(freshness, observed))
        first_path = sorted(observed)[0]
        observed[first_path] = "0" * 64
        self.assertFalse(self.module.freshness_matches(freshness, observed))

    def test_generated_artifacts_are_current(self):
        expected = self.module.build_expected_artifacts()
        self.assertEqual(self.module.check_artifacts(expected), [])


if __name__ == "__main__":
    unittest.main()
