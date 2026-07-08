<!-- authority: science_draft -->

# Support Formalization Target Selector V18

## Control Status

```yaml
artifact_id: "support_formalization_target_selector_v18_receipt"
artifact_type: "theoretical_decision_output"
task_id: "RT-20260708-019"
job_id: "AJ-RT-20260708-019-001"
role_id: "theoretical-continuation-selector"
created_at: "2026-07-08T11:20:48Z"
plan_task_id: "P7-T01"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select the first support-only formalization target from the v18 recommendation set."
support_only: true
proof_authority: false
```

This artifact implements v18 P7-T01. It selects exactly one support-only
formalization target and sequences the remaining targets. It does not implement
the checker. It is not proof authority, source-law adoption, general `EqSrc`
proof, metric construction, matter-coupling derivation, Einstein-equation
derivation, benchmark promotion, Gate Chair verdict, or completed derivation.

## Inputs

| Input | Status | Evidence |
| --- | --- | --- |
| Current frontier | routes to P7-T01 | `research_control/current_frontier.md` |
| Latest handoff | P7-T01 selector required | `research_control/handoffs/handoff-0711.yaml` |
| v18 plan | five allowed support formalization targets and done criteria | `implementations_plans/recommendations_implementation_plan_continue_task-v18.md` |
| v18 backlog | P7-T01 route type and next route P7-T02 | `research_control/design/v18_recommendation_backlog.yaml` |
| GR burden map | source-equivalence milestone and no-promotion constraints | `research_control/design/gr_derivation_burden_map.md` |
| Prior support selector precedent | support-only selector structure | `research_control/tasks/RT-20260706-017/artifacts/support_only_formalization_target_selector.md` |

## Candidate Target Evaluation

| Candidate target | Disposition | Reason |
| --- | --- | --- |
| `typed_EqSrc_orbit_checker` | selected | It is the explicit P7-T02 target, directly tied to `source_equivalence_eqsrc`, finite-record scope, and the prerequisite record shape needed by later closure and mutation tooling. |
| `closure_countermodel_generator` | sequenced later | It should use the finite typed orbit-closure record contract selected here, so it follows at P7-T03. |
| `no_target_import_mutation_tester` | sequenced later | It is valuable overread pressure, but it depends on stable support-tool surfaces and follows at P7-T04. |
| `metric_use_ledger_tex_validator` | sequenced later | It guards high-risk TeX references and follows at P7-T05 after lower-level support formalization tooling. |
| `detector_placeholder_collapse_checker` | sequenced later | It protects detector/readout placeholder language and follows at P7-T06 after earlier support-checker scaffolding exists. |

## Selected Target

```yaml
selected_formalization_target:
  target_id: "typed_EqSrc_orbit_checker"
  selected: true
  selected_next_plan_task_id: "P7-T02"
  planned_outputs:
    - "scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py"
    - "tests/test_typed_eqsrc_orbit_checker.py"
    - "research_control/tasks/<task-id>/artifacts/typed_eqsrc_orbit_checker_spec_v1.md"
  support_only: true
  proof_authority: false
  physics_promotion_authorized: false
```

The selected fragment should check finite typed EqSrc orbit-closure records
for declared objects, explicit identity maps, explicit inverse maps, explicit
composition table entries, source-only invariant preservation flags, and
fail-closed missing-data status.

## Remaining Target Sequence

```yaml
remaining_target_sequence:
  - plan_task_id: "P7-T03"
    target_id: "closure_countermodel_generator"
  - plan_task_id: "P7-T04"
    target_id: "no_target_import_mutation_tester"
  - plan_task_id: "P7-T05"
    target_id: "metric_use_ledger_tex_validator"
  - plan_task_id: "P7-T06"
    target_id: "detector_placeholder_collapse_checker"
```

## P7-T02 Handoff

Recommended next role:

```text
formalization-engineer@0.1.0 as a one-job provisional role if no registered
formalization-engineer role exists
```

Recommended next task:

```text
typed_eqsrc_orbit_checker_support_only
```

Minimum P7-T02 outputs:

- `scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py`
- `tests/test_typed_eqsrc_orbit_checker.py`
- `research_control/tasks/<task-id>/artifacts/typed_eqsrc_orbit_checker_spec_v1.md`

## Theoretical Decision Output

