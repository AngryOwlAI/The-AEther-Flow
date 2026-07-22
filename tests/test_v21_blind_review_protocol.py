from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "research_control/tasks/RT-20260722-004/artifacts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_module("test_v21_blind_builder", ARTIFACT_DIR / "build_blind_review_packet.py")
VALIDATOR = load_module("test_v21_blind_validator", ARTIFACT_DIR / "validate_blind_review_packet.py")


class BlindReviewProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ARTIFACT_DIR / "blind_review_source_fixture.json").read_text(encoding="utf-8"))
        cls.packet, cls.context = BUILDER.build_objects(cls.manifest)

    def validate(self, packet=None, context=None, packet_path=None, context_path=None):
        return VALIDATOR.validate_objects(
            self.manifest,
            packet if packet is not None else copy.deepcopy(self.packet),
            context if context is not None else copy.deepcopy(self.context),
            packet_path=packet_path or ARTIFACT_DIR / "packet.json",
            context_path=context_path or ARTIFACT_DIR / "context.json",
        )

    def test_fixture_passes_all_checks(self):
        report = self.validate()
        self.assertEqual("PASS", report["status"])
        self.assertEqual(0, report["failed_check_count"])
        self.assertEqual(0, report["leak_finding_count"])

    def test_rebuild_is_byte_deterministic(self):
        packet2, context2 = BUILDER.build_objects(copy.deepcopy(self.manifest))
        self.assertEqual(BUILDER.canonical_bytes(self.packet), BUILDER.canonical_bytes(packet2))
        self.assertEqual(BUILDER.canonical_bytes(self.context), BUILDER.canonical_bytes(context2))

    def test_process_metadata_values_are_absent_from_packet(self):
        packet_text = json.dumps(self.packet, sort_keys=True)
        uniquely_identifying_values = (
            self.manifest["process_metadata"]["task_id"],
            self.manifest["process_metadata"]["job_id"],
            self.manifest["process_metadata"]["plan_task_id"],
            self.manifest["process_metadata"]["route_history"],
            self.manifest["process_metadata"]["handoff_id"],
        )
        for value in uniquely_identifying_values:
            self.assertNotIn(value, packet_text)

    def test_context_records_withheld_fields_without_values(self):
        withheld = self.context["reviewer_not_received"]
        self.assertEqual(sorted(self.manifest["process_metadata"]), withheld["process_metadata_field_names"])
        context_text = json.dumps(self.context, sort_keys=True)
        uniquely_identifying_values = (
            self.manifest["process_metadata"]["task_id"],
            self.manifest["process_metadata"]["job_id"],
            self.manifest["process_metadata"]["plan_task_id"],
            self.manifest["process_metadata"]["route_history"],
            self.manifest["process_metadata"]["handoff_id"],
        )
        for value in uniquely_identifying_values:
            self.assertNotIn(value, context_text)

    def test_forbidden_key_is_rejected(self):
        packet = copy.deepcopy(self.packet)
        packet["validator_status"] = "green"
        report = self.validate(packet=packet)
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any(item["kind"] == "forbidden_key" for item in report["findings"]))

    def test_forbidden_workflow_token_is_rejected(self):
        packet = copy.deepcopy(self.packet)
        packet["claim_boundary"][0]["statement"] += " See handoff-9999."
        report = self.validate(packet=packet)
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any(item["kind"] == "handoff_id" for item in report["findings"]))

    def test_missing_assumption_is_rejected(self):
        packet = copy.deepcopy(self.packet)
        packet["assumption_register"].pop()
        report = self.validate(packet=packet)
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any(item["check_id"] == "assumption_register_exact" and item["status"] == "FAIL" for item in report["checks"]))

    def test_source_hash_drift_fails_closed(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["sources"][0]["sha256"] = "0" * 64
        with self.assertRaises(BUILDER.BuildError):
            BUILDER.build_objects(manifest)

    def test_non_verbatim_excerpt_fails_closed(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["scientific_material"][0]["content"] += "\nnot in source"
        with self.assertRaises(BUILDER.BuildError):
            BUILDER.build_objects(manifest)

    def test_packet_and_context_cannot_share_path(self):
        same = ARTIFACT_DIR / "same.json"
        report = self.validate(packet_path=same, context_path=same)
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any(item["check_id"] == "packet_context_path_separation" and item["status"] == "FAIL" for item in report["checks"]))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "same.json"
            with self.assertRaises(BUILDER.BuildError):
                BUILDER.write_objects(ARTIFACT_DIR / "blind_review_source_fixture.json", path, path)

    def test_context_must_not_claim_independence(self):
        context = copy.deepcopy(self.context)
        context["reviewer_independence_claimed"] = True
        report = self.validate(context=context)
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any(item["check_id"] == "no_independence_claim" and item["status"] == "FAIL" for item in report["checks"]))


if __name__ == "__main__":
    unittest.main()
