from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "research_control/design/refuter_countermodel_fixture_catalog_v1.md"
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/research_control/refuter_countermodel"
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

REQUIRED_CLASSES = {
    "finite_rr_e_separation_witness",
    "missing_certificate_witness",
    "malformed_certificate_witness",
    "detector_semantics_import_witness",
    "target_metric_import_witness",
    "finite_local_globalization_failure",
    "source_extension_as_derivation_overread",
    "scoped_evidence_as_adoption_overread",
}

REQUIRED_OBSTRUCTION_FIELDS = {
    "obstruction_id",
    "target_claim",
    "target_milestone",
    "failed_premise",
    "minimal_countermodel_available",
    "countermodel_path",
    "countermodel_scope",
    "certificate_gap",
    "source_extension_repair_possible",
    "global_no_go_claim_authorized",
    "future_source_extension_impossibility_authorized",
    "freeze_criteria_status",
    "route_cycle_control",
    "forbidden_conclusions",
}


def load_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_catalog() -> dict:
    text = CATALOG_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("catalog JSON block not found")
    return json.loads(match.group(1))


def load_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RefuterCountermodelFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()
        cls.linter = load_linter()
        cls.taxonomy = cls.linter.load_taxonomy(TAXONOMY_PATH)

    def fixture_paths(self) -> list[Path]:
        return sorted(FIXTURE_ROOT.glob("*.json"))

    def test_catalog_declares_all_required_fixture_classes_once(self) -> None:
        catalog_classes = [item["fixture_class"] for item in self.catalog["fixtures"]]
        self.assertEqual(set(catalog_classes), REQUIRED_CLASSES)
        self.assertEqual(len(catalog_classes), len(set(catalog_classes)))
        self.assertEqual(set(self.catalog["required_fixture_classes"]), REQUIRED_CLASSES)

    def test_catalog_paths_exist_and_match_fixture_ids(self) -> None:
        for item in self.catalog["fixtures"]:
            path = REPO_ROOT / item["path"]
            self.assertTrue(path.is_file(), item["path"])
            fixture = load_fixture(path)
            self.assertEqual(fixture["fixture_id"], item["fixture_id"])
            self.assertEqual(fixture["fixture_class"], item["fixture_class"])

    def test_every_fixture_has_required_refuter_obstruction_record(self) -> None:
        for path in self.fixture_paths():
            fixture = load_fixture(path)
            record = fixture["refuter_obstruction_record"]
            self.assertEqual(set(record), REQUIRED_OBSTRUCTION_FIELDS, path.name)
            self.assertTrue(record["minimal_countermodel_available"], path.name)
            self.assertEqual(record["countermodel_path"], path.relative_to(REPO_ROOT).as_posix())
            self.assertFalse(record["global_no_go_claim_authorized"], path.name)
            self.assertFalse(record["future_source_extension_impossibility_authorized"], path.name)
            self.assertGreaterEqual(len(record["forbidden_conclusions"]), 6, path.name)
            self.assertIn("freeze_decision", record["freeze_criteria_status"])
            self.assertIn("cycle_family", record["route_cycle_control"])

    def test_fixture_boundaries_do_not_promote_physics(self) -> None:
        for path in self.fixture_paths():
            boundary = load_fixture(path)["boundary"]
            self.assertFalse(boundary["proof_authority"], path.name)
            self.assertFalse(boundary["physics_promotion_authorized"], path.name)
            self.assertFalse(boundary["source_law_adopted"], path.name)
            self.assertFalse(boundary["matter_coupling_derived"], path.name)
            self.assertFalse(boundary["einstein_equations_derived"], path.name)
            self.assertFalse(boundary["completed_derivation_claimed"], path.name)

    def test_linter_detects_expected_classes_from_negative_snippets(self) -> None:
        for path in self.fixture_paths():
            fixture = load_fixture(path)
            snippets = fixture["claim_language_linter"]["negative_snippets"]
            expected = set(fixture["claim_language_linter"]["expected_class_ids"])
            report = self.linter.report_dict(
                self.linter.scan_text_map(
                    {
                        "tests/fixtures/claim_language/refuter_countermodel_fixture.md": "\n".join(
                            snippets
                        )
                    },
                    taxonomy=self.taxonomy,
                    reviewed_contexts=[],
                    active_handoffs=set(),
                ),
                scanned_paths=["tests/fixtures/claim_language/refuter_countermodel_fixture.md"],
            )
            observed = {finding["class_id"] for finding in report["findings"]}
            self.assertTrue(expected.issubset(observed), f"{path.name}: {expected - observed}")


if __name__ == "__main__":
    unittest.main()
