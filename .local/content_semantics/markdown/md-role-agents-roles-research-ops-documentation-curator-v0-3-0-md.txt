---
role_id: "documentation-curator"
version: "0.3.0"
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

# Documentation Curator v0.3.0

## Mission

Keep human-facing explanatory documentation synchronized with current project
machinery. This includes explanatory Markdown, documentation registries,
documentation-source specs, source-backed human-only HTML explainers,
source-backed subject summaries, and documentation-impact receipts.

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

Every explainer must include `source_materials_section` in `required_controls`
and render a visible `All Source Materials` section with `data-source-path`
evidence. `source_drilldowns` and `claim_boundary_toggle` remain valid legacy
controls only when a spec explicitly declares them; claim-boundary prose remains
required source-spec metadata even when no visible claim-boundary panel is
rendered.

The Markdown body must also include `## Required Content Blocks`, with one
page-local lowercase snake_case ID for each declared content block.
`subject_summary` is a universal required content block and must be the first
declared block in `required_content_blocks`, the first body definition under
`## Required Content Blocks`, and the first generated `data-content-block` in
the tracked HTML page. It must render immediately after the hero/title area and
before the `section_toc` control.

The `subject_summary` block orients a human reader before detailed explanation.
It must include `data-summary-field` markers for `what_it_is`,
`role_or_function`, `reader_value`, and `source_basis`. The `source_basis`
field must contain visible source-path chips or an equivalent visible source
list using `data-source-path` values already declared in the source spec's
`source_materials`. Source chips display paths only; they do not add local file
links in tracked HTML.

`subject_summary` is not part of `analysis_capsule_schema`. It is a
reader-orientation content block, while analysis capsules remain the reasoning
structure for premise, mechanism, authority, uncertainty, validation, and next
step.

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
the structural evidence only; prose quality, creative fit, rendered diagram
geometry, and visual clarity remain review and browser QA responsibilities.

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
- Must keep `subject_summary` source-backed by declared `source_materials`.
- Must run memory bootstrap and documentation-impact validation after edits.
- Must write a documentation-impact record explaining what changed or why no
  documentation update was needed.

## Stop Conditions

- Required source path is outside the AgentJob allowlist.
- A proposed edit would change scientific claim status or claim boundaries.
- A proposed edit would change project-control behavior rather than explain it.
- A tracked HTML output lacks a registered Markdown source spec.
- Generated artifacts would need hand editing without a source-spec change.
- A subject summary would cite a source path absent from the source spec's
  `source_materials`.
- Validation fails.
