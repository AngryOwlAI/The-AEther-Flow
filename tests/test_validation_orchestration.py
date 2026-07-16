from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


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

    def test_checkpoint_uses_write_only_sync_and_one_final_memory_core_gate(self) -> None:
        final_command = self.checkpoint.final_memory_validation_command()
        self.assertNotIn(final_command, self.checkpoint.post_sync_validation_commands())

        sync_result = self.checkpoint.CommandResult(
            ["memory_sync()"],
            0,
            json.dumps({"gate_id": "memory_sync", "mutated": True}),
            "",
            0.25,
        )
        core_result = self.checkpoint.CommandResult(
            final_command,
            0,
            "Memory system validation passed.",
            "",
            0.5,
        )
        results = [sync_result, core_result]

        counts = self.checkpoint.checkpoint_command_counts(results)
        self.assertEqual(counts["memory_sync"], 1)
        self.assertEqual(counts["memory_core"], 1)
        self.assertEqual(counts["compatibility_bootstrap"], 0)
        receipt = self.checkpoint.checkpoint_receipt(
            results,
            final_index_tree="final-tree-hash",
        )
        self.assertEqual(receipt["generator_passes"], 1)
        self.assertEqual(
            receipt["final_validator"]["gate_id"],
            "memory_legacy_composite",
        )
        self.assertEqual(
            receipt["final_validator"]["satisfies_obligation"],
            "memory_core",
        )
        self.assertEqual(
            receipt["final_validator"]["git_index_tree"],
            "final-tree-hash",
        )
        performance = self.checkpoint.checkpoint_performance(results)
        self.assertEqual(performance["subprocess_count"], 1)
        self.assertIn("duration_seconds", performance)
        self.assertIn("output_bytes", performance)
        self.assertEqual(performance["cache_hits"], 0)
        self.assertEqual(performance["cache_misses"], 0)

    def test_memory_sync_wrapper_is_tracked_only_and_fail_closed(self) -> None:
        calls: list[dict[str, object]] = []

        class Receipt:
            def to_dict(self) -> dict[str, object]:
                return {
                    "mutated": False,
                    "counts": {
                        "changed": 0,
                        "unchanged": 1,
                        "created": 0,
                        "pruned": 0,
                    },
                    "changed": [],
                    "created": [],
                    "pruned": [],
                    "local_retrieval_enabled": False,
                }

        def fake_sync(**kwargs):
            calls.append(kwargs)
            return Receipt()

        with mock.patch.object(self.checkpoint, "_load_memory_sync", return_value=fake_sync):
            result = self.checkpoint.memory_sync(rebuilt_pdf_paths=["pdf/example.pdf"])

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            calls,
            [
                {
                    "rebuilt_pdf_paths": ["pdf/example.pdf"],
                    "include_local_retrieval": False,
                }
            ],
        )
        self.assertEqual(json.loads(result.stdout)["gate_id"], "memory_sync")

        def failing_sync(**_kwargs):
            raise RuntimeError("sync fixture failure")

        with mock.patch.object(
            self.checkpoint,
            "_load_memory_sync",
            return_value=failing_sync,
        ):
            failed = self.checkpoint.memory_sync()
        self.assertEqual(failed.returncode, 1)
        self.assertIn("sync fixture failure", failed.stderr)

    def test_checkpoint_retains_second_sync_after_targeted_pdf_build(self) -> None:
        commands: list[list[str]] = []
        snapshots = iter(["entry-tree\n", "original-tree\n", "final-tree\n"])
        tex_path = "tex/example.tex"
        pdf_path = "pdf/example.pdf"

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, next(snapshots), "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(
                    command,
                    0,
                    f"{tex_path}\0{pdf_path}\0",
                    "",
                )
            return self.checkpoint.CommandResult(command, 0, "", "")

        sync_calls: list[dict[str, object]] = []

        def fake_sync(**kwargs):
            sync_calls.append(kwargs)
            return self.checkpoint.CommandResult(
                ["memory_sync()"],
                0,
                json.dumps({"gate_id": "memory_sync", "mutated": True}),
                "",
            )

        preflight = {tex_path: " M"}
        after_sync = {tex_path: "M "}
        after_pdf = {tex_path: "M ", pdf_path: "M "}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="memory-system-maintainer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[
                    preflight,
                    after_sync,
                    after_pdf,
                    after_pdf,
                    after_pdf,
                ],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=[tex_path, pdf_path],
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[tex_path],
            ),
            mock.patch.object(
                self.checkpoint,
                "post_sync_validation_commands",
                return_value=[],
            ),
            mock.patch.object(self.checkpoint, "memory_sync", side_effect=fake_sync),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertEqual(result["status"], "ready_to_commit")
        self.assertEqual(result["sync_passes"], 1)
        self.assertEqual(sync_calls, [{}, {"rebuilt_pdf_paths": [tex_path]}])
        self.assertEqual(result["checkpoint_receipt"]["generator_passes"], 2)
        self.assertEqual(
            result["checkpoint_receipt"]["final_validator"]["git_index_tree"],
            "final-tree",
        )
        self.assertIn(
            [
                ".venv/bin/python",
                ".codex/skills/project-memory-system/scripts/build_pdf_derivatives.py",
                tex_path,
            ],
            commands,
        )


if __name__ == "__main__":
    unittest.main()
