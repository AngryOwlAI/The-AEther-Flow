---
name: html-visual-explainer
description: Front door for generated human-only HTML explainers.
---

# HTML Visual Explainer

Use this skill when producing or validating tracked HTML explainers.

Rules:

- Tracked HTML under `html/` is generated-only.
- Every tracked HTML explainer must have a registered Markdown source spec.
- The source spec lives under `markdown/html-explainer-specs/`.
- The source spec must declare `title`, `purpose`, `audience`,
  `output_path`, `renderer_skill`, `source_materials`, `claim_boundary`, and
  `human_visual_only: true`.
- The source spec must also declare the interaction contract:
  `explainer_kind`, `interaction_model: "progressive_disclosure"`,
  `analysis_depth: "deep"`, and `required_controls`.
- The source spec must also declare the flexible presentation contract:
  `presentation_profile`, `layout_intent`, and
  `required_content_blocks`.
- Visual Atlas v2 source specs should also declare `topic_id`,
  `explainer_subject`, `reader_question`, `github_markdown_output_path`,
  `wiki_output_path`, `primary_visuals`, `reader_blocks`,
  `github_markdown_parity: true`, `standalone_html: true`, and
  `no_external_runtime: true`.
- Required atlas topics are tracked in
  `registries/EXPLAINER_TOPIC_REGISTRY.csv`. The topic registry validates
  concept coverage; it does not create source authority for generated pages.
- `explainer_kind` must be one of `project_overview`, `conceptual_model`,
  `workflow_process`, or `control_system`.
- `presentation_profile` is a layout archetype, not a hidden content-rule
  engine. It must be one of `atlas_hub`, `role_catalog`, `format_ladder`,
  `memory_system_map`, `workflow_lifecycle`, `technical_requirements`,
  `conceptual_model`, or `claim_boundary_map`.
- `layout_intent` must be nonblank prose explaining how this page should adapt
  the chosen profile.
  It is renderer guidance and validation metadata, not reader-facing content.
  Do not render `layout_intent`, registry `source_basis`, or derivative
  authority status as hero/title metadata chips. Keep registry binding in
  `<meta>` tags and visible source grounding in the summary/source sections.
- `required_content_blocks` must be a non-empty list of page-local IDs using
  lowercase snake_case. Each ID must be explained in a Markdown
  `## Required Content Blocks` section.
- Every tracked explainer must declare `subject_summary` as the first
  `required_content_blocks` value and define `subject_summary` first under
  `## Required Content Blocks`. The block is a source-backed functional
  summary of the page subject.
- Required atlas topics should include `what_this_does`,
  `why_aether_needs_it`, `system_map`, `how_it_works`,
  `objects_and_authority`, `example`, `non_example`, `common_confusions`,
  `what_this_does_not_authorize`, `source_map`, and `next_reading_path` in
  both source specs and generated outputs.
- Generated HTML must render `subject_summary` as the first
  `data-content-block`, immediately after the hero/title area and before
  `data-explainer-control="section_toc"`, under a reader-facing heading in the
  form `Summary of [Subject]`.
- `subject_summary` must include `data-summary-field` markers for
  `summary_text` and `source_basis`.
  The `summary_text` field is one coherent prose block that explains what the
  subject is, what functionality or role it has, why it matters to the project,
  and how it fits the surrounding research or project-control system.
  It must explain the subject, not the HTML page, source spec, renderer,
  navigation layout, or derivative status. Phrases such as "this page explains"
  are acceptable only in source-binding or boundary notes, not as the primary
  summary of the project component.
  The `summary_text` field must not include prose source-grounding sentences or
  source-list restatements. Grounding belongs in the separate `source_basis`
  field.
  The `source_basis` field must contain visible source-path chips or an
  equivalent visible source list. Every `data-source-path` inside
  `subject_summary` must already be declared in the spec's `source_materials`;
  add missing grounding files to `source_materials` before citing them.
  Source chips display paths only and must not add local file links.
  Active tracked HTML must not render the obsolete labels `Reader orientation`
  or `What This Explainer Describes`.
