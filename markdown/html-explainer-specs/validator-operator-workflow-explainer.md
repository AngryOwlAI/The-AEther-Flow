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
  - ".agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md"
  - "scripts/README.md"
  - "scripts/project_control/README.md"
  - "scripts/research_control/README.md"
  - "tests/README.md"
  - "scripts/validate_publication_process.py"
  - "scripts/project_control/validate_documentation_impact.py"
  - "scripts/project_control/generate_project_improvement_handoff.py"
  - "scripts/project_control/project_improvement_handoff_validation.py"
  - "scripts/research_control/checkpoint_research_transaction.py"
  - "scripts/research_control/validate_research_control.py"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md"
claim_boundary: "Human-only publication explainer for Validator And Operator Workflow. It explains existing command selection by change type, bootstrap versus validate-only, publication checks, documentation-impact checks, research-control checks, conditional source-bridge sidecar checkpoint evidence, unit-test triggers, screenshot evidence, troubleshooting, final review evidence, and PASS-result limits without changing validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, role authority, schemas, checkpoint gates, sidecar adoption status, generated-output authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Validator And Operator Workflow Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/validator-operator-workflow.publication-brief.md` as the page-specific editorial contract. The page is a
contributor operator guide under the post-migration Phase 4 quality
packet and the Phase 6 bridge checkpoint governance documentation update. It
improves reader orientation, footer-authority placement, and page-specific
operational structure without changing executable project behavior, validator
behavior, checkpoint behavior, sidecar status, or physics claim status.

## Source Basis

- `README.md`: Project front door, local environment, and public requirements.
- `AGENTS.md`: Authority hierarchy, generated-output boundaries, and required checks.
- `.codex/skills/project-memory-system/SKILL.md`: Bootstrap, validate-only, docs modes, and cleanup commands.
- `.codex/skills/improve-project-system/SKILL.md`: Project-system memory preflight, classifier, resolver, signal, documentation-impact, and checkpoint chain.
- `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`: Field contract for project-improvement handoff sidecars, including source-bridge metadata.
- `scripts/README.md`: Script groups and tooling authority boundary.
- `scripts/project_control/README.md`: Project-control script guidance for sidecar generation and validation.
- `scripts/research_control/README.md`: Research-control checkpoint and validation command guidance.
- `tests/README.md`: Unit-test coverage areas and command shape.
- `scripts/validate_publication_process.py`: Publication brief/spec/output consistency and no-network checks.
- `scripts/project_control/validate_documentation_impact.py`: Documentation-impact receipt validation.
- `scripts/project_control/generate_project_improvement_handoff.py`: Generator for project-improvement sidecars when completion signals require one.
- `scripts/project_control/project_improvement_handoff_validation.py`: Sidecar schema, source-bridge, and parity validation support.
- `scripts/research_control/checkpoint_research_transaction.py`: Checkpoint guard with conditional sidecar path acceptance tied to source-bridge evidence.
- `scripts/research_control/validate_research_control.py`: Tracked research-control and diff boundary checks.
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`:
  simplified public exists / does-not-exist table used by public-surface
  checks to distinguish scoped project status from downstream physics
  promotion.
- `research_control/design/epistemic_category_glossary.md`: category glossary
  used to distinguish validator receipts from scientific proof and publication
  surfaces from authority sources.
- `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`: Phase 6 checkpoint governance evidence for conditional source-bridge sidecar allowlisting.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Validator And Operator Workflow function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Command Decision Matrix`, `Conditional Sidecar Allowlist`, `When Extra Evidence Is Required`, `Troubleshooting Operator Failures`, `PASS Result Limits`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: operator command-selection guide only. This page cannot change
validator behavior, command semantics, routing behavior, documentation-impact
requirements, research-control requirements, schemas, checkpoint gates, or
physics status. It also cannot turn conditional sidecar path acceptance into a
global sidecar directory allowance or sidecar adoption claim.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Uses the bottom Reader Scope hook immediately above the marked authority footer in GitHub Markdown and tracked HTML.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Explains that public status checks must preserve the P14-T01 table and
  P14-T02 glossary boundaries and that a validator PASS does not authorize
  source-law adoption, `g_eff` scope expansion, matter-coupling adoption,
  Einstein equations, benchmark promotion, or completed derivation.
- Explains conditional bridge-sidecar acceptance as exact YAML/Markdown sidecar pairs named by source-bridge metadata, not a global sidecar directory allowance.
- Explains that positive and negative controls belong to validator evidence, while this page only documents the existing behavior.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
