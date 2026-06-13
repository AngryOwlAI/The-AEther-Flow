# HTML Explainer Depth Contract

Date: 2026-06-12
Authority lane: project-control design documentation

## Decision

Tracked human-only HTML explainers must be source-backed documentation pages,
not only structurally valid visual wrappers. The Markdown source spec remains
the authority for each tracked explainer, and the tracked HTML remains a
generated derivative. The new depth rule concerns documentation quality at the
human reading layer.

Accepted principle:

```text
structural validity is necessary, but not sufficient
```

## Problem

The explainer system already validates source binding, required markers,
hashes, controls, generated-output registration, and Mermaid parity. That is
the correct governance architecture, but it does not by itself ensure that the
page reads as finished documentation.

The upgrade kit identified a recurring failure mode: non-summary content blocks
were sometimes rendered as short source-spec instructions such as "Explain the
workflow" or "State that exact GR is the benchmark." Such pages can pass
structural validation while failing a human reader who needs vocabulary,
context, examples, source evidence, and explicit claim boundaries.

## Content Rule

Every non-summary content block should answer seven reader questions:

1. What is this?
2. Why does the project need it?
3. How does it work inside the project?
4. What source files ground it?
5. What can it legitimately claim?
6. What can it not claim?
7. Where should a reader go next?

The renderer may present those answers as prose, cards, a matrix, quote
callouts, a timeline, tabs, or another source-backed structure. It should
integrate authority boundaries where they clarify a specific section, but it
must not append the same generic claim-boundary paragraph to every content
block. The HTML must look like completed documentation rather than instructions
for future documentation.

## Audience Ladder

Each tracked explainer should support three reading layers:

- Plain-language layer: a short explanation that avoids project shorthand and
  tells a newcomer why the page matters.
- Technical bridge: project vocabulary connected to registries, claim states,
  workflow objects, validators, or source authority.
- Source-grounded deep dive: source chips, short quotations or paraphrases, and
  explanation of how the evidence constrains the page.

## Recommended Minimums

For each declared `required_content_blocks` entry other than
`subject_summary`:

- Provide at least 120 words of rendered explanatory text, or use a structured
  matrix with at least four meaningful rows and source-backed commentary.
- Include at least one visible source chip or equivalent `data-source-path`
  marker.
- Include an authority-status or claim-boundary sentence when the page
  discusses physics, roles, validators, generated outputs, or source authority.
- Do not let a visible block begin with directive verbs such as `Explain`,
  `State`, `Show`, `List`, `Provide`, `Preserve`, or `Point readers to` unless
  the text is explicitly a checklist item.
- For mixed lay/technical audiences, place a plain answer before dense project
  terms.

## Source Quotations

Short source quotation panels are encouraged when exact source wording clarifies
a boundary better than paraphrase. Each quote panel should state:

- source path,
- why the quote matters,
- what the source permits,
- what the source forbids.

Quotations should remain short and should not promote Markdown prose above
registered science or registry authority.

## Shared Reader Layer

The generated HTML set should use a shared standalone reader layer with:

- reading progress,
- active-section navigation,
- local page search,
- click-to-copy source chips,
- stronger visual distinction between authority, physics, workflow, generated
  derivative, warning, and validation content,
- mobile-safe layout and typography,
- no network assets,
- no runtime Mermaid import,
- no changes to Mermaid diagram definitions.

The reader layer should not render file-management metadata as title-section
cards. `layout_intent`, registry `source_basis`, and human-only derivative
status remain source-spec or registry metadata. They may appear in machine
metadata and validation evidence, while visible grounding belongs in
`subject_summary` source chips and the All Source Materials section.

Global simple/technical mode toggles and global expand/collapse buttons are
not part of the required reader layer. They add state without clear
source-backed reading value. A future page-specific disclosure control may be
introduced only when the source spec defines the need and browser QA verifies
the behavior.

## Advisory Depth Lint

The project-level advisory lint is `scripts/spec_depth_lint.py`.

It flags:

- content blocks with fewer than the target explanatory depth,
- visible blocks that start with directive verbs,
- source-spec `Required Content Blocks` definitions that are too short and
  directive.

The lint is advisory in design, but current tracked explainers should be kept
at a passing state after migration. It complements the deterministic memory
bootstrap validator; it does not replace source-spec review or browser QA.

## Non-Goals

This contract does not:

- add physics claims,
- alter canonical ontology TeX or manuscript TeX,
- promote generated HTML to authority,
- require a full deterministic HTML generator,
- require Mermaid on every page,
- change the source-spec-first governance path,
- make validators judge prose quality beyond narrow warning patterns.
