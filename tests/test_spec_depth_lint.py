from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "spec_depth_lint.py"


def load_depth_lint():
    spec = importlib.util.spec_from_file_location("spec_depth_lint", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SpecDepthLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.depth_lint = load_depth_lint()

    def test_html_instruction_block_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "html/example-explainer.html"
            path.parent.mkdir(parents=True)
            path.write_text(
                '<article data-content-block="example_block">'
                '<span data-source-path="README.md"></span>'
                "<p>Explain the project workflow.</p>"
                "</article>",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_html(path)

        self.assertTrue(any("instruction" in warning for warning in warnings))

    def test_html_structured_matrix_can_pass_word_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "html/example-explainer.html"
            path.parent.mkdir(parents=True)
            rows = "".join(
                f"<tr><td>Row {index}</td><td>Source-backed explanatory detail "
                "that helps a reader understand the project boundary, the "
                "allowed claim, the forbidden claim, and the practical next "
                "step inside the governed workflow.</td></tr>"
                for index in range(1, 5)
            )
            path.write_text(
                '<article data-content-block="example_block">'
                '<span data-source-path="README.md"></span>'
                f"<table>{rows}</table>"
                "</article>",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_html(path)

        self.assertEqual([], warnings)

    def test_html_self_referential_block_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "html/example-explainer.html"
            path.parent.mkdir(parents=True)
            path.write_text(
                '<article data-content-block="example_block">'
                '<span data-source-path="README.md"></span>'
                "<p>This page explains the project workflow and maps source materials.</p>"
                "</article>",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_html(path)

        self.assertTrue(any("project subject" in warning for warning in warnings))

    def test_spec_directive_block_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "markdown/html-explainer-specs/example-explainer.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "## Required Content Blocks\n\n"
                "- subject_summary: Render the summary first.\n"
                "- workflow_story: Explain the workflow.\n\n",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_spec(path)

        self.assertTrue(any("workflow_story" in warning for warning in warnings))

    def test_spec_state_as_noun_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "markdown/html-explainer-specs/example-explainer.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "## Required Content Blocks\n\n"
                "- subject_summary: Render the summary first.\n"
                "- state_entry: A completed lifecycle entry section covering tracked program state, latest handoffs, and task files.\n\n",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_spec(path)

        self.assertEqual([], warnings)

    def test_teaching_enabled_spec_requires_plain_language_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "markdown/html-explainer-specs/example-explainer.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\n"
                "teaching_loop:\n"
                "  enabled: true\n"
                "  required_teaching_blocks:\n"
                "    - \"plain_language_model\"\n"
                "    - \"glossary\"\n"
                "    - \"guided_walkthrough\"\n"
                "    - \"common_questions\"\n"
                "    - \"examples_and_non_examples\"\n"
                "    - \"misconception_repairs\"\n"
                "    - \"check_your_understanding\"\n"
                "---\n\n"
                "## Required Content Blocks\n\n"
                "- subject_summary: Render the summary first.\n"
                "- common_questions: Reader questions without source grounding.\n\n",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_spec(path)

        self.assertTrue(any("plain-language" in warning for warning in warnings))
        self.assertTrue(any("source paths" in warning for warning in warnings))

    def test_teaching_enabled_github_markdown_requires_common_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "github-facing/example-explainer.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Example\n\n## Start here\n", encoding="utf-8")

            warnings = self.depth_lint.lint_github_markdown(path)

        self.assertTrue(any("Common questions" in warning for warning in warnings))

    def test_github_markdown_self_reference_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "github-facing/example-explainer.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Example\n\n"
                "## Source Binding\n\n"
                "- **Derived from spec:** `markdown/html-explainer-specs/example.md`\n"
                "- **Related HTML:** `html/example.html`\n\n"
                "## Common questions\n\n"
                "Answered.\n\n"
                "## Common misunderstandings\n\n"
                "This page explains itself instead of the workflow.\n",
                encoding="utf-8",
            )

            warnings = self.depth_lint.lint_github_markdown(path)

        self.assertTrue(any("project subject" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
