from __future__ import annotations

import csv
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "project_control" / "audit_documentation_surfaces.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_documentation_surfaces", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_registry(root: Path, name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path = root / "registries" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def github_facing_page_text(extra: str = "") -> str:
    return f"""# Example

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/example.md`
- **Related HTML:** `html/example.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

This reader-facing page explains the example feature without acting as source authority.

## Why The Project Needs It

The page gives humans and external AI a controlled orientation before they inspect sources.

## How It Works

The page is derived from the registered explainer spec and keeps source paths visible.

## What It Is Not

It is not physics authority, control authority, or a replacement for registries.

## Diagram Reading Guide

Read the diagram as source-backed orientation, not as authority promotion.

```mermaid
flowchart TD
  A["Spec"] --> B["Reader page"]
```

## Source Authority

The registered spec and registries remain the evidence to inspect before changing project knowledge.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Aether-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

Inspect the source spec, the related HTML derivative, and the registry rows.

## All Source Materials

- `README.md`
{extra}
"""


def build_minimal_documentation_surface(root: Path) -> None:
    readme = root / "README.md"
    readme.write_text("# Example\n", encoding="utf-8")

    source = root / "markdown" / "html-explainer-specs" / "example.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(
        "---\n"
        "title: Example\n"
        "source_materials:\n"
        "  - \"README.md\"\n"
        "---\n"
        "# Example Spec\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "  A[\"Spec\"] --> B[\"Reader page\"]\n"
        "```\n",
        encoding="utf-8",
    )
    mirror = root / "github-facing" / "example.md"
    mirror.parent.mkdir(parents=True, exist_ok=True)
    mirror.write_text(github_facing_page_text(), encoding="utf-8")

    html = root / "html" / "example.html"
    html.parent.mkdir(parents=True, exist_ok=True)
    html.write_text("<!doctype html><title>Example</title>\n", encoding="utf-8")

    tex = root / "ontology" / "tex" / "example.tex"
    tex.parent.mkdir(parents=True, exist_ok=True)
    tex.write_text("\\section{Example}\n", encoding="utf-8")
    pdf = root / "ontology" / "pdfs" / "example.pdf"
    pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf.write_bytes(b"%PDF synthetic\n")

    wiki_markdown = root / "wiki" / "markdown" / "md-example.md"
    wiki_html = root / "wiki" / "html" / "html-example.md"
    wiki_tex = root / "wiki" / "tex" / "tex-example.md"
    wiki_pdf = root / "wiki" / "pdf" / "pdf-example.md"
    for path in (wiki_markdown, wiki_html, wiki_tex, wiki_pdf):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Generated note\n", encoding="utf-8")

    write_registry(
        root,
        "MARKDOWN_SOURCE_REGISTRY.csv",
        ["object_id", "path", "source_hash", "generated_outputs"],
        [
            {
                "object_id": "MD-HTML-SPEC-EXAMPLE",
                "path": "markdown/html-explainer-specs/example.md",
                "source_hash": file_hash(source),
                "generated_outputs": "wiki/markdown/md-example.md",
            }
        ],
    )
    write_registry(
        root,
        "HTML_EXPLAINER_REGISTRY.csv",
        [
            "object_id",
            "path",
            "source_hash",
            "generated_outputs",
            "source_basis",
            "source_basis_hash",
            "html_hash",
            "generated_from",
        ],
        [
            {
                "object_id": "HTML-EXAMPLE",
                "path": "html/example.html",
                "source_hash": file_hash(html),
                "generated_outputs": "wiki/html/html-example.md",
                "source_basis": "MD-HTML-SPEC-EXAMPLE",
                "source_basis_hash": file_hash(source),
                "html_hash": file_hash(html),
                "generated_from": "MD-HTML-SPEC-EXAMPLE",
            }
        ],
    )
    write_registry(
        root,
        "TEX_SOURCE_REGISTRY.csv",
        [
            "object_id",
            "path",
            "source_hash",
            "generated_outputs",
            "pdf_required",
            "pdf_object_id",
            "pdf_path",
        ],
        [
            {
                "object_id": "TEX-EXAMPLE",
                "path": "ontology/tex/example.tex",
                "source_hash": file_hash(tex),
                "generated_outputs": "ontology/pdfs/example.pdf;wiki/tex/tex-example.md",
                "pdf_required": "true",
                "pdf_object_id": "PDF-EXAMPLE",
                "pdf_path": "ontology/pdfs/example.pdf",
            }
        ],
    )
    write_registry(
        root,
        "PDF_DERIVATIVE_REGISTRY.csv",
        [
            "object_id",
            "path",
            "source_hash",
            "generated_outputs",
            "source_tex_object_id",
            "source_tex_path",
            "source_tex_hash",
            "pdf_hash",
        ],
        [
            {
                "object_id": "PDF-EXAMPLE",
                "path": "ontology/pdfs/example.pdf",
                "source_hash": file_hash(pdf),
                "generated_outputs": "wiki/pdf/pdf-example.md",
                "source_tex_object_id": "TEX-EXAMPLE",
                "source_tex_path": "ontology/tex/example.tex",
                "source_tex_hash": file_hash(tex),
                "pdf_hash": file_hash(pdf),
            }
        ],
    )
    write_registry(
        root,
        "WIKI_ARTIFACT_REGISTRY.csv",
        ["object_id", "path", "source_path"],
        [
            {
                "object_id": "WIKI-EXAMPLE",
                "path": "wiki/markdown/md-example.md",
                "source_path": "markdown/html-explainer-specs/example.md",
            }
        ],
    )
    write_registry(
        root,
        "FILE_OBJECT_REGISTRY.csv",
        ["object_id", "path"],
        [{"object_id": "MD-HTML-SPEC-EXAMPLE", "path": "markdown/html-explainer-specs/example.md"}],
    )
    write_registry(root, "CONTENT_SEMANTIC_REGISTRY.csv", ["object_id", "path", "extracted_text_path"], [])
    write_registry(
        root,
        "OBSIDIAN_VAULT_REGISTRY.csv",
        [
            "object_id",
            "path",
            "vault_note_path",
            "vault_raw_path",
            "vault_attachment_path",
            "vault_index_path",
        ],
        [],
    )
    write_registry(
        root,
        "OBJECT_RELATIONSHIP_REGISTRY.csv",
        ["object_id", "edge_id", "source_path", "target_path"],
        [],
    )


class DocumentationSurfaceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = load_audit_module()

    def test_audit_accepts_consistent_surface_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.counts["checked_markdown_rows"], 1)
        self.assertEqual(report.counts["checked_github_facing_explainers"], 1)

    def test_audit_detects_stale_markdown_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            write_registry(
                root,
                "MARKDOWN_SOURCE_REGISTRY.csv",
                ["object_id", "path", "source_hash", "generated_outputs"],
                [
                    {
                        "object_id": "MD-HTML-SPEC-EXAMPLE",
                        "path": "markdown/html-explainer-specs/example.md",
                        "source_hash": "stale",
                        "generated_outputs": "wiki/markdown/md-example.md",
                    }
                ],
            )
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertTrue(any("stale source_hash" in error for error in report.errors))

    def test_github_facing_explainer_may_differ_from_source_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertFalse(any("mirror body differs" in error for error in report.errors))

    def test_github_facing_explainer_rejects_renderer_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            page = root / "github-facing" / "example.md"
            page.write_text(
                github_facing_page_text("\n## Rendering Intent\n\nRenderer-only instruction.\n"),
                encoding="utf-8",
            )
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertTrue(any("renderer-instruction heading" in error for error in report.errors))

    def test_github_facing_explainer_requires_source_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            page = root / "github-facing" / "example.md"
            page.write_text(
                github_facing_page_text().replace(
                    "- **Derived from spec:** `markdown/html-explainer-specs/example.md`\n",
                    "",
                ),
                encoding="utf-8",
            )
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertTrue(any("Derived from spec must be" in error for error in report.errors))

    def test_html_source_basis_must_be_registered(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_minimal_documentation_surface(root)
            html = root / "html" / "example.html"
            source = root / "markdown" / "html-explainer-specs" / "example.md"
            write_registry(
                root,
                "HTML_EXPLAINER_REGISTRY.csv",
                [
                    "object_id",
                    "path",
                    "source_hash",
                    "generated_outputs",
                    "source_basis",
                    "source_basis_hash",
                    "html_hash",
                    "generated_from",
                ],
                [
                    {
                        "object_id": "HTML-EXAMPLE",
                        "path": "html/example.html",
                        "source_hash": file_hash(html),
                        "generated_outputs": "wiki/html/html-example.md",
                        "source_basis": "MD-MISSING",
                        "source_basis_hash": file_hash(source),
                        "html_hash": file_hash(html),
                        "generated_from": "MD-MISSING",
                    }
                ],
            )
            report = self.audit.audit_documentation_surfaces(root, include_local=False)
        self.assertTrue(any("source_basis is not registered" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
