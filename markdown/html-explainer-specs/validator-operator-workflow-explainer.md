---
topic_id: "TOPIC-VALIDATOR-OPERATOR-WORKFLOW"
explainer_subject: "Validator And Operator Workflow"
reader_question: "Which checks should an operator run, what does each protect, and what does PASS not prove?"
title: "Validator And Operator Workflow"
purpose: "Explain the validator and operator workflow as a source-backed Visual Atlas topic without changing project authority."
audience: "Technical but human-readable: maintainers, research agents, reviewers, and GitHub readers."
output_path: "html/validator-operator-workflow-explainer.html"
github_markdown_output_path: "github-facing/validator-operator-workflow-explainer.md"
wiki_output_path: "wiki/html/html-validator-operator-workflow-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - "scripts/project_control/audit_documentation_surfaces.py"
  - "scripts/validate_explainer_topic_coverage.py"
  - "scripts/validate_explainer_parity.py"
  - "scripts/validate_standalone_html.py"
  - "scripts/validate_reader_first_docs.py"
  - "scripts/validate_explainer_diagrams.py"
  - "scripts/spec_depth_lint.py"
  - "scripts/validate_teaching_qa.py"
claim_boundary: "Human-only Visual Atlas explainer for Validator And Operator Workflow. It teaches the project mechanism without creating physics claims, control authority, role authority, routing behavior, validator behavior, write permissions, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "technical_requirements"
layout_intent: "Use a concept-first atlas layout with a system map, authority matrix, examples, non-examples, source chips, and next-reading path for Validator And Operator Workflow."
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
  - id: "validator-operator-workflow-map"
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
    - "validator-operator-workflow-map"
---

# Validator And Operator Workflow Spec

## Rendering Intent

Teach the validator and operator workflow as a source-backed project mechanism. The explanation must start from the subject, not from page metadata, renderer behavior, or derivative status. Generated outputs remain human-readable derivatives.

## Required Diagrams

<!-- mermaid-diagram-id: validator-operator-workflow-map -->
```mermaid
flowchart TD
  A["Source bundle"] --> B["Validator And Operator Workflow"]
  B["Validator And Operator Workflow"] --> C["Reader model"]
  C["Reader model"] --> D["Source-backed output"]
  D["Source-backed output"] --> E["Validation"]
```

## Source-Backed Summary

Summary heading: `Summary of Validator And Operator Workflow`

Summary text:

Validator and operator workflow is the practical command map for safe project work. Bootstrap refreshes registries and generated wiki/retrieval surfaces; validate-only checks the current state; atlas validators check concept coverage, parity, standalone HTML, reader-first structure, and diagrams; depth and teaching validators catch shallow or unsupported docs; documentation-impact and research-control validators protect control receipts and job boundaries. PASS means the checked contract holds, not that physics claims are true.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `scripts/project_control/audit_documentation_surfaces.py`

## Required Content Blocks

- subject_summary: A source-backed summary of Validator And Operator Workflow with plain-language grounding in `AGENTS.md` and `.codex/skills/improve-project-system/SKILL.md`.
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
