<!-- authority: control -->

# Source Model Zoo Schema v18 Extension

## Status

This document implements v18 P6-T04. It extends
`research_control/design/source_model_zoo_schema_v1.md` for source-model zoo
entries that carry finite toy metric-response packets.

The positive scoped status is: additive draft/control retrieval support for
finite toy response source-model zoo entries. The extension is not a canonical
ontology edit, not a source law, not a target metric, not a physical metric,
not `g_eff`, not matter coupling, not stress-energy semantics, not matter
action, not Einstein equations, not benchmark promotion, not a Gate Chair
verdict, and not a completed derivation.

## Extension Rule

The v1 source model zoo schema remains valid. This v18 extension adds an
optional finite-toy-response entry class for packets whose source object,
response relation, stress result, and boundary status have already been
produced by bounded research-control tasks.

The extension has three purposes:

1. make finite toy response v2 retrievable through a stable registry row;
2. keep P6-T02 construction and P6-T03 stress status attached to the entry;
3. prevent zoo retrieval from becoming proof authority or physics promotion.

## Added Model Kind

The extension adds one model kind:

```yaml
model_kind_extension:
  - finite_toy_metric_response_model
```

This kind is allowed only when the entry records a finite source set, source
relations, an induced response relation, a stress status, and explicit
forbidden overreads. It does not extend the source ontology and does not
promote a finite graph-distance form to `g_eff`.

## Required Entry Fields

Entries using `finite_toy_metric_response_model` must include the v1 fields
and the following v18 fields:

```yaml
zoo_entry_id:
plan_task_id:
source_model_zoo_schema_extension:
lineage_tasks:
model_result:
stress_result:
freeze_status:
finite_toy_response_fields:
  finite_source_set:
  source_relation_family:
  incidence_record:
  invariant_orbit_structure:
  induced_response_relation:
  metric_response_analogue:
retrieval_keys:
distance_to_gr_status:
claim_boundary:
```

## Source-Model Zoo Registry

The machine retrieval index is:

```text
registries/SOURCE_MODEL_ZOO_REGISTRY.csv
```

Required columns are:

```csv
zoo_entry_id,model_id,model_kind,entry_status,task_id,entry_path,schema_extension_path,lineage_tasks,model_result,stress_result,freeze_status,allowed_reuse,forbidden_overreads,target_import_status,detector_semantics_status,stress_energy_status,matter_action_status,benchmark_status,validation_status,created_at,updated_at,notes
```

The registry is a control index only. It may route agents to the entry artifact
and to source paths, but it cannot be used as a theorem premise, source-law
adoption receipt, metric authority, benchmark receipt, or Gate Chair verdict.

## Finite Toy Response v2 Entry Contract

For the v18 P6-T04 entry, the required finite-toy markers are:

```yaml
zoo_entry_id: "FTMR-V2-PATH3"
model_kind: "finite_toy_metric_response_model"
finite_source_set: "S_v2 = {a,b,c}"
source_relation_family: "A_v2 = {{a,b},{b,c}}"
incidence_record: "Inc_v2(x,e) iff x in e"
induced_response_relation: "R_v2({x,y}) = d_A(x,y)"
metric_response_analogue: "D_v2 graph-distance form only not g_eff"
model_result: "positive_toy_model_constructed"
stress_result: "survives_as_finite_toy_model"
freeze_status: "not_frozen"
target_import_status: "blocked"
physics_promotion_authorized: false
```

## Formal Payload

Definition. A v18 finite-toy response zoo entry is admissible when its
response relation is computed only from the declared finite source relation
and every downstream interpretation outside the source tuple is recorded under
`forbidden_overreads`.

Proposition. The P6-T04 finite toy response v2 entry is admissible under this
extension.

Proof sketch. P6-T02 constructs the source tuple
`(S_v2,A_v2,Inc_v2)` and response `R_v2({x,y}) = d_A(x,y)` from source graph
distance. P6-T03 records tag-removal and source-relabeling survival while
blocking target distance, physical metric, empirical readout, `g_eff`, and
matter-coupling substitutions. The entry therefore has source-local model
data, stress status, and explicit overread blocks. No target metric, detector
semantics, stress-energy data, matter action, benchmark behavior, generated
derivative, validator status, registry status, role identity, handoff state,
approval state, or commit state is used as model payload.

## Validation Contract

A v18 finite toy response entry fails validation if it:

- omits the stable `zoo_entry_id`;
- omits the P6-T02 model lineage or P6-T03 stress lineage;
- lacks a finite source set or source relation family;
- lacks `R_v2({x,y}) = d_A(x,y)` or equivalent source-local response syntax;
- records target distance, physical metric, empirical readout, `g_eff`,
  stress-energy, matter action, benchmark behavior, or registry state as
  source model data;
- treats zoo retrieval as source-law adoption, matter coupling, Einstein
  equations, benchmark promotion, Gate Chair status, or completed derivation.

## Distance-to-GR Status

The extension changes no Distance-to-GR ledger row. It makes one finite toy
response model retrievable as draft/control scaffolding. The following burdens
remain blocked or unchanged: `g_eff`, matter coupling, stress-energy
semantics, matter action, Einstein equations, benchmark promotion, Gate Chair
status, and completed derivation.

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v18.md` [Internal project-control plan].

The Aether-Flow Research Project. (2026). `research_control/design/source_model_zoo_schema_v1.md` [Internal project-control schema].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260708-015/artifacts/finite_toy_response_v2_model_or_obstruction.tex` [Internal research-control artifact].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260708-016/artifacts/finite_toy_response_v2_refuter_stress.tex` [Internal research-control artifact].
