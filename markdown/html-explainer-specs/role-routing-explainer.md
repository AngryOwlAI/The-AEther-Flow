---
title: "Role Routing And Execution Contracts"
purpose: "Explain how registered roles, task overlays, one-job provisional roles, and execution-role records constrain actual AgentJob authority."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/role-routing-explainer.html"
github_markdown_output_path: "github-facing/role-routing-explainer.md"
wiki_output_path: "wiki/html/html-role-routing-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/role-routing.publication-brief.md"
document_type: "reference_catalog"
visual_strategy: "role_matrix"
migration_status: "reviewed"
source_materials:
  - "research_control/README.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - ".agents/schemas/ROLE_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - ".agents/roles/"
claim_boundary: "Human-only publication explainer for AEther-Flow role routing and execution contracts. It explains registered roles, task overlays, one-job provisional roles, execution-role records, authority levels, validators, and human gates without registering roles, changing role authority, changing schemas, changing routing behavior, changing AgentJob allowlists, or authorizing claim promotion."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Role Routing And Execution Contracts Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/role-routing.publication-brief.md` as the
page-specific editorial contract. The page is a reference catalog. It explains
how to inspect role contracts and execution-role records; it does not register
a role, expand authority, change schemas, or alter routing behavior.

## Source Basis

- `research_control/README.md` explains registered roles, task overlays,
  one-job provisional roles, execution-role records, and signal routing for
  recurring provisional-role patterns.
- `registries/AGENT_ROLE_REGISTRY.csv` supplies role identity, version,
  authority level, status, default output, default validators, and human-gate
  status.
- `registries/ROLE_EXECUTION_REGISTRY.csv` supplies task-local execution-role
  records and allowlist evidence.
- `.agents/schemas/ROLE_SCHEMA.md` defines registered role frontmatter and the
  rule that one-job semantics are fixed by an execution-role record.
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` defines `registered_role`,
  `task_overlay`, and `one_job_provisional_role`.
- `.agents/roles/` contains the active and historical role contracts named by
  the role registry.

## Required Opening

Open by separating role names from current authority. Explain that a registered
role is a template, a task overlay is one-job constrained adaptation, a
one-job provisional role is temporary, and an execution-role record plus the
AgentJob allowlist decide the actual write and claim boundary for one
transaction. Preserve Gate Chair human-gated status and do not imply that role
presence alone expands a current job.

## Visual Strategy

Use a role matrix and a routing decision table rather than a decorative graph.
The matrix should group active role families by authority level, output form,
validator family, and gate status. The decision table should distinguish
`registered_role`, `task_overlay`, and `one_job_provisional_role`.

## Required Reader Outcome

After reading, a maintainer or future agent should know that a role contract
is a stable template and that the execution-role record plus AgentJob allowlist
define actual one-job authority. The reader should know how to distinguish
direct registered-role use, task overlays, and one-job provisional roles; how
to preserve Gate Chair human-gated status; and why repeated provisional-role
patterns route to project-system review instead of becoming reusable by habit.

## Acceptance Criteria

- Distinguishes registered role, task overlay, and one-job provisional role.
- Lists active physics and active research-ops role categories with gate
  status.
- Explains role authority level, may/may-not fields, and execution-role
  records.
- Explains recurring provisional-role review as a project-system signal.
- States that role presence does not expand a current AgentJob allowlist.
- Moves the full generated-noncanonical paragraph to the marked authority
  footer in GitHub Markdown and tracked HTML.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
