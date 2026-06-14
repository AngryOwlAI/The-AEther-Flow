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
MERMAID_VALIDATOR_PATH = (
    REPO_ROOT
    / ".codex"
    / "skills"
    / "visual-explainer"
    / "subskills"
    / "mermaid-documentation"
    / "scripts"
    / "validate_mermaid_sources.py"
)


def load_memory_system():
    spec = importlib.util.spec_from_file_location("bootstrap_memory_system", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_mermaid_validator():
    spec = importlib.util.spec_from_file_location(
        "test_mermaid_validator", MERMAID_VALIDATOR_PATH
    )
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


MERMAID_SOURCE = "flowchart TD\n  A[Source] --> B[Derivative]\n"
MERMAID_RENDERER = "mermaid@11.15.0;mermaid-inline-svg-renderer@0.1.1"


def normalized_mermaid_source(source: str) -> str:
    lines = source.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(line.rstrip() for line in lines)


def mermaid_source_hash(source: str) -> str:
    return hashlib.sha256(normalized_mermaid_source(source).encode("utf-8")).hexdigest()


def write_mermaid_spec(
    root: Path,
    *,
    include_block: bool = True,
    duplicate_block: bool = False,
    path_text: str = "markdown/html-explainer-specs/synthetic.md",
    frontmatter: bool = True,
) -> Path:
    spec = root / path_text
    spec.parent.mkdir(parents=True, exist_ok=True)
    body = "# Synthetic\n\n"
    if include_block:
        body += (
            "<!-- mermaid-diagram-id: authority-ladder -->\n"
            "```mermaid\n"
            f"{MERMAID_SOURCE}"
            "```\n"
        )
    if duplicate_block:
        body += (
            "\n<!-- mermaid-diagram-id: authority-ladder -->\n"
            "```mermaid\n"
            f"{MERMAID_SOURCE}"
            "```\n"
        )
    if frontmatter:
        spec.write_text(
            "---\n"
            "mermaid_diagrams:\n"
            "  required: true\n"
            "  ids:\n"
            "    - authority-ladder\n"
            "---\n"
            f"{body}",
            encoding="utf-8",
        )
    else:
        spec.write_text(body, encoding="utf-8")
    return spec


def write_governed_html(
    root: Path,
    *,
    source: str = MERMAID_SOURCE,
    canvas_body: str | None = None,
    canvas_hash: str | None = None,
    zoom_label: str = "Fit",
    runtime_script: str = "",
    extra_body: str = "",
) -> Path:
    html = root / "html/synthetic.html"
    html.parent.mkdir(parents=True, exist_ok=True)
    if canvas_body is None:
        canvas_body = (
            '<svg width="100" height="40" viewBox="0 0 100 40" data-mermaid-rendered="true" '
            'data-mermaid-diagram-id="authority-ladder"><text>A</text></svg>'
        )
    canvas_hash = canvas_hash if canvas_hash is not None else mermaid_source_hash(source)
    html.write_text(
        "<!doctype html>\n"
        '<section class="diagram-shell" data-mermaid-diagram-id="authority-ladder">\n'
        '  <div class="mermaid-wrap">\n'
        '    <div class="zoom-controls"><span class="zoom-label">'
        f"{zoom_label}"
        "</span></div>\n"
        '    <div class="mermaid-viewport">\n'
        '      <div class="mermaid mermaid-canvas" '
        f'data-renderer="{MERMAID_RENDERER}" '
        f'data-render-source-sha256="{canvas_hash}">'
        f"{canvas_body}</div>\n"
        "    </div>\n"
        "  </div>\n"
        '  <script type="text/plain" class="diagram-source" data-mermaid-diagram-id="authority-ladder">\n'
        f"{source}"
        "  </script>\n"
        "</section>\n"
        f"{extra_body}\n"
        f"{runtime_script}\n",
        encoding="utf-8",
    )
    return html


def mermaid_markdown_row(path: str, role: str = "html_explainer_source_spec") -> dict[str, str]:
    return {
        "object_id": "MD-HTML-SPEC-SYNTHETIC",
        "path": path,
        "role": role,
        "authority_status": "canonical_markdown_source",
    }


def mermaid_html_row() -> dict[str, str]:
    return {
        "object_id": "HTML-SYNTHETIC",
        "path": "html/synthetic.html",
        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
    }


def flexible_spec_fields(
    *,
    profile: str = "workflow_lifecycle",
    layout_intent: str = "Use a synthetic source-backed test layout.",
    blocks: tuple[str, ...] = ("subject_summary", "synthetic_block"),
) -> str:
    block_lines = "".join(f'  - "{block}"\n' for block in blocks)
    return (
        f'presentation_profile: "{profile}"\n'
        f'layout_intent: "{layout_intent}"\n'
        "required_content_blocks:\n"
        f"{block_lines}"
    )


def flexible_required_blocks_section(
    blocks: tuple[str, ...] = ("subject_summary", "synthetic_block"),
) -> str:
    lines = "\n".join(
        f"- {block}: Synthetic block for structural evidence validation."
        for block in blocks
    )
    return f"## Required Content Blocks\n\n{lines}\n\n"


def synthetic_content_block(block_id: str = "synthetic_block", source_path: str = "README.md") -> str:
    return (
        f'<section data-content-block="{block_id}">'
        f'<span data-source-path="{source_path}"></span>'
        "</section>"
    )


def synthetic_subject_summary_block(source_path: str = "README.md") -> str:
    return (
        '<section data-content-block="subject_summary">'
        '<div data-summary-field="summary_text">Synthetic summary.</div>'
        '<div data-summary-field="source_basis">'
        f'<span data-source-path="{source_path}">{source_path}</span>'
        "</div>"
        "</section>"
    )


def valid_synthetic_spec_text() -> str:
    return (
        "---\n"
        'title: "Synthetic"\n'
        'purpose: "Test interaction markers."\n'
        'audience: "test"\n'
        'output_path: "html/synthetic.html"\n'
        'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
        "source_materials:\n"
        '  - "README.md"\n'
        'claim_boundary: "Human-only visualization."\n'
        "human_visual_only: true\n"
        "explainer_kind: \"workflow_process\"\n"
        "interaction_model: \"progressive_disclosure\"\n"
        "analysis_depth: \"deep\"\n"
        "required_controls:\n"
        "  - \"section_toc\"\n"
        "  - \"source_materials_section\"\n"
        "  - \"workflow_step_inspector\"\n"
        + flexible_spec_fields()
        + "---\n"
        "# Synthetic\n\n"
        + flexible_required_blocks_section()
    )


def valid_synthetic_html_text(content_block_html: str | None = None) -> str:
    if content_block_html is None:
        content_block_html = synthetic_subject_summary_block() + synthetic_content_block()
    return (
        '<!doctype html><meta name="aether-flow-source-basis" content="MD-HTML-SPEC-SYNTHETIC">'
        '<meta name="aether-flow-source-basis-hash" content="spec-hash">'
        '<meta name="aether-flow-human-visual-only" content="true">'
        "<style>"
        "p, td, th, .atlas-card { overflow-wrap: break-word; }"
        "code, pre { overflow-wrap: anywhere; }"
        ".card-grid { display: grid; }"
        ".layer .card-grid { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }"
        ".layer-strip { display: grid; grid-template-columns: 1fr; }"
        "</style>"
        f"{content_block_html}"
        '<nav data-explainer-control="section_toc"></nav>'
        '<section data-explainer-control="source_materials_section"></section>'
        '<ol data-explainer-control="workflow_step_inspector"></ol>'
        '<ul><li data-source-path="README.md"></li></ul>'
    )


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

    def test_github_facing_markdown_is_discovered_with_public_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/project-overview-explainer.md"
            spec.parent.mkdir(parents=True)
            spec.write_text("# Project Overview Spec\n", encoding="utf-8")
            page = root / "github-facing/project-overview-explainer.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Project Overview\n", encoding="utf-8")
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                rows = self.memory_system.discover_markdown_rows("2026-06-13T00:00:00Z")

        row_by_id = {row["object_id"]: row for row in rows}
        row = row_by_id["MD-GITHUB-FACING-PROJECT-OVERVIEW-EXPLAINER"]
        self.assertEqual(row["role"], "github_facing_documentation")
        self.assertEqual(row["authority_status"], "generated_noncanonical")
        self.assertEqual(row["audience"], "humans_and_agents")
        self.assertEqual(row["related_source"], "MD-HTML-SPEC-PROJECT-OVERVIEW-EXPLAINER")
        self.assertEqual(row["generated_from"], "MD-HTML-SPEC-PROJECT-OVERVIEW-EXPLAINER")
        self.assertEqual(row["owner_skill"], "documentation-curator")
        self.assertEqual(row["github_facing"], "true")
        self.assertEqual(row["agent_documentation"], "true")
        self.assertIn("non-authoritative for physics claims", row["notes"])

    def test_github_facing_markdown_stale_rows_are_pruned(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            registry_dir = root / "registries"
            registry_dir.mkdir(parents=True)
            registry_dir.joinpath("MARKDOWN_SOURCE_REGISTRY.csv").write_text(
                "object_id,path,format,role,authority_status,audience,source_hash,related_source,generated_from,generated_outputs,owner_skill,validation_status,last_validated_at,notes,github_facing,agent_documentation,contains_mermaid,contains_math\n"
                "MD-GITHUB-FACING-README,docs/github-facing/README.md,markdown,github_facing_documentation,canonical_markdown_source,humans_and_agents,old,,,,documentation-curator,PASS,2026-06-13T00:00:00Z,old,true,true,false,false\n",
                encoding="utf-8",
            )
            page = root / "github-facing/project-overview-explainer.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Project Overview Spec\n", encoding="utf-8")
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                rows = self.memory_system.merge_authored_registry(
                    "MARKDOWN_SOURCE_REGISTRY.csv",
                    self.memory_system.MARKDOWN_COLUMNS,
                    self.memory_system.discover_markdown_rows("2026-06-13T00:00:00Z"),
                    False,
                )

        object_ids = {row["object_id"] for row in rows}
        self.assertNotIn("MD-GITHUB-FACING-README", object_ids)
        self.assertIn("MD-GITHUB-FACING-PROJECT-OVERVIEW-EXPLAINER", object_ids)

    def test_stale_github_facing_generated_files_are_pruned(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            current_wiki = root / "wiki/markdown/md-github-facing-current.md"
            stale_wiki = root / "wiki/markdown/md-github-facing-stale.md"
            current_semantic = root / ".local/content_semantics/markdown/md-github-facing-current.txt"
            stale_semantic = root / ".local/content_semantics/markdown/md-github-facing-stale.txt"
            current_vault = root / ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-github-facing-current.md"
            stale_vault = root / ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-github-facing-stale.md"
            current_raw = root / ".local/obsidian/aether-flow-wiki/01_raw/markdown/md-github-facing-current.md"
            stale_raw = root / ".local/obsidian/aether-flow-wiki/01_raw/markdown/md-github-facing-stale.md"
            for path in [
                current_wiki,
                stale_wiki,
                current_semantic,
                stale_semantic,
                current_vault,
                stale_vault,
                current_raw,
                stale_raw,
            ]:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("generated\n", encoding="utf-8")

            rows_by_registry = {
                "WIKI_ARTIFACT_REGISTRY.csv": [{"path": "wiki/markdown/md-github-facing-current.md"}],
                "CONTENT_SEMANTIC_REGISTRY.csv": [
                    {"path": ".local/content_semantics/markdown/md-github-facing-current.txt"}
                ],
                "OBSIDIAN_VAULT_REGISTRY.csv": [
                    {
                        "path": ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-github-facing-current.md",
                        "vault_note_path": ".local/obsidian/aether-flow-wiki/02_sources/markdown/md-github-facing-current.md",
                        "vault_raw_path": ".local/obsidian/aether-flow-wiki/01_raw/markdown/md-github-facing-current.md",
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.prune_stale_github_facing_generated_files(rows_by_registry)

            self.assertTrue(current_wiki.exists())
            self.assertFalse(stale_wiki.exists())
            self.assertTrue(current_semantic.exists())
            self.assertFalse(stale_semantic.exists())
            self.assertTrue(current_vault.exists())
            self.assertFalse(stale_vault.exists())
            self.assertTrue(current_raw.exists())
            self.assertFalse(stale_raw.exists())

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

    def test_html_spec_contract_requires_interactive_analysis_fields(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/missing-interaction.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/missing-interaction.html").write_text(
                "<!doctype html>\n", encoding="utf-8"
            )
            spec.write_text(
                "---\n"
                'title: "Missing interaction"\n'
                'purpose: "Test interaction contract."\n'
                'audience: "test"\n'
                'output_path: "html/missing-interaction.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "---\n"
                "# Missing interaction\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-MISSING-INTERACTION",
                            "path": "markdown/html-explainer-specs/missing-interaction.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(any("missing required_controls" in error for error in report.errors))

    def test_html_specs_reject_removed_simple_deep_toggle(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/old-toggle.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Old Toggle"\n'
                'purpose: "Test removed simple/deep toggle."\n'
                'audience: "test"\n'
                'output_path: "html/old-toggle.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"project_overview\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"simple_and_deep\"\n"
                "required_controls:\n"
                "  - \"simple_deep_toggle\"\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                + flexible_spec_fields()
                + "---\n"
                "# Old Toggle\n\n"
                + flexible_required_blocks_section(),
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-OLD-TOGGLE",
                            "path": "markdown/html-explainer-specs/old-toggle.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(any("analysis_depth must be deep" in error for error in report.errors))
        self.assertTrue(any("unknown required_controls value" in error for error in report.errors))

    def test_html_specs_reject_obsolete_analysis_capsule_contract(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/obsolete-capsule.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/obsolete-capsule.html").write_text(
                "<!doctype html>\n", encoding="utf-8"
            )
            spec.write_text(
                "---\n"
                'title: "Obsolete Capsule"\n'
                'purpose: "Test obsolete capsule contract."\n'
                'audience: "test"\n'
                'output_path: "html/obsolete-capsule.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"conceptual_model\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"deep\"\n"
                "required_controls:\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                "analysis_capsule_schema:\n"
                "  - \"premise\"\n"
                + flexible_spec_fields()
                + "---\n"
                "# Obsolete Capsule\n\n"
                + flexible_required_blocks_section()
                + "## Required Analysis Capsules\n\n"
                "- premise: Test premise.\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-OBSOLETE-CAPSULE",
                            "path": "markdown/html-explainer-specs/obsolete-capsule.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(any("analysis_capsule_schema is obsolete" in error for error in report.errors))
        self.assertTrue(
            any("Required Analysis Capsules section is obsolete" in error for error in report.errors)
        )

    def test_html_spec_contract_requires_flexible_presentation_fields(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/bad-flex.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/bad-flex.html").write_text("<!doctype html>\n", encoding="utf-8")
            spec.write_text(
                "---\n"
                'title: "Bad Flex"\n'
                'purpose: "Test flexible contract."\n'
                'audience: "test"\n'
                'output_path: "html/bad-flex.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"conceptual_model\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"deep\"\n"
                "required_controls:\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                "presentation_profile: \"unknown_profile\"\n"
                "layout_intent: \"\"\n"
                "required_content_blocks:\n"
                "  - \"Bad-Block\"\n"
                "---\n"
                "# Bad Flex\n\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-BAD-FLEX",
                            "path": "markdown/html-explainer-specs/bad-flex.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(any("invalid presentation_profile" in error for error in report.errors))
        self.assertTrue(any("layout_intent must be nonblank" in error for error in report.errors))
        self.assertTrue(
            any("invalid required_content_blocks ID" in error for error in report.errors)
        )
        self.assertTrue(
            any("missing Required Content Blocks section" in error for error in report.errors)
        )

    def test_html_spec_contract_rejects_empty_content_blocks(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/empty-blocks.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/empty-blocks.html").write_text(
                "<!doctype html>\n", encoding="utf-8"
            )
            spec.write_text(
                "---\n"
                'title: "Empty Blocks"\n'
                'purpose: "Test required blocks."\n'
                'audience: "test"\n'
                'output_path: "html/empty-blocks.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"conceptual_model\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"deep\"\n"
                "required_controls:\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                "presentation_profile: \"conceptual_model\"\n"
                "layout_intent: \"Use a source-backed conceptual explanation.\"\n"
                "required_content_blocks:\n"
                "---\n"
                "# Empty Blocks\n\n"
                "## Required Content Blocks\n\n",
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-EMPTY-BLOCKS",
                            "path": "markdown/html-explainer-specs/empty-blocks.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(
            any("required_content_blocks must be a non-empty list" in error for error in report.errors)
        )

    def test_html_spec_contract_requires_subject_summary_first_block(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/missing-summary.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/missing-summary.html").write_text(
                "<!doctype html>\n", encoding="utf-8"
            )
            spec.write_text(
                valid_synthetic_spec_text()
                .replace("html/synthetic.html", "html/missing-summary.html")
                .replace(
                    flexible_spec_fields(),
                    flexible_spec_fields(blocks=("synthetic_block",)),
                )
                .replace(
                    flexible_required_blocks_section(),
                    flexible_required_blocks_section(blocks=("synthetic_block",)),
                ),
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-MISSING-SUMMARY",
                            "path": "markdown/html-explainer-specs/missing-summary.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(
            any(
                "first required_content_blocks value must be subject_summary" in error
                for error in report.errors
            )
        )
        self.assertTrue(
            any(
                "first Required Content Blocks definition must be subject_summary" in error
                for error in report.errors
            )
        )

    def test_html_spec_contract_requires_subject_summary_first_definition(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/wrong-body-order.md"
            spec.parent.mkdir(parents=True)
            (root / "html").mkdir()
            (root / "html/wrong-body-order.html").write_text(
                "<!doctype html>\n", encoding="utf-8"
            )
            spec.write_text(
                valid_synthetic_spec_text()
                .replace("html/synthetic.html", "html/wrong-body-order.html")
                .replace(
                    flexible_required_blocks_section(),
                    flexible_required_blocks_section(
                        blocks=("synthetic_block", "subject_summary")
                    ),
                ),
                encoding="utf-8",
            )
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_specs(
                    report,
                    [
                        {
                            "object_id": "MD-HTML-SPEC-WRONG-BODY-ORDER",
                            "path": "markdown/html-explainer-specs/wrong-body-order.md",
                            "role": "html_explainer_source_spec",
                        }
                    ],
                )
        self.assertTrue(
            any(
                "first Required Content Blocks definition must be subject_summary" in error
                for error in report.errors
            )
        )

    def test_html_registry_requires_declared_interactive_markers(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Synthetic"\n'
                'purpose: "Test interaction markers."\n'
                'audience: "test"\n'
                'output_path: "html/synthetic.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"workflow_process\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"deep\"\n"
                "required_controls:\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                "  - \"workflow_step_inspector\"\n"
                + flexible_spec_fields()
                + "---\n"
                "# Synthetic\n\n"
                + flexible_required_blocks_section(),
                encoding="utf-8",
            )
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                '<!doctype html><meta name="aether-flow-source-basis" content="MD-HTML-SPEC-SYNTHETIC">'
                '<meta name="aether-flow-source-basis-hash" content="spec-hash">'
                '<meta name="aether-flow-human-visual-only" content="true">'
                '<div data-explainer-control="section_toc"></div>',
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "missing HTML control marker source_materials_section" in error
                for error in report.errors
            )
        )
        self.assertTrue(
            any(
                "missing HTML control marker workflow_step_inspector" in error
                for error in report.errors
            )
        )

    def test_html_registry_requires_declared_content_block_marker(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(valid_synthetic_html_text(content_block_html=""), encoding="utf-8")
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "missing HTML content block marker synthetic_block" in error
                for error in report.errors
            )
        )

    def test_html_registry_requires_content_block_source_path_evidence(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text(
                    content_block_html='<section data-content-block="synthetic_block"></section>'
                ),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "content block synthetic_block missing source-path evidence" in error
                for error in report.errors
            )
        )

    def test_html_registry_requires_subject_summary_text_field(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            summary_without_text = (
                '<section data-content-block="subject_summary">'
                '<div data-summary-field="source_basis">'
                '<span data-source-path="README.md">README.md</span>'
                "</div>"
                "</section>"
            )
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text(
                    content_block_html=summary_without_text
                    + synthetic_content_block()
                ),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any("subject_summary missing summary field" in error for error in report.errors)
        )

    def test_html_registry_rejects_obsolete_subject_summary_heading(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text(
                    content_block_html=(
                        '<section data-content-block="subject_summary">'
                        "<h2>What This Explainer Describes</h2>"
                        + synthetic_subject_summary_block().replace(
                            '<section data-content-block="subject_summary">',
                            "",
                            1,
                        )
                    )
                    + synthetic_content_block()
                ),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "subject_summary uses obsolete visible label" in error
                for error in report.errors
            )
        )

    def test_html_registry_rejects_visible_file_metadata_chips(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html_text = valid_synthetic_html_text() + (
                '<aside class="meta-stack" aria-label="Page metadata">'
                "<strong>Layout intent</strong>"
                "</aside>"
            )
            html.write_text(html_text, encoding="utf-8")
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any("visible file metadata must not render" in error for error in report.errors)
        )

    def test_html_registry_rejects_removed_reader_toolbar_controls(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text()
                + '<button type="button" data-action="expand">Expand notes</button>'
                + '<button type="button" data-mode="simple">Simple view</button>',
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "removed reader toolbar control is still present" in error
                for error in report.errors
            )
        )

    def test_html_registry_rejects_obsolete_analysis_capsule_layer(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text()
                + '<section id="analysis" data-explainer-control="expandable_analysis_panels">'
                + '<p>Analysis capsules</p><h2>Claim-Aware Analysis</h2>'
                + '<article data-analysis-capsule="test"><div data-capsule-field="premise"></div></article>'
                + "</section>"
                + "<p>The legitimate claim is explanatory: this block may summarize existing source boundaries.</p>",
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any("analysis capsule section must not render" in error for error in report.errors)
        )
        self.assertTrue(
            any("content-block claim boilerplate must not render" in error for error in report.errors)
        )

    def test_html_registry_rejects_undeclared_subject_summary_source_path(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text(
                    content_block_html=synthetic_subject_summary_block(
                        "not-declared.md"
                    )
                    + synthetic_content_block()
                ),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "subject_summary cites undeclared source_materials" in error
                for error in report.errors
            )
        )

    def test_html_registry_requires_subject_summary_before_toc(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            summary = synthetic_subject_summary_block()
            block = synthetic_content_block()
            html_text = valid_synthetic_html_text(content_block_html=summary + block)
            html_text = html_text.replace(
                summary + block + '<nav data-explainer-control="section_toc"></nav>',
                '<nav data-explainer-control="section_toc"></nav>' + summary + block,
            )
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(html_text, encoding="utf-8")
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any("subject_summary must appear before section_toc" in error for error in report.errors)
        )

    def test_html_registry_requires_subject_summary_first_content_block(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(valid_synthetic_spec_text(), encoding="utf-8")
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                valid_synthetic_html_text(
                    content_block_html=synthetic_content_block()
                    + synthetic_subject_summary_block()
                ),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any(
                "first HTML content block marker must be subject_summary" in error
                for error in report.errors
            )
        )

    def test_html_registry_rejects_unreadable_three_layer_layout(self) -> None:
        report = self.memory_system.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            spec = root / "markdown/html-explainer-specs/synthetic.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(
                "---\n"
                'title: "Synthetic"\n'
                'purpose: "Test readable layout guard."\n'
                'audience: "test"\n'
                'output_path: "html/synthetic.html"\n'
                'renderer_skill: "visual-explainer@0.7.1-project-aether-flow"\n'
                "source_materials:\n"
                '  - "README.md"\n'
                'claim_boundary: "Human-only visualization."\n'
                "human_visual_only: true\n"
                "explainer_kind: \"project_overview\"\n"
                "interaction_model: \"progressive_disclosure\"\n"
                "analysis_depth: \"deep\"\n"
                "required_controls:\n"
                "  - \"section_toc\"\n"
                "  - \"source_materials_section\"\n"
                + flexible_spec_fields(profile="atlas_hub")
                + "---\n"
                "# Synthetic\n\n"
                + flexible_required_blocks_section(),
                encoding="utf-8",
            )
            html = root / "html/synthetic.html"
            html.parent.mkdir(parents=True)
            html.write_text(
                '<!doctype html><meta name="aether-flow-source-basis" content="MD-HTML-SPEC-SYNTHETIC">'
                '<meta name="aether-flow-source-basis-hash" content="spec-hash">'
                '<meta name="aether-flow-human-visual-only" content="true">'
                "<style>"
                "p, td, th, .atlas-card { overflow-wrap: anywhere; }"
                ".card-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }"
                ".layer-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }"
                "</style>"
                '<nav data-explainer-control="section_toc"></nav>'
                '<section data-explainer-control="source_materials_section"></section>'
                '<ul><li data-source-path="README.md"></li></ul>'
                + synthetic_content_block(),
                encoding="utf-8",
            )
            rows_by_registry = {
                "MARKDOWN_SOURCE_REGISTRY.csv": [
                    {
                        "object_id": "MD-HTML-SPEC-SYNTHETIC",
                        "path": "markdown/html-explainer-specs/synthetic.md",
                        "role": "html_explainer_source_spec",
                        "source_hash": "spec-hash",
                    }
                ],
                "HTML_EXPLAINER_REGISTRY.csv": [
                    {
                        "object_id": "HTML-SYNTHETIC",
                        "path": "html/synthetic.html",
                        "human_visual_only": "true",
                        "source_basis": "MD-HTML-SPEC-SYNTHETIC",
                        "source_basis_hash": "spec-hash",
                        "html_hash": self.memory_system.sha256_file(html),
                    }
                ],
            }
            with mock.patch.object(self.memory_system, "REPO_ROOT", root):
                self.memory_system.validate_html_registry(report, rows_by_registry)
        self.assertTrue(
            any("nested fixed three-column grids" in error for error in report.errors)
        )
        self.assertTrue(
            any("prose selector uses overflow-wrap:anywhere" in error for error in report.errors)
        )

    def test_html_registry_accepts_readable_three_layer_layout(self) -> None:
        report = self.memory_system.ValidationReport()
        html_text = (
            "<style>"
            "p, td, th, .atlas-card { overflow-wrap: break-word; }"
            "code, pre { overflow-wrap: anywhere; }"
            ".card-grid { display: grid; }"
            ".layer .card-grid { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }"
            ".layer-strip { display: grid; grid-template-columns: 1fr; }"
            "</style>"
        )
        self.memory_system.validate_html_layout_contract(report, "HTML-SYNTHETIC", html_text)
        self.assertEqual(report.errors, [])

    def test_html_registry_rejects_nonadaptive_mermaid_fit(self) -> None:
        report = self.memory_system.ValidationReport()
        html_text = (
            "<style>"
            ".mermaid-canvas svg { max-width: min(100%, 980px); height: auto; }"
            "</style>"
            '<div class="mermaid-canvas"><svg width="100%" style="max-width: 1200px;" viewBox="0 0 1200 400" data-mermaid-rendered="true"></svg></div>'
            "<script>"
            "const fit = () => { scale = 1; x = 0; y = 0; apply(); };"
            "</script>"
        )
        self.memory_system.validate_html_layout_contract(report, "HTML-SYNTHETIC", html_text)
        self.assertTrue(
            any("fixed max-width instead of adaptive viewBox fit" in error for error in report.errors)
        )
        self.assertTrue(
            any("missing adaptive fit helper readSvgNaturalSize" in error for error in report.errors)
        )
        self.assertTrue(
            any("missing explicit width and height" in error for error in report.errors)
        )
        self.assertTrue(
            any("retains root max-width style" in error for error in report.errors)
        )

    def test_html_registry_accepts_adaptive_mermaid_fit(self) -> None:
        report = self.memory_system.ValidationReport()
        html_text = (
            "<style>"
            ".mermaid-canvas svg { max-width: none; width: auto; height: auto; }"
            "</style>"
            '<div class="mermaid-canvas"><svg width="1200" height="400" viewBox="0 0 1200 400" data-mermaid-rendered="true"></svg></div>'
            "<script>"
            "function readSvgNaturalSize(svg) { return svg.viewBox.baseVal; }"
            "function setAdaptiveHeight() { return true; }"
            "function computeFit() { return { zoom: 1 }; }"
            "function setCanvasNaturalSize() { return true; }"
            "</script>"
        )
        self.memory_system.validate_html_layout_contract(report, "HTML-SYNTHETIC", html_text)
        self.assertEqual(report.errors, [])

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

    def test_mermaid_validator_accepts_declared_spec_and_matching_html(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root)
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertEqual(result.errors, [])

    def test_mermaid_validator_rejects_declared_id_missing_from_markdown(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root, include_block=False)
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [],
            )
        self.assertTrue(
            any("declared Mermaid ID missing from Markdown" in error for error in result.errors)
        )

    def test_mermaid_validator_rejects_html_source_parity_drift(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, source="flowchart TD\n  A[Source] --> C[Different]\n")
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("Mermaid source differs from Markdown" in error for error in result.errors))

    def test_mermaid_validator_rejects_tracked_html_cdn_import(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(
                root,
                runtime_script=(
                    '<script type="module">\n'
                    '  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";\n'
                    "</script>\n"
                ),
            )
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("remote URL" in error for error in result.errors))

    def test_mermaid_validator_rejects_tracked_html_bare_pre(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, extra_body='<pre class="mermaid">flowchart TD</pre>')
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("bare <pre" in error for error in result.errors))

    def test_mermaid_validator_rejects_missing_inline_svg(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, canvas_body="")
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("must embed exactly one inline SVG" in error for error in result.errors))

    def test_mermaid_validator_rejects_stale_render_hash(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, canvas_hash="stale")
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("data-render-source-sha256" in error for error in result.errors))

    def test_mermaid_validator_rejects_stale_svg_css_id_selector(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(
                root,
                canvas_body=(
                    '<svg id="mmd-authority-ladder-root-rewritten" width="100" height="40" viewBox="0 0 100 40" '
                    'data-mermaid-rendered="true" data-mermaid-diagram-id="authority-ladder">'
                    '<style>#mmd-authority-ladder-root .node rect{fill:#dfe8f2;}</style>'
                    '<g class="node"><rect id="mmd-authority-ladder-node"/></g></svg>'
                ),
            )
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("inline SVG style references missing id" in error for error in result.errors))

    def test_mermaid_validator_rejects_stale_zoom_label(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, zoom_label="Loading")
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("stale zoom label" in error for error in result.errors))

    def test_mermaid_validator_rejects_browser_runtime_markers(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(
                root,
                runtime_script=(
                    "<script>\n"
                    "  mermaid.initialize({ startOnLoad: false });\n"
                    "  mermaid.render('id', 'flowchart TD');\n"
                    "</script>\n"
                ),
            )
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(
            any("must not execute or import Mermaid in the browser" in error for error in result.errors)
        )

    def test_mermaid_validator_rejects_executable_script_literal_close_tags(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(
                root,
                runtime_script=(
                    "<script>\n"
                    "  const page = '<!doctype html><body></body></html>';\n"
                    "</script>\n"
                ),
            )
            result = validator.validate_mermaid_sources(
                root,
                [mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")],
                [mermaid_html_row()],
            )
        self.assertTrue(any("literal closing body/html tags" in error for error in result.errors))

    def test_mermaid_validator_accepts_ordinary_markdown_with_governed_id(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(
                root,
                path_text="markdown/ordinary.md",
                frontmatter=False,
            )
            result = validator.validate_mermaid_sources(
                root,
                [
                    {
                        "object_id": "MD-ORDINARY",
                        "path": "markdown/ordinary.md",
                        "role": "authored_markdown",
                        "authority_status": "canonical_markdown_source",
                    }
                ],
                [],
            )
        self.assertEqual(result.errors, [])

    def test_mermaid_validator_rejects_duplicate_id_in_markdown_source(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(
                root,
                duplicate_block=True,
                path_text="markdown/ordinary.md",
                frontmatter=False,
            )
            result = validator.validate_mermaid_sources(
                root,
                [
                    {
                        "object_id": "MD-ORDINARY",
                        "path": "markdown/ordinary.md",
                        "role": "authored_markdown",
                        "authority_status": "canonical_markdown_source",
                    }
                ],
                [],
            )
        self.assertTrue(any("duplicate Mermaid diagram ID authority-ladder" in error for error in result.errors))

    def test_mermaid_validator_rejects_governed_id_in_agents_markdown(self) -> None:
        validator = load_mermaid_validator()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root, path_text="AGENTS.md", frontmatter=False)
            result = validator.validate_mermaid_sources(
                root,
                [
                    {
                        "object_id": "MD-AGENTS",
                        "path": "AGENTS.md",
                        "role": "agent_guidance",
                        "authority_status": "project_control",
                    }
                ],
                [],
            )
        self.assertTrue(any("not allowed in AGENTS guidance" in error for error in result.errors))

    def test_validate_all_includes_mermaid_validation_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            write_mermaid_spec(root)
            write_governed_html(root, source="flowchart TD\n  A[Source] --> C[Different]\n")
            markdown_rows = [
                mermaid_markdown_row("markdown/html-explainer-specs/synthetic.md")
            ]
            html_rows = [mermaid_html_row()]

            def fake_read_csv_rows(path: Path) -> list[dict[str, str]]:
                if path.name == "MARKDOWN_SOURCE_REGISTRY.csv":
                    return markdown_rows
                if path.name == "HTML_EXPLAINER_REGISTRY.csv":
                    return html_rows
                return []

            with (
                mock.patch.object(self.memory_system, "REPO_ROOT", root),
                mock.patch.object(self.memory_system, "read_csv_rows", side_effect=fake_read_csv_rows),
                mock.patch.object(self.memory_system, "validate_columns"),
                mock.patch.object(self.memory_system, "validate_paths"),
                mock.patch.object(self.memory_system, "validate_source_hashes"),
                mock.patch.object(self.memory_system, "validate_tex_vocab"),
                mock.patch.object(self.memory_system, "validate_pdf_registry"),
                mock.patch.object(self.memory_system, "validate_html_specs"),
                mock.patch.object(self.memory_system, "validate_html_registry"),
                mock.patch.object(self.memory_system, "validate_wiki_registry"),
                mock.patch.object(self.memory_system, "validate_file_object_registry"),
                mock.patch.object(self.memory_system, "validate_folder_map"),
                mock.patch.object(self.memory_system, "validate_tracked_local_noise"),
            ):
                report = self.memory_system.validate_all()
        self.assertTrue(
            any("Mermaid:" in error and "source differs from Markdown" in error for error in report.errors)
        )

    def test_changed_spec_hash_updates_unchanged_html_registry_binding(self) -> None:
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
        self.assertEqual(rows[0]["source_basis_hash"], "new-spec-hash")

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
