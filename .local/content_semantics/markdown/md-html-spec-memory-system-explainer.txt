---
topic_id: "TOPIC-MEMORY-REGISTRIES-WIKI-RETRIEVAL"
explainer_subject: "Memory, Registries, Wiki, And Retrieval Surfaces"
reader_question: "How do registries, wiki notes, semantic extracts, and local memory help without overriding sources?"
title: "Memory, Registries, Wiki, And Retrieval Surfaces"
purpose: "Explain memory, registries, wiki, and retrieval surfaces as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/memory-system-explainer.html"
github_markdown_output_path: "github-facing/memory-system-explainer.md"
wiki_output_path: "wiki/html/html-memory-system-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
  - ".codex/skills/obsidian-wiki/SKILL.md"
claim_boundary: "Human-only Visual Atlas explainer for Memory, Registries, Wiki, And Retrieval Surfaces. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "memory_system_map"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Memory, Registries, Wiki, And Retrieval Surfaces."
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
  - id: "memory-registry-retrieval-map"
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
    - "memory-registry-retrieval-map"
---

# Memory, Registries, Wiki, And Retrieval Surfaces Spec

## Rendering Intent

Teach memory, registries, wiki, and retrieval surfaces as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: memory-registry-retrieval-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Memory, Registries, Wiki, And Retrieval Surfaces"]
  B["Memory, Registries, Wiki, And Retrieval Surfaces"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Memory, Registries, Wiki, And Retrieval Surfaces`

Summary text:

The memory system connects tracked source objects to generated wiki notes, indexes, semantic extracts, relationship rows, file-object rows, and local retrieval surfaces. Its purpose is discoverability and auditability: it helps agents find the right source and see whether generated outputs are stale. It does not let local memory override tracked sources, control state, registries, or validation failures.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of Memory, Registries, Wiki, And Retrieval Surfaces with plain-language grounding in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
