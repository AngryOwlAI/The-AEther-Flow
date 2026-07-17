<!-- authority: control -->

# Source-Equivalence Typed-Object Schema v1

## Metadata

```yaml
schema_id: source_equivalence_typed_object_schema_v1
schema_for:
  - TypedSourceEquivalenceObject_v1
  - registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv
authority_status: project_control
source_plan: implementations_plans/recommendations_implementation_plan_continue_task-v18.md
source_problem_statement: research_control/tasks/RT-20260707-013/artifacts/source_equivalence_typed_object_problem_statement_v1.md
created_at: 2026-07-07T10:52:51Z
physics_promotion_authorized: false
proof_authority: false
schema_update_no_physics_delta: true
population_deferred_to: P2-T03
next_route: P2-T03
```

## Purpose

This control schema gives a machine-readable shape for typed
source-equivalence objects before any source-equivalence row is populated. It
translates the P2-T01 problem-statement slots into a schema and an empty
registry contract only.

This schema is not a theorem, source law, canonical ontology edit, general
EqSrc discharge, RetainH adoption, GenH adoption, benchmark promotion, or
completed-derivation claim.

## Schema Model

The schema model is `source_equivalence_typed_object_v1`.

```yaml
source_equivalence_typed_object_v1:
  object_id:
    type: string
    required: true
    description: stable identifier for one typed source-equivalence object
  task_id:
    type: string
    required: true
    description: research-control task that created or updated the row
  artifact_path:
    type: path
    required: true
    description: canonical control artifact backing the object record
  source_family:
    source_family_symbol:
      type: string
      required: true
    source_domain_description:
      type: string
      required: true
    domain_status:
      enum:
        - declared
        - missing
        - partial
        - countermodel
      required: true
    finite_or_family_scope:
      enum:
        - finite
        - locally_finite
        - family_level
        - unspecified
      required: true
  objects:
    status:
      enum:
        - explicit
        - implicit
        - missing
      required: true
    object_set_statement:
      type: string
      required: true
    object_domain_reference:
      type: string
      required: false
  morphisms:
    status:
      enum:
        - explicit
        - generated
        - missing
        - countermodel
      required: true
    morphism_family_statement:
      type: string
      required: true
    witness_path:
      type: path
      required: false
  invariant_ledger:
    status:
      enum:
        - explicit
        - partial
        - missing
      required: true
    family_validity:
      enum:
        - proven
        - assumed
        - refuted
        - unknown
      required: true
    invariants:
      type: list
      required: true
    annotation_ledger:
      type: list
      required: false
    influence_ledger:
      type: list
      required: false
  comparison_rule:
    status:
      enum:
        - explicit
        - partial
        - missing
      required: true
    rule_statement:
      type: string
      required: true
    target_imports_forbidden:
      type: boolean
      required: true
      must_equal: false
  closure:
    identity:
      enum:
        - supplied
        - derived
        - missing
        - countermodel
      required: true
    inverse:
      enum:
        - supplied
        - derived
        - missing
        - countermodel
      required: true
    composition:
      enum:
        - supplied
        - derived
        - missing
        - countermodel
      required: true
    closure_witness_path:
      type: path
      required: false
  retainh:
    status:
      enum:
        - not_required
        - required
        - candidate
        - missing
        - adopted_by_gate
      required: true
    trigger_statement:
      type: string
      required: true
    gate_protected_adoption:
      type: boolean
      required: true
      must_equal: true
  genh:
    status:
      enum:
        - not_required
        - required
        - candidate
        - missing
        - adopted_by_gate
      required: true
    trigger_statement:
      type: string
      required: true
    gate_protected_adoption:
      type: boolean
      required: true
      must_equal: true
  no_target_guard:
    target_metric_imported:
      type: boolean
      required: true
      must_equal: false
    target_atlas_imported:
      type: boolean
      required: true
      must_equal: false
    stress_energy_semantics_imported:
      type: boolean
      required: true
      must_equal: false
    matter_action_imported:
      type: boolean
      required: true
      must_equal: false
  proof_state:
    enum:
      - draft_control
      - candidate
      - obstructed
      - refuted
      - gate_blocked
    required: true
  blocked_overread:
    type: list
    required: true
```

