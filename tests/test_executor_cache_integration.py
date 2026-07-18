from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.validation.cache import ValidationCache
from scripts.validation.executor import (
    AdapterResult,
    ExecutionCacheContext,
    GateCacheEvidence,
    execute_plan,
)
from scripts.validation.plan import build_plan


def _digest(character: str) -> str:
    return f"sha256:{character * 64}"


def _tree(character: str) -> str:
    return f"git-tree-sha1:{character * 40}"


def _gate(
    gate_id: str = "alpha",
    *,
    cache_policy: str = "exact_tree",
    description: str | None = None,
) -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "description": description or f"Synthetic {gate_id} gate.",
        "owner_role": "validator-engineer@0.2.0",
        "adapter": f"test:{gate_id}",
        "command_compatibility": [f"synthetic {gate_id}"],
        "input_globs": ["tests/**"],
        "output_globs": [],
        "global_invariant_justification": None,
        "scopes": ["working", "staged"],
        "severity": "blocking",
        "mutating": False,
        "cost_class": "fast",
        "prerequisites": [],
        "supersedes": [],
        "satisfies_obligations": [gate_id],
        "profiles": ["fast"],
        "path_tags": ["test"],
        "selection": {
            "operator": "all",
            "conditions": [{"condition_id": "always", "kind": "always", "values": []}],
        },
        "timeout_seconds": 5,
        "parallel_group": "test_read_only",
        "cache_policy": cache_policy,
        "receipt_schema": "validation_gate_result_v1",
        "test_shard": "synthetic",
    }


def _manifest(gate: dict[str, object]) -> dict[str, object]:
    return {
        "authority": {
            "benchmark_authority": False,
            "gate_chair_authority": False,
            "ontology_authority": False,
            "operational_validation_only": True,
            "physics_claim_authority": False,
            "proof_authority": False,
            "source_authoritative": False,
        },
        "execution_authority": "legacy",
        "gates": [gate],
        "manifest_id": "validation-gate-manifest-v1",
        "migration_epoch": "shadow_planner",
        "population_status": "populated",
        "schema_id": "validation_gate_manifest_v1",
        "schema_version": 1,
    }


def _plan(document: dict[str, object], scope: str = "working"):
    return build_plan(
        document,
        {
            "changed_paths": ["tests/test_executor_cache_integration.py"],
            "blocked_paths": [],
            "path_family_tags": ["test"],
            "path_family_details": [],
        },
        profile="fast",
        scopes=(scope,),
    )


class _CountingAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def run(self, _context) -> AdapterResult:
        self.calls += 1
        return AdapterResult(child_gates=("child-alpha",))


class ExecutorCacheIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository_root = Path(__file__).resolve().parents[1]
        (self.repository_root / ".local").mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(
            dir=self.repository_root / ".local",
            prefix="executor-cache-test-",
        )
        self.addCleanup(self.temporary.cleanup)
        self.local_root = Path(self.temporary.name)

    def cache(self, mode: str = "read_write", suffix: str = "") -> ValidationCache:
        return ValidationCache(
            root=self.local_root / f"cache{suffix}",
            repository_root=self.repository_root,
            mode=mode,
            writer_name="executor-integration-test",
            writer_version="1",
        )

    def context(
        self,
        cache: ValidationCache,
        *,
        tree_state: str = "working",
        tree_hash: str | None = None,
        implementation: str | None = None,
        environment: str | None = None,
        dependency: str | None = None,
        bypass: str | None = None,
        gate_id: str = "alpha",
        freshness_check=None,
    ) -> ExecutionCacheContext:
        return ExecutionCacheContext(
            cache=cache,
            tree_state=tree_state,
            tree_hash=tree_hash or _tree("1"),
            base_ref_name="HEAD",
            base_ref_commit="git-commit-sha1:" + "2" * 40,
            git_common_dir=self.repository_root / ".git",
            environment_fingerprint=environment or _digest("3"),
            dependency_lock_digest=dependency or _digest("4"),
            gate_evidence={
                gate_id: GateCacheEvidence(
                    implementation_digest=implementation or _digest("5"),
                    source_fingerprint_manifest=(
                        {
                            "input_id": "tests/test_executor_cache_integration.py",
                            "input_type": "file",
                            "digest": _digest("6"),
                        },
                    ),
                )
            },
            freshness_check=freshness_check or (lambda: True),
            mandatory_bypass_reason=bypass,
        )

    def execute(
        self,
        document: dict[str, object],
        adapter: _CountingAdapter,
        context: ExecutionCacheContext,
        run_id: str,
        *,
        scope: str = "working",
    ):
        gate_id = str(document["gates"][0]["gate_id"])  # type: ignore[index]
        return execute_plan(
            _plan(document, scope),
            document,
            {f"test:{gate_id}": adapter},
            receipt_root=self.local_root / "receipts",
            run_id=run_id,
            cache_context=context,
        )

    def test_repeated_exact_tree_uses_original_pass_without_rerunning_adapter(self) -> None:
        document = _manifest(_gate())
        adapter = _CountingAdapter()
        context = self.context(self.cache())

        first = self.execute(document, adapter, context, "RUN-cache-first")
        second = self.execute(document, adapter, context, "RUN-cache-second")

        self.assertEqual(adapter.calls, 1)
        self.assertEqual(first.receipt["gate_results"][0]["cache_status"], "MISS")
        hit = second.receipt["gate_results"][0]
        self.assertEqual(
            (second.status, hit["status"], hit["cache_status"]),
            ("PASS", "CACHE_HIT", "HIT"),
        )
        self.assertEqual(hit["original_status"], "PASS")
        self.assertEqual(hit["child_gates"], ["child-alpha"])
        self.assertEqual(hit["satisfied_obligations"], ["alpha"])
        self.assertGreaterEqual(hit["duration_saved_seconds"], 0)
        self.assertEqual(second.receipt["cache"]["adapter_execution_count"], 0)

    def test_working_evidence_cannot_satisfy_staged_execution(self) -> None:
        document = _manifest(_gate())
        adapter = _CountingAdapter()
        cache = self.cache()

        self.execute(document, adapter, self.context(cache), "RUN-working")
        staged = self.execute(
            document,
            adapter,
            self.context(cache, tree_state="staged", tree_hash=_tree("7")),
            "RUN-staged",
            scope="staged",
        )

        self.assertEqual(adapter.calls, 2)
        self.assertEqual(staged.receipt["gate_results"][0]["cache_status"], "MISS")

    def test_enabled_hit_and_disabled_execution_preserve_child_evidence(self) -> None:
        document = _manifest(_gate())
        enabled_adapter = _CountingAdapter()
        enabled = self.context(self.cache(suffix="-enabled"))
        self.execute(document, enabled_adapter, enabled, "RUN-parity-prime")
        hit = self.execute(document, enabled_adapter, enabled, "RUN-parity-hit")

        disabled_adapter = _CountingAdapter()
        disabled = self.context(self.cache("off", suffix="-disabled"))
        live = self.execute(document, disabled_adapter, disabled, "RUN-parity-disabled")

        hit_result = hit.receipt["gate_results"][0]
        live_result = live.receipt["gate_results"][0]
        self.assertEqual((hit.status, live.status), ("PASS", "PASS"))
        self.assertEqual(hit_result["child_gates"], live_result["child_gates"])
        self.assertEqual(
            hit_result["satisfied_obligations"],
            live_result["satisfied_obligations"],
        )

    def test_manifest_implementation_dependency_and_environment_changes_invalidate(self) -> None:
        changes = (
            ("manifest", {}, {"description": "Changed manifest description."}),
            ("implementation", {"implementation": _digest("7")}, {}),
            ("dependency", {"dependency": _digest("8")}, {}),
            ("environment", {"environment": _digest("9")}, {}),
        )
        for index, (label, context_change, gate_change) in enumerate(changes):
            with self.subTest(label=label):
                cache = self.cache(suffix=f"-{index}")
                adapter = _CountingAdapter()
                original = _manifest(_gate())
                self.execute(original, adapter, self.context(cache), f"RUN-{index}-base")
                changed = _manifest(_gate(**gate_change)) if gate_change else original
                outcome = self.execute(
                    changed,
                    adapter,
                    self.context(cache, **context_change),
                    f"RUN-{index}-changed",
                )
                self.assertEqual(adapter.calls, 2)
                self.assertEqual(outcome.receipt["gate_results"][0]["cache_status"], "MISS")

    def test_cache_off_explicit_bypass_and_fixed_safeguard_preserve_live_result(self) -> None:
        cases = (
            ("off", _manifest(_gate()), self.context(self.cache("off"))),
            ("explicit", _manifest(_gate()), self.context(self.cache(), bypass="parity_audit")),
            (
                "safeguard",
                _manifest(_gate("git_diff_check")),
                self.context(self.cache(), gate_id="git_diff_check"),
            ),
        )
        for index, (label, document, context) in enumerate(cases):
            with self.subTest(label=label):
                adapter = _CountingAdapter()
                first = self.execute(document, adapter, context, f"RUN-bypass-{index}-a")
                second = self.execute(document, adapter, context, f"RUN-bypass-{index}-b")
                self.assertEqual(adapter.calls, 2)
                for outcome in (first, second):
                    result = outcome.receipt["gate_results"][0]
                    self.assertEqual((outcome.status, result["status"]), ("PASS", "PASS"))
                    self.assertEqual(result["cache_status"], "BYPASSED")
                    self.assertEqual(result["child_gates"], ["child-alpha"])

        document = _manifest(_gate())
        stale_adapter = _CountingAdapter()
        stale_context = self.context(
            self.cache(suffix="-stale"),
            freshness_check=lambda: False,
        )
        first = self.execute(document, stale_adapter, stale_context, "RUN-stale-a")
        second = self.execute(document, stale_adapter, stale_context, "RUN-stale-b")
        self.assertEqual(stale_adapter.calls, 2)
        for outcome in (first, second):
            result = outcome.receipt["gate_results"][0]
            self.assertEqual(result["cache_reason"], "snapshot_stale_before_lookup")
            self.assertEqual(
                result["cache_write_reason"],
                "lookup_not_publishable:snapshot_stale_before_lookup",
            )

    def test_corrupt_entry_falls_back_to_live_execution_and_disables_later_reads(self) -> None:
        document = _manifest(_gate())
        adapter = _CountingAdapter()
        cache = self.cache()
        context = self.context(cache)
        first = self.execute(document, adapter, context, "RUN-corrupt-base")
        cache_key = first.receipt["gate_results"][0]["cache_key"]
        entry = cache.objects_root / str(cache_key)[:2] / f"{cache_key}.json"
        entry.write_text("{not-json", encoding="utf-8")

        second = self.execute(document, adapter, context, "RUN-corrupt-fallback")

        self.assertEqual(adapter.calls, 2)
        self.assertEqual(
            (second.status, second.receipt["gate_results"][0]["status"]),
            ("PASS", "PASS"),
        )
        self.assertEqual(second.receipt["gate_results"][0]["cache_reason"], "corrupt")
        self.assertTrue(second.receipt["cache"]["reads_disabled"])
        self.assertTrue(second.receipt["cache"]["diagnostics"])


if __name__ == "__main__":
    unittest.main()
