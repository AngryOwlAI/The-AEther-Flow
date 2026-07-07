# EqSrc Family-Closure Packet Setup v1

## 1. Control Status

- task_id: `RT-20260707-019`
- decision_id: `DDR-20260707-019`
- agent_job_id: `AJ-RT-20260707-019-001`
- parent_task_id: `RT-20260707-018`
- parent_handoff_id: `handoff-0687`
- plan_task_id: `P3-T01`
- task_type: `eqsrc_family_closure_theorem_or_countermodel_setup`
- status: `draft/control`
- physics_progress_status: `theorem_countermodel_setup_no_promotion`
- target_derivation_milestone: `source_equivalence_eqsrc`
- milestone_burden: `Set up one bounded EqSrc family-closure theorem-or-countermodel packet after typed-object audit and stress.`
- adoption_requested: `false`

This artifact sets up the next bounded packet. It does not prove family-level `EqSrc`, refute family-level `EqSrc`, adopt a primitive, promote a benchmark, or change canonical ontology.

## 2. Setup Declaration

```yaml
eqsrc_family_closure_packet_setup:
  source_family_symbol: "F_src"
  typed_object_artifact: "research_control/tasks/RT-20260707-015/artifacts/source_equivalence_typed_object_v1.tex"
  theorem_or_countermodel_artifact: "eqsrc_family_closure_theorem_or_countermodel_v1.tex"
  selected_packet_target: "P3_T02_family_level_eqsrc_closure_theorem_or_minimal_countermodel_attempt"
  max_primary_payload_count: 1
  allowed_primary_payloads:
    - "family_level_eqsrc_closure_theorem_candidate"
    - "minimal_family_closure_countermodel"
    - "RetainH_primitive_required"
    - "GenH_primitive_required"
    - "scoped_freeze_obstruction"
  required_primary_payload_rule: "The P3-T02 packet must output exactly one primary payload from allowed_primary_payloads; if a theorem candidate cannot be made under source-side assumptions, it must provide a minimal countermodel or a primitive-required/scoped-obstruction result."
  countermodel_obligation_required: true
  no_target_import_guard_required: true
  adoption_requested: false
  next_route: "P3-T02"
```

## 3. One Packet Target

The selected downstream packet target is:

```text
P3_T02_family_level_eqsrc_closure_theorem_or_minimal_countermodel_attempt
```

No second target is authorized in this packet. The downstream attempt must decide whether the current typed source-family data support a theorem candidate, a minimal countermodel, a primitive-required result, or a scoped freeze obstruction.

## 4. Typed Source Family

`F_src` denotes the source-side family built from the v18 typed-object record. The P3-T02 packet must treat the following as source-side input rather than target-side import:

- typed object definitions from `source_equivalence_typed_object_v1.tex`
- typed-object smuggling constraints from the v18 audit chain
- typed-object refuter stress obligations
- invariant-ledger requirements surfaced by the P2 selector

The P3-T02 packet must restate the family domain before attempting identity, inverse, or composition closure.

## 5. Family Closure Obligations

The P3-T02 packet must test all of the following obligations:

- identity closure over `F_src`
- inverse closure over `F_src`
- composition closure over `F_src`
- family-invariant ledger stability
- source-only comparison rule
- no-target-import guard
- theorem scope or obstruction scope

If any obligation fails, the artifact must not claim family-level `EqSrc` discharge. It must instead select one allowed primary payload and state the exact obstruction.

## 6. Required Primary Branch

The P3-T02 packet must produce exactly one primary branch:

```yaml
primary_result_one_of:
  - family_level_eqsrc_closure_theorem_candidate
  - minimal_family_closure_countermodel
  - RetainH_primitive_required
  - GenH_primitive_required
  - scoped_freeze_obstruction
```

The `family_level_eqsrc_closure_theorem_candidate` branch remains a candidate only. It must route to audit and stress before any ledger or ontology update.

## 7. RetainH and GenH Analysis

The P3-T02 packet must classify each primitive separately.

```yaml
RetainH_status_one_of:
  - not_required_here
  - required_but_missing
  - candidate_definition_needed
  - countermodel_blocks_current_route
  - deferred
GenH_status_one_of:
  - not_required_here
  - required_but_missing
  - candidate_definition_needed
  - countermodel_blocks_current_route
  - deferred
```

`RetainH` and `GenH` are not adopted by this setup packet. If either primitive is needed, the P3-T02 packet must state why the current source data do not derive it and must keep `adoption_requested_false`.

## 8. Countermodel Obligation

Even if the P3-T02 packet attempts a theorem-candidate branch, it must include at least one explicit attempted countermodel slot from this list:

```yaml
countermodel_slots:
  - missing_inverse_countermodel
  - missing_composition_countermodel
  - invariant_ledger_not_family_stable_countermodel
  - target_import_needed_countermodel
  - RetainH_needed_countermodel
  - GenH_needed_countermodel
```

If the primary branch is a countermodel, it must state whether the witness is finite, locally finite, schematic, or scoped by an explicitly named family condition.

## 9. No-Target-Import Guard

The theorem candidate, if attempted, must not use any of the following as premises:

- target metric
- target proper time
- target stress-energy tensor
- matter action
- Einstein equations
- benchmark status
- Gate Chair status
- generated validator status
- commit status
- external project reputation

These may be mentioned as forbidden conclusions or downstream obligations, but they cannot be used to prove family-level `EqSrc`.

## 10. Distance-to-GR Effect

```yaml
distance_to_gr_effect:
  changed: false
  effect: "no_distance_delta"
  reason: "P3-T01 defines the downstream packet target and obligations only. It supplies no theorem proof, countermodel witness, primitive adoption, coupling law, or Einstein-equation derivation."
```

## 11. Parent-Child Synthesis

The physicist-mathematician perspective requires a typed family, closure obligations, invariant ledger, and countermodel slots. The physicist-philosopher perspective requires the setup to distinguish ontology from mathematical model and empirical prediction. The parent decision fuses these into one downstream target with branch-limited outcomes and no promotion.

## 12. Forbidden Conclusions

This setup does not support:

- general `EqSrc` discharge
- source-law adoption
- `RetainH` adoption
- `GenH` adoption
- source detector/readout semantics adoption
- matter-coupling derivation
- stress-energy semantics
- Einstein-equation derivation
- benchmark promotion
- completed derivation
- global no-go claim
- future source-extension impossibility claim

## 13. Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan continue task v18* [Internal implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.

The AEther-Flow Research Project. (2026b). *Typed-object continuation selector v1* [Research-control artifact]. `research_control/tasks/RT-20260707-018/artifacts/typed_object_continuation_selector_v1.md`.

The AEther-Flow Research Project. (2026c). *Source-equivalence typed object v1* [Research-control TeX artifact]. `research_control/tasks/RT-20260707-015/artifacts/source_equivalence_typed_object_v1.tex`.

The AEther-Flow Research Project. (2026d). *V18 P2-T05 source-equivalence typed object Refuter stress v1* [Research-control TeX artifact]. `research_control/tasks/RT-20260707-017/artifacts/source_equivalence_typed_object_refuter_stress_v1.tex`.

