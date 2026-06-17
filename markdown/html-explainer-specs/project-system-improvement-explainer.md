---
title: "Project-System Improvement"
purpose: "Explain the bounded project-system improvement loop for documentation drift, validators, roles, schemas, memory tooling, signal routing, and operational reliability."
audience: "Maintainers and agents who need to repair the project machinery without confusing project-system changes with physics continuation."
output_path: "html/project-system-improvement-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "scripts/project_control/collect_project_improvement_signals.py"
  - "scripts/project_control/validate_documentation_impact.py"
claim_boundary: "Human-only project-system improvement explainer. It may summarize the classifier, resolver, signal registries, bounded AgentJob routing, documentation-impact record, and validation gates, but it does not change routing behavior, validator behavior, role authority, signal state, or scientific claim status."
human_visual_only: true
explainer_kind: "workflow_process"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "workflow_lifecycle"
layout_intent: "Use a workflow lifecycle view that separates classification, advisory resolution, bounded execution, documentation impact, regeneration, validation, and checkpoint readiness."
required_controls:
  - "section_toc"
  - "workflow_step_inspector"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "classifier_resolver"
  - "signal_registry"
  - "bounded_job_path"
  - "documentation_impact"
  - "checkpoint_boundary"
---

# Project-System Improvement Spec

## Rendering Intent

Create a source-backed explainer for the project-system repair workflow. The
subject is the improvement loop that handles documentation drift, validators,
roles, schemas, control-marked Markdown, memory tooling, generated-document
pipelines, and operational reliability. The explainer should show that this is
separate from physics continuation: it can repair project machinery and
documentation, but it cannot promote scientific claims.

The renderer's workflow layout is useful guidance, not a substitute for
curator judgment. The page should preserve the real conceptual order:

- inspect authority and registries;
- classify current changes;
- read advisory resolver state;
- validate project-improvement signals;
- route one bounded AgentJob;
- write documentation impact when required;
- regenerate memory/wiki/registry derivatives; and
- validate the transaction before checkpointing.

## Workflow Step Inspector Basis

Render the workflow inspector as the bounded project-system improvement loop:

1. Inspect root guidance, research-control guidance, relevant registries, and
   active source surfaces.
2. Classify changed paths and reason codes.
3. Resolve advisory routing state and open project-improvement signals.
4. Route at most one bounded AgentJob to the fitting project-system role.
5. Execute only within the job allowlist and source authority boundary.
6. Record documentation impact for state-changing project-system work.
7. Regenerate derived memory, registry, HTML, wiki, or GitHub-facing surfaces
   through the approved path.
8. Validate the transaction before treating it as checkpoint-ready.

## Source-Backed Summary

Summary heading: `Summary of Project-System Improvement`

Summary text:

Project-system improvement is the repair lane for the research machinery itself. It covers documentation drift, role and schema contracts, validator behavior, memory tooling, generated-document pipelines, trigger logic, signal routing, and operational reliability. The workflow begins with source inspection and a structural classifier, then uses an advisory resolver and signal registries to decide whether one bounded AgentJob is needed. A Documentation Curator job handles explanatory documentation drift; a Project-Control Maintainer or other project-system role handles contracts, validators, schemas, or control behavior. Every state-changing project-system AgentJob must record documentation impact, regenerate the source-first memory surfaces when needed, and pass research-control validation. The loop exists so the system can improve itself without turning maintenance work into physics continuation or claim promotion.

Summary source basis:

- `AGENTS.md`
- `research_control/README.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `scripts/project_control/classify_project_changes.py`

## Required Content Blocks

- subject_summary: A source-backed summary of Project-System Improvement that directly explains the repair lane, why it exists, how classifier and resolver state are used, and why it remains separate from physics continuation: `AGENTS.md`, `research_control/README.md`, `.codex/skills/improve-project-system/SKILL.md`, `scripts/project_control/classify_project_changes.py`.
- classifier_resolver: A reader-facing block on structural change classification, advisory resolver output, and the distinction between routing guidance and hard checkpoint gates; source paths: `.codex/skills/improve-project-system/SKILL.md`, `scripts/project_control/classify_project_changes.py`, `scripts/project_control/resolve_project_improvement.py`, `research_control/README.md`.
- signal_registry: A reader-facing block on project-improvement signal type rows, concrete signal instances, severity, terminal status evidence, and shared closure requirements; source paths: `.codex/skills/improve-project-system/SKILL.md`, `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`, `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`, `scripts/project_control/collect_project_improvement_signals.py`.
- bounded_job_path: A reader-facing block on the one-bounded-AgentJob discipline for documentation, contract, validation, memory, or director-review work, including role fit and path allowlists; source paths: `AGENTS.md`, `research_control/README.md`, `.codex/skills/improve-project-system/SKILL.md`.
- documentation_impact: A reader-facing block on documentation-impact receipts, changed path coverage, generated derivatives, classifier reason codes, no-op rationale, and required validators; source paths: `research_control/README.md`, `.codex/skills/improve-project-system/SKILL.md`, `scripts/project_control/validate_documentation_impact.py`.
- checkpoint_boundary: A reader-facing block on regeneration, validation, check-diff, and stop conditions that prevent project-system repair from becoming uncontrolled rewrite or scientific authority; source paths: `.codex/skills/improve-project-system/SKILL.md`, `research_control/README.md`, `AGENTS.md`.
