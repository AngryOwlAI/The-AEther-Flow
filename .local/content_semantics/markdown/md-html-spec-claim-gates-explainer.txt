---
topic_id: "TOPIC-CLAIM-GATES-NEGATIVE-RESULTS-FREEZE"
explainer_subject: "Claim Gates, Negative Results, And Freeze Criteria"
reader_question: "How does the project preserve failures and prevent premature claim promotion?"
title: "Claim Gates, Negative Results, And Freeze Criteria"
purpose: "Explain claim gates, negative results, and freeze criteria as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/claim-gates-explainer.html"
github_markdown_output_path: "github-facing/claim-gates-explainer.md"
wiki_output_path: "wiki/html/html-claim-gates-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Claim Gates, Negative Results, And Freeze Criteria. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "claim_boundary_map"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Claim Gates, Negative Results, And Freeze Criteria."
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
  - id: "claim-gate-preservation-map"
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
    - "claim-gate-preservation-map"
---

# Claim Gates, Negative Results, And Freeze Criteria Spec

## Rendering Intent

Teach claim gates, negative results, and freeze criteria as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: claim-gate-preservation-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Claim Gates, Negative Results, And Freeze Criteria"]
  B["Claim Gates, Negative Results, And Freeze Criteria"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Claim Gates, Negative Results, And Freeze Criteria`

Summary text:

Claim gates, negative-result preservation, and freeze criteria keep speculative work from becoming unsupported certainty. A failed route, obstruction, scoped no-go result, or repeated burden is not erased; it becomes evidence that shapes later routing. Claim gates require authority before promotion, while freeze criteria prevent repeated work from consuming the project without new mathematical payload.

Summary source basis:

- `AGENTS.md`
- `research_control/README.md`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of Claim Gates, Negative Results, And Freeze Criteria with plain-language grounding in `AGENTS.md` and `research_control/README.md`.
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
