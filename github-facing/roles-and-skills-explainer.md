# Roles And Skills Catalog

The roles and skills catalog is a navigation aid. It helps a maintainer or future agent find the role registry, versioned role contracts, skill entry points, default validator families, and human-gate cautions. It does not decide live authority for a transaction.

Current authority is task-local. A registered role is a stable template; a skill contract defines a workflow; an execution-role record binds one job to exact semantics; the AgentJob allowlist defines what paths can be read or written; the claim boundary states what must not be promoted; and completion evidence plus validators record whether the bounded transaction passed.

That inspection order matters because public catalogs can become misleading when read as permission. Superseded roles remain for history, the Gate Chair remains human-gated, Documentation Curator output remains noncanonical for claims, and provisional or overlay roles do not become reusable just because a page describes them.

## Authority Inspection Order

| Item | Function | Boundary |
| --- | --- | --- |
| Role registry | Inspect identity, version, status, authority level, human-gate state, and defaults. | Registry row first. |
| Role or skill contract | Inspect the active contract text for mission and boundaries. | Versioned source, not public summary. |
| Execution-role record | Inspect task-local authority delta and allowed write paths. | One-job authority surface. |
| AgentJob | Inspect executable allowlist, expected outputs, validators, and claim boundary. | Actual transaction boundary. |
| Completion | Inspect output paths and command results. | Evidence, not broad authority. |

## Active Role Families

| Item | Function | Boundary |
| --- | --- | --- |
| Research routing | Director of Research and Project-System Director. | Route one bounded step; do not promote claims. |
| Physics drafts | Ontology Formalizer, Candidate Constructor, Refuter, Smuggling Auditor, Theoretical Continuation Selector. | Draft/control science work only. |
| Scientific gate | Gate Chair. | Human-gated and paused without explicit tracked approval. |
| Project system | Project-Control Maintainer, Validator Engineer, Memory-System Maintainer. | Project-control work; no physics claim promotion. |
| Public documentation | Documentation Curator. | Publication pages and generated HTML remain noncanonical. |

## Skill Workflow Map

| Item | Function | Boundary |
| --- | --- | --- |
| continue-research | Research-control continuation and physics AgentJobs. | Not project-system repair by default. |
| improve-project-system | Project-system classifier, resolver, signals, receipts, and one bounded AgentJob. | Not physics derivation. |
| project-memory-system | Bootstrap, validate-only, wiki, registry, and memory refresh. | Not source replacement. |
| html-visual-explainer | Governed tracked HTML and GitHub Markdown pair. | No direct HTML-only authority. |
| visual-explainer | Visual treatment for governed explainers. | No external runtime in tracked HTML. |

## Catalog Overreads

| Item | Function | Boundary |
| --- | --- | --- |
| Superseded role | Historical contracts remain visible. | Status field decides current role state. |
| Skill mention | A workflow entry point exists. | AgentJob allowlist still controls writes. |
| Gate Chair row | The role is defined. | Execution and promotion remain human-gated. |
| Public catalog | The page orients readers. | It cannot register or modify roles. |

## Reader Scope

Reader scope: role and skill navigation only. This page cannot change role status, register roles, supersede roles, expand role authority, change skill contracts, change validator behavior, change routing, change allowlists, or promote physics claims.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- **Related HTML:** `html/roles-and-skills-explainer.html`
- **Publication brief:** `markdown/publication-briefs/roles-and-skills.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains active and superseded role status, physics and research-ops role families, skill entry points, default validator families, human-gated roles, and source-inspection order without changing role status, registering roles, superseding roles, expanding role authority, changing skill contracts, changing validator behavior, changing routing behavior, changing AgentJob allowlists, changing checkpoint behavior, or promoting physics claims.

## Source Materials

- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv` [Role identity, version, status, authority, gates, output form, validators, and notes.]
- AEther-Flow Project. (2026). `.agents/roles/` [Versioned role contracts named by the role registry.]
- AEther-Flow Project. (2026). `.codex/skills/continue-research/SKILL.md` [Research-control continuation workflow.]
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system improvement workflow.]
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Memory, wiki, registry, and derivative refresh workflow.]
- AEther-Flow Project. (2026). `.codex/skills/html-visual-explainer/SKILL.md` [Governed tracked HTML publication workflow.]
- AEther-Flow Project. (2026). `.codex/skills/visual-explainer/SKILL.md` [Visual treatment and tracked-publication constraints.]

## Safe Operating Summary

Safe summary: Use this catalog to locate current registry rows, role contracts, skill contracts, execution records, AgentJobs, and completion evidence.

Unsafe summary: A catalog row grants write permission, a superseded role is active because it appears in a table, or a skill entry point bypasses the AgentJob allowlist.
