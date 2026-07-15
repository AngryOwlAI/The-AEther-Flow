---
authority: control
task_id: "RT-20260715-006"
job_id: "AJ-RT-20260715-006-001"
plan_task_id: "P2-T05"
status: "PASS"
scientific_claims_changed: false
physics_promotion_authorized: false
proof_authority: false
---

# V19 first-wave equivalence and measured-savings audit

## Verdict

PASS. The first direct-consolidation wave preserves failure-mode coverage,
removes the intended eligible duplicate invocations, retains final staged
acceptance and rollback references, and changes no physics authority. P3-T01
is dependency-ready only after this audit transaction checkpoints.

## Equivalence evidence

- The fresh 11-fixture adversarial comparison passed with zero semantic
  mismatches, zero missing hard findings, zero missing warnings, zero
  legacy-FAIL/candidate-PASS cases, and all 42 claim taxonomy classes covered.
- The configuration-error and hermetic core-plus-diff composition guards
  passed. All 14 evidence-identity difference fields still fail closed.
- The 196-test focused first-wave suite passed in 68.24 seconds. It covers the
  adversarial corpus, claim-language taxonomy, local-runner plan, checkpoint
  working/staged distinction, index restoration, staged residue, and static
  orchestration contracts.
- The full repository suite passed all 613 tests. The live
  `legacy_consolidated` aggregate passed all 12 required gates with zero claim
  findings and no required or advisory failure.

## Current clean measurement

The same clean commit and tree were used for both commands. The legacy pair
(`research_control_core` followed by `research_control_diff`) produced the
same normalized 19,286-byte JSON result from each command: PASS, 0 errors,
123 operational warnings, and 0 claim findings. The consolidated path executes
only `research_control_diff` for that exact identity.

| Metric | Legacy pair | Consolidated | Observed difference |
| --- | ---: | ---: | ---: |
| Gate processes | 2 | 1 | -1 |
| Wall duration | 26.36 s | 13.26 s | -13.10 s (-49.70%) |
| Output bytes | 38,572 | 19,286 | -19,286 (-50.00%) |

This is one matched clean measurement, not a variance estimate or a
full-profile speedup claim.

## Invocation-count result

The first wave removes one eligible duplicate from the Make plan, two from the
local runner, and three from checkpoint validation when the two post-sync
duplicates and the independent final staged claim duplicate are counted.
That sum of six is across three separate entry-point plans; it is not a claim
that all six occur in every single transaction. No unexplained duplicate
evidence identity remains in the audited plans.

The checkpoint still executes an integrated working diff and a distinct final
staged diff. Working evidence does not satisfy staged acceptance.

## Runtime interpretation

The repository-wide suite took 617.50 seconds for 613 tests and emitted 2,726
bytes. The frozen clean baseline took 515.454875 seconds for 584 tests and
emitted 2,697 bytes. The samples are not comparable because the current suite
contains 29 more tests, the instrumentation differs, and only one current run
exists. The runtime hard guard therefore remains inactive; no speedup or
regression percentage is claimed from these full-suite samples.

## Rollback and retained authority

- `planner_mode=off`, `cache_mode=off`, `output_mode=legacy`, and
  `legacy_fallback=enabled` remain the policy safe values.
- The frozen legacy invocation inventory, validator commands, checkpoint
  rollback block, and final staged integrated diff remain available.
- P2 did not edit CI. The existing workflow remains unfiltered for push, pull
  request, and manual execution; future P11-T03 owns adding the separately
  scheduled-full workflow.
- `handoff-0740` and `EqSrc_family_closure_repair_or_stress` remain the
  ordinary research authority.

Raw output is retained under ignored `.local/v19_p2_t05_receipts/`. Those logs
are diagnostic receipts, not tracked project authority or physics evidence.
