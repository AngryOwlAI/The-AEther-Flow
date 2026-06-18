<!-- authority: explanatory -->

# Research Handoffs

This folder contains tracked handoff records for research-control continuation.

## File Pattern

Each handoff normally has two files:

- `handoff-NNNN.yaml` for machine-readable continuation state.
- `handoff-NNNN.md` for human-readable summary and next-step context.

Handoff numbers are monotonic and must not have gaps.

## What Belongs Here

- Final handoff records created at the end of bounded research-control work.
- Continuation summaries, next recommended actions, loop-risk routes, and
  project-improvement signal references.

## What Does Not Belong Here

- Draft handoff notes.
- Task-local artifacts.
- Generated wiki notes.
- Source authority that belongs in TeX, registries, or Markdown specs.

## Authority Boundary

Handoffs preserve continuation context, but they do not override registered
source files, registries, AgentJobs, completions, or human gates. Use
`research_control/program_state.yaml` and the latest handoff together when
resolving continuation.

