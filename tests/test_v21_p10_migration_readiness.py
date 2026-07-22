from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-003/artifacts/"
    "validate_v21_p10_migration_readiness.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("v21_p10_migration_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load P10 migration audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P10MigrationReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.validation, cls.receipt = cls.module.build_audit()

    def test_audit_completes_with_freeze_disposition(self) -> None:
        self.assertEqual(self.validation["audit_status"], "PASS")
        self.assertEqual(
            self.validation["rollout_disposition"],
            "FREEZE_BROADER_ROLLOUT_REPAIR_REQUIRED",
        )
        self.assertEqual(self.validation["work_item_status"], "completed")

    def test_exact_two_lifecycle_blockers_are_preserved(self) -> None:
        self.assertEqual(self.validation["finding_counts"]["blocker"], 2)
        self.assertEqual(
            [finding["finding_id"] for finding in self.validation["findings"]],
            ["P10-AUDIT-F001", "P10-AUDIT-F002"],
        )

    def test_attempt_hash_chain_passes_while_sealed_receipt_drifts(self) -> None:
        component = next(
            row for row in self.validation["components"] if row["component"] == "P10-T04"
        )
        self.assertEqual(component["hash_chain_status"], "PASS")
        self.assertEqual(component["event_count"], 8)
        self.assertEqual(component["committed_head_prefix_count"], 0)
        self.assertEqual(component["live_head_prefix_count"], 8)

    def test_burden_view_drift_is_limited_to_advancing_live_inputs(self) -> None:
        component = next(
            row for row in self.validation["components"] if row["component"] == "P10-T08"
        )
        self.assertEqual(component["structural_status"], "PASS")
        self.assertEqual(
            component["stale_live_input_paths"],
            [
                "registries/RESEARCH_TASK_REGISTRY.csv",
                "research_control/program_state.yaml",
            ],
        )
        self.assertTrue(component["active_task_advanced"])
        self.assertTrue(component["latest_handoff_advanced"])
        self.assertTrue(component["task_count_advanced"])

    def test_all_declared_historical_samples_resolve(self) -> None:
        samples = self.validation["historical_samples"]
        self.assertEqual(samples["status"], "PASS")
        self.assertEqual(samples["unresolved_sample_count"], 0)
        self.assertEqual(samples["candidate_count"], 7)
        self.assertEqual(samples["attempt_event_count"], 8)
        self.assertEqual(samples["event_store_event_count"], 20)
        self.assertEqual(samples["content_reference_count"], 3)

    def test_source_manifest_is_exact_and_regular(self) -> None:
        self.assertEqual(set(self.validation["source_hashes"]), set(self.module.SOURCE_PATHS))
        for relative, digest in self.validation["source_hashes"].items():
            path = REPO_ROOT / relative
            self.assertTrue(path.is_file())
            self.assertFalse(path.is_symlink())
            self.assertRegex(digest, re.compile(r"^[0-9a-f]{64}$"))

    def test_audit_changes_no_scientific_or_protected_authority(self) -> None:
        self.assertTrue(
            all(value is False for value in self.validation["authority_flags"].values())
        )
        self.assertEqual(
            self.receipt["result_status"], "PASS_AUDIT_FREEZE_BROADER_ROLLOUT"
        )

    def test_dependency_independent_successor_is_p11_t01(self) -> None:
        self.assertEqual(
            self.validation["next_dependency_independent_work_item"], "P11-T01"
        )
        self.assertEqual(self.validation["failed_check_count"], 0)


if __name__ == "__main__":
    unittest.main()
