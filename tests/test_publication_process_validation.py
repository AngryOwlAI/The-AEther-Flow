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

    def test_github_authority_footer_rejects_top_full_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "github-facing/test.md").write_text(
                "# Test Page\n\n"
                "This page is a generated noncanonical reader surface. It orients readers without changing authority.\n\n"
                "## Article Shape\n\nUses `README.md` and `AGENTS.md`.\n\n"
                "<!-- explainer-control: authority_footer -->\n"
                "## Source Binding And Authority\n\n"
                "This page is a generated noncanonical reader surface. It does not authorize changes.\n\n"
                "## Source Materials\n\n- `README.md`\n- `AGENTS.md`\n",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(
            any("GitHub generated-noncanonical paragraph must not appear before first section" in error for error in report.errors)
        )

    def test_html_authority_footer_rejects_top_full_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "html/test.html").write_text(
                '<!doctype html><meta name="aether-flow-human-visual-only" content="true">'
                "<header>This HTML file is a generated noncanonical reader surface. It does not change authority.</header>"
                "<main><p>README.md AGENTS.md</p></main>"
                '<footer data-explainer-control="authority_footer">'
                "This HTML file is a generated noncanonical reader surface. It does not change authority."
                "</footer>",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(
            any("HTML generated-noncanonical paragraph must appear only in authority_footer" in error for error in report.errors)
        )

    def test_github_reader_scope_accepts_bottom_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "github-facing/test.md").write_text(
                "# Test Page\n\n"
                "Subject first. This generated noncanonical page does not authorize changes.\n\n"
                "## Article Shape\n\nUses `README.md` and `AGENTS.md`.\n\n"
                "## Source Materials\n\n- `README.md`\n- `AGENTS.md`\n\n"
                "## Reader Scope\n\nReader scope: fixture boundary only.\n\n"
                "<!-- explainer-control: authority_footer -->\n"
                "## Source Binding And Authority\n\n"
                "This page is a generated noncanonical reader surface. It does not authorize changes.\n",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertEqual(report.errors, [])

    def test_github_reader_scope_rejects_top_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "github-facing/test.md").write_text(
                "# Test Page\n\n"
                "Reader scope: duplicate top boundary.\n\n"
                "## Article Shape\n\nUses `README.md` and `AGENTS.md`.\n\n"
                "## Source Materials\n\n- `README.md`\n- `AGENTS.md`\n\n"
                "## Reader Scope\n\nReader scope: fixture boundary only.\n\n"
                "<!-- explainer-control: authority_footer -->\n"
                "## Source Binding And Authority\n\n"
                "This page is a generated noncanonical reader surface. It does not authorize changes.\n",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("must not remain above the Reader Scope section" in error for error in report.errors))

    def test_github_reader_scope_rejects_nonadjacent_authority_footer(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "github-facing/test.md").write_text(
                "# Test Page\n\n"
                "Subject first. This generated noncanonical page does not authorize changes.\n\n"
                "## Article Shape\n\nUses `README.md` and `AGENTS.md`.\n\n"
                "## Reader Scope\n\nReader scope: fixture boundary only.\n\n"
                "## Source Materials\n\n- `README.md`\n- `AGENTS.md`\n\n"
                "<!-- explainer-control: authority_footer -->\n"
                "## Source Binding And Authority\n\n"
                "This page is a generated noncanonical reader surface. It does not authorize changes.\n",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("must immediately precede authority_footer marker" in error for error in report.errors))

    def test_html_reader_scope_accepts_footer_adjacent_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "html/test.html").write_text(
                '<!doctype html><meta name="aether-flow-human-visual-only" content="true">'
                "<main><p>README.md AGENTS.md</p>"
                '<section class="reader-scope" data-explainer-control="reader_scope" aria-labelledby="reader-scope-title">'
                '<h2 id="reader-scope-title">Reader Scope</h2>'
                "<p>Reader scope: fixture boundary only.</p>"
                "</section></main>"
                '<footer data-explainer-control="authority_footer">'
                "This HTML file is a generated noncanonical reader surface. It does not authorize changes."
                "</footer>",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertEqual(report.errors, [])

    def test_html_reader_scope_rejects_top_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "html/test.html").write_text(
                '<!doctype html><meta name="aether-flow-human-visual-only" content="true">'
                "<header>Reader scope: duplicate top boundary.</header>"
                "<main><p>README.md AGENTS.md</p>"
                '<section class="reader-scope" data-explainer-control="reader_scope" aria-labelledby="reader-scope-title">'
                '<h2 id="reader-scope-title">Reader Scope</h2>'
                "<p>Reader scope: fixture boundary only.</p>"
                "</section></main>"
                '<footer data-explainer-control="authority_footer">'
                "This HTML file is a generated noncanonical reader surface. It does not authorize changes."
                "</footer>",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("HTML Reader scope text must appear only in reader_scope section" in error for error in report.errors))

    def test_retired_topic_registry_fails_if_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "registries/EXPLAINER_TOPIC_REGISTRY.csv").write_text(
                "topic_id,topic_name\nTOPIC-RETIRED,Retired\n",
                encoding="utf-8",
            )
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("EXPLAINER_TOPIC_REGISTRY.csv is retired" in error for error in report.errors))

    def test_orphan_public_explainer_outputs_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_valid_fixture(root)
            (root / "markdown/html-explainer-specs/orphan-explainer.md").write_text("# Orphan\n", encoding="utf-8")
            (root / "github-facing/orphan-explainer.md").write_text("# Orphan\n", encoding="utf-8")
            (root / "html/orphan-explainer.html").write_text("<!doctype html><p>Orphan</p>", encoding="utf-8")
            report = self.validator.validate_publication_process(root)
        self.assertTrue(any("orphan public source spec" in error for error in report.errors))
        self.assertTrue(any("orphan public GitHub Markdown" in error for error in report.errors))
        self.assertTrue(any("orphan public HTML" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
