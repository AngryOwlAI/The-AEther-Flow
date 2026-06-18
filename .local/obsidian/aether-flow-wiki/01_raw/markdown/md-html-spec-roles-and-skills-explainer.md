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
  - ".agents/schemas/TEACHING_QA_PACKET_SCHEMA.md"
  - ".agents/roles/research_ops/director-of-research.v0.1.0.md"
  - ".agents/roles/research_ops/project-system-director.v0.1.0.md"
  - ".agents/roles/research_ops/project-control-maintainer.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.9.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.7.0.md"
  - ".agents/roles/research_ops/documentation-student.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-teacher.v0.1.0.md"
  - ".agents/roles/research_ops/validator-engineer.v0.1.0.md"
  - ".agents/roles/research_ops/memory-system-maintainer.v0.1.0.md"
  - ".agents/roles/research_ops/process-integrity-auditor.v0.1.0.md"
  - ".agents/roles/physics/ontology-formalizer.v0.1.0.md"
  - ".agents/roles/physics/candidate-constructor.v0.1.0.md"
  - ".agents/roles/physics/refuter.v0.1.0.md"
  - ".agents/roles/physics/smuggling-auditor.v0.1.0.md"
  - ".agents/roles/physics/gate-chair.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-curator.v0.1.0.md"
  - ".codex/skills/aether-teaching-explainer/SKILL.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/user-modified-project/SKILL.md"
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
  - ".codex/skills/grill-with-docs/SKILL.md"
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
`continue-research`, `improve-project-system`, `user-modified-project`,
`project-memory-system`, `markdown-wiki`, `tex-wiki`,
`pdf-derivative-build`, `obsidian-wiki`, `html-visual-explainer`,
`visual-explainer`, `aether-teaching-explainer`, `ontology-promotion`,
`grill-me`, `grill-with-docs`, and `mermaid-documentation`.

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

Summary heading: `Summary of Roles And Skills`

Summary text:

The roles-and-skills catalog is the active inventory of registered agent roles, historical role versions, task-local execution overlays, and repo-local skill front doors used by AEther-Flow. Its function is to show which role contracts currently govern work, which roles are status-defined or superseded for audit history, which support subroles may ask or answer teaching-loop questions, which skills provide project-governed procedures, and which tools are merely operator-context aids. This matters because skill availability is not project authority. Documentation Curator v0.9.0 owns subject-first explanatory specs, teaching packets, GitHub-facing Markdown, and source-backed HTML; Student and Teacher support the teaching loop without writing tracked docs; Project-Control Maintainer owns control contracts; Validator Engineer owns deterministic checks; physics roles remain separate from documentation and project-system work.

Summary source basis:

- `registries/AGENT_ROLE_REGISTRY.csv`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/roles/research_ops/documentation-curator.v0.9.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`


## Required Content Blocks

- subject_summary: A source-backed summary of Roles And Skills that directly explains the project subject, its functionality, why it matters, how it fits the physics or AI research-agent system, and its grounding source paths: `registries/AGENT_ROLE_REGISTRY.csv`, `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`, `.agents/roles/research_ops/documentation-curator.v0.9.0.md`, `.agents/roles/research_ops/documentation-student.v0.1.0.md`.
- active_role_catalog: A source-backed reader block on active roles that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `registries/AGENT_ROLE_REGISTRY.csv`, `.agents/roles/research_ops/documentation-curator.v0.9.0.md`.
- status_defined_roles: A source-backed reader block on status-defined roles that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `registries/AGENT_ROLE_REGISTRY.csv`, `.agents/roles/physics/gate-chair.v0.1.0.md`.
- superseded_audit_roles: A source-backed reader block on superseded roles that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `registries/AGENT_ROLE_REGISTRY.csv`, `registries/ROLE_EXECUTION_REGISTRY.csv`.
- repo_local_skill_catalog: A source-backed reader block on repo-local skills that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `.codex/skills/continue-research/SKILL.md`, `.codex/skills/improve-project-system/SKILL.md`, `.codex/skills/aether-teaching-explainer/SKILL.md`.
- declared_role_skill_evidence: A source-backed reader block on role-skill evidence that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `registries/AGENT_ROLE_REGISTRY.csv`, `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.
- inferred_support_skills: A source-backed reader block on support tools that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `AGENTS.md`, `registries/MARKDOWN_SOURCE_REGISTRY.csv`.
- operator_context_boundary: A source-backed reader block on operator boundary that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `AGENTS.md`, `research_control/README.md`.
