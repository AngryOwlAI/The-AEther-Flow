---
topic_id: "TOPIC-PROJECT-SYSTEM-IMPROVEMENT-LOOP"
explainer_subject: "Project-System Improvement Loop"
reader_question: "How does the project repair its own documentation, validators, memory tooling, and control contracts without touching physics claims?"
title: "Project-System Improvement Loop"
purpose: "Explain the project-system improvement loop as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/project-system-improvement-explainer.html"
github_markdown_output_path: "github-facing/project-system-improvement-explainer.md"
wiki_output_path: "wiki/html/html-project-system-improvement-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Project-System Improvement Loop. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Project-System Improvement Loop."
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
  - id: "project-system-improvement-map"
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
    - "project-system-improvement-map"
---

# Project-System Improvement Loop Spec

## Rendering Intent

Teach the project-system improvement loop as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: project-system-improvement-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Project-System Improvement Loop"]
  B["Project-System Improvement Loop"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Project-System Improvement Loop`

Summary text:

The project-system improvement loop handles changes to roles, schemas, validators, memory tooling, documentation, generated-output governance, and operational reliability. It starts from classification, memory preflight, resolver state, and registered signals, then creates or reuses one bounded AgentJob. It is separate from physics continuation and must not promote claims or edit science sources as part of system repair.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/resolve_project_improvement.py`

## Required Content Blocks

- subject_summary: A source-backed summary of Project-System Improvement Loop with plain-language grounding in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
