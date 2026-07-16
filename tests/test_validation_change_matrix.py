from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest import mock
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests/fixtures/validation_plans/change_matrix_v1.json"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
MATRIX_PATH = ROOT / "research_control/design/validation_change_matrix_v1.md"

from scripts.project_control import classify_project_changes as classifier
from scripts.validation.plan import load_manifest, render_explanation
from scripts.validation.profiles import resolve_profile


REQUIRED_CASE_IDS = {
    "pure_python_validator",
    "research_control_yaml",
    "registered_markdown",
    "tex_pdf_required",
    "tex_without_pdf",
    "html_spec_with_mermaid",
    "memory_code",
    "dependency_graph_input",
    "task_index_input",
    "scientific_checker",
    "local_retrieval_only",
    "ci_orchestration",
    "deletion",
    "rename",
    "mixed_change",
    "unknown_governed_path",
    "irrelevant_local_retrieval",
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class ValidationChangeMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.manifest = load_manifest(MANIFEST_PATH)
        cls.gates = {gate["gate_id"]: gate for gate in cls.manifest["gates"]}

    def test_fixture_schema_and_case_coverage(self) -> None:
        self.assertEqual(self.fixture["schema_id"], "validation_change_matrix_fixture_v1")
        self.assertEqual(self.fixture["plan_task_id"], "P5-T08")
        self.assertEqual(self.fixture["migration_epoch"], "shadow_planner")
        self.assertEqual(self.fixture["execution_authority"], "legacy")
        case_ids = [case["case_id"] for case in self.fixture["cases"]]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertEqual(set(case_ids), REQUIRED_CASE_IDS)

    def _evaluate(self, case: dict[str, object]):
        paths = list(case["paths"])
        classification = classifier.classify_paths(paths)
        resolution = resolve_profile(
            self.manifest,
            classification,
            requested_profile=str(case["requested_profile"]),
            scopes=tuple(case["scopes"]),
            shadow=True,
        )
        plan = resolution.plan
        selected_gates = [self.gates[gate_id] for gate_id in plan.selected_gate_ids]
        generators = sorted(
            str(gate["gate_id"]) for gate in selected_gates if gate["mutating"]
        )
        test_shards = sorted({str(gate["test_shard"]) for gate in selected_gates})
        explanation = render_explanation(plan)
        return classification, resolution, generators, test_shards, explanation

    def test_every_matrix_row_matches_the_golden_plan(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(case_id=case["case_id"]):
                classification, resolution, generators, test_shards, explanation = (
                    self._evaluate(case)
                )
                expected = case["expected"]
                plan = resolution.plan
                self.assertEqual(
                    classification["path_family_tags"], expected["path_family_tags"]
                )
                self.assertEqual(
                    classification["ignored_paths"], expected["ignored_paths"]
                )
                self.assertEqual(
                    classification["blocked_paths"], expected["blocked_paths"]
                )
                self.assertEqual(
                    classification["recommended_validation_profile"],
                    expected["classifier_profile"],
                )
                self.assertEqual(resolution.effective_profile, expected["effective_profile"])
                self.assertEqual(plan.status, expected["status"])
                self.assertTrue(
                    set(expected["required_gate_ids"]) <= set(plan.selected_gate_ids)
                )
                self.assertTrue(
                    set(expected["required_skipped_gate_ids"]) <= set(plan.skipped_gate_ids)
                )
                self.assertEqual(list(plan.unknown_paths), expected["unknown_paths"])
                self.assertEqual(generators, expected["generator_gate_ids"])
                self.assertEqual(test_shards, expected["test_shards"])
                self.assertEqual(
                    sha256_text(plan.canonical_json()), expected["canonical_plan_sha256"]
                )
                self.assertEqual(
                    sha256_text(explanation), expected["explanation_sha256"]
                )
                for fragment in expected["required_explanation_fragments"]:
                    self.assertIn(fragment, explanation)
                self.assertTrue(resolution.shadow_modifier_active)
                self.assertTrue(resolution.comparison_required)

    def test_golden_serialization_and_explanations_are_deterministic(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(case_id=case["case_id"]):
                first = self._evaluate(case)
                second = self._evaluate(case)
                self.assertEqual(
                    first[1].plan.canonical_json(), second[1].plan.canonical_json()
                )
                self.assertEqual(first[4], second[4])
                self.assertLessEqual(len(first[4].encode("utf-8")), 8192)
                for line in first[4].splitlines()[2:]:
                    self.assertIn("reasons=", line)
                    self.assertIn("obligations=", line)

    def test_every_selected_blocking_gate_has_legacy_shadow_evidence(self) -> None:
        for case in self.fixture["cases"]:
            _, resolution, _, _, _ = self._evaluate(case)
            for gate_id in resolution.plan.selected_gate_ids:
                gate = self.gates[gate_id]
                if gate["severity"] != "blocking":
                    continue
                with self.subTest(case_id=case["case_id"], gate_id=gate_id):
                    self.assertTrue(gate["command_compatibility"])
                    self.assertTrue(str(gate["adapter"]).startswith("legacy:"))

    def test_removed_ci_path_mapping_fails_closed_to_full(self) -> None:
        path = ".github/workflows/project-control-validation.yml"
        original = classifier.classify_path_family

        def without_ci_mapping(value, registry):
            result = original(value, registry)
            if value == path:
                result = dict(result)
                result["tags"] = [tag for tag in result["tags"] if tag != "ci_orchestration"]
                result["reasons"] = [
                    reason
                    for reason in result["reasons"]
                    if reason != "path_rule:ci_orchestration"
                ]
            return result

        with mock.patch.object(classifier, "classify_path_family", without_ci_mapping):
            classification = classifier.classify_paths([path])
        resolution = resolve_profile(
            self.manifest,
            classification,
            requested_profile="affected",
            shadow=True,
        )
        self.assertEqual(classification["path_family_tags"], ["unknown_governed_path"])
        self.assertEqual(resolution.effective_profile, "full")
        self.assertIn("profile_full_research_control", resolution.plan.selected_gate_ids)

    def test_local_retrieval_is_explicitly_non_authoritative(self) -> None:
        by_id = {case["case_id"]: case for case in self.fixture["cases"]}
        ignored = by_id["irrelevant_local_retrieval"]
        classification, resolution, _, _, _ = self._evaluate(ignored)
        self.assertEqual(classification["recommended_validation_profile"], "")
        self.assertEqual(classification["ignored_paths"], ignored["paths"])
        self.assertFalse(classification["project_system_improvement_required"])
        self.assertEqual(resolution.effective_profile, "fast")

        doctor = by_id["local_retrieval_only"]
        _, doctor_resolution, _, _, _ = self._evaluate(doctor)
        blocking = [
            gate_id
            for gate_id in doctor_resolution.plan.selected_gate_ids
            if self.gates[gate_id]["severity"] == "blocking"
        ]
        self.assertEqual(blocking, [])
        self.assertFalse(doctor_resolution.definition.repository_acceptance_authority)

    def test_deletion_and_rename_path_sets_remain_explicit(self) -> None:
        by_id = {case["case_id"]: case for case in self.fixture["cases"]}
        self.assertEqual(by_id["deletion"]["change_kind"], "deleted")
        self.assertEqual(len(by_id["deletion"]["paths"]), 1)
        self.assertEqual(by_id["rename"]["change_kind"], "renamed")
        self.assertEqual(len(by_id["rename"]["paths"]), 2)

    def test_registered_matrix_document_cites_every_executable_case(self) -> None:
        text = MATRIX_PATH.read_text(encoding="utf-8")
        self.assertIn("Plan task: `P5-T08`", text)
        self.assertIn("Legacy execution remains authoritative", text)
        for case in self.fixture["cases"]:
            self.assertIn(f"`{case['case_id']}`", text)


if __name__ == "__main__":
    unittest.main()
