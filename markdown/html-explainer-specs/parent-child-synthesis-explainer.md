---
title: "Parent-Child Parallel Synthesis"
purpose: "Explain parent_child_parallel_synthesis as internal perspective decomposition within one bounded physics AgentJob, preserving one-job authority and fused-output completion."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/parent-child-synthesis-explainer.html"
github_markdown_output_path: "github-facing/parent-child-synthesis-explainer.md"
wiki_output_path: "wiki/html/html-parent-child-synthesis-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/parent-child-synthesis.publication-brief.md"
document_type: "concept_explainer"
visual_strategy: "state_model"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/AGENT_JOB_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for parent_child_parallel_synthesis. It explains the internal parent and child perspective mode, inherited authority, conflict handling, and fused output without changing the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, role authority, write permissions, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Parent-Child Parallel Synthesis Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/parent-child-synthesis.publication-brief.md`
as the page-specific editorial contract. The page is a concept explainer for
an internal physics-AgentJob decomposition mode. It is not a schema edit,
validator edit, role-authority change, routing change, or permission to create
extra AgentJobs.

## Source Basis

- `README.md` establishes the linked physics and research-agent missions.
- `AGENTS.md` sets the authority hierarchy, project-system boundary, and
  generated-output limits.
- `research_control/README.md` states the one-job rule and the parent-child
  synthesis rule for future physics AgentJobs.
- `research_control/AGENTS.md` states that tracked control files carry
  authority and `.local` caches do not.
- `.agents/schemas/AGENT_JOB_SCHEMA.md` defines the supported
  `role_decomposition` shape and its external invariant.
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` states that parent-child
  synthesis does not create child execution-role records.
- `registries/AGENT_JOB_REGISTRY.csv` supplies AgentJob record evidence and
  output-path anchoring.

## Required Reader Outcome

After reading, a maintainer or future agent should know that
`parent_child_parallel_synthesis` is an internal decomposition inside one
physics AgentJob. The parent and child units inherit the same execution-role
record, claim boundary, write allowlist, source restrictions, validators, and
stop conditions. Child outputs support review; the fused output remains the
final artifact for completion, handoff, and downstream registry references.

## Visual Strategy

Use a state-model visual with two internal lanes: parent review/fusion and
child perspective outputs. The visual must keep a single outer AgentJob frame
around both lanes. It should teach the one-job invariant, inherited authority,
conflict review, and fused-output endpoint. Do not use browser-side Mermaid or
a generic validation flow.

## Acceptance Criteria

- States one Director decision, one outer AgentJob, one execution-role record,
  one completion record, and one fused output.
- Explains inherited authority, allowlists, source restrictions, claim
  boundaries, validators, and stop conditions.
- States that child outputs are supporting draft/control artifacts.
- Explains that unresolved blocking conflicts prevent PASS completion.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
