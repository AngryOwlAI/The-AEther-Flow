---
title: "Technical Requirements For Reproducible Operation"
purpose: "Explain the local tool tiers and command families needed to operate AEther-Flow reproducibly without treating tools, generated surfaces, or validator results as authority."
audience: "Maintainers, reviewers, future agents, operators, and external AI readers."
output_path: "html/technical-requirements-explainer.html"
github_markdown_output_path: "github-facing/technical-requirements-explainer.md"
wiki_output_path: "wiki/html/html-technical-requirements-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/technical-requirements.publication-brief.md"
document_type: "contributor_operator_guide"
visual_strategy: "annotated_table"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "requirements.txt"
  - "Makefile"
  - "scripts/README.md"
  - "tests/README.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
  - ".codex/skills/pdf-derivative-build/SKILL.md"
claim_boundary: "Human-only publication explainer for AEther-Flow technical requirements. It explains current local requirement tiers, Codex app harness assumptions, Python virtual environment setup, repository-owned command families, generated-memory refresh, screenshot QA, and PDF derivative build requirements without changing dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Technical Requirements Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/technical-requirements.publication-brief.md`
as the page-specific editorial contract. This page is a contributor/operator
guide. It explains the local technical tiers needed for reproducible
repository work, but it does not change those requirements or grant authority.

## Source Basis

- `README.md` supplies the current Codex app harness statement, Python
  environment instructions, requirement tiers, memory refresh commands,
  publication check command, smoke-test command, Obsidian sync command, and
  project-system workflow commands.
- `AGENTS.md` supplies the root authority hierarchy, generated-output
  boundaries, repository memory requirement, bootstrap and validate-only
  command expectations, and documentation-impact check requirement.
- `research_control/README.md` supplies research-control memory preflight,
  classification, resolver, documentation-impact, and research-control check
  command context.
- `requirements.txt` supplies the repository Python dependency ledger.
- `Makefile` supplies grouped local command targets such as `validate-memory`,
  `validate-project-control`, `validate-html-explainers`, and
  `audit-documentation-surfaces`.
- `scripts/README.md` explains script groups and the boundary between source
  scripts, generated outputs, and task-specific artifacts.
- `tests/README.md` explains unit-test coverage areas, command shape, and the
  fact that tests are evidence rather than independent scientific authority.
- `.codex/skills/project-memory-system/SKILL.md` defines bootstrap,
  validate-only, documentation publication check modes, and local-noise cleanup.
- `.codex/skills/improve-project-system/SKILL.md` defines the project-system
  improvement lane, memory preflight, classifier/resolver, signal validation,
  documentation-impact receipt, validation, and checkpoint expectations.
- `.codex/skills/html-visual-explainer/SKILL.md` defines the governed tracked
  HTML publication process, no-network HTML requirements, GitHub Markdown pair,
  and screenshot QA.
- `.codex/skills/visual-explainer/SKILL.md` defines project-local visual
  explainer constraints, tracked HTML governance, no external runtime, Mermaid
  build-time discipline, and screenshot review.
- `.codex/skills/pdf-derivative-build/SKILL.md` defines managed TeX-to-PDF
  derivative builds and their allowed output lanes.

## Required Reader Outcome

After reading, an operator should know which local tool tier is required for
the work at hand, which command family to inspect before running anything,
and why technical capability is not the same thing as authority. The reader
should also know that a missing convenience tool, a generated cache, or a
passing check cannot override registered sources, registries, task records,
role or skill contracts, AgentJob allowlists, completion evidence, or claim
boundaries.

## Visual Strategy

Use an annotated table as the primary visual: each row names a requirement
tier, its tools, its repository evidence, and what it does not authorize. Add
a compact operator sequence and a troubleshooting panel for missing
dependencies. Do not use a generic source-to-output diagram, browser-side
Mermaid execution, external runtime packages, remote fonts, remote CSS, or
tool-install buttons.

## Acceptance Criteria

- Explains requirement tiers for read-only inspection, governed Codex
  operation, Python validators, memory/wiki refresh, HTML screenshot QA, and
  PDF derivative work.
- Covers `.venv` usage, `requirements.txt`, Makefile targets, and
  repository-owned command families without changing them.
- Frames Node, npm, Playwright, and Mermaid as scoped to diagram and
  screenshot workflows.
- Frames Codex app as the current governed harness, not as scientific
  authority or permanent lock-in.
- Separates local retrieval and generated surfaces from canonical authority.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
