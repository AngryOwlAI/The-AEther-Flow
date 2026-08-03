<!-- authority: control -->

# Project-Improvement Handoff: improve-project-handoff_20260803_003

## Source

- Source task: `RT-20260803-003`
- Source decision: `DDR-20260803-003`
- Source job: `AJ-RT-20260803-003-001`
- Source completion: `research_control/tasks/RT-20260803-003/jobs/completions/AJC-AJ-RT-20260803-003-001.yaml`
- Regular research handoff: `handoff-0945`

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
| Signal IDs | `PIS-RT-20260803-003-001` |
| Signal count | 1 |
| Highest severity | high |
| Selected signal | `PIS-RT-20260803-003-001` |
| Routing basis | `highest_severity_then_created_at_then_signal_id` |

## Issues

### IPH-ISSUE-001: Control Contract Drift: PIS-RT-20260803-003-001

Signal: `PIS-RT-20260803-003-001`

Type: `control_contract_drift`

Severity: high

Description: Synchronize exact Gate C source-side adoption versus derivational coupling status plus Gate E negative-verdict and Gate A source-validation labels across aliases renderers validators and generated views without changing canonical science.

Evidence:

- `research_control/tasks/RT-20260803-003/artifacts/v21_p16_t02_overread_findings.yaml`: Synchronize exact Gate C source-side adoption versus derivational coupling status plus Gate E negative-verdict and Gate A source-validation labels across aliases renderers validators and generated views without changing canonical science.

Impact: Project-system follow-up is required under the improvement workflow.

Recommended next step: Run /improve-project-system to process this signal as one bounded project-system AgentJob.

## Solution Plan

Status: implementation payload and renderer-authority recovery complete;
governed checkpoint pending.

The Project-System Director selected
`project-control-maintainer@0.2.0` and activated
`AJ-RT-20260803-005-001`. Generation 233 executed that exact bounded AgentJob
once.

The bounded implementation must:

1. preserve the exact protected Gate A, Gate C, Gate E, and P16-T02 source
   hashes;
2. represent the exact finite source-side Gate C postulate adoption and the
   still-open `g_eff`-dependent matter-coupling derivation as different typed
   states across the ledger, aliases, calibrations, validators, renderers, and
   focused tests;
3. represent P9-T09 as an existing protected negative Gate E verdict while
   keeping any future positive closure evidence-dependent and human-gated;
4. synchronize only the current Gate A TeX source validation label to `PASS`,
   preserving immutable historical failure evidence; and
5. regenerate managed derivatives through approved generators, close the
   signal only against a PASS completion, and invoke one governed checkpoint.

The implementation must stop if it would broaden Gate C adoption, weaken the
open derivational burden, change any canonical Gate decision or science source,
or hand-edit a generated derivative.

## Precheckpoint blocker

The bounded P16-T02 status payload and focused checks pass, but the affected
validation profile fails the sealed P10-T05 current-renderer authority binding
for `scripts/research_control/render_current_frontier.py`. The historical
validator and its test are outside `AJ-RT-20260803-005-001`'s immutable write
allowlist. Reverting the renderer would recreate the Gate C status
contradiction, so generation 233 stopped with zero checkpoint invocations.

Generation 234 completed the distinct `improve-project-system` recovery. It
preserves the implemented payload and sealed historical evidence, adds one
fail-closed chained current-renderer binding, and restores P10 migration
readiness. One fresh governed checkpoint remains before the separate P16-T02
canonical alignment re-audit.

## Resolution

- Resolved by job: `AJ-RT-20260803-006-001`.
- Resolution evidence: `research_control/tasks/RT-20260803-006/jobs/completions/AJC-AJ-RT-20260803-006-001.yaml`.
- Resolved at: `2026-08-03T10:00:44Z`.

## Notes

This Markdown mirror is operator-facing. The YAML sidecar remains the
machine-readable control artifact. The implemented payload and validator
recovery create no science, Gate, benchmark, publication, external-action,
push, or completed-derivation authority. The signal is resolved against the
PASS completion, and a fresh P16-T02 canonical alignment audit
remains separate until after the recovery checkpoint.
