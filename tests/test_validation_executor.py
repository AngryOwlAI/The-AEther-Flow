from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

from scripts.validation.executor import (
    AdapterResult,
    ExecutionContext,
    ExecutorError,
    SubprocessAdapter,
    execute_plan,
)
from scripts.validation.plan import build_plan
from scripts.validation.run import DEFAULT_BINDINGS, load_adapters, load_plan


def gate(
    gate_id: str,
    *,
    severity: str = "blocking",
    cost_class: str = "fast",
    prerequisites: tuple[str, ...] = (),
    parallel_group: str = "test_read_only",
    mutating: bool = False,
    timeout_seconds: int = 5,
) -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "description": f"Synthetic {gate_id} gate.",
        "owner_role": "validator-engineer@0.2.0",
        "adapter": f"test:{gate_id}",
        "command_compatibility": [f"synthetic {gate_id}"],
        "input_globs": ["tests/**"],
        "output_globs": [],
        "global_invariant_justification": None,
        "scopes": ["working"],
        "severity": severity,
        "mutating": mutating,
        "cost_class": cost_class,
        "prerequisites": list(prerequisites),
        "supersedes": [],
        "satisfies_obligations": [gate_id],
        "profiles": ["fast"],
        "path_tags": ["test"],
        "selection": {
            "operator": "all",
            "conditions": [
                {"condition_id": "always", "kind": "always", "values": []}
            ],
        },
        "timeout_seconds": timeout_seconds,
        "parallel_group": parallel_group,
        "cache_policy": "ineligible",
        "receipt_schema": "validation_gate_result_v1",
        "test_shard": "synthetic",
    }


def manifest(*gates: dict[str, object]) -> dict[str, object]:
    authority = {
        "benchmark_authority": False,
        "gate_chair_authority": False,
        "ontology_authority": False,
        "operational_validation_only": True,
        "physics_claim_authority": False,
        "proof_authority": False,
        "source_authoritative": False,
    }
    return {
        "authority": authority,
        "execution_authority": "legacy",
        "gates": list(gates),
        "manifest_id": "validation-gate-manifest-v1",
        "migration_epoch": "shadow_planner",
        "population_status": "populated",
        "schema_id": "validation_gate_manifest_v1",
        "schema_version": 1,
    }


def plan_for(document: dict[str, object]):
    return build_plan(
        document,
        {
            "changed_paths": ["tests/test_validation_executor.py"],
            "blocked_paths": [],
            "path_family_tags": ["test"],
            "path_family_details": [],
        },
        profile="fast",
        scopes=("working",),
    )


class FunctionAdapter:
    def __init__(self, function):
        self.function = function

    def run(self, context):
        return self.function(context)


def result_adapter(
    exit_code: int = 0,
    *,
    stdout: bytes = b"",
    stderr: bytes = b"",
    child_gates: tuple[str, ...] = (),
):
    def run(context):
        context.stdout_path.write_bytes(stdout)
        context.stderr_path.write_bytes(stderr)
        return AdapterResult(exit_code=exit_code, child_gates=child_gates)

    return FunctionAdapter(run)


