<!-- authority: control -->

# Parent Fusion Notes: Finite Toy Response v2 Model Zoo Integration

## Status

This artifact implements the parent synthesis for v18 P6-T04,
`finite_toy_response_v2_model_zoo_integration`, under
`RT-20260708-017`.

## Inputs

- P6-T01 source specification:
  `research_control/tasks/RT-20260708-014/artifacts/finite_toy_response_v2_source_spec.tex`
- P6-T02 model-or-obstruction artifact:
  `research_control/tasks/RT-20260708-015/artifacts/finite_toy_response_v2_model_or_obstruction.tex`
- P6-T03 Refuter stress artifact:
  `research_control/tasks/RT-20260708-016/artifacts/finite_toy_response_v2_refuter_stress.tex`
- v1 source-model zoo schema and zoo:
  `research_control/design/source_model_zoo_schema_v1.md` and
  `research_control/design/source_model_zoo_v1.md`

## Fusion Decision

The finite toy response v2 model is integrated as source-model zoo entry
`FTMR-V2-PATH3` with model id `SMZ-FTRV2-PATH3-001`.

The integrated source data are:

```yaml
finite_source_set: "S_v2 = {a,b,c}"
source_relation_family: "A_v2 = {{a,b},{b,c}}"
incidence_record: "Inc_v2(x,e) iff x in e"
induced_response_relation: "R_v2({x,y}) = d_A(x,y)"
metric_response_analogue: "D_v2 graph-distance form only not g_eff"
model_result: "positive_toy_model_constructed"
stress_result: "survives_as_finite_toy_model"
freeze_status: "not_frozen"
```

The model is retrievable through:

- `research_control/design/source_model_zoo_schema_v18_extension.md`;
- `registries/SOURCE_MODEL_ZOO_REGISTRY.csv`;
- `research_control/tasks/RT-20260708-017/artifacts/finite_toy_response_v2_model_zoo_entry.yaml`.

## Authority Boundary

The source-model zoo entry is draft/control scaffolding only. It does not
adopt a source law, import target metric data, construct `g_eff`, derive
matter coupling, derive Einstein equations, promote a benchmark, issue a Gate
Chair verdict, or complete the derivation.

The registry row is a retrieval index. It is not a theorem premise, not
physics evidence by itself, and not authority over the P6-T02 or P6-T03
source artifacts.

## New Mathematical Payload

Definition. `FTMR-V2-PATH3` is the source-model zoo entry for the finite path
source object `P_v2 = (S_v2,A_v2,Inc_v2)` and response
`R_v2({x,y}) = d_A(x,y)`.

Proposition. `FTMR-V2-PATH3` is admissible as a draft/control
finite-toy-response source-model zoo entry because its model fields are
source-local and its forbidden-overread fields block target and downstream
substitutions.

Proof sketch. P6-T02 provides the finite source path and source graph-distance
response. P6-T03 provides tag-removal and source-relabeling survival plus
blocked-overread status for target distance, physical metric, empirical
readout, `g_eff`, and matter coupling. P6-T04 records these facts in the zoo
without treating the registry, generated derivatives, validation state, role
identity, handoff state, approval state, or commit state as source model data.

## Distance-to-GR Status

No Distance-to-GR ledger row is updated. The entry improves retrieval of the
finite toy response v2 route but does not discharge `g_eff`, matter coupling,
stress-energy semantics, matter action, Einstein equations, benchmark
promotion, Gate Chair status, or completed derivation.

## Next Route

The next route is P6-T05:
`finite_toy_response_v2_selector`.
