---
topic_id: "TOPIC-AETHER-FLOW-ONTOLOGY"
explainer_subject: "AEther-Flow Ontology"
reader_question: "What ontology is being modeled, and where does ontology stop before empirical or derivational authority begins?"
title: "AEther-Flow Ontology"
purpose: "Explain the AEther-flow ontology as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/aether-flow-ontology-explainer.html"
github_markdown_output_path: "github-facing/aether-flow-ontology-explainer.md"
wiki_output_path: "wiki/html/html-aether-flow-ontology-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
claim_boundary: "Human-only Visual Atlas explainer for AEther-Flow Ontology. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "conceptual_model"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for AEther-Flow Ontology."
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
  - id: "ontology-model-map"
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
    - "ontology-model-map"
---

# AEther-Flow Ontology Spec

## Rendering Intent

Teach the AEther-flow ontology as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: ontology-model-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["AEther-Flow Ontology"]
  B["AEther-Flow Ontology"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of AEther-Flow Ontology`

Summary text:

AEther-Flow ontology names the project vocabulary for substrate, flow, relational structure, and the intended bridge toward relativistic geometry. Its function is to organize hypotheses and derivational targets, not to declare empirical acceptance. The ontology is useful only when its assumptions, mathematical objects, and claim boundaries are kept separate from generated explanations and from benchmark equations that have not yet been derived from the substrate.

Summary source basis:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `registries/TEX_SOURCE_REGISTRY.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of AEther-Flow Ontology with plain-language grounding in `README.md` and `AGENTS.md`.
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
