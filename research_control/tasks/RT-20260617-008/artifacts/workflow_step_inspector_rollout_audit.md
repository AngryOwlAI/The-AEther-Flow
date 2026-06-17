# Workflow Step Inspector Rollout Audit

## Objective

Implement a source-backed Workflow Step Inspector pattern for explainer subjects
that are workflow or control-system pages, and synchronize the matching
GitHub-facing Markdown and tracked HTML derivatives.

## Curator Decision

Applied `Workflow Step Inspector` to the eight source specs that declare
`workflow_step_inspector` in `required_controls`:

- `research-agent-workflow-explainer`
- `role-routing-explainer`
- `research-control-system-explainer`
- `claim-gates-explainer`
- `source-authority-explainer`
- `memory-system-explainer`
- `project-system-improvement-explainer`
- `documentation-curator-teaching-loop-explainer`

Each applied page now has a page-specific inspector sequence in the source
spec, a matching `## Workflow Step Inspector` section in `github-facing/`, and
an HTML `data-explainer-control="workflow_step_inspector"` section headed
`Workflow Step Inspector`.

## Explicit Non-Applications

The following pages were inspected and left without the workflow-step section:

- `project-overview-explainer`: atlas hub, not a single operational workflow.
- `aether-flow-ontology-explainer`: conceptual physics model; a workflow-step
  section could imply derivation progress or process authority.
- `roles-and-skills-explainer`: role catalog; the correct reader shape is a
  catalog/association model rather than a workflow.
- `gr-derivation-roadmap-explainer`: sequential roadmap, but intentionally a
  claim-boundary planning surface, not a current workflow gate.
- `technical-requirements-explainer`: requirements ladder; a workflow-step
  section would duplicate setup tiers without improving authority clarity.

## Contract Update

`research_control/design/github_facing_explainer_contract.md` now requires
`## Workflow Step Inspector` in a GitHub-facing page when its matching source
spec declares `workflow_step_inspector`. The audit script enforces this
conditional requirement.

## Validation Intent

The final transaction should pass source-spec depth lint, teaching-QA
validation, unit tests, bootstrap, documentation-surface audit,
documentation-impact validation, research-control validation, check-diff, and
`git diff --check`.

## Claim Boundary

This rollout changes documentation contracts and generated documentation
derivatives only. It does not change physics claims, routing behavior, role
authority, validator semantics outside the GitHub-facing workflow-step guard,
or generated-output authority.
