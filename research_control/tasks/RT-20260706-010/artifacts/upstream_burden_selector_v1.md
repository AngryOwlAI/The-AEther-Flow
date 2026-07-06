<!-- authority: science_draft -->

# Upstream-Burden Selector v1

## Control Status

```yaml
artifact_id: "upstream_burden_selector_v1"
artifact_type: "theoretical_decision_output"
task_id: "RT-20260706-010"
job_id: "AJ-RT-20260706-010-001"
role_id: "theoretical-continuation-selector"
created_at: "2026-07-06T08:39:37Z"
plan_task_id: "P6-T01"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select whether to attack EqSrc, RetainH, GenH, or continue matter-coupling candidate repair."
```

This artifact implements v17 P6-T01. It selects the next upstream-equivalence
route after the first candidate cycle. It uses the required inputs from P2,
P4, P5, and the current `EqSrc`, `RetainH`, and `GenH` Distance-to-GR ledger
rows.

The selector result is route classification only. It is not an `EqSrc`
theorem, not an `EqSrc` discharge, not `RetainH` adoption, not `GenH` adoption,
not source-law adoption, not matter-coupling repair, not a matter-coupling
derivation, not stress-energy semantics, not a matter action, not Einstein
equations, not benchmark promotion, not a Gate Chair verdict, and not a
completed derivation.

## Inputs

| Input | Status | Evidence |
| --- | --- | --- |
| P2 candidate cycle | `audited_stress_survived_draft_control_candidate_pending_exact_scoped_gate_question`; no repair required; no freeze required | `research_control/tasks/RT-20260705-053/artifacts/v17_coupling_law_candidate_cycle_report.md` |
| P4 detector route | selected `metric_use_ledger_integration_packet`; detector replacement candidate survived only as source-side candidate data | `research_control/tasks/RT-20260706-005/artifacts/detector_replacement_route_selector_v1.md` |
| P5 metric-use ledger | 19 ledger rows; all high-risk metric-adjacent uses audited with forbidden interpretations | `registries/METRIC_USE_LEDGER.csv` |
| `EqSrc` ledger status | draft object exists; general equivalence theorem missing | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `RetainH` ledger status | blocked by missing primitive; no canonical retention proof | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `GenH` ledger status | blocked by missing primitive; no canonical generator proof | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| Upstream trigger integration | future selectors must record `EqSrc`, `RetainH`, and `GenH` trigger status without treating trigger status as proof or adoption | `research_control/tasks/RT-20260705-018/artifacts/upstream_trigger_selector_integration_v16.md` |
| Current handoff | routes to P6-T01 upstream-burden selector | `research_control/handoffs/handoff-0641.yaml` |
| v17 plan | requires exactly one selected upstream route | `implementations_plans/recommendations_implementation_plan_continue_task-v17.md` |

## Upstream Primitive Trigger Status

```yaml
upstream_primitive_trigger_status:
  EqSrc:
    triggered: true
    trigger_kind: "selected_route_target"
    trigger_basis: "The active v17 P6-T01 task explicitly asks whether to attack EqSrc, and the Distance-to-GR ledger row for source_equivalence_eqsrc reports draft object exists with general_equivalence_theorem_missing."
    selected_for_next_packet: true
    authority_limit: "Trigger status means only that the next bounded packet should attempt EqSrc theorem work; it does not discharge EqSrc."
  RetainH:
    triggered: false
    trigger_kind: "not_selected"
    trigger_basis: "No current selected theorem attempt has yet shown that H-indexed retention or preservation must be primitive rather than a premise, lemma, or later dependency."
    selected_for_next_packet: false
    authority_limit: "Non-trigger status is not a no-go theorem and does not prove RetainH unnecessary."
  GenH:
    triggered: false
    trigger_kind: "not_selected"
    trigger_basis: "No current selected theorem attempt has yet required generated-family construction, enumeration, closure, or generator adoption before EqSrc theorem setup."
    selected_for_next_packet: false
    authority_limit: "Non-trigger status is not a no-go theorem and does not prove GenH unnecessary."
```

The trigger block records the selected route target and the two deferred
primitive routes. The P6-T02 attempt must refine whether its proposed theorem
requires explicit certificate premises, record-independent source equivalence,
family-wide source equivalence, `RetainH`, or `GenH`.

## Route Selection

```yaml
upstream_burden_route_selection:
  selected_route: "EqSrc_theorem_attempt"
  selected_next_plan_task_id: "P6-T02"
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_next_plan_route_type: "selected_upstream_equivalence_attempt"
  selected_next_role_family: "ontology-formalizer@0.2.0 task overlay"
  selected_next_packet_requires_human_gate: false
  selected_next_artifact: "research_control/tasks/<task-id>/artifacts/selected_upstream_equivalence_attempt_v1.tex"
```

