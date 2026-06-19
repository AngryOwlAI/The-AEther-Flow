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
claim_boundary: "Human-only publication explainer for Validator And Operator Workflow. It explains existing command selection by change type, bootstrap versus validate-only, publication checks, documentation-impact checks, research-control checks, unit-test triggers, screenshot evidence, troubleshooting, final review evidence, and PASS-result limits without changing validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, role authority, schemas, checkpoint gates, generated-output authority, or physics claim status."
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
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `README.md`: Project front door, local environment, and public requirements.
- `AGENTS.md`: Authority hierarchy, generated-output boundaries, and required checks.
- `.codex/skills/project-memory-system/SKILL.md`: Bootstrap, validate-only, docs modes, and cleanup commands.
- `.codex/skills/improve-project-system/SKILL.md`: Project-system memory preflight, classifier, resolver, signal, documentation-impact, and checkpoint chain.
- `scripts/README.md`: Script groups and tooling authority boundary.
- `tests/README.md`: Unit-test coverage areas and command shape.
- `scripts/validate_publication_process.py`: Publication brief/spec/output consistency and no-network checks.
- `scripts/project_control/validate_documentation_impact.py`: Documentation-impact receipt validation.
- `scripts/research_control/validate_research_control.py`: Tracked research-control and diff boundary checks.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Validator And Operator Workflow function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Command Decision Matrix`, `When Extra Evidence Is Required`, `Troubleshooting Operator Failures`, `PASS Result Limits`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
