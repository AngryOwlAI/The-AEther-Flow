<!-- authority: explanatory -->

# Research-Control Tasks

This folder contains task-local records for bounded research and project-system
transactions.

## Typical Task Anatomy

A task folder may include:

- `00_TASK.yaml` for task identity and closure state.
- `DDR-*.md` for the Director Decision Record.
- `jobs/AJ-*.yaml` for the AgentJob contract.
- `jobs/completions/AJC-*.yaml` for completion receipts.
- `roles/*.yaml` for execution-role records.
- `documentation_impact.yaml` when documentation impact is required.
- `artifacts/` for task-local outputs.

## What Belongs Here

- Immutable or superseded task records.
- Bounded role outputs and receipts.
- Task-local audit artifacts.

## What Does Not Belong Here

- Per-task README files unless a future policy explicitly requires them.
- Generated wiki notes.
- Canonical ontology TeX outside a task-local draft/control artifact.
- Untracked scratch work.

## Authority Boundary

Task records are control evidence for a bounded transaction. They do not by
themselves promote scientific claims unless the proper source, registry,
refutation, and gate sequence also supports that promotion.

