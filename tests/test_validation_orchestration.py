from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MakeValidationOrchestrationTests(unittest.TestCase):
    def test_validate_project_control_runs_one_research_control_spine(self) -> None:
        completed = subprocess.run(
            ["make", "-n", "PYTHON=.venv/bin/python", "validate-project-control"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        research_control_commands = [
            line.strip()
            for line in completed.stdout.splitlines()
            if "scripts/research_control/validate_research_control.py" in line
        ]

        self.assertEqual(
            research_control_commands,
            [
                ".venv/bin/python scripts/research_control/validate_research_control.py "
                "--check-diff"
            ],
        )


class RunnerCheckpointValidationOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_script(
            "run_full_research_control_validation_orchestration_test",
            "scripts/research_control/run_full_research_control_validation.py",
        )
        cls.checkpoint = load_script(
            "checkpoint_research_transaction_orchestration_test",
            "scripts/research_control/checkpoint_research_transaction.py",
        )

    def test_local_runner_uses_one_diff_superset_and_disclaims_ci_equivalence(self) -> None:
        plan = self.runner.command_plan()
        research_control_commands = [
            entry for entry in plan
            if "scripts/research_control/validate_research_control.py" in entry["command"]
        ]

        self.assertEqual(
            [entry["label"] for entry in research_control_commands],
            ["research_control_diff_validation"],
        )
        coverage = self.runner.coverage_map(plan)
        self.assertTrue(coverage["research_control_core_obligation"])
        self.assertTrue(coverage["research_control_diff_obligation"])

        completed = subprocess.run(
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
        report = json.loads(completed.stdout)
        self.assertFalse(report["ci_equivalent"])
        self.assertEqual(
            report["ci_equivalence_status"],
            "not_equivalent_until_v19_p11_centralization",
        )

    def test_checkpoint_keeps_one_working_diff_gate_and_a_distinct_staged_gate(self) -> None:
        working_commands = [
            command
            for command in self.checkpoint.post_sync_validation_commands()
            if "scripts/research_control/validate_research_control.py" in command
        ]
        staged_command = [
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
            "--staged-only",
        ]

        self.assertEqual(
            working_commands,
            [[
                ".venv/bin/python",
                "scripts/research_control/validate_research_control.py",
                "--check-diff",
            ]],
        )
        counts = self.checkpoint.checkpoint_command_counts([
            self.checkpoint.CommandResult(working_commands[0], 0, "", ""),
            self.checkpoint.CommandResult(staged_command, 0, "", ""),
        ])
        self.assertEqual(counts["research_control_plain_working"], 0)
        self.assertEqual(counts["research_control_diff_working"], 1)
        self.assertEqual(counts["research_control_diff_staged"], 1)
        self.assertTrue(counts["working_and_staged_scopes_distinct"])


if __name__ == "__main__":
    unittest.main()
