from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts/research_control/run_full_research_control_validation.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("validation_wrapper_test_runner", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def shared_full_plan() -> dict:
    return {
        "schema_id": "validation_plan_v1",
        "status": "READY",
        "requested_profile": "full",
        "effective_profile": "full",
        "manifest_hash": "manifest-hash",
        "execution_authority": "legacy",
        "planner_executes_commands": False,
        "selected_gate_ids": [
            "research_control_core",
            "research_control_diff",
            "compact_frontier_freshness",
            "profile_full_research_control",
        ],
    }


def completed(command: list[str], returncode: int, stdout: str = "", stderr: str = ""):
    return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr=stderr)


class MakeValidationProfileWrapperTests(unittest.TestCase):
    def make_plan(self, target: str, *variables: str) -> str:
        result = subprocess.run(
            ["make", "-n", "PYTHON=.venv/bin/python", *variables, target],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def test_five_public_targets_delegate_to_shared_cli_profiles(self) -> None:
        expectations = {
            "validate-fast": "plan --profile fast --paths Makefile --explain",
            "validate-affected": "plan --profile affected --paths Makefile --explain",
            "validate-checkpoint-plan": "plan --profile checkpoint --staged --explain",
            "validate-full": "plan --profile full --paths --explain",
            "validate-doctor": "plan --profile doctor --scope local_retrieval --explain",
        }
        for target, expected in expectations.items():
            with self.subTest(target=target):
                plan = self.make_plan(target, "VALIDATION_PATHS=Makefile")
                self.assertIn("-m scripts.validation.cli", plan)
                self.assertIn(expected, plan)

    def test_compatibility_target_plans_once_then_runs_legacy_chain_once(self) -> None:
        plan = self.make_plan("validate-project-control")

        self.assertEqual(plan.count("plan --profile full --paths --explain"), 1)
        self.assertEqual(
            plan.count("scripts/research_control/validate_research_control.py --check-diff"),
            1,
        )
        self.assertEqual(plan.count("unittest discover -s tests"), 1)
        self.assertIn('"compatibility_wrapper":true', plan)
        self.assertIn('"execution_authority":"legacy"', plan)


class LocalFullRunnerWrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = load_runner()

    def run_main(self, argv: list[str], side_effect: list[subprocess.CompletedProcess]):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(self.runner.subprocess, "run", side_effect=side_effect) as run:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = self.runner.main(argv)
        report = json.loads(stdout.getvalue()) if stdout.getvalue() else None
        return exit_code, report, stderr.getvalue(), run

    def test_runner_delegates_selection_then_execution_and_reports_deprecation(self) -> None:
        planner = completed(self.runner.planner_command(), 0, json.dumps(shared_full_plan()))
        legacy = completed(self.runner.legacy_command(), 0, "Research-control validation PASS")

        exit_code, report, stderr, run = self.run_main(["--json"], [planner, legacy])

        self.assertEqual(exit_code, 0)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[0].args[0], self.runner.planner_command())
        self.assertEqual(run.call_args_list[1].args[0], self.runner.legacy_command())
        self.assertEqual(report["schema_id"], self.runner.REPORT_SCHEMA_ID)
        self.assertEqual(report["legacy_execution_status"], "PASS")
        self.assertEqual(report["execution_authority"], "legacy")
        self.assertFalse(report["planner_executes_commands"])
        self.assertFalse(report["ci_equivalent"])
        self.assertTrue(report["compatibility_wrapper_deprecated"])
        self.assertIn("DEPRECATED_COMPATIBILITY_WRAPPER", stderr)

    def test_plan_only_preserves_optional_output_and_skips_legacy_execution(self) -> None:
        planner = completed(self.runner.planner_command(), 0, json.dumps(shared_full_plan()))
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "plan.json"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(self.runner.subprocess, "run", return_value=planner) as run:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    exit_code = self.runner.main(
                        ["--plan-only", "--include-smoke-tests", "--output", str(output)]
                    )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(report["schema_id"], self.runner.PLAN_SCHEMA_ID)
        self.assertEqual(report["legacy_execution_status"], "NOT_RUN")
        self.assertEqual(
            report["include_smoke_tests_compatibility"],
            "accepted_no_op_full_profile_already_selects_repository_tests",
        )

    def test_planner_and_legacy_exit_codes_propagate(self) -> None:
        planner_failure = completed(self.runner.planner_command(), 2, stderr="blocked")
        exit_code, report, _, run = self.run_main(["--json"], [planner_failure])
        self.assertEqual(exit_code, 2)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(report["required_failure_labels"], ["validation_plan_full"])

        planner = completed(self.runner.planner_command(), 0, json.dumps(shared_full_plan()))
        legacy_failure = completed(self.runner.legacy_command(), 7, stderr="legacy failed")
        exit_code, report, _, run = self.run_main(["--json"], [planner, legacy_failure])
        self.assertEqual(exit_code, 7)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(report["required_failure_labels"], ["legacy_validate_project_control"])

    def test_runner_full_selection_matches_direct_shared_cli(self) -> None:
        direct = subprocess.run(
            [
                ".venv/bin/python",
                "-m",
                "scripts.validation.cli",
                "plan",
                "--profile",
                "full",
                "--paths",
                "--json",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        wrapped = subprocess.run(
            [
                ".venv/bin/python",
                "scripts/research_control/run_full_research_control_validation.py",
                "--plan-only",
                "--json",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        direct_plan = json.loads(direct.stdout)
        wrapper_report = json.loads(wrapped.stdout)

        self.assertEqual(wrapper_report["manifest_hash"], direct_plan["manifest_hash"])
        self.assertEqual(wrapper_report["selected_gate_ids"], direct_plan["selected_gate_ids"])
        self.assertEqual(wrapper_report["shared_plan"], direct_plan)


if __name__ == "__main__":
    unittest.main()
