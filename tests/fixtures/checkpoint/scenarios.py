"""Rollback-safe checkpoint scenarios over synthetic Git repositories."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.validation.plan import load_manifest
from scripts.validation.staged import (
    GateOutcome,
    StagedExecutionContext,
    run_staged_acceptance,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"


def classification(paths, **_kwargs) -> dict[str, object]:
    """Classify synthetic paths without reading live registries or control state."""

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
    """Small real Git repository whose entry index and HEAD are observable."""

    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "checkpoint-fixture@example.invalid")
        self.git("config", "user.name", "Checkpoint Fixture")

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
        self.write(".gitignore", ".checkpoint-cache/\n")
        for path, text in files.items():
            self.write(path, text)
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "baseline")


@dataclass(frozen=True, slots=True)
class PlannerScenario:
    name: str
    planner_status: str
    legacy_status: str
    expected_status: str
    expected_finding: str = ""


class CheckpointFixtureTests(unittest.TestCase):
    """Exercise checkpoint safety without validating or mutating the live tree."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)

    def repo(self) -> TemporaryGitRepository:
        repo = TemporaryGitRepository()
        self.addCleanup(repo.cleanup)
        return repo

    def run_acceptance(
        self,
        repo: TemporaryGitRepository,
        paths: list[str],
        *,
        planner_status: str = "PASS",
        legacy_status: str = "PASS",
    ) -> tuple[dict[str, object], list[tuple[str, ...]]]:
        calls: list[tuple[str, ...]] = []

        def injected_executor(
            gate_ids: tuple[str, ...],
            context: StagedExecutionContext,
        ) -> tuple[GateOutcome, ...]:
            calls.append(gate_ids)
            return tuple(
                GateOutcome(
                    gate_id=gate_id,
                    status=planner_status,
                    scope=context.scope,
                    tree_hash=context.tree_hash,
                )
                for gate_id in gate_ids
            )

        receipt = run_staged_acceptance(
            repo.root,
            transaction_paths=paths,
            allowed_path_globs=paths,
            manifest=self.manifest,
            classifier=classification,
            gate_executor=injected_executor,
            legacy_status_provider=lambda gate_ids: {
                gate_id: legacy_status for gate_id in gate_ids
            },
            agent_job_id="AJ-CHECKPOINT-FIXTURE",
        )
        return receipt, calls

    def test_actual_git_add_delete_rename_restores_exact_entry_index(self) -> None:
        repo = self.repo()
        repo.commit_files(
            {
                "modify.py": "before\n",
                "delete.py": "delete\n",
                "rename-old.py": "rename\n",
            }
        )
        entry_tree = repo.git("write-tree")
        entry_head = repo.git("rev-parse", "HEAD")
        repo.write("modify.py", "after\n")
        repo.write("added.py", "added\n")
        (repo.root / "delete.py").unlink()
        (repo.root / "rename-old.py").rename(repo.root / "rename-new.py")
        paths = [
            "added.py",
            "delete.py",
            "modify.py",
            "rename-new.py",
            "rename-old.py",
        ]

        receipt, calls = self.run_acceptance(repo, paths)

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["staged_paths"], sorted(paths))
        self.assertNotEqual(receipt["index"]["final_staged_tree"], entry_tree)
        self.assertEqual(receipt["index"]["restored_tree"], entry_tree)
        self.assertTrue(receipt["index"]["restored"])
        self.assertEqual(repo.git("write-tree"), entry_tree)
        self.assertEqual(repo.git("rev-parse", "HEAD"), entry_head)
        self.assertEqual(len(calls), 1)

    def test_residue_and_ignored_paths_fail_before_commit_and_restore_index(self) -> None:
        for scenario in ("unstaged_residue", "ignored_only"):
            with self.subTest(scenario=scenario):
                repo = self.repo()
                repo.commit_files({"tracked.py": "before\n"})
                entry_tree = repo.git("write-tree")
                entry_head = repo.git("rev-parse", "HEAD")
                if scenario == "unstaged_residue":
                    repo.write("tracked.py", "after\n")
                    repo.write("outside.txt", "residue\n")
                    paths = ["tracked.py"]
                    expected_finding = "unstaged_transaction_residue"
                else:
                    repo.write(".checkpoint-cache/result.json", "{}\n")
                    paths = [".checkpoint-cache/result.json"]
                    expected_finding = "git_command_failed"

                receipt, calls = self.run_acceptance(repo, paths)

                self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
                self.assertEqual(receipt["finding"]["code"], expected_finding)
                self.assertEqual(calls, [])
                self.assertEqual(receipt["index"]["restored_tree"], entry_tree)
                self.assertTrue(receipt["index"]["restored"])
                self.assertEqual(repo.git("write-tree"), entry_tree)
                self.assertEqual(repo.git("rev-parse", "HEAD"), entry_head)
                self.assertFalse(receipt["authority"]["commit_performed"])

    def test_injected_planner_outcomes_restore_index_and_never_commit(self) -> None:
        scenarios = (
            PlannerScenario("pass", "PASS", "PASS", "PASS"),
            PlannerScenario("fail", "FAIL", "FAIL", "FAIL"),
            PlannerScenario("advisory", "WARN", "WARN", "FAIL"),
            PlannerScenario("cache_hit", "CACHE_HIT", "CACHE_HIT", "FAIL"),
            PlannerScenario(
                "mismatch",
                "PASS",
                "FAIL",
                "BLOCKED_CONFIGURATION",
                "legacy_shadow_mismatch",
            ),
        )
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        entry_tree = repo.git("write-tree")
        entry_head = repo.git("rev-parse", "HEAD")
        repo.write("tracked.py", "after\n")
        for scenario in scenarios:
            with self.subTest(scenario=scenario.name):
                receipt, calls = self.run_acceptance(
                    repo,
                    ["tracked.py"],
                    planner_status=scenario.planner_status,
                    legacy_status=scenario.legacy_status,
                )

                self.assertEqual(receipt["status"], scenario.expected_status)
                self.assertEqual(len(calls), 1)
                self.assertTrue(calls[0])
                if scenario.expected_finding:
                    self.assertEqual(
                        receipt["finding"]["code"],
                        scenario.expected_finding,
                    )
                    self.assertEqual(receipt["shadow_comparison"]["status"], "FAIL")
                else:
                    self.assertEqual(receipt["shadow_comparison"]["status"], "PASS")
                self.assertEqual(receipt["index"]["restored_tree"], entry_tree)
                self.assertTrue(receipt["index"]["restored"])
                self.assertEqual(repo.git("write-tree"), entry_tree)
                self.assertEqual(repo.git("rev-parse", "HEAD"), entry_head)
                self.assertFalse(receipt["authority"]["commit_performed"])
