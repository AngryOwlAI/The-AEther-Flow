from __future__ import annotations

from copy import deepcopy
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/research_control/checkpoint_research_transaction.py"
VALIDATOR_PATH = REPO_ROOT / "scripts/research_control/validate_research_control.py"
P12_T05_DIRTY_MANIFEST_PATHS = (
    "FOLDER_MAP.md",
    "output/ai_methodology_metrics_dashboard.json",
    "output/ai_methodology_metrics_dashboard.md",
    "output/compact_current_frontier_v16.json",
    "output/compact_current_frontier_v16.yaml",
    "output/physics_progress_metrics.json",
    "output/physics_progress_metrics.md",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/CONTENT_SEMANTIC_REGISTRY.csv",
    "registries/CONTENT_SEMANTIC_REGISTRY.meta.json",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/FILE_OBJECT_REGISTRY.csv",
    "registries/FILE_OBJECT_REGISTRY.meta.json",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
    "registries/OBJECT_RELATIONSHIP_REGISTRY.csv",
    "registries/OBJECT_RELATIONSHIP_REGISTRY.meta.json",
    "registries/OBSIDIAN_VAULT_REGISTRY.csv",
    "registries/OBSIDIAN_VAULT_REGISTRY.meta.json",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
    "registries/WIKI_ARTIFACT_REGISTRY.csv",
    "registries/WIKI_ARTIFACT_REGISTRY.meta.json",
    "research_control/current_frontier.md",
    "research_control/handoffs/handoff-0837.md",
    "research_control/handoffs/handoff-0837.yaml",
    "research_control/program_state.yaml",
    "research_control/tasks/RT-20260723-004/00_TASK.yaml",
    "research_control/tasks/RT-20260723-004/DDR-20260723-004.md",
    "research_control/tasks/RT-20260723-004/artifacts/fixtures/scientific_quality_metric_cases.json",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_calibration_warning_policy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_compact_receipt.json",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_metric_taxonomy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_validation_report.json",
    "research_control/tasks/RT-20260723-004/artifacts/validate_scientific_quality_metrics.py",
    "research_control/tasks/RT-20260723-004/artifacts/validation_blocker_checkpoint_planner_unknown_scientific_quality_paths_v1.yaml",
    "research_control/tasks/RT-20260723-004/documentation_impact.yaml",
    "research_control/tasks/RT-20260723-004/jobs/AJ-RT-20260723-004-001.yaml",
    "research_control/tasks/RT-20260723-004/jobs/completions/AJC-AJ-RT-20260723-004-001.yaml",
    "research_control/tasks/RT-20260723-004/roles/project-control-maintainer@0.2.0--RT-20260723-004.yaml",
    "research_control/tasks/TASK_INDEX.csv",
    "research_control/tasks/TASK_INDEX.md",
    "scripts/research_control/render_ai_methodology_metrics_dashboard.py",
    "scripts/research_control/report_physics_progress_metrics.py",
    "scripts/research_control/scientific_quality_metrics.py",
    "tests/test_report_physics_progress_metrics.py",
    "tests/test_research_control.py",
    "tests/test_scientific_quality_metrics.py",
    "wiki/indexes/ai_methodology_metrics_dashboard.md",
    "wiki/indexes/by-authority-status.md",
    "wiki/indexes/by-format.md",
    "wiki/indexes/by-owner-skill.md",
    "wiki/indexes/compact_current_frontier_v16.md",
    "wiki/indexes/documentation-by-authority-status.md",
    "wiki/indexes/documentation-by-format.md",
    "wiki/indexes/documentation-by-owner-skill.md",
    "wiki/indexes/research_control_task_index.md",
    "wiki/markdown/md-research-control-current-frontier.md",
    "wiki/markdown/md-research-control-task-index.md",
    "wiki/markdown/md-research-control-tasks-rt-20260723-004-scientific-quality-calibration-warning-policy-v1.md",
    "wiki/markdown/md-research-control-tasks-rt-20260723-004-scientific-quality-metric-taxonomy-v1.md",
)


