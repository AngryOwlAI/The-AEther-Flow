from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
LEGACY_COVERAGE_PATH = (
    ROOT / "tests/fixtures/validation_manifest/legacy_gate_coverage_v1.json"
)

from scripts.validation.plan import load_manifest
from scripts.validation.staged import (
    GateOutcome,
    StagedExecutionContext,
    run_staged_acceptance,
)


def classification(
    paths: tuple[str, ...], *, unknown: tuple[str, ...] = ()
) -> dict[str, object]:
    details = [
        {
            "path": path,
            "tags": ["unknown_governed_path"] if path in unknown else ["validator_code"],
            "reasons": [],
            "canonical_paths": [],
            "generated_derivatives": [],
            "affected_source_object_ids": [],
        }
        for path in paths
    ]
    return {
        "changed_paths": list(paths),
        "blocked_paths": [],
        "ignored_paths": [],
        "path_family_tags": ["unknown_governed_path"] if unknown else ["validator_code"],
        "path_family_details": details,
        "recommended_validation_profile": "full" if unknown else "affected",
    }


class TemporaryGitRepository:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.git("config", "user.email", "staged-tests@example.invalid")
        self.git("config", "user.name", "Staged Tests")

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
        for path, text in files.items():
            self.write(path, text)
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "baseline")


class PassingExecutor:
    def __init__(self, repo: TemporaryGitRepository | None = None) -> None:
        self.repo = repo
        self.calls: list[tuple[tuple[str, ...], StagedExecutionContext]] = []
        self.mutate_index = False

    def __call__(
        self,
        gate_ids: tuple[str, ...],
        context: StagedExecutionContext,
    ) -> tuple[GateOutcome, ...]:
        self.calls.append((gate_ids, context))
        if self.mutate_index:
            assert self.repo is not None
            self.repo.write("late.txt", "late index mutation\n")
            self.repo.git("add", "late.txt")
        return tuple(
            GateOutcome(
                gate_id=gate_id,
                status="PASS",
                scope=context.scope,
                tree_hash=context.tree_hash,
            )
            for gate_id in gate_ids
        )


