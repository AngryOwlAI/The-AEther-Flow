<!-- authority: control -->

# V17 Candidate Audit-Lane Disposition

## Status

```yaml
plan_task_id: "P1-T04"
selected_disposition: "route_to_smuggling_audit"
selected_next_plan_task_id: "P2-T01"
candidate_status: "audit_eligible_only"
physics_promotion_authorized: false
distance_to_gr_delta: "none"
```

P1-T04 selects exactly one disposition for the existing
`SourceCouplingLawCandidate_EStar_v1` candidate after the P1-T03
target-floor self-check. The selected disposition is
`route_to_smuggling_audit`.

## Inputs

| Input | Status | Use |
| --- | --- | --- |
| `handoff-0621` | completed | Requires one bounded P1-T04 Director handoff packet. |
| P1-T03 self-check | pass | Records all six target-floor fields as pass and `primary_fail_closed_branch: none`. |
| v17 P1-T04 plan text | inspected | Requires exactly one candidate disposition and no Gate Chair route before later audit and stress support. |
| v17 backlog P1-T04 row | inspected | Routes successful P1-T04 to P2-T01. |
| Route-orbit advisory warning | inspected | Does not create a hard gate or physics authority; P1-T04 records why Gate Chair is not lawful yet. |

## Candidate Disposition Table

| Candidate disposition | Selected | Reason |
| --- | --- | --- |
| `route_to_smuggling_audit` | yes | P1-T03 passed all six target-floor fields, recorded no primary fail-closed branch, and marked the candidate eligible for smuggling audit. |
| `route_to_repair_candidate_constructor` | no | No failed P1-T03 field or construction defect was recorded. |
| `route_to_refuter_for_obstruction_stress` | no | No obstruction exists to stress-test; refuter stress remains downstream of audit disposition. |
| `route_to_theoretical_selector` | no | The next execution role is determined directly by the v17 plan and P1-T03 result. |
| `route_to_freeze_review` | no | No repeated-burden hard gate, scoped obstruction, or failed candidate floor is present. |

## Selected Next Route

```yaml
selected_next_route:
  route_id: "v17_p2_t01_smuggling_audit_of_source_side_coupling_law_candidate"
  plan_task_id: "P2-T01"
  role_family: "smuggling-auditor@0.2.0"
  target_derivation_milestone: "matter_coupling"
  milestone_burden: "Audit the coupling-law candidate for target import, detector import, stress-energy import, matter-action import, benchmark import, and process-authority laundering."
  requires_human_gate: false
```

The next bounded packet should audit the existing `K_{E_*}` candidate. It
must not reconstruct the candidate, stress-test it as a refuter packet, or
route to Gate Chair authority.

## Gate Advisory Disposition

The resolver reported an advisory `gate_ready_without_gate` warning. P1-T04
does not select a Gate Chair route because the plan explicitly blocks Gate
Chair routing unless a later audit and stress chain supports a protected
question. At this point audit success and stress success do not exist.

## Claim Boundary

The P1-T04 handoff does not establish any of the following:

- source-law adoption
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption
- unrestricted `RR_E` theorem
- matter-semantics adoption
- detector-semantics adoption
- coupling-law adoption
- matter-coupling derivation or adoption
- stress-energy semantics or stress-energy tensor
- matter action
- Einstein equations
- benchmark promotion
- proof authority
- completed derivation

## Distance-To-GR Effect

No Distance-to-GR ledger row changes. P1-T04 selects the audit lane only. The
`matter_coupling` burden remains accepted only as scoped source-extension
evidence/precondition, with coupling-law adoption and matter-coupling
derivation still blocked.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.

The AEther-Flow Research Project. (2026b). *Handoff 0621* [Internal
research-control handoff]. `research_control/handoffs/handoff-0621.yaml`.

The AEther-Flow Research Project. (2026c). *Source-side coupling-law candidate
self-check v1* [Internal control artifact].
`research_control/tasks/RT-20260705-048/artifacts/source_side_coupling_law_candidate_self_check_v1.yaml`.
