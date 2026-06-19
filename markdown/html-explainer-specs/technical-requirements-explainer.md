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
claim_boundary: "Human-only publication explainer for Technical Requirements For Reproducible Operation. It explains current local requirement tiers, Codex app harness assumptions, Python virtual environment setup, repository-owned command families, generated-memory refresh, screenshot QA, and PDF derivative build requirements without changing dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Technical Requirements For Reproducible Operation Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/technical-requirements.publication-brief.md` as the page-specific editorial contract. The page is a
contributor operator guide under the post-migration Phase 4 quality
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `README.md`: Codex app harness statement, Python environment, requirement tiers, and command families.
- `AGENTS.md`: Authority hierarchy, memory requirement, generated-output boundaries, and required checks.
- `research_control/README.md`: Memory preflight, classifier/resolver, documentation-impact, and research-control checks.
- `requirements.txt`: Repository Python dependency ledger.
- `Makefile`: Grouped local command targets.
- `scripts/README.md`: Script groups and script authority boundary.
- `tests/README.md`: Unit-test areas and commands.
- `.codex/skills/project-memory-system/SKILL.md`: Memory/wiki/registry refresh and validate-only modes.
- `.codex/skills/improve-project-system/SKILL.md`: Project-system workflow and checks.
- `.codex/skills/html-visual-explainer/SKILL.md`: Governed tracked HTML publication and screenshot QA.
- `.codex/skills/visual-explainer/SKILL.md`: Visual explainer constraints and no external runtime for tracked pages.
- `.codex/skills/pdf-derivative-build/SKILL.md`: Managed TeX-to-PDF derivative build lane.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Technical Requirements For Reproducible Operation function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Requirement Tier Matrix`, `Repository Command Families`, `Scoped Tooling`, `Tool Authority Boundary`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
