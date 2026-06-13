---
title: "Research System"
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
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a workflow lifecycle with a concrete object-path trace, state diagrams, and evidence panels for task, AgentJob, role, artifact, completion, handoff, and registry records."
required_controls:
  - "section_toc"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "state_entry"
  - "director_decision"
  - "agentjob_lifecycle"
  - "role_execution"
  - "validation_completion_handoff"
  - "registry_update"
mermaid_diagrams:
  required: true
  ids:
    - "research-system-loop"
    - "agentjob-lifecycle"
---

# Research System Spec

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

The page should include a concrete object path for task execution:
`research_control/program_state.yaml` -> latest `handoff-*` -> Director
decision -> `00_TASK.yaml` -> `jobs/AJ-*.yaml` -> `roles/*.yaml` ->
`artifacts/*` -> completion YAML -> next handoff -> registries.

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
- High-level model: why the research system exists and how it supports both
  physics and AI research-agent development.
- Operational model: Director -> AgentJob -> role execution -> validation ->
  completion -> handoff.
- Low-level evidence model: task directories, DDRs, AgentJob YAML, execution
  role records, completions, handoffs, and registries.
- Concrete trace: show the file/path lifecycle from `program_state.yaml` and a
  latest handoff through task YAML, job YAML, role YAML, artifacts,
  completion, next handoff, and registry updates.
- Workflow step inspector for each operational step.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

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

## Source-Backed Summary

Summary heading: `Summary of Research System`

Summary text:

The research system is the governed workflow that turns a question,
continuation state, or project-improvement signal into bounded agent work with
explicit roles, decisions, registries, and validation. Its functionality is to
separate physics continuation from project-system maintenance, resolve tracked
state before acting, assign one bounded AgentJob, constrain that job with role
authority and allowlists, and preserve completion evidence for the next
handoff. This matters because the repository is not an informal chat log or
autonomous proof engine; it is a controlled research program where claims,
refutations, repairs, generated derivatives, and negative results must remain
auditable. The workflow fits the larger project by making research progress
reproducible without allowing workflow completion to stand in for scientific
acceptance.

Summary source basis:

- `research_control/AGENTS.md`
- `research_control/README.md`
- `.codex/skills/continue-research/SKILL.md`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`

## Required Content Blocks

- subject_summary: Summarize the research-agent workflow, its lifecycle function, why bounded execution matters, and which declared control sources ground the summary.
- state_entry: A completed lifecycle entry section covering tracked program state, latest handoffs, task files, and why local scratch context cannot override tracked control state.
- director_decision: A source-backed account of how a Director decision selects one role, one bounded objective, claim boundaries, allowed paths, validators, and stop conditions before execution begins.
- agentjob_lifecycle: A detailed explanation of `00_TASK.yaml`, `jobs/AJ-*.yaml`, task-local role overlays, allowed writes, expected outputs, and why one bounded AgentJob is the unit of accountable work.
- role_execution: A documentation section explaining registered roles, task overlays, provisional roles, role authority, removed or expanded permissions, expiry, and validator evidence.
- validation_completion_handoff: A completed validation story from command execution through completion YAML, validation status, documentation impact, and next handoff without implying scientific acceptance.
- registry_update: A source-backed section explaining how task, Director decision, AgentJob, role execution, claim boundary, Markdown, HTML, and generated-output registries preserve provenance and queryable memory.
