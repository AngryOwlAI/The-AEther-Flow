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

## Generated Task Index

Generated task-index surfaces are available for navigation and retrieval:

- `TASK_INDEX.csv`
- `TASK_INDEX.md`
- `../../wiki/indexes/research_control_task_index.md`

These files are generated from tracked task records and the task-index schema.
They help humans and agents locate task folders, completion receipts, and next
actions. They are not canonical task authority.

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

Generated task-index files are lower-authority navigation and memory-retrieval
support. Canonical research-control authority remains in the task folders,
Director Decision Records, AgentJobs, completion records, handoffs,
`program_state.yaml`, and registries. Generated indexes must not be read as
physics proof, benchmark promotion, Gate Chair authority, ontology adoption, or
completed-derivation evidence.
