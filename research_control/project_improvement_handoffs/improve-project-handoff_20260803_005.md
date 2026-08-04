<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_20260803_005

## Source

- Source task: `RT-20260803-014`
- Source decision: `DDR-20260803-014`
- Source job: `AJ-RT-20260803-014-001`
- Source completion: `research_control/tasks/RT-20260803-014/jobs/completions/AJC-AJ-RT-20260803-014-001.yaml`
- Regular research handoff: `handoff-0955`

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
| Signal IDs | `PIS-RT-20260803-014-001` |
| Signal count | 1 |
| Highest severity | high |
| Selected signal | `PIS-RT-20260803-014-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Control Contract Drift: PIS-RT-20260803-014-001

Signal: `PIS-RT-20260803-014-001`

Type: `control_contract_drift`

Severity: high

Description: Align the current internal skeptical-review contract and current display projections with the review-independence taxonomy while preserving historical IDs and artifacts; add fail-closed regression coverage before a fresh P16-T04 re-audit.

Evidence:

- `research_control/tasks/RT-20260803-014/artifacts/v21_p16_t04_severity_repair_matrix.yaml`: Align the current internal skeptical-review contract and current display projections with the review-independence taxonomy while preserving historical IDs and artifacts; add fail-closed regression coverage before a fresh P16-T04 re-audit.

Impact: Project-system follow-up is required under the improvement workflow.

Recommended next step: Run /improve-project-system to process this signal as one bounded project-system AgentJob.

## Solution Plan

Status: completed through `AJ-RT-20260803-015-001`; one governed checkpoint
remains before the separate fresh P16-T04 re-audit.

The Project-System Director selected one task-scoped
`project-control-maintainer@0.2.0` job. It must preserve all historical role
IDs, task IDs, review artifacts, completions, and hashes while making the
current same-context AI skeptical-review contract and current role/task
display projection unambiguously internal. External human review and
independent replication language remains reserved for evidence satisfying the
registered taxonomy.

The implementation must add fail-closed role-name, task-display,
schema-language, red-team-artifact, and claim-linter regressions; regenerate
only approved derivatives; resolve the signal only on PASS; checkpoint once;
and route a fresh P16-T04 re-audit. It may not execute that re-audit or P16-T05
inside the repair job.

## Resolution

- Resolved by job: `AJ-RT-20260803-015-001`.
- Resolution evidence: `research_control/tasks/RT-20260803-015/jobs/completions/AJC-AJ-RT-20260803-015-001.yaml`.
- Resolved at: `2026-08-03T22:21:45Z`.

## Notes

Generation 246 executed the selected implementation once. The current display
name and role kind identify internal skeptical review, every recorded P16-T04
historical hash remains exact, and all 73 focused fail-closed regressions pass.
This Markdown mirror is operator-facing; the YAML sidecar remains the
machine-readable control artifact. The repair creates no external human review,
independence, replication, science, Gate, benchmark, proof, publication, push,
or completed-derivation authority.
