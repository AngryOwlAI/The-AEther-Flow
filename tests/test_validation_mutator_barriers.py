from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validation.executor import AdapterResult, ExecutorError, execute_plan
from scripts.validation.plan import build_plan


def gate(
    gate_id: str,
    *,
    mutating: bool,
    output_globs: tuple[str, ...] = (),
    path_tags: tuple[str, ...] = ("test",),
    conditions: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "description": f"Synthetic {gate_id} gate.",
        "owner_role": "validator-engineer@0.2.0",
        "adapter": f"test:{gate_id}",
        "command_compatibility": [f"synthetic {gate_id}"],
        "input_globs": ["tests/**"],
        "output_globs": list(output_globs),
        "global_invariant_justification": None,
        "scopes": ["working"],
        "severity": "blocking",
        "mutating": mutating,
        "cost_class": "fast" if not mutating else "slow",
        "prerequisites": [],
        "supersedes": [],
        "satisfies_obligations": [gate_id],
        "profiles": ["affected"],
        "path_tags": list(path_tags),
        "selection": {
            "operator": "all",
            "conditions": conditions
            or [{"condition_id": "always", "kind": "always", "values": []}],
        },
        "timeout_seconds": 5,
        "parallel_group": "legacy_mutating_serial" if mutating else "test_read_only",
        "cache_policy": "ineligible",
        "receipt_schema": "validation_gate_result_v1",
        "test_shard": "synthetic",
    }


def manifest(*gates: dict[str, object]) -> dict[str, object]:
    return {
        "schema_id": "validation_gate_manifest_v1",
        "schema_version": 1,
        "manifest_id": "validation-gate-manifest-v1",
        "migration_epoch": "shadow_planner",
        "population_status": "populated",
        "execution_authority": "legacy",
        "authority": {
            "benchmark_authority": False,
            "gate_chair_authority": False,
            "ontology_authority": False,
            "operational_validation_only": True,
            "physics_claim_authority": False,
            "proof_authority": False,
            "source_authoritative": False,
        },
        "gates": list(gates),
    }


def plan_for(document: dict[str, object], *, tags: tuple[str, ...] = ("test",)):
    return build_plan(
        document,
        {
            "changed_paths": ["tests/test_validation_mutator_barriers.py"],
            "blocked_paths": [],
            "path_family_tags": list(tags),
            "path_family_details": [],
        },
        profile="affected",
        scopes=("working",),
    )


class FunctionAdapter:
    def __init__(self, function):
        self.function = function

    def run(self, context):
        return self.function(context)


