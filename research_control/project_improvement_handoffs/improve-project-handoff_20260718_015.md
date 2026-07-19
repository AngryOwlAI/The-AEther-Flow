<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_20260718_015

## Source

- Source task: `RT-20260718-015`
- Source decision: `DDR-20260718-015`
- Source job: `AJ-RT-20260718-015-001`
- Source completion: `research_control/tasks/RT-20260718-015/jobs/completions/AJC-AJ-RT-20260718-015-001.yaml`
- Regular research handoff: `handoff-0741`

## Boundary

This sidecar is a project-system improvement handoff. It does not replace the
normal research handoff, does not become the latest `/continue-research`
handoff, and does not authorize project-system repair from the research lane.

Authorized consumer: `/improve-project-system`.

Unauthorized effects:

- physics claim promotion;
- canonical science source edits;
- generated derivative hand edits;
- replacement of `research_control/handoffs/handoff-####.yaml`.

## Signal Summary

| Field | Value |
| --- | --- |
| Signal IDs | `PIS-RT-20260718-015-001` |
| Signal count | 1 |
| Highest severity | high |
| Selected signal | `PIS-RT-20260718-015-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Validator Gap: PIS-RT-20260718-015-001

Signal: `PIS-RT-20260718-015-001`

Type: `validator_gap`

Severity: high

Description: The governed checkpoint planner rejected mandatory output/compact_current_frontier_v16.yaml and output/compact_current_frontier_v16.json as unknown_governed_path and therefore could not produce a safe shadow plan. No files were staged or committed.

Evidence:

- `research_control/tasks/RT-20260718-015/jobs/completions/AJC-AJ-RT-20260718-015-001.yaml`: The governed checkpoint planner rejected mandatory output/compact_current_frontier_v16.yaml and output/compact_current_frontier_v16.json as unknown_governed_path and therefore could not produce a safe shadow plan. No files were staged or committed.

Impact: Project-system follow-up is required under the improvement workflow.

Recommended next step: Run /improve-project-system to process this signal as one bounded project-system AgentJob.

## Solution Plan

Status: absent.

If no executable plan is present, Project-System Director should convert this
issue inventory into one bounded AgentJob or reject the signal with explicit
evidence.

## Resolution

- Resolved by job: `AJ-RT-20260718-016-001`.
- Resolution evidence: `research_control/tasks/RT-20260718-016/jobs/completions/AJC-AJ-RT-20260718-016-001.yaml`.
- Resolved at: `2026-07-19T05:08:30Z`.

## Notes

The exact compact-current-frontier YAML and JSON paths are now classified as
generated derivatives while unknown unrecognized paths remain fail-closed.
Handoff-0741 and the RT-015 scientific payload are unchanged. This Markdown
mirror is operator-facing; the YAML sidecar remains the machine-readable
control artifact.
