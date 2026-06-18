---
topic_id: "TOPIC-DOC-CURATOR-TEACHING-LOOP"
explainer_subject: "Documentation Curator Teaching Loop"
reader_question: "How do Student, Teacher, packet, Curator, spec, GitHub Markdown, HTML, and wiki surfaces interact?"
title: "Documentation Curator Teaching Loop"
purpose: "Explain the Documentation Curator teaching loop as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/documentation-curator-teaching-loop-explainer.html"
github_markdown_output_path: "github-facing/documentation-curator-teaching-loop-explainer.md"
wiki_output_path: "wiki/html/html-documentation-curator-teaching-loop-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - ".agents/roles/research_ops/documentation-curator.v1.0.0.md"
  - ".agents/roles/research_ops/documentation-student.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-teacher.v0.1.0.md"
  - ".agents/schemas/TEACHING_QA_PACKET_SCHEMA.md"
  - "research_control/design/documentation_curator_visual_atlas_contract.md"
  - "registries/EXPLAINER_TOPIC_REGISTRY.csv"
  - "markdown/teaching-packets/documentation-curator-teaching-loop.teaching-qa.md"
claim_boundary: "Human-only Visual Atlas explainer for Documentation Curator Teaching Loop. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Documentation Curator Teaching Loop."
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
  - id: "teaching-loop-map"
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
    - "teaching-loop-map"
teaching_loop:
  enabled: true
  rounds: "2"
  student_role: "documentation-student@0.1.0"
  teacher_role: "documentation-teacher@0.1.0"
  audience_model: "technical_newcomer"
  qa_packet: "markdown/teaching-packets/documentation-curator-teaching-loop.teaching-qa.md"
  required_teaching_blocks:
    - "plain_language_model"
    - "glossary"
    - "guided_walkthrough"
    - "common_questions"
    - "examples_and_non_examples"
    - "misconception_repairs"
    - "check_your_understanding"
---

# Documentation Curator Teaching Loop Spec

## Rendering Intent

Teach the Documentation Curator teaching loop as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: teaching-loop-map -->
```mermaid
flowchart TD
  Subject["Selected subject"] --> Sources["Declared source bundle"]
  Sources --> Student["Documentation Student<br/>questions only"]
  Student --> Teacher["Documentation Teacher<br/>source-bound answers"]
  Teacher --> Packet["Curated Teaching Q&A packet"]
  Packet --> Curator["Documentation Curator<br/>writes the explanation"]
  Curator --> Spec["Markdown source spec"]
  Spec --> GitHub["GitHub-facing Markdown"]
  Spec --> HTML["Standalone HTML explainer"]
  Spec --> Wiki["Generated wiki/index surfaces"]
  GitHub --> Validation["Validation"]
  HTML --> Validation
  Wiki --> Validation
```

## Source-Backed Summary

Summary heading: `Summary of Documentation Curator Teaching Loop`

Summary text:

The Documentation Curator teaching loop improves explanations without changing authority. The Curator selects a subject and source bundle. Documentation Student asks reader-diagnostic questions. Documentation Teacher answers only from the selected sources. The Curator turns that support into a curated teaching packet, a Markdown source spec, GitHub-facing Markdown, tracked standalone HTML, and generated wiki navigation surfaces. Student and Teacher do not write tracked docs directly.

Summary source basis:

- `AGENTS.md`
- `.agents/roles/research_ops/documentation-curator.v1.0.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Documentation Curator Teaching Loop with plain-language grounding in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `AGENTS.md` and `.agents/roles/research_ops/documentation-curator.v1.0.0.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.

## Teaching Q&A Basis

This topic uses `markdown/teaching-packets/documentation-curator-teaching-loop.teaching-qa.md` as explanatory support only. The packet helps the Documentation Curator identify plain-language questions, examples, non-examples, common confusions, source gaps, and boundaries. It does not create project behavior, role authority, routing behavior, validator behavior, claim status, ontology authority, benchmark authority, or generated-output authority.
