---
topic_id: "TOPIC-PARENT-CHILD-SYNTHESIS"
explainer_subject: "Parent-Child Parallel Synthesis"
reader_question: "How can one AgentJob use parent and child perspectives without creating extra authority?"
title: "Parent-Child Parallel Synthesis"
purpose: "Explain parent-child parallel synthesis as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/parent-child-synthesis-explainer.html"
github_markdown_output_path: "github-facing/parent-child-synthesis-explainer.md"
wiki_output_path: "wiki/html/html-parent-child-synthesis-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Parent-Child Parallel Synthesis. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Parent-Child Parallel Synthesis."
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
  - id: "parent-child-authority-map"
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
    - "parent-child-authority-map"
teaching_loop:
  enabled: true
  rounds: "2"
  student_role: "documentation-student@0.1.0"
  teacher_role: "documentation-teacher@0.1.0"
  audience_model: "technical_newcomer"
  qa_packet: "markdown/teaching-packets/parent-child-synthesis.teaching-qa.md"
  required_teaching_blocks:
    - "plain_language_model"
    - "glossary"
    - "guided_walkthrough"
    - "common_questions"
    - "examples_and_non_examples"
    - "misconception_repairs"
    - "check_your_understanding"
---

# Parent-Child Parallel Synthesis Spec

## Rendering Intent

Teach parent-child parallel synthesis as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: parent-child-authority-map -->
```mermaid
flowchart TD
  State["Tracked state or handoff"] --> Director["Director decision"]
  Director --> Job["One bounded AgentJob"]
  Job --> Role["One execution-role contract"]
  Role --> Parent["Parent unit<br/>synthesis and arbitration"]
  Role --> ChildA["Child unit A<br/>perspective 1"]
  Role --> ChildB["Child unit B<br/>perspective 2"]
  ChildA --> Fusion["Conflict resolution<br/>and fused output"]
  ChildB --> Fusion
  Parent --> Fusion
  Fusion --> Artifact["One final artifact"]
  Artifact --> Validators["Validators"]
  Validators --> Completion["One completion record"]
  Completion --> Handoff["Next handoff"]
```

## Source-Backed Summary

Summary heading: `Summary of Parent-Child Parallel Synthesis`

Summary text:

Parent-child parallel synthesis increases analytical pressure inside one bounded AgentJob. A parent unit and two child-perspective units may examine the same problem from different angles, but all units inherit the outer job source restrictions, write allowlist, validators, stop conditions, claim boundary, and execution-role contract. Child outputs are support artifacts. The parent resolves conflicts into one fused output, one validation path, one completion record, and one handoff.

Summary source basis:

- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Parent-Child Parallel Synthesis with plain-language grounding in `AGENTS.md` and `research_control/README.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `AGENTS.md` and `research_control/README.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.

## Teaching Q&A Basis

This topic uses `markdown/teaching-packets/parent-child-synthesis.teaching-qa.md` as explanatory support only. The packet helps the Documentation Curator identify plain-language questions, examples, non-examples, common confusions, source gaps, and boundaries. It does not create project behavior, role authority, routing behavior, validator behavior, claim status, ontology authority, benchmark authority, or generated-output authority.
