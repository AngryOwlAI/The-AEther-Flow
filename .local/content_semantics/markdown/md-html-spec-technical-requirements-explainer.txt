---
title: "Technical Requirements"
purpose: "Explain tiered technical requirements for reading, validating, regenerating memory/wiki surfaces, rendering diagram-backed HTML, using local retrieval, and refreshing PDFs."
audience: "Technical but human-readable: maintainers and operators who need to run or regenerate project surfaces without confusing project requirements with local operator aids."
output_path: "html/technical-requirements-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "requirements.txt"
  - "Makefile"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/obsidian-wiki/SKILL.md"
  - ".codex/skills/pdf-derivative-build/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md"
  - ".codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package.json"
  - ".codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package-lock.json"
claim_boundary: "Human-only technical-requirements visualization. It explains existing setup tiers and regeneration requirements without changing dependency policy, validator behavior, scripts, role authority, or scientific claim status."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "technical_requirements"
layout_intent: "Use a tiered requirements matrix with project-requirement versus operator-environment-aid labels, command callouts, and source-backed setup evidence."
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "read_inspect_tier"
  - "validators_memory_scripts_tier"
  - "memory_regeneration_tier"
  - "diagram_rendering_tier"
  - "local_retrieval_tier"
  - "pdf_refresh_tier"
  - "project_vs_operator_aid"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
---

# Technical Requirements Spec

## Rendering Intent

Create a tracked HTML drilldown that explains requirements by workflow tier,
not as one undifferentiated dependency list.

Use two labels:

- Project requirement: required by tracked scripts/contracts in this repo.
- Operator environment aid: useful in this machine or session, but not
  required project authority.

Examples:

- Python `.venv` plus `requirements.txt`: project requirement for validators
  and memory scripts.
- Node.js, npm, Mermaid package, and Playwright Chromium: project requirement
  when regenerating Mermaid-backed tracked HTML.
- Obsidian app: optional operator environment aid for reading the generated
  local vault.
- Codex global skills or plugins: operator environment aid unless mirrored into
  `.codex/skills/`.

## Required Visual Structure

- Tiered requirements matrix with commands and labels.
- Setup command callouts for Python and diagram rendering.
- Optional-local-reader panel for Obsidian and `.local/` retrieval surfaces.
- PDF-refresh panel that scopes LaTeX only to TeX derivative work.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Content Blocks

- subject_summary: Summarize what the technical requirements explainer covers,
  how it separates read-only inspection, validation, regeneration, diagram
  rendering, local retrieval, and PDF refresh tiers, why readers need that
  distinction, and which sources ground the summary.
- read_inspect_tier: Explain browser, text editor, and Git as the minimum
  read/inspect layer.
- validators_memory_scripts_tier: Explain Python `.venv`, `requirements.txt`,
  PyMuPDF, and Python validator commands.
- memory_regeneration_tier: Explain project-memory-system scripts and `make
  validate-memory` for regenerating registries, wiki, vault sync, and query
  checks.
- diagram_rendering_tier: Explain Node.js, npm, pinned Mermaid package,
  Playwright Chromium, and the inline-SVG renderer path.
- local_retrieval_tier: Explain optional Obsidian and
  `.local/obsidian/aether-flow-wiki/` plus local semantic/query surfaces.
- pdf_refresh_tier: Explain LaTeX/PDF build requirements only when TeX
  derivatives are in scope.
- project_vs_operator_aid: Label each requirement as project requirement or
  operator environment aid.

## Required Analysis Capsules

### Requirements Are Tiered

- premise: Not every reader or operator needs every tool.
- mechanism: The page should separate read-only inspection, Python validation,
  memory regeneration, diagram rendering, optional local retrieval,
  and PDF refresh work into distinct tiers.
- source_basis: `README.md`, `requirements.txt`, `Makefile`,
  `.codex/skills/project-memory-system/SKILL.md`, and Mermaid subskill setup
  documentation.
- authority_status: Human-only setup explanation; tracked scripts and contracts
  define project requirements.
- uncertainty: System-level tool availability can differ across machines.
- validation_or_test: Run the tier-specific command after installing the tier,
  such as bootstrap validation, renderer `--check`, local vault lint, or PDF
  build validation.
- next_step: Install the lowest tier needed for the intended workflow before
  running broader validation.

### Operator Aids Are Not Project Authority

- premise: The current Codex workspace may expose useful tools that are not
  durable project requirements.
- mechanism: Label Obsidian, global Codex skills, plugins, and bundled tools
  as operator environment aids unless the requirement is tracked in this repo.
- source_basis: `.codex/skills/obsidian-wiki/SKILL.md`, `.codex/skills/*`,
  and `README.md`.
- authority_status: Explanation of requirement boundaries.
- uncertainty: A future task may promote an aid into a project requirement by
  adding tracked contracts, scripts, or registry documentation.
- validation_or_test: Check whether the requirement appears in tracked docs,
  scripts, `requirements.txt`, or package manifests.
- next_step: Keep README commands concise and use this explainer for the
  richer tiered model.

## Non-Goals

- Do not change dependency versions or install new tools.
- Do not make Obsidian or global Codex plugins required project authority.
- Do not change validator behavior or scripts.
- Do not introduce physics claims.
