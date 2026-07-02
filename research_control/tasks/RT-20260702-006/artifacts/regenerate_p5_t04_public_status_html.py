#!/usr/bin/env python3
"""Regenerate P5-T04 public-status HTML derivative content.

This task-local renderer patch applies exact source-spec-driven replacements
to the seven affected HTML derivatives. It fails closed if the expected
current derivative text is absent.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-006"
REPORT_PATH = TASK_DIR / "artifacts" / "p5_t04_regeneration_report.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def source_hash_from_spec(html_path: str) -> tuple[str, str]:
    spec_path = ROOT / "markdown" / "html-explainer-specs" / Path(html_path).name.replace(
        ".html", ".md"
    )
    spec_text = spec_path.read_text(encoding="utf-8")
    object_id = ""
    registry = (ROOT / "registries" / "MARKDOWN_SOURCE_REGISTRY.csv").read_text(
        encoding="utf-8"
    )
    for line in registry.splitlines():
        if f",{spec_path.relative_to(ROOT)}," in line:
            object_id = line.split(",", 1)[0]
            break
    return object_id, hashlib.sha256(spec_text.encode("utf-8")).hexdigest()


def assert_source_basis(html_path: str, text: str) -> dict[str, str]:
    expected_object, expected_hash = source_hash_from_spec(html_path)
    object_match = re.search(
        r'<meta name="aether-flow-source-basis" content="([^"]+)">', text
    )
    hash_match = re.search(
        r'<meta name="aether-flow-source-basis-hash" content="([^"]+)">', text
    )
    if not object_match or not hash_match:
        raise RuntimeError(f"{html_path}: missing source-basis metadata")
    actual_object = object_match.group(1)
    actual_hash = hash_match.group(1)
    if expected_object and actual_object != expected_object:
        raise RuntimeError(
            f"{html_path}: source-basis object mismatch {actual_object} != {expected_object}"
        )
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"{html_path}: source-basis hash mismatch {actual_hash} != {expected_hash}"
        )
    return {"source_basis": actual_object, "source_basis_hash": actual_hash}


def replace_once(text: str, old: str, new: str, html_path: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{html_path}: expected one {label!r} block, found {count}")
    return text.replace(old, new, 1)


REPLACEMENTS: dict[str, list[tuple[str, str, str]]] = {
    "html/project-overview-explainer.html": [
        (
            "nav-public-status",
            '      <a href="#path">Reading path</a>\n'
            '      <a href="#boundaries">Boundaries</a>\n',
            '      <a href="#path">Reading path</a>\n'
            '      <a href="#public-status">Public status</a>\n'
            '      <a href="#boundaries">Boundaries</a>\n',
        ),
        (
            "public-status-section",
            '    <section id="boundaries" aria-labelledby="boundaries-title">\n'
            '      <h2 id="boundaries-title">Boundaries To Preserve</h2>\n',
            '    <section id="public-status" aria-labelledby="public-status-title">\n'
            '      <h2 id="public-status-title">Public Status Boundary</h2>\n'
            '      <p>Use <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> before summarizing current public status. It preserves that GR is not derived; <code>M_src</code> is scoped source-only status; <code>g_eff</code> is scoped source-extension object status; matter coupling remains evidence/precondition status only; Einstein equations and benchmark promotion remain blocked.</p>\n'
            '      <ul class="boundary-list">\n'
            '        <li><code>M_src</code> is not a target manifold, metric, matter-coupling result, benchmark promotion, or completed derivation.</li>\n'
            '        <li><code>g_eff</code> is not an unscoped Lorentzian metric, matter-coupling result, Einstein-equation result, benchmark promotion, or completed derivation.</li>\n'
            '        <li>Matter-coupling evidence and preconditions do not adopt a coupling law, matter semantics, detector semantics, stress-energy semantics, or matter action.</li>\n'
            '        <li>Generated public pages render status for readers; they do not create source authority or scientific promotion.</li>\n'
            '      </ul>\n'
            '    </section>\n\n'
            '    <section id="boundaries" aria-labelledby="boundaries-title">\n'
            '      <h2 id="boundaries-title">Boundaries To Preserve</h2>\n',
        ),
        (
            "public-status-source",
            '        <article class="source-panel"><code data-source-path="research_control/design/documentation_curator_publication_process.md">research_control/design/documentation_curator_publication_process.md</code><p>Publication brief, source spec, GitHub Markdown, tracked HTML, review, and validation process.</p></article>\n'
            "      </div>\n",
            '        <article class="source-panel"><code data-source-path="research_control/design/documentation_curator_publication_process.md">research_control/design/documentation_curator_publication_process.md</code><p>Publication brief, source spec, GitHub Markdown, tracked HTML, review, and validation process.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code><p>Public status table contract for high-risk rows, blocked overreads, and generated-output non-authority.</p></article>\n'
            "      </div>\n",
        ),
    ],
    "html/aether-flow-physics-program-explainer.html": [
        (
            "public-status-path",
            '        <article class="source-panel">\n'
            "          <h3>Burden and claims</h3>\n"
            '          <p>Use <code>research_control/design/gr_derivation_burden_map.md</code> and <code>registries/CLAIM_BOUNDARY_REGISTRY.csv</code> before summarizing status.</p>\n'
            "        </article>\n"
            "      </div>\n"
            "    </section>\n\n"
            '    <section aria-labelledby="qualifiers-title">\n',
            '        <article class="source-panel">\n'
            "          <h3>Burden and claims</h3>\n"
            '          <p>Use <code>research_control/design/gr_derivation_burden_map.md</code> and <code>registries/CLAIM_BOUNDARY_REGISTRY.csv</code> before summarizing status.</p>\n'
            "        </article>\n"
            '        <article class="source-panel">\n'
            "          <h3>Public status table</h3>\n"
            '          <p>Use <code>research_control/design/public_status_table_source_spec.md</code> for current high-risk public rows and blocked overreads.</p>\n'
            "        </article>\n"
            "      </div>\n"
            "    </section>\n\n"
            '    <section aria-labelledby="qualifiers-title">\n',
        ),
        (
            "status-boundary-section",
            '    <section aria-labelledby="summaries-title">\n'
            '      <h2 id="summaries-title">Safe And Unsafe Summaries</h2>\n',
            '    <section aria-labelledby="public-status-title">\n'
            '      <h2 id="public-status-title">Current Public Status Rows</h2>\n'
            '      <div class="layers">\n'
            '        <div class="layer"><div class="label">GR derivation</div><div class="body">Not derived from source substrate in tracked state.</div><div class="boundary">No completed derivation, benchmark promotion, or Einstein-equation derivation follows from public documentation.</div></div>\n'
            '        <div class="layer"><div class="label"><code>M_src</code></div><div class="body">Scoped source-only status.</div><div class="boundary">Not a target manifold, metric, matter-coupling result, benchmark promotion, or completed derivation.</div></div>\n'
            '        <div class="layer"><div class="label"><code>g_eff</code></div><div class="body">Scoped source-extension object status.</div><div class="boundary">Not an unscoped Lorentzian metric, matter-coupling result, Einstein-equation result, benchmark promotion, or completed derivation.</div></div>\n'
            '        <div class="layer"><div class="label">Matter coupling</div><div class="body">Scoped evidence/preconditions exist, but matter coupling is not derived or adopted.</div><div class="boundary">No coupling-law adoption, matter semantics, detector semantics, stress-energy semantics, stress-energy tensor, or matter action.</div></div>\n'
            "      </div>\n"
            "    </section>\n\n"
            '    <section aria-labelledby="summaries-title">\n'
            '      <h2 id="summaries-title">Safe And Unsafe Summaries</h2>\n',
        ),
        (
            "public-status-source",
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</li>\n'
            '        <li>AEther-Flow Project. (2026). <code data-source-path="registries/CLAIM_BOUNDARY_REGISTRY.csv">registries/CLAIM_BOUNDARY_REGISTRY.csv</code> [Claim boundary registry].</li>\n',
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</li>\n'
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> [Public status table source spec].</li>\n'
            '        <li>AEther-Flow Project. (2026). <code data-source-path="registries/CLAIM_BOUNDARY_REGISTRY.csv">registries/CLAIM_BOUNDARY_REGISTRY.csv</code> [Claim boundary registry].</li>\n',
        ),
    ],
    "html/exact-gr-benchmark-boundary-explainer.html": [
        (
            "public-status-ladder",
            '        <article class="step">\n'
            '          <span class="tag">4</span>\n'
            '          <h3>Registered Markdown</h3>\n'
            '          <p><code>README.md</code>, <code>AGENTS.md</code>, and <code>ontology/aether-and-aether-flow.md</code> summarize and constrain the public framing.</p>\n'
            '        </article>\n'
            '        <article class="step">\n'
            '          <span class="tag">5</span>\n'
            '          <h3>Public Derivatives</h3>\n'
            '          <p>GitHub-facing Markdown and HTML explainers aid reading. They are not independent scientific authority.</p>\n'
            '        </article>\n',
            '        <article class="step">\n'
            '          <span class="tag">4</span>\n'
            '          <h3>Public Status Source</h3>\n'
            '          <p><code>research_control/design/public_status_table_source_spec.md</code> fixes high-risk public rows and blocked overreads.</p>\n'
            '        </article>\n'
            '        <article class="step">\n'
            '          <span class="tag">5</span>\n'
            '          <h3>Registered Markdown</h3>\n'
            '          <p><code>README.md</code>, <code>AGENTS.md</code>, and <code>ontology/aether-and-aether-flow.md</code> summarize and constrain the public framing.</p>\n'
            '        </article>\n'
            '        <article class="step">\n'
            '          <span class="tag">6</span>\n'
            '          <h3>Public Derivatives</h3>\n'
            '          <p>GitHub-facing Markdown and HTML explainers aid reading. They are not independent scientific authority.</p>\n'
            '        </article>\n',
        ),
        (
            "public-status-failure",
            '        <article class="failure danger">\n'
            "          <h3>Scoped obstruction becomes global rejection</h3>\n"
            "          <p>Unsafe: one blocked route rejects the ontology. Safe: scoped obstruction remains scoped unless a source authority says otherwise.</p>\n"
            "        </article>\n"
            "      </div>\n"
            "    </section>\n\n"
            '    <section aria-labelledby="sources-title" data-explainer-control="source_materials_section">\n',
            '        <article class="failure danger">\n'
            "          <h3>Scoped obstruction becomes global rejection</h3>\n"
            "          <p>Unsafe: one blocked route rejects the ontology. Safe: scoped obstruction remains scoped unless a source authority says otherwise.</p>\n"
            "        </article>\n"
            '        <article class="failure danger">\n'
            "          <h3>Public status becomes promotion</h3>\n"
            "          <p>Unsafe: scoped <code>M_src</code>, scoped <code>g_eff</code>, or matter-coupling evidence proves benchmark promotion. Safe: the public status table keeps those rows scoped and upstream burdens open.</p>\n"
            "        </article>\n"
            "      </div>\n"
            "    </section>\n\n"
            '    <section aria-labelledby="sources-title" data-explainer-control="source_materials_section">\n',
        ),
        (
            "public-status-source",
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</li>\n',
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</li>\n'
            '        <li>AEther-Flow Project. (2026). <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> [Public status table source spec].</li>\n',
        ),
    ],
    "html/gr-derivation-roadmap-explainer.html": [
        (
            "timeline-statuses",
            '        <div class="step">\n'
            "          <strong>M_src</strong>\n"
            "          <span>Source-manifold construction burden.</span>\n"
            '          <span class="chip draft">draft object exists</span>\n'
            "        </div>\n"
            '        <div class="step">\n'
            "          <strong>g_eff</strong>\n"
            "          <span>Effective metric law.</span>\n"
            '          <span class="chip blocked">not started</span>\n'
            "        </div>\n"
            '        <div class="step">\n'
            "          <strong>Matter coupling</strong>\n"
            "          <span>Universal same-metric coupling burden.</span>\n"
            '          <span class="chip blocked">not started</span>\n'
            "        </div>\n",
            '        <div class="step">\n'
            "          <strong>M_src</strong>\n"
            "          <span>Scoped source-only source-manifold status.</span>\n"
            '          <span class="chip draft">scoped source-only</span>\n'
            "        </div>\n"
            '        <div class="step">\n'
            "          <strong>g_eff</strong>\n"
            "          <span>Scoped source-extension object status; unscoped metric remains blocked.</span>\n"
            '          <span class="chip draft">source-extension</span>\n'
            "        </div>\n"
            '        <div class="step">\n'
            "          <strong>Matter coupling</strong>\n"
            "          <span>Scoped evidence/preconditions exist; derivation is not adopted.</span>\n"
            '          <span class="chip draft">preconditions only</span>\n'
            "        </div>\n",
        ),
        (
            "frontier-statuses",
            '          <p>Draft object exists through source-side interface work. Full <code>M_src</code> remains unadopted and cannot be used as a completed bridge.</p>\n',
            '          <p>Scoped source-only <code>M_src</code> status exists for the current public table. It is not a target manifold, metric, matter-coupling result, benchmark promotion, or completed derivation.</p>\n',
        ),
        (
            "downstream-burdens",
            '          <p><code>g_eff</code>, matter coupling, and Einstein equations remain not started in the ledger.</p>\n',
            '          <p><code>g_eff</code> has scoped source-extension object status; matter coupling remains scoped evidence/preconditions only; Einstein equations remain not started in the ledger.</p>\n',
        ),
        (
            "public-status-source",
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="registries/DISTANCE_TO_GR_LEDGER.csv">registries/DISTANCE_TO_GR_LEDGER.csv</code> [Distance-to-GR ledger].</div>\n',
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="registries/DISTANCE_TO_GR_LEDGER.csv">registries/DISTANCE_TO_GR_LEDGER.csv</code> [Distance-to-GR ledger].</div>\n'
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> [Public status table source spec].</div>\n',
        ),
        (
            "reader-scope",
            '      <p>Reader scope: roadmap explanation only. It does not update physics status, discharge a milestone, adopt <code>M_src</code>, derive <code>g_eff</code>, derive matter coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or supersede tracked source files.</p>\n',
            '      <p>Reader scope: roadmap explanation only. It does not update physics status, discharge a milestone, expand scoped <code>M_src</code> status, expand scoped <code>g_eff</code> status, derive matter coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or supersede tracked source files.</p>\n',
        ),
        (
            "footer-scope",
            '    <p>This HTML file is a generated noncanonical reader surface. It is derived from <code>markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md</code> and the publication brief <code>markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md</code>. It explains the roadmap, but it does not update physics status, discharge a milestone, adopt <code>M_src</code>, derive <code>g_eff</code>, derive matter coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, change source authority, or supersede tracked source files.</p>\n',
            '    <p>This HTML file is a generated noncanonical reader surface. It is derived from <code>markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md</code> and the publication brief <code>markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md</code>. It explains the roadmap, but it does not update physics status, discharge a milestone, expand scoped <code>M_src</code> status, expand scoped <code>g_eff</code> status, derive matter coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, change source authority, or supersede tracked source files.</p>\n',
        ),
    ],
    "html/claim-gates-explainer.html": [
        (
            "public-status-gates-section",
            '    <section id="gate-chair">\n'
            "      <h2>Gate Chair Remains Human-Gated</h2>\n",
            '    <section id="public-status-gates">\n'
            "      <h2>Public Status Gate Examples</h2>\n"
            '      <p><code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> gives the public high-risk rows. A scoped row can be accepted for public status without becoming downstream physics promotion.</p>\n'
            '      <table class="matrix">\n'
            "        <thead><tr><th>Scoped public row</th><th>Blocked overread</th></tr></thead>\n"
            "        <tbody>\n"
            "          <tr><td><code>M_src</code> is scoped source-only status.</td><td>Not a target manifold, metric, matter-coupling result, benchmark promotion, or completed derivation.</td></tr>\n"
            "          <tr><td><code>g_eff</code> is scoped source-extension object status.</td><td>Not an unscoped Lorentzian metric, matter-coupling result, Einstein-equation result, benchmark promotion, or completed derivation.</td></tr>\n"
            "          <tr><td>Matter-coupling evidence/preconditions are scoped.</td><td>No source-law adoption, coupling-law adoption, stress-energy semantics, matter action, or Einstein-equation derivation.</td></tr>\n"
            "        </tbody>\n"
            "      </table>\n"
            "    </section>\n\n"
            '    <section id="gate-chair">\n'
            "      <h2>Gate Chair Remains Human-Gated</h2>\n",
        ),
        (
            "public-status-source",
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</div>\n'
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="registries/CLAIM_BOUNDARY_REGISTRY.csv">registries/CLAIM_BOUNDARY_REGISTRY.csv</code> [Claim boundary registry].</div>\n',
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="research_control/design/gr_derivation_burden_map.md">research_control/design/gr_derivation_burden_map.md</code> [GR derivation burden map].</div>\n'
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code> [Public status table source spec].</div>\n'
            '        <div class="source">AEther-Flow Project. (2026). <code data-source-path="registries/CLAIM_BOUNDARY_REGISTRY.csv">registries/CLAIM_BOUNDARY_REGISTRY.csv</code> [Claim boundary registry].</div>\n',
        ),
    ],
    "html/source-authority-explainer.html": [
        (
            "public-status-checklist",
            "        <li>Preserve exact qualifiers.</li>\n"
            "      </ol>\n"
            "    </section>\n\n"
            '    <section id="failures" aria-labelledby="failures-title">\n',
            "        <li>Preserve exact qualifiers.</li>\n"
            "        <li>Trace public status renderings to the public status source spec, ledger row, and row-specific evidence path.</li>\n"
            "      </ol>\n"
            "    </section>\n\n"
            '    <section id="public-status-authority" aria-labelledby="public-status-authority-title">\n'
            '      <h2 id="public-status-authority-title">Public Status Source Chain</h2>\n'
            '      <p>Public status renderings must trace back to <code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code>, <code data-source-path="registries/DISTANCE_TO_GR_LEDGER.csv">registries/DISTANCE_TO_GR_LEDGER.csv</code>, and row-specific evidence paths before citing <code>M_src</code>, <code>g_eff</code>, matter-coupling evidence, Einstein-equation status, or benchmark status. HTML and GitHub-facing Markdown may render that status; they cannot override it.</p>\n'
            "    </section>\n\n"
            '    <section id="failures" aria-labelledby="failures-title">\n',
        ),
        (
            "public-status-source",
            '        <article class="source-panel"><code data-source-path="registries/HTML_EXPLAINER_REGISTRY.csv">registries/HTML_EXPLAINER_REGISTRY.csv</code><p>Generated HTML rows bound to source specs and source-basis hashes.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="registries/WIKI_ARTIFACT_REGISTRY.csv">registries/WIKI_ARTIFACT_REGISTRY.csv</code><p>Generated wiki-note rows and source-object hash bindings.</p></article>\n',
            '        <article class="source-panel"><code data-source-path="registries/HTML_EXPLAINER_REGISTRY.csv">registries/HTML_EXPLAINER_REGISTRY.csv</code><p>Generated HTML rows bound to source specs and source-basis hashes.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code><p>Canonical public status table source spec for high-risk public status renderings.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="registries/WIKI_ARTIFACT_REGISTRY.csv">registries/WIKI_ARTIFACT_REGISTRY.csv</code><p>Generated wiki-note rows and source-object hash bindings.</p></article>\n',
        ),
    ],
    "html/validator-operator-workflow-explainer.html": [
        (
            "pass-limits-public-status",
            '        <article class="ve-card"><strong>No broad promotion</strong><p>PASS does not promote physics claims, role authority, sidecar adoption, or generated outputs.</p><p>Human-gated authority remains protected.</p></article>\n',
            '        <article class="ve-card"><strong>No broad promotion</strong><p>PASS does not promote physics claims, role authority, sidecar adoption, or generated outputs.</p><p>Human-gated authority remains protected.</p></article>\n'
            '        <article class="ve-card"><strong>Public status checks</strong><p>Preserve <code>research_control/design/public_status_table_source_spec.md</code> boundaries.</p><p>PASS does not authorize source-law adoption, <code>g_eff</code> scope expansion, matter-coupling adoption, Einstein equations, benchmark promotion, or completed derivation.</p></article>\n',
        ),
        (
            "public-status-source",
            '        <article class="source-panel"><code data-source-path="scripts/research_control/validate_research_control.py">scripts/research_control/validate_research_control.py</code><p>Tracked research-control and diff boundary checks.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md">research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md</code><p>Phase 6 conditional sidecar checkpoint governance evidence.</p></article>\n',
            '        <article class="source-panel"><code data-source-path="scripts/research_control/validate_research_control.py">scripts/research_control/validate_research_control.py</code><p>Tracked research-control and diff boundary checks.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="research_control/design/public_status_table_source_spec.md">research_control/design/public_status_table_source_spec.md</code><p>Public status table source spec used by public-surface checks to separate validator receipts from physics-promotion authority.</p></article>\n'
            '        <article class="source-panel"><code data-source-path="research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md">research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md</code><p>Phase 6 conditional sidecar checkpoint governance evidence.</p></article>\n',
        ),
    ],
}


def main() -> None:
    report = {
        "task_id": "RT-20260702-006",
        "job_id": "AJ-RT-20260702-006-001",
        "mode": "exact_match_source_spec_derivative_regeneration",
        "html_derivatives": [],
    }
    for html_path, replacements in REPLACEMENTS.items():
        path = ROOT / html_path
        before = sha256(path)
        text = read(html_path)
        source_basis = assert_source_basis(html_path, text)
        labels = []
        for label, old, new in replacements:
            text = replace_once(text, old, new, html_path, label)
            labels.append(label)
        write(html_path, text)
        after = sha256(path)
        report["html_derivatives"].append(
            {
                "path": html_path,
                "before_hash": before,
                "after_hash": after,
                "changed": before != after,
                "replacement_labels": labels,
                **source_basis,
            }
        )
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
