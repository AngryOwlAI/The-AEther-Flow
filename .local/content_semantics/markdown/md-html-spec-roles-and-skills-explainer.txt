---
title: "Roles And Skills Explainer"
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
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
required_content_blocks:
  - "active_role_catalog"
  - "status_defined_roles"
  - "superseded_audit_roles"
  - "repo_local_skill_catalog"
  - "declared_role_skill_evidence"
  - "inferred_support_skills"
  - "operator_context_boundary"
source_drilldowns:
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - ".agents/roles/research_ops/documentation-curator.v0.2.0.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
---

# Roles And Skills Explainer Spec

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

- Active-first role catalog with status badges.
- Separate audit appendix for `status_defined` and `superseded` roles.
- Repo-local skill catalog grouped by workflow, memory/wiki, visual
  explanation, research promotion, and grill/design support.
- Evidence-first role/skill association table. Declared associations should
  cite role contracts, registries, or skill contracts. Inferred associations
  must be labeled `likely support skill` and backed by source paths.
- Operator-context note separating project requirements from useful
  environment aids.
- Source drilldowns and claim-boundary inspection.

## Required Content Blocks

- active_role_catalog: List current active roles, what each does, authority
  level, default validators, and role contract path.
- status_defined_roles: Explain defined but human-gated roles, especially Gate
  Chair, without routing new work to them automatically.
- superseded_audit_roles: Preserve superseded role contracts for audit history
  and old execution records.
- repo_local_skill_catalog: Explain governed repo-local skills and front doors
  only, with paths under `.codex/skills/`.
- declared_role_skill_evidence: Show declared role/skill relationships from
  role contracts, registry rows, and skill contracts.
- inferred_support_skills: Label inferred support skills as `likely support
  skill`, for example Documentation Curator with `html-visual-explainer`,
  `visual-explainer`, and `project-memory-system`.
- operator_context_boundary: Distinguish project-governed roles and skills
  from global Codex plugins, bundled tools, or machine-local operator aids.

## Required Analysis Capsules

### Active Roles Are The Operating System

- premise: Readers need the current role system before historical audit
  context.
- mechanism: The page should visually prioritize `active` rows in
  `AGENT_ROLE_REGISTRY.csv`, then place `status_defined` and `superseded`
  roles in separate bands.
- source_basis: `registries/AGENT_ROLE_REGISTRY.csv`, role contracts under
  `.agents/roles/`, and `registries/ROLE_EXECUTION_REGISTRY.csv`.
- authority_status: Human-only catalog; registries and role contracts carry
  project-control authority.
- uncertainty: A task-local execution-role overlay can narrow or expand a role
  only for one AgentJob.
- validation_or_test: Check the registry row, role contract path, task-local
  execution-role file, and AgentJob allowlist before executing work.
- next_step: Use the role-routing explainer to inspect how a role is selected
  for one task.

### Skills Are Repo-Local Contracts

- premise: The project can only govern skills tracked in `.codex/skills/`.
- mechanism: The catalog should list repo-local skill contracts as governed
  front doors, while labeling external/global tools as operator context only.
- source_basis: `.codex/skills/*/SKILL.md`,
  `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`,
  and `registries/MARKDOWN_SOURCE_REGISTRY.csv`.
- authority_status: Human-only explanation of skill contracts.
- uncertainty: A current Codex session may expose additional global skills or
  plugins that are useful but not durable repo requirements.
- validation_or_test: Confirm a skill path is tracked in the repository before
  treating it as project authority.
- next_step: Keep inferred support-skill associations explicitly labeled and
  source-backed.

## Non-Goals

- Do not register, remove, or supersede roles.
- Do not add or modify skill contracts.
- Do not treat external plugins or global skills as project authority.
- Do not change routing, validators, or scientific claim status.
