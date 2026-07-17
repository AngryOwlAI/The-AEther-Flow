from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/research_control/run_full_research_control_validation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_full_research_control_validation", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LocalFullWrapperCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_compatibility_projection_is_shared_manifest_derived(self) -> None:
        plan = self.module.command_plan()
        by_gate = {entry["gate_id"]: entry for entry in plan}
        coverage = self.module.coverage_map(plan)

        self.assertNotIn("ValidationCommand", vars(self.module))
        self.assertNotIn("base_command_plan", vars(self.module))
        self.assertEqual(
            by_gate["research_control_diff"]["command"],
            ["scripts/research_control/validate_research_control.py", "--check-diff"],
        )
        self.assertEqual(
            by_gate["research_control_diff"]["label"],
            "research_control_diff_validation",
        )
        self.assertTrue(coverage["research_control_core_obligation"])
        self.assertTrue(coverage["research_control_diff_obligation"])
        self.assertTrue(all(coverage.values()))

    def test_claim_language_summary_remains_available_to_checkpoint(self) -> None:
        summary = self.module.claim_language_summary(
            "claim-language warning scoped_obstruction\n"
        )

        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary["warning_count"], 1)
        self.assertEqual(
            summary["finding_ids"],
            ["claim_language_changed:scoped_obstruction"],
        )


if __name__ == "__main__":
    unittest.main()
