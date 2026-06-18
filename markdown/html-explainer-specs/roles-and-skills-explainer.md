---
topic_id: "TOPIC-ROLES-SKILLS-CATALOG"
explainer_subject: "Roles And Skills Catalog"
reader_question: "Which role and skill contracts govern work, and why is availability not authority?"
title: "Roles And Skills Catalog"
purpose: "Explain the roles and skills catalog as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/roles-and-skills-explainer.html"
github_markdown_output_path: "github-facing/roles-and-skills-explainer.md"
wiki_output_path: "wiki/html/html-roles-and-skills-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - ".agents/roles/research_ops/documentation-curator.v1.0.0.md"
  - ".agents/roles/research_ops/documentation-student.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-teacher.v0.1.0.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
claim_boundary: "Human-only Visual Atlas explainer for Roles And Skills Catalog. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "role_catalog"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Roles And Skills Catalog."
required_controls:
  - "section_toc"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "what_this_does"
  - "why_aether_needs_it"
  - "system_map"
  - "how_it_works"
  - "objects_and_authority"
  - "example"
  - "non_example"
  - "common_confusions"
  - "what_this_does_not_authorize"
  - "source_map"
  - "next_reading_path"
primary_visuals:
  - id: "roles-skills-catalog-map"
    type: "mermaid"
    required_in_github_markdown: true
    required_in_html: true
reader_blocks:
  - "what_this_does"
  - "why_aether_needs_it"
  - "system_map"
  - "how_it_works"
  - "objects_and_authority"
  - "example"
  - "non_example"
  - "common_confusions"
  - "what_this_does_not_authorize"
  - "source_map"
  - "next_reading_path"
github_markdown_parity: true
standalone_html: true
no_external_runtime: true
mermaid_diagrams:
  required: true
  ids:
    - "roles-skills-catalog-map"
---

# Roles And Skills Catalog Spec

## Rendering Intent

Teach the roles and skills catalog as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: roles-skills-catalog-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Roles And Skills Catalog"]
  B["Roles And Skills Catalog"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Roles And Skills Catalog`

Summary text:

The roles and skills catalog lists the project-governed execution roles and local skill front doors that structure work. It separates stable role authority, historical versions, task-local overlays, support subroles, and general tool availability. This matters because having a skill or tool available does not authorize source edits; only the selected role, AgentJob allowlist, and project-control contract do.

Summary source basis:

- `registries/AGENT_ROLE_REGISTRY.csv`
- `.agents/roles/research_ops/documentation-curator.v1.0.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Roles And Skills Catalog with plain-language grounding in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `registries/AGENT_ROLE_REGISTRY.csv` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
