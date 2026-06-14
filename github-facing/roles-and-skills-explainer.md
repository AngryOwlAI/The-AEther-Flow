# Roles And Skills

This page catalogs current roles, historical role states, repo-local skills, and the boundary between project authority and operator tools.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- **Related HTML:** `html/roles-and-skills-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The roles-and-skills catalog is the active inventory of registered agent roles, historical role versions, task-local execution overlays, and repo-local skill front doors used by the project. Its function is to show which role contracts currently govern work, which roles are status-defined or superseded for audit history, which skills provide project-governed procedures, and which tools are merely operator-context aids. This matters because skills are useful only inside the right authority boundary: Documentation Curator can maintain explanatory specs and source-backed HTML, Project-Control Maintainer owns control contracts, Validator Engineer owns deterministic checks, and physics roles remain separate from documentation work. The catalog fits the overall system by giving maintainers a readable map from registry rows to role contracts and skill procedures before they execute a task.

## What This Feature Does

The catalog is active-first: active registered roles are the current operating surface, status-defined roles remain paused or human-gated, and superseded roles remain audit history. Repo-local skills are governed procedures under `.codex/skills/`.

## Why The Project Needs It

A tool can help without owning authority. External plugins, browser automation, shell commands, and global user skills are operator context unless their contract is mirrored into this repository. The catalog prevents accidental authority from convenience.

## How It Works

Active role map:

| Role group | Examples | Owns |
| --- | --- | --- |
| Routing/control | Director of Research, Project-System Director | bounded decisions and project-system routing |
| Project maintenance | Project-Control Maintainer, Validator Engineer, Memory-System Maintainer | control contracts, checks, memory tooling |
| Documentation | Documentation Curator | explanatory Markdown, source specs, source-backed HTML derivatives |
| Physics work | Ontology Formalizer, Candidate Constructor, Refuter, Smuggling Auditor | science drafts, candidate construction, obstruction preservation |
| Human-gated | Gate Chair | promotion decisions only when explicitly authorized |

Repo-local skills include `continue-research`, `improve-project-system`, `project-memory-system`, `markdown-wiki`, `tex-wiki`, `pdf-derivative-build`, `obsidian-wiki`, `html-visual-explainer`, `visual-explainer`, `ontology-promotion`, `grill-me`, and Mermaid documentation support.

## What It Is Not

It is not a role registration change, not a permission grant, not proof that a global tool is project authority, and not a reason to reuse superseded role permissions for new work.

## Diagram Reading Guide

The current source spec does not declare a Mermaid diagram. Read the tables as the visual guide: active roles dominate, status-defined roles are paused or gated, superseded roles are provenance, and operator tools remain outside project authority.

No Mermaid diagram is declared in the current registered source spec for this page.

## Source Authority

The catalog is grounded in the agent role registry, role execution registry, Markdown source registry, execution-role schema, role contracts, and repo-local skill contracts.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Check `registries/AGENT_ROLE_REGISTRY.csv` before selecting a role.
- Check the task-local execution role before writing.
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
- `.agents/roles/research_ops/director-of-research.v0.1.0.md`
- `.agents/roles/research_ops/project-system-director.v0.1.0.md`
- `.agents/roles/research_ops/project-control-maintainer.v0.1.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.4.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.3.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.2.0.md`
- `.agents/roles/research_ops/validator-engineer.v0.1.0.md`
- `.agents/roles/research_ops/memory-system-maintainer.v0.1.0.md`
- `.agents/roles/research_ops/process-integrity-auditor.v0.1.0.md`
- `.agents/roles/physics/ontology-formalizer.v0.1.0.md`
- `.agents/roles/physics/candidate-constructor.v0.1.0.md`
- `.agents/roles/physics/refuter.v0.1.0.md`
- `.agents/roles/physics/smuggling-auditor.v0.1.0.md`
- `.agents/roles/physics/gate-chair.v0.1.0.md`
- `.agents/roles/research_ops/documentation-curator.v0.1.0.md`
- `.codex/skills/continue-research/SKILL.md`
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