- Every explainer requires `section_toc` and `source_materials_section`.
  `source_drilldowns` and `claim_boundary_toggle` are valid legacy controls
  when a source spec declares them, but they are no longer universal visible
  panels.
  `workflow_step_inspector` is required for
  `workflow_process` and `control_system` explainers.
  Workflow step inspectors must be page-specific and source-backed. Do not
  reuse a generic object-path trace unless that exact trace is the subject's
  workflow. When a paired GitHub-facing Markdown derivative exists, include a
  matching `## Workflow Step Inspector` reader section for every source spec
  that declares `workflow_step_inspector`.
- The generated HTML must include lightweight structural markers:
  `data-explainer-control="<control>"`, `data-content-block="<id>"`,
  `data-summary-field="<field>"`, and `data-source-path` in the visible source
  materials section and source-backed content blocks. Validation checks marker
  presence, not visual design or JavaScript behavior.
- The generated HTML must include each declared content block as
  `data-content-block="<id>"`. Each content block must contain at least one
  `data-source-path` marker. The visual form can be a table, matrix, card
  group, sidebar, callout, inspector panel, accordion, or other appropriate
  source-backed presentation for the chosen profile.
- Every non-summary content block must be finished reader-facing documentation,
  not a copied source-spec directive. Each block should answer what the subject
  is, why the project needs it, how it works inside the project, which sources
  ground it, and where the reader should go next. Add authority or claim-boundary
  context only when it helps the specific block; do not append generic claim
  boilerplate to every section. A block may satisfy this through prose, term
  cards, a matrix, a timeline, quote panels, or another source-backed form.
  Blocks must not describe themselves as content blocks, visual sections, or
  explainer coverage. They should teach the project functionality directly.
- A spec may declare an optional teaching enrichment contract:
  `teaching_loop.enabled: true`, `rounds`, `student_role`, `teacher_role`,
  `audience_model`, `qa_packet`, and `required_teaching_blocks`. The packet
  path must point under `markdown/teaching-packets/`, and the body must include
  a `## Teaching Q&A Basis` section that states the packet is explanatory
  support only.
- Teaching-enabled explainers should render the packet as finished teaching
  material, not raw transcript: Start Here, Why This Exists, Mental Model, Key
  Terms, Guided Walkthrough, Common Questions, Examples and Non-Examples,
  Common Confusions, What This Does Not Authorize, Check Your Understanding,
  and Where To Go Next are preferred reader blocks when they fit the page.
  The teaching loop should ask and answer why the project component exists and
  how it works. It should not ask the reader to study the page as an object.
- The teaching loop does not introduce a separate renderer or authority lane.
  Documentation Curator remains the tracked-doc writer; Documentation Student
  asks questions only; Documentation Teacher answers only from selected
  sources; the packet is explanatory support, never source authority.
- For current tracked explainers, use the project depth contract at
  `research_control/design/html_explainer_depth_contract.md` and run
  `scripts/spec_depth_lint.py --root .` after generation. The lint is advisory
  by design, but migrated current explainers should remain warning-free.
- For teaching-enabled explainers, also run
  `scripts/validate_teaching_qa.py --root .`.
- Visible content blocks must not begin with renderer-instruction stubs such as
  `Explain`, `State`, `Show`, `List`, `Provide`, `Preserve`, or
  `Point readers to` unless the text is explicitly a checklist item.
- Use the shared no-network reader layer when rendering tracked explainers:
  reading progress, active-section navigation, local search, and copyable
  source chips. Do not add global simple/technical mode toggles or global
  expand/collapse buttons unless a later source-spec-backed task defines a
  page-specific need and browser-verifies it. The helper script is
  `scripts/enhance_html_explainers.py`; preserve source-spec authority and do
  not treat that helper as an independent HTML source.
