from __future__ import annotations

import copy
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
    / "mechanized_checks"
    / "check_finite_local_candidate.py"
)
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "research_control" / "finite_local_candidate"
VALID_FIXTURE = FIXTURE_DIR / "valid_support_only.yaml"
TARGET_IMPORT_FIXTURE = FIXTURE_DIR / "target_import_overread.yaml"
MALFORMED_REFERENCE_FIXTURE = FIXTURE_DIR / "malformed_reference.yaml"


def load_module():
    spec = importlib.util.spec_from_file_location("check_finite_local_candidate", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FiniteLocalCandidateCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_module()
        cls.fixture = cls.checker.load_fixture(VALID_FIXTURE)

    def check(self, data):
        return self.checker.check_fixture(copy.deepcopy(data))

    def result_by_predicate(self, report, predicate):
        return next(
            result for result in report.predicate_results if result.predicate == predicate
        )

    def test_valid_fixture_produces_nonempty_support_only_output(self) -> None:
        report = self.check(copy.deepcopy(self.fixture))
        output = report.to_dict()
        self.assertEqual(report.status, "pass_support_only")
        self.assertEqual(output["checker_id"], "finite_local_candidate_checker")
        self.assertEqual(output["boundary_statement"], self.checker.BOUNDARY_STATEMENT)
        self.assertGreaterEqual(len(output["predicate_results"]), 18)
        self.assertFalse(output["tooling_error"])
        self.assertEqual(output["physics_obstruction"], "")

    def test_bottom_completeness_predicate_passes_on_valid_fixture(self) -> None:
        report = self.check(copy.deepcopy(self.fixture))
        result = self.result_by_predicate(report, "bottom_result_totality")
        self.assertEqual(result.status, "pass")

    def test_no_target_import_rejection(self) -> None:
        report = self.checker.check_path(TARGET_IMPORT_FIXTURE)
        self.assertEqual(report.status, "fail_target_import")
        self.assertIn("target_metric", report.forbidden_overread_flags)

    def test_evidence_as_adoption_rejection(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["boundary_markers"]["bridge_compatibility"] = "adopted_source_law"
        report = self.check(data)
        self.assertEqual(report.status, "fail_evidence_as_adoption")
        self.assertIn("evidence_as_adoption", report.forbidden_overread_flags)

    def test_scoped_geff_overread_rejection(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["boundary_markers"]["scoped_geff_boundary"] = "adopted"
        report = self.check(data)
        self.assertEqual(report.status, "fail_geff_overread")
        self.assertIn("geff_overread", report.forbidden_overread_flags)

    def test_process_authority_as_proof_rejection(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["boundary_markers"]["process_authority_not_proof"] = False
        report = self.check(data)
        self.assertEqual(report.status, "fail_process_authority_overread")
        self.assertIn("process_authority_as_proof", report.forbidden_overread_flags)

    def test_relabeling_invariance_failure(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["variation_relabeling"]["relabelings"][0]["map"] = [
            {"from": "tau_left", "to": "tau_right"},
            {"from": "tau_right", "to": "tau_right"},
        ]
        report = self.check(data)
        self.assertEqual(report.status, "fail_relabeling_invariance")

    def test_finite_variation_stability_failure(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["variation_relabeling"]["finite_variations"][0]["result"] = "unstable"
        report = self.check(data)
        self.assertEqual(report.status, "fail_variation_stability")

    def test_malformed_fixture_failure(self) -> None:
        report = self.checker.check_path(MALFORMED_REFERENCE_FIXTURE)
        self.assertEqual(report.status, "fail_malformed_fixture")
        self.assertTrue(
            any(
                result.predicate == "token_state_references_resolve"
                and result.status == "fail"
                for result in report.predicate_results
            )
        )

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--fixture",
            str(VALID_FIXTURE),
            "--json",
        ]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["status"], "pass_support_only")

    def test_markdown_report_contains_exact_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--fixture",
                    str(VALID_FIXTURE),
                    "--markdown",
                    str(report_path),
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = report_path.read_text(encoding="utf-8")
        self.assertIn(self.checker.BOUNDARY_STATEMENT, text)


if __name__ == "__main__":
    unittest.main()
