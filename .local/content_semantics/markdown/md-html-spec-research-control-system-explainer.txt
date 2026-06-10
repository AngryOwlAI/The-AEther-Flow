---
title: "Research-Control System Explainer"
purpose: "Provide a human-readable visual overview of the project authority chain, research-control loop, project-system improvement loop, and Documentation Curator v0.2.0 source-backed HTML boundary."
audience: "Project maintainers, research agents, and reviewers who need a compact mental model of the control system."
output_path: "html/research-control-system-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "README.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
  - ".agents/roles/research_ops/documentation-curator.v0.2.0.md"
  - "scripts/research_control/validate_research_control.py"
  - ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"
claim_boundary: "Human-only project-system visualization. It explains existing authority boundaries and validator behavior without changing physics claims, control contracts, routing decisions, or registry authority."
human_visual_only: true
---

# Research-Control System Explainer Spec

## Rendering Intent

Create a self-contained HTML explainer for the repository control system. The
page should emphasize the source-first authority hierarchy, the separation
between physics continuation and project-system improvement, and the
Documentation Curator v0.2.0 rule that tracked HTML is valid only when backed
by this Markdown source spec.

## Required Visual Structure

- An authority ladder showing canonical sources, registries, Markdown specs,
  and generated derivatives.
- A two-lane workflow view separating `continue-research` from
  `improve-project-system`.
- A Documentation Curator v0.2.0 panel showing spec-first HTML generation.
- A validator gate panel listing bootstrap, documentation-impact validation,
  research-control validation, project-improvement signal validation, tests,
  and diff checks.
- A claim-boundary notice stating that the page is human-only and
  non-authoritative.

## Non-Goals

- Do not introduce physics claims.
- Do not change project-control rules.
- Do not present generated HTML as an authority source.
- Do not use external images or network-dependent assets.
