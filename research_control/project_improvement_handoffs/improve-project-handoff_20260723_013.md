<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_20260723_013

## Source

- Source task: `RT-20260723-013`
- Source decision: `DDR-20260723-013`
- Source job: `AJ-RT-20260723-013-001`
- Source completion: `research_control/tasks/RT-20260723-013/jobs/completions/AJC-AJ-RT-20260723-013-001.yaml`
- Regular research handoff: `handoff-0846`

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
| Signal IDs | `PIS-RT-20260723-013-001` |
| Signal count | 1 |
| Highest severity | high |
| Selected signal | `PIS-RT-20260723-013-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Generated Artifact Drift: PIS-RT-20260723-013-001

Signal: `PIS-RT-20260723-013-001`

Type: `generated_artifact_drift`

Severity: high

Description: The current P12-T05 validator returns FAIL because scientific_quality_validation_report.json and scientific_quality_compact_receipt.json embed stale hashes for the taxonomy, calibration policy, and fixture corpus. P12-T07 preserves the three exact live-versus-embedded deltas and does not repair the predecessor.

Evidence:

- `research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_ablation_results.json`: The current P12-T05 validator returns FAIL because scientific_quality_validation_report.json and scientific_quality_compact_receipt.json embed stale hashes for the taxonomy, calibration policy, and fixture corpus. P12-T07 preserves the three exact live-versus-embedded deltas and does not repair the predecessor.

Impact: Project-system follow-up is required under the improvement workflow.

Recommended next step: Run /improve-project-system to process this signal as one bounded project-system AgentJob.

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
