from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_publication_process.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_publication_process", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PublicationProcessValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def write_valid_fixture(self, root: Path) -> None:
        (root / "registries").mkdir()
        (root / "markdown/publication-briefs").mkdir(parents=True)
        (root / "markdown/html-explainer-specs").mkdir(parents=True)
        (root / "github-facing").mkdir()
        (root / "html").mkdir()
        (root / "research_control/tasks/RT-TEST/artifacts/screenshots").mkdir(parents=True)
        (root / "README.md").write_text("# Readme\n", encoding="utf-8")
        (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
        (root / "registries/PUBLICATION_BRIEF_REGISTRY.csv").write_text(
            "brief_id,page_title,document_type,migration_status,brief_path,source_spec_path,github_markdown_path,html_output_path,source_materials,visual_strategy,review_status,screenshot_desktop_path,screenshot_mobile_path,before_after_review_path,owner_role,approval_required_before_corpus_migration,notes\n"
            "PB-TEST,Test Page,overview_article,reviewed,markdown/publication-briefs/test.publication-brief.md,markdown/html-explainer-specs/test.md,github-facing/test.md,html/test.html,README.md;AGENTS.md,source_matrix,pilot_review_pass,research_control/tasks/RT-TEST/artifacts/screenshots/desktop.png,research_control/tasks/RT-TEST/artifacts/screenshots/mobile.png,research_control/tasks/RT-TEST/artifacts/review.md,documentation-curator,true,fixture\n",
            encoding="utf-8",
        )
        (root / "registries/EXPLAINER_TOPIC_REGISTRY.csv").write_text(
            "topic_id,topic_name,required,status,document_family,source_spec_path,github_markdown_path,html_output_path,publication_brief_id,migration_status,source_bundle,output_surfaces,owner_role,claim_boundary_id,notes\n"
            "TOPIC-TEST,Test Page,true,active,front_door,markdown/html-explainer-specs/test.md,github-facing/test.md,html/test.html,PB-TEST,reviewed,README.md;AGENTS.md,github_markdown;html,documentation-curator,CB-TEST,fixture\n",
            encoding="utf-8",
        )
        (root / "markdown/publication-briefs/test.publication-brief.md").write_text(
            "---\n"
            'brief_id: "PB-TEST"\n'
            'subject: "Test Page"\n'
            'reader: "Reader"\n'
            'reader_job: "Understand the fixture."\n'
            'document_type: "overview_article"\n'
            'reading_experience: "Article."\n'
            "narrative_structure:\n"
            '  - "Open with subject."\n'
            'visual_strategy: "source_matrix"\n'
            "source_basis:\n"
            '  - "README.md"\n'
            '  - "AGENTS.md"\n'
            "authority_boundaries:\n"
            '  - "Generated pages are noncanonical."\n'
            "output_surfaces:\n"
            '  - "github-facing/test.md"\n'
            '  - "html/test.html"\n'
            "acceptance_criteria:\n"
            '  - "No old skeleton."\n'
            "forbidden_patterns:\n"
            '  - "Generic system map."\n'
            'migration_status: "reviewed"\n'
            "---\n"
            "# Brief\n",
            encoding="utf-8",
        )
        (root / "markdown/html-explainer-specs/test.md").write_text(
            "---\n"
            'title: "Test Page"\n'
            'purpose: "Test."\n'
            'audience: "Reader."\n'
            'output_path: "html/test.html"\n'
            'github_markdown_output_path: "github-facing/test.md"\n'
            'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
            'publication_brief: "markdown/publication-briefs/test.publication-brief.md"\n'
            'document_type: "overview_article"\n'
            'visual_strategy: "source_matrix"\n'
            'migration_status: "reviewed"\n'
            "source_materials:\n"
            '  - "README.md"\n'
            '  - "AGENTS.md"\n'
            'claim_boundary: "Generated noncanonical fixture."\n'
            "human_visual_only: true\n"
            "standalone_html: true\n"
            "no_external_runtime: true\n"
            "---\n"
            "# Spec\n",
            encoding="utf-8",
        )
        (root / "github-facing/test.md").write_text(
            "# Test Page\n\nSubject first. This generated noncanonical page does not authorize changes.\n\n"
            "## Article Shape\n\nUses `README.md` and `AGENTS.md`.\n\n"
            "## Source Materials\n\n- `README.md`\n- `AGENTS.md`\n",
            encoding="utf-8",
        )
        (root / "html/test.html").write_text(
            '<!doctype html><meta name="aether-flow-human-visual-only" content="true">'
            "<p>Generated noncanonical page. README.md AGENTS.md</p>",
            encoding="utf-8",
        )
        (root / "research_control/tasks/RT-TEST/artifacts/screenshots/desktop.png").write_bytes(b"png")
        (root / "research_control/tasks/RT-TEST/artifacts/screenshots/mobile.png").write_bytes(b"png")
        (root / "research_control/tasks/RT-TEST/artifacts/review.md").write_text("PASS\n", encoding="utf-8")

    def test_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            report = self.validator.validate_publication_process(root)
        self.assertEqual(report.errors, [])

    def test_forbidden_migrated_heading_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            page = root / "github-facing/test.md"
            page.write_text(page.read_text(encoding="utf-8") + "\n## System Map\n\nOld skeleton.\n", encoding="utf-8")
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("forbidden old heading" in error for error in report.errors))

    def test_external_runtime_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "html/test.html").write_text('<script src="https://example.test/app.js"></script>', encoding="utf-8")
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("banned public-doc runtime" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
