<!-- authority: control -->

# V19 P1-T05 rollback tabletop and comparison report

Status: `PASS`

## Decision summary

P1-T05 defines fail-closed shadow comparison and rollback control while legacy
validation remains authoritative. No planner path exists or becomes
authoritative in this packet. The tabletop exercises prove that planned
orchestration and cache failures have bounded restoration routes that do not
rewrite task history or scientific state.

## Tabletop 1: planned P2 direct-superset consolidation

| Field | Exercise result |
| --- | --- |
| Planned change | P2-T01 replaces the plain research-control core invocation immediately followed by its same-scope diff superset |
| Injected failure | Consolidated execution omits one normalized hard finding or selects a different changed-path set |
| Detected by | P1-T03 adversarial corpus plus matched selected-path hard-finding authority-field and exit-status comparison |
| Trigger | Missing hard finding or unexplained path mismatch |
| Immediate response | Keep or restore the legacy pair; reject consolidation; do not advance the epoch |
| Restored surfaces | Make or wrapper composition only; no task history or scientific source changes |
| Re-entry evidence | Focused repair fixture, complete adversarial corpus, and clean matched live parity |
| Result | `PASS_TABLETOP` |

The exercise restores acceptance coverage, including the diff-only invariant,
instead of merely restoring a command label.

## Tabletop 2: planned exact-tree cache failure

| Field | Exercise result |
| --- | --- |
| Planned change | P10 exact-tree cache reads a prior validation receipt |
| Injected failure | Receipt key matches gate name but differs in tree, implementation, environment, or staged scope |
| Detected by | Full cache-key comparison and final uncached gate requirement |
| Trigger | Cross-tree or cross-environment cache reuse |
| Immediate response | Set cache mode off, discard the suspect local receipt, and run the authoritative path uncached |
| Restored surfaces | Local cache state and orchestration only; tracked authority and scientific state remain unchanged |
| Re-entry evidence | Conservative cache audit, negative reuse fixture, and uncached exact-tree parity |
| Result | `PASS_TABLETOP` |

Cache failure cannot convert stale evidence into validation or physics
authority. Cache disablement is always a safe fallback.

## Destructive retirement citation audit

No active destructive-retirement AgentJob exists. The future inventory has one
conditional retirement branch in P3-T04, one assessment-only packet in P9-T04,
and one destructive compatibility-retirement packet in P11-T05. The policy
requires any actual retirement AgentJob, especially P11-T05, to cite
`research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md`
in its allowed reads and completion source basis and to name replacement,
parity, rollback, reference-migration, and historical-readability evidence.

Result: `PASS_NO_ACTIVE_DESTRUCTIVE_JOB`; future citation gate is explicit.

## Full-profile instrumentation matched pairs

The three pairs ran alternately on clean commit
`57438af555214bc0785dcb390ee6254f580b8a62`, Git tree
`e33993071fba583aaa48f27366744ccf98cee395`, scope `commit_tree`, Apple M3
Ultra, Python 3.12.13, dependency-lock hash
`d36a504821c016637dfb496f08134fcb44bf027a490abd7132457e8c64253a2a`,
and declared cache state `disabled`.

| Pair | Uninstrumented | Instrumented | Pair overhead | Status parity | Trace events | Distinct gate IDs | Reported duplicate identities |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 1 | 80.97 s | 81.44 s | 0.580% | 14/14 PASS in both | 25 PASS | 17 | 3 |
| 2 | 82.16 s | 78.38 s | -4.601% | 14/14 PASS in both | 25 PASS | 17 | 3 |
| 3 | 84.30 s | 85.54 s | 1.471% | 14/14 PASS in both | 25 PASS | 17 | 3 |

Median pair overhead is 0.580 percent. Median uninstrumented duration is 82.16
seconds and median instrumented duration is 81.44 seconds. Every command label,
return code, and aggregate status matched. The repeated identities are legacy
baseline observations; no work was removed or treated as additional evidence.

### Budget disposition

The full-profile portion now has three matched pairs below the two-percent
target and five-percent hard guard. `V19-PERF-TRACE-001` remains
`PROVISIONAL_NONBLOCKING` because its activation rule also requires three
matched pairs for affected and checkpoint profiles. No hard budget is
activated by P1-T05.

### Local evidence hashes

| Evidence | SHA-256 |
| --- | --- |
| Pair 1 uninstrumented full receipt | `117429ccddb1fc445d2f662de151969aff75564212d3804e221c0ab45bf4a715` |
| Pair 1 instrumented full receipt | `82496b3dd87b9c1ce0d59d3da0eb2a85b7c92b3075462bf5ba01d8012f9f251d` |
| Pair 1 trace summary | `89e45ebe305e242e23cd0767b8a4e14bdf1bb160e2d6924e2cb79425b6d24fe4` |
| Pair 2 uninstrumented full receipt | `95296fcc267c0da77e0e6636e07a598acaf748965dffcff91a444f834ae95244` |
| Pair 2 instrumented full receipt | `f2eb3e162dc808a231717c06e95c07ca4c96c566faeade223dc23241b49cb69d` |
| Pair 2 trace summary | `053fe9d2b7dad8e046fcf0e05399f719930ba045f1f1b8847dcf7ffb65ee0671` |
| Pair 3 uninstrumented full receipt | `e53f7b5c5b1d907dd38e593f23a4aacb1e8000e37d8ca0cebd3d58b1dbec7bd6` |
| Pair 3 instrumented full receipt | `ac0809ebf120033af0608077cebefa3e864415394db75d50d452b3ff402b0213` |
| Pair 3 trace summary | `f68735129805e80e80c8cb7a6c4405fa10cf5fa2b435f6c3c20d6f0a2d614351` |

Raw receipts remain ignored below
`.local/validation-traces/p1-t05-matched-pairs-e3399307/`. They are operational
diagnostics, not tracked authority.

## Acceptance matrix

| P1-T05 requirement | Evidence | Status |
| --- | --- | --- |
| Five migration epochs | Policy epoch state machine | PASS |
| Legacy authority in shadow mode | Shadow comparison contract | PASS |
| Planner, cache, compact-output, and fallback switches | Feature-switch table | PASS |
| Three clean shadow runs plus adversarial corpus required before cutover | Minimum cutover evidence | PASS_POLICY |
| Rollback triggers cover findings, paths, index, cache, output, and performance | Rollback trigger table | PASS |
| Make, CI, skills, checkpoint, cache, and output restoration | Restoration matrix | PASS |
| Planned P2 and cache-failure tabletop drills | This report | PASS |
| Destructive retirement citation requirement | Policy and audit above | PASS |
| No scientific or orchestration authority expansion | Claim boundary and policy | PASS |

## Authority boundary

This report is project-control evidence only. It does not activate a planner,
cache, compact output, supersedence, deduplication, hard performance guard, or
legacy retirement. It does not prove a physics claim or advance Distance-to-GR.
`handoff-0740` and `EqSrc_family_closure_repair_or_stress` remain unchanged.
