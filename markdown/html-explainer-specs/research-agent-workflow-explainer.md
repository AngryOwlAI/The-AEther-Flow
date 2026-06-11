---
title: "Research System Explainer"
purpose: "Show how the project research system uses Director decisions, AgentJobs, role contracts, validation, completions, registries, and handoffs to make theoretical work auditable."
audience: "Technical but human-readable: maintainers, research agents, and reviewers who need the operational model of the research system."
output_path: "html/research-agent-workflow-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - "registries/RESEARCH_TASK_REGISTRY.csv"
claim_boundary: "Human-only research-system visualization. It explains existing research-control and project-system workflow structure without changing routing behavior, role authority, validators, or physics claim status."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
  - "workflow_step_inspector"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "research_control/AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
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
    - "research-system-loop"
    - "agentjob-lifecycle"
---

# Research System Explainer Spec

## Rendering Intent

Create a tracked HTML drilldown for the project research system. The page
should describe the system as an operational discipline for theoretical work:
questions become bounded tasks, the Director selects role and boundary, an
AgentJob constrains allowed work, validators check outputs, completions record
results, and handoffs preserve the next state.

The page should keep two boundaries visible:

- `continue-research` is for physics continuation from tracked state.
- `improve-project-system` is for roles, validators, memory tooling, docs, and
  generated-doc pipelines.

## Required Visual Structure

- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- High-level model: why the research system exists and how it supports both
  physics and AI research-agent development.
- Operational model: Director -> AgentJob -> role execution -> validation ->
  completion -> handoff.
- Low-level evidence model: task directories, DDRs, AgentJob YAML, execution
  role records, completions, handoffs, and registries.
- Workflow step inspector for each operational step.
- Source drilldowns and claim-boundary inspection.

## Required Governed Mermaid Diagrams

<!-- mermaid-diagram-id: research-system-loop -->
```mermaid
flowchart TD
  State["Tracked state and latest handoff"] --> Director["Director decision"]
  Director --> Job["Bounded AgentJob"]
  Job --> Role["Execution role"]
  Role --> Outputs["Allowed outputs"]
  Outputs --> Validators["Validators and diff gates"]
  Validators --> Completion["Completion record"]
  Completion --> Handoff["Next handoff"]
  Handoff --> State
  Validators --> Registry["Registry updates"]
  Registry --> State
```

<!-- mermaid-diagram-id: agentjob-lifecycle -->
```mermaid
stateDiagram-v2
  [*] --> Proposed
  Proposed --> Active: Director selects role
  Active --> Executing: allowed reads and writes
  Executing --> Validating: outputs produced
  Validating --> Completed: validators pass
  Validating --> Blocked: validator or boundary failure
  Completed --> HandoffReady: completion recorded
  Blocked --> HandoffReady: obstruction recorded
  HandoffReady --> [*]
```

## Required Analysis Capsules

### Bounded Research Transaction

- premise: The research system advances through bounded transactions rather
  than open-ended editing.
- mechanism: A Director decision selects a role and objective; an AgentJob binds
  reads, writes, outputs, validators, and claim boundaries; completion and
  handoff records preserve the result.
- source_basis: `research_control/README.md`, `research_control/AGENTS.md`,
  `registries/AGENT_JOB_REGISTRY.csv`, and
  `registries/DIRECTOR_DECISION_REGISTRY.csv`.
- authority_status: Project-control explanation; it does not prove a physics
  result.
- uncertainty: A completed transaction may preserve progress, obstruction, or a
  negative result without establishing the broader theory.
- validation_or_test: Check task files, completion records, registry rows,
  validator receipts, and diff boundaries before accepting a transaction.
- next_step: Use the role-routing explainer to inspect how roles are selected
  and constrained.

### Two Continuation Modes

- premise: Physics continuation and project-system improvement are separate
  modes with different authority boundaries.
- mechanism: `continue-research` resolves tracked research state and may open
  one bounded physics AgentJob; `improve-project-system` handles roles,
  validators, docs, memory tooling, and generated-document pipelines.
- source_basis: `.codex/skills/continue-research/SKILL.md`,
  `.codex/skills/improve-project-system/SKILL.md`, and `AGENTS.md`.
- authority_status: Workflow explanation only.
- uncertainty: Project-system improvements can strengthen the research system
  without changing scientific claim status.
- validation_or_test: Verify skill, role, and claim-boundary rows for the
  selected mode.
- next_step: Keep workflow status separate from claim promotion.

## Non-Goals

- Do not add or modify workflow rules.
- Do not change role contracts, validators, schemas, or routing behavior.
- Do not promote project-system status to scientific evidence.
- Do not use external images or network-dependent assets.
