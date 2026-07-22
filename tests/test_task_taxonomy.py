from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TaskTaxonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.taxonomy = load_module("task_taxonomy", "task_taxonomy.py")

    def explicit_task(self) -> dict[str, object]:
        return {
            "task_id": "RT-NEW",
            "title": "Readable task title",
            "task_type": "raw_free_form_task_type",
            "created_at": self.taxonomy.EFFECTIVE_AT,
            "task_taxonomy": {
                "schema_id": self.taxonomy.SCHEMA_ID,
                "work_kind": "integration_or_selection",
                "milestone": "source_equivalence_eqsrc",
                "candidate_family": "not_applicable",
                "result_kind": "implemented_and_validated_or_precisely_blocked",
                "authority": "project_control",
                "scope": "project_system",
            },
        }

    def test_embedded_policy_matches_executable_contract(self) -> None:
        self.assertEqual(self.taxonomy.load_policy(REPO_ROOT), self.taxonomy.DEFAULT_POLICY)

    def test_explicit_classification_preserves_raw_fields(self) -> None:
        result = self.taxonomy.classify_task(self.explicit_task())

        self.assertEqual(result["errors"], [])
        self.assertEqual(result["taxonomy_source"], "explicit")
        self.assertEqual(result["taxonomy_confidence"], "high")
        self.assertEqual(result["title"], "Readable task title")
        self.assertEqual(result["raw_task_type"], "raw_free_form_task_type")
        self.assertEqual(result["scope"], "project_system")
        self.assertFalse(result["stronger_science_inferred"])

    def test_new_task_without_explicit_taxonomy_fails_closed(self) -> None:
        task = self.explicit_task()
        task.pop("task_taxonomy")

        result = self.taxonomy.classify_task(task)

        self.assertIn("required_explicit_task_taxonomy_missing", result["errors"])
        self.assertIn("scope", result["unknown_fields"])

    def test_unknown_enum_and_extra_field_are_rejected(self) -> None:
        task = self.explicit_task()
        taxonomy = task["task_taxonomy"]
        assert isinstance(taxonomy, dict)
        taxonomy["scope"] = "unbounded_scientific_truth"
        taxonomy["scientific_rank"] = "proved"

        result = self.taxonomy.classify_task(task)

        self.assertTrue(any(error.startswith("task_taxonomy_invalid_scope") for error in result["errors"]))
        self.assertTrue(any(error.startswith("task_taxonomy_extra_fields") for error in result["errors"]))

    def test_plan_metadata_classification_is_additive(self) -> None:
        task = {
            "task_id": "RT-OLD",
            "task_type": "legacy_title",
            "created_at": "2026-07-01T00:00:00Z",
            "implementation_plan": {"plan_task_id": "P10-T02"},
        }
        plan_item = {
            "plan_task_id": "P10-T02",
            "title": "Normalize task taxonomy",
            "work_kind": "integration_or_selection",
            "task_class": "project_system",
            "target_derivation_milestone": "source_equivalence_eqsrc",
            "expected_result_kind": "implemented_and_validated_or_precisely_blocked",
        }

        result = self.taxonomy.classify_task(
            task,
            role={"authority_level": "project_control"},
            plan_item=plan_item,
        )

        self.assertEqual(result["taxonomy_source"], "plan_metadata")
        self.assertEqual(result["candidate_family"], "not_applicable")
        self.assertEqual(result["scope"], "project_system")
        self.assertFalse(result["historical_source_mutated"])
        self.assertFalse(result["stronger_science_inferred"])

    def test_repository_report_records_zero_mutation_and_strengthening(self) -> None:
        report = self.taxonomy.build_repository_report(REPO_ROOT)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"]["explicit_required_error_count"], 0)
        self.assertEqual(report["counts"]["historical_source_mutation_count"], 0)
        self.assertEqual(report["counts"]["stronger_science_inference_count"], 0)
        self.assertFalse(report["authority_boundary"]["scientific_status_changed"])


if __name__ == "__main__":
    unittest.main()
