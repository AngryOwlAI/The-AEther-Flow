<!-- authority: control -->

# V19 Validation Performance and Safety Budget

## Status and authority

This document freezes the acceptance budgets for v19 before any optimization
changes validator, test, checkpoint, Make, skill, or CI behavior. It is
project-control policy, not physics evidence. The budgets are measurement and
rollback constraints for later v19 tasks; they do not authorize removal of a
gate, orchestration cutover, cache reuse, or path filtering.

The frozen baseline sources are:

- `research_control/tasks/RT-20260712-003/artifacts/v19_baseline_benchmark.json`
- `research_control/design/v19_legacy_validation_invocation_graph.json`
- `implementations_plans/recommendations_implementation_plan_continue_task-v19.md`

The ordinary research authority remains `handoff-0740`. Timing, output size,
PASS counts, cache hits, receipts, CI status, and duplicate counts are
operational evidence only. None is a physics proof or Distance-to-GR advance.

## Budget-state vocabulary

- **Target** is the intended steady-state acceptance range.
- **Hard guard** is the rollback boundary after its activation condition is met.
- **Advisory trend** detects regression before a hard guard is crossed.
- **Comparable** means the measurement satisfies the environment, repository,
  scope, instrumentation, and cache rules below.
- **Provisional nonblocking** means a threshold is frozen but cannot block or
  authorize cutover until its comparability activation condition is satisfied.

Safety budgets are blocking immediately because their pass criteria are
semantic invariants. Performance and output hard guards become blocking only
at the activation point stated for each budget. A performance gain never
compensates for a safety failure.

## Comparable measurement protocol

Every performance claim must name a baseline receipt and a post-change receipt.
Both receipts must record the exact tree or commit, selected profile and gate
IDs, implementation and configuration digests when available, Python version,
dependency-lock digest, machine or CI runner identity, cache state,
instrumentation state, duration, subprocess count, output bytes, and status.

Local runtime comparisons are comparable when they use the same machine class
as the P0-T03 baseline (`Mac15,14`, Apple M3 Ultra), Python 3.12, the same
dependency-lock digest, the same declared cache state, the same validation
profile and representative transaction corpus, and equivalent instrumentation.
OS patch changes are allowed only when recorded and when a three-run control
shows no unexplained environment regression. Otherwise the result is trend
evidence, not a hard-guard result.

CI comparisons are comparable only within the same runner class, dependency
setup policy, cache policy, workflow responsibility, and declared gate union.
Path-filtered CI is not comparable to the unfiltered baseline unless the
receipt separately proves the full declared gate union.

Runtime activation requires at least three comparable successful post-rollout
runs. Use the median for the primary comparison and retain every individual
run. CI also requires at least three comparable successful official runs.
Output and duplicate-identity budgets may activate earlier because they are
deterministic for one declared plan and console rendering mode, but complete
receipt preservation must already be demonstrated.

## Runtime, CI, duplication, and output budgets

