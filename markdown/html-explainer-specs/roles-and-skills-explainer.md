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
claim_boundary: "Human-only publication explainer for the AEther-Flow roles and skills catalog. It explains active and superseded role status, physics and research-ops role families, skill entry points, default validator families, human-gated roles, and source-inspection order without changing role status, registering roles, superseding roles, expanding role authority, changing skill contracts, changing validator behavior, changing routing behavior, changing AgentJob allowlists, changing checkpoint behavior, or promoting physics claims."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Roles And Skills Catalog Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/roles-and-skills.publication-brief.md` as
the page-specific editorial contract. This page is a reference catalog. It
helps readers find role and skill authority surfaces; it does not replace
`registries/AGENT_ROLE_REGISTRY.csv`, role contracts, skill contracts,
execution-role records, or AgentJob allowlists.

## Source Basis

- `registries/AGENT_ROLE_REGISTRY.csv` supplies role identity, version, role
  kind, contract path, authority level, status, autonomy fields, output form,
  default validators, human-gate status, and notes.
- `.agents/roles/` contains the versioned role contracts named by the role
  registry. Active role contracts describe current role missions and
  boundaries; superseded versions remain historical support for old execution
  records.
- `.codex/skills/continue-research/SKILL.md` defines research-control
  continuation, Director routing, one bounded AgentJob per invocation, memory
  preflight, execution-role records, parent-child synthesis, and checkpoint
  discipline.
- `.codex/skills/improve-project-system/SKILL.md` defines the project-system
  improvement lane, classifier and resolver usage, signal handling, one
  bounded AgentJob, documentation-impact requirements, validation, and
  checkpointing.
- `.codex/skills/project-memory-system/SKILL.md` defines bootstrap,
  validate-only, documentation publication validation modes, and local-noise
  cleanup for registry, wiki, memory, and derivative refresh.
- `.codex/skills/html-visual-explainer/SKILL.md` defines governed tracked
  HTML requirements, publication-brief binding, source-spec fields,
  no-network boundaries, GitHub Markdown pairing, validation, and screenshot
  QA.
- `.codex/skills/visual-explainer/SKILL.md` defines the visual explainer
  rendering discipline for governed Documentation Curator pages, including
  source-first HTML, source grounding, no external runtime for tracked HTML,
  role matrices, annotated tables, and screenshot review.

## Required Reader Outcome

After reading, an operator should know that `AGENT_ROLE_REGISTRY.csv` is the
role catalog authority, role contracts are versioned control templates, and
skill contracts define workflow procedures. The reader should also know that
actual current authority for one transaction still comes from the
execution-role record, the AgentJob allowlist, the claim boundary, completion
evidence, and validators.

## Visual Strategy

Use a static role matrix grouped by active physics roles, active research-ops
roles, and human-gated status. Use a compact superseded-role panel so
historical contracts are not mistaken for active roles. Add a skill-to-workflow
map and validator-family map. Do not include browser-side search, external
runtime packages, or any role-registration controls.

## Acceptance Criteria

- Explains active versus superseded role status.
- Separates physics roles, research-ops roles, and the human-gated Gate Chair.
- Maps skill entry points to owned workflow lanes.
- Explains default validators by role family without changing any validator.
- States where real authority lives.
- States why the page is a navigation catalog only.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
