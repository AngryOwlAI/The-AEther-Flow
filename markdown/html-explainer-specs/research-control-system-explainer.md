---
topic_id: "TOPIC-RESEARCH-CONTROL-SYSTEM"
explainer_subject: "Research Control System"
reader_question: "How does tracked research-control state preserve task history, completions, approvals, and handoffs?"
title: "Research Control System"
purpose: "Explain the research-control system as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/research-control-system-explainer.html"
github_markdown_output_path: "github-facing/research-control-system-explainer.md"
wiki_output_path: "wiki/html/html-research-control-system-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - "registries/RESEARCH_TASK_REGISTRY.csv"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - "registries/AGENT_JOB_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Research Control System. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Research Control System."
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
  - id: "research-control-system-map"
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
    - "research-control-system-map"
---

# Research Control System Spec

## Rendering Intent

Teach the research-control system as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: research-control-system-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Research Control System"]
  B["Research Control System"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Research Control System`

Summary text:

The research-control system is the tracked state spine for tasks, Director decisions, AgentJobs, execution roles, artifacts, completions, approvals, handoffs, and documentation-impact receipts. It preserves project history and makes bounded work auditable. It supports both physics continuation and project-system improvement while keeping generated caches and local retrieval surfaces subordinate to tracked state.

Summary source basis:

- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `registries/RESEARCH_TASK_REGISTRY.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of Research Control System with plain-language grounding in `AGENTS.md` and `research_control/README.md`.
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
