---
title: "Research-Agent Workflow"
purpose: "Explain how AEther-Flow routes bounded physics and project-system work through source-first control records without expanding role or claim authority."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/research-agent-workflow-explainer.html"
github_markdown_output_path: "github-facing/research-agent-workflow-explainer.md"
wiki_output_path: "wiki/html/html-research-agent-workflow-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/research-agent-workflow.publication-brief.md"
document_type: "workflow_guide"
visual_strategy: "process_timeline"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for the AEther-Flow research-agent workflow. It explains request classification, continuation, project-system improvement, one bounded AgentJob per invocation, memory preflight, role contracts, validators, generated outputs, and human gates without changing routing behavior, role authority, validator requirements, write permissions, claim boundaries, or physics status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Research-Agent Workflow Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/research-agent-workflow.publication-brief.md`
as the page-specific editorial contract. The page is a workflow guide for the
project's source-first operating discipline. It is not a routing change, role
registration, validator change, physics review, or authorization to treat
generated outputs as authority.

## Source Basis

- `README.md` defines the two linked missions: physics research and AI
  research-agent development.
- `AGENTS.md` defines authority hierarchy, continuation boundaries,
  project-system improvement boundaries, and generated-output limits.
- `research_control/README.md` defines Director decisions, AgentJobs,
  execution-role records, completions, handoffs, memory preflight, one-job
  rule, validation, and documentation-impact discipline.
- `research_control/AGENTS.md` defines tracked control state, editing rules,
  and `.local` cache boundaries.
- `.codex/skills/continue-research/SKILL.md` defines the continuation workflow
  for one bounded research-control AgentJob.
- `.codex/skills/improve-project-system/SKILL.md` defines the project-system
  improvement workflow for one bounded project-system AgentJob.
- `registries/AGENT_ROLE_REGISTRY.csv` supplies role authority levels,
  human-gate status, default validators, and Documentation Curator limits.

## Required Reader Outcome

After reading, a maintainer or future agent should know which workflow lane to
use, why there is at most one bounded AgentJob per invocation, how memory
preflight should guide source inspection without overriding source authority,
and why validators, generated artifacts, and public explainers do not promote
physics claims or role authority.

## Visual Strategy

Use a process timeline with two lanes: physics continuation and project-system
improvement. The visual should show request intake, classification or state
resolution, memory preflight, Director routing, one AgentJob, validation,
completion, and handoff. Include a separate stop-condition decision tree. Do
not use a generic source-to-checks diagram or browser-side Mermaid.

## Acceptance Criteria

- Explains the two linked missions and why the agent workflow exists.
- Separates continuation from project-system improvement.
- States one bounded AgentJob per invocation.
- Explains memory preflight as navigation, not authority.
- Explains role contracts and execution-role records without expanding role
  authority.
- States that validators and generated outputs are boundary checks or reader
  aids, not scientific verdicts.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
