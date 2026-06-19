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

## Required Opening

Open with the external invariant: one Director decision, one outer AgentJob,
one execution-role record, one completion record, and one fused output. Then
explain that child outputs are supporting `draft/control` artifacts, that all
authority is inherited from the outer job, and that an unresolved declared
blocking conflict prevents PASS completion. State explicitly that this mode is
scoped to future physics research AgentJobs and is not a universal rule for
all non-physics project-system work.

## Visual Strategy

Use a two-lane parent/child/fusion diagram inside a single outer AgentJob
frame. The reader learns how internal perspective decomposition improves
review coverage without adding AgentJobs, write authority, role records, or
claim authority. The tracked HTML may render this as a local CSS frame; GitHub
Markdown may render it as a native invariant table plus conflict path.

## Required Reader Outcome

After reading, a maintainer or future agent should know that
`parent_child_parallel_synthesis` is an internal decomposition inside one
physics AgentJob. The parent and child units inherit the same execution-role
record, claim boundary, write allowlist, source restrictions, validators, and
stop conditions. Child outputs support review; the fused output remains the
final artifact for completion, handoff, and downstream registry references.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: concept orientation only. This explanation cannot change the
one-job rule, AgentJob schema, execution-role schema, validators, routing
behavior, role authority, write permissions, or physics claim status.

## Acceptance Criteria

- States one Director decision, one outer AgentJob, one execution-role record,
  one completion record, and one fused output.
- Explains inherited authority, allowlists, source restrictions, claim
  boundaries, validators, and stop conditions.
- States that child outputs are supporting draft/control artifacts.
- Explains that unresolved blocking conflicts prevent PASS completion.
- States that the mode is not required for all non-physics tasks.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in GitHub Markdown and tracked HTML.
- Moves the full generated-noncanonical paragraph to the marked authority
  footer in GitHub Markdown and tracked HTML.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
