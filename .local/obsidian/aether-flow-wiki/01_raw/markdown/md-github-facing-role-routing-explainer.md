# Role Routing Spec

## Rendering Intent

Create a tracked HTML drilldown for role routing. The page should explain how
the Director chooses a role, how a role is bound to one task through an
execution-role record, and how the system distinguishes:

- registered role used directly,
- `task_overlay` for a bounded task-specific delta,
- `one_job_provisional_role` for a temporary role or distinct one-job identity.

The page must not change role contracts or routing rules.

## Required Visual Structure

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Adaptive diagram fit: diagram-backed boxes must read the rendered
  SVG viewBox, set the box height from diagram aspect ratio and available
  width within bounded min/max limits, and make Fit recompute that best-fit
  geometry so horizontal diagrams do not collapse to intrinsic SVG width.
- Three-layer readability: stack the high-level, operational, and evidence
  layer sections vertically; cards inside each layer must auto-fit at a
  readable minimum width rather than nesting fixed three-column grids.
- High-level model: why role routing exists.
- Operational model: problem type -> authority class -> role candidates ->
  selected role -> execution-role record -> AgentJob.
- Low-level evidence model: role registry, execution-role registry, Director
  decision registry, schema, and task-local role record.
- Workflow step inspector for role selection.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

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

## Source-Backed Summary

Summary heading: `Summary of Role Routing`

Summary text:

Role routing is the project's decision system for assigning bounded work to
the correct registered role or task-local execution overlay. Its functionality
is to connect task state, Director decisions, base role contracts, provisional
or overlay authority, and registry evidence so an agent knows who owns the
change, what paths may be written, which validators are required, and when the
job must stop. This matters because the repository contains physics roles,
documentation roles, validator roles, memory roles, and project-control roles
with different authority levels; collapsing them into one generic helper would
risk claim promotion, direct derivative edits, or untracked control changes.
Role routing fits the overall project by making authority selection itself
auditable before implementation begins.

Summary source basis:

- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`

## Required Content Blocks

- subject_summary: Summarize role routing as authority selection, why the project needs it, how it fits bounded AgentJobs, and which declared sources ground the summary.
- authority_classification: A completed explanation of how task authority class separates physics work, project-control maintenance, documentation curation, validation, memory maintenance, and process auditing before a role is selected.
- director_routing: A source-backed account of how Director decisions bind a selected role to one job, one claim boundary, allowed read and write paths, expected outputs, validators, and stop conditions.
- execution_role_contract: A detailed section on task-local execution-role records, role contracts, allowlists, removed permissions, expanded permissions, expiry, and validation evidence.
- overlay_provisional_boundary: A matrix explaining registered roles, task overlays, and one-job provisional roles, including why repeated provisional-role patterns must route to project-system review rather than silently becoming policy.
