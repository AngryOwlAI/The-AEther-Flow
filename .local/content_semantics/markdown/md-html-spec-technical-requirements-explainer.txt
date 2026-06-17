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

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Tiered requirements matrix with commands and labels.
- Setup command callouts for Python and diagram rendering.
- Optional-local-reader panel for Obsidian and `.local/` retrieval surfaces.
- PDF-refresh panel that scopes LaTeX only to TeX derivative work.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Source-Backed Summary

Summary heading: `Summary of Technical Requirements`

Summary text:

The technical requirements explainer describes the local runtime, package, validation, rendering, retrieval, and derivative-build requirements needed to inspect or regenerate project surfaces safely. Its function is to separate read-only inspection, Python validator execution, memory and wiki regeneration, governed Mermaid inline-SVG rendering, local Obsidian or semantic retrieval, and LaTeX/PDF refresh into distinct tiers. This matters because not every reader needs every tool, and optional operator aids such as Obsidian or global Codex plugins should not be mistaken for project authority. The requirements map turns setup files and skill contracts into a practical dependency model for maintainers who need repeatable validation without changing dependency policy or scientific claims.

Summary source basis:

- `README.md`
- `requirements.txt`
- `Makefile`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package.json`


## Required Content Blocks

- subject_summary: A source-backed summary of Technical Requirements that directly explains the project subject, its functionality, why it matters, how it fits the physics or AI research-agent system, and its grounding source paths: `README.md`, `requirements.txt`, `Makefile`, `.codex/skills/project-memory-system/SKILL.md`.
- read_inspect_tier: A source-backed reader block on read and inspect that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `README.md`, `AGENTS.md`.
- validators_memory_scripts_tier: A source-backed reader block on python validators that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `requirements.txt`, `Makefile`, `.codex/skills/project-memory-system/SKILL.md`.
- memory_regeneration_tier: A source-backed reader block on memory regeneration that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `.codex/skills/project-memory-system/SKILL.md`, `.codex/skills/markdown-wiki/SKILL.md`.
- diagram_rendering_tier: A source-backed reader block on diagram rendering that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`, `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package.json`.
- local_retrieval_tier: A source-backed reader block on local retrieval that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `.codex/skills/obsidian-wiki/SKILL.md`, `.codex/skills/project-memory-system/SKILL.md`.
- pdf_refresh_tier: A source-backed reader block on pdf refresh that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `.codex/skills/pdf-derivative-build/SKILL.md`, `registries/PDF_DERIVATIVE_REGISTRY.csv`.
- project_vs_operator_aid: A source-backed reader block on requirement boundary that explains the project functionality, why it matters, how it works inside AEther-Flow, what boundary constrains it, and where to inspect next; source paths: `README.md`, `AGENTS.md`.