| Budget ID | Metric and scope | Target | Hard guard | Advisory trend | Measurement method | Activation and comparable rule | Rollback threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `V19-PERF-FULL-001` | Unfiltered full repository suite on comparable local hardware | 100-160 s | 180 s | Investigate a median above 160 s or a greater than 10% regression from the last accepted comparable median | Wall-clock monotonic duration for the complete declared full profile; receipt records tests, gates, subprocesses, parses, output, cache, tree, and environment | Provisional nonblocking until three comparable PASS runs exist with the same full gate union and equivalent instrumentation | Block cutover or restore the last authoritative orchestration if the three-run median exceeds 180 s, or if two consecutive comparable runs exceed 180 s after activation |
| `V19-PERF-AFFECTED-001` | Representative affected-loop validation before checkpoint | 5-30 s | 45 s | Investigate a median above 30 s or a greater than 10% regression | Monotonic duration across the frozen representative change-family corpus, reported per case and as median and maximum | Provisional nonblocking until the change matrix and at least three comparable runs per representative family exist; unknown governed paths fail closed | Block affected-profile authority or restore the prior selector if the corpus median exceeds 45 s, any required family is omitted, or two consecutive comparable medians exceed 45 s |
| `V19-PERF-CHECKPOINT-001` | Representative governed checkpoint transaction | 60-90 s | 120 s | Investigate a median above 90 s or a greater than 10% regression | End-to-end monotonic duration from entry-index snapshot through final index-integrity result, excluding an explicitly recorded human wait | Provisional nonblocking until three comparable PASS transactions use the same representative corpus and preserve final staged checks | Block checkpoint cutover or restore the legacy checkpoint path if the three-run median exceeds 120 s or two consecutive comparable transactions exceed 120 s |
| `V19-PERF-CI-001` | Main CI validation critical path after v19 rollout | at most 300 s | 480 s | Investigate a three-run median above 300 s or a greater than 10% regression | Official CI job timestamps for the declared blocking critical path plus gate-union receipt; setup and cache state remain explicit | Provisional nonblocking until three comparable official PASS runs exist after deduplication and the same blocking gate union is proven | Block CI topology promotion or restore the last accepted workflow if the three-run median exceeds 480 s or two consecutive comparable official runs exceed 480 s |
| `V19-PERF-TRACE-001` | Validation tracing and receipt instrumentation overhead | at most 2% of matched uninstrumented duration | 5% | Investigate an overhead median above 2% | Alternating matched instrumented and uninstrumented runs on the same tree, scope, environment, and cache state | Provisional nonblocking until at least three matched pairs exist for affected, checkpoint, and full profiles | Disable or repair the new instrumentation before cutover if median overhead exceeds 5%, or if tracing changes status, findings, tracked state, or exit code |
| `V19-DUP-IDENTITY-001` | Duplicate deterministic gate evidence identities within one scope and exact tree | 0 | 0 unexplained duplicates | Any nonzero count is reported with gate and parent IDs | Expand the executed plan and count repeated canonical evidence-identity tuples; declared replay and nondeterminism experiments are tagged and counted separately | Activates when the planner can emit stable evidence identities; legacy counts remain baseline observations | Block plan authority or restore the prior plan if any unexplained duplicate identity executes; an explicit replay experiment is not a violation but cannot satisfy an additional obligation |
| `V19-OUT-PASS-001` | Default console output for a successful gate or aggregate run | at most 1 KiB | 2 KiB | Investigate output above 1 KiB | Count UTF-8 bytes written to stdout and stderr in default compact mode; full detail is hashed in a receipt file | Activates when the compact reporter preserves the complete machine-readable receipt and deterministic status | Disable compact-mode promotion or repair the reporter if output exceeds 2 KiB, omits required summary fields, or changes status |
| `V19-OUT-FAIL-001` | Default console summary for a failed gate or aggregate run | at most 4 KiB | 8 KiB | Investigate output above 4 KiB | Count UTF-8 stdout and stderr bytes for the default bounded failure view while comparing its IDs and counts with the full receipt | Activates only after adversarial fixtures prove that the full receipt retains every finding | Disable compact-mode promotion or repair the reporter if output exceeds 8 KiB, loses a hard finding or receipt reference, changes ordering nondeterministically, or changes exit status |
| `V19-OUT-FINDINGS-001` | Actionable findings rendered in the default failure summary | at most 5 | 10 | Investigate summaries needing more than 5 to identify the failed groups | Count rendered actionable findings; group totals and the full receipt remain complete | Activates with `V19-OUT-FAIL-001` after full-receipt parity is proven | Disable or repair compact rendering if more than 10 findings are rendered by default or if bounding hides a hard-finding group, count, ID, or receipt path |

Subprocess launches, registry parses, graph builds, cache hits and misses, gate
counts, and output bytes are mandatory instrumentation fields under
`V19-R43`. Until comparable task-specific baselines exist, their reduction is
an advisory trend rather than an independent deletion target. They may explain
runtime movement but cannot authorize removal of a unique invariant.

## Non-negotiable safety budgets

