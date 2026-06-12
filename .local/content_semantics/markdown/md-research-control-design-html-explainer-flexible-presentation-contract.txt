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
claim-boundary metadata, interaction, analysis-capsule, and validation fields:

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

Every tracked explainer must include a `subject_summary` content block. This
block gives the reader a source-backed functional summary of the page subject
before the detailed explanation begins. It is a universal summary requirement,
not a new authority layer. The block may cite only
paths declared in the source spec's `source_materials`; if the best summary
evidence is absent, add that source path to `source_materials` before citing it
in the generated HTML. The source spec must list `subject_summary` as the first
entry in `required_content_blocks`, and the Markdown body's
`## Required Content Blocks` section must define `subject_summary` first, so
frontmatter order, body-definition order, and rendered content-block order stay
aligned.

`subject_summary` has a fixed semantic shape with adaptive visual presentation.
It must tell the reader in one coherent prose block:

- what the subject is
- what functionality or role it has
- why it matters for the project itself
- how it fits the surrounding research or project-control system
- which source files ground the summary

The block ID is universal, but its Markdown body description is page-specific.
For the ontology explainer, the source spec should define it as:

```text
- subject_summary: Summarize the project-specific Æther-flow ontology, its role
  in the exact-GR benchmark program, and the source files grounding the summary.
```

The project overview hub is not exempt. Its `subject_summary` describes the
explainer atlas itself: what the atlas is, what role it plays in routing
readers, why that matters, how it fits the project, and which specs or source
files ground the hub.

`subject_summary` is not part of `analysis_capsule_schema`. Analysis capsules
remain the reasoning structure for premise, mechanism, authority, uncertainty,
validation, and next step. `subject_summary` is a source-backed summary content
block.

Generated HTML must mark these summary elements with `data-summary-field`
values:

- `summary_text`
- `source_basis`

`subject_summary` does not add a separate claim-boundary field. Page-relevant
authority or claim-boundary caution belongs inside `summary_text` when it is
necessary to explain what the subject is, why the subject matters, or how the
subject fits the project. Ontology and claim-gate summaries should make
boundaries explicit; technical or setup summaries may use lighter authority
language. Existing claim-boundary metadata and analysis capsules remain
mandatory through their own contract.

The `source_basis` summary field must contain visible file-path chips or an
equivalent visible source-path list. Hidden structural markers are insufficient
for this field because the summary must orient human readers to the grounding
files before the detailed explanation begins. In tracked HTML, these chips
display paths and `data-source-path` markers only; they do not add local file
links because local browser link behavior is inconsistent and can create
portability or security concerns.

The generated page should render this block immediately after the hero/title
area and before the section table of contents under the reader-facing heading
`Summary of [Subject]`, for example `Summary of Claim Gates`. The section
table of contents and detailed explanation, diagrams, catalogs, workflow steps,
or evidence matrices follow the summary. Active tracked HTML must not render
the obsolete labels `Reader orientation` or `What This Explainer Describes`.

The visual form is intentionally adaptive. A content block may be a table,
matrix, chip row, card group, sidebar, callout, accordion, popover, inspector
panel, or another source-backed structure suited to the page.

Every tracked explainer must also expose the complete source list as a visible
`All Source Materials` section marked with
`data-explainer-control="source_materials_section"`. Legacy source drilldowns
and claim-boundary toggles remain valid only when a source spec explicitly
declares them; they are not universal visible panels.

## Validator Scope

Validators enforce deterministic structural evidence only:

- required source-spec fields exist
- `presentation_profile` is allowed
- `layout_intent` is nonblank
- `required_content_blocks` is non-empty and syntactically valid
- the first declared `required_content_blocks` value is `subject_summary`
- the first block definition under `## Required Content Blocks` is
  `- subject_summary:`
- each required block appears as `data-content-block`
- each required block contains source-path evidence
- every `data-source-path` inside `subject_summary` is declared in the source
  spec's `source_materials`
- `subject_summary` contains the required `data-summary-field` markers:
  `summary_text` and `source_basis`
- the `source_basis` summary field contains visible `data-source-path` evidence
- the first `data-content-block` marker on the page is
  `data-content-block="subject_summary"`
