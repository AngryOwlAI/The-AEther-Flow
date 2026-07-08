<!-- authority: control -->

# Minimal Countermodel Obligation Schema v1

## Metadata

```yaml
schema_id: minimal_countermodel_obligation_schema_v1
schema_for:
  - CountermodelObligationRecord_v1
  - registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv
authority_status: project_control
source_plan: implementations_plans/recommendations_implementation_plan_continue_task-v18.md
source_policy: research_control/design/minimal_countermodel_obligation_policy_v1.md
created_at: 2026-07-08T00:57:13Z
plan_task_id: P4-T02
recommendation_ids: ["V18-R03"]
physics_promotion_authorized: false
proof_authority: false
schema_update_no_physics_delta: true
next_plan_task_id: "P4-T03"
```

## Purpose

This schema materializes the P4-T01 minimal countermodel-obligation policy as
a machine-readable registry shape. The registry is an index of obligation
slots, result artifacts, and local overread guards for theorem or
theorem-like control packets.

The schema and registry do not prove any theorem, discharge general EqSrc,
adopt RetainH, adopt GenH, adopt a source law, derive matter coupling, derive
Einstein equations, promote a benchmark, issue a Gate Chair verdict, establish
a program-wide no-go theorem, or claim completed derivation.

## Registry Contract

`registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv` must use this exact header:

```csv
obligation_id,task_id,artifact_path,theorem_family,countermodel_slot,status,result_artifact,obstruction_id,scope,global_no_go_claimed,created_at,notes
```

Each row records one obligation slot for one tracked artifact. A row may point
to a countermodel, an obstruction, a source-purity audit, a primitive-boundary
witness, a waiver, or a pending obligation. The row is control evidence only.

## Field Schema

```yaml
CountermodelObligationRecord_v1:
  obligation_id:
    type: string
    required: true
    description: stable identifier for this countermodel obligation row
  task_id:
    type: string
    required: true
    description: research-control task that created the indexed result
  artifact_path:
    type: path
    required: true
    description: canonical tracked artifact that created or motivated the obligation row
  theorem_family:
    type: string
    required: true
    enum:
      - eqsrc
      - matter_coupling
      - detector_readout
      - toy_model
      - other
  countermodel_slot:
    type: string
    required: true
    description: policy slot name such as missing_inverse_countermodel
  status:
    type: string
    required: true
    enum:
      - filled
      - pending
      - waived_by_ddr
      - not_applicable_by_ddr
      - deferred_by_ddr
  result_artifact:
    type: path
    required: true
    description: artifact or receipt where the slot result is recorded
  obstruction_id:
    type: string
    required: false
    description: local obstruction identifier when the slot is obstruction-backed
  scope:
    type: string
    required: true
    description: local scope of the slot result or obligation
  global_no_go_claimed:
    type: boolean
    required: true
    must_equal_for_seed_rows: false
    description: true only if separately authorized by a tracked broad no-go result
  created_at:
    type: datetime
    required: true
  notes:
    type: string
    required: true
```

## Status Semantics

`filled` means the row points to an artifact containing a countermodel,
obstruction, audit result, primitive-boundary witness, or other slot result.
It does not mean that the relevant theorem family is proven or refuted.

`pending` means the obligation is live and must be resolved by a later packet.
It is valid only when the next route names the resolver or explains why the
obligation is intentionally left open.

`waived_by_ddr`, `not_applicable_by_ddr`, and `deferred_by_ddr` require an
explicit Director Decision Record. A waiver row must name the DDR in `notes`
and use the DDR path as `result_artifact` when no separate result artifact
exists.

## Seed-Row Rules

P4-T02 seed rows are limited to already tracked P3 outputs. They may index the
P3-T02 missing-inverse countermodel, the P3-T03 RetainH and GenH
primitive-boundary omission slots, the P3-T04 source-purity audit slot, and the
P3-T05 finite/local countermodel and scoped-obstruction records.

Seed rows must satisfy:

- `status` is `filled`;
- `global_no_go_claimed` is `false`;
- `result_artifact` exists in the repository;
- any nonblank `obstruction_id` is local to the source artifact;
- `notes` blocks overread into adoption, promotion, completed derivation, or a
  program-wide no-go conclusion.

## Forbidden Overreads

The registry must not be used as independent theorem authority. In particular:

- a filled obligation is not general EqSrc discharge;
- a local countermodel is not a program-wide no-go conclusion;
- a scoped obstruction is not future source-extension impossibility;
- a primitive-boundary row is not RetainH or GenH adoption;
- a source-purity audit row is not proof that all future target imports are
  impossible;
- a registry row is not a Distance-to-GR ledger delta;
- validation of this registry is not physics proof authority.

## Validator Requirements

P4-T03 must add advisory validation for this schema and registry. The initial
validator should warn for missing historical slots but hard-fail changed rows
that claim adoption, promotion, completed derivation, future source-extension
impossibility, or program-wide no-go conclusions without protected authority.

```yaml
minimal_countermodel_obligation_schema_v1:
  registry_path: registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv
  required_columns:
    - obligation_id
    - task_id
    - artifact_path
    - theorem_family
    - countermodel_slot
    - status
    - result_artifact
    - obstruction_id
    - scope
    - global_no_go_claimed
    - created_at
    - notes
  initial_status: seeded_from_p3_outputs
  next_validator_packet: P4-T03
  proof_authority: false
  physics_promotion_authorized: false
```

## References

The AEther-Flow Research Project. (2026a). *Minimal countermodel obligation
policy v1* [Project-control Markdown source].
`research_control/design/minimal_countermodel_obligation_policy_v1.md`.

The AEther-Flow Research Project. (2026b). *V18 recommendation implementation
plan continue task* [Project-control Markdown source].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.
