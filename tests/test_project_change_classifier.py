from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    research_control_dir = REPO_ROOT / "scripts" / "research_control"
    if str(research_control_dir) not in sys.path:
        sys.path.insert(0, str(research_control_dir))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProjectChangeClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = load_module("classify_project_changes", "classify_project_changes.py")
        cls.doc_impact = load_module("validate_documentation_impact", "validate_documentation_impact.py")
        cls.resolver = load_module("resolve_project_improvement", "resolve_project_improvement.py")

    def test_role_skill_and_validator_changes_require_documentation_impact(self) -> None:
        result = self.classifier.classify_paths(
            [
                ".agents/roles/research_ops/documentation-curator.v0.1.0.md",
                ".codex/skills/continue-research/SKILL.md",
                "scripts/project_control/validate_documentation_impact.py",
            ]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertTrue(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "documentation-curator")
        self.assertIn("role_contract_changed", result["reason_codes"])
        self.assertIn("skill_contract_changed", result["reason_codes"])
        self.assertIn("validator_changed", result["reason_codes"])

    def test_physics_tex_change_does_not_trigger_curator_by_default(self) -> None:
        result = self.classifier.classify_paths(
            ["ontology/tex/aether_flow_foundations.tex"]
        )
        self.assertFalse(result["docs_impact_required"])
        self.assertFalse(result["project_system_improvement_required"])
        self.assertIn("physics_source_changed", result["reason_codes"])

    def test_generated_only_change_blocks_until_source_boundary_is_explained(self) -> None:
        result = self.classifier.classify_paths(["wiki/markdown/example.md"])
        self.assertTrue(result["docs_impact_required"])
        self.assertIn("wiki/markdown/example.md", result["blocked_paths"])
        self.assertIn("direct_generated_derivative_edit", result["reason_codes"])

    def test_generated_change_with_canonical_source_is_not_direct_edit_block(self) -> None:
        result = self.classifier.classify_paths(
            ["README.md", "wiki/markdown/md-readme.md"]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertEqual(result["blocked_paths"], [])
        self.assertIn("generated_derivative_changed", result["reason_codes"])

    def test_documentation_impact_validator_accepts_current_record(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "scripts/project_control/validate_documentation_impact.py",
                "research_control/tasks/RT-20260610-001/documentation_impact.yaml",
            ]
        )
        self.assertEqual(report.errors, [])

    def test_documentation_impact_validator_requires_update_or_record(self) -> None:
        report = self.doc_impact.validate_paths(
            ["scripts/project_control/validate_documentation_impact.py"]
        )
        self.assertTrue(any("documentation impact is required" in error for error in report.errors))

    def test_resolver_recommends_curator_for_docs_impact(self) -> None:
        result = self.resolver.resolve_project_improvement(
            [".codex/skills/continue-research/SKILL.md"]
        )
        self.assertEqual(result["boundary"], "documentation_curator_required")
        self.assertEqual(result["recommended_role"], "documentation-curator")


if __name__ == "__main__":
    unittest.main()
