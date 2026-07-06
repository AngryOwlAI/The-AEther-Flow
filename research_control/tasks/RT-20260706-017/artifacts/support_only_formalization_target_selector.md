<!-- authority: science_draft -->

# Support-Only Formalization Target Selector

## Control Status

```yaml
artifact_id: "support_only_formalization_target_selector_v1"
artifact_type: "theoretical_decision_output"
task_id: "RT-20260706-017"
job_id: "AJ-RT-20260706-017-001"
role_id: "theoretical-continuation-selector"
created_at: "2026-07-06T11:48:24Z"
plan_task_id: "P8-T01"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one low-level formal fragment for support-only mechanization."
```

This artifact implements v17 P8-T01. It selects exactly one support-only
formalization target and justifies a toolchain. It does not mechanize the
fragment. It is not proof authority, source-law adoption, matter-coupling
derivation, Einstein-equation derivation, benchmark promotion, Gate Chair
verdict, or completed derivation.

## Inputs

| Input | Status | Evidence |
| --- | --- | --- |
| Current frontier | routes to P8-T01 | `research_control/current_frontier.md` |
| Latest handoff | P8-T01 selector required | `research_control/handoffs/handoff-0648.yaml` |
| v17 plan | five candidate targets and done criteria | `implementations_plans/recommendations_implementation_plan_continue_task-v17.md` |
| Certificate algebra checklist | fail-closed source-certificate control surface | `research_control/design/source_certificate_algebra_checklist.md` |
| Certificate operation laws | draft/control theorem material with fail-closed behavior | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` |
| V16 formalization selector | prior support-only certificate evaluator precedent | `research_control/tasks/RT-20260705-008/artifacts/v16_formalization_scope_selector.md` |
| V16 executable support spec | Python support-only evaluator precedent | `research_control/tasks/RT-20260705-009/artifacts/v16_support_only_certificate_spec.md` |

## Candidate Target Evaluation

| Candidate target | Disposition | Reason |
| --- | --- | --- |
| `source_certificate_identity_composition_restriction` | not selected | Important, but narrower and closer to theorem-style proof obligations. The current safer prerequisite is an evaluator for allowed and fail-closed branches. |
| `fail_closed_certificate_evaluation` | selected | It is finite, local, deterministic, already grounded in registered certificate controls, and covers the widest set of positive and negative certificate branches without creating proof authority. |
| `finite_toy_tag_removal_obstruction` | not selected | Already has older support-only mechanization precedent and is less central to the current certificate-algebra route. |
| `no_target_import_guard_taxonomy` | not selected | Essential, but best treated as one branch in the fail-closed evaluator rather than the whole fragment. |
| `claim_graph_non_promotion_constraints` | not selected | Valuable project-control validation, but less directly tied to the low-level source-certificate formal fragment requested by P8. |

## Selected Target

```yaml
selected_formalization_target:
  target_id: "fail_closed_certificate_evaluation"
  selected: true
  source_artifact_path: "research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex"
  proof_normal_form_row_id: "PNF-RT-20260706-014-003"
  support_only: true
  proof_authority: false
  physics_promotion_authorized: false
```

The selected fragment should model a finite certificate record and return one
of two support-only classifications:

- `declared_equivalence_allowed` for a valid source-side certificate record
  with declared source fields and no forbidden imports;
- `declared_equivalence_blocked` with a fail-closed reason for missing,
  malformed, target-importing, detector-semantics, process-authority,
  stress-energy, matter-action, benchmark, or scoped-evidence branches.

## Selected Toolchain

```yaml
selected_toolchain:
  kind: "custom finite checker"
  implementation_language: "Python"
  planned_test_harness: "unittest"
  selected_for_p8_t02: true
