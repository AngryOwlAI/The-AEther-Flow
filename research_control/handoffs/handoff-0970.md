<!-- authority: control -->

# Handoff 0970 — V22 P0-T03 is qualifying-complete

The tracked identity of this handoff is `handoff-0970`.

## Result

`RT-20260808-004` repairs the exact V21/V22 package-ID collision recorded by
`handoff-0969`:

- ordinary routing resolves the backlog named by `selected_next_route.plan_id`;
- completed dependencies use `(plan_id, plan_task_id)` identity;
- V21 handoffs retain their historical behavior;
- unknown plan identities fail closed;
- the exact uncheckpointed P0-T03 transaction is admitted only through a
  hash-bound atomic recovery record;
- `.gitignore` and versioned recommendation backlogs have exact classifier
  families; and
- V22 P1-T01 has an explicit project-system runtime route.

The task-local repair receipt has zero findings and the 117 focused route,
classifier, and checkpoint-planner tests pass. V22 P0-T03 is therefore
qualifying-complete. This is project-system evidence only; it changes no
scientific claim, Gate, benchmark, external-review, replication, publication,
or Distance-to-GR status.

## Next bounded route

After the single atomic governed checkpoint for `AJ-RT-20260808-004-001`, run
one separately admitted V22 `P1-T01` `improve-project-system` AgentJob. Its
scope is the three-track charter, authority matrix, separated scorecards and
budgets, typed cross-track links, non-promotion fixtures, and repository-split
decision criteria.

P1-T01 is selected but has not been executed. Do not begin P1-T02 or any later
package until its exact dependencies and runtime route are separately admitted.
No tag, public release, publication, submission, push, reviewer contact, or
other external action is authorized.