class StagedValidationTests(unittest.TestCase):
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
        executor: PassingExecutor | None = None,
        classifier=None,
        prior_evidence: tuple[dict[str, object], ...] = (),
        legacy_override: dict[str, str] | None = None,
        allowlist: tuple[str, ...] | None = None,
    ) -> dict[str, object]:
        executor = executor or PassingExecutor()
        captured: dict[str, tuple[str, ...]] = {}

        def recording_executor(
            gate_ids: tuple[str, ...], context: StagedExecutionContext
        ) -> tuple[GateOutcome, ...]:
            captured["gate_ids"] = gate_ids
            return executor(gate_ids, context)

        def legacy_statuses(gate_ids: tuple[str, ...]) -> dict[str, str]:
            statuses = {gate_id: "PASS" for gate_id in gate_ids}
            statuses.update(legacy_override or {})
            return statuses

        return run_staged_acceptance(
            repo.root,
            transaction_paths=paths,
            allowed_path_globs=allowlist or tuple(paths),
            manifest=self.manifest,
            classifier=classifier
            or (lambda values, **_: classification(tuple(values))),
            gate_executor=recording_executor,
            legacy_status_provider=legacy_statuses,
            prior_evidence=prior_evidence,
            working_plan={
                "scope": "working",
                "tree_hash": "working-sha256:" + ("a" * 64),
                "selected_gate_ids": ["classify_changes"],
            },
        )

    def test_add_delete_rename_and_generated_output_bind_one_exact_tree(self) -> None:
        repo = self.repo()
        repo.commit_files(
            {
                "keep.py": "before\n",
                "delete.py": "delete\n",
                "rename-old.py": "rename\n",
            }
        )
        entry_tree = repo.git("write-tree")
        repo.write("keep.py", "after\n")
        (repo.root / "delete.py").unlink()
        (repo.root / "rename-old.py").rename(repo.root / "rename-new.py")
        repo.write("wiki/generated.md", "generated\n")
        paths = [
            "keep.py",
            "delete.py",
            "rename-old.py",
            "rename-new.py",
            "wiki/generated.md",
        ]
        executor = PassingExecutor()

        receipt = self.run_acceptance(repo, paths, executor=executor)

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["scope"], "staged")
        self.assertTrue(receipt["tree_hash"].startswith("git-sha1:"))
        self.assertEqual(
            receipt["staged_paths"],
            sorted(paths),
        )
        self.assertEqual(len(executor.calls), 1)
        gate_ids, context = executor.calls[0]
        self.assertEqual(len(gate_ids), len(set(gate_ids)))
        self.assertEqual(context.tree_hash, receipt["tree_hash"])
        legacy_coverage = json.loads(LEGACY_COVERAGE_PATH.read_text(encoding="utf-8"))
        legacy_blocking = {
            entry["canonical_gate_id"]
            for entry in legacy_coverage["entries"]
            if entry["authority"] == "blocking" and not entry["mutating"]
        }
        self.assertLessEqual(set(gate_ids), legacy_blocking)
        self.assertEqual(receipt["shadow_comparison"]["status"], "PASS")
        self.assertEqual(receipt["plans"]["working"]["scope"], "working")
        self.assertFalse(receipt["plans"]["working"]["staged_reusable"])
        self.assertEqual(receipt["plans"]["staged"]["scopes"], ["staged"])
        self.assertEqual(repo.git("write-tree"), entry_tree)
        self.assertTrue(receipt["index"]["restored"])

    def test_unstaged_unrelated_residue_blocks_before_gate_execution(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("tracked.py", "after\n")
        repo.write("unrelated.txt", "residue\n")
        executor = PassingExecutor()

        receipt = self.run_acceptance(repo, ["tracked.py"], executor=executor)

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "unstaged_transaction_residue")
        self.assertEqual(receipt["residue"]["before_execution"], ["unrelated.txt"])
        self.assertEqual(executor.calls, [])
        self.assertEqual(repo.git("write-tree"), entry_tree)

    def test_preexisting_staged_path_outside_transaction_is_rejected_and_restored(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n", "stale.py": "before\n"})
        repo.write("stale.py", "already staged\n")
        repo.git("add", "stale.py")
        entry_tree = repo.git("write-tree")
        repo.write("tracked.py", "transaction\n")
        executor = PassingExecutor()

        receipt = self.run_acceptance(
            repo,
            ["tracked.py"],
            executor=executor,
            allowlist=("tracked.py", "stale.py"),
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(
            receipt["finding"]["code"], "staged_path_outside_transaction"
        )
        self.assertEqual(executor.calls, [])
        self.assertEqual(repo.git("write-tree"), entry_tree)
        self.assertTrue(receipt["index"]["restored"])

    def test_stale_working_evidence_never_satisfies_staged_gate(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        repo.write("tracked.py", "after\n")
        executor = PassingExecutor()
        stale = (
            {
                "gate_id": "classify_changes",
                "status": "PASS",
                "scope": "tree_state=working;base_ref=HEAD",
                "tree_hash": "working-sha256:" + ("b" * 64),
            },
        )

        receipt = self.run_acceptance(
            repo,
            ["tracked.py"],
            executor=executor,
            prior_evidence=stale,
        )

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(receipt["evidence_reuse"]["accepted_gate_ids"], [])
        self.assertEqual(
            receipt["evidence_reuse"]["rejections"][0]["reason"],
            "working_scope_cannot_satisfy_staged",
        )

    def test_unknown_governed_path_fails_closed_and_restores_index(self) -> None:
        repo = self.repo()
        repo.commit_files({"known.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("future.rule", "unknown\n")
        executor = PassingExecutor()

        receipt = self.run_acceptance(
            repo,
            ["future.rule"],
            executor=executor,
            classifier=lambda values, **_: classification(
                tuple(values), unknown=("future.rule",)
            ),
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "unknown_or_blocked_path")
        self.assertEqual(executor.calls, [])
        self.assertEqual(repo.git("write-tree"), entry_tree)

    def test_gate_index_mutation_blocks_wrong_tree_and_restores_entry_index(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("tracked.py", "after\n")
        executor = PassingExecutor(repo)
        executor.mutate_index = True

        receipt = self.run_acceptance(
            repo,
            ["tracked.py"],
            executor=executor,
            allowlist=("tracked.py", "late.txt"),
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "staged_tree_changed")
        self.assertEqual(repo.git("write-tree"), entry_tree)
        self.assertTrue(receipt["index"]["restored"])

    def test_gate_executor_exception_restores_entry_index(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("tracked.py", "after\n")

        receipt = run_staged_acceptance(
            repo.root,
            transaction_paths=("tracked.py",),
            allowed_path_globs=("tracked.py",),
            manifest=self.manifest,
            classifier=lambda values, **_: classification(tuple(values)),
            gate_executor=lambda _gate_ids, _context: (_ for _ in ()).throw(
                RuntimeError("fixture executor failure")
            ),
            legacy_status_provider=lambda gate_ids: {
                gate_id: "PASS" for gate_id in gate_ids
            },
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "gate_executor_failed")
        self.assertEqual(repo.git("write-tree"), entry_tree)
        self.assertTrue(receipt["index"]["restored"])

    def test_unexplained_legacy_shadow_mismatch_fails_closed(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        repo.write("tracked.py", "after\n")

        receipt = self.run_acceptance(
            repo,
            ["tracked.py"],
            legacy_override={"classify_changes": "FAIL"},
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "legacy_shadow_mismatch")
        self.assertIn("classify_changes", receipt["shadow_comparison"]["mismatches"])
        self.assertTrue(receipt["authority"]["legacy_result_authoritative"])

    def test_duplicate_or_missing_gate_outcomes_fail_closed(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        repo.write("tracked.py", "after\n")

        def duplicate_executor(
            gate_ids: tuple[str, ...], context: StagedExecutionContext
        ) -> tuple[GateOutcome, ...]:
            outcomes = [
                GateOutcome(gate_id, "PASS", context.scope, context.tree_hash)
                for gate_id in gate_ids
            ]
            outcomes.append(outcomes[0])
            return tuple(outcomes)

        receipt = run_staged_acceptance(
            repo.root,
            transaction_paths=("tracked.py",),
            allowed_path_globs=("tracked.py",),
            manifest=self.manifest,
            classifier=lambda values, **_: classification(tuple(values)),
            gate_executor=duplicate_executor,
            legacy_status_provider=lambda gate_ids: {
                gate_id: "PASS" for gate_id in gate_ids
            },
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "gate_execution_cardinality")
        self.assertTrue(receipt["index"]["restored"])

    def test_allowlist_rejects_unapproved_staged_path(self) -> None:
        repo = self.repo()
        repo.commit_files({"tracked.py": "before\n"})
        entry_tree = repo.git("write-tree")
        repo.write("tracked.py", "after\n")
        repo.write("generated/output.json", "{}\n")

        receipt = self.run_acceptance(
            repo,
            ["tracked.py", "generated/output.json"],
            allowlist=("tracked.py",),
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["finding"]["code"], "path_outside_agentjob_allowlist")
        self.assertEqual(repo.git("write-tree"), entry_tree)


if __name__ == "__main__":
    unittest.main()
