---
title: "Roles And Skills"
purpose: "Catalog active registered roles, defined or superseded role states, repo-local governed skills, and evidence-labeled role/skill associations."
audience: "Technical but human-readable: maintainers, research agents, and reviewers who need to know which roles and repo-local skills govern current work."
output_path: "html/roles-and-skills-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - ".agents/roles/research_ops/director-of-research.v0.1.0.md"
  - ".agents/roles/research_ops/project-system-director.v0.1.0.md"
  - ".agents/roles/research_ops/project-control-maintainer.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.4.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.3.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.2.0.md"
  - ".agents/roles/research_ops/validator-engineer.v0.1.0.md"
  - ".agents/roles/research_ops/memory-system-maintainer.v0.1.0.md"
  - ".agents/roles/research_ops/process-integrity-auditor.v0.1.0.md"
  - ".agents/roles/physics/ontology-formalizer.v0.1.0.md"
  - ".agents/roles/physics/candidate-constructor.v0.1.0.md"
  - ".agents/roles/physics/refuter.v0.1.0.md"
  - ".agents/roles/physics/smuggling-auditor.v0.1.0.md"
  - ".agents/roles/physics/gate-chair.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.1.0.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/markdown-wiki/SKILL.md"
  - ".codex/skills/tex-wiki/SKILL.md"
  - ".codex/skills/pdf-derivative-build/SKILL.md"
  - ".codex/skills/obsidian-wiki/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md"
  - ".codex/skills/ontology-promotion/SKILL.md"
  - ".codex/skills/grill-me/SKILL.md"
claim_boundary: "Human-only role and skill catalog. It explains registered role status, repo-local skill contracts, and evidence-labeled support-skill associations without changing role authority, routing behavior, skill contracts, validator behavior, or scientific claim status."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "role_catalog"
layout_intent: "Use an active-first catalog with compact role cards, status bands, repo-local skill groups, and evidence-labeled declared versus likely support-skill associations."
required_controls:
  - "section_toc"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "active_role_catalog"
  - "status_defined_roles"
  - "superseded_audit_roles"
  - "repo_local_skill_catalog"
  - "declared_role_skill_evidence"
  - "inferred_support_skills"
  - "operator_context_boundary"
---

# Roles And Skills Spec

## Rendering Intent

Create a tracked HTML drilldown for registered roles and repo-local skills. The
page should be active-first: roles with `status: active` are the current
operating system and should visually dominate. Historical or paused roles must
remain visible for auditability but should not compete with active contracts.

Use these role status meanings:

- `active`: usable current role.
- `status_defined`: defined but human-gated or paused.
- `superseded`: preserved for old execution records, not used for new routing.

The main skill catalog covers repo-local governed skills only:
`continue-research`, `improve-project-system`, `project-memory-system`,
`markdown-wiki`, `tex-wiki`, `pdf-derivative-build`, `obsidian-wiki`,
`html-visual-explainer`, `visual-explainer`, `ontology-promotion`, `grill-me`,
and `mermaid-documentation`.

External Codex plugins, global user skills, bundled tools, and operator-local
helpers may be mentioned only in a clearly labeled operator-context note. They
are not project contract authority unless mirrored into `.codex/skills/`.

## Required Visual Structure

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Active-first role catalog with status badges.
- Separate audit appendix for `status_defined` and `superseded` roles.
- Repo-local skill catalog grouped by workflow, memory/wiki, visual
  explanation, research promotion, and grill/design support.
- Evidence-first role/skill association table. Declared associations should
  cite role contracts, registries, or skill contracts. Inferred associations
  must be labeled `likely support skill` and backed by source paths.
- Operator-context note separating project requirements from useful
  environment aids.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Source-Backed Summary

Summary heading: `Summary of Roles and Skills`

Summary text:

The roles-and-skills catalog is the active inventory of registered agent
roles, historical role versions, task-local execution overlays, and repo-local
skill front doors used by the project. Its function is to show which role
contracts currently govern work, which roles are status-defined or superseded
for audit history, which skills provide project-governed procedures, and which
tools are merely operator-context aids. This matters because skills are useful
only inside the right authority boundary: Documentation Curator can maintain
explanatory specs and source-backed HTML, Project-Control Maintainer owns
control contracts, Validator Engineer owns deterministic checks, and physics
roles remain separate from documentation work. The catalog fits the overall
system by giving maintainers a readable map from registry rows to role
contracts and skill procedures before they execute a task.

Summary source basis:

- `registries/AGENT_ROLE_REGISTRY.csv`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/roles/research_ops/documentation-curator.v0.4.0.md`
- `.codex/skills/html-visual-explainer/SKILL.md`

## Required Content Blocks

- subject_summary: Summarize the roles-and-skills catalog, its active-first role inventory, why skill/role boundaries matter, and which declared sources ground the summary.
- active_role_catalog: A primary catalog of current active roles, what each does, which authority lane it occupies, and which outputs or validators normally constrain it.
- status_defined_roles: A secondary section for defined but human-gated roles, especially Gate Chair authority, explaining why status-defined does not mean every agent may execute it autonomously.
- superseded_audit_roles: An audit-history section preserving superseded role contracts for provenance, historical execution records, and comparison without reactivating obsolete permissions.
- repo_local_skill_catalog: A grouped catalog of repo-local skills by continuation, project-system improvement, memory/wiki, HTML visual explanation, Mermaid rendering, PDF/TeX, ontology promotion, and design support.
- declared_role_skill_evidence: A source-backed evidence section showing declared role/skill relationships from role contracts, skill contracts, registries, and task overlays rather than inferred convenience.
- inferred_support_skills: A bounded support-skills section explaining when global or operator tools can help without becoming project authority or substituting for registered repo-local skills.
- operator_context_boundary: A visible boundary explaining that browser, editor, shell, and global Codex tools are operator context aids, while project authority remains in tracked sources, registries, and task records.
