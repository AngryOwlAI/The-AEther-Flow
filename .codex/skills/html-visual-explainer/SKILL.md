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
  `analysis_depth: "simple_and_deep"`, `required_controls`,
  `source_drilldowns`, and `analysis_capsule_schema`.
- `explainer_kind` must be one of `project_overview`, `conceptual_model`,
  `workflow_process`, or `control_system`.
- Every explainer requires `simple_deep_toggle`, `section_toc`,
  `expandable_analysis_panels`, `source_drilldowns`, and
  `claim_boundary_toggle`. `workflow_step_inspector` is required for
  `workflow_process` and `control_system` explainers.
- The Markdown body must include `## Required Analysis Capsules` and name each
  capsule field: `premise`, `mechanism`, `source_basis`, `authority_status`,
  `uncertainty`, `validation_or_test`, and `next_step`.
- The generated HTML must include lightweight structural markers:
  `data-explainer-control="<control>"`, at least one `data-analysis-capsule`,
  `data-capsule-field="<field>"`, and `data-source-path` for source
  drilldowns. Validation checks marker presence, not visual design or
  JavaScript behavior.
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
