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
    / "closure_countermodel_generator.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("closure_countermodel_generator", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ClosureCountermodelGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_module()

    def cases_by_mode(self):
        bundle = self.generator.generate_bundle()
        return {case["mode"]: case for case in bundle["cases"]}

    def test_bundle_contains_all_modes_and_support_boundary(self) -> None:
        bundle = self.generator.generate_bundle()
        self.assertEqual(set(bundle["configured_modes"]), set(self.generator.MODES))
        self.assertEqual({case["mode"] for case in bundle["cases"]}, set(self.generator.MODES))
        self.assertEqual(bundle["case_count"], len(self.generator.MODES))
        self.assertTrue(bundle["support_only"])
        self.assertFalse(bundle["proof_authority"])
        self.assertFalse(bundle["physics_promotion_authorized"])
        self.assertEqual(bundle["boundary_statement"], self.generator.BOUNDARY_STATEMENT)

    def test_cases_are_finite_records_with_explicit_authority_flags(self) -> None:
        for mode, case in self.cases_by_mode().items():
            record = case["record"]
            self.assertEqual(record["metadata"]["countermodel_mode"], mode)
            self.assertTrue(record["metadata"]["support_only"])
            self.assertFalse(record["metadata"]["proof_authority"])
            self.assertFalse(record["metadata"]["physics_promotion_authorized"])
            self.assertEqual(
                record["metadata"]["boundary_statement"],
                self.generator.orbit_checker.BOUNDARY_STATEMENT,
            )
            self.assertGreater(len(record["typed_objects"]), 0)
            self.assertTrue(record["countermodel_metadata"]["minimal_finite_record"])
            self.assertFalse(record["countermodel_metadata"]["global_no_go_claimed"])
            for value in record["forbidden_authority"].values():
                self.assertFalse(value)

    def test_generated_records_fail_closed_in_expected_checker_modes(self) -> None:
        cases = self.cases_by_mode()
        for mode, expected_status in self.generator.EXPECTED_CHECKER_STATUS.items():
            report = self.generator.orbit_checker.check_fixture(cases[mode]["record"])
            self.assertEqual(report.status, expected_status, mode)
            self.assertTrue(report.support_only)
            self.assertFalse(report.proof_authority)

    def test_missing_composition_exposes_composition_predicate_failure(self) -> None:
        record = self.cases_by_mode()["missing_composition"]["record"]
        report = self.generator.orbit_checker.check_fixture(record)
        predicate = next(
            result
            for result in report.predicate_results
            if result.predicate == "composition_table_explicit_and_correct"
        )
        self.assertEqual(predicate.status, "fail")
        self.assertEqual(predicate.status_code, "fail_composition_table")

    def test_primitive_modes_mark_requirement_without_adoption(self) -> None:
        retainh = self.cases_by_mode()["RetainH_required"]["record"]
        genh = self.cases_by_mode()["GenH_required"]["record"]
        self.assertEqual(retainh["primitive_requirements"]["retainh"]["status"], "required")
        self.assertFalse(retainh["primitive_requirements"]["retainh"]["adopted"])
        self.assertEqual(retainh["primitive_requirements"]["genh"]["status"], "not_required")
        self.assertEqual(genh["primitive_requirements"]["genh"]["status"], "required")
        self.assertFalse(genh["primitive_requirements"]["genh"]["adopted"])
        self.assertEqual(genh["primitive_requirements"]["retainh"]["status"], "not_required")

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--mode", "all", "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["generator_id"], "closure_countermodel_generator")
        self.assertEqual(parsed["case_count"], len(self.generator.MODES))
        self.assertFalse(parsed["proof_authority"])

    def test_cli_writes_one_fixture_per_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_dir = Path(temp_dir) / "fixtures"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--mode",
                    "all",
                    "--fixture-dir",
                    str(fixture_dir),
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            files = sorted(path.name for path in fixture_dir.glob("*.json"))
            self.assertEqual(files, sorted(f"{mode}.json" for mode in self.generator.MODES))
            record = json.loads((fixture_dir / "missing_identity.json").read_text())
        self.assertEqual(record["metadata"]["countermodel_mode"], "missing_identity")

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
        self.assertIn(self.generator.BOUNDARY_STATEMENT, text)


if __name__ == "__main__":
    unittest.main()
