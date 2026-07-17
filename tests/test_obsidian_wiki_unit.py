from __future__ import annotations

import hashlib
import importlib.util
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / ".codex" / "skills" / "project-memory-system" / "scripts"
LIB_PATH = SCRIPT_DIR / "obsidian_wiki_lib.py"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "obsidian_wiki" / "mini_repo"
FIXED_TIME = "2099-01-01T00:00:00Z"


def load_obsidian_wiki():
    spec = importlib.util.spec_from_file_location("obsidian_wiki_lib_unit", LIB_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@contextmanager
def miniature_repository() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "mini_repo"
        shutil.copytree(FIXTURE_ROOT, root)
        yield root


class ObsidianWikiUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obsidian = load_obsidian_wiki()

    def prepare_local_state(
        self, root: Path
    ) -> tuple[dict[str, list[dict[str, str]]], Path]:
        self.obsidian.write_generated_registries(
            root,
            self.obsidian.load_rows_by_registry(root),
            FIXED_TIME,
            write_semantic_text=True,
        )
        rows_by_registry = self.obsidian.load_rows_by_registry(root)
        vault = root / self.obsidian.VAULT_ROOT_RELATIVE
        self.obsidian.write_vault(root, vault, rows_by_registry)
        return rows_by_registry, vault

    def test_fixture_repository_has_expected_source_formats(self) -> None:
        rows_by_registry = self.obsidian.load_rows_by_registry(FIXTURE_ROOT)
        source_rows = self.obsidian.source_rows_with_registry(rows_by_registry)

        self.assertEqual(len(source_rows), 4)
        self.assertEqual({row["format"] for row in source_rows}, {"markdown", "tex", "html"})
        for row in source_rows:
            source = FIXTURE_ROOT / row["path"]
            self.assertTrue(source.is_file())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), row["source_hash"])

    def test_text_extractors_cover_markdown_tex_and_html(self) -> None:
        with miniature_repository() as root:
            md_result = self.obsidian.extract_markdown(root / "README.md")
            tex_result = self.obsidian.extract_tex(root / "ontology/tex/source.tex")
            html_result = self.obsidian.extract_html(root / "html/explainer.html")

        self.assertIn("Lorentzian Fixture", md_result.headings)
        self.assertIn("research_control/tasks/TASK_INDEX.md", md_result.links)
        self.assertIn("Fixture Geometry", tex_result.headings)
        self.assertIn("sec:fixture", tex_result.labels)
        self.assertIn("Visible Fixture Flow", html_result.headings)
        self.assertIn("../README.md", html_result.links)
        self.assertNotIn("fixtureHidden", html_result.text)

    def test_pdf_extractor_reads_existing_project_pdf(self) -> None:
        try:
            import fitz
        except ModuleNotFoundError:
            self.skipTest("PyMuPDF is not installed")

        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "tiny-fixture.pdf"
            document = fitz.open()
            try:
                page = document.new_page()
                page.insert_text(
                    (72, 72),
                    "Tiny Lorentzian PDF fixture for conditional extraction coverage.",
                )
                document.save(pdf_path)
            finally:
                document.close()
            result = self.obsidian.extract_pdf(pdf_path)

        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.page_count, 1)
        self.assertIn("Lorentzian PDF fixture", result.text)

    def test_generated_registry_rows_cover_source_objects(self) -> None:
        with miniature_repository() as root:
            rows_by_registry = self.obsidian.load_rows_by_registry(root)
            source_rows = self.obsidian.source_rows_with_registry(rows_by_registry)
            obsidian_rows = self.obsidian.generate_obsidian_vault_rows(
                root, rows_by_registry, FIXED_TIME
            )
            semantic_rows = self.obsidian.generate_content_semantic_rows(
                root, rows_by_registry, FIXED_TIME, write_text=False
            )
            relationship_rows = self.obsidian.generate_relationship_rows(
                root,
                rows_by_registry,
                obsidian_rows,
                semantic_rows,
                FIXED_TIME,
            )

        self.assertEqual(len(obsidian_rows), len(source_rows))
        self.assertEqual(len(semantic_rows), len(source_rows))
        self.assertTrue(
            any(row["relationship_type"] == "has_vault_note" for row in relationship_rows)
        )
        self.assertTrue(
            any(
                row["relationship_type"] == "has_content_semantics"
                for row in relationship_rows
            )
        )

    def test_memory_index_searches_extracted_content(self) -> None:
        with miniature_repository() as root:
            self.prepare_local_state(root)
            index_path = root / ".local" / "memory_index" / "unit.sqlite"
            self.obsidian.build_memory_index(root, index_path)
            payload = self.obsidian.search_index(
                root,
                "Lorentzian",
                None,
                10,
                index_path,
            )

        self.assertTrue(payload["results"])
        self.assertTrue(
            any(row["object_id"] == "MD-FIXTURE-README" for row in payload["results"])
        )

    def test_memory_index_searches_generated_task_index_content(self) -> None:
        with miniature_repository() as root:
            self.prepare_local_state(root)
            index_path = root / ".local" / "memory_index" / "unit.sqlite"
            self.obsidian.build_memory_index(root, index_path)
            payload = self.obsidian.search_index(
                root,
                "Generated navigation support",
                None,
                10,
                index_path,
                literal=True,
            )

        self.assertTrue(
            any(
                row["object_id"] == "MD-RESEARCH-CONTROL-TASK-INDEX"
                for row in payload["results"]
            )
        )

    def test_lookup_matches_control_registry_identifier_fields(self) -> None:
        with miniature_repository() as root:
            payload = self.obsidian.lookup_object(root, "RT-FIXTURE-001")

        self.assertEqual(payload["match_count"], 1)
        self.assertEqual(payload["primary_registry"], "RESEARCH_TASK_REGISTRY.csv")
        self.assertIn("task_id", payload["matches"][0]["matched_fields"])

    def test_search_falls_back_to_exact_registry_lookup_on_fts_parse_error(self) -> None:
        with miniature_repository() as root:
            index_path = root / ".local" / "memory_index" / "unit.sqlite"
            self.obsidian.build_memory_index(root, index_path)
            payload = self.obsidian.search_index(
                root,
                "RT-FIXTURE-001",
                None,
                10,
                index_path,
            )

        self.assertEqual(payload["fallback"], "exact_registry_field_lookup")
        self.assertIn("fts_error", payload)
        self.assertEqual(payload["results"][0]["object_id"], "RT-FIXTURE-001")

    def test_status_reports_stale_local_retrieval_as_warning(self) -> None:
        with miniature_repository() as root:
            self.prepare_local_state(root)
            (root / "README.md").write_text(
                "# Changed source\n\nThis mutation makes the raw mirror stale.\n",
                encoding="utf-8",
            )
            payload = self.obsidian.status(root)

        self.assertEqual(payload["freshness_status"], "WARN")
        self.assertEqual(payload["core_validation_status"], "PASS")
        self.assertEqual(payload["local_retrieval_status"], "WARN")
        self.assertEqual(payload["freshness_categories"]["blocking"], [])
        self.assertEqual(payload["freshness_categories"]["non_blocking"], [])
        self.assertTrue(
            any("raw mirror is stale" in warning for warning in payload["freshness_warnings"])
        )
        self.assertTrue(
            any(
                "Memory SQLite index is missing" in warning
                for warning in payload["freshness_warnings"]
            )
        )
        self.assertTrue(
            any(
                "raw mirror is stale" in warning
                for warning in payload["freshness_categories"]["local_cache_only"]
            )
        )

    def test_vault_writes_declared_index_paths(self) -> None:
        with miniature_repository() as root:
            rows_by_registry, _ = self.prepare_local_state(root)
            obsidian_rows = rows_by_registry["OBSIDIAN_VAULT_REGISTRY.csv"]
            missing = [
                row["vault_index_path"]
                for row in obsidian_rows
                if not (root / row["vault_index_path"]).exists()
            ]
            writes_are_isolated = not root.resolve().is_relative_to(
                (REPO_ROOT / ".local").resolve()
            )

        self.assertEqual(missing, [])
        self.assertTrue(writes_are_isolated)

    def test_vault_preserves_manual_local_notes(self) -> None:
        with miniature_repository() as root:
            rows_by_registry, vault = self.prepare_local_state(root)
            readme_row = next(
                row
                for row in rows_by_registry["OBSIDIAN_VAULT_REGISTRY.csv"]
                if row["source_object_id"] == "MD-FIXTURE-README"
            )
            note_path = root / readme_row["vault_note_path"]
            original = note_path.read_text(encoding="utf-8")
            note_path.write_text(
                original.replace(
                    self.obsidian.DEFAULT_MANUAL_NOTES,
                    "Manual observation retained across regeneration.",
                ),
                encoding="utf-8",
            )
            self.obsidian.write_vault(root, vault, rows_by_registry)
            regenerated = note_path.read_text(encoding="utf-8")

        self.assertIn("Manual observation retained across regeneration.", regenerated)


if __name__ == "__main__":
    unittest.main()
