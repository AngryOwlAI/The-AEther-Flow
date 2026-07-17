from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/research_control/checkpoint_research_transaction.py"


def load_checkpoint_module():
    name = "checkpoint_research_transaction_planner_test"
    spec = importlib.util.spec_from_file_location(name, SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def classification(paths, **_kwargs) -> dict[str, object]:
    values = tuple(sorted(str(path) for path in paths))
    return {
        "changed_paths": list(values),
        "blocked_paths": [],
        "ignored_paths": [],
        "path_family_tags": ["validator_code"],
        "path_family_details": [
            {
                "path": path,
                "tags": ["validator_code"],
                "reasons": [],
                "canonical_paths": [],
                "generated_derivatives": [],
                "affected_source_object_ids": [],
            }
            for path in values
        ],
        "recommended_validation_profile": "affected",
    }


class TemporaryGitRepository:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "checkpoint-tests@example.invalid")
        self.git("config", "user.name", "Checkpoint Tests")

    def cleanup(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ("git", *arguments),
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise AssertionError(completed.stderr)
        return completed.stdout.strip()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit_files(self, files: dict[str, str]) -> None:
        self.write(".gitignore", ".local/\n")
        for path, text in files.items():
            self.write(path, text)
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "baseline")


class CheckpointPlannerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checkpoint = load_checkpoint_module()

    def test_cli_defaults_to_compare_and_retains_explicit_legacy_fallback(self) -> None:
        self.assertEqual(self.checkpoint.parse_args([]).validation_mode, "compare")
        self.assertEqual(
            self.checkpoint.parse_args(["--legacy-validation"]).validation_mode,
            "legacy",
        )
        self.assertEqual(
            self.checkpoint.parse_args(["--compare-validation"]).validation_mode,
            "compare",
        )

    def test_planner_selects_tracked_generators_and_excludes_local_or_self_mutators(self) -> None:
        plan = self.checkpoint.plan_checkpoint_validation(
            ["research_control/tasks/RT-TEST/00_TASK.yaml"]
        )

        self.assertIn("memory_sync", plan.generator_gate_ids)
        self.assertNotIn("continue_memory_preflight", plan.generator_gate_ids)
        self.assertIn("continue_memory_preflight", plan.local_only_gate_ids)
        self.assertIn("checkpoint_transaction", plan.orchestrator_gate_ids)

        pdf_plan = self.checkpoint.plan_checkpoint_validation(
            ["legacy_ontology/tex/aether_flow_consistency.tex"]
        )
        self.assertIn("targeted_pdf_build", pdf_plan.generator_gate_ids)

    def test_validation_manifest_schema_transaction_has_safe_shadow_plan(self) -> None:
        manifest_path = "research_control/design/validation_gate_manifest_v1.yaml"
        plan = self.checkpoint.plan_checkpoint_validation(
            [
                manifest_path,
                "research_control/design/route_diagnostic_cache_schema_v1.md",
            ]
        )
        details = {
            item["path"]: item for item in plan.classification["path_family_details"]
        }

        self.assertEqual(
            details[manifest_path]["tags"],
            ["role_or_schema_contract"],
        )
        self.assertNotIn(
            "unknown_governed_path",
            plan.classification["path_family_tags"],
        )
        self.assertIn("route_signature_diagnostic", plan.selected_gate_ids)

    def test_planning_expands_git_collapsed_untracked_directory(self) -> None:
        command = [
            "git",
            "ls-files",
            "--others",
            "--exclude-standard",
            "--",
            "research_control/tasks/RT-TEST/",
        ]
        with mock.patch.object(
            self.checkpoint,
            "run_command",
            return_value=self.checkpoint.CommandResult(
                command,
                0,
                "research_control/tasks/RT-TEST/00_TASK.yaml\n"
                "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml\n",
                "",
            ),
        ):
            paths = self.checkpoint.checkpoint_planning_paths(
                {
                    "research_control/tasks/RT-TEST/": "??",
                    "registries/AGENT_JOB_REGISTRY.csv": " M",
                }
            )

        self.assertEqual(
            paths,
            (
                "registries/AGENT_JOB_REGISTRY.csv",
                "research_control/tasks/RT-TEST/00_TASK.yaml",
                "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            ),
        )

    def repo(self) -> TemporaryGitRepository:
        repo = TemporaryGitRepository()
        self.addCleanup(repo.cleanup)
        return repo

    def planner_plan(self, *generators: str):
        return self.checkpoint.CheckpointValidationPlan(
            manifest={},
            classification={},
            selected_gate_ids=tuple(generators) + ("checkpoint_transaction",),
            generator_gate_ids=tuple(generators),
            local_only_gate_ids=("continue_memory_preflight",),
            orchestrator_gate_ids=("checkpoint_transaction",),
        )

    def run_shadow(
        self, repo: TemporaryGitRepository, paths: list[str]
    ) -> tuple[dict[str, object], dict[str, object], list[object]]:
        commands: list[object] = []

        def passing_command(command: list[str]):
            return self.checkpoint.CommandResult(command, 0, "", "")

        manifest = self.checkpoint.load_manifest(
            self.checkpoint.VALIDATION_MANIFEST_PATH
        )
        with mock.patch.object(
            self.checkpoint, "run_command", side_effect=passing_command
        ):
            receipt, integration = self.checkpoint.run_checkpoint_staged_acceptance(
                repo.root,
                transaction_paths=paths,
                allowed_path_globs=paths,
                manifest=manifest,
                agent_job_id="AJ-TEST",
                command_results=commands,
                classifier=classification,
            )
        return receipt, integration, commands

    def test_three_representative_transactions_match_legacy_on_exact_index(self) -> None:
        for scenario in ("add", "modify", "delete"):
            with self.subTest(scenario=scenario):
                repo = self.repo()
                baseline = {"sample.py": "before\n"}
                repo.commit_files(baseline)
                entry_tree = repo.git("write-tree")
                path = "added.py" if scenario == "add" else "sample.py"
                if scenario == "add":
                    repo.write(path, "new\n")
                elif scenario == "modify":
                    repo.write(path, "after\n")
                else:
                    (repo.root / path).unlink()

                receipt, integration, commands = self.run_shadow(repo, [path])

                self.assertEqual(receipt["status"], "PASS")
                self.assertEqual(receipt["shadow_comparison"]["status"], "PASS")
                self.assertEqual(receipt["index"]["restored_tree"], entry_tree)
                self.assertTrue(receipt["index"]["restored"])
                self.assertEqual(integration["status"], "PASS")
                self.assertEqual(len(integration["child_receipts"]), 1)
                self.assertEqual(
                    len(commands), len(integration["required_gate_ids"])
                )

    def test_shadow_status_mismatch_fails_closed_and_restores_index(self) -> None:
        repo = self.repo()
        repo.commit_files({"sample.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("sample.py", "after\n")

        def divergent_adapter(adapter, _context):
            adapter.legacy_statuses[adapter.gate_id] = "FAIL"
            return self.checkpoint.AdapterResult(exit_code=0)

        with mock.patch.object(
            self.checkpoint.CheckpointCommandAdapter,
            "run",
            divergent_adapter,
        ):
            receipt, _integration, _commands = self.run_shadow(repo, ["sample.py"])

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "legacy_shadow_mismatch")
        self.assertEqual(receipt["index"]["restored_tree"], entry_tree)
        self.assertTrue(receipt["index"]["restored"])

    def test_compare_mode_preserves_no_action_without_staged_acceptance(self) -> None:
        def fake_run(command: list[str]):
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "entry-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, "tracked.txt\0", "")
            return self.checkpoint.CommandResult(command, 0, "", "")

        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint, "execution_role_ref_for_job", return_value="role-ref"
            ),
            mock.patch.object(
                self.checkpoint, "git_status_paths", side_effect=[{}, {}, {}]
            ),
            mock.patch.object(
                self.checkpoint, "allowed_patterns_for_changed_paths", return_value=[]
            ),
            mock.patch.object(
                self.checkpoint,
                "plan_checkpoint_validation",
                return_value=self.planner_plan("memory_sync"),
            ),
            mock.patch.object(
                self.checkpoint,
                "run_precheck",
                return_value={
                    "status": "PASS",
                    "tree_hash": "working-sha256:" + "a" * 64,
                    "requested_gate": "path_policy_sanity",
                    "counts": {},
                },
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                return_value=self.checkpoint.CommandResult(
                    ["memory_sync()"], 0, "{}", ""
                ),
            ),
            mock.patch.object(
                self.checkpoint, "changed_registered_tex_requiring_pdf", return_value=[]
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
            mock.patch.object(
                self.checkpoint, "run_checkpoint_staged_acceptance"
            ) as staged,
        ):
            result = self.checkpoint.checkpoint(
                "AJ-TEST", no_commit=True, validation_mode="compare"
            )

        self.assertEqual(result["status"], "no_action")
        self.assertEqual(
            result["checkpoint_receipt"]["planner_integration"]["staged_acceptance"]["status"],
            "NOT_RUN",
        )
        staged.assert_not_called()

    def test_compare_mode_pdf_failure_restores_original_index(self) -> None:
        commands: list[list[str]] = []
        tex_path = "legacy_ontology/tex/aether_flow_consistency.tex"

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "original-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, f"{tex_path}\0", "")
            if any(value.endswith("build_pdf_derivatives.py") for value in command):
                return self.checkpoint.CommandResult(command, 1, "", "pdf failed")
            return self.checkpoint.CommandResult(command, 0, "", "")

        working = {tex_path: " M"}
        staged = {tex_path: "M "}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint, "execution_role_ref_for_job", return_value="role-ref"
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[working, staged, staged],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=[tex_path, "pdf/**"],
            ),
            mock.patch.object(
                self.checkpoint,
                "plan_checkpoint_validation",
                return_value=self.planner_plan("memory_sync", "targeted_pdf_build"),
            ),
            mock.patch.object(
                self.checkpoint, "run_precheck", return_value={"status": "PASS"}
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                return_value=self.checkpoint.CommandResult(
                    ["memory_sync()"], 0, "{}", ""
                ),
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[tex_path],
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint._checkpoint_impl(
                "AJ-TEST", no_commit=True, validation_mode="compare"
            )

        self.assertEqual(result["reason"], "targeted PDF build failed")
        self.assertIn(["git", "read-tree", "original-tree"], commands)

    def test_disallowed_preexisting_path_blocks_before_planning(self) -> None:
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint, "execution_role_ref_for_job", return_value="role-ref"
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                return_value={"outside.txt": " M"},
            ),
            mock.patch.object(
                self.checkpoint, "allowed_patterns_for_changed_paths", return_value=[]
            ),
            mock.patch.object(
                self.checkpoint, "plan_checkpoint_validation"
            ) as planner,
        ):
            result = self.checkpoint._checkpoint_impl(
                "AJ-TEST", no_commit=True, validation_mode="compare"
            )

        self.assertEqual(
            result["reason"],
            "preexisting changes outside the AgentJob or sync allowlist",
        )
        planner.assert_not_called()

    def test_commit_failure_restores_original_index(self) -> None:
        commands: list[list[str]] = []
        path = "changed.txt"

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                tree = "final-tree" if commands.count(command) > 1 else "original-tree"
                return self.checkpoint.CommandResult(command, 0, tree + "\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, f"{path}\0", "")
            if command[:2] == ["git", "commit"]:
                return self.checkpoint.CommandResult(command, 1, "", "commit failed")
            return self.checkpoint.CommandResult(command, 0, "", "")

        working = {path: " M"}
        staged = {path: "M "}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={
                    "job_id": "AJ-TEST",
                    "task_id": "RT-TEST",
                    "decision_id": "DDR-TEST",
                    "notes": "test",
                },
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint, "execution_role_ref_for_job", return_value="role-ref"
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[working, staged, staged, staged],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=[path],
            ),
            mock.patch.object(
                self.checkpoint, "changed_registered_tex_requiring_pdf", return_value=[]
            ),
            mock.patch.object(
                self.checkpoint, "post_sync_validation_commands", return_value=[]
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                return_value=self.checkpoint.CommandResult(
                    ["memory_sync()"], 0, "{}", ""
                ),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint._checkpoint_impl("AJ-TEST")

        self.assertEqual(result["reason"], "git commit failed")
        self.assertIn(["git", "read-tree", "original-tree"], commands)


if __name__ == "__main__":
    unittest.main()
