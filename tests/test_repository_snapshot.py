from __future__ import annotations

import csv
import hashlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validation.snapshot import (
    RepositorySnapshot,
    SnapshotParseError,
    SnapshotRequest,
    StaleSnapshotError,
    UndeclaredComponentError,
)


class SyntheticRepository:
    def __init__(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary_directory.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Snapshot Test")
        self.git("config", "user.email", "snapshot@example.invalid")

        self.write(
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "task_id,status\nRT-002,active\nRT-001,completed\n",
        )
        self.write(
            "registries/AGENT_JOB_REGISTRY.csv",
            "job_id,status,completion_path\n"
            "AJ-002,completed,research_control/tasks/RT-002/jobs/completions/AJC-002.yaml\n"
            "AJ-001,completed,research_control/tasks/RT-001/jobs/completions/AJC-001.yaml\n",
        )
        self.write(
            "research_control/program_state.yaml",
            'program_id: "fixture"\nstatus: "active"\n',
        )
        self.write(
            "research_control/handoffs/handoff-0002.yaml",
            'handoff_id: "handoff-0002"\nstatus: "active"\n',
        )
        self.write(
            "research_control/handoffs/handoff-0001.yaml",
            'handoff_id: "handoff-0001"\nstatus: "completed"\n',
        )
        self.write(
            "research_control/tasks/RT-002/jobs/completions/AJC-002.yaml",
            'completion_id: "AJC-002"\nvalidation_status: "PASS"\n',
        )
        self.write(
            "research_control/tasks/RT-001/jobs/completions/AJC-001.yaml",
            'completion_id: "AJC-001"\nvalidation_status: "PASS"\n',
        )
        self.write(
            "control/example.yaml",
            'alpha:\n  beta: "value"\n  flags:\n    - "one"\n    - "two"\nzeta: true\n',
        )
        self.write("sources/info.txt", "snapshot source\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture baseline")

    def close(self) -> None:
        self._temporary_directory.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()

    def write(self, relative_path: str, text: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class RepositorySnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = SyntheticRepository()

    def tearDown(self) -> None:
        self.repository.close()

    def capture(
        self,
        request: SnapshotRequest,
        *,
        scope: str = "working",
        configuration: dict[str, object] | None = None,
    ) -> RepositorySnapshot:
        return RepositorySnapshot.capture(
            self.repository.root,
            request,
            scope=scope,
            configuration=configuration,
        )

    def test_capture_is_lazy_and_registry_parse_is_cached(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(registries=("RESEARCH_TASK_REGISTRY.csv",))
        )
        self.assertEqual(snapshot.instrumentation["file_reads"], 0)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 0)

        first = snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")
        self.assertEqual([row["task_id"] for row in first], ["RT-002", "RT-001"])
        self.assertEqual(snapshot.instrumentation["file_reads"], 1)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 1)

        second = snapshot.registry_rows("registries/RESEARCH_TASK_REGISTRY.csv")
        self.assertIs(first, second)
        self.assertEqual(snapshot.instrumentation["file_reads"], 1)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 1)
        self.assertGreaterEqual(snapshot.instrumentation["cache_hits"], 1)

    def test_views_and_instrumentation_are_deeply_immutable(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(
                registries=("RESEARCH_TASK_REGISTRY.csv",),
                yaml_paths=("control/example.yaml",),
            )
        )
        rows = snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")
        payload = snapshot.yaml_document("control/example.yaml")

        with self.assertRaises(TypeError):
            rows[0]["status"] = "changed"  # type: ignore[index]
        with self.assertRaises(AttributeError):
            rows.append({})  # type: ignore[attr-defined]
        with self.assertRaises(TypeError):
            payload["alpha"]["beta"] = "changed"  # type: ignore[index]
        self.assertIsInstance(payload["alpha"]["flags"], tuple)
        with self.assertRaises(TypeError):
            snapshot.instrumentation["file_reads"] = 99  # type: ignore[index]

    def test_undeclared_components_are_rejected(self) -> None:
        snapshot = self.capture(SnapshotRequest())
        with self.assertRaises(UndeclaredComponentError):
            snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")
        with self.assertRaises(UndeclaredComponentError):
            snapshot.yaml_document("control/example.yaml")
        with self.assertRaises(UndeclaredComponentError):
            snapshot.program_state()
        with self.assertRaises(UndeclaredComponentError):
            snapshot.handoffs()
        with self.assertRaises(UndeclaredComponentError):
            snapshot.job_completions()
        with self.assertRaises(UndeclaredComponentError):
            snapshot.changed_paths()
        with self.assertRaises(UndeclaredComponentError):
            snapshot.source_hash("sources/info.txt")
        self.assertEqual(snapshot.instrumentation["file_reads"], 0)

    def test_program_handoffs_and_completions_are_deterministic_and_cached(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(
                include_program_state=True,
                include_handoffs=True,
                include_job_completions=True,
            )
        )
        self.assertEqual(snapshot.program_state()["program_id"], "fixture")
        handoffs = snapshot.handoffs()
        completions = snapshot.job_completions()

        self.assertEqual(
            [document.path for document in handoffs],
            [
                "research_control/handoffs/handoff-0001.yaml",
                "research_control/handoffs/handoff-0002.yaml",
            ],
        )
        self.assertEqual(
            [document.path for document in completions],
            [
                "research_control/tasks/RT-001/jobs/completions/AJC-001.yaml",
                "research_control/tasks/RT-002/jobs/completions/AJC-002.yaml",
            ],
        )
        self.assertEqual(snapshot.instrumentation["file_reads"], 6)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 1)
        self.assertEqual(snapshot.instrumentation["yaml_parses"], 5)

        self.assertIs(handoffs, snapshot.handoffs())
        self.assertIs(completions, snapshot.job_completions())
        self.assertEqual(snapshot.instrumentation["file_reads"], 6)

    def test_working_snapshot_rejects_changed_tracked_content(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(registries=("RESEARCH_TASK_REGISTRY.csv",))
        )
        snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")
        self.repository.write(
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "task_id,status\nRT-002,completed\nRT-001,completed\n",
        )
        with self.assertRaises(StaleSnapshotError):
            snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")

    def test_working_snapshot_binds_untracked_file_content(self) -> None:
        self.repository.write("scratch/input.txt", "first\n")
        snapshot = self.capture(
            SnapshotRequest(source_hash_paths=("scratch/input.txt",))
        )
        first_hash = snapshot.source_hash("scratch/input.txt")
        self.assertEqual(first_hash, hashlib.sha256(b"first\n").hexdigest())

        self.repository.write("scratch/input.txt", "second\n")
        with self.assertRaises(StaleSnapshotError):
            snapshot.source_hash("scratch/input.txt")

    def test_failed_midread_freshness_check_does_not_cache_source(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(source_hash_paths=("sources/info.txt",))
        )
        real_assert_fresh = snapshot.assert_fresh
        check_count = 0

        def fail_second_check() -> None:
            nonlocal check_count
            check_count += 1
            if check_count == 2:
                raise StaleSnapshotError("simulated post-read state change")
            real_assert_fresh()

        snapshot.assert_fresh = fail_second_check  # type: ignore[method-assign]
        with self.assertRaises(StaleSnapshotError):
            snapshot.source_hash("sources/info.txt")
        self.assertEqual(snapshot.instrumentation["file_reads"], 1)

        snapshot.assert_fresh = real_assert_fresh  # type: ignore[method-assign]
        expected = hashlib.sha256(b"snapshot source\n").hexdigest()
        self.assertEqual(snapshot.source_hash("sources/info.txt"), expected)
        self.assertEqual(snapshot.instrumentation["file_reads"], 2)

    def test_staged_snapshot_reads_index_and_rejects_index_change(self) -> None:
        self.repository.write("control/example.yaml", 'version: "staged-one"\n')
        self.repository.git("add", "control/example.yaml")
        self.repository.write("control/example.yaml", 'version: "working-only"\n')
        snapshot = self.capture(
            SnapshotRequest(yaml_paths=("control/example.yaml",)),
            scope="staged",
        )

        self.assertEqual(snapshot.yaml_document("control/example.yaml")["version"], "staged-one")
        snapshot.assert_fresh()

        self.repository.git("add", "control/example.yaml")
        with self.assertRaises(StaleSnapshotError):
            snapshot.yaml_document("control/example.yaml")

    def test_strict_yaml_and_csv_errors_keep_source_context(self) -> None:
        self.repository.write("control/example.yaml", "bad: unquoted: colon\n")
        yaml_snapshot = self.capture(
            SnapshotRequest(yaml_paths=("control/example.yaml",))
        )
        with self.assertRaisesRegex(SnapshotParseError, "control/example.yaml"):
            yaml_snapshot.yaml_document("control/example.yaml")

        self.repository.write(
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "task_id,task_id\nRT-001,RT-001\n",
        )
        csv_snapshot = self.capture(
            SnapshotRequest(registries=("RESEARCH_TASK_REGISTRY.csv",))
        )
        with self.assertRaisesRegex(SnapshotParseError, "headers are duplicated"):
            csv_snapshot.registry_rows("RESEARCH_TASK_REGISTRY.csv")

    def test_changed_paths_are_sorted_and_scope_specific(self) -> None:
        self.repository.write("sources/info.txt", "changed\n")
        self.repository.write("alpha.txt", "untracked\n")
        working = self.capture(SnapshotRequest(include_git_changed_paths=True))
        self.assertEqual(
            working.changed_paths(),
            ("alpha.txt", "sources/info.txt"),
        )

        self.repository.git("add", "sources/info.txt")
        staged = self.capture(
            SnapshotRequest(include_git_changed_paths=True),
            scope="staged",
        )
        self.assertEqual(staged.changed_paths(), ("sources/info.txt",))

    def test_source_hashes_are_stable_sorted_and_parse_free(self) -> None:
        snapshot = self.capture(
            SnapshotRequest(
                source_hash_paths=(
                    "sources/info.txt",
                    "control/example.yaml",
                )
            )
        )
        expected = hashlib.sha256(b"snapshot source\n").hexdigest()
        self.assertEqual(snapshot.source_hash("sources/info.txt"), expected)
        hashes = snapshot.source_hashes()
        self.assertEqual(tuple(hashes), ("control/example.yaml", "sources/info.txt"))
        self.assertEqual(snapshot.instrumentation["file_reads"], 2)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 0)
        self.assertEqual(snapshot.instrumentation["yaml_parses"], 0)
        self.assertEqual(snapshot.source_hash("sources/info.txt"), expected)
        self.assertEqual(snapshot.instrumentation["file_reads"], 2)

    def test_identity_is_deterministic_and_configuration_sensitive(self) -> None:
        request = SnapshotRequest(
            registries=("RESEARCH_TASK_REGISTRY.csv",),
            include_program_state=True,
        )
        first = self.capture(request, configuration={"profile": "affected", "strict": True})
        second = self.capture(request, configuration={"strict": True, "profile": "affected"})
        changed = self.capture(request, configuration={"profile": "full", "strict": True})

        self.assertEqual(first.identity.snapshot_id, second.identity.snapshot_id)
        self.assertEqual(
            first.identity.configuration_fingerprint,
            second.identity.configuration_fingerprint,
        )
        self.assertNotEqual(first.identity.snapshot_id, changed.identity.snapshot_id)
        self.assertEqual(first.instrumentation["file_reads"], 0)

    def test_shared_snapshot_preserves_findings_with_fewer_parses(self) -> None:
        registry_paths = (
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
        )

        def parse_direct(path_text: str) -> tuple[dict[str, str], ...]:
            text = (self.repository.root / path_text).read_text(encoding="utf-8")
            return tuple(
                {key: value or "" for key, value in row.items()}
                for row in csv.DictReader(io.StringIO(text, newline=""))
            )

        def findings(
            task_rows: tuple[dict[str, str], ...] | tuple[object, ...],
            job_rows: tuple[dict[str, str], ...] | tuple[object, ...],
        ) -> tuple[str, ...]:
            task_findings = [
                f"task:{row['task_id']}:{row['status']}"
                for row in task_rows
                if row["status"] != "completed"  # type: ignore[index]
            ]
            job_findings = [
                f"job:{row['job_id']}:{row['status']}"
                for row in job_rows
                if row["status"] != "completed"  # type: ignore[index]
            ]
            return tuple(sorted(task_findings + job_findings))

        direct_results = []
        direct_reads = 0
        direct_parses = 0
        for _consumer in ("research_control", "dependency_graph", "physics_metrics"):
            direct_results.append(
                findings(parse_direct(registry_paths[0]), parse_direct(registry_paths[1]))
            )
            direct_reads += 2
            direct_parses += 2

        snapshot = self.capture(SnapshotRequest(registries=registry_paths))
        shared_results = []
        for _consumer in ("research_control", "dependency_graph", "physics_metrics"):
            shared_results.append(
                findings(
                    snapshot.registry_rows(registry_paths[0]),
                    snapshot.registry_rows(registry_paths[1]),
                )
            )

        self.assertEqual(shared_results, direct_results)
        self.assertEqual(direct_reads, 6)
        self.assertEqual(direct_parses, 6)
        self.assertEqual(snapshot.instrumentation["file_reads"], 2)
        self.assertEqual(snapshot.instrumentation["csv_parses"], 2)
        self.assertEqual(snapshot.instrumentation["component_loads"], 2)


if __name__ == "__main__":
    unittest.main()
