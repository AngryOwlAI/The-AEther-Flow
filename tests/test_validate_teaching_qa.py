from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_teaching_qa.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_teaching_qa", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SPEC_TEXT = """---
title: "Role Routing"
purpose: "Teach role routing."
audience: "humans"
output_path: "html/role-routing-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
claim_boundary: "Teaching only."
human_visual_only: true
teaching_loop:
  enabled: true
  rounds: 2
  student_role: "documentation-student@0.1.0"
  teacher_role: "documentation-teacher@0.1.0"
  audience_model: "layperson"
  qa_packet: "markdown/teaching-packets/role-routing.teaching-qa.md"
  required_teaching_blocks:
    - "plain_language_model"
    - "glossary"
    - "guided_walkthrough"
    - "common_questions"
    - "examples_and_non_examples"
    - "misconception_repairs"
    - "check_your_understanding"
---

# Role Routing Spec

## Teaching Q&A Basis

This explainer uses `markdown/teaching-packets/role-routing.teaching-qa.md` as explanatory support only.
"""


PACKET_TEXT = """---
packet_id: "role-routing.teaching-qa.v0.1"
topic_slug: "role-routing"
source_spec: "markdown/html-explainer-specs/role-routing-explainer.md"
derived_outputs:
  - "html/role-routing-explainer.html"
audience_model: "layperson"
student_role: "documentation-student@0.1.0"
teacher_role: "documentation-teacher@0.1.0"
rounds: 2
source_materials:
  - "README.md"
  - "AGENTS.md"
claim_boundary: "Teaching only."
authority_status: "curated_explanatory_support"
---

# Teaching Q&A Packet: Role Routing

## Curator Feature Selection

Plain-language topic: role routing.

## Round 1 Student Questions

### Q1
What is role routing?

## Round 1 Teacher Answers

### A1
Plain answer:
Role routing chooses the allowed helper for one bounded task.

Technical anchor:
The job records the role and allowed paths.

Source paths:
- README.md
- AGENTS.md

Boundary note:
This answer does not change authority.

Curator note:
Show a concrete workflow.

## Round 2 Student Follow-up Questions

### Q1
What happens if the wrong role is selected?

## Round 2 Teacher Answers

### A1
Plain answer:
The task should stop at the boundary.

Technical anchor:
Validators and allowlists define the boundary.

Source paths:
- README.md
- AGENTS.md

Boundary note:
This answer does not authorize bypassing validators.

Curator note:
Add a misconception repair.

## Curator Synthesis Notes

### Concepts that must appear in the HTML explainer

- Role selection.

### Concepts that must appear in GitHub-facing Markdown

- Authority boundary.

### Glossary candidates

- Role.

### Common confusions to repair

- Decomposition is not a new job.

### Examples and non-examples

- Example and non-example.

### Next reading notes

- README.md.

### Source gaps

- None.

### Claims intentionally not made

- No new authority.
"""


class TeachingQaValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def write_fixture(self, root: Path, packet_text: str = PACKET_TEXT) -> None:
        spec = root / "markdown/html-explainer-specs/role-routing-explainer.md"
        packet = root / "markdown/teaching-packets/role-routing.teaching-qa.md"
        spec.parent.mkdir(parents=True)
        packet.parent.mkdir(parents=True)
        spec.write_text(SPEC_TEXT, encoding="utf-8")
        packet.write_text(packet_text, encoding="utf-8")

    def test_valid_packet_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            errors = self.validator.validate_root(root)

        self.assertEqual([], errors)

    def test_teacher_answer_requires_boundary_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, PACKET_TEXT.replace("Boundary note:", "Boundary:"))
            errors = self.validator.validate_root(root)

        self.assertTrue(any("Boundary note" in error for error in errors))

    def test_generated_source_material_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = PACKET_TEXT.replace('- "AGENTS.md"', '- "html/role-routing-explainer.html"')
            self.write_fixture(root, packet)
            errors = self.validator.validate_root(root)

        self.assertTrue(any("generated output as authority" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
