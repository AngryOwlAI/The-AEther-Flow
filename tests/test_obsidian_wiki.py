from __future__ import annotations

import csv
import hashlib
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

    def test_lookup_matches_control_registry_identifier_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry_dir = root / "registries"
            registry_dir.mkdir()
            (registry_dir / "RESEARCH_TASK_REGISTRY.csv").write_text(
                "task_id,path,task_type,status\n"
                "RT-TEST-001,research_control/tasks/RT-TEST-001,synthetic,completed\n",
                encoding="utf-8",
            )

            payload = self.obsidian.lookup_object(root, "RT-TEST-001")

        self.assertEqual(payload["match_count"], 1)
        self.assertEqual(payload["primary_registry"], "RESEARCH_TASK_REGISTRY.csv")
        self.assertIn("task_id", payload["matches"][0]["matched_fields"])

    def test_search_falls_back_to_exact_registry_lookup_on_fts_parse_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry_dir = root / "registries"
            registry_dir.mkdir()
            (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv").write_text(
                "signal_id,status,signal_type\n"
                "MSL-MSRC-ATLASGLUE-LAW,open,memory_retrieval_failure\n",
                encoding="utf-8",
            )
            index_path = Path(tmp) / "memory.sqlite"
            self.obsidian.build_memory_index(root, index_path)

            payload = self.obsidian.search_index(
                root,
                "MSL-MSRC-ATLASGLUE-LAW",
                None,
                10,
                index_path,
            )

        self.assertEqual(payload["fallback"], "exact_registry_field_lookup")
        self.assertIn("fts_error", payload)
        self.assertEqual(payload["results"][0]["object_id"], "MSL-MSRC-ATLASGLUE-LAW")

    def test_status_reports_stale_local_retrieval_as_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "markdown/source.md"
            raw = root / ".local/obsidian/aether-flow-wiki/01_raw/markdown/md-test.md"
            note = root / ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-test.md"
            semantic = root / ".local/content_semantics/markdown/md-test.txt"
            for path in [source, raw, note, semantic]:
                path.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("new source\n", encoding="utf-8")
            raw.write_text("old source\n", encoding="utf-8")
            note.write_text('object_id: "MD-TEST"\n', encoding="utf-8")
            semantic.write_text("new source\n", encoding="utf-8")
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            semantic_hash = hashlib.sha256(semantic.read_bytes()).hexdigest()
            registry_dir = root / "registries"
            registry_dir.mkdir()

            def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
                with (registry_dir / name).open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

            write_csv(
                "MARKDOWN_SOURCE_REGISTRY.csv",
                ["object_id", "path", "format", "source_hash"],
                [
                    {
                        "object_id": "MD-TEST",
                        "path": "markdown/source.md",
                        "format": "markdown",
                        "source_hash": source_hash,
                    }
                ],
            )
            write_csv("TEX_SOURCE_REGISTRY.csv", ["object_id", "path", "format", "source_hash"], [])
            write_csv("PDF_DERIVATIVE_REGISTRY.csv", ["object_id", "path", "format", "source_hash"], [])
            write_csv("HTML_EXPLAINER_REGISTRY.csv", ["object_id", "path", "format", "source_hash"], [])
            write_csv("WIKI_ARTIFACT_REGISTRY.csv", ["object_id", "path"], [])
            write_csv(
                "OBSIDIAN_VAULT_REGISTRY.csv",
                ["object_id", "source_object_id", "vault_note_path", "vault_raw_path", "vault_index_path"],
                [
                    {
                        "object_id": "VAULT-MD-TEST",
                        "source_object_id": "MD-TEST",
                        "vault_note_path": ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-test.md",
                        "vault_raw_path": ".local/obsidian/aether-flow-wiki/01_raw/markdown/md-test.md",
                        "vault_index_path": ".local/obsidian/aether-flow-wiki/03_indexes/by-format-markdown.md",
                    }
                ],
            )
            write_csv(
                "CONTENT_SEMANTIC_REGISTRY.csv",
                [
                    "object_id",
                    "source_object_id",
                    "extraction_status",
                    "extracted_text_path",
                    "content_hash",
                ],
                [
                    {
                        "object_id": "SEMANTIC-MD-TEST",
                        "source_object_id": "MD-TEST",
                        "extraction_status": "PASS",
                        "extracted_text_path": ".local/content_semantics/markdown/md-test.txt",
                        "content_hash": semantic_hash,
                    }
                ],
            )
            write_csv("OBJECT_RELATIONSHIP_REGISTRY.csv", ["object_id", "source_object_id", "target_object_id"], [])

            payload = self.obsidian.status(root)

        self.assertEqual(payload["freshness_status"], "WARN")
        self.assertEqual(payload["core_validation_status"], "PASS")
        self.assertEqual(payload["local_retrieval_status"], "WARN")
        self.assertEqual(payload["freshness_categories"]["blocking"], [])
        self.assertEqual(payload["freshness_categories"]["non_blocking"], [])
        self.assertTrue(any("raw mirror is stale" in warning for warning in payload["freshness_warnings"]))
        self.assertTrue(any("Memory SQLite index is missing" in warning for warning in payload["freshness_warnings"]))
        self.assertTrue(
            any("raw mirror is stale" in warning for warning in payload["freshness_categories"]["local_cache_only"])
        )

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