| Budget ID | Protected safeguard and pass criterion | Measurement method | Comparable rule | Rollback threshold |
| --- | --- | --- | --- | --- |
| `V19-SAFE-STAGED-ALLOWLIST-001` | Final staged paths are a subset of the selected AgentJob allowlist and the exact staged tree is the one accepted | Compare final staged paths and tree hash with the AgentJob and aggregate receipt | Applies to every governed checkpoint; no working-tree or pre-generation result is comparable | Any unauthorized path, wrong tree, or missing final comparison is immediately blocking and requires restoration of the entry index and prior checkpoint path |
| `V19-SAFE-AUTHORITY-001` | Role authority, execution overlay, required human gate, and protected adoption boundaries all pass | Run registered role, overlay, decision, and approval validators and retain finding IDs | Applies to every governed task; performance environment variance is irrelevant | Any missing or bypassed role or human gate is immediately blocking; roll back the transaction and orchestration change |
| `V19-SAFE-CLAIMS-001` | Changed claim-bearing paths pass the complete applicable claim taxonomy and reviewed-context rules | Compare changed-path selection and normalized hard findings with the authoritative legacy result during migration | Same base reference, path set, taxonomy, configuration, and exact tree are required | Any missing hard finding, path, taxonomy class, or reviewed-context check is immediately blocking and requires rollback |
| `V19-SAFE-RESIDUE-001` | No unauthorized unstaged transaction residue remains after final staged validation | Compare final working tree, index, entry snapshot, and allowlist after all mutators | Only the final post-generation state is comparable | Any unexplained residue, index-restoration failure, or post-validation mutation is immediately blocking and requires index restoration and rollback |
| `V19-SAFE-WHITESPACE-001` | Final transaction passes Git whitespace validation | Run `git diff --check` against the exact final transaction state | Same diff scope and exact tree are required | Any whitespace error is immediately blocking; no runtime benefit overrides it |
| `V19-SAFE-SOURCE-AUTHORITY-001` | Canonical sources and registries remain authoritative; generated derivatives are not hand-edited or treated as independent proof | Validate source registration, source hashes, provenance, generated-output boundaries, and protected paths | Applies to every affected authority surface; output or runtime measurements are irrelevant | Any authority inversion, manual derivative edit, stale required derivative, or validator-as-proof promotion is immediately blocking and requires rollback |
| `V19-SAFE-LIVE-SUBSYSTEM-001` | The full acceptance corpus retains at least one live acceptance path for research control, dependency graph, memory core, publication/documentation, scientific-support families when affected, and local retrieval health in its proper doctor or scheduled scope | Enumerate subsystem obligations in the manifest and map each to one executed live acceptance or an explicit unaffected determination; scheduled runs retain the unfiltered live cases | Fixture tests are not comparable substitutes for the retained live acceptance; local retrieval remains operational rather than tracked authority | Removing the last live acceptance for a subsystem, or misclassifying local-only evidence as transaction authority, is immediately blocking and requires restoration |
| `V19-SAFE-SCHEDULED-FULL-001` | An unfiltered scheduled full validation remains enabled and cache-bypasses the declared nondeterminism and coverage backstops | Inspect the authoritative CI schedule and its emitted unfiltered gate union | A path-filtered or cache-only run is not comparable | Missing, filtered, disabled, or silently cached scheduled-full coverage blocks rollout and requires restoration of the last accepted schedule |

## Cross-budget decision law

1. Safety failures are blocking on the first observed occurrence.
2. Performance hard guards do not activate until their explicit comparability
   requirements are met; before activation they are trend evidence only.
3. Output bounding changes presentation only. The complete machine-readable
   finding set, counts, status, provenance, and receipt hash remain available.
4. A budget cannot be met by deleting, skipping, suppressing, downgrading, or
   path-filtering the last implementation of a unique invariant.
5. Unknown gate equivalence is non-deduplicable. Working-tree evidence never
   satisfies a staged-tree obligation, and pre-generation evidence never
   satisfies a post-generation obligation.
6. Baseline and post-change receipts are required for every performance claim.
7. Threshold changes require a new tracked Project-System Director decision,
   an updated budget source, documentation-impact evidence, and validation.
   Silent threshold drift is prohibited.

## Frozen baseline interpretation

P0-T03 recorded a 515.455-second repaired clean-clone PASS for 584 tests on the
M3 Ultra and a 565.154-second exact current-state run with two state-contract
baseline failures. The historical audit recorded 507.215 seconds for the full
suite and 1,025 seconds for the CI validation step. These are indicative
baselines, not variance estimates. The P0-T04 graph recorded 37 provisional
gates, 53 concrete invocations, three direct same-state subset/superset pairs,
six legitimate cross-scope repetitions, and no unresolved invocation.

The runtime targets are therefore frozen as desired v19 outcomes, while their
hard guards remain provisional until comparable post-rollout evidence exists.
The safety budgets are not provisional.

## Review result

P0-T05 freezes nine performance, duplication, and output budgets and eight
non-negotiable safety budgets. Every budget has a measurement method,
comparison rule, and rollback threshold. The policy preserves complete
failure-mode coverage and grants no physics, proof, benchmark, cache, CI,
checkpoint, or orchestration authority.
