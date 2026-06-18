---
topic_id: "TOPIC-SOURCE-AUTHORITY-GENERATED-DERIVATIVES"
explainer_subject: "Source Authority And Generated Derivatives"
reader_question: "Which files define project truth, and which files are reader or retrieval derivatives?"
title: "Source Authority And Generated Derivatives"
purpose: "Explain source authority and generated derivatives as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/source-authority-explainer.html"
github_markdown_output_path: "github-facing/source-authority-explainer.md"
wiki_output_path: "wiki/html/html-source-authority-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Source Authority And Generated Derivatives. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "format_ladder"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Source Authority And Generated Derivatives."
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
  - id: "source-authority-trust-map"
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
    - "source-authority-trust-map"
teaching_loop:
  enabled: true
  rounds: "2"
  student_role: "documentation-student@0.1.0"
  teacher_role: "documentation-teacher@0.1.0"
  audience_model: "technical_newcomer"
  qa_packet: "markdown/teaching-packets/source-authority.teaching-qa.md"
  required_teaching_blocks:
    - "plain_language_model"
    - "glossary"
    - "guided_walkthrough"
    - "common_questions"
    - "examples_and_non_examples"
    - "misconception_repairs"
    - "check_your_understanding"
---

# Source Authority And Generated Derivatives Spec

## Rendering Intent

Teach source authority and generated derivatives as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: source-authority-trust-map -->
```mermaid
flowchart TD
  Tex["Registered TeX<br/>physics authority"] --> PDF["PDF derivatives"]
  Reg["Registries<br/>routing/provenance authority"] --> Wiki["Wiki/index derivatives"]
  MD["Registered Markdown<br/>front-door/control/source specs"] --> GH["GitHub-facing Markdown"]
  MD --> HTML["Standalone HTML explainers"]
  Local[".local scratch/cache<br/>non-authority"] -.-> Human["Reader convenience only"]
  Tex --> Claims["Scientific claim status"]
  Reg --> Routing["Routing and provenance"]
  MD --> Guidance["Project guidance and explainer contracts"]
  PDF -.-> Read["Human reading"]
  Wiki -.-> Navigate["Navigation/search"]
  GH -.-> Orient["GitHub orientation"]
  HTML -.-> Teach["Visual teaching"]
```

## Source-Backed Summary

Summary heading: `Summary of Source Authority And Generated Derivatives`

Summary text:

Source authority and generated derivatives form the trust map of AEther-Flow. Registered TeX carries physics and derivational claims; registries carry provenance, routing, generated-output, and memory fields; registered Markdown carries guidance, role and skill contracts, source specs, and control notes. HTML, GitHub-facing Markdown, wiki notes, PDFs, semantic extracts, Obsidian notes, and local caches are useful only because they point back to authority.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of Source Authority And Generated Derivatives with plain-language grounding in `AGENTS.md` and `.codex/skills/project-memory-system/SKILL.md`.
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

## Teaching Q&A Basis

This topic uses `markdown/teaching-packets/source-authority.teaching-qa.md` as explanatory support only. The packet helps the Documentation Curator identify plain-language questions, examples, non-examples, common confusions, source gaps, and boundaries. It does not create project behavior, role authority, routing behavior, validator behavior, claim status, ontology authority, benchmark authority, or generated-output authority.
