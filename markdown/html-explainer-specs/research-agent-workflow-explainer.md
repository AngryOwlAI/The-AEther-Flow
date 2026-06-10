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
- A validation gate showing bootstrap, documentation-impact validation,
  project-improvement signal validation, research-control validation, tests,
  and diff checks.
- A claim-boundary notice stating that this page is human-only and
  non-authoritative.

## Non-Goals

- Do not add or modify workflow rules.
- Do not change role contracts, validators, schemas, or routing behavior.
- Do not promote project-system status to scientific evidence.
- Do not use external images or network-dependent assets.
