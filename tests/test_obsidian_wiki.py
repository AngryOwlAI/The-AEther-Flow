from __future__ import annotations

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / ".codex" / "skills" / "project-memory-system" / "scripts"
LIB_PATH = SCRIPT_DIR / "obsidian_wiki_lib.py"


def load_obsidian_wiki():
    spec = importlib.util.spec_from_file_location("obsidian_wiki_lib", LIB_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ObsidianWikiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obsidian = load_obsidian_wiki()

    def test_text_extractors_cover_markdown_tex_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = root / "sample.md"
            tex = root / "sample.tex"
            html = root / "sample.html"
            markdown.write_text("# Heading\n\n[Link](target.md)\n\n$E=mc^2$\n", encoding="utf-8")
            tex.write_text(
                "\\section{Geometry}\\label{sec:geometry}\\begin{equation}x=1\\end{equation}\\ref{sec:geometry}",
                encoding="utf-8",
            )
            html.write_text(
                "<html><head><title>Title</title><style>.x{}</style></head>"
                "<body><h1>Visible</h1><script>hidden()</script><a href='x.html'>x</a></body></html>",
                encoding="utf-8",
            )
            md_result = self.obsidian.extract_markdown(markdown)
            tex_result = self.obsidian.extract_tex(tex)
            html_result = self.obsidian.extract_html(html)
        self.assertIn("Heading", md_result.headings)
        self.assertIn("target.md", md_result.links)
        self.assertIn("Geometry", tex_result.headings)
        self.assertIn("sec:geometry", tex_result.labels)
        self.assertIn("Visible", html_result.headings)
        self.assertIn("x.html", html_result.links)
        self.assertNotIn("hidden", html_result.text)

    def test_pdf_extractor_reads_existing_project_pdf(self) -> None:
        try:
            import fitz  # noqa: F401
        except ModuleNotFoundError:
            self.skipTest("PyMuPDF is not installed")
        pdf_path = next((REPO_ROOT / "ontology" / "pdfs").glob("*.pdf"))
        result = self.obsidian.extract_pdf(pdf_path)
        self.assertEqual(result.status, "PASS")
        self.assertGreater(result.page_count, 0)
        self.assertGreater(len(result.text), 100)

    def test_generated_registry_rows_cover_source_objects(self) -> None:
        rows_by_registry = self.obsidian.load_rows_by_registry(REPO_ROOT)
        source_rows = self.obsidian.source_rows_with_registry(rows_by_registry)
        obsidian_rows = self.obsidian.generate_obsidian_vault_rows(
            REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z"
        )
        semantic_rows = self.obsidian.generate_content_semantic_rows(
            REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z", write_text=False
        )
        relationship_rows = self.obsidian.generate_relationship_rows(
            REPO_ROOT, rows_by_registry, obsidian_rows, semantic_rows, "2099-01-01T00:00:00Z"
        )
        self.assertEqual(len(obsidian_rows), len(source_rows))
        self.assertEqual(len(semantic_rows), len(source_rows))
        self.assertTrue(any(row["relationship_type"] == "has_vault_note" for row in relationship_rows))
        self.assertTrue(any(row["relationship_type"] == "has_content_semantics" for row in relationship_rows))

    def test_memory_index_searches_extracted_content(self) -> None:
        self.obsidian.write_generated_registries(
            REPO_ROOT,
            self.obsidian.load_rows_by_registry(REPO_ROOT),
            "2099-01-01T00:00:00Z",
            write_semantic_text=True,
        )
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "memory.sqlite"
            self.obsidian.build_memory_index(REPO_ROOT, index_path)
            self.assertTrue(index_path.exists())
            conn = sqlite3.connect(index_path)
            try:
                rows = conn.execute(
                    "SELECT object_id FROM docs_fts WHERE docs_fts MATCH ? LIMIT 1",
                    ("Lorentzian",),
                ).fetchall()
            finally:
                conn.close()
        self.assertTrue(rows)

    def test_vault_writes_declared_index_paths(self) -> None:
        rows_by_registry = self.obsidian.load_rows_by_registry(REPO_ROOT)
        local_root = REPO_ROOT / ".local"
        local_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=local_root) as tmp:
            vault = Path(tmp) / "vault"
            obsidian_rows = self.obsidian.generate_obsidian_vault_rows(
                REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z", vault=vault
            )
            semantic_rows = self.obsidian.generate_content_semantic_rows(
                REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z", write_text=False
            )
            relationship_rows = self.obsidian.generate_relationship_rows(
                REPO_ROOT, rows_by_registry, obsidian_rows, semantic_rows, "2099-01-01T00:00:00Z"
            )
            rows_by_registry.update(
                {
                    "OBSIDIAN_VAULT_REGISTRY.csv": obsidian_rows,
                    "CONTENT_SEMANTIC_REGISTRY.csv": semantic_rows,
                    "OBJECT_RELATIONSHIP_REGISTRY.csv": relationship_rows,
                }
            )
            self.obsidian.write_vault(REPO_ROOT, vault, rows_by_registry)
            missing = [
                row["vault_index_path"]
                for row in obsidian_rows
                if not (REPO_ROOT / row["vault_index_path"]).exists()
            ]
        self.assertEqual(missing, [])

    def test_vault_preserves_manual_local_notes(self) -> None:
        rows_by_registry = self.obsidian.load_rows_by_registry(REPO_ROOT)
        local_root = REPO_ROOT / ".local"
        local_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=local_root) as tmp:
            vault = Path(tmp) / "vault"
            obsidian_rows = self.obsidian.generate_obsidian_vault_rows(
                REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z", vault=vault
            )
            semantic_rows = self.obsidian.generate_content_semantic_rows(
                REPO_ROOT, rows_by_registry, "2099-01-01T00:00:00Z", write_text=False
            )
            relationship_rows = self.obsidian.generate_relationship_rows(
                REPO_ROOT, rows_by_registry, obsidian_rows, semantic_rows, "2099-01-01T00:00:00Z"
            )
            rows_by_registry.update(
                {
                    "OBSIDIAN_VAULT_REGISTRY.csv": obsidian_rows,
                    "CONTENT_SEMANTIC_REGISTRY.csv": semantic_rows,
                    "OBJECT_RELATIONSHIP_REGISTRY.csv": relationship_rows,
                }
            )
            self.obsidian.write_vault(REPO_ROOT, vault, rows_by_registry)
            readme_row = next(row for row in obsidian_rows if row["source_object_id"] == "MD-README")
            note_path = REPO_ROOT / readme_row["vault_note_path"]
            original = note_path.read_text(encoding="utf-8")
            note_path.write_text(
                original.replace(
                    self.obsidian.DEFAULT_MANUAL_NOTES,
                    "Manual observation retained across regeneration.",
                ),
                encoding="utf-8",
            )
            self.obsidian.write_vault(REPO_ROOT, vault, rows_by_registry)
            regenerated = note_path.read_text(encoding="utf-8")
        self.assertIn("Manual observation retained across regeneration.", regenerated)


if __name__ == "__main__":
    unittest.main()
