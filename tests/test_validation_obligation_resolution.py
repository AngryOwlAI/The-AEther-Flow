from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "research_control/design/validation_obligation_resolution_policy_v1.md"
SKILLS = {
    name: ROOT / f".codex/skills/{name}/SKILL.md"
    for name in ("continue-research", "improve-project-system", "user-modified-project")
}
DIRECT_RECIPES = (
    "bootstrap_memory_system.py --validate-only",
    "validate_documentation_impact.py",
    "validate_research_control.py --check-diff",
    "validate_claim_language.py --changed --json",
)


class ValidationObligationResolutionTests(unittest.TestCase):
    def test_skills_name_obligations_without_repeating_direct_recipes(self) -> None:
        required = {
            "memory_core",
            "documentation_impact",
            "research_control_diff",
            "claim_language_changed",
            "checkpoint_transaction",
        }
        for name, path in SKILLS.items():
            with self.subTest(skill=name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("validation_obligation_resolution_policy_v1.md", text)
                self.assertTrue(required.issubset(set(re.findall(r"`([a-z_]+)`", text))))
                for recipe in DIRECT_RECIPES:
                    self.assertNotIn(recipe, text)
                for block in re.findall(r"```zsh\n(.*?)\n```", text, flags=re.DOTALL):
                    self.assertFalse(
                        "validate_research_control.py" in block and "--check-diff" in block
                    )

    def test_memory_preflight_and_checkpoint_entry_point_remain_explicit(self) -> None:
        continue_text = SKILLS["continue-research"].read_text(encoding="utf-8")
        improve_text = SKILLS["improve-project-system"].read_text(encoding="utf-8")
        self.assertIn("query_memory.py status --json", continue_text)
        self.assertIn("query_memory.py status --json", improve_text)
        self.assertIn("checkpoint_research_transaction.py", continue_text)
        for path in SKILLS.values():
            text = " ".join(path.read_text(encoding="utf-8").split())
            self.assertIn("final staged acceptance", text)

    def test_policy_has_one_recipe_per_named_gate(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        rows = re.findall(r"^\| `([a-z_]+)` \| `([^`]+)` \|$", text, flags=re.MULTILINE)
        gates = [gate for gate, _ in rows]
        self.assertEqual(len(gates), len(set(gates)))
        self.assertEqual(
            set(gates),
            {
                "memory_sync",
                "memory_core",
                "project_improvement_signals",
                "documentation_impact",
                "research_control_core",
                "research_control_diff",
                "claim_language_changed",
                "git_diff_check",
                "checkpoint_transaction",
            },
        )
        self.assertIn(
            "working result never satisfies a staged obligation", " ".join(text.split())
        )

    def test_active_project_control_maintainer_semantics_are_unchanged(self) -> None:
        with (ROOT / "registries/AGENT_ROLE_REGISTRY.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = [
                row
                for row in csv.DictReader(handle)
                if row["role_id"] == "project-control-maintainer"
                and row["status"] == "active"
            ]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["version"], "0.2.0")
        self.assertEqual(row["may_promote_claims"], "false")
        self.assertEqual(row["requires_human_gate"], "false")
        self.assertEqual(
            row["default_validators"],
            "validate_documentation_impact;validate_research_control;unittest",
        )

    def test_skill_contracts_are_mutable_memory_preflight_sources(self) -> None:
        validator = (
            ROOT / "scripts/research_control/validate_research_control.py"
        ).read_text(encoding="utf-8")
        for object_id in (
            "MD-SKILL-CONTINUE-RESEARCH",
            "MD-SKILL-IMPROVE-PROJECT-SYSTEM",
            "MD-SKILL-USER-MODIFIED-PROJECT",
        ):
            self.assertIn(f'"{object_id}"', validator)


if __name__ == "__main__":
    unittest.main()
