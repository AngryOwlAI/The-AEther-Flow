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
  - ".agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "scripts/project_control/generate_project_improvement_handoff.py"
  - "scripts/project_control/project_improvement_handoff_validation.py"
  - "scripts/project_control/README.md"
  - "scripts/research_control/checkpoint_research_transaction.py"
  - "scripts/research_control/validate_research_control.py"
  - "scripts/research_control/README.md"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
  - "research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md"
claim_boundary: "Human-only publication explainer for Project-System Improvement Loop. It explains classifier output, registered signal routing, advisory resolver output, project-improvement sidecar routing, one bounded AgentJob execution, documentation-impact receipts, exact source-bridge sidecar checkpoint boundaries, and signal-resolution evidence without creating sidecars, replacing normal research handoffs, changing validators, routing behavior, role authority, signal rows, signal types, checkpoint behavior, generated-output authority, or physics claim status."
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
packet and the Phase 6 bridge checkpoint governance documentation update. It
improves reader orientation, footer-authority placement, and page-specific
operational structure without changing executable project behavior, sidecar
state, checkpoint behavior, or physics claim status.

## Source Basis

- `AGENTS.md`: Root authority hierarchy and the split between physics continuation and project-system work.
- `research_control/README.md`: Research-control memory preflight, project-system signal, documentation-impact, and resolver rules.
- `.codex/skills/improve-project-system/SKILL.md`: Execution workflow for project-system improvement packets.
- `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`: Field contract for project-improvement handoff sidecars, including source-bridge metadata.
- `scripts/project_control/classify_project_changes.py`: Deterministic current-diff classification.
- `scripts/project_control/resolve_project_improvement.py`: Advisory routing across current diffs and open signals.
- `scripts/project_control/generate_project_improvement_handoff.py`: Generator for project-improvement handoff sidecars when completion signals require one.
- `scripts/project_control/project_improvement_handoff_validation.py`: Sidecar schema, source-bridge, and parity validation support.
- `scripts/project_control/README.md`: Operator-facing description of project-control bridge scripts.
- `scripts/research_control/checkpoint_research_transaction.py`: Checkpoint guard with conditional sidecar path acceptance tied to source-bridge evidence.
- `scripts/research_control/validate_research_control.py`: Research-control and `--check-diff` validator with the same exact sidecar boundary.
- `scripts/research_control/README.md`: Operator-facing checkpoint and research-control validation guidance.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`: Controlled signal vocabulary and default routing metadata.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`: Concrete signal instances, severity, status, evidence, and resolution fields.
- `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`: Phase 6 checkpoint governance evidence for conditional source-bridge sidecar allowlisting.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Project-System Improvement Loop function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Improvement Loop Map`, `Bridge Sidecar Flow`, `Diff, Signal, Resolver`, `Evidence To Close A Signal`, `Failure Boundaries`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: project-system workflow orientation only. This page cannot
create or close signals, create sidecars, replace normal research handoffs,
change routing behavior, change validator behavior, expand role authority,
change checkpoint behavior, or authorize physics claim promotion.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Uses the bottom Reader Scope hook immediately above the marked authority footer in GitHub Markdown and tracked HTML.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Explains bridge sidecars as separate project-system handoff packets that do not replace normal research handoffs.
- Explains conditional checkpoint and `--check-diff` acceptance as exact source-bridge sidecar path handling, not a global sidecar directory allowance.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
