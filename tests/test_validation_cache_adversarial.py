from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import replace
import os
from pathlib import Path
import threading
import unittest
from unittest import mock

from scripts.validation import cache as cache_module
from scripts.validation.cache import ValidationCache
from tests import test_executor_cache_integration as executor_tests
from tests import test_validation_cache as cache_tests


class _SafeguardAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def run(self, _context):
        from scripts.validation.executor import AdapterResult

        self.calls += 1
        return AdapterResult(
            child_gates=("final_staged_allowlist", "residue_validation")
        )


class ValidationCacheAdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unit = cache_tests.ValidationCacheTests(methodName="runTest")
        self.unit.setUp()
        self.addCleanup(self.unit.tearDown)
        self.integration = executor_tests.ExecutorCacheIntegrationTests(
            methodName="runTest"
        )
        self.integration.setUp()
        self.addCleanup(self.integration.temporary.cleanup)

    def _cache_at(self, name: str, mode: str = "read_write") -> ValidationCache:
        return ValidationCache(
            root=self.unit.work_root / name / "v1",
            repository_root=self.unit.repository_root,
            mode=mode,
            writer_name="validation-cache-test",
            writer_version="1.0.0",
        )

    def _store(self, cache: ValidationCache, key: dict[str, object]):
        sources = self.unit.sources()
        return cache.store(
            key,
            self.unit.result(key, sources),
            source_fingerprint_manifest=sources,
            gate_policy="exact_tree",
            created_at="2026-07-18T00:30:00Z",
        )

    def _lookup(self, cache: ValidationCache, key: dict[str, object]):
        return cache.lookup(
            key,
            gate_policy="exact_tree",
            mandatory_bypass=False,
            freshness_check=lambda: True,
        )

    def test_input_bytes_change_with_preserved_timestamp_misses(self) -> None:
        source = self.unit.work_root / "input.bin"
        source.write_bytes(b"alpha-input")
        timestamp = source.stat().st_mtime_ns
        key = self.unit.key()
        key["tree_hash"] = cache_tests._sha256(source.read_bytes())
        writer = self._cache_at("preserved-mtime")
        self.assertEqual(self._store(writer, key).status, "STORED")

        source.write_bytes(b"omega-input")
        os.utime(source, ns=(timestamp, timestamp))
        changed = deepcopy(key)
        changed["tree_hash"] = cache_tests._sha256(source.read_bytes())

        self.assertEqual(source.stat().st_mtime_ns, timestamp)
        self.assertNotEqual(changed["tree_hash"], key["tree_hash"])
        outcome = self._lookup(self._cache_at("preserved-mtime", "read_only"), changed)
        self.assertEqual((outcome.status, outcome.reason), ("MISS", "absent"))

    def test_every_adversarial_identity_change_misses_or_is_unresolved(self) -> None:
        key = self.unit.key()
        writer = self._cache_at("identity")
        self.assertEqual(self._store(writer, key).status, "STORED")
        mutations = {
            "validator_source": lambda value: value.update(
                implementation_digest=cache_tests._digest("changed-validator-source")
            ),
            "manifest": lambda value: value.update(
                manifest_digest=cache_tests._digest("changed-manifest")
            ),
            "environment": lambda value: value.update(
                environment_fingerprint=cache_tests._digest("changed-environment")
            ),
            "dependency_lock": lambda value: value.update(
                dependency_lock_digest=cache_tests._digest("changed-dependency-lock")
            ),
            "base_ref": lambda value: value.update(
                base_ref={
                    "name": "feature/other",
                    "commit": "git-sha1:" + "a" * 40,
                }
            ),
            "profile": lambda value: value["scope"].update(profile="full"),
            "scope": lambda value: value["scope"].update(
                scope_kind="staged", tree_state="staged"
            ),
            "repository": lambda value: value["scope"].update(
                repository_identity_digest=cache_tests._digest(
                    "temporary-repository"
                )
            ),
            "receipt_schema": lambda value: value["receipt_schema"].update(
                run_receipt_version=2
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                changed = deepcopy(key)
                mutate(changed)
                outcome = self._lookup(
                    self._cache_at("identity", "read_only"),
                    changed,
                )
                self.assertEqual(outcome.status, "MISS")
                self.assertIn(outcome.reason, {"absent", "key_unresolved"})

    def test_corrupt_status_finding_counts_and_receipt_hash_fail_closed(self) -> None:
        corruptions = {
            "status": lambda entry: entry["original_result"].update(status="FAIL"),
            "finding_counts": lambda entry: entry["original_result"].update(
                finding_count=1,
                findings_truncated=False,
            ),
        }
        for label, mutate in corruptions.items():
            with self.subTest(label=label):
                key = self.unit.key()
                writer = self._cache_at(f"corrupt-{label}")
                write = self._store(writer, key)
                assert write.entry_path is not None
                entry = cache_module._strict_json_loads(write.entry_path.read_bytes())
                mutate(entry)
                entry["result_hash"] = cache_tests._sha256(
                    cache_tests._canonical(entry["original_result"])
                )
                write.entry_path.write_bytes(cache_module._entry_bytes(entry))

                reader = self._cache_at(f"corrupt-{label}", "read_only")
                outcome = self._lookup(reader, key)
                self.assertEqual((outcome.status, outcome.reason), ("MISS", "corrupt"))
                self.assertTrue(reader.reads_disabled)

        key = self.unit.key()
        writer = self._cache_at("corrupt-receipt")
        self.assertEqual(self._store(writer, key).status, "STORED")
        original_receipt = self.unit.receipt_path.read_bytes()
        self.unit.receipt_path.write_bytes(b'{"status":"ALTERED"}\n')
        self.addCleanup(self.unit.receipt_path.write_bytes, original_receipt)
        reader = self._cache_at("corrupt-receipt", "read_only")
        outcome = self._lookup(reader, key)
        self.assertEqual((outcome.status, outcome.reason), ("MISS", "corrupt"))
        self.assertTrue(reader.reads_disabled)

    def test_branch_scope_and_tree_state_reuse_are_isolated(self) -> None:
        document = executor_tests._manifest(executor_tests._gate())
        cases = (
            (
                "working_to_staged",
                {"tree_state": "staged", "tree_hash": executor_tests._tree("7")},
                {"scope": "staged"},
            ),
            (
                "branch",
                {},
                {
                    "context_replace": {
                        "base_ref_name": "feature/other",
                        "base_ref_commit": "git-commit-sha1:" + "8" * 40,
                    }
                },
            ),
        )
        for index, (label, context_changes, execution_changes) in enumerate(cases):
            with self.subTest(label=label):
                adapter = executor_tests._CountingAdapter()
                cache = self.integration.cache(suffix=f"-isolation-{index}")
                original_context = self.integration.context(cache)
                self.integration.execute(
                    document,
                    adapter,
                    original_context,
                    f"RUN-isolation-{index}-base",
                )
                changed_context = self.integration.context(cache, **context_changes)
                changed_context = replace(
                    changed_context,
                    **execution_changes.get("context_replace", {}),
                )
                outcome = self.integration.execute(
                    document,
                    adapter,
                    changed_context,
                    f"RUN-isolation-{index}-changed",
                    scope=execution_changes.get("scope", "working"),
                )
                self.assertEqual(adapter.calls, 2)
                self.assertEqual(
                    outcome.receipt["gate_results"][0]["cache_status"],
                    "MISS",
                )

    def test_concurrent_writers_publish_one_complete_entry(self) -> None:
        key = self.unit.key()
        sources = self.unit.sources()
        result = self.unit.result(key, sources)
        barrier = threading.Barrier(8)

        def publish(_index: int):
            cache = self._cache_at("concurrent")
            barrier.wait(timeout=5)
            return cache.store(
                key,
                result,
                source_fingerprint_manifest=sources,
                gate_policy="exact_tree",
                created_at="2026-07-18T00:30:00Z",
            )

        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(publish, range(8)))
        self.assertEqual(sum(item.status == "STORED" for item in outcomes), 1)
        self.assertEqual(sum(item.status == "EXISTS" for item in outcomes), 7)
        reader = self._cache_at("concurrent", "read_only")
        self.assertTrue(self._lookup(reader, key).hit)
        temporary_files = list((self.unit.work_root / "concurrent").rglob("*.tmp"))
        self.assertEqual(temporary_files, [])

    def test_interrupted_atomic_rename_leaves_no_partial_and_retry_succeeds(self) -> None:
        key = self.unit.key()
        cache = self._cache_at("interrupted")
        with mock.patch.object(
            cache_module.os,
            "replace",
            side_effect=OSError("simulated interrupted rename"),
        ):
            failed = self._store(cache, key)
        self.assertEqual(failed.status, "SKIPPED")
        self.assertIn("simulated interrupted rename", failed.reason)
        self.assertEqual(list((self.unit.work_root / "interrupted").rglob("*.tmp")), [])
        self.assertEqual(list((self.unit.work_root / "interrupted").rglob("*.json")), [])

        retry = self._store(cache, key)
        self.assertEqual(retry.status, "STORED")
        self.assertTrue(self._lookup(self._cache_at("interrupted", "read_only"), key).hit)

    def test_final_safeguards_always_execute(self) -> None:
        document = executor_tests._manifest(
            executor_tests._gate("checkpoint_transaction")
        )
        adapter = _SafeguardAdapter()
        cache = self.integration.cache(suffix="-safeguard")
        context = self.integration.context(cache, gate_id="checkpoint_transaction")

        first = self.integration.execute(
            document, adapter, context, "RUN-safeguard-first"
        )
        second = self.integration.execute(
            document, adapter, context, "RUN-safeguard-second"
        )

        self.assertEqual(adapter.calls, 2)
        for outcome in (first, second):
            gate_result = outcome.receipt["gate_results"][0]
            self.assertEqual((outcome.status, gate_result["status"]), ("PASS", "PASS"))
            self.assertEqual(gate_result["cache_status"], "BYPASSED")
            self.assertEqual(
                gate_result["cache_reason"],
                "mandatory_bypass",
            )
            self.assertEqual(
                gate_result["child_gates"],
                ["final_staged_allowlist", "residue_validation"],
            )

    def test_clear_rollback_reruns_uncached_with_normalized_parity(self) -> None:
        document = executor_tests._manifest(executor_tests._gate())
        adapter = executor_tests._CountingAdapter()
        cache = self.integration.cache(suffix="-rollback")
        context = self.integration.context(cache)
        self.integration.execute(document, adapter, context, "RUN-rollback-prime")
        hit = self.integration.execute(document, adapter, context, "RUN-rollback-hit")
        removed = cache.clear()
        self.assertGreaterEqual(removed, 2)

        disabled = self.integration.context(
            self.integration.cache("off", suffix="-rollback")
        )
        uncached = self.integration.execute(
            document,
            adapter,
            disabled,
            "RUN-rollback-uncached",
        )
        hit_result = hit.receipt["gate_results"][0]
        uncached_result = uncached.receipt["gate_results"][0]
        normalized_hit = (
            hit_result["original_status"],
            tuple(hit_result["child_gates"]),
            tuple(hit_result["satisfied_obligations"]),
        )
        normalized_uncached = (
            uncached_result["status"],
            tuple(uncached_result["child_gates"]),
            tuple(uncached_result["satisfied_obligations"]),
        )
        self.assertEqual(normalized_hit, normalized_uncached)
        self.assertEqual(adapter.calls, 2)
        self.assertEqual(uncached_result["cache_status"], "BYPASSED")


if __name__ == "__main__":
    unittest.main()
