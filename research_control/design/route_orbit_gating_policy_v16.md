<!-- authority: control -->

# Route-Orbit Gating Policy v16

## Purpose

`route_orbit_gating_policy_v16` converts route-orbit diagnostics from
advisory observations into selective control gates for v16 continuation.

The policy is intentionally narrow. It prevents repeated same-burden
process-only cycling, but it does not block legitimate theorem decomposition,
finite/local construction, certificate work, red-team integration, or required
validator repair.

This is a project-control policy. It is not a physics proof, not a global
no-go theorem, not a route rejection theorem, not source-law adoption, not
matter-coupling derivation, not benchmark promotion, and not a completed
derivation claim.

## Definitions

`route orbit` means a repeated continuation pattern where the project keeps
returning to the same derivation burden without adding mathematical payload,
finite/local evidence, a countermodel, a source model, a certificate instance,
an executable support specification, a required validation repair, a newly
required protected gate, or an external review finding that must be integrated.

`same-burden task` means a completed task whose `target_derivation_milestone`
and `milestone_burden` match the previous task in the candidate run.

`weak payload` means a packet whose completion depends mainly on process
receipts, routing labels, registry rows, generated derivatives, validation
status, or restated evidence status rather than a payload class from
`minimum_physics_payload_schema_v1`.

`legitimate multi-packet theorem work` means a sequence of packets that shares
a burden but adds one or more of the following:

- a new definition;
- a theorem statement;
- a proof attempt;
- a proved conditional theorem;
- an explicit finite witness;
- a minimal countermodel;
- an obstruction record;
- a source model;
- a certificate instance;
- an executable support specification;
- an attack fixture;
- a scored route matrix with new criteria or evidence;
- a validation repair needed before honest continuation;
- a protected gate transition that cannot lawfully be skipped;
- an external red-team finding requiring integration.

## Hard-Gate Rule

A `freeze_review` or `validation_repair` selector is required when three
consecutive same-burden tasks satisfy all of these conditions:

1. The same `target_derivation_milestone` is repeated.
2. The same `milestone_burden` is repeated.
3. No new mathematical payload is recorded.
4. No new finite/local witness is recorded.
5. No new countermodel is recorded.
6. No new source model is recorded.
7. No new certificate instance is recorded.
8. No new executable support specification is recorded.
9. No validator failure requiring repair is present.
10. No protected gate has newly become required.
11. No external red-team finding requires integration.

When the hard gate triggers, the next packet must do exactly one of the
following:

- perform a freeze review and choose a lawful route status;
- run a repair selector that names the failed process or validator condition;
- route to a protected gate when the repeated burden is gate-ready and the
  required authority exists;
- withdraw or narrow the repeated burden with explicit evidence.

The hard gate does not prove the route impossible. It only blocks further
process-only repetition under the same burden.

## Advisory-Warning Rule

Emit a warning, but do not hard-gate, when any of these conditions occurs:

- two same-burden tasks occur with weak payload;
- a selector repeats the same route but adds a scored matrix with new evidence;
- a documentation-only task follows a physics task;
- a validator or renderer refresh creates no physics payload but is required;
- a support-only executable specification is introduced before standing
  validator integration;
- current-frontier or dependency-graph rendering changes only generated
  derivatives.

Advisory warnings remain operational diagnostics. They do not change physics
authority, prove obstruction, or promote any result.

## Exemptions

The hard-gate rule must not trigger when a same-burden sequence is making
tracked progress through one of these lawful routes:

- theorem decomposition with new premises, lemmas, cases, or failure branches;
- finite/local source-model construction;
- certificate-instance construction or audit;
- countermodel minimization;
- source-extension stress or smuggling audit;
- target-import attack fixture creation;
- validation repair after an actual validator failure;
- external red-team finding integration;
- Gate Chair review under explicit human authorization;
- publication or documentation packet that explicitly classifies itself as
  non-physics project work.

## Gate Outputs

Future validators or reports should classify route-orbit evaluation as:

```yaml
route_orbit_gate:
  status: "PASS | WARN | HARD_GATE"
  policy_id: "route_orbit_gating_policy_v16"
  evaluated_task_ids:
    - "RT-YYYYMMDD-NNN"
  repeated_target_derivation_milestone: "matter_coupling"
  repeated_milestone_burden: "example burden"
  consecutive_same_burden_count: 3
  payload_evidence_paths:
    - "research_control/tasks/RT-YYYYMMDD-NNN/artifacts/example.md"
  hard_gate_reason: "three same-burden no-payload tasks"
  required_next_packet: "freeze_review | validation_repair | protected_gate | burden_narrowing"
  physics_claim_authority_created: false
```

`PASS` means no route-orbit concern is detected. `WARN` means a sequence
should be watched but may continue. `HARD_GATE` means the next packet is
restricted to one of the listed gate outputs.

## Relationship To Minimum Payload Schema

The policy depends on `minimum_physics_payload_schema_v1` for payload
classification. Process receipts excluded by that schema must not be counted
as physics payload for route-orbit purposes.

The policy does not itself implement validator enforcement. It supplies the
control contract for P7-T03 or later validator work.

## Done Criteria

- Three same-burden no-payload cycles require freeze review or repair.
- Two weak same-burden cycles warn but do not hard-gate.
- Legitimate multi-packet theorem, witness, countermodel, source-model,
  certificate, attack-fixture, red-team, and validator-repair work remains
  permitted.
- The policy explicitly rejects global no-go overread.
- The policy creates no physics delta and no proof authority.
