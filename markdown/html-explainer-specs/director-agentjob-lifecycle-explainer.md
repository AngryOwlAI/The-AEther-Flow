---
topic_id: "TOPIC-DIRECTOR-AGENTJOB-LIFECYCLE"
explainer_subject: "Director Decisions And AgentJob Lifecycle"
reader_question: "How does a Director decision become one bounded job, one output, one completion, and one next state?"
title: "Director Decisions And AgentJob Lifecycle"
purpose: "Explain Director decisions and AgentJob lifecycle as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/director-agentjob-lifecycle-explainer.html"
github_markdown_output_path: "github-facing/director-agentjob-lifecycle-explainer.md"
wiki_output_path: "wiki/html/html-director-agentjob-lifecycle-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Director Decisions And AgentJob Lifecycle. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Director Decisions And AgentJob Lifecycle."
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
  - id: "director-agentjob-lifecycle-map"
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
    - "director-agentjob-lifecycle-map"
---

# Director Decisions And AgentJob Lifecycle Spec

## Rendering Intent

Teach Director decisions and AgentJob lifecycle as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: director-agentjob-lifecycle-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Director Decisions And AgentJob Lifecycle"]
  B["Director Decisions And AgentJob Lifecycle"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Director Decisions And AgentJob Lifecycle`

Summary text:

Director decisions and AgentJobs are the control path that prevents open-ended work. The Director selects a role and one bounded objective; the AgentJob records allowed reads, allowed writes, expected outputs, validators, stop conditions, and claim boundary; the execution role performs the work; the completion records command evidence and verdict; the handoff preserves the next state. This lifecycle is project-control authority, not physics authority.

Summary source basis:

- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Director Decisions And AgentJob Lifecycle with plain-language grounding in `AGENTS.md` and `research_control/README.md`.
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
