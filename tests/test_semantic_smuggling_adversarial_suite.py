from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MUTATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_mutator.py"
)


def load_mutator():
    spec = importlib.util.spec_from_file_location("p11_t04_semantic_smuggling_mutator", MUTATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SemanticSmugglingAdversarialSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mutator = load_mutator()
        cls.catalog = cls.mutator.build_catalog()
        cls.report = cls.mutator.build_comparison(cls.catalog)

    def test_catalog_covers_every_required_attack_class(self) -> None:
        self.assertEqual(
            set(self.catalog["attack_classes"]), set(self.mutator.ATTACK_CLASSES)
        )
        observed = {
            fixture["attack_class"]
            for fixture in self.catalog["fixtures"]
            if fixture["label"] == "attack"
        }
        self.assertEqual(observed, set(self.mutator.ATTACK_CLASSES))

    def test_catalog_has_attack_and_benign_controls(self) -> None:
        self.assertGreaterEqual(self.catalog["attack_fixture_count"], 12)
        self.assertGreaterEqual(self.catalog["benign_fixture_count"], 6)
        self.assertEqual(
            len(self.catalog["fixtures"]),
            self.catalog["attack_fixture_count"] + self.catalog["benign_fixture_count"],
        )

    def test_corpus_generation_is_byte_deterministic(self) -> None:
        first = self.mutator.generated_outputs()
        second = self.mutator.generated_outputs()
        self.assertEqual(first, second)
        self.assertEqual(
            self.catalog["corpus_sha256"],
            self.mutator.sha256_bytes(
                self.mutator.canonical_bytes(list(self.mutator.FIXTURES))
            ),
        )

    def test_all_attacks_are_detected_by_bounded_semantic_probe(self) -> None:
        attack_rows = [row for row in self.report["rows"] if row["label"] == "attack"]
        self.assertTrue(attack_rows)
        for row in attack_rows:
            self.assertTrue(row["semantic_detected"], row["fixture_id"])
            self.assertFalse(row["missing_expected_semantic_rule_ids"], row["fixture_id"])
        self.assertEqual(self.report["probe"]["metrics"]["false_negative"], 0)

    def test_benign_controls_have_no_semantic_false_positive(self) -> None:
        benign_rows = [row for row in self.report["rows"] if row["label"] == "benign"]
        self.assertTrue(benign_rows)
        for row in benign_rows:
            self.assertFalse(row["semantic_detected"], row["fixture_id"])
        self.assertEqual(self.report["probe"]["metrics"]["false_positive"], 0)

    def test_direct_import_controls_fail_current_lexical_linter(self) -> None:
        ids = {
            fixture["fixture_id"]
            for fixture in self.catalog["fixtures"]
            if fixture["direct_import_control"]
        }
        rows = {row["fixture_id"]: row for row in self.report["rows"]}
        self.assertTrue(ids)
        for fixture_id in ids:
            self.assertTrue(rows[fixture_id]["lexical_detected"], fixture_id)

    def test_comparison_demonstrates_lexical_blind_spot_without_policy_change(self) -> None:
        self.assertGreaterEqual(
            self.report["lexical_linter"]["metrics"]["false_negative"], 1
        )
        self.assertFalse(self.report["production_linter_changed"])
        self.assertEqual(self.report["status"], "PASS")

    def test_misleading_certificate_and_prompt_attacks_are_explicit(self) -> None:
        rows = {row["fixture_id"]: row for row in self.report["rows"]}
        self.assertIn(
            "misleading_no_target_certificate",
            rows["ATT-MISLEADING-CERTIFICATE-001"]["semantic_rule_ids"],
        )
        self.assertIn(
            "prompt_level_proper_time_import",
            rows["ATT-PROMPT-WORLDLINE-READOUT-001"]["semantic_rule_ids"],
        )
        self.assertIn(
            "prompt_level_benchmark_import",
            rows["ATT-PROMPT-REFERENCE-SUITE-001"]["semantic_rule_ids"],
        )

    def test_boundaries_and_limitations_remain_non_promotional(self) -> None:
        for fixture in self.catalog["fixtures"]:
            self.assertTrue(all(value is False for value in fixture["boundary"].values()))
        self.assertTrue(all(value is False for value in self.report["boundary"].values()))
        limitations = " ".join(self.report["limitations"]).casefold()
        self.assertIn("does not establish semantic completeness", limitations)
        self.assertIn("blind", limitations)
        self.assertIn("human", limitations)

    def test_written_outputs_match_deterministic_rebuild(self) -> None:
        result = self.mutator.check_outputs()
        self.assertEqual(result["status"], "PASS", json.dumps(result, sort_keys=True))
        self.assertEqual(result["drift_paths"], [])


if __name__ == "__main__":
    unittest.main()
