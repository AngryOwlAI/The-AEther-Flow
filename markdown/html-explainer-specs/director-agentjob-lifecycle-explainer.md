---
title: "Director Decisions And AgentJob Lifecycle"
purpose: "Explain how Director Decision Records, AgentJobs, execution roles, completions, handoffs, and registries form the durable research-control record chain."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/director-agentjob-lifecycle-explainer.html"
github_markdown_output_path: "github-facing/director-agentjob-lifecycle-explainer.md"
wiki_output_path: "wiki/html/html-director-agentjob-lifecycle-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/director-agentjob-lifecycle.publication-brief.md"
document_type: "decision_or_lifecycle_guide"
visual_strategy: "state_model"
migration_status: "reviewed"
source_materials:
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/DIRECTOR_DECISION_SCHEMA.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for Director decisions and the AgentJob lifecycle. It explains task, DDR, AgentJob, execution-role, completion, handoff, registry, allowlist, validator, claim-boundary, and stop-condition relationships without editing schemas, changing task behavior, altering routing, expanding authority, mutating historical records, or treating completion evidence as broad proof."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Director Decisions And AgentJob Lifecycle Source Spec

## Publication Brief Binding

Use
`markdown/publication-briefs/director-agentjob-lifecycle.publication-brief.md`
as the page-specific editorial contract. The page is a lifecycle guide for
tracked research-control records. It is not a schema edit, task-behavior
change, routing change, role registration, or permission to mutate historical
control records.

## Source Basis

- `research_control/README.md` defines the authority model, one-job rule,
  execution-role records, memory preflight, validation, and documentation
  impact.
- `research_control/AGENTS.md` defines tracked control-state authority and
  immutable-record editing rules.
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` defines required Director
  Decision Record fields and sections.
- `.agents/schemas/AGENT_JOB_SCHEMA.md` defines required AgentJob fields,
  memory-preflight receipts, optional routing fields, and physics-specific
  decomposition fields.
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` defines registered-role,
  task-overlay, and one-job provisional execution-role records.
- `registries/DIRECTOR_DECISION_REGISTRY.csv` records DDR provenance.
- `registries/AGENT_JOB_REGISTRY.csv` records AgentJob provenance,
  completion paths, allowed writes, outputs, and status.
- `registries/ROLE_EXECUTION_REGISTRY.csv` records the exact execution-role
  contract used for each AgentJob.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the durable
record chain and know why activated or created DDRs, AgentJobs, completions,
approvals, and handoffs are superseded rather than edited. They should also
know that a completion record is evidence for one bounded transaction, not a
broad proof, role-registration act, schema change, or generated-output
authority grant.

## Visual Strategy

Use a state model. The visual should place task, DDR, AgentJob, execution-role
record, completion, handoff, and registry rows in order. Pair it with a record
matrix, an allowlist and stop-condition checklist, and safe-versus-unsafe edit
examples. Do not use browser-side Mermaid.

## Acceptance Criteria

- Explains task, DDR, AgentJob, execution-role record, completion, handoff,
  and registry relationships.
- States that activated or created DDRs, AgentJobs, completions, approvals,
  and handoffs are superseded rather than rewritten.
- Explains allowlists, validators, claim boundaries, and stop conditions.
- States that completion evidence is transaction evidence, not broad proof.
- Names common operator mistakes and safe corrective actions.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
