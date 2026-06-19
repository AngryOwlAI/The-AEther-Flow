---
title: "Roles And Skills Catalog"
purpose: "Explain how AEther-Flow active roles, superseded role versions, human-gated roles, and skill entry points should be navigated without treating the catalog as execution authority."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/roles-and-skills-explainer.html"
github_markdown_output_path: "github-facing/roles-and-skills-explainer.md"
wiki_output_path: "wiki/html/html-roles-and-skills-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/roles-and-skills.publication-brief.md"
document_type: "reference_catalog"
visual_strategy: "role_matrix"
migration_status: "reviewed"
source_materials:
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - ".agents/roles/"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
claim_boundary: "Human-only publication explainer for Roles And Skills Catalog. It explains active and superseded role status, physics and research-ops role families, skill entry points, default validator families, human-gated roles, and source-inspection order without changing role status, registering roles, superseding roles, expanding role authority, changing skill contracts, changing validator behavior, changing routing behavior, changing AgentJob allowlists, changing checkpoint behavior, or promoting physics claims."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Roles And Skills Catalog Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/roles-and-skills.publication-brief.md` as the page-specific editorial contract. The page is a
reference catalog under the post-migration Phase 4 quality
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `registries/AGENT_ROLE_REGISTRY.csv`: Role identity, version, status, authority, gates, output form, validators, and notes.
- `.agents/roles/`: Versioned role contracts named by the role registry.
- `.codex/skills/continue-research/SKILL.md`: Research-control continuation workflow.
- `.codex/skills/improve-project-system/SKILL.md`: Project-system improvement workflow.
- `.codex/skills/project-memory-system/SKILL.md`: Memory, wiki, registry, and derivative refresh workflow.
- `.codex/skills/html-visual-explainer/SKILL.md`: Governed tracked HTML publication workflow.
- `.codex/skills/visual-explainer/SKILL.md`: Visual treatment and tracked-publication constraints.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Roles And Skills Catalog function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Authority Inspection Order`, `Active Role Families`, `Skill Workflow Map`, `Catalog Overreads`. The HTML derivative may render these
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
