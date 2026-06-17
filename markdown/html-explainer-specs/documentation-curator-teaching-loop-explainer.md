---
title: "Documentation Curator Teaching Loop"
purpose: "Explain the Documentation Curator's subject-first teaching loop, including Student questions, Teacher answers, curated packets, source specs, GitHub-facing Markdown, and HTML derivatives."
audience: "Maintainers, documentation agents, and reviewers who need to understand how teaching-enriched explainers are produced without making teaching packets or generated pages authoritative."
output_path: "html/documentation-curator-teaching-loop-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - ".agents/roles/research_ops/documentation-curator.v0.9.0.md"
  - ".agents/roles/research_ops/documentation-student.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-teacher.v0.1.0.md"
  - ".agents/schemas/TEACHING_QA_PACKET_SCHEMA.md"
  - ".codex/skills/aether-teaching-explainer/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "research_control/design/github_facing_explainer_contract.md"
  - "markdown/teaching-packets/project-overview.teaching-qa.md"
  - "markdown/teaching-packets/role-routing.teaching-qa.md"
  - "scripts/validate_teaching_qa.py"
claim_boundary: "Human-only Documentation Curator teaching-loop explainer. It may summarize subject-first documentation, Student questions, Teacher answers, curated Q&A packets, source-spec distillation, GitHub-facing Markdown, HTML derivatives, and validators, but it does not change role authority, schemas, validators, routing, claim status, or generated-output authority."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a teaching-loop lifecycle view that follows source selection, Student questions, Teacher answers, Curator synthesis, spec updates, derivative refresh, and validation."
required_controls:
  - "section_toc"
  - "workflow_step_inspector"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "curator_authority"
  - "student_teacher_loop"
  - "packet_schema"
  - "derivative_sync"
  - "advisory_format_boundary"
---

# Documentation Curator Teaching Loop Spec

## Rendering Intent

Create a source-backed explainer for the Documentation Curator teaching loop.
The subject is the governed method for improving explanations: the Curator
selects a source bundle, the Student asks lay-reader questions, the Teacher
answers inside the source boundary, the Curator synthesizes a teaching packet,
and the packet is distilled into source specs, GitHub-facing Markdown, and
HTML derivatives.

The page should make two boundaries obvious. First, the Curator is the only
documentation writer in the loop; Student and Teacher are support subroles.
Second, the teaching packet and generated derivatives are explanatory support,
not authority for physics, routing, validators, schemas, roles, or generated
outputs.

## Source-Backed Summary

Summary heading: `Summary of Documentation Curator Teaching Loop`

Summary text:

The Documentation Curator teaching loop is the project's method for making source-backed explainers easier to understand without weakening authority boundaries. The Curator chooses a subject and source bundle, then uses a Documentation Student to ask plain reader-centered questions and a Documentation Teacher to answer those questions inside the declared source bundle. The Curator reviews the exchange, writes or updates a curated Teaching Q&A packet, and distills that packet into the Markdown source spec, GitHub-facing Markdown, and tracked human-only HTML derivative. The loop is subject-first: it must explain what the project component does, why the project needs it, how it works, what it can and cannot claim, and where a reader should go next. It does not let generated pages, teaching packets, Student questions, or Teacher answers become independent authority.

Summary source basis:

- `.agents/roles/research_ops/documentation-curator.v0.9.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`
- `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`

## Required Content Blocks

- subject_summary: A source-backed summary of Documentation Curator Teaching Loop that directly explains the teaching method, role split, subject-first rule, derivative outputs, and nonauthority boundary: `.agents/roles/research_ops/documentation-curator.v0.9.0.md`, `.agents/roles/research_ops/documentation-student.v0.1.0.md`, `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`, `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`.
- curator_authority: A reader-facing block on Curator ownership of explanatory Markdown, source specs, teaching packets, GitHub-facing Markdown, HTML derivatives, and documentation-impact receipts; source paths: `.agents/roles/research_ops/documentation-curator.v0.9.0.md`, `.codex/skills/html-visual-explainer/SKILL.md`, `research_control/design/github_facing_explainer_contract.md`.
- student_teacher_loop: A reader-facing block on Student questions, Teacher answers, two-round support, source-bundle limits, and why support subroles cannot write tracked documentation; source paths: `.agents/roles/research_ops/documentation-student.v0.1.0.md`, `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`, `.agents/roles/research_ops/documentation-curator.v0.9.0.md`.
- packet_schema: A reader-facing block on Teaching Q&A packet fields, required body sections, source gaps, claims intentionally not made, and validator expectations; source paths: `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`, `scripts/validate_teaching_qa.py`, `markdown/teaching-packets/project-overview.teaching-qa.md`, `markdown/teaching-packets/role-routing.teaching-qa.md`.
- derivative_sync: A reader-facing block on how curated teaching content is distilled into the Markdown source spec, GitHub-facing Markdown, and tracked HTML derivative while preserving source-spec authority; source paths: `.codex/skills/aether-teaching-explainer/SKILL.md`, `.codex/skills/html-visual-explainer/SKILL.md`, `research_control/design/github_facing_explainer_contract.md`.
- advisory_format_boundary: A reader-facing block on renderer and lint scripts as quality guidance: they check structure, depth, and source binding, but they do not decide which project functionality deserves coverage; source paths: `.agents/roles/research_ops/documentation-curator.v0.9.0.md`, `.codex/skills/html-visual-explainer/SKILL.md`, `scripts/validate_teaching_qa.py`.
