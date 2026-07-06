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


class LocalCiEquivalentValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_default_plan_covers_p11_t02_required_checks(self) -> None:
        plan = self.module.command_plan()
        labels = {entry["label"] for entry in plan}
        coverage = self.module.coverage_map(plan)

        self.assertIn("memory_validate_only", labels)
        self.assertIn("current_frontier_check", labels)
        self.assertIn("compact_current_frontier_check", labels)
        self.assertIn("dependency_graph_check", labels)
        self.assertIn("task_index_validation", labels)
        self.assertIn("claim_graph_validation", labels)
        self.assertIn("claim_language_changed_lint", labels)
        self.assertIn("documentation_impact_validation", labels)
        self.assertIn("research_control_validation", labels)
        self.assertIn("research_control_diff_validation", labels)
        self.assertIn("route_signature_extraction", labels)
        self.assertIn("route_orbit_advisory", labels)
        self.assertIn("whitespace_diff_check", labels)
        self.assertNotIn("repository_smoke_tests", labels)
        self.assertTrue(all(coverage.values()))

    def test_smoke_suite_is_explicit_opt_in(self) -> None:
        default_labels = {entry["label"] for entry in self.module.command_plan()}
        smoke_labels = {entry["label"] for entry in self.module.command_plan(include_smoke_tests=True)}

        self.assertNotIn("repository_smoke_tests", default_labels)
        self.assertIn("repository_smoke_tests", smoke_labels)

    def test_report_marks_required_failures_but_keeps_boundary_fields(self) -> None:
        results = [
            {
                "label": "research_control_validation",
                "command": [".venv/bin/python", "scripts/research_control/validate_research_control.py"],
                "purpose": "test",
                "authority_level": "required-gate",
                "required": True,
                "advisory": False,
                "returncode": 1,
                "status": "FAIL",
                "stdout_tail": "",
                "stderr_tail": "failure",
            },
            {
                "label": "route_orbit_advisory",
                "command": [".venv/bin/python", "scripts/research_control/validate_route_orbits.py"],
                "purpose": "test",
                "authority_level": "advisory-diagnostic",
                "required": True,
                "advisory": True,
                "returncode": 1,
                "status": "FAIL",
                "stdout_tail": "",
                "stderr_tail": "advisory failure",
            },
        ]

        report = self.module.build_report(results, include_smoke_tests=False, repo_root=REPO_ROOT)

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["required_failure_labels"], ["research_control_validation"])
        self.assertEqual(report["advisory_failure_labels"], ["route_orbit_advisory"])
        self.assertTrue(report["operational_receipt_only"])
        self.assertTrue(report["no_physics_delta"])
        self.assertFalse(report["physics_proof_authority"])


if __name__ == "__main__":
    unittest.main()
