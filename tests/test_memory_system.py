from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


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
    spec = importlib.util.spec_from_file_location("bootstrap_memory_system", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_snapshot() -> dict[str, str]:
    paths = []
    paths.append(REPO_ROOT / "FOLDER_MAP.md")
    paths.extend((REPO_ROOT / "registries").glob("*.csv"))
    paths.extend((REPO_ROOT / "registries").glob("*.json"))
    paths.extend((REPO_ROOT / "wiki").rglob("*.md"))
    return {
        path.relative_to(REPO_ROOT).as_posix(): file_hash(path)
        for path in sorted(paths)
        if path.exists()
    }


class MemorySystemSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.memory_system = load_memory_system()

    def test_validate_only_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--validate-only"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bootstrap_is_idempotent_for_generated_outputs(self) -> None:
        before = generated_snapshot()
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = generated_snapshot()
        self.assertEqual(before, after)

    def test_duplicate_object_ids_are_errors(self) -> None:
        errors = self.memory_system.find_duplicate_object_ids(
            {
                "A.csv": [{"object_id": "DUPLICATE-ID"}],
                "B.csv": [{"object_id": "DUPLICATE-ID"}],
            }
        )
        self.assertTrue(any("duplicate object_id" in error for error in errors))

    def test_path_traversal_is_rejected(self) -> None:
        reason = self.memory_system.validate_relative_path("../outside.md")
        self.assertEqual(reason, "path traversal is not allowed")

    def test_stale_pdf_source_hash_is_an_error(self) -> None:
        rows_by_registry = {
            name: self.memory_system.read_csv_rows(self.memory_system.registry_path(name))
            for name in self.memory_system.SOURCE_REGISTRY_NAMES
        }
        rows_by_registry["PDF_DERIVATIVE_REGISTRY.csv"] = [
            dict(row) for row in rows_by_registry["PDF_DERIVATIVE_REGISTRY.csv"]
        ]
        rows_by_registry["PDF_DERIVATIVE_REGISTRY.csv"][0]["source_tex_hash"] = "stale"
        report = self.memory_system.ValidationReport()
        self.memory_system.validate_pdf_registry(report, rows_by_registry)
        self.assertTrue(any("stale source_tex_hash" in error for error in report.errors))

    def test_merge_refreshes_mechanical_fields_without_overwriting_judgments(self) -> None:
        existing_rows = [
            {
                "object_id": "TEX-TEST",
                "path": "ontology/tex/test.tex",
                "format": "tex",
                "source_hash": "old-hash",
                "last_validated_at": "2000-01-01T00:00:00Z",
                "claim_status": "open_derivation_claim",
            }
        ]
        discovered_rows = [
            {
                "object_id": "TEX-TEST",
                "path": "ontology/tex/test.tex",
                "format": "tex",
                "source_hash": "new-hash",
                "last_validated_at": "2099-01-01T00:00:00Z",
                "claim_status": "benchmark_claim",
            }
        ]
        with (
            mock.patch.object(self.memory_system, "read_csv_rows", return_value=existing_rows),
            mock.patch.object(self.memory_system, "write_csv_if_changed"),
        ):
            rows = self.memory_system.merge_authored_registry(
                "TEX_SOURCE_REGISTRY.csv",
                self.memory_system.TEX_COLUMNS,
                discovered_rows,
                refresh_existing=False,
            )
        self.assertEqual(rows[0]["source_hash"], "new-hash")
        self.assertEqual(rows[0]["last_validated_at"], "2099-01-01T00:00:00Z")
        self.assertEqual(rows[0]["claim_status"], "open_derivation_claim")

    def test_rebuilt_pdf_paths_stamp_built_at(self) -> None:
        tex_rows = self.memory_system.read_csv_rows(
            self.memory_system.registry_path("TEX_SOURCE_REGISTRY.csv")
        )
        target_pdf_path = tex_rows[0]["pdf_path"]
        with mock.patch.object(self.memory_system, "write_csv_if_changed"):
            rows = self.memory_system.generate_pdf_rows(
                tex_rows,
                "2099-01-01T00:00:00Z",
                rebuilt_pdf_paths={target_pdf_path},
            )
        rebuilt_row = next(row for row in rows if row["path"] == target_pdf_path)
        self.assertEqual(rebuilt_row["built_at"], "2099-01-01T00:00:00Z")

    def test_html_spec_contract_requires_source_backed_fields(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/missing-fields.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Missing fields"\n'
                "---\n"
                "# Missing fields\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-MISSING-FIELDS",
                            "path": "markdown/html-explainer-specs/missing-fields.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(any("missing output_path" in error for error in report.errors))
        self.assertTrue(any("missing source_materials" in error for error in report.errors))

    def test_generate_html_rows_binds_new_html_to_source_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            (root / "registries").mkdir()
            (root / "html").mkdir()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Synthetic"\n'
                'purpose: "Test binding."\n'
                'audience: "test"\n'
                'output_path: "html/synthetic.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "---\n",
                encoding="utf-8",
            )
            html = root / "html/synthetic.html"
            html.write_text("<!doctype html><title>Synthetic</title>\n", encoding="utf-8")
            (root / "registries/HTML_EXPLAINER_REGISTRY.csv").write_text(
                ",".join(self.memory_system.HTML_COLUMNS) + "\n",
                encoding="utf-8",
            )
            markdown_rows = [
                {
                    "object_id": "MD-HTML-SPEC-SYNTHETIC",
                    "path": "markdown/html-explainer-specs/synthetic.md",
                    "role": "html_explainer_source_spec",
                    "source_hash": "spec-hash",
                }
            ]
            with (
                mock.patch.object(self.memory_system, "REPO_ROOT", root),
                mock.patch.object(self.memory_system, "write_csv_if_changed"),
            ):
                rows = self.memory_system.generate_html_rows(
                    "2099-01-01T00:00:00Z", markdown_rows
                )
        self.assertEqual(rows[0]["source_basis"], "MD-HTML-SPEC-SYNTHETIC")
        self.assertEqual(rows[0]["source_basis_hash"], "spec-hash")
        self.assertEqual(
            rows[0]["visual_explainer_skill_version"],
            "visual-explainer@0.7.1-project-aether-flow",
        )

    def test_stale_html_source_basis_hash_is_an_error(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                '<!doctype html><meta name="aether-flow-source-basis" content="MD-HTML-SPEC-SYNTHETIC">'
                '<meta name="aether-flow-source-basis-hash" content="old-hash">'
                '<meta name="aether-flow-human-visual-only" content="true">',
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "new-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "old-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(any("stale source_basis_hash" in error for error in report.errors))

    def test_unchanged_html_does_not_mask_changed_spec_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            (root / "registries").mkdir()
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text("<!doctype html><title>Synthetic</title>\n", encoding="utf-8")
            html_hash = self.memory_system.sha256_file(html)
            existing_row = {
                "object_id": "HTML-SYNTHETIC",
                "path": "html/synthetic.html",
                "format": "html",
                "role": "html_visual_explainer",
                "authority_status": "generated_noncanonical",
                "audience": "humans",
                "source_hash": html_hash,
                "related_source": "MD-HTML-SPEC-SYNTHETIC",
                "generated_from": "MD-HTML-SPEC-SYNTHETIC",
                "generated_outputs": "wiki/html/html-synthetic.md",
                "owner_skill": "html-visual-explainer",
                "validation_status": "PASS",
                "last_validated_at": "2000-01-01T00:00:00Z",
                "notes": "Human-only generated visual explainer.",
                "human_visual_only": "true",
                "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                "source_basis_hash": "old-spec-hash",
                "html_hash": html_hash,
                "visual_explainer_skill_version": "visual-explainer@0.7.1-project-aether-flow",
            }
            (root / "registries/HTML_EXPLAINER_REGISTRY.csv").write_text(
                ",".join(self.memory_system.HTML_COLUMNS)
                + "\n"
                + ",".join(existing_row[column] for column in self.memory_system.HTML_COLUMNS)
                + "\n",
                encoding="utf-8",
            )
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Synthetic"\n'
                'purpose: "Test stale binding."\n'
                'audience: "test"\n'
                'output_path: "html/synthetic.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "---\n",
                encoding="utf-8",
            )
            markdown_rows = [
                {
                    "object_id": "MD-HTML-SPEC-SYNTHETIC",
                    "path": "markdown/html-explainer-specs/synthetic.md",
                    "role": "html_explainer_source_spec",
                    "source_hash": "new-spec-hash",
                }
            ]
            with (
                mock.patch.object(self.memory_system, "REPO_ROOT", root),
                mock.patch.object(self.memory_system, "write_csv_if_changed"),
            ):
                rows = self.memory_system.generate_html_rows(
                    "2099-01-01T00:00:00Z", markdown_rows
                )
        self.assertEqual(rows[0]["source_basis_hash"], "old-spec-hash")

    def test_wiki_artifact_rows_cover_registered_sources(self) -> None:
        rows_by_registry = {
            name: self.memory_system.read_csv_rows(self.memory_system.registry_path(name))
            for name in self.memory_system.SOURCE_REGISTRY_NAMES
        }
        source_rows = self.memory_system.all_source_rows(rows_by_registry)
        wiki_rows = self.memory_system.existing_by_id(
            self.memory_system.read_csv_rows(
                self.memory_system.registry_path("WIKI_ARTIFACT_REGISTRY.csv")
            )
        )
        for source_row in source_rows:
            wiki_id = self.memory_system.wiki_object_id(source_row["object_id"])
            self.assertIn(wiki_id, wiki_rows)
            self.assertTrue((REPO_ROOT / wiki_rows[wiki_id]["path"]).exists())

    def test_file_object_registry_includes_generated_wiki_rows(self) -> None:
        file_rows = self.memory_system.existing_by_id(
            self.memory_system.read_csv_rows(
                self.memory_system.registry_path("FILE_OBJECT_REGISTRY.csv")
            )
        )
        wiki_rows = self.memory_system.read_csv_rows(
            self.memory_system.registry_path("WIKI_ARTIFACT_REGISTRY.csv")
        )
        for row in wiki_rows:
            self.assertIn(row["object_id"], file_rows)

    def test_folder_map_classifies_core_lanes(self) -> None:
        rows_by_registry = {
            name: self.memory_system.read_csv_rows(self.memory_system.registry_path(name))
            for name in self.memory_system.SOURCE_REGISTRY_NAMES
            + self.memory_system.GENERATED_REGISTRY_NAMES
        }
        cases = {
            "ontology/tex": "canonical source",
            "registries": "control authority",
            "wiki/tex": "generated derivative",
            ".local/obsidian": "local retrieval",
            ".codex/skills/project-memory-system/scripts": "tooling",
            "markdown/ontology-promotions": "reserved lane",
        }
        for folder, expected_category in cases.items():
            category, _reason = self.memory_system.classify_folder(folder, rows_by_registry)
            self.assertEqual(category, expected_category, folder)

    def test_folder_map_mentions_task_artifact_relationships(self) -> None:
        rows_by_registry = {
            name: self.memory_system.read_csv_rows(self.memory_system.registry_path(name))
            for name in self.memory_system.SOURCE_REGISTRY_NAMES
            + self.memory_system.GENERATED_REGISTRY_NAMES
        }
        text = self.memory_system.folder_map_text(rows_by_registry)
        self.assertIn("| `research_control/tasks` | `control authority`", text)
        self.assertIn("bounded proposal, audit, refutation, repair, and handoff", text)
        self.assertIn("| `wiki/tex` | `generated derivative`", text)


if __name__ == "__main__":
    unittest.main()
