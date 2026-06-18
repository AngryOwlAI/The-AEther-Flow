<!-- authority: explanatory -->

# Local Agent Configurations

This folder contains local Codex agent configuration files used by governed
project workflows.

## Current Purpose

The active use is the Documentation Curator teaching loop:

- `documentation-student.toml` represents the bounded Student subrole that
  asks lay-reader questions.
- `documentation-teacher.toml` represents the bounded Teacher subrole that
  answers from the selected source bundle.

These helper agents support the Curator. They do not write tracked
documentation directly and do not create project authority by themselves.

## What Belongs Here

- Local agent configuration files that support repo-governed workflows.
- Configuration that can be traced to registered role contracts and task
  allowlists.

## What Does Not Belong Here

- Role contracts. Those belong under `.agents/roles/`.
- Skill contracts. Those belong under `.codex/skills/`.
- Task outputs, teaching packets, or final documentation.

## Authority Boundary

Agent config files are operational support. Role authority comes from the
registered role contracts and task-local execution-role records, not from these
local configuration files alone.

