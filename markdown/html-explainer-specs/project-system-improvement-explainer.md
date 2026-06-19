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
claim_boundary: "Human-only publication explainer for the AEther-Flow project-system improvement loop. It explains classifier output, registered signal routing, advisory resolver output, one bounded AgentJob execution, documentation-impact receipts, and signal-resolution evidence without changing validators, routing behavior, role authority, signal rows, signal types, checkpoint behavior, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Project-System Improvement Loop Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/project-system-improvement.publication-brief.md`
as the page-specific editorial contract. The page is a workflow guide. It
explains the existing project-system improvement loop; it does not register
signals, close signals, change validators, change routing, expand role
authority, or promote physics claims.

## Source Basis

- `AGENTS.md` separates project-system improvement from physics continuation,
  requires memory use before project-knowledge changes, and states generated
  artifact boundaries.
- `research_control/README.md` defines the research-control authority model,
  memory preflight, documentation-impact receipt gate, signal registry rules,
  resolver advisory status, and one-bounded-Job discipline.
- `.codex/skills/improve-project-system/SKILL.md` defines the execution
  workflow for project-system work, including memory preflight, classifier and
  resolver checks, signal validation, one bounded AgentJob, documentation
  impact, and checkpoint behavior.
- `scripts/project_control/classify_project_changes.py` supplies the
  deterministic current-diff classification behavior for documentation impact
  and project-system improvement requirements.
- `scripts/project_control/resolve_project_improvement.py` supplies advisory
  routing behavior that compares open signals with current Git-change
  classification.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` supplies the
  controlled signal vocabulary and default recommended routing metadata.
- `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` supplies concrete
  signal instances, status, severity, evidence, and resolution fields.

## Required Reader Outcome

After reading, a maintainer or future agent should know that project-system
work starts from observed state: current Git diff classification, registered
open signals, and memory-backed source inspection. The reader should know that
the resolver is advisory, that one invocation may execute at most one bounded
AgentJob, that every state-changing project-system AgentJob needs a
documentation-impact receipt, and that a signal cannot leave the open backlog
without explicit evidence.

## Visual Strategy

Use a process timeline from observed issue to bounded AgentJob and evidence.
Add a classifier/resolver/checkpoint-gate comparison table and an evidence
checklist. Do not make the timeline look like a validator change or a signal
closure action.

## Acceptance Criteria

- Explains classification before routing.
- Distinguishes current Git diff work from registered open signals.
- States that resolver output is advisory and checkpoint blocking comes from
  validators or concrete authority violations.
- Explains signal type registry versus signal instance registry.
- Explains one bounded AgentJob per invocation.
- Explains documentation-impact receipts for state-changing project-system
  AgentJobs.
- Explains evidence required to move a signal out of open backlog.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