class ValidationExecutorTests(unittest.TestCase):
    def execute(self, document, adapters, **kwargs):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return execute_plan(
            plan_for(document),
            document,
            adapters,
            receipt_root=Path(temporary.name),
            **kwargs,
        )

    def test_success_captures_raw_output_and_complete_metadata(self) -> None:
        document = manifest(gate("alpha"))
        outcome = self.execute(
            document,
            {
                "test:alpha": result_adapter(
                    stdout=b"full stdout\n",
                    stderr=b"full stderr\n",
                    child_gates=("child-a",),
                )
            },
        )

        self.assertEqual((outcome.status, outcome.exit_code), ("PASS", 0))
        self.assertIsNotNone(outcome.receipt_path)
        receipt = json.loads(outcome.receipt_path.read_text(encoding="utf-8"))
        gate_result = receipt["gate_results"][0]
        self.assertEqual(gate_result["gate_id"], "alpha")
        self.assertEqual(gate_result["reason"], "completed")
        self.assertEqual(gate_result["stdout_bytes"], 12)
        self.assertEqual(gate_result["stderr_bytes"], 12)
        self.assertEqual(gate_result["child_gates"], ["child-a"])
        self.assertEqual(gate_result["satisfied_obligations"], ["alpha"])
        self.assertTrue(Path(gate_result["stdout_path"]).read_bytes())
        self.assertFalse(receipt["authority"]["physics_claim_authority"])

    def test_fast_hard_failure_prevents_expensive_work(self) -> None:
        document = manifest(
            gate("fast_failure"),
            gate("slow_gate", cost_class="slow", parallel_group="slow"),
        )
        slow_called = False

        def slow(context):
            nonlocal slow_called
            slow_called = True
            return AdapterResult()

        outcome = self.execute(
            document,
            {
                "test:fast_failure": result_adapter(9),
                "test:slow_gate": FunctionAdapter(slow),
            },
        )

        self.assertEqual((outcome.status, outcome.exit_code), ("FAIL", 1))
        self.assertFalse(slow_called)
        self.assertEqual(
            [(entry["gate_id"], entry["status"], entry["reason"]) for entry in outcome.receipt["gate_results"]],
            [
                ("fast_failure", "FAIL", "nonzero_exit"),
                ("slow_gate", "SKIP_NOT_APPLICABLE", "fail_fast"),
            ],
        )

    def test_advisory_failure_warns_without_nonzero_run_exit(self) -> None:
        document = manifest(gate("advisory", severity="advisory"))
        outcome = self.execute(document, {"test:advisory": result_adapter(7)})
        self.assertEqual((outcome.status, outcome.exit_code), ("WARN", 0))
        self.assertEqual(outcome.receipt["gate_results"][0]["severity"], "advisory")

    def test_timeout_and_child_process_crash_are_explicit_failures(self) -> None:
        def timeout(_context):
            raise TimeoutError("bounded timeout")

        def crash(_context):
            raise ChildProcessError("signal 9")

        for gate_id, function, reason in (
            ("timeout", timeout, "timeout"),
            ("crash", crash, "child_process_crash"),
        ):
            with self.subTest(gate_id=gate_id):
                document = manifest(gate(gate_id))
                outcome = self.execute(
                    document, {f"test:{gate_id}": FunctionAdapter(function)}
                )
                self.assertEqual((outcome.status, outcome.exit_code), ("FAIL", 1))
                self.assertEqual(outcome.receipt["gate_results"][0]["reason"], reason)

    def test_cancellation_writes_a_valid_deterministic_partial_receipt(self) -> None:
        cancellation = threading.Event()
        document = manifest(
            gate("first"),
            gate("second", cost_class="medium", parallel_group="later"),
        )

        def cancel(context):
            context.cancellation.set()
            return AdapterResult()

        outcome = self.execute(
            document,
            {
                "test:first": FunctionAdapter(cancel),
                "test:second": result_adapter(),
            },
            cancellation=cancellation,
        )

        self.assertEqual((outcome.status, outcome.exit_code), ("BLOCKED_CONFIGURATION", 2))
        self.assertTrue(outcome.receipt["cancelled"])
        self.assertEqual(
            [(entry["gate_id"], entry["reason"]) for entry in outcome.receipt["gate_results"]],
            [("first", "completed"), ("second", "cancelled_before_start")],
        )
        self.assertTrue(outcome.receipt_path.is_file())

    def test_parallel_completion_never_changes_plan_order(self) -> None:
        document = manifest(gate("alpha"), gate("beta"))

        def delayed(delay):
            def run(context):
                time.sleep(delay)
                return AdapterResult()

            return FunctionAdapter(run)

        outcome = self.execute(
            document,
            {"test:alpha": delayed(0.03), "test:beta": delayed(0.0)},
            max_workers=2,
        )
        self.assertEqual(
            [entry["gate_id"] for entry in outcome.receipt["gate_results"]],
            ["alpha", "beta"],
        )

    def test_receipt_write_failure_fails_closed(self) -> None:
        document = manifest(gate("alpha"))
        with mock.patch("scripts.validation.executor.os.replace", side_effect=OSError("denied")):
            outcome = self.execute(document, {"test:alpha": result_adapter()})
        self.assertEqual((outcome.status, outcome.exit_code), ("BLOCKED_CONFIGURATION", 2))
        self.assertIsNone(outcome.receipt_path)
        self.assertEqual(outcome.error, "receipt_write_failed: denied")

    def test_mutated_plan_unknown_adapter_and_mutating_gate_fail_closed(self) -> None:
        document = manifest(gate("alpha"))
        planned = plan_for(document)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ExecutorError, "plan does not match"):
                execute_plan(
                    replace(planned, manifest_hash="0" * 64),
                    document,
                    {"test:alpha": result_adapter()},
                    receipt_root=Path(directory),
                )
            with self.assertRaisesRegex(ExecutorError, "missing adapter"):
                execute_plan(planned, document, {}, receipt_root=Path(directory))

        mutating_document = manifest(gate("mutator", mutating=True))
        with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(
            ExecutorError, "mutating gate"
        ):
            execute_plan(
                plan_for(mutating_document),
                mutating_document,
                {"test:mutator": result_adapter()},
                receipt_root=Path(directory),
            )

    def test_repo_local_cache_is_outside_job_mutation_scope(self) -> None:
        mutator = gate("memory_sync", mutating=True)
        mutator["output_globs"] = ["generated/**"]
        document = manifest(mutator)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            calls = 0

            def synchronize(_context):
                nonlocal calls
                calls += 1
                generated = root / "generated" / "state.txt"
                cache = root / ".local" / "content_semantics" / "state.txt"
                generated.parent.mkdir(parents=True, exist_ok=True)
                cache.parent.mkdir(parents=True, exist_ok=True)
                generated.write_text("stable\n", encoding="utf-8")
                cache.write_text(f"refresh-{calls}\n", encoding="utf-8")
                return AdapterResult()

            outcome = execute_plan(
                plan_for(document),
                document,
                {"test:memory_sync": FunctionAdapter(synchronize)},
                receipt_root=root / ".local" / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
                max_stabilization_passes=2,
            )

        self.assertEqual((outcome.status, outcome.exit_code), ("PASS", 0))
        self.assertEqual(calls, 2)
        self.assertEqual(
            outcome.receipt["mutator_barrier"]["changed_paths"],
            ["generated/state.txt"],
        )

    def test_subprocess_adapter_captures_output_and_reports_crash(self) -> None:
        success = manifest(gate("process"))
        outcome = self.execute(
            success,
            {
                "test:process": SubprocessAdapter(
                    (sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)")
                )
            },
        )
        gate_result = outcome.receipt["gate_results"][0]
        self.assertEqual(gate_result["status"], "PASS")
        self.assertGreater(gate_result["stdout_bytes"], 0)
        self.assertGreater(gate_result["stderr_bytes"], 0)

        crashed = self.execute(
            success,
            {
                "test:process": SubprocessAdapter(
                    (sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGKILL)")
                )
            },
        )
        self.assertEqual(crashed.receipt["gate_results"][0]["reason"], "child_process_crash")

    def test_subprocess_adapter_enforces_manifest_timeout(self) -> None:
        document = manifest(gate("process", timeout_seconds=1))
        outcome = self.execute(
            document,
            {
                "test:process": SubprocessAdapter(
                    (sys.executable, "-c", "import time; time.sleep(5)"),
                    poll_interval_seconds=0.01,
                )
            },
        )
        self.assertEqual((outcome.status, outcome.exit_code), ("FAIL", 1))
        self.assertEqual(outcome.receipt["gate_results"][0]["reason"], "timeout")

    def test_subprocess_adapter_expands_plan_path_placeholders_without_a_shell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stdout = root / "stdout"
            stderr = root / "stderr"
            context = ExecutionContext(
                gate_id="process",
                timeout_seconds=5,
                stdout_path=stdout,
                stderr_path=stderr,
                cancellation=threading.Event(),
                changed_paths=("tex/example.tex", "README.md"),
                scopes=("working",),
            )
            adapter = SubprocessAdapter(
                (
                    sys.executable,
                    "-c",
                    "import sys; print('|'.join(sys.argv[1:]))",
                    "{changed_paths}",
                    "{changed_path_args}",
                    "{changed_tex_paths}",
                    "{claim_language_mode_args}",
                )
            )

            result = adapter.run(context)

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(
                stdout.read_text(encoding="utf-8").strip(),
                "tex/example.tex|README.md|--paths|tex/example.tex|README.md|tex/example.tex|--changed",
            )

    def test_changed_tex_placeholder_is_a_safe_no_op_for_an_empty_target_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "must-not-run"
            stdout = root / "stdout"
            stderr = root / "stderr"
            adapter = SubprocessAdapter(
                (
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path(__import__('sys').argv[1]).write_text('ran')",
                    str(marker),
                    "{changed_tex_paths}",
                )
            )

            result = adapter.run(
                ExecutionContext(
                    gate_id="targeted_pdf_build",
                    timeout_seconds=5,
                    stdout_path=stdout,
                    stderr_path=stderr,
                    cancellation=threading.Event(),
                    changed_paths=(),
                    scopes=("repository",),
                )
            )

            self.assertEqual(result.exit_code, 0)
            self.assertFalse(marker.exists())
            self.assertIn("no changed TeX paths", stdout.read_text(encoding="utf-8"))
            self.assertEqual(stderr.read_bytes(), b"")

    def test_claim_language_placeholder_selects_staged_or_full_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter = SubprocessAdapter(
                (
                    sys.executable,
                    "-c",
                    "import sys; print('|'.join(sys.argv[1:]))",
                    "{claim_language_mode_args}",
                )
            )
            cases = (
                (("README.md",), ("staged",), "--staged"),
                ((), ("repository",), "--changed"),
            )
            for index, (changed_paths, scopes, expected) in enumerate(cases):
                with self.subTest(scopes=scopes):
                    stdout = root / f"stdout-{index}"
                    stderr = root / f"stderr-{index}"
                    result = adapter.run(
                        ExecutionContext(
                            gate_id="process",
                            timeout_seconds=5,
                            stdout_path=stdout,
                            stderr_path=stderr,
                            cancellation=threading.Event(),
                            changed_paths=changed_paths,
                            scopes=scopes,
                        )
                    )
                    self.assertEqual(result.exit_code, 0)
                    self.assertEqual(stdout.read_text(encoding="utf-8").strip(), expected)

    def test_loaded_plan_requires_exact_non_promotion_authority(self) -> None:
        document = manifest(gate("alpha"))
        planned = plan_for(document).to_dict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(planned), encoding="utf-8")
            self.assertEqual(load_plan(path).canonical_json(), plan_for(document).canonical_json())
            planned["authority"]["ontology_authority"] = True
            path.write_text(json.dumps(planned), encoding="utf-8")
            with self.assertRaisesRegex(ExecutorError, "authority boundary"):
                load_plan(path)

    def test_authoritative_plan_executes_with_consistent_receipt_authority(self) -> None:
        document = manifest(gate("alpha"))
        document["migration_epoch"] = "planner_authoritative"
        document["execution_authority"] = "manifest_planner"
        outcome = self.execute(document, {"test:alpha": result_adapter()})
        self.assertEqual((outcome.status, outcome.exit_code), ("PASS", 0))
        self.assertEqual(outcome.receipt["execution_authority"], "manifest_planner")
        self.assertEqual(outcome.receipt["migration_epoch"], "planner_authoritative")
        self.assertEqual(
            outcome.receipt["feature_switches"],
            {
                "planner_mode": "authoritative",
                "cache_mode": "off",
                "output_mode": "legacy",
                "legacy_fallback": "enabled",
            },
        )
        self.assertTrue(outcome.receipt["authority"]["planner_result_authoritative"])
        self.assertFalse(outcome.receipt["authority"]["legacy_result_authoritative"])

        payload = plan_for(document).to_dict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(load_plan(path).execution_authority, "manifest_planner")

    def test_default_bindings_cover_the_canonical_current_full_plan(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest_path = root / "research_control/design/validation_gate_manifest_v1.yaml"
        from scripts.project_control.classify_project_changes import classify_paths
        from scripts.validation.plan import load_manifest

        document = load_manifest(manifest_path)
        adapters = load_adapters(DEFAULT_BINDINGS, document)
        full = build_plan(
            document,
            classify_paths([]),
            profile="full",
            scopes=("repository",),
        )
        by_id = {gate["gate_id"]: gate for gate in document["gates"]}
        missing = [
            gate_id
            for gate_id in full.selected_gate_ids
            if by_id[gate_id]["adapter"] not in adapters
        ]
        self.assertEqual(missing, [])

        affected = build_plan(
            document,
            classify_paths(
                ("research_control/design/validation_obligation_catalog_v1.yaml",)
            ),
            profile="affected",
            scopes=("repository",),
        )
        missing = [
            gate_id
            for gate_id in affected.selected_gate_ids
            if by_id[gate_id]["adapter"] not in adapters
        ]
        self.assertIn("route_signature_diagnostic", affected.selected_gate_ids)
        self.assertEqual(missing, [])

        drifted = json.loads(json.dumps(document))
        drifted["gates"][0]["description"] = "Drifted gate."
        with self.assertRaisesRegex(ExecutorError, "gate catalog"):
            load_adapters(DEFAULT_BINDINGS, drifted)

        binding_document = json.loads(DEFAULT_BINDINGS.read_text(encoding="utf-8"))
        aggregate = next(
            binding
            for binding in binding_document["bindings"]
            if binding["kind"] == "dependency_aggregate"
        )
        aggregate["child_gate_ids"] = []
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bindings.json"
            path.write_text(json.dumps(binding_document), encoding="utf-8")
            with self.assertRaisesRegex(ExecutorError, "differs from prerequisites"):
                load_adapters(path, document)

    def test_shadow_status_matches_legacy_normalization_corpus(self) -> None:
        corpus = (
            ("blocking", 0, "PASS", 0),
            ("blocking", 3, "FAIL", 1),
            ("advisory", 4, "WARN", 0),
            ("local_only", 5, "WARN", 0),
        )
        for severity, legacy_exit, expected_status, expected_exit in corpus:
            with self.subTest(severity=severity, legacy_exit=legacy_exit):
                document = manifest(gate("legacy", severity=severity))
                outcome = self.execute(
                    document, {"test:legacy": result_adapter(legacy_exit)}
                )
                self.assertEqual((outcome.status, outcome.exit_code), (expected_status, expected_exit))


if __name__ == "__main__":
    unittest.main()
