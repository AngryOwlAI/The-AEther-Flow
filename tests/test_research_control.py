from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ResearchControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strict_yaml = load_module("strict_yaml", "strict_yaml.py")
        cls.validator = load_module("validate_research_control", "validate_research_control.py")
        cls.resolver = load_module("resolve_latest_handoff", "resolve_latest_handoff.py")
        cls.continue_research = load_module("continue_research", "continue_research.py")

    def test_strict_yaml_parses_nested_maps_and_lists(self) -> None:
        parsed = self.strict_yaml.loads(
            'name: "demo"\n'
            "enabled: true\n"
            "items:\n"
            '  - "alpha"\n'
            "nested:\n"
            '  child: "value"\n'
        )
        self.assertEqual(parsed["name"], "demo")
        self.assertTrue(parsed["enabled"])
        self.assertEqual(parsed["items"], ["alpha"])
        self.assertEqual(parsed["nested"]["child"], "value")

    def test_strict_yaml_rejects_anchors(self) -> None:
        with self.assertRaises(self.strict_yaml.StrictYamlError):
            self.strict_yaml.loads('name: &bad "demo"\n')

    def test_static_research_control_validation_passes(self) -> None:
        report = self.validator.validate_all()
        self.assertEqual(report.errors, [])

    def test_resolve_latest_handoff(self) -> None:
        latest = self.resolver.resolve_latest()
        self.assertEqual(latest["handoff_id"], "handoff-0001")
        self.assertEqual(latest["task_id"], "RT-20260608-001")

    def test_write_path_diff_rejects_undeclared_path(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-08T00:00:00Z",
                "allowed_write_paths": "research_control/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(self.validator, "changed_paths", return_value=["wiki/changed.md"]):
            self.validator.validate_diff(report, jobs, "HEAD", False)
        self.assertTrue(any("not allowed" in error for error in report.errors))

    def test_write_path_diff_accepts_declared_path(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-08T00:00:00Z",
                "allowed_write_paths": "research_control/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=["research_control/tasks/example.yaml"],
        ):
            self.validator.validate_diff(report, jobs, "HEAD", False)
        self.assertEqual(report.errors, [])

    def test_continue_research_reports_one_job_boundary(self) -> None:
        status = self.continue_research.continuation_status()
        self.assertEqual(status["status"], "ready")
        self.assertEqual(status["execution_boundary"], "one bounded AgentJob per invocation")


if __name__ == "__main__":
    unittest.main()
