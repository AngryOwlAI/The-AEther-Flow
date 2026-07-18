---
authority: control
object_id: "MD-V20-GOAL-RELAY-EXECUTION-POLICY-V3"
task_id: "RT-20260718-012"
plan_id: "recommendations_implementation_plan_continue_task-v20"
plan_task_id: "P0-T03"
schema_version: "v20-goal-relay-execution-policy.v3"
status: "active"
owner_skill: "continue-research-goal"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
---

# V20 autonomous `continue-research-goal` execution policy

## Authority and supersession

This policy is the governed P0-T03 supersession for autonomous goal pursuit.
It replaces P0-T03's immediate-stop assumptions only where the user-authorized
autonomous-relay plan and the tracked `continue-research-goal.v3` contract say
that a safe, authorized recovery or independent in-scope route must continue.
The original v20 plan, P0-T02 backlog, v1/v2 goal records, and completed P0-T02
transaction remain historical evidence and are not rewritten.

The runtime launcher skill, relay-worker skill, goal schema, and state helper
are the executable contract. This policy describes and validates that contract;
it grants no scientific, ontology, Gate Chair, publication, push, or external
system authority.

The relay terminates only when one of these conditions is established from
canonical evidence:

1. the exact goal completion contract is met;
2. the user cancels or an explicit finite pass/deadline guard is reached; or
3. no safe authorized AI recovery or dependency-independent in-scope route
   remains, and an evidence-backed record names the smallest specific human
   action required.

## Immutable launch contract

Every new goal is a `continue-research-goal.v3` record initialized through the
helper. The original goal text is preserved byte-for-byte. Initialization also
records and hashes:

- an effective completion contract;
- repository, branch, HEAD, saved-project, and launcher bindings;
- explicit scheduling guards, including JSON `null` for omitted guards;
- an immutable `scope_contract`;
- the first immutable generation route.

The launcher may use `single_objective` or `multi_step` scope:

- `single_objective` is the default for a task-specific request. Its one work
  item may use several generations or tracked transactions, but unused passes
  may not implement another plan task.
- `multi_step` is lawful only when the original user goal explicitly includes
  every work item. Its contract records exact work-item identifiers,
  dependencies, dependency-source evidence, exclusions, and source hashes.
  It may advance only to a listed dependency-ready item.

`cross_task_relay_reuse: false` forbids repurposing a task-specific goal. It
does not forbid an explicitly initialized `multi_step` goal from completing
multiple included tasks. Neither mode may broaden the original goal.

For this P0-T03 transaction the scope is `single_objective`: implement and
validate the v3 relay policy. P0-T04 is deliberately outside its scope and
requires a fresh user-authorized goal.

## Generation and worker invariants

There is at most one live continuation and one outer worker frame per
generation. Every state-changing research or project-system repair frame
consumes one pass. Every explicit deadline applies to every frame.

Each generation has an immutable route containing:

- `worker_skill`: `continue-research` or `improve-project-system`;
- `reason_id` and `strategy_id`;
- `source_generation`;
- `work_item_id`;
- canonical `blocker_fingerprint`;
- evidence hashes; and
- an exact dirty-state manifest when a repair route owns dirty state.

`reserve-successor` copies the already-approved route. It cannot accept an
arbitrary replacement worker, task, or strategy. `consume` and `returned`
must match the routed worker skill. A generation invokes its worker at most
once and a consumed generation is never rerun.

Worker prose is telemetry. Progress, completion, dispatch, repair, and stop
decisions derive from tracked task state, AgentJob and completion records,
Git checkpoints, validators, immutable hashes, and other canonical evidence.

## Autonomous routing table

| Observed canonical condition | Required route | Lawful stop |
| --- | --- | --- |
| Completion contract proven | Atomically record `terminal_complete`, release leases, and store the deterministic completion summary | Immediate success |
| A dependency-ready included item remains | Approve a fresh `continue-research` route for that item | Never solely because an included task boundary was crossed |
| An attributable validator, checkpoint, generated-derivative, or dirty-state failure exists | Use `improve-project-system` when classifier, resolver, or signal evidence selects it; otherwise use a task-local `continue-research` repair | Only when no authorized repair fits or the current state differs from the exact manifest |
| No progress, repeated fingerprint, missing datum, or indeterminate result | Enter `recovery_required` with a materially distinct strategy selected from tracked authority | Only after all applicable distinct strategies are exhausted |
| One work item reaches a protected human gate but an independent included item remains | Mark the gated item `deferred_human_gate` and continue the independent item | Only when every remaining required item depends on protected human action |
| Dispatch definitively created no child | Reinspect, record recovery evidence, and reserve a fresh generation | Not merely for the zero-child result |
| Dispatch created exactly one matching unclaimed child | Adopt that child without creating another | Not applicable |
| Dispatch is ambiguous, duplicated, or capability is unavailable | Preserve evidence and terminalize with exact human intervention | Immediately |
| A finite pass or deadline guard is reached | Preserve the guard without extension | Immediately, naming the extension-or-cancellation decision required |
| Protected authority, credentials, push/publication, goal expansion, repository/branch change, corrupt state, lease ambiguity, competing successor, or uncertain consumed invocation is required | Do not improvise | Immediately, with the smallest exact human action |

