from __future__ import annotations

import csv
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = (
    REPO_ROOT / "research_control" / "tasks" / "RT-20260721-009" / "artifacts"
)
if str(ARTIFACT_DIR) not in sys.path:
    sys.path.insert(0, str(ARTIFACT_DIR))

import v21_current_burden_status_renderer as renderer  # noqa: E402
import validate_v21_current_burden_status as validator  # noqa: E402


HANDOFF_PATH = f"research_control/handoffs/{renderer.load_yaml_mapping(REPO_ROOT, renderer.PROGRAM_STATE_PATH)['latest_handoff_id']}.yaml"
SOURCE_PATHS = (
    renderer.DEFINITIONS_PATH,
    renderer.LEDGER_PATH,
    renderer.PROGRAM_STATE_PATH,
    renderer.TASK_REGISTRY_PATH,
    renderer.BURDEN_MAP_PATH,
    HANDOFF_PATH,
)
SOURCE_COMMIT = "a" * 40


class CurrentBurdenStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.tempdir.name)
        for rel_path in SOURCE_PATHS:
            destination = self.repo_root / rel_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / rel_path, destination)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def build(self):
        return renderer.build_bundle(self.repo_root, source_commit=SOURCE_COMMIT)

    def mutate_ledger(self, mutator) -> None:
        path = self.repo_root / renderer.LEDGER_PATH
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        mutator(rows)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_baseline_snapshot_has_all_definitions_and_burdens(self) -> None:
        snapshot, _markdown, _receipt = self.build()
        self.assertEqual(snapshot["definition_count"], 10)
        self.assertEqual(snapshot["burden_count"], 14)
        self.assertFalse(snapshot["authority"]["generated_status_is_independent_authority"])

    def test_bundle_rebuild_is_deterministic(self) -> None:
        self.assertEqual(self.build(), self.build())

    def test_duplicate_burden_identity_fails_closed(self) -> None:
        self.mutate_ledger(
            lambda rows: rows[1].__setitem__("burden_id", rows[0]["burden_id"])
        )
        with self.assertRaisesRegex(renderer.BurdenStatusError, "duplicate burden_id"):
            self.build()

    def test_unmapped_milestone_fails_closed(self) -> None:
        self.mutate_ledger(
            lambda rows: rows[0].__setitem__("milestone", "not_a_defined_milestone")
        )
        with self.assertRaisesRegex(renderer.BurdenStatusError, "unmapped milestone"):
            self.build()

    def test_blank_required_ledger_value_fails_closed(self) -> None:
        self.mutate_ledger(lambda rows: rows[0].__setitem__("accept_criteria", ""))
        with self.assertRaisesRegex(renderer.BurdenStatusError, "blank fields"):
            self.build()

    def test_program_state_handoff_contradiction_fails_closed(self) -> None:
        path = self.repo_root / HANDOFF_PATH
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"^next_action:.*$",
            'next_action: "intentionally contradictory fixture"',
            text,
            count=1,
            flags=re.MULTILINE,
        )
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(renderer.BurdenStatusError, "next actions disagree"):
            self.build()

    def test_stable_definition_status_field_fails_closed(self) -> None:
        path = self.repo_root / renderer.DEFINITIONS_PATH
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            '    required_object: "selected primitive source arena and unresolved source-order or evolution slot"',
            '    current_status: "stale fixture"\n'
            '    required_object: "selected primitive source arena and unresolved source-order or evolution slot"',
            1,
        )
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(renderer.BurdenStatusError, "mutable status fields"):
            self.build()

    def test_definition_dependency_cycle_fails_closed(self) -> None:
        path = self.repo_root / renderer.DEFINITIONS_PATH
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "    depends_on: []",
            '    depends_on:\n      - "benchmark_promotion"',
            1,
        )
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(renderer.BurdenStatusError, "dependency cycle"):
            self.build()

    def test_recorded_source_hash_freshness_rejects_mutation(self) -> None:
        _snapshot, _markdown, receipt = self.build()
        validator.verify_recorded_source_hashes(self.repo_root, receipt)
        self.mutate_ledger(
            lambda rows: rows[0].__setitem__(
                "current_status", rows[0]["current_status"] + " stale"
            )
        )
        with self.assertRaisesRegex(validator.ValidationError, "stale recorded source hash"):
            validator.verify_recorded_source_hashes(self.repo_root, receipt)

    def test_generated_markdown_is_non_authoritative_and_complete(self) -> None:
        snapshot, markdown, _receipt = self.build()
        self.assertIn("authority: generated_noncanonical", markdown)
        for definition in snapshot["definitions"]:
            for row in definition["current_rows"]:
                self.assertEqual(
                    markdown.count(f"#### `{row['burden_id']}` generated detail"), 1
                )

    def test_tracked_output_drift_is_detected(self) -> None:
        _snapshot, markdown, receipt = self.build()
        renderer.write_outputs(self.repo_root, markdown, receipt)
        output = self.repo_root / renderer.OUTPUT_PATH
        output.write_text(markdown + "stale fixture\n", encoding="utf-8")
        self.assertEqual(
            renderer.drift_paths(self.repo_root, markdown, receipt),
            [renderer.OUTPUT_PATH],
        )


if __name__ == "__main__":
    unittest.main()
