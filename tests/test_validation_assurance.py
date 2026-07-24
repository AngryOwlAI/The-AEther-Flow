from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from scripts.validation import assurance

REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationAssuranceTests(unittest.TestCase):
    def test_coverage_requires_nonempty_evidence_and_floor(self) -> None:
        passing = {
            "totals": {
                "num_statements": 40,
                "num_branches": 12,
                "percent_covered": 87.5,
            }
        }
        result = assurance.evaluate_coverage(passing, minimum_percent=85.0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observed_percent"], 87.5)
        self.assertTrue(result["authority"]["operational_evidence_only"])
        self.assertFalse(result["authority"]["proof_authority"])

        below_floor = {
            "totals": {
                "num_statements": 40,
                "num_branches": 12,
                "percent_covered": 84.99,
            }
        }
        self.assertEqual(
            assurance.evaluate_coverage(below_floor, minimum_percent=85.0)["status"],
            "FAIL",
        )
        empty = {
            "totals": {
                "num_statements": 0,
                "num_branches": 0,
                "percent_covered": 100.0,
            }
        }
        self.assertEqual(
            assurance.evaluate_coverage(empty, minimum_percent=85.0)["status"],
            "FAIL",
        )

    def test_percentage_rejects_booleans_nan_and_out_of_range(self) -> None:
        base = {"totals": {"num_statements": 1, "num_branches": 0}}
        for value in (True, float("nan"), -0.01, 100.01, "99"):
            with self.subTest(value=value):
                report = {"totals": {**base["totals"], "percent_covered": value}}
                with self.assertRaises(assurance.AssuranceEvidenceError):
                    assurance.evaluate_coverage(report, minimum_percent=85.0)

    def test_mutation_requires_measured_mutants_floor_and_dispositions(self) -> None:
        passing = {
            "counts": {
                "killed": 12,
                "survived": 0,
                "suspicious": 0,
                "timeout": 0,
                "untested": 0,
                "skipped": 1,
            },
            "survivor_dispositions": [],
        }
        result = assurance.evaluate_mutation(passing, minimum_percent=100.0)
        self.assertEqual(
            result,
            {
                "schema_id": "validation_assurance_evaluation_v1",
                "kind": "mutation",
                "status": "PASS",
                "minimum_percent": 100.0,
                "observed_percent": 100.0,
                "measured_mutants": 12,
                "unresolved_mutants": 0,
                "disposition_count": 0,
                "counts": {
                    "killed": 12,
                    "survived": 0,
                    "suspicious": 0,
                    "timeout": 0,
                    "untested": 0,
                    "skipped": 1,
                },
                "authority": {
                    "operational_evidence_only": True,
                    "proof_authority": False,
                    "scientific_claim_authority": False,
                },
            },
        )

        survivor = {
            "counts": {"killed": 9, "survived": 1},
            "survivor_dispositions": [],
        }
        self.assertEqual(
            assurance.evaluate_mutation(survivor, minimum_percent=90.0)["status"],
            "FAIL",
        )
        survivor["survivor_dispositions"] = [{"mutant_id": "m1", "reason": "equivalent"}]
        self.assertEqual(
            assurance.evaluate_mutation(survivor, minimum_percent=90.0)["status"],
            "PASS",
        )

        no_mutants = {"counts": {}, "survivor_dispositions": []}
        self.assertEqual(
            assurance.evaluate_mutation(no_mutants, minimum_percent=0.0),
            {
                "schema_id": "validation_assurance_evaluation_v1",
                "kind": "mutation",
                "status": "FAIL",
                "minimum_percent": 0.0,
                "observed_percent": 0.0,
                "measured_mutants": 0,
                "unresolved_mutants": 0,
                "disposition_count": 0,
                "counts": {
                    "killed": 0,
                    "survived": 0,
                    "suspicious": 0,
                    "timeout": 0,
                    "untested": 0,
                    "skipped": 0,
                },
                "authority": {
                    "operational_evidence_only": True,
                    "proof_authority": False,
                    "scientific_claim_authority": False,
                },
            },
        )

        single = {"counts": {"killed": 1}}
        self.assertEqual(
            assurance.evaluate_mutation(single, minimum_percent=100.0)["status"],
            "PASS",
        )

        all_unresolved_states = {
            "counts": {
                "killed": 1,
                "survived": 1,
                "suspicious": 1,
                "timeout": 1,
                "untested": 1,
            },
            "survivor_dispositions": [
                {"mutant_id": "survived"},
                {"mutant_id": "suspicious"},
                {"mutant_id": "timeout"},
                {"mutant_id": "untested"},
            ],
        }
        unresolved_result = assurance.evaluate_mutation(
            all_unresolved_states,
            minimum_percent=20.0,
        )
        self.assertEqual(unresolved_result["status"], "PASS")
        self.assertEqual(unresolved_result["observed_percent"], 20.0)
        self.assertEqual(unresolved_result["unresolved_mutants"], 4)
        self.assertEqual(unresolved_result["disposition_count"], 4)

    def test_mutation_rejects_negative_or_boolean_counts(self) -> None:
        for value in (-1, True, 1.5):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    assurance.AssuranceEvidenceError,
                    r"counts\.killed must be a nonnegative integer",
                ):
                    assurance.evaluate_mutation(
                        {
                            "counts": {"killed": value},
                            "survivor_dispositions": [],
                        },
                        minimum_percent=0.0,
                    )

        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "minimum_percent must be between 0 and 100",
        ):
            assurance.evaluate_mutation({"counts": {}}, minimum_percent=-1.0)
        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "counts must be an object",
        ):
            assurance.evaluate_mutation({}, minimum_percent=0.0)
        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "survivor_dispositions must be an array",
        ):
            assurance.evaluate_mutation(
                {"counts": {"killed": 1}, "survivor_dispositions": None},
                minimum_percent=0.0,
            )

    def test_mutmut_normalization_is_bounded_to_exact_prefix(self) -> None:
        text = """
    scripts.validation.assurance.x_evaluate_mutation__mutmut_1: killed
    scripts.validation.assurance.x_evaluate_mutation__mutmut_2: killed
    scripts.validation.assurance.x_evaluate_mutation__mutmut_3: survived
    scripts.validation.assurance.x_evaluate_bandit__mutmut_1: not checked
"""
        report = assurance.normalize_mutmut_results(
            text,
            target_prefix="scripts.validation.assurance.x_evaluate_mutation__",
        )
        self.assertEqual(
            report,
            {
                "schema_id": "normalized_mutmut_result_v1",
                "target_prefix": (
                    "scripts.validation.assurance.x_evaluate_mutation__"
                ),
                "mutant_count": 3,
                "counts": {
                    "killed": 2,
                    "survived": 1,
                    "suspicious": 0,
                    "timeout": 0,
                    "untested": 0,
                    "skipped": 0,
                },
                "survivor_dispositions": [],
            },
        )
        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "no mutmut results matched target_prefix",
        ):
            assurance.normalize_mutmut_results(text, target_prefix="missing.")
        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "target_prefix must be nonempty",
        ):
            assurance.normalize_mutmut_results(text, target_prefix="")
        with self.assertRaisesRegex(
            assurance.AssuranceEvidenceError,
            "unknown mutmut state: unknown",
        ):
            assurance.normalize_mutmut_results(
                "    target.mutmut_1: unknown\n",
                target_prefix="target.",
            )

    def test_bandit_blocks_only_undispositioned_high_findings(self) -> None:
        report = {
            "results": [
                {
                    "test_id": "B101",
                    "filename": "tests/example.py",
                    "line_number": 7,
                    "issue_severity": "LOW",
                },
                {
                    "test_id": "B602",
                    "filename": "scripts/example.py",
                    "line_number": 11,
                    "issue_severity": "HIGH",
                },
            ]
        }
        failed = assurance.evaluate_bandit(report)
        self.assertEqual(failed["status"], "FAIL")
        self.assertEqual(failed["finding_counts"], {"LOW": 1, "MEDIUM": 0, "HIGH": 1})
        key = "B602:scripts/example.py:11"
        passed = assurance.evaluate_bandit(report, dispositions={key: {"status": "accepted"}})
        self.assertEqual(passed["status"], "PASS")
        self.assertEqual(passed["disposition_count"], 1)

    def test_bandit_rejects_malformed_identity_or_severity(self) -> None:
        malformed = {
            "results": [
                {
                    "test_id": "B101",
                    "filename": "x.py",
                    "line_number": 0,
                    "issue_severity": "CRITICAL",
                }
            ]
        }
        with self.assertRaises(assurance.AssuranceEvidenceError):
            assurance.evaluate_bandit(malformed)

    def test_pip_audit_requires_disposition_for_every_vulnerability(self) -> None:
        report = {
            "dependencies": [
                {
                    "name": "example",
                    "version": "1.0",
                    "vulns": [{"id": "PYSEC-1"}],
                },
                {"name": "clean", "version": "2.0", "vulns": []},
            ]
        }
        failed = assurance.evaluate_pip_audit(report)
        self.assertEqual(failed["status"], "FAIL")
        self.assertEqual(failed["unresolved_vulnerabilities"], ["example:PYSEC-1"])
        passed = assurance.evaluate_pip_audit(
            report,
            dispositions={"example:PYSEC-1": {"status": "mitigated"}},
        )
        self.assertEqual(passed["status"], "PASS")
        self.assertEqual(passed["dependency_count"], 2)

    def test_cli_is_deterministic_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "coverage.json"
            report_path.write_text(
                json.dumps(
                    {
                        "totals": {
                            "num_statements": 10,
                            "num_branches": 2,
                            "percent_covered": 90.0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            command = [
                sys.executable,
                "-m",
                "scripts.validation.assurance",
                "coverage",
                "--input",
                str(report_path),
                "--minimum-percent",
                "85",
            ]
            first = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            second = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(json.loads(first.stdout)["status"], "PASS")

            report_path.write_text("{not-json", encoding="utf-8")
            malformed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(malformed.returncode, 2)
            self.assertEqual(json.loads(malformed.stdout)["status"], "ERROR")

    def test_main_dispatches_every_evidence_kind(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reports = {
                "coverage": {
                    "totals": {
                        "num_statements": 10,
                        "num_branches": 2,
                        "percent_covered": 90.0,
                    }
                },
                "mutation": {
                    "counts": {"killed": 2},
                    "survivor_dispositions": [],
                },
                "bandit": {"results": []},
                "pip-audit": {"dependencies": []},
            }
            for kind, report in reports.items():
                with self.subTest(kind=kind):
                    report_path = root / f"{kind}.json"
                    report_path.write_text(json.dumps(report), encoding="utf-8")
                    arguments = [kind, "--input", str(report_path)]
                    if kind in {"coverage", "mutation"}:
                        arguments.extend(["--minimum-percent", "85"])
                    output = StringIO()
                    with redirect_stdout(output):
                        return_code = assurance.main(arguments)
                    self.assertEqual(return_code, 0)
                    self.assertEqual(json.loads(output.getvalue())["status"], "PASS")

            malformed_path = root / "malformed.json"
            malformed_path.write_text("{", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                return_code = assurance.main(
                    ["coverage", "--input", str(malformed_path)]
                )
            self.assertEqual(return_code, 2)
            self.assertEqual(json.loads(output.getvalue())["status"], "ERROR")

            mutmut_path = root / "mutmut-results.txt"
            mutmut_path.write_text(
                "    target.mutmut_1: killed\n",
                encoding="utf-8",
            )
            output = StringIO()
            with redirect_stdout(output):
                return_code = assurance.main(
                    [
                        "mutmut",
                        "--input",
                        str(mutmut_path),
                        "--target-prefix",
                        "target.",
                        "--minimum-percent",
                        "100",
                    ]
                )
            self.assertEqual(return_code, 0)
            self.assertEqual(json.loads(output.getvalue())["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
