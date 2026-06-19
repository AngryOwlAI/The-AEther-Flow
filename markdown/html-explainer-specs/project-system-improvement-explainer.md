---
title: "Project-System Improvement Loop"
purpose: "Explain how documentation drift, control drift, validator gaps, memory issues, and routing ambiguity become bounded project-system work."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/project-system-improvement-explainer.html"
github_markdown_output_path: "github-facing/project-system-improvement-explainer.md"
wiki_output_path: "wiki/html/html-project-system-improvement-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/project-system-improvement.publication-brief.md"
document_type: "workflow_guide"
visual_strategy: "process_timeline"
migration_status: "reviewed"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for Project-System Improvement Loop. It explains classifier output, registered signal routing, advisory resolver output, one bounded AgentJob execution, documentation-impact receipts, and signal-resolution evidence without changing validators, routing behavior, role authority, signal rows, signal types, checkpoint behavior, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Project-System Improvement Loop Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/project-system-improvement.publication-brief.md` as the page-specific editorial contract. The page is a
workflow guide under the post-migration Phase 4 quality
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `AGENTS.md`: Root authority hierarchy and the split between physics continuation and project-system work.
- `research_control/README.md`: Research-control memory preflight, project-system signal, documentation-impact, and resolver rules.
- `.codex/skills/improve-project-system/SKILL.md`: Execution workflow for project-system improvement packets.
- `scripts/project_control/classify_project_changes.py`: Deterministic current-diff classification.
- `scripts/project_control/resolve_project_improvement.py`: Advisory routing across current diffs and open signals.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`: Controlled signal vocabulary and default routing metadata.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`: Concrete signal instances, severity, status, evidence, and resolution fields.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Project-System Improvement Loop function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Improvement Loop Map`, `Diff, Signal, Resolver`, `Evidence To Close A Signal`, `Failure Boundaries`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: project-system workflow orientation only. This page cannot
create or close signals, change routing behavior, change validator behavior,
expand role authority, or authorize physics claim promotion.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Uses the bottom Reader Scope hook immediately above the marked authority footer in GitHub Markdown and tracked HTML.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