```

This toolchain is selected because it:

- needs no new dependency;
- matches existing repository support-only formalization practice;
- can encode a finite record evaluator with deterministic results;
- can emit a JSON validation report for P8-T02;
- has low risk of being mistaken for external proof-assistant authority.

Lean, Coq, Agda, TLA+, and Alloy are not selected for P8-T02. They may be
useful later, but they add dependency and interpretation risk for a fragment
whose immediate value is finite fail-closed branch coverage.

## P8-T02 Handoff

Recommended next role:

```text
formalization-engineer@0.1.0 as a one-job provisional role if no registered
formalization-engineer role exists
```

Recommended next task:

```text
support_only_formalization_fragment for fail_closed_certificate_evaluation
```

Minimum P8-T02 outputs:

- `research_control/formalization/fail_closed_certificate_evaluation/README.md`
- `research_control/formalization/fail_closed_certificate_evaluation/fail_closed_certificate_evaluation.py`
- `research_control/formalization/fail_closed_certificate_evaluation/test_fail_closed_certificate_evaluation.py`
- `research_control/formalization/fail_closed_certificate_evaluation/validation_report.json`

## Theoretical Decision Output

```yaml
theoretical_decision_output:
  selected_next_packet_type: "bounded_theoretical_calculation"
  selected_formalization_target: "fail_closed_certificate_evaluation"
  selected_toolchain: "custom finite checker implemented in Python"
  selected_next_plan_task_id: "P8-T02"
  selected_next_packet_requires_human_gate: false
  decision_basis: "The fail-closed certificate evaluator is the narrowest useful formalization target that covers missing, malformed, target-import, detector-semantics, process-authority, stress-energy, matter-action, benchmark, and scoped-evidence branches while preserving source-side control status."
  theoretical_method: "Compare each candidate target against source grounding, finite-checker feasibility, traceability to proof-normal-form rows, dependency risk, and overread risk."
  preserves_claim_blocks: true
  requires_human_gate: false
  human_gate_reason: "No protected ontology edit, Gate Chair verdict, benchmark claim, source-law adoption, or physics promotion is selected."
  next_execution_role_family: "formalization-engineer@0.1.0 one-job provisional role if not registered"
  decision_consequence: "P8-T02 may mechanize only fail_closed_certificate_evaluation and must publish support_only true proof_authority false physics_promotion_authorized false."
  new_payload_novelty: "Selects a concrete finite checker target tied to PNF-RT-20260706-014-003 and prior certificate algebra surfaces."
```

## Distance-To-GR Status

```yaml
distance_to_gr_delta:
  changed: false
  effect: "no_distance_delta"
  burden_id: "matter_coupling"
  milestone: "matter_coupling"
  ledger_row_updated: false
```

| Burden | Status after this selector |
| --- | --- |
| Source ontology primitives | unchanged |
| Source equivalence EqSrc | unchanged |
| RetainH | unchanged |
| GenH | unchanged |
| ObsLoc_lc | unchanged |
| Resp_lc | unchanged |
| M_src | unchanged |
| g_eff | unchanged |
| matter coupling | support-only formalization target selected; not derived or adopted |
| Einstein equations | blocked |
| finite-variation robustness | unchanged |
| benchmark promotion | blocked |
| Gate Chair status | unchanged; no verdict issued |
| current route freeze or hard-fail status | not frozen |

## New Mathematical Payload

```yaml
new_mathematical_payload:
  - payload_id: "P8T01-PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "fail_closed_certificate_evaluation"
    summary: "Selects the finite fail-closed certificate evaluator as the single P8-T02 mechanization target."
  - payload_id: "P8T01-PAYLOAD-002"
    payload_type: "dependency_map_update"
    object_name: "certificate algebra to support-only finite checker"
    summary: "Maps source certificate operation laws and proof-normal-form row PNF-RT-20260706-014-003 to a support-only finite checker route."
```

## Forbidden Conclusions

This selector does not authorize:

- canonical ontology edit
- source-law adoption
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption
- unrestricted `RR_E` theorem authority
- `MetricData(E)` adoption
- `g_eff` scope expansion
- physical Lorentzian metric authority
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
- proof authority
- completed derivation

## Parent-Child Synthesis

```yaml
parent_child_synthesis:
  mode: "parent_child_parallel_synthesis"
  child_outputs:
    - "research_control/tasks/RT-20260706-017/artifacts/child_phys_math_support_only_formalization_target_selector.yaml"
    - "research_control/tasks/RT-20260706-017/artifacts/child_phys_phil_support_only_formalization_target_selector.yaml"
  conflict_review: "research_control/tasks/RT-20260706-017/artifacts/parent_conflict_review_support_only_formalization_target_selector.yaml"
  fusion_notes: "research_control/tasks/RT-20260706-017/artifacts/parent_fusion_notes_support_only_formalization_target_selector.md"
  unresolved_conflicts: []
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Source certificate algebra
checklist* [Research-control design note].

The AEther-Flow Research Project. (2026c). *Source certificate operation laws
v1* [Research-control TeX artifact].

The AEther-Flow Research Project. (2026d). *V16 formalization scope selector*
[Research-control task artifact].

The AEther-Flow Research Project. (2026e). *V16 support-only executable
certificate spec* [Research-control task artifact].
