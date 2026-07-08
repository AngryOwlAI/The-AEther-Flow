from __future__ import annotations

import csv
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
PROJECT_SCRIPT_PATH = REPO_ROOT / "scripts" / "project_control" / "validate_claim_language.py"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "countermodel_obligations"


def load_research_validator():
    if str(RESEARCH_SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(RESEARCH_SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "validate_research_control",
        RESEARCH_SCRIPT_DIR / "validate_research_control.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_claim_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", PROJECT_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CountermodelObligationValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_research_validator()
        cls.claim_linter = load_claim_linter()

    def run_registry_fixture(self, fixture_name: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry_dir = root / "registries"
            registry_dir.mkdir(parents=True)
            shutil.copyfile(
                FIXTURE_DIR / fixture_name,
                registry_dir / "COUNTERMODEL_OBLIGATION_REGISTRY.csv",
            )
            with (registry_dir / "COUNTERMODEL_OBLIGATION_REGISTRY.csv").open(
                newline="",
                encoding="utf-8",
            ) as handle:
                for row in csv.DictReader(handle):
                    for field_name in ("artifact_path", "result_artifact"):
                        value = row[field_name]
                        if value:
                            path = root / value
                            path.parent.mkdir(parents=True, exist_ok=True)
                            path.write_text("fixture\n", encoding="utf-8")

            report = self.validator.ValidationReport()
            with (
                mock.patch.object(self.validator, "REPO_ROOT", root),
                mock.patch.object(self.validator, "REGISTRY_DIR", registry_dir),
            ):
                rows = self.validator.read_csv_rows("COUNTERMODEL_OBLIGATION_REGISTRY.csv")
                self.validator.validate_countermodel_obligation_registry(report, rows)
            return report

    def test_good_registry_passes_without_warnings(self) -> None:
        report = self.run_registry_fixture("good_registry.csv")

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_missing_slot_warns_without_hard_failure(self) -> None:
        report = self.run_registry_fixture("missing_slot_registry.csv")

        self.assertEqual(report.errors, [])
        self.assertTrue(
            any("missing_countermodel_slot" in warning for warning in report.warnings),
            report.warnings,
        )

    def test_global_no_go_claim_hard_fails(self) -> None:
        report = self.run_registry_fixture("global_no_go_registry.csv")

        self.assertTrue(
            any("countermodel_overread_as_global_no_go" in error for error in report.errors),
            report.errors,
        )

    def test_future_theorem_completion_without_obligations_warns(self) -> None:
        report = self.validator.ValidationReport()
        job_row = {
            "role_id": "candidate-constructor",
            "created_at": "2026-07-08T02:00:00Z",
            "started_at": "2026-07-08T02:00:00Z",
            "completed_at": "2026-07-08T02:00:00Z",
        }
        job_contract = {"objective": "Build a theorem attempt for EqSrc."}
        completion = {
            "completed_at": "2026-07-08T02:00:00Z",
            "verdict": "conditional theorem candidate recorded",
        }

        self.validator.validate_countermodel_obligation_completion(
            report,
            job_row,
            job_contract,
            completion,
            "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml",
        )

        self.assertEqual(report.errors, [])
        self.assertTrue(
            any("theorem_without_countermodel_justification" in warning for warning in report.warnings),
            report.warnings,
        )

    def test_claim_language_countermodel_global_no_go_hard_fails(self) -> None:
        taxonomy = self.claim_linter.load_taxonomy()
        report = self.claim_linter.report_dict(
            self.claim_linter.scan_text_map(
                {"research_control/current_frontier.md": "A local countermodel proves global no-go.\n"},
                taxonomy=taxonomy,
                reviewed_contexts=[],
                active_handoffs=set(),
            ),
            scanned_paths=["research_control/current_frontier.md"],
        )

        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            "countermodel_overread_as_global_no_go",
            {finding["class_id"] for finding in report["findings"]},
        )


if __name__ == "__main__":
    unittest.main()
