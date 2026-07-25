from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260721-005"
    / "artifacts"
    / "validate_v21_candidate_lineage.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_v21_candidate_lineage", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CandidateLineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_live_snapshot_passes_exact_seed_checks(self) -> None:
        validation, receipt = self.validator.validate()

        self.assertEqual(validation["validation_status"], "PASS")
        self.assertEqual(validation["failed_check_count"], 0)
        self.assertEqual(validation["record_counts"]["families"], 5)
        self.assertEqual(validation["record_counts"]["candidates"], 7)
        self.assertEqual(validation["record_counts"]["lineage_edges"], 6)
        self.assertEqual(validation["record_counts"]["candidate_stages"], 22)
        self.assertEqual(validation["record_counts"]["adoption_events"], 0)
        self.assertEqual(validation["record_counts"]["rejection_events"], 0)
        self.assertEqual(receipt["result_status"], "PASS")
        self.assertFalse(receipt["authority_boundary"]["physics_promotion_authorized"])

    def test_historical_registered_source_drift_uses_current_authority(self) -> None:
        seed = json.loads(
            (
                REPO_ROOT
                / "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json"
            ).read_text(encoding="utf-8")
        )
        source_path = "ontology/tex/aether_flow_foundations.tex"
        historical_sha256 = seed["source_hashes"][source_path]

        self.assertNotEqual(
            historical_sha256,
            self.validator.file_sha256(source_path),
        )
        self.assertTrue(
            self.validator.historical_source_binding_matches(
                source_path,
                historical_sha256,
            )
        )

    def test_historical_registered_source_drift_rejects_stale_current_registry(self) -> None:
        seed = json.loads(
            (
                REPO_ROOT
                / "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json"
            ).read_text(encoding="utf-8")
        )
        source_path = "ontology/tex/aether_flow_foundations.tex"
        historical_sha256 = seed["source_hashes"][source_path]
        registry_path = "registries/TEX_SOURCE_REGISTRY.csv"

        with tempfile.TemporaryDirectory() as tempdir:
            repo_root = Path(tempdir)
            for relative in (source_path, registry_path):
                destination = repo_root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO_ROOT / relative, destination)
            current_sha256 = self.validator.file_sha256(source_path)
            registry = repo_root / registry_path
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    current_sha256,
                    "0" * 64,
                    1,
                ),
                encoding="utf-8",
            )

            self.assertFalse(
                self.validator.historical_source_binding_matches(
                    source_path,
                    historical_sha256,
                    repo_root=repo_root,
                )
            )

    def test_changed_identity_content_changes_digest(self) -> None:
        seed = json.loads(
            (
                REPO_ROOT
                / "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json"
            ).read_text(encoding="utf-8")
        )
        contract = self.validator.load_schema_contract()
        candidate = seed["candidates"][0]
        fields = contract["candidate_identity_fields"]
        original = {field: candidate[field] for field in fields}
        changed = dict(original)
        changed["statement_sha256"] = "0" * 64

        self.assertNotEqual(
            self.validator.canonical_sha256(original),
            self.validator.canonical_sha256(changed),
        )

    def test_cycle_detection_rejects_reverse_edge(self) -> None:
        candidate_ids = {"A", "B"}
        acyclic_edges = [{"from_candidate_id": "A", "to_candidate_id": "B"}]
        cyclic_edges = acyclic_edges + [{"from_candidate_id": "B", "to_candidate_id": "A"}]

        self.assertTrue(self.validator.acyclic(candidate_ids, acyclic_edges))
        self.assertFalse(self.validator.acyclic(candidate_ids, cyclic_edges))

    def test_explicit_absence_is_not_observed_history(self) -> None:
        seed = json.loads(
            (
                REPO_ROOT
                / "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual(len(seed["explicit_absences"]), 1)
        self.assertFalse(seed["explicit_absences"][0]["counted_as_observed"])
        graded_stages = [
            stage
            for stage in seed["stage_records"]
            if stage["candidate_id"] == "EQSRC-GRADED-ORBIT-ROOT-V1"
        ]
        self.assertNotIn("stress", {stage["stage_kind"] for stage in graded_stages})


if __name__ == "__main__":
    unittest.main()
