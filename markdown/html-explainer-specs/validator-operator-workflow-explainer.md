---
title: "Validator And Operator Workflow"
purpose: "Explain how maintainers and future agents choose the correct command chain for documentation, memory, project-control, and research-control work."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/validator-operator-workflow-explainer.html"
github_markdown_output_path: "github-facing/validator-operator-workflow-explainer.md"
wiki_output_path: "wiki/html/html-validator-operator-workflow-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/validator-operator-workflow.publication-brief.md"
document_type: "contributor_operator_guide"
visual_strategy: "annotated_table"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "scripts/README.md"
  - "tests/README.md"
  - "scripts/validate_publication_process.py"
  - "scripts/project_control/validate_documentation_impact.py"
  - "scripts/research_control/validate_research_control.py"
claim_boundary: "Human-only publication explainer for the AEther-Flow validator and operator workflow. It explains existing command selection by change type, bootstrap versus validate-only, publication checks, documentation-impact checks, research-control checks, unit-test triggers, screenshot evidence, troubleshooting, final review evidence, and PASS-result limits without changing validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, role authority, schemas, checkpoint gates, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Validator And Operator Workflow Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/validator-operator-workflow.publication-brief.md`
as the page-specific editorial contract. The page is a contributor/operator
guide. It explains existing checks and evidence expectations; it does not
change validators, commands, role contracts, schemas, routing behavior,
checkpoint gates, generated-output authority, or physics claim status.

## Source Basis

- `README.md` gives the public front-door context, separates physics claims
  from project-system tooling claims, and names the local Python environment.
- `AGENTS.md` defines repository authority, generated-output boundaries,
  required bootstrap checks, documentation-impact checks, and the rule against
  hand-editing generated artifacts.
- `.codex/skills/project-memory-system/SKILL.md` defines bootstrap,
  validate-only, docs-only, docs-validate-only, and strict-docs modes for the
  memory/wiki/registry derivative system.
- `.codex/skills/improve-project-system/SKILL.md` defines the project-system
  execution chain: memory preflight, classifier, resolver, signal validation,
  one bounded AgentJob, documentation impact, bootstrap, research-control
  checks, and checkpoint.
- `scripts/README.md` explains script groups and the authority boundary for
  tooling changes.
- `tests/README.md` explains unit-test coverage areas and full or targeted
  test commands.
- `scripts/validate_publication_process.py` checks publication brief/spec/page
  consistency, no-network HTML, source visibility, authority language,
  evidence paths, orphan public pages, duplicate section skeletons, and retired
  process patterns.
- `scripts/project_control/validate_documentation_impact.py` checks that
  documentation-impact receipts cover live source changes, generated
  derivatives, classifier reason codes, and required validators.
- `scripts/research_control/validate_research_control.py` checks the tracked
  research-control spine, registry shapes, role/job/task/claim-boundary
  records, memory preflight receipts, protected authority markers, and optional
  diff write-path boundaries.

## Required Reader Outcome

After reading, an operator should know how to choose checks by change type:
memory/source registry changes need bootstrap, publication pages need the
publication-process check plus screenshots, state-changing project-system
AgentJobs need documentation-impact and research-control checks, script or
test changes need unit tests, and final review needs evidence paths rather
than a free-text claim of success.

## Visual Strategy

Use an annotated command matrix as the primary visual. Add a compact decision
path for when to add documentation-impact, research-control, unit-test, and
screenshot checks. Add a troubleshooting panel for known failures such as
stale `.local` retrieval warnings, missing screenshot evidence, orphan public
surfaces, and write-path boundary errors.

## Acceptance Criteria

- Explains validation by change type.
- Explains bootstrap versus validate-only.
- Explains publication-process checks.
- Explains documentation-impact checks.
- Explains research-control validation and `--check-diff`.
- Explains unit-test trigger conditions.
- Explains screenshot evidence for tracked HTML pages.
- Explains what validator PASS does and does not mean.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