- the first `data-content-block="subject_summary"` marker appears before the
  first `data-explainer-control="section_toc"` marker
- active tracked HTML does not contain the obsolete visible labels
  `Reader orientation` or `What This Explainer Describes`
- required control, source-material, analysis-capsule, source-basis, hash, and
  Mermaid parity markers remain valid
- Mermaid inline SVG output uses explicit numeric dimensions derived from
  `viewBox`
- tracked HTML remains generated, human-only, source-backed, and
  non-authoritative

Validators do not judge prose quality, visual quality, completeness, or
creative fit. Those are handled by source-spec review and visual QA.

## Rendered QA

Universal `subject_summary` migration requires rendered QA across every
currently tracked HTML explainer, not a representative sample. The QA pass must
check summary visibility, absence of mobile body overflow, readable visible
source chips, absence of obsolete summary labels, and intact
table-of-contents and diagram behavior for each page.

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

When a spec declares registered Mermaid diagrams, Markdown Mermaid source remains
canonical and tracked HTML must use build-time inline SVG with preserved source
parity.

## Migration Scope

Universal validator-backed explainer contract changes apply to all currently
tracked HTML explainers in one bounded transaction. A partial migration is not
valid once a universal validator rule lands because unmigrated source specs or
HTML outputs would fail the shared contract.

The same transaction must update the project-local skill contracts that future
agents use to create or regenerate tracked explainers. At minimum, this includes
`.codex/skills/html-visual-explainer/SKILL.md` and
`.codex/skills/visual-explainer/SKILL.md`, so operational instructions match the
validator-backed `subject_summary` rule.

The implementation must also update the Documentation Curator role contract so
ownership of source-backed subject summaries is explicit in the role that owns
human-facing explanatory documentation. Because registered role versions are
immutable in meaning, the role-contract update must follow the repository's
role-versioning rules by registering `documentation-curator@0.4.0` and
superseding `documentation-curator@0.3.0`, rather than silently changing
historical execution semantics.

The implementation transaction is Project-Control Maintainer work, not
Documentation Curator work, because it changes validator behavior, skill
contracts, and a permanent registered role version. Documentation Curator owns
future source-backed subject-summary use after the capability is registered.

For this contract, "related Markdown files" means the canonical explainer source
specs under `markdown/html-explainer-specs/*.md` and any upstream declared
`source_materials` needed to ground the summary. Generated wiki Markdown under
`wiki/` remains derivative and must be regenerated by the memory system rather
than edited directly.
README changes are normally out of scope for this subject-summary migration
unless an existing concise explainer-system section needs a one-sentence
alignment update. The durable contract belongs in this design note, skill
contracts, the role contract, source specs, validators, and generated pages.

Subject-summary prose is manually authored per source spec during migration.
Scripts may validate structure and regenerate derivative artifacts, but they do
not derive the reader-facing summary text automatically from source files.
Each summary should target 150-240 words total, excluding visible source chips.
This is a source-review and rendered-QA guideline, not a validator-enforced word
count.

Implementation should update focused tests and validator behavior together
before bulk spec and HTML migration. Required test cases include missing
`subject_summary`, wrong first declared block, missing `summary_text`, missing
source-path evidence, undeclared summary source paths, wrong rendered
placement, and obsolete visible summary labels. The migrated source specs and
generated HTML are then driven to the executable contract.

The actual validator, registry, role-version, source-spec, generated-HTML, and
generated-derivative changes must run inside a fresh bounded Project-Control
Maintainer research-control transaction with an explicit AgentJob write-path
allowlist. The design-session documentation itself does not authorize loose
control-contract or generated-output edits.
Design-session edits to `CONTEXT.md` and this design note are included in that
transaction scope and must be covered by the same allowlist and validation path
before checkpointing.

The flexible-presentation migration applies to all tracked HTML explainers in
one transaction:

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
- broadly rewrite analysis capsules; only narrow duplicate-opening cleanup is
  allowed when a new subject summary makes existing prose redundant
- add a full deterministic HTML generator
- add a new CSV registry for presentation profiles

The Documentation Curator or LLM renderer remains responsible for choosing the
best presentation from the spec. Python validators check structural evidence.
