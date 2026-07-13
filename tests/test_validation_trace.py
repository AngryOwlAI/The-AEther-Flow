from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = REPO_ROOT / "scripts" / "validation" / "trace.py"


def load_trace_module():
    spec = importlib.util.spec_from_file_location("validation_trace_p1_t04", TRACE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TRACE = load_trace_module()


class ValidationTraceTests(unittest.TestCase):
    def make_session(self, root: Path, trace_id: str) -> object:
        return TRACE.TraceSession(trace_id=trace_id, trace_dir=root, enabled=True)

    def test_disabled_session_changes_neither_status_nor_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            session = TRACE.TraceSession(trace_id="disabled", trace_dir=root, enabled=False)
            completed = session.run_subprocess(
                [sys.executable, "-c", "print('unchanged')"],
                scope="working_tree",
                tree_hash="tree-a",
                cache_state="disabled",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(completed.stdout, "unchanged\n")
            self.assertEqual(list(root.iterdir()), [])

    def test_gate_event_contains_required_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self.make_session(Path(temp_dir), "required-fields")
            with session.gate(
                "research_control_core",
                scope="working_tree",
                tree_hash="tree-a",
                cache_state="disabled",
            ) as span:
                span.set_result(status="PASS", output_bytes=17)
            event = session.finalize()["events"][0]
            required = {
                "gate_id",
                "scope",
                "tree_hash",
                "parent_gate_id",
                "start",
                "end",
                "status",
                "output_bytes",
                "cache_state",
            }
            self.assertTrue(required.issubset(event))
            self.assertEqual(event["output_bytes"], 17)
            self.assertTrue(event["local_non_authoritative"])

    def test_nested_parentage_and_duplicate_identity_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self.make_session(Path(temp_dir), "nested")
            with session.gate(
                "profile_full_research_control",
                scope="working_tree",
                tree_hash="tree-a",
                cache_state="disabled",
            ):
                for _ in range(2):
                    with session.gate(
                        "memory_core",
                        scope="working_tree",
                        tree_hash="tree-a",
                        cache_state="disabled",
                    ):
                        pass
            report = session.finalize()
            root_event = next(
                event
                for event in report["events"]
                if event["gate_id"] == "profile_full_research_control"
            )
            children = [
                event for event in report["events"] if event["gate_id"] == "memory_core"
            ]
            self.assertEqual(len(children), 2)
            self.assertTrue(
                all(event["parent_event_id"] == root_event["event_id"] for event in children)
            )
            self.assertTrue(
                all(event["parent_gate_id"] == root_event["gate_id"] for event in children)
            )
            self.assertEqual(report["duplicate_identity_count"], 1)
            self.assertFalse(children[0]["duplicate_identity"])
            self.assertTrue(children[1]["duplicate_identity"])

    def test_normalized_serialization_is_deterministic(self) -> None:
        normalized: list[str] = []
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for trace_id in ("first", "second"):
                session = self.make_session(root, trace_id)
                with session.gate(
                    "research_control_core",
                    scope="working_tree",
                    tree_hash="tree-a",
                    cache_state="disabled",
                ):
                    with session.gate(
                        "claim_language_changed",
                        scope="working_tree",
                        tree_hash="tree-a",
                        cache_state="disabled",
                    ):
                        pass
                report = session.finalize()
                normalized.append(TRACE.normalized_trace_json(report["events"]))
        self.assertEqual(normalized[0], normalized[1])

    def test_subprocess_wrapper_preserves_failure_without_leaking_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self.make_session(Path(temp_dir), "failure")
            completed = session.run_subprocess(
                [
                    sys.executable,
                    "-c",
                    "import sys; print('private detail'); sys.exit(7)",
                ],
                gate_id="fixture_failure",
                scope="fixture",
                tree_hash="tree-a",
                cache_state="disabled",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            report = session.finalize()
            self.assertEqual(completed.returncode, 7)
            event = report["events"][0]
            self.assertEqual(event["status"], "FAIL")
            self.assertEqual(event["output_bytes"], len("private detail\n"))
            serialized = json.dumps(report)
            self.assertNotIn("private detail", serialized)

    def test_recursive_python_subprocess_is_a_child_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            child_script = root / "child.py"
            child_script.write_text(
                "import subprocess, sys\n"
                "result = subprocess.run([sys.executable, '-c', 'print(42)'], "
                "text=True, stdout=subprocess.PIPE, check=False)\n"
                "raise SystemExit(result.returncode)\n",
                encoding="utf-8",
            )
            session = self.make_session(root / "traces", "recursive")
            completed = session.run_subprocess(
                [sys.executable, str(child_script)],
                gate_id="parent_python_gate",
                scope="fixture",
                tree_hash="tree-a",
                cache_state="disabled",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            report = session.finalize()
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(report["event_count"], 2)
            parent = next(
                event for event in report["events"] if event["gate_id"] == "parent_python_gate"
            )
            child = next(event for event in report["events"] if event is not parent)
            self.assertEqual(child["parent_event_id"], parent["event_id"])
            self.assertEqual(child["parent_gate_id"], parent["gate_id"])

    def test_known_commands_use_canonical_gate_ids(self) -> None:
        cases = {
            (
                ".venv/bin/python",
                "scripts/research_control/validate_research_control.py",
                "--check-diff",
            ): "research_control_diff",
            (
                ".venv/bin/python",
                ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
                "--validate-only",
            ): "memory_core",
            ("git", "diff", "--check"): "git_diff_check",
        }
        for command, expected in cases.items():
            with self.subTest(command=command):
                self.assertEqual(TRACE.canonical_gate_id(command), expected)

    def test_trace_write_failure_does_not_replace_command_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session = self.make_session(Path(temp_dir), "write-failure")
            with mock.patch.object(session, "_append_event", side_effect=OSError("no space")):
                completed = session.run_subprocess(
                    [sys.executable, "-c", "raise SystemExit(0)"],
                    gate_id="fixture",
                    scope="fixture",
                    tree_hash="tree-a",
                    cache_state="disabled",
                    check=False,
                )
            self.assertEqual(completed.returncode, 0)

    def test_environment_switch_can_disable_cli_tracing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "target.py"
            script.write_text("print('same output')\n", encoding="utf-8")
            environment = dict(os.environ)
            environment[TRACE.TRACE_ENV] = "0"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(TRACE_PATH),
                    "--gate-id",
                    "fixture",
                    "--scope",
                    "fixture",
                    "--tree-hash",
                    "tree-a",
                    "--trace-dir",
                    str(root / "traces"),
                    "--python-script",
                    str(script),
                ],
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(completed.stdout, "same output\n")
            self.assertFalse((root / "traces").exists())

    def test_enabled_cli_preserves_stdout_and_exit_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "target.py"
            script.write_text("print('same output')\n", encoding="utf-8")
            environment = dict(os.environ)
            environment[TRACE.TRACE_ENV] = "1"
            direct = subprocess.run(
                [sys.executable, str(script)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            traced = subprocess.run(
                [
                    sys.executable,
                    str(TRACE_PATH),
                    "--trace-id",
                    "enabled-cli",
                    "--gate-id",
                    "fixture",
                    "--scope",
                    "fixture",
                    "--tree-hash",
                    "tree-a",
                    "--trace-dir",
                    str(root / "traces"),
                    "--python-script",
                    str(script),
                ],
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(traced.returncode, direct.returncode)
            self.assertEqual(traced.stdout, direct.stdout)
            self.assertEqual(traced.stderr, direct.stderr)
            report = json.loads((root / "traces" / "enabled-cli.json").read_text())
            self.assertEqual(report["event_count"], 1)


if __name__ == "__main__":
    unittest.main()