The selected route is `EqSrc_theorem_attempt`. The reason is that `EqSrc` is
already represented as a draft object with a named missing theorem burden.
Attacking that theorem burden is narrower than introducing new `RetainH` or
`GenH` primitives, and it is more directly relevant than returning to
matter-coupling repair when no current repair or freeze trigger exists.

## Alternative Routes

| Route option | Disposition | Reason |
| --- | --- | --- |
| `EqSrc_theorem_attempt` | selected | Existing draft-object burden; ledger reports `general_equivalence_theorem_missing`; can be attempted without adopting new primitives. |
| `RetainH_primitive_attempt` | deferred | `RetainH` is blocked by missing primitive, but no current theorem setup has isolated H-indexed retention as the immediate primitive needed before EqSrc. |
| `GenH_primitive_attempt` | deferred | `GenH` is blocked by missing primitive, but no current theorem setup has isolated generated-family construction or closure as the immediate primitive needed before EqSrc. |
| `matter_coupling_candidate_repair` | not selected | P2 and P4 do not require repair, and P5 ledger guards the relevant metric-adjacent overreads. |
| `finite_local_model_zoo_expansion` | deferred | Finite examples may become useful after P6-T02 states the exact EqSrc theorem premises or obstruction. |
| `scoped_obstruction_freeze_review` | not selected | No P2, P4, or P5 source reports a scoped obstruction or freeze trigger for the current upstream route. |

## Theoretical Decision Output

```yaml
theoretical_decision_output:
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_route: "EqSrc_theorem_attempt"
  selected_next_plan_route_type: "selected_upstream_equivalence_attempt"
  decision_basis: "P2 and P4 produced guarded draft/control candidate evidence without a current repair or freeze requirement, P5 supplied metric-use guard coverage, and the Distance-to-GR ledger still lists EqSrc as an existing draft object whose general equivalence theorem is missing. The lowest-authority constructive continuation is therefore EqSrc theorem attempt before introducing RetainH or GenH primitives."
  theoretical_method: "Compare each v17 P6-T01 allowed route against the P2 candidate-cycle result, P4 detector route status, P5 metric-use ledger status, EqSrc RetainH GenH ledger rows, and upstream trigger-integration policy. Select the route that attacks an existing upstream theorem burden while preserving all adoption, benchmark, Gate Chair, and completed-derivation blocks."
  preserves_claim_blocks: true
  requires_human_gate: false
  human_gate_reason: "No protected Gate Chair verdict, canonical ontology edit, source-law adoption, benchmark claim, or physics promotion is selected."
  next_execution_role_family: "ontology-formalizer@0.2.0 task overlay"
  selected_next_packet_objective: "Execute P6-T02 by writing selected_upstream_equivalence_attempt_v1.tex as an EqSrc theorem-attempt packet with explicit premises, failure branches, and no downstream promotion."
  selected_next_packet_requires_human_gate: false
  decision_consequence: "P6-T01 completes without EqSrc discharge, RetainH adoption, GenH adoption, matter-coupling repair, freeze, benchmark promotion, or completed derivation; immediate continuation is P6-T02."
  new_payload_novelty: "Converts the completed P2/P4/P5 guarded candidate cycle into a dependency-ordered upstream theorem route: attempt EqSrc first, then let the theorem attempt expose whether RetainH or GenH primitives are truly immediate dependencies."
```

## Freeze Criteria

```yaml
freeze_criteria_status:
  repeated_burden: true
  freeze_evaluation_required: true
  scoped_obstruction_present: false
  repeated_unmet_burdens_no_new_payload: false
  new_mathematical_payload_present: true
  freeze_decision: "not_frozen"
  active_freeze_label: "V17-P6-T01-UPSTREAM-BURDEN-SELECTOR"
  freeze_if:
    - "A later packet repeats upstream selection without executing an EqSrc theorem attempt, primitive attempt, finite witness, scoped obstruction, or distinct dependency-map update."
    - "A later packet treats EqSrc route selection as EqSrc discharge."
    - "A later packet introduces RetainH or GenH adoption without a bounded theorem or primitive packet and audit."
  do_not_freeze_if:
    - "The next packet executes P6-T02 as an EqSrc theorem attempt and records its exact premises and failure branches."
    - "The P6-T02 theorem attempt reveals a precise RetainH or GenH dependency and routes that dependency as a separate bounded packet."
```

The route is not frozen. A constructive non-promotional `EqSrc` theorem-attempt
packet remains available.

