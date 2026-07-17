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
    / "support_formalization"
    / "typed_eqsrc_orbit_checker.py"
)
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "research_control" / "typed_eqsrc_orbit"
VALID_FIXTURE = FIXTURE_DIR / "valid_support_only.yaml"
ORBIT_CLOSURE_FAILURE = FIXTURE_DIR / "orbit_closure_failure.yaml"
TYPE_MISMATCH_FIXTURE = FIXTURE_DIR / "type_mismatch.yaml"
TARGET_IMPORT_FIXTURE = FIXTURE_DIR / "target_import_overread.yaml"


def load_module():
    spec = importlib.util.spec_from_file_location("typed_eqsrc_orbit_checker", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TypedEqSrcOrbitCheckerTests(unittest.TestCase):
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

    def test_valid_fixture_produces_support_only_pass(self) -> None:
        report = self.check(copy.deepcopy(self.fixture))
        output = report.to_dict()
        self.assertEqual(report.status, "pass_support_only")
        self.assertEqual(output["checker_id"], "typed_eqsrc_orbit_checker")
        self.assertTrue(output["support_only"])
        self.assertFalse(output["proof_authority"])
        self.assertFalse(output["physics_promotion_authorized"])
        self.assertEqual(output["boundary_statement"], self.checker.BOUNDARY_STATEMENT)
        self.assertGreaterEqual(len(output["predicate_results"]), 12)
        self.assertEqual(output["checked_counts"]["typed_objects"], 3)

    def test_identity_inverse_and_composition_predicates_pass(self) -> None:
        report = self.check(copy.deepcopy(self.fixture))
        for predicate in (
            "identity_maps_explicit_and_total",
            "inverse_maps_declared_and_verified",
            "composition_table_explicit_and_correct",
        ):
            self.assertEqual(self.result_by_predicate(report, predicate).status, "pass")

    def test_orbit_closure_failure_is_fail_closed(self) -> None:
        report = self.checker.check_path(ORBIT_CLOSURE_FAILURE)
        self.assertEqual(report.status, "fail_orbit_closure")
        self.assertEqual(
            self.result_by_predicate(report, "maps_preserve_orbit_closure").status,
            "fail",
        )

    def test_type_mismatch_is_rejected(self) -> None:
        report = self.checker.check_path(TYPE_MISMATCH_FIXTURE)
        self.assertEqual(report.status, "fail_type_mismatch")

    def test_target_import_overread_is_rejected(self) -> None:
        report = self.checker.check_path(TARGET_IMPORT_FIXTURE)
        self.assertEqual(report.status, "fail_target_import")
        self.assertIn("target_metric_imported", report.forbidden_overread_flags)

    def test_proof_authority_overread_is_rejected(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["metadata"]["proof_authority"] = True
        data["forbidden_authority"]["proof_authority"] = True
        report = self.check(data)
        self.assertEqual(report.status, "fail_authority_overread")
        self.assertIn("proof_authority", report.forbidden_overread_flags)

    def test_missing_composition_table_fails_closed(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["composition_table"] = []
        report = self.check(data)
        self.assertEqual(report.status, "fail_malformed_record")
        self.assertEqual(
            self.result_by_predicate(report, "composition_table_explicit_and_correct").status,
            "fail",
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
        self.assertFalse(parsed["proof_authority"])

    def test_markdown_report_contains_boundary(self) -> None:
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
