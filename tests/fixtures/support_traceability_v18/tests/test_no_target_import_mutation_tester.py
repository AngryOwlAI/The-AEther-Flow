from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "no_target_import_mutation_tester.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "no_target_import_mutation_tester", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class NoTargetImportMutationTesterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tester = load_module()

    def test_report_contains_plan_mutations_and_support_boundary(self) -> None:
        report = self.tester.generate_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            tuple(report["configured_mutations"]),
            (
                "insert_target_metric_premise",
                "insert_proper_time_normalization",
                "insert_empirical_detector_protocol",
                "insert_stress_energy_semantics",
                "insert_matter_action_premise",
                "insert_benchmark_behavior_premise",
                "insert_validator_as_proof_premise",
            ),
        )
        self.assertEqual(report["mutation_count"], len(self.tester.MUTATIONS))
        self.assertEqual(report["base_safe_text_status"], "PASS")
        self.assertTrue(report["support_only"])
        self.assertFalse(report["proof_authority"])
        self.assertFalse(report["physics_promotion_authorized"])
        self.assertFalse(report["source_law_adopted"])
        self.assertFalse(report["validator_behavior_changed"])

    def test_each_mutation_fails_closed_with_expected_linter_classes(self) -> None:
        report = self.tester.generate_report()
        for result in report["mutation_results"]:
            self.assertTrue(result["fail_closed"], result["mutation_id"])
            self.assertEqual(result["observed_status"], "FAIL", result["mutation_id"])
            self.assertEqual(result["missing_expected_linter_class_ids"], [])
            for class_id in result["expected_linter_class_ids"]:
                self.assertIn(class_id, result["observed_linter_class_ids"])
            self.assertTrue(result["support_only"])
            self.assertFalse(result["proof_authority"])
            self.assertFalse(result["physics_promotion_authorized"])

    def test_single_mutation_selection_is_supported(self) -> None:
        report = self.tester.generate_report("insert_validator_as_proof_premise")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["mutation_count"], 1)
        result = report["mutation_results"][0]
        self.assertEqual(result["mutation_id"], "insert_validator_as_proof_premise")
        self.assertIn(
            "validator_pass_used_as_proof",
            result["observed_linter_class_ids"],
        )

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--mutation", "all", "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["tester_id"], "no_target_import_mutation_tester")
        self.assertEqual(parsed["status"], "PASS")
        self.assertFalse(parsed["proof_authority"])

    def test_cli_writes_one_fixture_per_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_dir = Path(temp_dir) / "fixtures"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--fixture-dir",
                    str(fixture_dir),
                    "--mutation",
                    "all",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            files = sorted(path.name for path in fixture_dir.glob("*.json"))
            self.assertEqual(
                files,
                sorted(f"{mutation_id}.json" for mutation_id in self.tester.MUTATION_IDS),
            )
            fixture = json.loads(
                (fixture_dir / "insert_target_metric_premise.json").read_text(
                    encoding="utf-8"
                )
            )
        self.assertIn("Target-metric certificate", fixture["mutated_text"])
        self.assertFalse(fixture["proof_authority"])

    def test_markdown_report_contains_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--markdown", str(report_path)],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = report_path.read_text(encoding="utf-8")
        self.assertIn(self.tester.BOUNDARY_STATEMENT, text)
        self.assertIn("insert_benchmark_behavior_premise", text)


if __name__ == "__main__":
    unittest.main()
