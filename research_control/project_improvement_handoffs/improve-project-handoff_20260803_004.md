<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_20260803_004

## Source

- Source task: `RT-20260803-010`
- Source decision: `DDR-20260803-010`
- Source job: `AJ-RT-20260803-010-001`
- Source completion: `research_control/tasks/RT-20260803-010/jobs/completions/AJC-AJ-RT-20260803-010-001.yaml`
- Regular research handoff: `handoff-0951`

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
| Signal IDs | `PIS-RT-20260803-010-001` |
| Signal count | 1 |
| Highest severity | high |
| Selected signal | `PIS-RT-20260803-010-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Control Contract Drift: PIS-RT-20260803-010-001

Signal: `PIS-RT-20260803-010-001`

Type: `control_contract_drift`

Severity: high

Description: Preserve sealed RT-20260803-005 evidence and synchronize the exact Gate A decision row with a fresh fail-closed exact-object validator plus regression coverage.

Evidence:

- `research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_reaudit_findings.yaml`: Preserve sealed RT-20260803-005 evidence and synchronize the exact Gate A decision row with a fresh fail-closed exact-object validator plus regression coverage.

Impact: Project-system follow-up is required under the improvement workflow.

Recommended next step: Run /improve-project-system to process this signal as one bounded project-system AgentJob.

## Solution Plan

Status: completed pending governed checkpoint.

Project-System Director converted the issue into one bounded
`AJ-RT-20260803-011-001` Project-Control Maintainer job. The job verified the
exact Gate A object ID, path, and immutable source hash; synchronized only its
operational registry-validation status; added a fresh exact-object validator;
and added six fail-closed regressions that reject cross-object substitution.

## Resolution

- Resolved by job: `AJ-RT-20260803-011-001`.
- Resolution evidence: `research_control/tasks/RT-20260803-011/jobs/completions/AJC-AJ-RT-20260803-011-001.yaml`.
- Resolved at: `2026-08-03T16:47:10Z`.

One governed checkpoint remains. After it, the research lane must run a fresh
P16-T02 canonical Gate A-E consistency re-audit before P16-T03 or P16-T04.

## Notes

This Markdown mirror is operator-facing. The YAML sidecar remains the
machine-readable control artifact.
