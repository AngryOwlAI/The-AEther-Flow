---
topic_id: "TOPIC-EXACT-GR-BENCHMARK-BOUNDARY"
explainer_subject: "Exact-GR Benchmark Boundary"
reader_question: "How does the project use exact general relativity without claiming the substrate derivation is finished?"
title: "Exact-GR Benchmark Boundary"
purpose: "Explain the exact-GR benchmark boundary as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/exact-gr-benchmark-boundary-explainer.html"
github_markdown_output_path: "github-facing/exact-gr-benchmark-boundary-explainer.md"
wiki_output_path: "wiki/html/html-exact-gr-benchmark-boundary-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for Exact-GR Benchmark Boundary. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "claim_boundary_map"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Exact-GR Benchmark Boundary."
required_controls:
  - "section_toc"
  - "source_materials_section"
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
  - id: "exact-gr-boundary-map"
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
    - "exact-gr-boundary-map"
---

# Exact-GR Benchmark Boundary Spec

## Rendering Intent

Teach the exact-GR benchmark boundary as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: exact-gr-boundary-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Exact-GR Benchmark Boundary"]
  B["Exact-GR Benchmark Boundary"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Exact-GR Benchmark Boundary`

Summary text:

The exact-GR benchmark boundary is the rule that ordinary general relativity supplies the comparison target while the first-principles derivation from AEther-flow substrate structure remains open. The boundary protects the difference between matching a known theory, importing a known equation, proposing a route, and deriving the route from authorized source-side assumptions. It is a claim-control mechanism as much as a physics orientation.

Summary source basis:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `research_control/design/gr_derivation_burden_map.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Exact-GR Benchmark Boundary with plain-language grounding in `README.md` and `AGENTS.md`.
- what_this_does: Plain-language reader block for What This Does grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- why_aether_needs_it: Plain-language reader block for Why AEther Needs It grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- system_map: Plain-language reader block for System Map grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- how_it_works: Plain-language reader block for How It Works grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- objects_and_authority: Plain-language reader block for Objects And Authority grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- example: Plain-language reader block for Example grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- non_example: Plain-language reader block for Non-Example grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- common_confusions: Plain-language reader block for Common Confusions grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- what_this_does_not_authorize: Plain-language reader block for What This Does Not Authorize grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- source_map: Plain-language reader block for Source Map grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
- next_reading_path: Plain-language reader block for Next Reading Path grounded in `README.md` and `AGENTS.md`; it must teach the project mechanism, preserve authority boundaries, and expose source evidence.
