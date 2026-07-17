<!-- authority: control -->

# P7-T06 dependency-graph final audit

This is operational project-system evidence only. It changes no production
graph code, test, fixture, workflow, planner authority, ordinary research
state, scientific claim, benchmark status, proof status, or physics authority.

## Current result

The complete 18-test dependency-graph shard passes in 21.535 seconds. The
historical graph-module baseline was 378.598 seconds, so the observed
descriptive reduction is 357.063 seconds, or 94.312 percent. This is below the
frozen 45–90-second target maximum and the provisional 120-second hard guard.
The comparison uses the same Mac15,14 machine model, Python 3.12.13,
requirements digest, and warm-cache class, but the repository tree, corpus,
and instrumentation differ; it is trend evidence rather than an activated
hard-guard decision.

Three fresh snapshot/build/render transactions are byte-identical. Their
median total is 2.970185 seconds:

| Metric | Observed |
| --- | ---: |
| Sources captured and loaded once | 1,684 |
| Maximum loads for any source | 1 |
| Graph builds per transaction | 1 |
| Render calls per transaction | 3 |
| Nodes | 18,334 |
| Edges | 64,729 |
| JSON bytes | 55,048,052 |
| Markdown bytes | 16,811 |
| DOT bytes | 14,643,323 |
| Total serialized bytes | 69,708,186 |

The isolated live implicit-versus-explicit double-build passes in 6.302
seconds outside the fast path. The full-profile repository-test gate and graph
freshness gate remain selected and cache-ineligible under legacy execution
authority.

## Legacy assertion coverage

Every assertion family in the seven-test legacy module at
`bb0f9849c97d8e908b9b5fc15e0dd5ff42f08412` remains covered:

| Legacy assertion family | Current coverage |
| --- | --- |
| Required frontier and authority boundary | Separate shared-graph property tests plus negative fixtures |
| Edge referential integrity and class/provenance fields | Shared referential-integrity test plus malformed-edge fixtures |
| Unchanged-state determinism | Shared render hashes plus repeated and reordered synthetic builds |
| Freeze-summary overread protection | Retained focused freeze-summary test |
| CLI writes JSON, Markdown, and DOT | Combined write/fresh/stale lifecycle plus format-content test |
| Fresh CLI check passes | Combined lifecycle test |
| Stale CLI check fails | Combined lifecycle plus all-format mutation harness |

## Failure-mode audit

All nine plan-named mutations are detected with zero false passes:

| Mutation | Detection |
| --- | --- |
| Missing required node | `Resp_lc` required-frontier failure |
| Dangling edge | Specific missing target-node failure |
| Unknown class | `GraphBuilder` rejects the unknown node class |
| Stale JSON | `stale`, `fresh=false`, unequal hashes |
| Stale Markdown | CLI lifecycle and helper report the mutated format |
| Stale DOT | `stale`, `fresh=false`, unequal hashes |
| Missing file | Missing output fails freshness; missing source changes fingerprint |
| Authority overread | Exact non-authoritative boundary mismatch |
| Nondeterministic ordering | Reversed rows and handoff enumeration remain byte-identical |

The affected blocking legacy/planner comparison is also exact: 11 legacy
blocking gates and 11 planner blocking gates, with zero unexplained mismatch.
Legacy execution remains authoritative.

## Full-suite and residual boundary

The active-lifecycle repository suite ran 865 tests in 207.888 seconds with one
expected skip, one failure, and one error. Both findings are direct
active-transaction conditions: the active AgentJob intentionally has no
completion path, and `checkpoint_required_after_execution` remains false until
the job is completed. No implementation test failed.

After control closure, the stable completed-state repository suite passed all
865 tests in 208.159 seconds with one expected skip and zero failures or
errors. The 21.535-second graph shard accounts for 10.345 percent of that
current suite. Compared descriptively with the historical 507.215-second
baseline, the current run saves 299.056 seconds, or 58.960 percent.

Purely subtracting the observed graph-module saving from the historical
507.215-second suite gives 150.152 seconds, which lies in the frozen
100–160-second target; that arithmetic projection is not a current suite
measurement. The actual 208.159-second suite remains above the current
160-second target maximum and the provisional 180-second threshold. That
threshold is not an activated hard guard: the frozen budget requires three
comparable completed measurements, while P7-T06 provides one. The result is
therefore a PASS for P7-T06 with an explicit residual full-suite cost, not a
claim that the repository has reached its final runtime target.

The workflow runs full project-control validation on `main` pushes, pull
requests, and manual dispatch, but it has no cron trigger. This packet therefore
claims one scheduled-style full-profile live execution outside the fast path,
not scheduled-cron acceptance. CI-topology changes remain outside P7-T06.

The logical next route after fresh derivatives and a governed checkpoint is
P8-T01.