def load_checkpoint_module():
    name = "checkpoint_research_transaction_planner_test"
    spec = importlib.util.spec_from_file_location(name, SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_validator_module():
    name = "validate_research_control_checkpoint_binding_test"
    script_dir = str(VALIDATOR_PATH.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(name, VALIDATOR_PATH)
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
        cls.validator = load_validator_module()

    def test_staged_diff_command_binds_the_explicit_agent_job(self) -> None:
        command = self.checkpoint.staged_gate_command(
            "research_control_diff",
            agent_job_id="AJ-EXPLICIT",
        )

        self.assertEqual(
            command,
            [
                ".venv/bin/python",
                "scripts/research_control/validate_research_control.py",
                "--check-diff",
                "--staged-only",
                "--json",
                "--job-id",
                "AJ-EXPLICIT",
            ],
        )

    def test_working_diff_command_binds_the_explicit_agent_job(self) -> None:
        commands = self.checkpoint.post_sync_validation_commands("AJ-EXPLICIT")

        self.assertIn(
            [
                ".venv/bin/python",
                "scripts/research_control/validate_research_control.py",
                "--check-diff",
                "--job-id",
                "AJ-EXPLICIT",
            ],
            commands,
        )

    def test_diff_validator_uses_explicit_older_agent_job(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-OLDER": {
                "job_id": "AJ-OLDER",
                "role_id": "validator-engineer",
                "status": "completed",
                "created_at": "2026-07-01T00:00:00Z",
                "allowed_write_paths": "research_control/tasks/RT-OLDER/**",
                "output_paths": "",
            },
            "AJ-LATER": {
                "job_id": "AJ-LATER",
                "role_id": "validator-engineer",
                "status": "completed",
                "created_at": "2026-07-02T00:00:00Z",
                "allowed_write_paths": "research_control/tasks/RT-LATER/**",
                "output_paths": "",
            },
        }
        changed = "research_control/tasks/RT-OLDER/result.yaml"
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=[changed],
        ):
            self.validator.validate_diff(
                report,
                jobs,
                "HEAD",
                False,
                "AJ-OLDER",
            )

        self.assertEqual(report.errors, [])

    def test_diff_validator_rejects_missing_explicit_agent_job(self) -> None:
        report = self.validator.ValidationReport()
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=[],
        ):
            self.validator.validate_diff(
                report,
                {},
                "HEAD",
                False,
                "AJ-MISSING",
            )

        self.assertEqual(
            report.errors,
            ["--job-id AJ-MISSING: AgentJob does not exist"],
        )

    def test_diff_validator_rejects_ineligible_explicit_agent_job(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-PLANNED": {
                "job_id": "AJ-PLANNED",
                "status": "planned",
                "created_at": "2026-07-01T00:00:00Z",
                "allowed_write_paths": "research_control/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=[],
        ):
            self.validator.validate_diff(
                report,
                jobs,
                "HEAD",
                False,
                "AJ-PLANNED",
            )

        self.assertEqual(
            report.errors,
            [
                "--job-id AJ-PLANNED: AgentJob status "
                "'planned' is not active or completed"
            ],
        )

    def test_cli_defaults_to_planner_and_retains_explicit_fallbacks(self) -> None:
        self.assertEqual(self.checkpoint.parse_args([]).validation_mode, "planner")
        self.assertEqual(
            self.checkpoint.parse_args(["--planner-validation"]).validation_mode,
            "planner",
        )
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
        self.assertNotIn("test_shard_repository", plan.selected_gate_ids)

        pdf_plan = self.checkpoint.plan_checkpoint_validation(
            ["legacy_ontology/tex/aether_flow_consistency.tex"]
        )
        self.assertIn("targeted_pdf_build", pdf_plan.generator_gate_ids)

    def test_planner_selects_repository_shard_for_cadence_obligation(self) -> None:
        plan = self.checkpoint.plan_checkpoint_validation(
            ["research_control/tasks/RT-TEST/00_TASK.yaml"],
            role_obligations=("test_shard_repository",),
        )

        self.assertIn("test_shard_repository", plan.selected_gate_ids)

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

    def test_p12_t05_dirty_manifest_has_safe_shadow_plan(self) -> None:
        self.assertEqual(len(P12_T05_DIRTY_MANIFEST_PATHS), 61)
        plan = self.checkpoint.plan_checkpoint_validation(
            P12_T05_DIRTY_MANIFEST_PATHS
        )

        self.assertNotIn(
            "unknown_governed_path",
            plan.classification["path_family_tags"],
        )
        self.assertIn("checkpoint_transaction", plan.selected_gate_ids)
        self.assertTrue(plan.generator_gate_ids)

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
        self,
        repo: TemporaryGitRepository,
        paths: list[str],
        *,
        role_obligations: tuple[str, ...] = (),
    ) -> tuple[dict[str, object], dict[str, object], list[object]]:
        commands: list[object] = []

        def passing_command(command: list[str]):
            return self.checkpoint.CommandResult(command, 0, "", "")

        manifest = self.checkpoint.load_manifest(
            self.checkpoint.VALIDATION_MANIFEST_PATH
        )
        manifest = deepcopy(manifest)
        manifest["migration_epoch"] = "shadow_planner"
        manifest["execution_authority"] = "legacy"
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
                role_obligations=role_obligations,
                compare_legacy=True,
            )
        return receipt, integration, commands

    def test_staged_acceptance_executes_repository_shard_when_cadence_is_due(
        self,
    ) -> None:
        repo = self.repo()
        repo.commit_files({"sample.py": "before\n"})
        repo.write("sample.py", "after\n")

        receipt, integration, commands = self.run_shadow(
            repo,
            ["sample.py"],
            role_obligations=("test_shard_repository",),
        )

        self.assertEqual(receipt["status"], "PASS")
        self.assertIn(
            "test_shard_repository",
            integration["required_gate_ids"],
        )
        self.assertIn(
            [".venv/bin/python", "-m", "unittest", "discover", "-s", "tests"],
            [result.command for result in commands],
        )

    def test_repository_test_cadence_counts_only_new_completed_scientific_jobs(
        self,
    ) -> None:
        roles = [
            {
                "role_id": "scientist",
                "version": "1",
                "role_kind": "scientific_test",
            },
            {
                "role_id": "validator",
                "version": "1",
                "role_kind": "project_system_validation",
            },
        ]

        def scientific(job_id: str, ordinal: int) -> dict[str, str]:
            return {
                "job_id": job_id,
                "role_id": "scientist",
                "role_version": "1",
                "status": "completed",
                "completed_at": f"2026-07-27T05:{ordinal:02d}:00Z",
            }

        anchor = scientific(
            self.checkpoint.REPOSITORY_TEST_CADENCE_ANCHOR_JOB_ID,
            0,
        )
        first_nine = [
            scientific(f"AJ-SCIENCE-{ordinal:02d}", ordinal)
            for ordinal in range(1, 10)
        ]
        tenth = scientific("AJ-SCIENCE-10", 10)

        before_boundary = self.checkpoint.repository_test_cadence_decision(
            first_nine[-1],
            job_rows=[anchor, *first_nine],
            committed_job_rows=[anchor, *first_nine[:-1]],
            role_rows=roles,
        )
        at_boundary = self.checkpoint.repository_test_cadence_decision(
            tenth,
            job_rows=[anchor, *first_nine, tenth],
            committed_job_rows=[anchor, *first_nine],
            role_rows=roles,
        )

        self.assertFalse(before_boundary["required"])
        self.assertEqual(
            before_boundary["working_completed_scientific_jobs_since_anchor"],
            9,
        )
        self.assertTrue(at_boundary["required"])
        self.assertEqual(at_boundary["due_boundary_ordinal"], 10)

        recovery = {
            "job_id": "AJ-RECOVERY",
            "role_id": "validator",
            "role_version": "1",
            "status": "completed",
            "completed_at": "2026-07-27T05:11:00Z",
        }
        recovery_before_commit = self.checkpoint.repository_test_cadence_decision(
            recovery,
            job_rows=[anchor, *first_nine, tenth, recovery],
            committed_job_rows=[anchor, *first_nine],
            role_rows=roles,
        )
        recovery_after_commit = self.checkpoint.repository_test_cadence_decision(
            recovery,
            job_rows=[anchor, *first_nine, tenth, recovery],
            committed_job_rows=[anchor, *first_nine, tenth],
            role_rows=roles,
        )

        self.assertTrue(recovery_before_commit["required"])
        self.assertFalse(recovery_after_commit["required"])
        self.assertEqual(
            recovery_after_commit["reason"],
            "project_system_job_does_not_advance_cadence",
        )

    def test_repository_test_cadence_fails_safe_without_anchor(self) -> None:
        job = {
            "job_id": "AJ-SCIENCE-01",
            "role_id": "scientist",
            "role_version": "1",
            "status": "completed",
            "completed_at": "2026-07-27T05:01:00Z",
        }
        decision = self.checkpoint.repository_test_cadence_decision(
            job,
            job_rows=[job],
            committed_job_rows=[],
            role_rows=[
                {
                    "role_id": "scientist",
                    "version": "1",
                    "role_kind": "scientific_test",
                }
            ],
        )

        self.assertTrue(decision["required"])
        self.assertEqual(decision["reason"], "cadence_state_invalid_fail_safe")

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
            result = self.checkpoint._checkpoint_impl(
                "AJ-TEST", validation_mode="legacy"
            )

        self.assertEqual(result["reason"], "git commit failed")
        self.assertIn(["git", "read-tree", "original-tree"], commands)


if __name__ == "__main__":
    unittest.main()
