<!-- authority: science_draft -->

# Detector-Replacement Route Selector v1

## Control Status

```yaml
artifact_id: "detector_replacement_route_selector_v1"
artifact_type: "theoretical_decision_output"
task_id: "RT-20260706-005"
job_id: "AJ-RT-20260706-005-001"
role_id: "theoretical-continuation-selector"
created_at: "2026-07-06T06:21:02Z"
plan_task_id: "P4-T05"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one next route after detector replacement candidate or obstruction."
```

This artifact implements v17 P4-T05. It classifies exactly one object:
`SourceDetectorReplacementCandidate_EStar_v1`, the finite draft/control
source-side detector-replacement candidate constructed in `RT-20260706-002`,
audited in `RT-20260706-003`, and stress-tested in `RT-20260706-004`.

The selector result is route classification only. It is not detector
semantics, not detector-semantics adoption, not source-law adoption, not
matter semantics, not coupling-law adoption, not matter-coupling derivation,
not stress-energy semantics, not a matter action, not Einstein equations, not
benchmark promotion, not a Gate Chair verdict, and not a completed derivation.

## Inputs

| Input | Status | Evidence |
| --- | --- | --- |
| Candidate construction | finite source-side detector-replacement candidate | `research_control/tasks/RT-20260706-002/artifacts/detector_semantics_replacement_candidate_v1.tex` |
| Smuggling audit | `source_pure_as_written` | `research_control/tasks/RT-20260706-003/artifacts/detector_replacement_smuggling_audit_v1.tex` |
| Refuter stress | `survives_as_source_replacement_candidate` | `research_control/tasks/RT-20260706-004/artifacts/detector_replacement_refuter_stress_v1.tex` |
| Current handoff | routes to P4-T05 selector | `research_control/handoffs/handoff-0636.yaml` |
| v17 plan | requires exactly one selected detector route | `implementations_plans/recommendations_implementation_plan_continue_task-v17.md` |

## Route Selection

```yaml
detector_replacement_route_selection:
  candidate: "SourceDetectorReplacementCandidate_EStar_v1"
  candidate_status: "draft/control source-side detector-replacement candidate"
  construction_status: "constructed in RT-20260706-002"
  audit_status: "source_pure_as_written in RT-20260706-003"
  stress_status: "survives_as_source_replacement_candidate in RT-20260706-004"
  selected_route: "metric_use_ledger_integration_packet"
  selected_next_plan_task_id: "P5-T01"
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_next_plan_route_type: "project_control_schema_update"
  selected_next_role_family: "project-control-maintainer@0.2.0 task overlay"
  selected_next_packet_requires_human_gate: false
```

The selected route is `metric_use_ledger_integration_packet`. The reason is
not that the detector replacement failed. It is that the candidate survived
only as a source-side placeholder candidate, so the next useful control step is
to ledger every high-risk metric, detector, proper-time, readout, and process
use before any later `K_E` repair integration or source-model expansion.

## Alternative Routes

| Route option | Disposition | Reason |
| --- | --- | --- |
| `metric_use_ledger_integration_packet` | selected | The candidate survived audit and stress, and the next risk is silent overread of `g_eff`, source readout tokens, proper-time language, detector language, target-metric language, or process receipts near matter-coupling work. |
| `integrate_detector_replacement_into_K_E_candidate_repair` | deferred | Direct integration before the ledger would risk importing physical detector or metric semantics without a tracked use classification. |
| `detector_obstruction_freeze_review` | not selected | P4-T04 did not return `scoped_obstruction` or `freeze_route`; it returned `bridge_facing_candidate_path`. |
| `ontology_law_research_packet_for_missing_source_primitive` | not selected | P4-T04 did not isolate a derivation-critical missing source law; a conservative source-side continuation remains open. |
| `source_model_zoo_expansion` | deferred | Expansion is useful only after metric and detector use categories are ledgered so examples do not become untracked evidence. |

## Theoretical Decision Output

