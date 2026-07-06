from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "collect_validation_artifacts.py"


def load_module():
    spec = importlib.util.spec_from_file_location("collect_validation_artifacts", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidationArtifactCollectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def sample_full_report(self) -> dict:
        return {
            "schema_id": "research_control_local_ci_equivalent_report_v1",
            "generated_at": "2026-07-06T00:00:00Z",
            "status": "PASS",
            "required_failure_labels": [],
            "advisory_failure_labels": ["route_orbit_advisory"],
            "required_check_coverage": {
                "memory_validate_only": True,
                "research_control_validation": True,
            },
            "commands": [
                {
                    "label": "memory_validate_only",
                    "status": "PASS",
                    "returncode": 0,
                    "required": True,
                    "advisory": False,
                    "authority_level": "required-gate",
                    "purpose": "test",
                    "command": [".venv/bin/python", "bootstrap.py"],
                },
                {
                    "label": "route_orbit_advisory",
                    "status": "FAIL",
                    "returncode": 1,
                    "required": True,
                    "advisory": True,
                    "authority_level": "advisory-diagnostic",
                    "purpose": "test",
                    "command": [".venv/bin/python", "route.py"],
                },
            ],
        }

    def test_summary_preserves_operational_boundary(self) -> None:
        summary = self.module.build_summary(self.sample_full_report(), repo_root=REPO_ROOT)

        self.assertEqual(summary["status"], "PASS")
        self.assertTrue(summary["operational_receipt_only"])
        self.assertTrue(summary["no_physics_delta"])
        self.assertFalse(summary["physics_proof_authority"])
        self.assertIn("not physics proof authority", summary["boundary_note"])
        self.assertEqual(summary["command_counts"]["required_non_advisory_total"], 1)
        self.assertEqual(summary["command_counts"]["required_non_advisory_passed"], 1)
        self.assertEqual(summary["command_counts"]["advisory_total"], 1)
        self.assertEqual(summary["command_counts"]["advisory_passed"], 0)

    def test_required_non_advisory_failure_fails_summary(self) -> None:
        report = self.sample_full_report()
        report["status"] = "FAIL"
        report["required_failure_labels"] = ["memory_validate_only"]
        report["commands"][0]["status"] = "FAIL"

        summary = self.module.build_summary(report, repo_root=REPO_ROOT)

        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["required_failure_labels"], ["memory_validate_only"])

    def test_markdown_contains_command_table_and_boundaries(self) -> None:
        summary = self.module.build_summary(self.sample_full_report(), repo_root=REPO_ROOT)

        markdown = self.module.render_markdown(summary)

        self.assertIn("# Validation Summary", markdown)
        self.assertIn("operational receipt only", markdown)
        self.assertIn("not physics proof authority", markdown)
        self.assertIn("| memory_validate_only | PASS | true | false | required-gate |", markdown)

    def test_main_writes_json_and_markdown_from_source_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.json"
            json_output = root / "validation_summary.json"
            markdown_output = root / "validation_summary.md"
            source.write_text(json.dumps(self.sample_full_report()), encoding="utf-8")

            exit_code = self.module.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--source-report",
                    str(source),
                    "--output-json",
                    str(json_output),
                    "--output-markdown",
                    str(markdown_output),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(json_output.read_text(encoding="utf-8"))["status"], "PASS")
            self.assertIn("Validation Summary", markdown_output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
