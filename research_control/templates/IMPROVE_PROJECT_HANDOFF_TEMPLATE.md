<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_YYYYMMDD_NNN

## Source

- Source task: `RT-YYYYMMDD-NNN`
- Source decision: `DDR-YYYYMMDD-NNN`
- Source job: `AJ-RT-YYYYMMDD-NNN-NNN`
- Source completion: `research_control/tasks/RT-YYYYMMDD-NNN/jobs/completions/AJC-AJ-RT-YYYYMMDD-NNN-NNN.yaml`
- Regular research handoff: `handoff-0000`

## Boundary

This sidecar is a project-system improvement handoff. It does not replace the
normal research handoff, does not become the latest `/continue-research`
handoff, and does not authorize project-system repair from the research lane.

Authorized consumer: `/improve-project-system`.

Unauthorized effects:

- physics claim promotion;
- canonical science source edits;
- generated derivative hand edits;
- replacement of `research_control/handoffs/handoff-####.yaml`;
- generator, resolver, checkpoint, skill, role, or schema changes unless a
  separate bounded AgentJob authorizes them.

## Signal Summary

| Field | Value |
| --- | --- |
| Signal IDs | `PIS-RT-YYYYMMDD-NNN-001` |
| Signal count | 1 |
| Highest severity | medium |
| Selected signal | `PIS-RT-YYYYMMDD-NNN-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Short Machine-Readable Issue Title

Signal: `PIS-RT-YYYYMMDD-NNN-001`

Type: `validator_gap`

Severity: medium

Evidence:

- `research_control/tasks/RT-YYYYMMDD-NNN/jobs/completions/AJC-AJ-RT-YYYYMMDD-NNN-NNN.yaml`:
  concrete observed behavior.

Impact: How this affects operators or future agents.

Recommended next step: one bounded `/improve-project-system` repair step.

## Solution Plan

Status: absent.

If no executable plan is present, Project-System Director should convert this
issue inventory into one bounded AgentJob or reject the signal with explicit
evidence.

## Resolution

- Resolved by job: none.
- Resolution evidence: none.
- Resolved at: none.

## Notes

This Markdown mirror is operator-facing. The YAML sidecar remains the
machine-readable control artifact.
