---
title: "Role Routing Explainer"
purpose: "Explain how the project decides which AI agent role executes a bounded task, how the execution-role contract constrains that role, and how routing avoids authority drift."
audience: "Technical but human-readable: maintainers and research agents who need to understand role selection before executing or reviewing tasks."
output_path: "html/role-routing-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
claim_boundary: "Human-only role-routing visualization. It explains existing role selection and execution-role constraints without changing role authority, routing behavior, schemas, validators, or scientific claim status."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a routing lifecycle with decision-tree diagrams, role-contract panels, and evidence drilldowns that distinguish direct registered roles, task overlays, and one-job provisional roles."
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
  - "workflow_step_inspector"
required_content_blocks:
  - "authority_classification"
  - "director_routing"
  - "execution_role_contract"
  - "overlay_provisional_boundary"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
mermaid_diagrams:
  required: true
  ids:
    - "role-routing-decision-tree"
    - "execution-role-contract-map"
---

# Role Routing Explainer Spec

## Rendering Intent

Create a tracked HTML drilldown for role routing. The page should explain how
the Director chooses a role, how a role is bound to one task through an
execution-role record, and how the system distinguishes:

- registered role used directly,
- `task_overlay` for a bounded task-specific delta,
- `one_job_provisional_role` for a temporary role or distinct one-job identity.

The page must not change role contracts or routing rules.

## Required Visual Structure

- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Adaptive diagram fit: governed Mermaid diagram boxes must read the rendered
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
- Source drilldowns and claim-boundary inspection.

## Required Governed Mermaid Diagrams

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

## Required Content Blocks

- authority_classification: Explain how the task authority class separates
  science-bearing, project-system, documentation, validator, and memory work.
- director_routing: Explain how Director decisions bind a selected role to one
  bounded AgentJob.
- execution_role_contract: Explain task-local execution-role records,
  constraints, removed permissions, expanded permissions, and validator
  bindings.
- overlay_provisional_boundary: Explain when a task overlay or one-job
  provisional role is allowed and why repeated provisional patterns require
  review rather than silent promotion.

## Required Analysis Capsules

### Role Selection Is Authority Selection

- premise: Choosing a role is choosing the authority boundary for one bounded
  task.
- mechanism: The Director compares the task against registered role contracts,
  source classes, allowed writes, forbidden surfaces, validators, and claim
  boundaries before opening an AgentJob.
- source_basis: `research_control/README.md`,
  `registries/AGENT_ROLE_REGISTRY.csv`, and
  `registries/DIRECTOR_DECISION_REGISTRY.csv`.
- authority_status: Workflow explanation; it does not alter role authority.
- uncertainty: A role template may be close but not exact; the execution-role
  record is the job-specific contract.
- validation_or_test: Check the Director decision, execution-role record, and
  AgentJob allowlist.
- next_step: Inspect the task-local execution-role file before executing or
  reviewing work.

### Execution Role Prevents Drift

- premise: The execution-role record prevents a role from silently gaining or
  losing authority during a task.
- mechanism: It records whether the job uses a registered role, task overlay,
  or one-job provisional role, then binds added constraints, removed
  permissions, expanded permissions, allowed writes, human gates, and expiry.
- source_basis: `registries/ROLE_EXECUTION_REGISTRY.csv` and
  `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.
- authority_status: Project-control explanation.
- uncertainty: Repeated provisional patterns may indicate a role-design gap,
  but they do not become permanent by convention.
- validation_or_test: Validate role execution rows against task-local role
  records and AgentJob fields.
- next_step: Use the research-system explainer to see how the selected role
  executes inside the full task loop.

## Non-Goals

- Do not register new roles.
- Do not change role contracts, schemas, routing rules, or validators.
- Do not modify scientific claim status.
- Do not use external images or network-dependent assets.
