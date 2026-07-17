from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock

from scripts.validation.cache import (
    CacheValidationError,
    ValidationCache,
    add_cache_arguments,
    cache_key_for,
    cache_mode_from_namespace,
    main,
    validate_key_material,
)


def _sha256(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def _digest(label: str) -> str:
    return _sha256(label.encode("utf-8"))


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


class ValidationCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository_root = Path.cwd().absolute()
        local = self.repository_root / ".local"
        local.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(
            prefix="validation-cache-test-",
            dir=local,
        )
        self.work_root = Path(self.temporary.name)
        self.cache_root = self.work_root / "cache" / "v1"
        self.receipt_path = self.work_root / "receipts" / "gate-full.json"
        self.receipt_path.parent.mkdir(parents=True)
        self.receipt_path.write_bytes(b'{"status":"PASS","complete":true}\n')

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def key(self, gate_id: str = "gate-one") -> dict[str, object]:
        return {
            "schema_id": "validation_cache_key_v1",
            "schema_version": 1,
            "contract_id": "validation-cache-contract-v1",
            "gate_id": gate_id,
            "scope": {
                "scope_kind": "working",
                "tree_state": "working",
                "profile": "affected",
                "mode": "planner",
                "selection_digest": _digest("selection"),
                "repository_identity_digest": _digest("repository"),
            },
            "tree_hash": _digest("working-tree"),
            "base_ref": {
                "name": "main",
                "commit": f"git-sha1:{hashlib.sha1(b'base').hexdigest()}",
            },
            "implementation_digest": _digest("implementation"),
            "manifest_digest": _digest("manifest"),
            "config_digest": _digest("config"),
            "environment_fingerprint": _digest("environment"),
            "dependency_lock_digest": _digest("dependencies"),
            "receipt_schema": {
                "gate_result_id": "validation_gate_result_v1",
                "gate_result_version": 1,
                "run_receipt_id": "validation_run_receipt_v1",
                "run_receipt_version": 1,
            },
        }

    def sources(self, suffix: str = "") -> list[dict[str, object]]:
        values = [
            {
                "input_id": "scripts/validation/gate.py",
                "input_type": "file",
                "digest": _digest(f"gate{suffix}"),
            },
            {
                "input_id": "synthetic:git-state",
                "input_type": "synthetic",
                "digest": _digest(f"git{suffix}"),
            },
        ]
        return sorted(values, key=lambda item: str(item["input_id"]))

    def receipt(self) -> dict[str, object]:
        relative = self.receipt_path.relative_to(self.repository_root).as_posix()
        return {
            "artifact_id": "GATE-FULL-RECEIPT-001",
            "path": relative,
            "content_hash": _sha256(self.receipt_path.read_bytes()),
            "local_only": True,
            "authoritative": False,
        }

    def result(
        self,
        key: dict[str, object],
        sources: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "schema_id": "validation_gate_result_v1",
            "gate_id": key["gate_id"],
            "severity": "blocking",
            "status": "PASS",
            "cache_status": "MISS",
            "input_fingerprint": _sha256(_canonical(sources)),
            "implementation_fingerprint": key["implementation_digest"],
            "started_at": "2026-07-17T22:00:00Z",
            "finished_at": "2026-07-17T22:00:00Z",
            "duration_ms": 0,
            "error_count": 0,
            "warning_count": 0,
            "finding_count": 0,
            "shown_finding_count": 0,
            "findings_truncated": False,
            "shown_findings": [],
            "full_receipt": self.receipt(),
            "satisfied_obligation_ids": ["OBLIGATION-ONE"],
            "child_gate_ids": [],
            "mutated_paths": [],
            "artifact_refs": [],
        }

    def cache(self, mode: str, **overrides: object) -> ValidationCache:
        arguments: dict[str, object] = {
            "root": self.cache_root,
            "repository_root": self.repository_root,
            "mode": mode,
            "writer_name": "validation-cache-test",
            "writer_version": "1.0.0",
        }
        arguments.update(overrides)
        return ValidationCache(**arguments)  # type: ignore[arg-type]

    def store(
        self,
        cache: ValidationCache,
        key: dict[str, object] | None = None,
        *,
        created_at: str = "2026-07-17T22:00:01Z",
    ):
        selected = key or self.key()
        sources = self.sources()
        return cache.store(
            selected,
            self.result(selected, sources),
            source_fingerprint_manifest=sources,
            gate_policy="exact_tree",
            created_at=created_at,
        )

    def lookup(
        self,
        cache: ValidationCache,
        key: dict[str, object] | None = None,
        *,
        freshness_check=lambda: True,
        gate_policy: str = "exact_tree",
        mandatory_bypass: bool = False,
    ):
        return cache.lookup(
            key or self.key(),
            gate_policy=gate_policy,
            mandatory_bypass=mandatory_bypass,
            freshness_check=freshness_check,
        )

    def test_default_off_and_read_only_never_publish(self) -> None:
        key = self.key()
        sources = self.sources()
        for mode in ("off", "read_only"):
            with self.subTest(mode=mode):
                cache = self.cache(mode)
                write = cache.store(
                    key,
                    self.result(key, sources),
                    source_fingerprint_manifest=sources,
                    gate_policy="exact_tree",
                )
                self.assertEqual(write.status, "SKIPPED")
                self.assertFalse(self.cache_root.exists())
        disabled = self.lookup(self.cache("off"))
        self.assertEqual((disabled.status, disabled.reason), ("DISABLED", "cache_mode_off"))

    def test_store_exact_hit_and_emit_current_hit_result(self) -> None:
        writer = self.cache("read_write")
        write = self.store(writer)
        self.assertEqual(write.status, "STORED")
        self.assertIsNotNone(write.entry_path)
        assert write.entry_path is not None
        entry_bytes = write.entry_path.read_bytes()
        entry = json.loads(entry_bytes)
        self.assertEqual(entry["byte_size"], len(entry_bytes))
        self.assertEqual(entry["cache_key"], cache_key_for(self.key()))
        self.assertEqual(entry["authority"]["operational_validation_only"], True)
        self.assertEqual(entry["authority"]["source_authoritative"], False)

        reader = self.cache("read_only")
        lookup = self.lookup(reader)
        self.assertTrue(lookup.hit)
        self.assertEqual(lookup.result_hash, entry["result_hash"])
        hit = lookup.as_hit_result(
            started_at="2026-07-17T22:01:00Z",
            finished_at="2026-07-17T22:01:00Z",
            duration_ms=0,
        )
        self.assertEqual(hit["status"], "CACHE_HIT")
        self.assertEqual(hit["cache_status"], "HIT")
        self.assertEqual(lookup.original_result["status"], "PASS")  # type: ignore[index]

    def test_every_key_dimension_invalidates_without_fuzzy_fallback(self) -> None:
        writer = self.cache("read_write")
        self.assertEqual(self.store(writer).status, "STORED")
        reader = self.cache("read_only")
        base = self.key()
        mutations = {
            "gate_id": lambda value: value.update(gate_id="gate-two"),
            "scope_kind": lambda value: value["scope"].update(scope_kind="repository"),
            "tree_state": lambda value: value["scope"].update(
                scope_kind="staged", tree_state="staged"
            ),
            "profile": lambda value: value["scope"].update(profile="full"),
            "mode": lambda value: value["scope"].update(mode="shadow"),
            "selection": lambda value: value["scope"].update(
                selection_digest=_digest("selection-two")
            ),
            "repository": lambda value: value["scope"].update(
                repository_identity_digest=_digest("repository-two")
            ),
            "tree_hash": lambda value: value.update(tree_hash=_digest("tree-two")),
            "base_ref": lambda value: value.update(
                base_ref={
                    "name": "origin/main",
                    "commit": f"git-sha1:{hashlib.sha1(b'base-two').hexdigest()}",
                }
            ),
            "implementation": lambda value: value.update(
                implementation_digest=_digest("implementation-two")
            ),
            "manifest": lambda value: value.update(
                manifest_digest=_digest("manifest-two")
            ),
            "config": lambda value: value.update(config_digest=_digest("config-two")),
            "environment": lambda value: value.update(
                environment_fingerprint=_digest("environment-two")
            ),
            "dependencies": lambda value: value.update(
                dependency_lock_digest=_digest("dependencies-two")
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(dimension=name):
                candidate = deepcopy(base)
                mutate(candidate)
                outcome = self.lookup(reader, candidate)
                self.assertEqual((outcome.status, outcome.reason), ("MISS", "absent"))
                self.assertFalse(reader.reads_disabled)

        unresolved = deepcopy(base)
        unresolved["receipt_schema"]["run_receipt_version"] = 2  # type: ignore[index]
        outcome = self.lookup(reader, unresolved)
        self.assertEqual((outcome.status, outcome.reason), ("MISS", "key_unresolved"))
        self.assertFalse(reader.reads_disabled)

    def test_explicit_wrong_key_entries_report_bounded_miss_reasons(self) -> None:
        scenarios = {
            "wrong_tree": lambda value: value.update(tree_hash=_digest("another-tree")),
            "wrong_scope": lambda value: value["scope"].update(profile="full"),
            "wrong_implementation": lambda value: value.update(
                implementation_digest=_digest("another-implementation")
            ),
        }
        for index, (reason, mutate) in enumerate(scenarios.items()):
            with self.subTest(reason=reason):
                root = self.work_root / f"mismatch-{index}" / "v1"
                writer = ValidationCache(
                    root=root,
                    repository_root=self.repository_root,
                    mode="read_write",
                    writer_name="validation-cache-test",
                    writer_version="1.0.0",
                )
                stored = self.store(writer)
                assert stored.entry_path is not None
                candidate = self.key()
                mutate(candidate)
                candidate_key = cache_key_for(candidate)
                offered = (
                    root
                    / "objects"
                    / candidate_key[:2]
                    / f"{candidate_key}.json"
                )
                offered.parent.mkdir(parents=True)
                offered.write_bytes(stored.entry_path.read_bytes())
                reader = ValidationCache(
                    root=root,
                    repository_root=self.repository_root,
                    mode="read_only",
                    writer_name="validation-cache-test",
                    writer_version="1.0.0",
                )
                lookup = self.lookup(reader, candidate)
                self.assertEqual((lookup.status, lookup.reason), ("MISS", reason))
                self.assertTrue(reader.reads_disabled)

    def test_unknown_or_noncanonical_key_material_is_rejected(self) -> None:
        key = self.key()
        key["unknown"] = True
        with self.assertRaises(CacheValidationError):
            validate_key_material(key)
        key = self.key()
        key["scope"]["selection_digest"] = "not-qualified"  # type: ignore[index]
        with self.assertRaises(CacheValidationError):
            cache_key_for(key)

    def test_policy_bypass_and_freshness_checks_prevent_hits(self) -> None:
        writer = self.cache("read_write")
        self.assertEqual(self.store(writer).status, "STORED")
        reader = self.cache("read_only")
        ineligible = self.lookup(reader, gate_policy="ineligible")
        self.assertEqual(ineligible.reason, "gate_policy_ineligible")
        bypass = self.lookup(reader, mandatory_bypass=True)
        self.assertEqual(bypass.reason, "mandatory_bypass")

        before_calls = 0

        def stale_before() -> bool:
            nonlocal before_calls
            before_calls += 1
            return False

        self.assertEqual(
            self.lookup(reader, freshness_check=stale_before).reason,
            "snapshot_stale_before_lookup",
        )
        self.assertEqual(before_calls, 1)

        calls = 0

        def stale_after() -> bool:
            nonlocal calls
            calls += 1
            return calls == 1

        self.assertEqual(
            self.lookup(reader, freshness_check=stale_after).reason,
            "snapshot_stale_before_accept",
        )
        self.assertEqual(calls, 2)

    def test_ineligible_and_nonclean_results_are_never_stored(self) -> None:
        key = self.key()
        sources = self.sources()
        cache = self.cache("read_write")
        self.assertEqual(
            cache.store(
                key,
                self.result(key, sources),
                source_fingerprint_manifest=sources,
                gate_policy="ineligible",
            ).reason,
            "gate_policy_ineligible",
        )
        variants = []
        failed = self.result(key, sources)
        failed["status"] = "FAIL"
        variants.append(failed)
        warned = self.result(key, sources)
        warned["warning_count"] = 1
        variants.append(warned)
        prior_hit = self.result(key, sources)
        prior_hit["status"] = "CACHE_HIT"
        prior_hit["cache_status"] = "HIT"
        variants.append(prior_hit)
        mutating = self.result(key, sources)
        mutating["mutated_paths"] = ["tracked.txt"]
        variants.append(mutating)
        truncated = self.result(key, sources)
        truncated["finding_count"] = 1
        truncated["findings_truncated"] = True
        variants.append(truncated)
        for result in variants:
            with self.subTest(status=result["status"], mutation=result["mutated_paths"]):
                outcome = cache.store(
                    key,
                    result,
                    source_fingerprint_manifest=sources,
                    gate_policy="exact_tree",
                )
                self.assertEqual(outcome.status, "SKIPPED")
                self.assertTrue(outcome.reason.startswith("invalid:"))
        self.assertFalse(self.cache_root.exists())

    def test_corrupt_entry_disables_reads_for_invocation(self) -> None:
        writer = self.cache("read_write")
        write = self.store(writer)
        assert write.entry_path is not None
        write.entry_path.write_bytes(b'{"schema_id":"partial"')
        reader = self.cache("read_only")
        first = self.lookup(reader)
        self.assertEqual((first.status, first.reason), ("MISS", "corrupt"))
        self.assertTrue(reader.reads_disabled)
        second = self.lookup(reader)
        self.assertEqual(
            (second.status, second.reason),
            ("DISABLED", "reads_disabled_after_corruption"),
        )
        self.assertEqual(len(reader.diagnostics), 1)

    def test_unpublished_partial_temporary_file_is_not_a_hit(self) -> None:
        key = self.key()
        cache_key = cache_key_for(key)
        shard = self.cache_root / "objects" / cache_key[:2]
        shard.mkdir(parents=True)
        (shard / f".{cache_key}.json.partial.tmp").write_bytes(b'{"partial":')
        reader = self.cache("read_only")
        outcome = self.lookup(reader, key)
        self.assertEqual((outcome.status, outcome.reason), ("MISS", "absent"))
        self.assertFalse(reader.reads_disabled)

    def test_altered_receipt_and_source_hash_fail_closed(self) -> None:
        writer = self.cache("read_write")
        write = self.store(writer)
        self.receipt_path.write_bytes(b'{"status":"ALTERED"}\n')
        altered_receipt = self.lookup(self.cache("read_only"))
        self.assertEqual(altered_receipt.reason, "corrupt")

        self.receipt_path.write_bytes(b'{"status":"PASS","complete":true}\n')
        other_root = self.work_root / "source-corrupt" / "v1"
        other = ValidationCache(
            root=other_root,
            repository_root=self.repository_root,
            mode="read_write",
            writer_name="validation-cache-test",
            writer_version="1.0.0",
        )
        other_write = self.store(other)
        assert other_write.entry_path is not None
        entry = json.loads(other_write.entry_path.read_text(encoding="utf-8"))
        entry["source_fingerprint_hash"] = _digest("wrong")
        other_write.entry_path.write_text(
            json.dumps(entry, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        altered_source = ValidationCache(
            root=other_root,
            repository_root=self.repository_root,
            mode="read_only",
            writer_name="validation-cache-test",
            writer_version="1.0.0",
        )
        self.assertEqual(self.lookup(altered_source).reason, "corrupt")

    def test_symlinked_entry_and_parent_are_rejected(self) -> None:
        writer = self.cache("read_write")
        write = self.store(writer)
        assert write.entry_path is not None
        write.entry_path.unlink()
        write.entry_path.symlink_to(self.receipt_path)
        reader = self.cache("read_only")
        self.assertEqual(self.lookup(reader).reason, "corrupt")

        real_parent = self.work_root / "real-parent"
        real_parent.mkdir()
        linked_parent = self.work_root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        unsafe = ValidationCache(
            root=linked_parent / "v1",
            repository_root=self.repository_root,
            mode="read_write",
            writer_name="validation-cache-test",
            writer_version="1.0.0",
        )
        self.assertEqual(self.store(unsafe).status, "SKIPPED")
        self.assertIn("real directory", self.store(unsafe).reason)

    def test_concurrent_identical_writers_publish_no_partial_entry(self) -> None:
        cache = self.cache("read_write")
        barrier = threading.Barrier(8)

        def publish() -> str:
            barrier.wait()
            return self.store(cache).status

        with ThreadPoolExecutor(max_workers=8) as pool:
            statuses = list(pool.map(lambda _: publish(), range(8)))
        self.assertEqual(statuses.count("STORED"), 1)
        self.assertEqual(statuses.count("EXISTS"), 7)
        self.assertFalse(cache.reads_disabled)
        self.assertTrue(self.lookup(self.cache("read_only")).hit)
        temporary_files = list(self.cache_root.rglob("*.tmp"))
        self.assertEqual(temporary_files, [])

    def test_concurrent_readers_observe_only_absent_or_complete_hit(self) -> None:
        barrier = threading.Barrier(9)

        def publish() -> str:
            barrier.wait()
            return self.store(self.cache("read_write")).status

        def read_repeatedly() -> list[str]:
            reader = self.cache("read_only")
            barrier.wait()
            return [self.lookup(reader).reason for _ in range(32)]

        with ThreadPoolExecutor(max_workers=9) as pool:
            writer_future = pool.submit(publish)
            reader_futures = [pool.submit(read_repeatedly) for _ in range(8)]
            writer_status = writer_future.result()
            observed = [
                reason
                for future in reader_futures
                for reason in future.result()
            ]
        self.assertEqual(writer_status, "STORED")
        self.assertTrue(set(observed) <= {"absent", "exact_match"})
        self.assertNotIn("corrupt", observed)
        self.assertTrue(self.lookup(self.cache("read_only")).hit)

    def test_different_bytes_at_same_key_are_treated_as_collision(self) -> None:
        cache = self.cache("read_write")
        self.assertEqual(
            self.store(cache, created_at="2026-07-17T22:00:01Z").status,
            "STORED",
        )
        collision = self.store(cache, created_at="2026-07-17T22:00:02Z")
        self.assertEqual((collision.status, collision.reason), ("REJECTED", "collision"))
        self.assertTrue(cache.reads_disabled)

    def test_capacity_eviction_is_oldest_first_with_key_tiebreak(self) -> None:
        cache = self.cache("read_write", max_entries=2)
        keys = [self.key(f"gate-{number}") for number in (1, 2, 3)]
        for index, key in enumerate(keys):
            outcome = self.store(
                cache,
                key,
                created_at=f"2026-07-17T22:00:0{index + 1}Z",
            )
            self.assertEqual(outcome.status, "STORED")
        reader = self.cache("read_only")
        self.assertEqual(self.lookup(reader, keys[0]).reason, "absent")
        self.assertTrue(self.lookup(reader, keys[1]).hit)
        self.assertTrue(self.lookup(reader, keys[2]).hit)
        inspection = reader.inspect()
        self.assertEqual((inspection.entry_count, inspection.valid_count), (2, 2))

    def test_equal_age_eviction_uses_ascending_cache_key_tiebreak(self) -> None:
        cache = self.cache("read_write", max_entries=1)
        keys = [self.key("gate-tie-a"), self.key("gate-tie-b")]
        timestamp = "2026-07-17T22:00:01Z"
        self.store(cache, keys[0], created_at=timestamp)
        self.store(cache, keys[1], created_at=timestamp)
        ordered = sorted((cache_key_for(key), key) for key in keys)
        reader = self.cache("read_only")
        self.assertEqual(self.lookup(reader, ordered[0][1]).reason, "absent")
        self.assertTrue(self.lookup(reader, ordered[1][1]).hit)

    def test_age_and_aggregate_limits_skip_unretainable_write(self) -> None:
        aged = self.cache(
            "read_write",
            max_age_seconds=5,
            now=lambda: "2026-07-17T22:00:10Z",
        )
        outcome = self.store(aged, created_at="2026-07-17T22:00:00Z")
        self.assertEqual((outcome.status, outcome.reason), ("SKIPPED", "evicted_by_policy"))
        self.assertEqual(aged.inspect().entry_count, 0)

        tiny = ValidationCache(
            root=self.work_root / "tiny" / "v1",
            repository_root=self.repository_root,
            mode="read_write",
            writer_name="validation-cache-test",
            writer_version="1.0.0",
            max_total_bytes=1,
        )
        outcome = self.store(tiny)
        self.assertEqual((outcome.status, outcome.reason), ("SKIPPED", "evicted_by_policy"))

    def test_inspection_is_read_only_and_clear_removes_local_state(self) -> None:
        cache = self.cache("read_write")
        write = self.store(cache)
        assert write.entry_path is not None
        before = write.entry_path.read_bytes()
        before_mtime = write.entry_path.stat().st_mtime_ns
        inspection = cache.inspect()
        self.assertEqual((inspection.entry_count, inspection.invalid_count), (1, 0))
        self.assertEqual(write.entry_path.read_bytes(), before)
        self.assertEqual(write.entry_path.stat().st_mtime_ns, before_mtime)
        removed = cache.clear()
        self.assertGreaterEqual(removed, 2)
        self.assertEqual(cache.inspect().entry_count, 0)

    def test_clear_refuses_symlinked_local_state(self) -> None:
        cache = self.cache("read_write")
        write = self.store(cache)
        assert write.entry_path is not None
        write.entry_path.unlink()
        write.entry_path.symlink_to(self.receipt_path)
        with self.assertRaises(CacheValidationError):
            cache.clear()

    def test_cli_control_surface_defaults_off_and_supports_override(self) -> None:
        parser = argparse.ArgumentParser()
        add_cache_arguments(parser)
        default = parser.parse_args([])
        self.assertEqual(cache_mode_from_namespace(default), "off")
        writable = parser.parse_args(["--cache-mode", "read_write"])
        self.assertEqual(cache_mode_from_namespace(writable), "read_write")
        disabled = parser.parse_args(["--cache-mode", "read_write", "--no-cache"])
        self.assertEqual(cache_mode_from_namespace(disabled), "off")
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["--clear-cache", "--inspect-cache"])

    def test_cli_inspection_and_clear_are_bounded(self) -> None:
        cache = self.cache("read_write")
        self.assertEqual(self.store(cache).status, "STORED")
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            exit_code = main(
                [
                    "--cache-root",
                    str(self.cache_root),
                    "--cache-mode",
                    "read_only",
                    "--inspect-cache",
                ]
            )
        self.assertEqual(exit_code, 0)
        inspected = json.loads(output.getvalue())
        self.assertEqual(inspected["schema_id"], "validation_cache_inspection_v1")
        self.assertEqual(inspected["entry_count"], 1)

        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            exit_code = main(
                ["--cache-root", str(self.cache_root), "--clear-cache"]
            )
        self.assertEqual(exit_code, 0)
        cleared = json.loads(output.getvalue())
        self.assertEqual(cleared["schema_id"], "validation_cache_clear_v1")
        self.assertGreaterEqual(cleared["removed_file_count"], 2)

    def test_cli_rejects_cache_root_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            output = io.StringIO()
            with mock.patch("sys.stdout", output):
                exit_code = main(["--cache-root", outside, "--inspect-cache"])
        self.assertEqual(exit_code, 2)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "BLOCKED_CONFIGURATION")

    def test_hit_result_rejects_inconsistent_current_timing(self) -> None:
        cache = self.cache("read_write")
        self.assertEqual(self.store(cache).status, "STORED")
        hit = self.lookup(self.cache("read_only"))
        with self.assertRaises(CacheValidationError):
            hit.as_hit_result(
                started_at="2026-07-17T22:01:00Z",
                finished_at="2026-07-17T22:01:01Z",
                duration_ms=0,
            )


if __name__ == "__main__":
    unittest.main()
