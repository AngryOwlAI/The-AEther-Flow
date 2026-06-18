<!-- authority: explanatory -->

# Scripts

This folder contains repository scripts used for project-control, research
control, documentation validation, teaching QA, and explainer linting.

## Script Groups

- `project_control/` contains classifier, resolver, documentation-impact,
  documentation-surface audit, and project-improvement signal tooling.
- `research_control/` contains continuation, handoff resolution, strict YAML,
  validation, and checkpoint tooling.
- Root-level scripts support HTML explainer enhancement, spec-depth linting,
  and teaching-QA validation.

## What Belongs Here

- Source scripts that operate tracked project workflows.
- Small command-line tools used by validators or task receipts.

## What Does Not Belong Here

- Generated outputs.
- Local caches.
- Task-specific artifacts.
- Long-form documentation that belongs in Markdown sources.

## Authority Boundary

Scripts enforce or automate project behavior only when invoked by the tracked
workflow. If a script changes validation, routing, or checkpoint behavior, the
change must be handled as a project-system transaction with tests and
documentation impact.

