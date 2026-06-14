# Role Routing

This page explains how the project decides which role may execute a bounded task and how that role is constrained for one job.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/role-routing-explainer.md`
- **Related HTML:** `html/role-routing-explainer.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

Role routing maps a request to an authority class, compares candidate roles, records a Director decision, and binds execution to a registered role, task overlay, or one-job provisional role.

## Why The Project Needs It

A generic helper role is dangerous here because documentation, validators, memory tooling, control contracts, physics drafts, smuggling audits, and Gate Chair decisions have different authority. Routing keeps those lanes separate.

## How It Works

Routing asks four questions:

1. Is the work science-bearing, project-control, documentation, validation, memory, or process repair?
2. Does a registered role fit without permission changes?
3. If not, is a task overlay sufficient for one bounded delta?
4. If a one-job provisional role is used repeatedly, should Project-System Director review it for human-authorized registration?

The execution-role record then names allowed writes, removed permissions, expanded permissions, validators, expiry, and the AgentJob boundary.

## What It Is Not

It is not a way to silently expand role authority, not a permanent-role registration shortcut, not a Gate Chair substitute, and not permission to ignore the AgentJob allowlist.

## Diagram Reading Guide

The decision tree starts with authority classification and routes to science, project-system, or documentation roles. The contract map shows that direct roles, overlays, and provisional roles all terminate in a task-local execution-role record.

<!-- mermaid-diagram-id: role-routing-decision-tree -->
```mermaid
flowchart TD
  Request["Task request or handoff"] --> Authority["Identify authority class"]
  Authority --> Science["Science-bearing work"]
  Authority --> ProjectSystem["Project-system work"]
  Authority --> Docs["Explanatory documentation"]
  Science --> ScienceRoles["Ontology Formalizer<br/>Candidate Constructor<br/>Refuter<br/>Smuggling Auditor<br/>Gate Chair"]
  ProjectSystem --> OpsRoles["Project-System Director<br/>Project-Control Maintainer<br/>Validator Engineer<br/>Memory-System Maintainer"]
  Docs --> Curator["Documentation Curator"]
  ScienceRoles --> Director["Director decision"]
  OpsRoles --> Director
  Curator --> Director
  Director --> AgentJob["Bounded AgentJob"]
```

<!-- mermaid-diagram-id: execution-role-contract-map -->
```mermaid
flowchart TD
  Registered["Registered role template"] --> Fit{"Fits without change?"}
  Fit -->|"yes"| Direct["registered_role"]
  Fit -->|"needs bounded delta"| Overlay["task_overlay"]
  Fit -->|"new one-job identity"| Provisional["one_job_provisional_role"]
  Direct --> Execution["Execution-role record"]
  Overlay --> Execution
  Provisional --> Execution
  Execution --> Allowed["Allowed writes and validators"]
  Execution --> Removed["Removed permissions"]
  Execution --> Expanded["Explicit expansions"]
  Execution --> Expiry["Expires after AgentJob"]
  Allowed --> Job["AgentJob boundary"]
```

## Source Authority

The role registry, role execution registry, Director decision registry, scoped research-control guidance, and execution-role schema define the authority evidence. This page explains those rows but does not amend them.

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

- Read `registries/AGENT_ROLE_REGISTRY.csv` for active role status.
- Read the task-local `roles/*.yaml` before executing a job.
- Read roles-and-skills for the active catalog.
- Use improve-project-system for routing ambiguity.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