class MutatorBarrierTests(unittest.TestCase):
    def execute(self, document, adapters, *, maximum=3, replan=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        return root, execute_plan(
            plan_for(document),
            document,
            adapters,
            receipt_root=root / "receipts",
            mutation_root=root,
            allowed_mutation_globs=("generated/**", "pdf/**"),
            max_stabilization_passes=maximum,
            replan_if_new_tags=replan,
        )

    def test_unchanged_mutator_stabilizes_in_one_pass_before_read_only(self) -> None:
        events: list[str] = []
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",)),
            gate("memory_core", mutating=False),
        )
        adapters = {
            "test:memory_sync": FunctionAdapter(
                lambda _context: events.append("mutator") or AdapterResult()
            ),
            "test:memory_core": FunctionAdapter(
                lambda _context: events.append("read_only") or AdapterResult()
            ),
        }

        _, outcome = self.execute(document, adapters)

        self.assertEqual((outcome.status, outcome.exit_code), ("PASS", 0))
        self.assertEqual(events, ["mutator", "read_only"])
        self.assertEqual(outcome.receipt["mutator_barrier"]["pass_count"], 1)
        self.assertEqual(outcome.receipt["mutator_barrier"]["status"], "STABLE")

    def test_changed_mutator_requires_a_second_stable_pass(self) -> None:
        calls = 0
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",))
        )

        def synchronize(_context):
            nonlocal calls
            calls += 1
            path = root / "generated" / "state.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            if calls == 1:
                path.write_text("stable\n", encoding="utf-8")
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {"test:memory_sync": FunctionAdapter(synchronize)},
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
                max_stabilization_passes=2,
            )

        self.assertEqual(outcome.status, "PASS")
        self.assertEqual(calls, 2)
        self.assertEqual(outcome.receipt["mutator_barrier"]["pass_count"], 2)

    def test_non_converging_mutator_fails_at_the_bound(self) -> None:
        calls = 0
        read_only_called = False
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",)),
            gate("memory_core", mutating=False),
        )

        def synchronize(_context):
            nonlocal calls
            calls += 1
            path = root / "generated" / "counter.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(calls), encoding="utf-8")
            return AdapterResult()

        def validate(_context):
            nonlocal read_only_called
            read_only_called = True
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {
                    "test:memory_sync": FunctionAdapter(synchronize),
                    "test:memory_core": FunctionAdapter(validate),
                },
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
                max_stabilization_passes=2,
            )

        self.assertEqual((outcome.status, outcome.exit_code), ("FAIL", 1))
        self.assertFalse(read_only_called)
        self.assertEqual(outcome.receipt["mutator_barrier"]["status"], "NON_CONVERGING")
        self.assertEqual(outcome.receipt["mutator_barrier"]["finding_id"], "V19-MUTATOR-NON-CONVERGENCE")

    def test_targeted_pdf_is_followed_by_a_second_memory_sync(self) -> None:
        events: list[str] = []
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",)),
            gate("targeted_pdf_build", mutating=True, output_globs=("pdf/**",)),
        )

        def synchronize(_context):
            events.append("memory_sync")
            pdf = root / "pdf" / "paper.pdf"
            registry = root / "generated" / "pdf-registry.txt"
            if pdf.exists() and not registry.exists():
                registry.parent.mkdir(parents=True, exist_ok=True)
                registry.write_text("paper.pdf\n", encoding="utf-8")
            return AdapterResult()

        def build_pdf(_context):
            events.append("targeted_pdf_build")
            pdf = root / "pdf" / "paper.pdf"
            pdf.parent.mkdir(parents=True, exist_ok=True)
            if not pdf.exists():
                pdf.write_bytes(b"pdf")
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {
                    "test:memory_sync": FunctionAdapter(synchronize),
                    "test:targeted_pdf_build": FunctionAdapter(build_pdf),
                },
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**", "pdf/**"),
                max_stabilization_passes=3,
            )

        self.assertEqual(outcome.status, "PASS")
        self.assertEqual(
            events[:4],
            ["memory_sync", "targeted_pdf_build", "memory_sync", "targeted_pdf_build"],
        )
        self.assertTrue(outcome.receipt["mutator_barrier"]["targeted_pdf_second_sync_observed"])

    def test_disallowed_output_fails_closed_with_exact_path(self) -> None:
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",))
        )

        def escape(_context):
            (root / "outside.txt").write_text("blocked", encoding="utf-8")
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {"test:memory_sync": FunctionAdapter(escape)},
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
            )

        barrier = outcome.receipt["mutator_barrier"]
        self.assertEqual((outcome.status, outcome.exit_code), ("BLOCKED_CONFIGURATION", 2))
        self.assertEqual(barrier["status"], "DISALLOWED_OUTPUT")
        self.assertEqual(barrier["passes"][0]["gate_results"][0]["disallowed_paths"], ["outside.txt"])

    def test_job_allowlist_rejects_an_otherwise_declared_output(self) -> None:
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",))
        )

        def generate(_context):
            path = root / "generated" / "state.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("blocked", encoding="utf-8")
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {"test:memory_sync": FunctionAdapter(generate)},
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("pdf/**",),
            )

        mutation = outcome.receipt["mutator_barrier"]["passes"][0]["gate_results"][0]
        self.assertEqual(outcome.status, "BLOCKED_CONFIGURATION")
        self.assertEqual(mutation["declared_output_globs"], ["generated/**"])
        self.assertEqual(mutation["job_allowed_output_globs"], ["pdf/**"])
        self.assertEqual(mutation["disallowed_paths"], ["generated/state.txt"])

    def test_mutators_are_rejected_when_cache_eligible(self) -> None:
        mutator = gate("memory_sync", mutating=True, output_globs=("generated/**",))
        mutator["cache_policy"] = "exact_tree"
        document = manifest(mutator)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ExecutorError, "may not be cached"):
                execute_plan(
                    plan_for(document),
                    document,
                    {"test:memory_sync": FunctionAdapter(lambda _context: AdapterResult())},
                    receipt_root=root / "receipts",
                    mutation_root=root,
                    allowed_mutation_globs=("generated/**",),
                )

    def test_failed_mutator_records_rollback_metadata_and_blocks_read_only(self) -> None:
        read_only_called = False
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",)),
            gate("memory_core", mutating=False),
        )

        def fail_after_write(_context):
            path = root / "generated" / "partial.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("partial", encoding="utf-8")
            return AdapterResult(exit_code=9)

        def validate(_context):
            nonlocal read_only_called
            read_only_called = True
            return AdapterResult()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {
                    "test:memory_sync": FunctionAdapter(fail_after_write),
                    "test:memory_core": FunctionAdapter(validate),
                },
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
            )

        mutation = outcome.receipt["mutator_barrier"]["passes"][0]["gate_results"][0]
        self.assertEqual((outcome.status, outcome.exit_code), ("FAIL", 1))
        self.assertFalse(read_only_called)
        self.assertTrue(mutation["rollback"]["required"])
        self.assertEqual(mutation["rollback"]["changed_paths"], ["generated/partial.txt"])
        self.assertRegex(mutation["rollback"]["before_tree_hash"], r"^[0-9a-f]{64}$")

    def test_replans_only_when_callback_reports_new_affected_tags(self) -> None:
        replan_calls: list[tuple[str, ...]] = []
        late_read_only_called = False
        conditional = [{
            "condition_id": "generated",
            "kind": "path_tag_any",
            "values": ["generated"],
        }]
        document = manifest(
            gate("memory_sync", mutating=True, output_globs=("generated/**",)),
            gate("late_check", mutating=False, conditions=conditional),
        )

        def synchronize(_context):
            path = root / "generated" / "state.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("stable", encoding="utf-8")
            return AdapterResult()

        def late_check(_context):
            nonlocal late_read_only_called
            late_read_only_called = True
            return AdapterResult()

        def replan(changed_paths):
            replan_calls.append(tuple(changed_paths))
            return plan_for(document, tags=("test", "generated"))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outcome = execute_plan(
                plan_for(document),
                document,
                {
                    "test:memory_sync": FunctionAdapter(synchronize),
                    "test:late_check": FunctionAdapter(late_check),
                },
                receipt_root=root / "receipts",
                mutation_root=root,
                allowed_mutation_globs=("generated/**",),
                max_stabilization_passes=2,
                replan_if_new_tags=replan,
            )

        self.assertEqual(outcome.status, "PASS")
        self.assertEqual(replan_calls, [("generated/state.txt",)])
        self.assertTrue(late_read_only_called)
        self.assertEqual(outcome.receipt["mutator_barrier"]["replan_count"], 1)


if __name__ == "__main__":
    unittest.main()
