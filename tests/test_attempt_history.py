from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "research_control/tasks/RT-20260721-006/artifacts"
VALIDATOR_PATH = ARTIFACT_DIR / "validate_v21_attempt_ledger.py"
RENDERER_PATH = ARTIFACT_DIR / "render_v21_attempt_report.py"
LEDGER_PATH = ARTIFACT_DIR / "v21_research_attempt_ledger.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("v21_attempt_validator_test", VALIDATOR_PATH)
renderer = load_module("v21_attempt_renderer_test", RENDERER_PATH)


class AttemptHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_canonical_ledger_passes(self) -> None:
        metrics = validator.validate_ledger_data(self.ledger)
        self.assertEqual(metrics["event_count"], 8)
        self.assertEqual(metrics["privacy_finding_count"], 0)

    def test_positive_future_revision_is_allowed(self) -> None:
        revised = copy.deepcopy(self.ledger)
        revised["revision"] = 2
        metrics = validator.validate_ledger_data(
            revised, verify_sources=False, verify_head=False
        )
        self.assertEqual(metrics["event_count"], 8)

    def test_unknown_top_level_field_is_rejected(self) -> None:
        extended = copy.deepcopy(self.ledger)
        extended["unexpected_field"] = "not allowed"
        with self.assertRaisesRegex(validator.LedgerValidationError, "ledger fields mismatch"):
            validator.validate_ledger_data(
                extended, verify_sources=False, verify_head=False
            )

    def test_tampered_payload_hash_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.ledger)
        tampered["events"][0]["summary"] += " changed"
        with self.assertRaisesRegex(validator.LedgerValidationError, "payload_sha256 mismatch"):
            validator.validate_ledger_data(tampered, verify_sources=False, verify_head=False)

    def test_finalized_head_prefix_cannot_be_deleted_or_mutated(self) -> None:
        shortened = copy.deepcopy(self.ledger)
        shortened["events"].pop()
        with self.assertRaisesRegex(validator.LedgerValidationError, "deletion"):
            validator.validate_head_prefix(shortened, self.ledger)
        changed = copy.deepcopy(self.ledger)
        changed["events"][0]["summary"] += " changed"
        with self.assertRaisesRegex(validator.LedgerValidationError, "mutation"):
            validator.validate_head_prefix(changed, self.ledger)

    def test_private_field_and_credential_pattern_are_rejected(self) -> None:
        with_field = copy.deepcopy(self.ledger)
        with_field["private_reasoning"] = "not permitted"
        findings = validator.scan_for_private_material(with_field)
        self.assertTrue(any("forbidden field" in item for item in findings))
        with_value = copy.deepcopy(self.ledger)
        with_value["events"][0]["summary"] = "sk-1234567890abcdefghijklmnop"
        findings = validator.scan_for_private_material(with_value)
        self.assertTrue(any("credential-like" in item for item in findings))

    def test_path_traversal_is_rejected(self) -> None:
        traversing = copy.deepcopy(self.ledger)
        traversing["events"][0]["source_refs"][0]["path"] = "../outside.yaml"
        with self.assertRaisesRegex(validator.LedgerValidationError, "path invalid"):
            validator.validate_ledger_data(
                traversing, verify_sources=False, verify_head=False
            )

    def test_process_events_never_become_physics_results(self) -> None:
        promoted = copy.deepcopy(self.ledger)
        promoted["events"][0]["physics_result"] = True
        with self.assertRaisesRegex(validator.LedgerValidationError, "physics_result"):
            validator.validate_ledger_data(promoted, verify_sources=False, verify_head=False)

    def test_report_is_deterministic(self) -> None:
        metrics = validator.validate_ledger_data(self.ledger)
        first = renderer.render(self.ledger, metrics)
        second = renderer.render(copy.deepcopy(self.ledger), copy.deepcopy(metrics))
        self.assertEqual(first, second)
        self.assertIn("Process or review evidence is not physics evidence", first)

    def test_every_missing_event_type_has_explicit_absence(self) -> None:
        metrics = validator.validate_ledger_data(self.ledger)
        self.assertEqual(metrics["event_type_counts"]["abandoned"], 0)
        self.assertEqual(self.ledger["explicit_absences"][0]["event_type"], "abandoned")
        self.assertFalse(self.ledger["explicit_absences"][0]["inference_performed"])


if __name__ == "__main__":
    unittest.main()
