# Roles And Skills

Roles define who may do project work; skills define governed procedures for doing that work inside the repository.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- **Related HTML:** `html/roles-and-skills-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The roles-and-skills catalog is the active inventory of registered agent roles, historical role versions, task-local execution overlays, and repo-local skill front doors used by AEther-Flow. Its function is to show which role contracts currently govern work, which roles are status-defined or superseded for audit history, which support subroles may ask or answer teaching-loop questions, which skills provide project-governed procedures, and which tools are merely operator-context aids. This matters because skill availability is not project authority. Documentation Curator v0.9.0 owns subject-first explanatory specs, teaching packets, GitHub-facing Markdown, and source-backed HTML; Student and Teacher support the teaching loop without writing tracked docs; Project-Control Maintainer owns control contracts; Validator Engineer owns deterministic checks; physics roles remain separate from documentation and project-system work.

## What This Feature Does

Roles define authority and skills define governed workflows.

## Why The Project Needs It

The project needs the catalog because available tools and actual permission are different things.

## How It Works

The role registry lists active, status-defined, and superseded roles; execution-role records bind roles to tasks; repo-local skills define procedures for continuation, project-system improvement, memory, documentation, and teaching.

## What It Is Not

It is not a permission grant, not a role registration shortcut, not proof that global tools are project authority, and not a reason to reuse superseded permissions.

## Diagram Reading Guide

The useful structure is the active-role map, audit states, repo-local skill groups, and operator-context boundary.

## Source Authority

Authority comes from the agent role registry, execution-role registry, role contracts, schemas, and repo-local skill contracts.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize the feature for orientation
- identify source files to inspect next
- explain workflow boundaries in plain language

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this derivative as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Check the active role version before routing a job.
- Use repo-local skills for governed workflows.
- Treat external tools as operator aids unless registered.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`
- `.agents/roles/research_ops/director-of-research.v0.1.0.md`
- `.agents/roles/research_ops/project-system-director.v0.1.0.md`
- `.agents/roles/research_ops/project-control-maintainer.v0.1.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.9.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.7.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`
- `.agents/roles/research_ops/validator-engineer.v0.1.0.md`
- `.agents/roles/research_ops/memory-system-maintainer.v0.1.0.md`
- `.agents/roles/research_ops/process-integrity-auditor.v0.1.0.md`
- `.agents/roles/physics/ontology-formalizer.v0.1.0.md`
- `.agents/roles/physics/candidate-constructor.v0.1.0.md`
- `.agents/roles/physics/refuter.v0.1.0.md`
- `.agents/roles/physics/smuggling-auditor.v0.1.0.md`
- `.agents/roles/physics/gate-chair.v0.1.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.1.0.md`
- `.codex/skills/aether-teaching-explainer/SKILL.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/markdown-wiki/SKILL.md`
- `.codex/skills/tex-wiki/SKILL.md`
- `.codex/skills/pdf-derivative-build/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`
- `.codex/skills/ontology-promotion/SKILL.md`
- `.codex/skills/grill-me/SKILL.md`
- `.codex/skills/grill-with-docs/SKILL.md`