```yaml
theoretical_decision_output:
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_formalization_target: "typed_EqSrc_orbit_checker"
  selected_toolchain: "custom finite checker implemented in Python"
  selected_next_plan_task_id: "P7-T02"
  selected_next_packet_requires_human_gate: false
  decision_basis: "P7-T01 must select exactly one target and route to P7-T02. The typed EqSrc orbit checker is the explicit P7-T02 target, is finite-record scoped, and supplies the record contract needed before later closure countermodel and mutation-test tooling."
  theoretical_method: "Compare each allowed target against plan order, source-equivalence relevance, finite-checker feasibility, dependency ordering, and proof-authority overread risk."
  preserves_claim_blocks: true
  requires_human_gate: false
  human_gate_reason: "No protected ontology edit, Gate Chair verdict, benchmark claim, source-law adoption, proof authority, or physics promotion is selected."
  next_execution_role_family: "formalization-engineer@0.1.0 one-job provisional role if not registered"
  decision_consequence: "P7-T02 may implement only typed_EqSrc_orbit_checker and must publish support_only true proof_authority false physics_promotion_authorized false."
  new_payload_novelty: "Selects a concrete finite EqSrc orbit-closure checker target and sequences the remaining v18 support formalization targets."
```

## Distance-To-GR Status

```yaml
distance_to_gr_delta:
  changed: false
  effect: "no_distance_delta"
  burden_id: "source_equivalence_eqsrc"
  milestone: "source_equivalence_eqsrc"
  ledger_row_updated: false
```

| Burden | Status after this selector |
| --- | --- |
| Source ontology primitives | unchanged; no canonical ontology edit |
| Source equivalence EqSrc | support-only checker target selected; no EqSrc theorem adoption |
| RetainH | unchanged; not adopted |
| GenH | unchanged; not adopted |
| ObsLoc_lc | unchanged |
| Resp_lc | unchanged |
| M_src | unchanged |
| g_eff | unchanged; not constructed |
| matter coupling | unchanged; not derived or adopted |
| Einstein equations | blocked; no field-equation derivation |
| finite-variation robustness | unchanged |
| benchmark promotion | blocked |
| Gate Chair status | unchanged; no verdict issued |
| current route freeze or hard-fail status | not frozen; P7-T02 support-only implementation route selected |

## New Mathematical Payload

```yaml
new_mathematical_payload:
  - payload_id: "P7T01-PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "typed_EqSrc_orbit_checker"
    summary: "Selects the typed EqSrc orbit checker as the single P7-T02 implementation target."
  - payload_id: "P7T01-PAYLOAD-002"
    payload_type: "dependency_map_update"
    object_name: "v18 support formalization target sequence"
    summary: "Sequences closure countermodel generator, no-target import mutation tester, metric-use ledger TeX validator, and detector-placeholder collapse checker after the typed EqSrc checker."
```

## Forbidden Conclusions

This selector does not authorize:

- canonical ontology edit
- source-law adoption
- unrestricted `EqSrc` theorem authority
- target metric import
- physical metric construction
- `g_eff` construction or adoption
- matter-coupling derivation or adoption
- stress-energy semantics
- stress-energy tensor
- matter action
- Einstein equations
- benchmark promotion
- Gate Chair verdict
- proof authority
- validator-as-proof authority
- completed derivation

## Parent-Child Synthesis

```yaml
parent_child_synthesis:
  mode: "parent_child_parallel_synthesis"
  child_outputs:
    - "research_control/tasks/RT-20260708-019/artifacts/child_phys_math_support_formalization_target_selector_v18.yaml"
    - "research_control/tasks/RT-20260708-019/artifacts/child_phys_phil_support_formalization_target_selector_v18.yaml"
  conflict_review: "research_control/tasks/RT-20260708-019/artifacts/parent_conflict_review_support_formalization_target_selector_v18.yaml"
  fusion_notes: "research_control/tasks/RT-20260708-019/artifacts/parent_fusion_notes_support_formalization_target_selector_v18.md"
  unresolved_conflicts: []
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *V18 recommendation backlog*
[Research-control design record].

The AEther-Flow Research Project. (2026c). *GR derivation burden map*
[Research-control design note].

The AEther-Flow Research Project. (2026d). *Support-only formalization target
selector* [Research-control task artifact].
