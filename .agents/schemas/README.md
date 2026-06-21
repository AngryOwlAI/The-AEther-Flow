<!-- authority: explanatory -->

# Agent Schemas

This folder contains reusable schema documentation for the project-control
objects used by the research-agent system.

## What Belongs Here

- Abstract schema descriptions for Director decisions, AgentJobs, execution
  roles, role contracts, documentation-impact records, and teaching Q&A
  packets.
- Prospective completion schemas that define reusable field meanings and
  allowed values for future governed research-control receipts.
- Schema notes that define required fields, field meanings, and authority
  constraints for repeated control objects.

## What Does Not Belong Here

- Concrete task files. Those belong under `research_control/tasks/`.
- Concrete templates for new task records. Those belong under
  `research_control/templates/`.
- Generated registry rows or generated wiki notes.

## Relationship To Templates

The schema files explain the shape and meaning of a record class. The template
files under `research_control/templates/` are practical starting points for
creating new records. A template may be copied into a task folder, but this
schema folder remains the explanatory source for object structure.

## Active Schema Contracts

- `PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md` defines the Phase 5 prospective
  hard-enforcement completion fields, obstruction/freeze receipt vocabulary,
  route-cycle controls, and Candidate Constructor no-fog result rules for
  future physics AgentJobs that opt into the mathematical-decisiveness
  contract.

## Authority Boundary

Schema files are project-control authority. They can affect validator
expectations, routing behavior, and checkpoint boundaries. Do not alter schema
meaning as part of ordinary documentation cleanup unless the owning task
explicitly authorizes schema-contract work.
