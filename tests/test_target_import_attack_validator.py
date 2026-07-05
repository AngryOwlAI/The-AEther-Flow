from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
BAD_FIXTURE_SET_PATH = (
    REPO_ROOT / "tests/fixtures/research_control/target_import_attack/bad_target_import_fixtures_v16.json"
)
GOOD_FIXTURE_SET_PATH = (
    REPO_ROOT / "tests/fixtures/research_control/target_import_attack/good_target_import_fixtures_v16.json"
)


def load_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_fixture_set(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_snippets(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!-- fixture: (?P<key>[-_a-zA-Z0-9]+) -->\n(?P<body>.*?)\n<!-- /fixture -->",
        flags=re.DOTALL,
    )
    return {match.group("key"): match.group("body").strip() for match in pattern.finditer(text)}


class TargetImportAttackValidatorIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.linter = load_linter()
        cls.taxonomy = cls.linter.load_taxonomy(TAXONOMY_PATH)

    def scan(self, snippet: str) -> dict:
        scanned_path = "research_control/current_frontier.md"
        findings = self.linter.scan_text_map(
            {scanned_path: snippet},
            taxonomy=self.taxonomy,
            reviewed_contexts=[],
            active_handoffs=set(),
        )
        return self.linter.report_dict(findings, scanned_paths=[scanned_path])

    def test_bad_fixtures_fail_target_import_specific_classes(self) -> None:
        fixture_set = load_fixture_set(BAD_FIXTURE_SET_PATH)
        snippets = load_snippets(REPO_ROOT / fixture_set["snippet_path"])

        for fixture in fixture_set["fixtures"]:
            report = self.scan(snippets[fixture["snippet_key"]])
            observed = {finding["class_id"] for finding in report["findings"]}

            self.assertEqual(report["status"], "FAIL", fixture["fixture_id"])
            self.assertIn(
                fixture["expected_future_target_import_class_id"],
                observed,
                fixture["fixture_id"],
            )

    def test_good_fixtures_remain_source_safe(self) -> None:
        fixture_set = load_fixture_set(GOOD_FIXTURE_SET_PATH)
        snippets = load_snippets(REPO_ROOT / fixture_set["snippet_path"])

        for fixture in fixture_set["fixtures"]:
            report = self.scan(snippets[fixture["snippet_key"]])

            self.assertEqual(report["status"], "PASS", fixture["fixture_id"])
            self.assertEqual(report["finding_count"], 0, fixture["fixture_id"])

    def test_required_validation_outputs_are_covered(self) -> None:
        fixture_set = load_fixture_set(BAD_FIXTURE_SET_PATH)
        classes = {fixture["fixture_class"] for fixture in fixture_set["fixtures"]}

        self.assertIn("target_metric_used_as_source_certificate", classes)
        self.assertIn("proper_time_used_as_source_readout", classes)
        self.assertIn("stress_energy_tensor_used_to_prove_matter_semantics", classes)
        self.assertIn("validator_pass_used_as_proof", classes)
        self.assertIn("finite_local_model_rendered_as_universal_matter_coupling", classes)


if __name__ == "__main__":
    unittest.main()
