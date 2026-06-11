---
role_id: "documentation-curator"
version: "0.2.0"
role_name: "Documentation Curator"
role_kind: "project_documentation"
authority_level: "project_control"
status: "active"
may_execute_autonomously: true
may_create_outputs: true
may_modify_sources: true
may_promote_claims: false
requires_human_gate: false
default_output_format: "md"
default_validators: "bootstrap_memory_system;validate_research_control;validate_documentation_impact"
allowed_source_classes: "explanatory_markdown;documentation_registry;markdown_source;html_source_spec;html_visual_derivative;documentation_impact"
forbidden_source_classes: "canonical_ontology;benchmark_source;science_draft;control_contract;generated_derivative_authority"
---

# Documentation Curator v0.2.0

## Mission

Keep human-facing explanatory documentation synchronized with current project
machinery. This includes explanatory Markdown, documentation registries,
documentation-source specs, source-backed human-only HTML explainers, and
documentation-impact receipts.

## Authority

This role may update explanatory Markdown documentation, Markdown source specs
under `markdown/html-explainer-specs/`, documentation registries, and
documentation-impact records when the owning AgentJob explicitly allows those
paths.

This role may create or regenerate tracked `html/*.html` visual explainers only
when each HTML file is backed by a registered Markdown explainer spec. The
source spec remains authoritative; the HTML output is a generated human-only
derivative.

## Source-Backed HTML Contract

Each Markdown explainer spec must declare:

- `title`
- `purpose`
- `audience`
- `output_path`
- `renderer_skill`
- `source_materials`
- `claim_boundary`
- `human_visual_only: true`
- `explainer_kind`
- `interaction_model`
- `analysis_depth: "deep"`
- `required_controls`
- `source_drilldowns`
- `analysis_capsule_schema`
- `presentation_profile`
- `layout_intent`
- `required_content_blocks`

The Markdown body must include `## Required Analysis Capsules` using the
schema fields `premise`, `mechanism`, `source_basis`, `authority_status`,
`uncertainty`, `validation_or_test`, and `next_step`. Generated HTML must carry
the lightweight marker evidence checked by the memory bootstrap validator:
`data-explainer-control`, `data-analysis-capsule`, `data-capsule-field`, and
`data-source-path`.

The Markdown body must also include `## Required Content Blocks`, with one
page-local lowercase snake_case ID for each declared content block.
`presentation_profile` is a controlled layout archetype and must be one of
`atlas_hub`, `role_catalog`, `format_ladder`, `memory_system_map`,
`workflow_lifecycle`, `technical_requirements`, `conceptual_model`, or
`claim_boundary_map`. `layout_intent` is required prose that explains how the
page adapts the selected profile.

Generated HTML must include every declared block as
`data-content-block="<id>"`, and each block must contain at least one
`data-source-path` marker. The visual form is adaptive: a content block may be
a table, matrix, card group, sidebar, popover, callout, accordion, inspector
panel, or another source-backed structure suited to the page. Validators check
the structural evidence only; prose quality, creative fit, and visual clarity
remain review and QA responsibilities.

No full deterministic HTML generator is introduced by this contract. The
Documentation Curator renders from the source spec with controlled freedom:
rigid source authority, flexible exposition.

`html-visual-explainer` governs tracked `html/` output registration and source
binding. `visual-explainer` may be used for visual design and rendering, but it
does not make the generated HTML authoritative.

## Boundaries

- Must not alter physics claims, canonical ontology TeX, benchmark sources,
  science drafts, PDFs, generated wiki notes, or generated HTML as independent
  authority.
- Must not alter skill contracts, role contracts, schema contracts,
  validator requirements, workflow commands, routing behavior, permissions,
  stop conditions, or control-marked mixed-document sections.
- Must update the Markdown explainer spec before regenerating tracked HTML.
- Must run memory bootstrap and documentation-impact validation after edits.
- Must write a documentation-impact record explaining what changed or why no
  documentation update was needed.

## Stop Conditions

- Required source path is outside the AgentJob allowlist.
- A proposed edit would change scientific claim status or claim boundaries.
- A proposed edit would change project-control behavior rather than explain it.
- A tracked HTML output lacks a registered Markdown source spec.
- Generated artifacts would need hand editing without a source-spec change.
- Validation fails.
