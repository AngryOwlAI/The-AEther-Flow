---
title: "Research-Agent Workflow Explainer"
purpose: "Show how Director decisions, AgentJobs, role execution records, claim boundaries, validation, and handoffs organize bounded theoretical-physics research work."
audience: "Project maintainers, research agents, and reviewers who need a human-readable view of the research-agent workflow."
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
claim_boundary: "Human-only workflow visualization. It explains existing research-control and project-system workflow structure without changing routing behavior, role authority, validators, or physics claim status."
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
---

# Research-Agent Workflow Explainer Spec

## Rendering Intent

Create a self-contained HTML explainer that shows the operational loop used by
the project. The page should make bounded execution, validation, and authority
separation clear to human readers.

## Required Visual Structure

- A Director-to-AgentJob flow with decision, role selection, allowed writes,
  outputs, completion, validation, and handoff.
- A two-lane split between `continue-research` for physics work and
  `improve-project-system` for roles, validators, memory tooling, and docs.
- A role boundary panel showing that workflow status is not physics proof.
- A staged-autonomy harness panel explaining that the system is developed by
  doing real physics/math research under human accountability and deterministic
  validation.
- A validation gate showing bootstrap, documentation-impact validation,
  project-improvement signal validation, research-control validation, tests,
  and diff checks.
- Expandable source drilldowns that state why each cited source matters and
  what workflow, role, or validation boundary it checks.
- A claim-boundary notice stating that this page is human-only and
  non-authoritative.
- Deep-first progressive-disclosure controls for expandable analysis capsules,
  source drilldowns, claim-boundary inspection, and a workflow step inspector.

## Required Analysis Capsules

### Bounded AgentJob Loop

- premise: The research-agent workflow advances through one bounded job at a
  time.
- mechanism: Director decisions select a role and job boundary; AgentJobs bind
  allowed reads, writes, outputs, validators, and handoff expectations.
- source_basis: `research_control/README.md`, `research_control/AGENTS.md`,
  and the AgentJob and Director registries.
- authority_status: Project-control explanation; it does not prove a physics
  result.
- uncertainty: A completed workflow step may preserve progress, obstruction, or
  negative result without establishing the broader theory.
- validation_or_test: Check completion records, registry rows, validators, and
  diff checks before accepting a workflow transaction.
- next_step: Inspect each workflow step's inputs, outputs, authority, and
  validators through the page inspector.

### Staged-Autonomy Harness

- premise: The AI system is being developed toward staged autonomy by operating
  on the live GR-derivation research problem.
- mechanism: The harness tests agent roles, routing, refutation, novelty
  search, claim gates, memory, and validation against real theoretical physics
  work while humans retain accountability.
- source_basis: `README.md`, `AGENTS.md`, `.codex/skills/continue-research/SKILL.md`,
  and `.codex/skills/improve-project-system/SKILL.md`.
- authority_status: AI-methodology and workflow explanation only.
- uncertainty: Current agent work remains human-scaffolded and validator-gated;
  autonomous research capability is not assumed.
- validation_or_test: Autonomy claims require measurable task success,
  reproducible handoffs, controlled evaluation, and failure-mode tracking.
- next_step: Keep autonomy language separate from physics claim status in every
  generated explainer.

## Non-Goals

- Do not add or modify workflow rules.
- Do not change role contracts, validators, schemas, or routing behavior.
- Do not promote project-system status to scientific evidence.
- Do not use external images or network-dependent assets.