## Recovery ledger and loop prevention

`recovery_required` is nonterminal. Every approved recovery appends a ledger
entry linked to the source generation, journal event, route hash, blocker
fingerprint, evidence, and strategy. The same
`(blocker_fingerprint, strategy_id)` pair may execute only once. An unchanged
or repeated fingerprint therefore triggers strategy switching, not automatic
termination, while a distinct applicable strategy remains.

No arbitrary retry count substitutes for this ledger. Explicit user pass and
deadline caps remain authoritative, however, and are never auto-extended.

Allowed materially distinct strategies can include theoretical selection,
source acquisition, bounded calculation, candidate construction, refutation,
an ontology-law research packet within its existing authority, a task-local
repair, or governed project-system repair. Selection still comes from the
Director and current tracked routing authority; the relay does not invent
permissions.

## Dirty-state repair boundary

A failed transaction may cross into a repair frame only with an exact manifest
that records:

- owning task and AgentJob;
- current HEAD;
- complete porcelain state;
- each changed path and content hash; and
- each failed gate and evidence hash.

The manifest is hashed into the route. `consume` and `returned` must observe an
exact match. An unexplained path, hash, owner, HEAD, porcelain, or gate
difference requires human intervention. Repair may preserve and complete the
authorized transaction; it may not use dirty state as permission to widen
scope.

## Dispatch reconciliation

A definitive dispatch failure or timeout is reconciled only after the current
task state is inspected:

- zero matching children permits a new generation;
- exactly one matching unclaimed child is adopted;
- two or more matching children, a claimed or competing child, inability to
  inspect task state, or uncertain invocation consumption is ambiguous and
  requires human intervention.

The relay never steals a lease, deletes runtime evidence, retries an ambiguous
create, or starts a second live continuation.

## Terminal evidence and reporting

Every verified v3 frame stores a standardized `work_result` containing the
work-item status, task ID, AgentJob ID, completion path and hash, checkpoint
commit, validator results, progress summary, explicit zero-job reason when no
AgentJob was used, and out-of-scope remaining work.

Successful terminalization atomically stores a deterministic summary derived
from the exact original goal, completion contract, finalized receipts,
referenced tasks/jobs/completions, checkpoints, validators, final canonical
fingerprint, and work outside scope. `summarize` is read-only and validates the
record before rendering:

1. `Goal reached.`
2. the exact original goal quoted without normalization;
3. completed work across generations;
4. supporting task, AgentJob, completion, checkpoint, and validator evidence;
5. deliberately out-of-scope work; and
6. `That goal was reached.`

Every non-success terminal requires a `human_intervention` object proving that
safe authorized strategies were exhausted, listing attempted and remaining
strategies, binding the blocking evidence, and naming the exact required
action. Its report begins `Goal not reached — human action required`.

## Prohibited operations

No route may push, merge, rebase, open a pull request, publish, install a
plugin, weaken or skip validation, steal a lease, rerun a consumed generation,
hand-edit a goal record, use native goal operations in place of the helper,
expand the scope, change repository/branch binding, edit canonical ontology,
grant Gate Chair authority, or promote worker prose to evidence.

## Compatibility and completion boundary

The helper retains byte-compatible read and validation behavior for
`continue-research-goal.v1` and `continue-research-goal.v2`. Those records are
never migrated, mutated, or automatically resumed by v3.

The P0-T03 completion contract is met only when:

- the launcher, worker, schema/helper, and focused tests implement this policy;
- every scenario in `v20_goal_relay_scenarios.json` maps to a legal v3 state;
- the task validator verifies runtime tokens, source hashes, immutable
  P0-T02 history, and scenario coverage;
- affected research-control, documentation-impact, memory, and diff gates pass;
- a governed checkpoint records the exact transaction without push.

This project-control result changes no physics claim and produces
`no_distance_delta`.
