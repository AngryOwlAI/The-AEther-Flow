from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "validate_metric_use_tex_references.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_metric_use_tex_references", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_ledger(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=load_module().LEDGER_HEADER)
        writer.writeheader()
        writer.writerows(rows)


def ledger_row(artifact_path: str, object_used: str) -> dict[str, str]:
    return {
        "use_id": f"MUL-TEST-{abs(hash((artifact_path, object_used))) % 100000:05d}",
        "task_id": "RT-TEST",
        "artifact_path": artifact_path,
        "object_used": object_used,
        "use_category": "blocked_physical_metric_use",
        "declared_scope": f"{object_used} appears only as support validation fixture coverage",
        "allowed_use": "Use only for validator fixture coverage",
        "forbidden_interpretations": (
            "physical_lorentzian_metric;proper_time_normalization;detector_calibration;"
            "stress_energy_semantics;matter_action_premise;Einstein_equation_premise;"
            "benchmark_fit_premise"
        ),
        "no_target_guard_path": artifact_path,
        "audit_status": "blocked_by_scope",
        "stress_status": "not_applicable",
        "created_at": "2026-07-08T13:24:00Z",
        "notes": f"Fixture row covering {object_used}",
    }


class MetricUseTexReferenceValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()

    def test_repository_configured_metric_use_tex_references_pass(self) -> None:
        report = self.validator.build_report(
            repo_root=REPO_ROOT,
            ledger_path=REPO_ROOT / self.validator.DEFAULT_LEDGER,
            failure_mode="hard-fail",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)
        self.assertGreaterEqual(report["configured_path_count"], 3)
        self.assertTrue(report["support_only"])
        self.assertFalse(report["proof_authority"])
        self.assertFalse(report["physics_promotion_authorized"])
        self.assertEqual(
            tuple(report["high_risk_classes"]),
            (
                "g_eff",
                "metricdata_e",
                "proper_time",
                "detector_calibration",
                "stress_energy",
                "matter_action",
            ),
        )

    def test_unledgered_body_references_fail_hard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tex_path = root / "artifacts" / "fixture.tex"
            tex_path.parent.mkdir(parents=True)
            tex_path.write_text(
                "\n".join(
                    [
                        "This body uses g_eff.",
                        "MetricData(E) appears as a target-looking token.",
                        "A proper time detector calibration is asserted.",
                        "Stress-energy and matter action language appears.",
                    ]
                ),
                encoding="utf-8",
            )
            ledger = root / "registries" / "METRIC_USE_LEDGER.csv"
            write_ledger(ledger, [])

            report = self.validator.build_report(
                repo_root=root,
                ledger_path=ledger,
                explicit_paths=["artifacts/fixture.tex"],
                failure_mode="hard-fail",
            )

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(
            {finding["class_id"] for finding in report["findings"]},
            {
                "g_eff",
                "metricdata_e",
                "proper_time",
                "detector_calibration",
                "stress_energy",
                "matter_action",
            },
        )

    def test_warning_mode_exits_zero_with_warn_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tex_path = root / "fixture.tex"
            tex_path.write_text("g_eff and MetricData(E) are unledgered.\n", encoding="utf-8")
            ledger = root / "registries" / "METRIC_USE_LEDGER.csv"
            write_ledger(ledger, [])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--repo-root",
                    str(root),
                    "--ledger",
                    str(ledger),
                    "--paths",
                    str(tex_path),
                    "--failure-mode",
                    "warn",
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["status"], "WARN")
        self.assertGreater(parsed["finding_count"], 0)

    def test_ledger_rows_cover_detected_classes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            artifact_path = "artifacts/fixture.tex"
            tex_path = root / artifact_path
            tex_path.parent.mkdir(parents=True)
            tex_path.write_text(
                "g_eff MetricData(E) proper time detector calibration stress-energy matter action\n",
                encoding="utf-8",
            )
            ledger = root / "registries" / "METRIC_USE_LEDGER.csv"
            write_ledger(
                ledger,
                [
                    ledger_row(artifact_path, "g_eff"),
                    ledger_row(artifact_path, "MetricData(E)"),
                    ledger_row(artifact_path, "proper_time"),
                    ledger_row(artifact_path, "detector_calibration"),
                    ledger_row(artifact_path, "stress_energy"),
                    ledger_row(artifact_path, "matter_action"),
                ],
            )

            report = self.validator.build_report(
                repo_root=root,
                ledger_path=ledger,
                explicit_paths=[artifact_path],
                failure_mode="hard-fail",
            )

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)

    def test_no_use_justification_allows_unledgered_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tex_path = root / "fixture.tex"
            tex_path.write_text(
                "% metric-use-ledger: no-use-justification all quoted negative example only\n"
                "g_eff MetricData(E) proper time detector calibration stress-energy matter action\n",
                encoding="utf-8",
            )
            ledger = root / "registries" / "METRIC_USE_LEDGER.csv"
            write_ledger(ledger, [])

            report = self.validator.build_report(
                repo_root=root,
                ledger_path=ledger,
                explicit_paths=[str(tex_path)],
                failure_mode="hard-fail",
            )

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)
        self.assertEqual(
            set(report["path_reports"][0]["no_use_justified_classes"]),
            {
                "g_eff",
                "metricdata_e",
                "proper_time",
                "detector_calibration",
                "stress_energy",
                "matter_action",
            },
        )

    def test_tex_macro_declarations_are_not_semantic_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tex_path = root / "fixture.tex"
            tex_path.write_text(
                "\\newcommand{\\geff}{g_{\\mathrm{eff}}}\n"
                "\\newcommand{\\MatterAction}{matter action}\n",
                encoding="utf-8",
            )
            ledger = root / "registries" / "METRIC_USE_LEDGER.csv"
            write_ledger(ledger, [])

            report = self.validator.build_report(
                repo_root=root,
                ledger_path=ledger,
                explicit_paths=[str(tex_path)],
                failure_mode="hard-fail",
            )

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
