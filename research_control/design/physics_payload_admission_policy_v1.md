<!-- authority: control -->

# Physics Payload Admission Policy v1

## Purpose

`physics_payload_admission_policy_v1` implements v21 P12-T01 as a prospective
AgentJob admission gate. A physics-facing job must name a materially new
payload and the assumptions, candidate family, source basis, and expected
artifact that make the declaration auditable. A project-system job must use a
separate admission path and explain why its output is control machinery rather
than physics progress.

The policy evaluates the shape and authority boundary of a proposed packet. It
does not establish that a theorem is true, that a proof is sound, that an
external result is correct, that an obstruction is global, or that a candidate
should be adopted. It creates no ontology, source-law, metric, Distance-to-GR,
benchmark, publication, or Gate Chair authority.

## Activation and Compatibility

```yaml
physics_payload_admission_policy:
  policy_id: "physics_payload_admission_policy_v1"
  schema_id: "physics_payload_admission_v1"
  active_after: "2026-07-22T16:24:16Z"
  enforcement: "hard_failure"
  applies_to: "prospective AgentJobs"
  historical_jobs_without_block: "legacy_readable"
  theorem_truth_evaluated: false
  physics_promotion_authorized: false
```

AgentJobs created after `active_after` must include
`physics_payload_admission`. Older AgentJobs remain readable without the
block. A historical record that voluntarily contains the block may still be
checked, but the absence of a block cannot invalidate it retroactively.

## Admission Paths

The expected path is determined independently of the job's declaration.

- `physics` applies when the task taxonomy scope is `scientific`,
  `scientific_audit`, or `mixed`, or when the selected role is a registered
  physics role. A theoretical-continuation selector remains physics-facing.
- `project_system` applies to project-control, methodology, validation,
  documentation, routing-support, and other non-physics tasks. These packets
  use `payload_type: not_applicable` and cannot count as physics progress.

A declaration that disagrees with the independently derived path fails.

## Required Common Record

```yaml
physics_payload_admission:
  schema_id: "physics_payload_admission_v1"
  policy_id: "physics_payload_admission_policy_v1"
  admission_path: "physics"
  payload_type: "proof_step"
  candidate_family: "named candidate or source family"
  assumption_delta:
    - "new, removed, narrowed, or explicitly unchanged assumption and why"
  materiality_basis: "why the proposed artifact is new payload"
  source_basis:
    - "canonical object ID or source path"
  expected_artifact_paths:
    - "repo-relative expected output path"
  process_receipts_excluded_from_payload:
    - "validator_pass"
    - "checkpoint_pass"
    - "documentation_receipt"
    - "role_or_route_selection"
  authority_limits:
    theorem_truth_inferred: false
    scientific_status_changed: false
    ontology_or_source_law_adopted: false
    distance_to_gr_changed: false
    physics_promotion_authorized: false
```

`candidate_family` and `assumption_delta` are required even when the expected
outcome is negative. An unchanged assumption set must say what remains fixed
and why; a bare `none` is not sufficient.

## Qualifying Physics Payload Types

The controlled types are:

- `theorem`;
- `proof_step`;
- `countermodel`;
- `source_law`;
- `external_result`;
- `independent_replication`;
- `justified_ledger_delta`;
- `source_acquisition`;
- `precise_obstruction`;
- `finite_witness`;
- `source_model`;
- `candidate_construction`;
- `route_decision`.

The label is an admission declaration, not a success verdict. A proposed
`theorem`, `proof_step`, or `source_law` remains draft/control or proposal-only
until its own completion, review, and protected gates say otherwise.

### Source acquisition

Missing local evidence is not a reason to manufacture a result or stop an
authorized research route. `source_acquisition` is admissible when
`payload_details` names a concrete `acquisition_target` and sets
`primary_source_requirement: true`. Acquired material remains external source
evidence; it is not automatically a project theorem or ontology input.

### Precise obstruction

`precise_obstruction` is admissible when `payload_details` names the exact
`obstruction_scope` and sets `global_no_go_claimed: false`. A scoped failure
cannot be strengthened into impossibility without a separate no-go theorem.

### Route decision

Selector-only work is not material merely because a role or route was chosen.
`route_decision` is admissible only when `payload_details` sets
`resolves_new_route_decision: true`, provides a stable `decision_identity`,
and cites `not_already_encoded_evidence`. Ordinary routing receipts and
restatements of an existing handoff fail admission.

## Project-System Record

A project-system job uses the common record with:

```yaml
admission_path: "project_system"
payload_type: "not_applicable"
candidate_family: "not_applicable"
project_system_justification: "specific control output and boundary"
```

It must still declare an `assumption_delta`, `source_basis`, expected artifacts,
process-receipt exclusions, and false authority flags. This makes support work
auditable without relabeling it as physics.

## Non-Payload Receipts

The following never satisfy physics admission by themselves:

- validator or test PASS;
- checkpoint, registry, documentation, or handoff receipts;
- role selection, route selection, or task creation;
- generated derivatives or dashboards;
- agreement, confidence, or reviewer count;
- a Distance-to-GR edit without a separately justified new evidence object.

## Completion Boundary

Admission answers only: "Is this a bounded, auditable packet with a qualifying
declared payload or an honestly separate project-system purpose?" Completion
must still validate the produced artifact, preserve claim gates, and record a
precise result. Neither admission nor completion may infer scientific truth
from process cleanliness.