```yaml
theoretical_decision_output:
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_route: "metric_use_ledger_integration_packet"
  selected_next_plan_route_type: "project_control_schema_update"
  decision_basis: "SourceDetectorReplacementCandidate_EStar_v1 was constructed as finite draft/control source-side data, audited as source_pure_as_written, and stress-survived only as a source replacement candidate. Under the v17 P4-T05 allowed route set, the lowest-authority useful next route is metric-use ledger integration before any K_E repair integration or model-zoo expansion."
  theoretical_method: "Compare each v17 P4-T05 allowed route against the P4-T02 candidate, P4-T03 audit, P4-T04 stress, handoff-0636, active role registry, and GR burden map. Select the route that adds guard information while preserving all detector, metric, adoption, benchmark, and completed-derivation blocks."
  preserves_claim_blocks: true
  requires_human_gate: false
  human_gate_reason: "No protected Gate Chair verdict, ontology edit, benchmark claim, or physics promotion is selected."
  next_execution_role_family: "project-control-maintainer@0.2.0 task overlay"
  selected_next_packet_objective: "Create the P5-T01 metric-use ledger schema and initial registry surface for every g_eff and metric-adjacent reference in matter-coupling tasks."
  selected_next_packet_requires_human_gate: false
  decision_consequence: "P4 completes without detector-semantics adoption and routes immediate continuation to P5-T01. Later K_E repair integration remains deferred until metric-use categories are explicitly tracked."
  new_payload_novelty: "Converts detector-replacement audit-and-stress survival into a single guarded continuation route: metric-use ledger integration before any further use of the detector placeholder in K_E-adjacent work."
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
  active_freeze_label: "V17-DETECTOR-REPLACEMENT-ROUTE-SELECTOR"
  freeze_if:
    - "A later packet treats stress survival as detector-semantics adoption."
    - "A later packet uses g_eff, proper time, detector response, target metric, or process receipts as matter-coupling premises without ledger classification."
    - "A later packet repeats detector candidate construction, audit, stress, or selector routing without P5 ledger work, repair integration, obstruction, or distinct route decision."
  do_not_freeze_if:
    - "The next packet completes P5-T01 metric-use ledger schema work without promotion."
    - "A later packet integrates detector replacement into K_E only after ledgered use categories and no-target guards are present."
```

The route is not frozen. A non-promotional project-control ledger route remains
available and is the selected immediate continuation.

## Distance-To-GR Status

```yaml
distance_to_gr_delta:
  changed: false
  effect: "no_distance_delta"
  burden_id: "matter_coupling"
  milestone: "matter_coupling"
  ledger_row_updated: false
  downstream_unlocked:
    - "bounded_v17_p5_t01_metric_use_ledger_schema"
    - "later_detector_replacement_integration_after_ledger"
  downstream_still_blocked:
    - "canonical ontology edit"
    - "source-law adoption"
    - "matter semantics adoption"
    - "detector semantics adoption"
    - "coupling-law adoption"
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
| Source equivalence EqSrc | unchanged |
| RetainH | unchanged |
| GenH | unchanged |
| ObsLoc_lc | unchanged |
| Resp_lc | unchanged |
| M_src | unchanged; scoped source-only context retained |
| g_eff | unchanged; selected for future metric-use ledger control, not physical metric adoption |
| matter coupling | selector chose metric-use ledger integration; no detector semantics, coupling law, or matter coupling is adopted or derived |
| Einstein equations | blocked; no field-equation derivation |
| finite-variation robustness | unchanged |
| benchmark promotion | blocked; no benchmark evidence or promotion |
| Gate Chair status | unchanged; no verdict issued |
| current route freeze or hard-fail status | not frozen |

## New Mathematical Payload

```yaml
new_mathematical_payload:
  - payload_id: "P4T05-PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "SourceDetectorReplacementCandidate_EStar_v1 metric-use ledger route"
    summary: "Selects metric_use_ledger_integration_packet as the single route after detector-replacement construction, audit, and stress."
  - payload_id: "P4T05-PAYLOAD-002"
    payload_type: "dependency_map_update"
    object_name: "detector replacement survival to P5 metric-use ledger"
    summary: "Maps the completed detector-replacement candidate cycle to P5-T01 ledger schema work before any K_E repair integration."
  - payload_id: "P4T05-PAYLOAD-003"
    payload_type: "source_extension_classification"
    object_name: "SourceDetectorReplacementCandidate_EStar_v1 post-stress route status"
    summary: "Classifies the candidate as draft/control source-side route evidence requiring metric-use guard tracking, not detector semantics or matter coupling."
```

## Forbidden Conclusions

This selector does not authorize:

- canonical ontology edit
- source-law adoption
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
    - "research_control/tasks/RT-20260706-005/artifacts/child_phys_math_detector_replacement_route_selector.yaml"
    - "research_control/tasks/RT-20260706-005/artifacts/child_phys_phil_detector_replacement_route_selector.yaml"
  conflict_review: "research_control/tasks/RT-20260706-005/artifacts/parent_conflict_review_detector_replacement_route_selector.yaml"
  fusion_notes: "research_control/tasks/RT-20260706-005/artifacts/parent_fusion_notes_detector_replacement_route_selector.md"
  unresolved_conflicts: []
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Source-side detector-replacement
candidate D_src(E_*) v1* [Research-control TeX artifact].

The AEther-Flow Research Project. (2026c). *Detector-replacement smuggling
audit v1* [Research-control TeX artifact].

The AEther-Flow Research Project. (2026d). *Detector-replacement Refuter stress
v1* [Research-control TeX artifact].

The AEther-Flow Research Project. (2026e). *Handoff 0636* [Internal
research-control handoff].
