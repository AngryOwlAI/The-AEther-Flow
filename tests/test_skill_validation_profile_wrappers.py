from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest import mock

from scripts.validation import cli as validation_cli


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATHS = (
    ".codex/skills/continue-research/SKILL.md",
    ".codex/skills/improve-project-system/SKILL.md",
    ".codex/skills/user-modified-project/SKILL.md",
    ".codex/skills/project-memory-system/SKILL.md",
)
WORKFLOW_EXAMPLES = {
    "research": ".codex/skills/continue-research/SKILL.md",
    "project_system": ".codex/skills/improve-project-system/SKILL.md",
    "user_modified": ".codex/skills/user-modified-project/SKILL.md",
}
PROFILE_PLAN_COMMANDS = (
    ".venv/bin/python -m scripts.validation.cli plan --profile <fast|affected|full> --paths <changed-path> --explain",
    ".venv/bin/python -m scripts.validation.cli plan --profile checkpoint --staged --explain",
    ".venv/bin/python -m scripts.validation.cli plan --profile doctor --scope local_retrieval --explain",
)


class SkillValidationProfileWrapperTests(unittest.TestCase):
    def read_skill(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def plan(self, *arguments: str) -> dict[str, object]:
        output = io.StringIO()
        with (
            mock.patch.object(
                subprocess,
                "run",
                side_effect=AssertionError("profile planning executed subprocess.run"),
            ),
            mock.patch.object(
                subprocess,
                "Popen",
                side_effect=AssertionError("profile planning executed subprocess.Popen"),
            ),
            redirect_stdout(output),
        ):
            exit_code = validation_cli.main(["plan", *arguments, "--json"])
        self.assertEqual(exit_code, 0)
        return json.loads(output.getvalue())

    def test_four_skills_use_the_shared_profile_wrapper_contract(self) -> None:
        for relative_path in SKILL_PATHS:
            with self.subTest(skill=relative_path):
                text = self.read_skill(relative_path)
                self.assertEqual(text.count("## Validation Profile Wrapper"), 1)
                self.assertIn("-m scripts.validation.cli plan", text)
                for profile in ("fast", "affected", "checkpoint", "full", "doctor"):
                    self.assertIn(f"`{profile}`", text)
                self.assertIn("planner_executes_commands=false", text)
                self.assertIn("legacy execution remains authoritative", text)
                self.assertIn("final staged", text)
                self.assertIn(
                    "research_control/design/agent_validation_output_consumption_policy_v1.md",
                    text,
                )
                self.assertIn("canonical source inspection", text)

    def test_profile_command_surface_is_identical_across_skills(self) -> None:
        for relative_path in SKILL_PATHS:
            with self.subTest(skill=relative_path):
                text = self.read_skill(relative_path)
                observed = tuple(
                    line
                    for line in text.splitlines()
                    if "-m scripts.validation.cli plan" in line
                )
                self.assertEqual(observed, PROFILE_PLAN_COMMANDS)

    def test_no_skill_recreates_the_retired_precheckpoint_full_chain(self) -> None:
        retired_chain = (
            "scripts/project_control/validate_documentation_impact.py",
            "scripts/research_control/validate_research_control.py --check-diff",
            "bootstrap_memory_system.py --validate-only",
            "-m unittest discover -s tests",
            "git diff --check",
        )
        for relative_path in SKILL_PATHS:
            with self.subTest(skill=relative_path):
                text = self.read_skill(relative_path)
                self.assertFalse(all(command in text for command in retired_chain))
        memory_skill = self.read_skill(SKILL_PATHS[-1])
        self.assertNotIn("make PYTHON=.venv/bin/python validate-memory\n", memory_skill)
        self.assertNotIn("make PYTHON=.venv/bin/python validate-memory-full\n", memory_skill)

    def test_research_project_system_and_user_modified_examples_are_plan_only(self) -> None:
        for workflow, relative_path in WORKFLOW_EXAMPLES.items():
            with self.subTest(workflow=workflow):
                plan = self.plan(
                    "--profile",
                    "affected",
                    "--paths",
                    relative_path,
                )
                self.assertEqual(plan["status"], "READY")
                self.assertEqual(plan["requested_profile"], "affected")
                self.assertEqual(plan["effective_profile"], "affected")
                self.assertFalse(plan["planner_executes_commands"])
                self.assertEqual(plan["execution_authority"], "legacy")
                self.assertNotIn("checkpoint_transaction", plan["selected_gate_ids"])

    def test_checkpoint_profile_selects_but_does_not_execute_final_transaction(self) -> None:
        plan = self.plan(
            "--profile",
            "checkpoint",
            "--scope",
            "staged",
            "--paths",
            SKILL_PATHS[0],
        )
        self.assertEqual(plan["status"], "READY")
        self.assertFalse(plan["planner_executes_commands"])
        self.assertEqual(plan["execution_authority"], "legacy")
        self.assertIn("checkpoint_transaction", plan["selected_gate_ids"])

    def test_doctor_profile_remains_local_and_nonblocking(self) -> None:
        plan = self.plan(
            "--profile",
            "doctor",
            "--scope",
            "local_retrieval",
            "--paths",
        )
        self.assertEqual(plan["status"], "READY")
        self.assertFalse(plan["planner_executes_commands"])
        selected = set(plan["selected_gate_ids"])
        severities = {
            entry["gate_id"]: entry["severity"]
            for entry in plan["entries"]
            if entry["gate_id"] in selected
        }
        self.assertTrue(selected)
        self.assertNotIn("blocking", severities.values())
        self.assertNotIn("checkpoint_transaction", selected)


if __name__ == "__main__":
    unittest.main()
