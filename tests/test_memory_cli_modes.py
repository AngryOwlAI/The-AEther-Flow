from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".codex"
    / "skills"
    / "project-memory-system"
    / "scripts"
    / "bootstrap_memory_system.py"
)


def load_memory_system():
    spec = importlib.util.spec_from_file_location("memory_cli_modes", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DocumentationMemoryModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.memory = load_memory_system()

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name).resolve()
        self.repo_patch = mock.patch.object(self.memory, "REPO_ROOT", self.root)
        self.folder_map_patch = mock.patch.object(
            self.memory, "FOLDER_MAP_PATH", self.root / "FOLDER_MAP.md"
        )
        self.repo_patch.start()
        self.folder_map_patch.start()
        self.addCleanup(self.repo_patch.stop)
        self.addCleanup(self.folder_map_patch.stop)
        self.addCleanup(self.tempdir.cleanup)
        self._create_mixed_fixture()

    def _write_registry(self, name: str, rows: list[dict[str, str]]) -> None:
        path = self.root / "registries" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.memory.csv_text(self.memory.REGISTRIES[name], rows),
            encoding="utf-8",
        )

    def _common_row(self, **overrides: str) -> dict[str, str]:
        row = {field: "" for field in self.memory.COMMON_COLUMNS}
        row.update(
            {
                "format": "markdown",
                "role": "authored_markdown",
                "authority_status": "canonical_markdown_source",
                "audience": "humans_and_agents",
                "owner_skill": "markdown-wiki",
                "validation_status": "PASS",
                "last_validated_at": "2026-07-15T00:00:00Z",
                "notes": "fixture",
            }
        )
        row.update(overrides)
        return row

    def _create_mixed_fixture(self) -> None:
        for name in self.memory.REGISTRIES:
            self._write_registry(name, [])
        for directory in [
            "html",
            "wiki/markdown",
            "wiki/html",
            "wiki/indexes",
            "ontology/tex",
            "ontology/pdfs",
            ".local/content_semantics/tex",
        ]:
            (self.root / directory).mkdir(parents=True, exist_ok=True)

        readme = self.root / "README.md"
        readme.write_text("# Documentation fixture\n", encoding="utf-8")
        markdown_row = self._common_row(
            object_id="MD-README",
            path="README.md",
            source_hash=self.memory.sha256_file(readme),
            generated_outputs="wiki/markdown/md-readme.md",
            owner_skill="project-memory-system",
        )
        markdown_row.update(
            {
                "github_facing": "true",
                "agent_documentation": "false",
                "contains_mermaid": "false",
                "contains_math": "false",
            }
        )
        self._write_registry("MARKDOWN_SOURCE_REGISTRY.csv", [markdown_row])

        wiki_path = self.root / "wiki/markdown/md-readme.md"
        wiki_text = self.memory.wiki_note_text(
            markdown_row, {markdown_row["object_id"]: markdown_row}
        )
        wiki_path.write_text(wiki_text, encoding="utf-8")
        wiki_hash = self.memory.sha256_file(wiki_path)
        wiki_row = self._common_row(
            object_id="WIKI-MD-README",
            path="wiki/markdown/md-readme.md",
            format="wiki_markdown",
            role="generated_metadata_note",
            authority_status="generated_noncanonical",
            source_hash=wiki_hash,
            related_source="MD-README",
            generated_from="MD-README",
            owner_skill="markdown-wiki",
        )
        wiki_row.update(
            {
                "source_object_id": "MD-README",
                "source_path": "README.md",
                "source_object_hash": markdown_row["source_hash"],
                "wiki_hash": wiki_hash,
                "wiki_kind": "markdown",
                "generated_at": "2026-07-15T00:00:00Z",
            }
        )
        self._write_registry("WIKI_ARTIFACT_REGISTRY.csv", [wiki_row])

        file_rows = []
        for registry_name, row in [
            ("MARKDOWN_SOURCE_REGISTRY.csv", markdown_row),
            ("WIKI_ARTIFACT_REGISTRY.csv", wiki_row),
        ]:
            mirror = {field: row.get(field, "") for field in self.memory.COMMON_COLUMNS}
            mirror["source_registry"] = registry_name
            file_rows.append(mirror)
        self._write_registry("FILE_OBJECT_REGISTRY.csv", file_rows)
        self.memory.generate_documentation_indexes(
            {
                "MARKDOWN_SOURCE_REGISTRY.csv": [markdown_row],
                "HTML_EXPLAINER_REGISTRY.csv": [],
                "WIKI_ARTIFACT_REGISTRY.csv": [wiki_row],
            }
        )

        tex_path = self.root / "ontology/tex/corrupted.tex"
        tex_path.write_text("corrupted fixture TeX\n", encoding="utf-8")
        tex_row = self._common_row(
            object_id="TEX-ONTOLOGY-CORRUPTED",
            path="ontology/tex/corrupted.tex",
            format="tex",
            role="ontology_source",
            authority_status="canonical",
            source_hash="0" * 64,
            owner_skill="tex-wiki",
        )
        tex_row.update(
            {
                "pdf_required": "false",
                "claim_status": "benchmark_claim",
                "research_status": "canonical_ontology",
                "ontology_promotion_status": "accepted",
                "equation_scope": "gr_benchmark",
            }
        )
        self._write_registry("TEX_SOURCE_REGISTRY.csv", [tex_row])
        (self.root / "ontology/pdfs/corrupted.pdf").write_bytes(b"not a real PDF")
        (self.root / ".local/content_semantics/tex/corrupted.txt").write_text(
            "stale local retrieval\n", encoding="utf-8"
        )

    def test_documentation_core_ignores_corrupted_tex_but_full_core_detects_it(self) -> None:
        with mock.patch.object(self.memory, "validate_mermaid_documentation"):
            documentation = self.memory.documentation_validate_core()
            full = self.memory.memory_validate_core()

        self.assertTrue(documentation.ok, documentation.errors)
        self.assertNotIn("memory_core.tex_vocabulary", documentation.check_ids)
        self.assertTrue(
            any("TEX-ONTOLOGY-CORRUPTED" in error for error in full.errors),
            full.errors,
        )

    def test_documentation_core_detects_documentation_corruption(self) -> None:
        (self.root / "README.md").write_text(
            "# Documentation fixture changed\n", encoding="utf-8"
        )
        with mock.patch.object(self.memory, "validate_mermaid_documentation"):
            report = self.memory.documentation_validate_core()

        self.assertFalse(report.ok)
        self.assertTrue(
            any("MD-README" in error and "stale source_hash" in error for error in report.errors),
            report.errors,
        )

    def test_documentation_sync_never_calls_unrelated_family_owners(self) -> None:
        forbidden = AssertionError("unrelated family owner was called")
        with (
            mock.patch.object(self.memory, "discover_tex_rows", side_effect=forbidden),
            mock.patch.object(self.memory, "generate_pdf_rows", side_effect=forbidden),
            mock.patch.object(self.memory, "write_generated_registries", side_effect=forbidden),
            mock.patch.object(self.memory, "local_retrieval_health", side_effect=forbidden),
        ):
            summary = self.memory.documentation_sync()

        self.assertEqual(summary["selected_object_count"], 2)
        self.assertEqual(
            summary["excluded_families"],
            self.memory.DOCUMENTATION_EXCLUDED_FAMILIES,
        )
        tex_rows = self.memory.read_csv_rows(
            self.root / "registries/TEX_SOURCE_REGISTRY.csv"
        )
        self.assertEqual(tex_rows[0]["source_hash"], "0" * 64)
        by_format = (
            self.root / "wiki/indexes/documentation-by-format.md"
        ).read_text(encoding="utf-8")
        self.assertIn("MD-README", by_format)
        self.assertNotIn("TEX-ONTOLOGY-CORRUPTED", by_format)
        self.memory.generate_indexes(self.memory.source_rows_by_registry())
        after_full_index_sync = (
            self.root / "wiki/indexes/documentation-by-format.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(by_format, after_full_index_sync)
        self.assertTrue(
            (self.root / ".local/content_semantics/tex/corrupted.txt").exists()
        )

    def test_documentation_validation_composes_only_scoped_core_and_publication(self) -> None:
        publication = self.memory.ValidationReport(
            gate_id="publication_validation",
            check_ids=["publication_validation.process"],
        )
        with (
            mock.patch.object(self.memory, "validate_mermaid_documentation"),
            mock.patch.object(self.memory, "publication_validation", return_value=publication),
        ):
            report = self.memory.documentation_validation()

        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.gate_id, "documentation_validation")
        self.assertIn("documentation_core.source_hash", report.check_ids)
        self.assertIn("publication_validation.process", report.check_ids)
        self.assertNotIn("memory_core.tex_vocabulary", report.check_ids)
        self.assertNotIn("local_retrieval_health.freshness", report.check_ids)

    def test_docs_cli_modes_do_not_fall_through_to_full_compatibility(self) -> None:
        summary = {
            "gate_id": "documentation_scope",
            "selected_object_count": 2,
            "selected_counts": {},
            "excluded_families": self.memory.DOCUMENTATION_EXCLUDED_FAMILIES,
            "excluded_registered_counts": {},
            "no_physics_authority": True,
        }
        report = self.memory.ValidationReport(gate_id="documentation_validation")
        forbidden = AssertionError("full compatibility owner was called")
        with (
            mock.patch.object(self.memory, "documentation_sync", return_value=summary) as sync,
            mock.patch.object(
                self.memory, "documentation_scope_summary", return_value=summary
            ),
            mock.patch.object(
                self.memory, "documentation_validation", return_value=report
            ) as validate,
            mock.patch.object(self.memory, "source_rows_by_registry", return_value={}),
            mock.patch.object(self.memory, "read_csv_rows", return_value=[]),
            mock.patch.object(self.memory, "validate_all", side_effect=forbidden),
            mock.patch.object(self.memory, "bootstrap", side_effect=forbidden),
        ):
            for argv in (["--docs-only"], ["--docs-validate-only"]):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(self.memory.main(argv), 0)
                self.assertIn("Documentation mode summary:", output.getvalue())

        sync.assert_called_once_with(refresh_existing=False)
        self.assertEqual(validate.call_count, 2)

    def test_check_alias_still_uses_full_validation(self) -> None:
        report = self.memory.ValidationReport(gate_id="memory_legacy_composite")
        output = io.StringIO()
        with mock.patch.object(self.memory, "validate_all", return_value=report) as validate:
            with redirect_stdout(output):
                self.assertEqual(self.memory.main(["--check"]), 0)

        validate.assert_called_once_with(strict_docs=False)
        self.assertNotIn("Documentation mode summary:", output.getvalue())

    def test_cli_rejects_conflicting_modes(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.memory.parse_args(["--docs-only", "--validate-only"])


if __name__ == "__main__":
    unittest.main()
