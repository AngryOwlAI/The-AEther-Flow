# HTML Explainer Flexible Presentation Contract

Date: 2026-06-11
Authority lane: project-control design documentation

## Decision

Tracked human-only HTML explainers keep rigid source authority while allowing
flexible exposition.

Accepted principle:

```text
rigid authority, flexible exposition
```

The Markdown source spec remains the authority for each tracked HTML
explainer. The HTML file remains a generated, human-reading derivative.

## Source-Spec Fields

Every registered source spec under `markdown/html-explainer-specs/` must
declare these presentation fields in addition to the existing source,
drilldown, claim-boundary, interaction, analysis-capsule, and validation
fields:

- `presentation_profile`: controlled layout archetype.
- `layout_intent`: required nonblank prose explaining how the page adapts that
  profile.
- `required_content_blocks`: required non-empty list of page-local coverage
  obligations.

`presentation_profile` controls form. `required_content_blocks` controls
coverage. `layout_intent` gives the renderer room to choose the best
explanatory structure for the subject.

## Presentation Profiles

The initial controlled vocabulary is:

- `atlas_hub`
- `role_catalog`
- `format_ladder`
- `memory_system_map`
- `workflow_lifecycle`
- `technical_requirements`
- `conceptual_model`
- `claim_boundary_map`

This vocabulary is documented in the skill and role contracts and mirrored in
the deterministic validator constants. It is not a new CSV registry in this
migration. If the vocabulary later needs ownership metadata, lifecycle state,
or provenance history, it can be promoted into a registry through a separate
bounded project-system task.

## Required Content Blocks

`required_content_blocks` uses page-local IDs with global syntax rules:

- IDs must be lowercase snake_case.
- IDs must appear in the Markdown body under `## Required Content Blocks`.
- Each listed ID must appear in generated HTML as
  `data-content-block="<id>"`.
- Each generated content block must contain at least one `data-source-path`
  marker.

The visual form is intentionally adaptive. A content block may be a table,
matrix, chip row, card group, sidebar, callout, accordion, popover, inspector
panel, or another source-backed structure suited to the page.

## Validator Scope

Validators enforce deterministic structural evidence only:

- required source-spec fields exist
- `presentation_profile` is allowed
- `layout_intent` is nonblank
- `required_content_blocks` is non-empty and syntactically valid
- each required block appears as `data-content-block`
- each required block contains source-path evidence
- existing control, source-drilldown, claim-boundary, analysis-capsule,
  source-basis, hash, and Mermaid parity markers remain valid
- tracked HTML remains generated, human-only, source-backed, and
  non-authoritative

Validators do not judge prose quality, visual quality, completeness, or
creative fit. Those are handled by source-spec review and visual QA.

## Mermaid Policy

Mermaid is profile-guided, not mandatory for every explainer.

Usually expected:

- `atlas_hub`
- `memory_system_map`
- `workflow_lifecycle`
- `claim_boundary_map`

Often optional:

- `role_catalog`
- `format_ladder`
- `technical_requirements`
- `conceptual_model`

When a spec declares governed Mermaid diagrams, Markdown Mermaid source remains
canonical and tracked HTML must use build-time inline SVG with preserved source
parity.

## Migration Scope

This migration applies to all tracked HTML explainers in one transaction:

- update `html-visual-explainer` guidance
- update Documentation Curator guidance
- update validator constants and tests
- retrofit all existing source specs
- regenerate all affected tracked HTML pages
- add roles-and-skills, memory-system, and technical-requirements explainers
- update README links and concise requirement tiers
- make the overview page the grouped atlas index

## Non-Goals

This design does not:

- add physics claims
- change canonical science sources
- change control-routing semantics
- promote generated HTML to authority
- add a full deterministic HTML generator
- add a new CSV registry for presentation profiles

The Documentation Curator or LLM renderer remains responsible for choosing the
best presentation from the spec. Python validators check structural evidence.