## Field Semantics

`source_family` records the source-side family under inspection and whether it
is declared, partial, missing, or already countermodeled.

`objects` records the object set. A future row must not treat an implicit or
missing object set as a completed equivalence object.

`morphisms` records the morphism family or its obstruction. A generated
morphism family must still cite a source-side witness path.

`invariant_ledger` records invariant, annotation, and influence ledgers. The
`family_validity` field separates proven, assumed, refuted, and unknown
statuses.

`comparison_rule` records the source-side comparison rule. The
`target_imports_forbidden` field must remain `false` for target imports: a row
with target imports is invalid for this source-equivalence registry.

`closure` records identity, inverse, and composition evidence. Missing or
countermodel status is valid control data; it is not a failure of the registry.

`retainh` and `genh` record RetainH and GenH trigger status. The
`adopted_by_gate` value is gate-protected and cannot be written by P2-T02 or
ordinary schema/registry maintenance. It requires a protected Gate Chair or
human-gated authority record that explicitly authorizes adoption.

`no_target_guard` records blocked target imports. Every boolean in this guard
must be `false` for a valid source-equivalence object row.

`proof_state` records only control status. It does not grant proof authority.

## Registry Contract

`registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv` must use this exact header:

```csv
object_id,artifact_path,task_id,source_family_symbol,object_set_status,morphism_status,invariant_ledger_status,comparison_rule_status,identity_closure_status,inverse_closure_status,composition_closure_status,retainh_status,genh_status,no_target_guard_status,proof_state,blocked_overread,created_at,notes
```

P2-T02 creates the registry with the header only. P2-T03 or a later authorized
packet may populate rows.

Future rows must map as follows:

| CSV column | Schema field |
| --- | --- |
| `object_id` | `object_id` |
| `artifact_path` | `artifact_path` |
| `task_id` | `task_id` |
| `source_family_symbol` | `source_family.source_family_symbol` |
| `object_set_status` | `objects.status` |
| `morphism_status` | `morphisms.status` |
| `invariant_ledger_status` | `invariant_ledger.status` |
| `comparison_rule_status` | `comparison_rule.status` |
| `identity_closure_status` | `closure.identity` |
| `inverse_closure_status` | `closure.inverse` |
| `composition_closure_status` | `closure.composition` |
| `retainh_status` | `retainh.status` |
| `genh_status` | `genh.status` |
| `no_target_guard_status` | source-side guard summary from `no_target_guard` booleans |
| `proof_state` | `proof_state` |
| `blocked_overread` | `blocked_overread` |
| `created_at` | row creation timestamp |
| `notes` | concise control note |

## Gate-Protection Rule

The following values and claims are gate-protected:

- `retainh.status: adopted_by_gate`
- `genh.status: adopted_by_gate`
- source-law adoption
- canonical ontology modification
- general EqSrc discharge
- benchmark promotion
- completed derivation

P2-T02 sets none of those protected statuses. A future registry row may only
use `adopted_by_gate` when a protected Gate Chair or human-gated authority
record explicitly names the adoption and the relevant source-side burden.

## Validation Expectations

The P2-T02 packet is valid only when:

- `research_control/design/source_equivalence_typed_object_schema_v1.md` exists.
- `registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv` exists.
- The registry has the exact header and zero data rows.
- The schema marks RetainH and GenH adoption fields as gate-protected.
- The schema blocks target metric, target atlas, stress-energy semantics, and
  matter action imports.
- The schema records no physics delta and no proof authority.
- The next route remains `P2-T03`.

## APA 7 Sources

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan
continue task v18* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Source-equivalence typed-object
problem statement v1* [Internal control artifact].

The AEther-Flow Research Project. (2026c). *Handoff 0682* [Internal
research-control handoff].
