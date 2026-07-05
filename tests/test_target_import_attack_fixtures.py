from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "research_control/design/target_import_attack_fixture_catalog_v16.md"
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

REQUIRED_BAD_CLASSES = {
    "target_metric_used_as_source_certificate",
    "lorentzian_signature_used_as_certificate_validity",
    "proper_time_used_as_source_readout",
    "detector_calibration_treated_as_source_label",
    "stress_energy_tensor_used_to_prove_matter_semantics",
    "matter_action_used_to_prove_coupling_law",
    "einstein_equations_used_as_upstream_premise",
    "benchmark_fit_used_as_source_evidence",
    "gate_chair_scoped_evidence_used_as_source_law",
    "validator_pass_used_as_proof",
    "generated_wiki_note_used_as_authority",
    "finite_local_model_rendered_as_universal_matter_coupling",
}

REQUIRED_GOOD_CLASSES = {
    "source_transport_certificate_with_no_target_guard",
    "scoped_evidence_precondition_wording",
    "target_import_fail_closed_wording",
    "detector_semantics_blocked_wording",
    "einstein_equations_not_started_wording",
    "benchmark_promotion_protected_wording",
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


def load_snippets(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!-- fixture: (?P<key>[-_a-zA-Z0-9]+) -->\n(?P<body>.*?)\n<!-- /fixture -->",
        flags=re.DOTALL,
    )
    return {match.group("key"): match.group("body").strip() for match in pattern.finditer(text)}


class TargetImportAttackFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog()
        cls.linter = load_linter()
        cls.taxonomy = cls.linter.load_taxonomy(TAXONOMY_PATH)

    def fixture_set(self, mode: str) -> dict:
        for item in self.catalog["fixture_sets"]:
            if item["mode"] == mode:
                path = REPO_ROOT / item["path"]
                return json.loads(path.read_text(encoding="utf-8"))
        raise AssertionError(f"missing fixture set: {mode}")

    def scan(self, snippet: str) -> dict:
        scanned_path = "research_control/current_frontier.md"
        return self.linter.report_dict(
            self.linter.scan_text_map(
                {scanned_path: snippet},
                taxonomy=self.taxonomy,
                reviewed_contexts=[],
                active_handoffs=set(),
            ),
            scanned_paths=[scanned_path],
        )

    def test_catalog_declares_required_classes(self) -> None:
        self.assertEqual(set(self.catalog["required_bad_fixture_classes"]), REQUIRED_BAD_CLASSES)
        self.assertEqual(set(self.catalog["required_good_fixture_classes"]), REQUIRED_GOOD_CLASSES)

    def test_bad_fixture_set_fails_expected_current_linter_classes(self) -> None:
        fixture_set = self.fixture_set("bad")
        snippets = load_snippets(REPO_ROOT / fixture_set["snippet_path"])
        classes = [fixture["fixture_class"] for fixture in fixture_set["fixtures"]]
        self.assertEqual(set(classes), REQUIRED_BAD_CLASSES)
        self.assertEqual(len(classes), len(set(classes)))
        for fixture in fixture_set["fixtures"]:
            snippet = snippets[fixture["snippet_key"]]
            report = self.scan(snippet)
            observed = {finding["class_id"] for finding in report["findings"]}
            expected = set(fixture["expected_current_linter_class_ids"])
            self.assertEqual(report["status"], "FAIL", fixture["fixture_id"])
            self.assertTrue(expected.issubset(observed), fixture["fixture_id"])

    def test_good_fixture_set_passes_current_linter(self) -> None:
        fixture_set = self.fixture_set("good")
        snippets = load_snippets(REPO_ROOT / fixture_set["snippet_path"])
        classes = [fixture["fixture_class"] for fixture in fixture_set["fixtures"]]
        self.assertEqual(set(classes), REQUIRED_GOOD_CLASSES)
        self.assertEqual(len(classes), len(set(classes)))
        for fixture in fixture_set["fixtures"]:
            snippet = snippets[fixture["snippet_key"]]
            report = self.scan(snippet)
            self.assertEqual(report["status"], "PASS", fixture["fixture_id"])
            self.assertEqual(report["finding_count"], 0, fixture["fixture_id"])

    def test_fixture_boundaries_do_not_promote_physics_or_change_validator(self) -> None:
        for mode in ("bad", "good"):
            for fixture in self.fixture_set(mode)["fixtures"]:
                boundary = fixture["boundary"]
                self.assertFalse(boundary["proof_authority"], fixture["fixture_id"])
                self.assertFalse(boundary["physics_promotion_authorized"], fixture["fixture_id"])
                self.assertFalse(boundary["source_law_adopted"], fixture["fixture_id"])
                self.assertFalse(boundary["matter_coupling_derived"], fixture["fixture_id"])
                self.assertFalse(boundary["einstein_equations_derived"], fixture["fixture_id"])
                self.assertFalse(boundary["completed_derivation_claimed"], fixture["fixture_id"])
                self.assertFalse(boundary["validator_behavior_changed"], fixture["fixture_id"])


if __name__ == "__main__":
    unittest.main()

