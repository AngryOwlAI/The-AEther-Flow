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
- The source spec must also declare the interactive analysis contract:
  `explainer_kind`, `interaction_model: "progressive_disclosure"`,
  `analysis_depth: "deep"`, `required_controls`,
  `source_drilldowns`, and `analysis_capsule_schema`.
- The source spec must also declare the flexible presentation contract:
  `presentation_profile`, `layout_intent`, and
  `required_content_blocks`.
- `explainer_kind` must be one of `project_overview`, `conceptual_model`,
  `workflow_process`, or `control_system`.
- `presentation_profile` is a layout archetype, not a hidden content-rule
  engine. It must be one of `atlas_hub`, `role_catalog`, `format_ladder`,
  `memory_system_map`, `workflow_lifecycle`, `technical_requirements`,
  `conceptual_model`, or `claim_boundary_map`.
- `layout_intent` must be nonblank prose explaining how this page should adapt
  the chosen profile.
- `required_content_blocks` must be a non-empty list of page-local IDs using
  lowercase snake_case. Each ID must be explained in a Markdown
  `## Required Content Blocks` section.
- Every explainer requires `section_toc`, `expandable_analysis_panels`,
  `source_drilldowns`, and `claim_boundary_toggle`.
  `workflow_step_inspector` is required for
  `workflow_process` and `control_system` explainers.
- The Markdown body must include `## Required Analysis Capsules` and name each
  capsule field: `premise`, `mechanism`, `source_basis`, `authority_status`,
  `uncertainty`, `validation_or_test`, and `next_step`.
- The generated HTML must include lightweight structural markers:
  `data-explainer-control="<control>"`, at least one `data-analysis-capsule`,
  `data-capsule-field="<field>"`, and `data-source-path` for source
  drilldowns. Validation checks marker presence, not visual design or
  JavaScript behavior.
- The generated HTML must include each declared content block as
  `data-content-block="<id>"`. Each content block must contain at least one
  `data-source-path` marker. The visual form can be a table, matrix, card
  group, sidebar, callout, inspector panel, accordion, or other appropriate
  source-backed presentation for the chosen profile.
- Validator scope remains deterministic and structural: required fields,
  allowed profile values, nonblank intent, content-block markers, source-path
  evidence, required controls, analysis capsule markers, hashes, and Mermaid
  parity. Quality, completeness, and visual judgment remain source-spec review
  and visual QA responsibilities.
- Do not add a full deterministic HTML generator for flexible presentation.
  The Documentation Curator or LLM renderer chooses the best exposition from
  the source spec; validators enforce structural evidence.
- Mermaid use is profile-guided, not universal. `memory_system_map`,
  `workflow_lifecycle`, `claim_boundary_map`, and `atlas_hub` normally benefit
  from governed Mermaid. `role_catalog`, `format_ladder`, and
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
- Analysis capsule rows must be allowed to shrink on mobile. Use
  `min-width: 0` on capsule rows, `dt`, and `dd`, and keep capsule `dl` tracks
  at `minmax(0, 1fr)` so labeled evidence rows do not create horizontal page
  overflow.
- If the source spec declares `mermaid_diagrams` or the Markdown source
  contains governed Mermaid blocks, tracked HTML generation must follow
  `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`.
  Governed Mermaid-backed tracked HTML must be single-file portable: embed
  build-time sanitized inline SVG in the diagram shell, preserve the Mermaid
  source in `script.diagram-source`, and do not import or execute Mermaid in the
  browser.
- Governed Mermaid diagram boxes must adapt to the rendered inline SVG aspect
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