- Tracked public HTML must not use external runtime dependencies: no NPX,
  `@agent-native/core`, hosted Plan MCP, localhost bridge artifacts, CDN
  scripts, remote CSS, remote fonts, hosted comments, external analytics, or
  browser-side Mermaid execution. Use build-time inline SVG or local semantic
  diagram markup for visuals.
- The summary prose should be manually authored per source spec. Do not derive
  `subject_summary` automatically from source files. Target 150-240 words,
  excluding visible source chips, as a review guideline rather than a validator
  rule.
- For corrective revamps, the source spec may intentionally reset the rendered
  explanation from zero. Existing tracked HTML is a generated derivative and may
  be replaced wholesale after the source spec and source bundle are inspected.
  Do not preserve self-referential prose merely because it appears in the old
  HTML.
- Validator scope remains deterministic and structural: required fields,
  allowed profile values, nonblank intent, content-block markers, source-path
  evidence, subject-summary order, subject-summary field markers, declared
  subject-summary sources, obsolete summary-label rejection, required controls,
  obsolete analysis-capsule rejection, boilerplate rejection, hashes, and Mermaid
  parity. Quality, completeness, rendered geometry, and visual judgment remain
  source-spec review and browser QA responsibilities.
- Do not add a full deterministic HTML generator for flexible presentation.
  The Documentation Curator or LLM renderer chooses the best exposition from
  the source spec; validators enforce structural evidence.
- Mermaid use is profile-guided, not universal. `memory_system_map`,
  `workflow_lifecycle`, `claim_boundary_map`, and `atlas_hub` normally benefit
  from registered Mermaid diagrams. `role_catalog`, `format_ladder`, and
  `technical_requirements` may be clearer as catalogs, tables, tier cards, or
  evidence matrices.
- Three-layer model sections must remain readable at desktop and mobile
  widths. Use a stacked `.layer-strip` (`grid-template-columns: 1fr`) and make
  cards inside each layer auto-fit with a minimum readable width, for example
  `.layer .card-grid { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }`.
  Do not nest a fixed three-column `.card-grid` inside a fixed three-column
  `.layer-strip`.
- Normal prose must use `overflow-wrap: break-word`; reserve
  `overflow-wrap: anywhere` for `code` and `pre` where long paths or hashes may
  otherwise overflow.
- Active tracked explainers must not render the obsolete
  `Analysis capsules` / `Claim-Aware Analysis` section, `data-analysis-capsule`
  markers, or `data-capsule-field` markers.
- If the source spec declares `mermaid_diagrams` or the Markdown source
  contains registered Mermaid blocks, tracked HTML generation must follow
  `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`.
  Registered Mermaid-backed tracked HTML must be single-file portable: embed
  build-time sanitized inline SVG in the diagram shell, preserve the Mermaid
  source in `script.diagram-source`, and do not import or execute Mermaid in the
  browser.
- Diagram-backed boxes must adapt to the rendered inline SVG aspect
  ratio. Read the SVG natural size from `viewBox`, set the diagram box height
  from `height / width * available_width` within bounded min/max limits, and
  make the Fit control recompute that viewBox-based fit. Do not leave Mermaid
  SVGs constrained by browser intrinsic sizing or a fixed `max-width` cap that
  makes wide diagrams render as small strips.
- `html-visual-explainer` governs tracked `html/` output registration and
  source-binding rules.
- `visual-explainer` may be used for visual layout and rendering.
- HTML is human-only and never scientific, control, or registry authority.
- Direct HTML-only edits are blocked. Modify the Markdown source spec, then
  regenerate the HTML output.

Implementation metadata is validated by:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

`--check` is a compatibility alias, but new instructions should use
`--validate-only`.

Visual Atlas v2 coverage and portability are additionally validated by:

```zsh
.venv/bin/python scripts/validate_explainer_topic_coverage.py --root .
.venv/bin/python scripts/validate_explainer_parity.py --root .
.venv/bin/python scripts/validate_standalone_html.py --root .
.venv/bin/python scripts/validate_reader_first_docs.py --root .
.venv/bin/python scripts/validate_explainer_diagrams.py --root .
```