## Distance-To-GR Status

```yaml
distance_to_gr_delta:
  changed: false
  effect: "no_distance_delta"
  burden_id: "source_equivalence_eqsrc"
  milestone: "source_equivalence_eqsrc"
  ledger_row_updated: false
  downstream_unlocked:
    - "bounded_v17_p6_t02_eqsrc_theorem_attempt"
  downstream_still_blocked:
    - "EqSrc discharge"
    - "RetainH adoption"
    - "GenH adoption"
    - "canonical ontology edit"
    - "source-law adoption"
    - "MetricData(E) adoption"
    - "g_eff scope expansion"
    - "physical metric authority"
    - "matter-coupling derivation or adoption"
    - "stress-energy semantics"
    - "stress-energy tensor"
    - "matter action"
    - "Einstein equations"
    - "benchmark promotion"
    - "Gate Chair verdict"
    - "completed derivation"
```

| Burden | Status after this selector |
| --- | --- |
| Source ontology primitives | unchanged; no canonical ontology edit |
| Source equivalence EqSrc | selected for P6-T02 theorem attempt; not discharged |
| RetainH | unchanged; missing primitive deferred |
| GenH | unchanged; missing primitive deferred |
| ObsLoc_lc | unchanged |
| Resp_lc | unchanged |
| M_src | unchanged; scoped source-only object remains bounded |
| g_eff | unchanged; metric-use ledger guards remain active; no scope expansion |
| matter coupling | no repair selected; scoped evidence/precondition status unchanged |
| Einstein equations | blocked; no field-equation derivation |
| finite-variation robustness | unchanged |
| benchmark promotion | blocked; no benchmark evidence or promotion |
| Gate Chair status | unchanged; no verdict issued |
| current route freeze or hard-fail status | not frozen |

## New Mathematical Payload

```yaml
new_mathematical_payload:
  - payload_id: "P6T01-PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "EqSrc theorem attempt route"
    summary: "Selects EqSrc_theorem_attempt as the single v17 P6-T01 route after P2 candidate-cycle P4 detector-route and P5 metric-use ledger completion."
  - payload_id: "P6T01-PAYLOAD-002"
    payload_type: "dependency_map_update"
    object_name: "P2/P4/P5 guarded candidate cycle to EqSrc theorem attempt"
    summary: "Maps the guarded matter-coupling candidate cycle back to the existing EqSrc theorem burden before RetainH or GenH primitive introduction."
  - payload_id: "P6T01-PAYLOAD-003"
    payload_type: "packet_selection"
    object_name: "EqSrc RetainH GenH trigger status"
    summary: "Records EqSrc selected for the next theorem-attempt packet while RetainH and GenH remain deferred until a theorem setup requires them."
```

## Forbidden Conclusions

This selector does not authorize:

- canonical ontology edit
- EqSrc discharge
- RetainH adoption
- GenH adoption
- source-law adoption
- MetricData(E) adoption
- g_eff scope expansion
- physical metric authority
- detector calibration
- matter-semantics adoption
- detector-semantics adoption
- coupling-law adoption
- matter-coupling derivation or adoption
- stress-energy semantics
- stress-energy tensor
- matter action
- Einstein equations
- benchmark promotion
- Gate Chair verdict
- completed derivation
- future source-extension impossibility
- program-wide no-go conclusion
- generated derivative, validator, registry, role, handoff, approval, cache,
  checkpoint, commit, or current-frontier rendering as proof authority

## Parent-Child Synthesis

```yaml
parent_child_synthesis:
  mode: "parent_child_parallel_synthesis"
  child_outputs:
    - "research_control/tasks/RT-20260706-010/artifacts/child_phys_math_upstream_burden_selector.yaml"
    - "research_control/tasks/RT-20260706-010/artifacts/child_phys_phil_upstream_burden_selector.yaml"
  conflict_review: "research_control/tasks/RT-20260706-010/artifacts/parent_conflict_review_upstream_burden_selector.yaml"
  fusion_notes: "research_control/tasks/RT-20260706-010/artifacts/parent_fusion_notes_upstream_burden_selector.md"
  unresolved_conflicts: []
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *V17 coupling-law candidate cycle
report* [Internal research-control artifact].

The AEther-Flow Research Project. (2026c). *Detector-replacement route selector
v1* [Internal research-control artifact].

The AEther-Flow Research Project. (2026d). *Metric-use ledger* [Internal
research-control registry].

The AEther-Flow Research Project. (2026e). *Distance-to-GR ledger* [Internal
research-control registry].

The AEther-Flow Research Project. (2026f). *Upstream trigger selector
integration v16* [Internal research-control artifact].
