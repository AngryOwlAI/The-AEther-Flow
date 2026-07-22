from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot.py"
)
SPEC = importlib.util.spec_from_file_location("v21_event_store_pilot", PILOT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class EventStorePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = MODULE.load_fixture()
        cls.bundle = MODULE.build_bundle(cls.fixture)

    @staticmethod
    def failed_names(checks: list[dict[str, object]]) -> set[str]:
        return {str(item["name"]) for item in checks if item["status"] != "PASS"}

    def test_live_pinned_pilot_passes_exactly_bounded_slice(self) -> None:
        receipt = self.bundle["compact_receipt"]
        self.assertEqual("PASS", receipt["validation_status"])
        self.assertEqual(20, receipt["event_count"])
        self.assertEqual(7, receipt["domain_count"])
        self.assertEqual(4, receipt["view_count"])
        self.assertEqual(0, receipt["mismatch_count"])
        self.assertEqual(0, receipt["unmapped_field_count"])

    def test_rebuild_is_byte_deterministic(self) -> None:
        rebuilt = MODULE.build_bundle(self.fixture)
        self.assertEqual(self.bundle["files"], rebuilt["files"])
        self.assertEqual(self.bundle["sqlite_report"], rebuilt["sqlite_report"])

    def test_every_event_uses_full_stable_content_identity(self) -> None:
        for event in self.bundle["events"]:
            expected = "EVT-V21-" + MODULE.sha256_bytes(
                MODULE.canonical_json_bytes(MODULE.event_identity_basis(event))
            )
            self.assertEqual(expected, event["event_id"])
            self.assertEqual(72, len(event["event_id"]))

    def test_chain_gap_and_hash_mutation_fail_closed(self) -> None:
        mutated = copy.deepcopy(self.bundle["events"])
        mutated[5]["sequence"] += 1
        mutated[8]["payload"]["legacy_row"]["status"] = "mutated"
        failed = self.failed_names(MODULE.validate_events(mutated, self.bundle["sources"]))
        self.assertIn("sequence_is_contiguous", failed)
        self.assertIn("event_hash_chain", failed)
        self.assertIn("event_identity", failed)

    def test_unknown_transition_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.bundle["events"])
        mutated[0]["event_type"] = "task_magically_promoted"
        failed = self.failed_names(MODULE.validate_events(mutated, self.bundle["sources"]))
        self.assertIn("known_event_types", failed)

    def test_pinned_source_hash_mutation_is_rejected(self) -> None:
        loader = MODULE.git_source_loader(REPO_ROOT, self.fixture["pinned_commit"])
        target = self.fixture["sources"][0]["path"]

        def mutated_loader(path: str) -> bytes:
            data = loader(path)
            return data + b"# drift\n" if path == target else data

        with self.assertRaisesRegex(MODULE.PilotError, "pinned source hash mismatch"):
            MODULE.build_bundle(self.fixture, mutated_loader)

    def test_task_view_has_exact_selected_source_bytes(self) -> None:
        task_events = sorted(
            (
                event
                for event in self.bundle["events"]
                if event["event_domain"] == "task"
            ),
            key=lambda event: event["payload"]["source_ordinal"],
        )
        expected = (
            task_events[0]["payload"]["legacy_header"]
            + "\n"
            + "\n".join(event["payload"]["legacy_raw_line"] for event in task_events)
            + "\n"
        ).encode("utf-8")
        self.assertEqual(expected, self.bundle["files"][MODULE.OUTPUT_NAMES["task_view"]])

    def test_candidate_view_preserves_complete_document(self) -> None:
        generated = json.loads(
            self.bundle["files"][MODULE.OUTPUT_NAMES["candidate_view"]]
        )
        source = self.bundle["sources"]["candidate_registry"]["document"]
        self.assertEqual(source, generated)
        self.assertEqual(7, generated["record_counts"]["candidates"])
        self.assertEqual(0, generated["record_counts"]["adoption_events"])

    def test_handoff_and_status_views_account_for_every_field(self) -> None:
        accounting = self.bundle["parity_receipt"]["field_accounting"]
        for handoff in accounting["handoff_view"]:
            self.assertEqual([], handoff["unmapped_paths"])
            self.assertTrue(handoff["mapped_paths"])
            self.assertTrue(handoff["excluded_paths"])
        self.assertEqual([], accounting["status_view"]["unmapped_paths"])
        self.assertEqual(
            self.fixture["status_view_fields"],
            accounting["status_view"]["mapped_paths"],
        )

    def test_disposable_sqlite_rebuild_matches_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "pilot.sqlite3"
            report = MODULE.rebuild_sqlite(self.bundle["events"], database)
            self.assertTrue(database.is_file())
            self.assertEqual(20, report["event_count"])
            self.assertEqual(3, report["selected_task_count"])
            self.assertEqual(
                self.bundle["events"][-1]["event_hash"], report["chain_head"]
            )
            self.assertFalse(report["authority"])
            self.assertFalse(report["tracked"])

    def test_decimal_legacy_values_are_string_encoded_and_receipted(self) -> None:
        receipt = self.bundle["parity_receipt"]
        decimal_shape = next(
            shape
            for shape in receipt["unsupported_legacy_shapes"]
            if "binary-float" in shape["shape"]
        )
        converted = decimal_shape["converted_paths"]
        self.assertGreaterEqual(len(converted), 3)
        handoff = next(
            event["payload"]["document"]
            for event in self.bundle["events"]
            if event["subject_id"] == "handoff-0806"
        )
        value = handoff["candidate_lifecycle_metrics"]["audit_to_stress_survival"]["value"]
        self.assertIsInstance(value, str)
        self.assertEqual("0.5714", value)

    def test_all_authority_surfaces_remain_false_or_unchanged(self) -> None:
        for event in self.bundle["events"]:
            self.assertEqual(MODULE.AUTHORITY_FLAGS, event["authority"])
        authority = self.bundle["parity_receipt"]["authority"]
        self.assertTrue(authority["project_control_shadow_pilot_only"])
        for key, value in authority.items():
            if key != "project_control_shadow_pilot_only":
                self.assertFalse(value, key)
        self.assertNotIn("registries/", " ".join(self.bundle["files"]))

    def test_check_detects_generated_view_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            database = root / "pilot.sqlite3"
            MODULE.write_bundle(self.bundle, root, database)
            self.assertEqual([], MODULE.check_bundle(self.bundle, root))
            target = root / MODULE.OUTPUT_NAMES["status_view"]
            target.write_bytes(target.read_bytes() + b"drift\n")
            self.assertEqual([str(target)], MODULE.check_bundle(self.bundle, root))


if __name__ == "__main__":
    unittest.main()
