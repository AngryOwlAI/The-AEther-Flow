<!-- authority: control -->

# Matter-Coupling Dependency DAG v1

## Purpose

This artifact implements P4-T02 of
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
It populates the matter-coupling dependency DAG from tracked authority
surfaces under the schema in
`research_control/design/matter_coupling_dependency_dag_schema_v1.md`.

The DAG is navigational project-control support. It is not proof authority,
not a source-law adoption, not matter-semantics adoption, not
detector-semantics adoption, not coupling-law adoption, not matter-coupling
derivation or adoption, not stress-energy semantics, not a stress-energy
tensor, not a matter action, not Einstein equations, not benchmark promotion,
and not a completed derivation.

## Authority Boundary

Every node and edge below cites tracked authority. Generated wiki notes, local
Obsidian notes, semantic extracts, SQLite memory, validator output, registry
metadata, role identity, handoff text, and commit status are support surfaces
only. They do not promote any physics claim.

No high-risk node below uses bare `accepted` status. Scoped Gate Chair results
are rendered as `scoped_evidence_precondition` or as source-bound
non-promotional support.

## Source Inventory

| Source ID | Path | Registry | Object ID | Hash or ledger field | Authority use |
| --- | --- | --- | --- | --- | --- |
| `src_plan_v15` | `implementations_plans/recommendations_implementation_plan_continue_task-v15.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V15` | `624f13305a1518a63b25c9b543f5fbf408b983fb3cf9c0b504475c5ef320e5ba` | P4-T02 task requirements and done criteria. |
| `src_schema_p4_t01` | `research_control/design/matter_coupling_dependency_dag_schema_v1.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-SCHEMA-V1` | `7e63b792cc9d7effc7da57750d166724496cbd368d4399ab086f8634b6af4834` | Required node kinds, layers, guards, and edge vocabulary. |
| `src_current_frontier` | `research_control/current_frontier.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-CURRENT-FRONTIER` | `ef889e74878398ae246e980c4c629336d69125f4ce0c617a3584662b72e21a91` | Current matter-coupling boundary and next route summary. |
| `src_distance_ledger` | `registries/DISTANCE_TO_GR_LEDGER.csv` | `DISTANCE_TO_GR_LEDGER.csv` | `matter_coupling` row and downstream rows | `0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61` | Ledger statuses, missing burdens, physical-status separation, and overread guards. |
| `src_m_src_gate` | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-RESEARCH-CONTROL-M-SRC-GSC-INTEGRATED-SOURCE-ONLY-ADOPTION-THEOREM-GATE-CHAIR-REVIEW` | `9d7af3bce56a9ec2af58cd0d9f10bb759609680710d6332d68d0db0bf4fae09d` | Scoped source-only `M_src` adopted object context; no target manifold, metric, matter coupling, Einstein equations, benchmark, or completed derivation. |
| `src_p2_manifest` | `research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T01-T02-SOURCE-SIDE-MATTER-SEMANTICS-OBJECT-CERTIFICATE-MANIFEST` | `81f8d552d04c942522bd7aab128a9bb65b4ab1a165c0c2e6468d8a877069c24d` | Source-side matter-semantics objects and certificate classes. |
| `src_p2_theorem` | `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T03-NARROW-SOURCE-SIDE-MATTER-SEMANTICS-EQUIVALENCE-THEOREM` | `aca8af857f2a53bfcbdd775b147323dab9e8a814ec78409faace45eef61bc04b` | Conditional source-side theorem under explicit certificates. |
| `src_p2_audit` | `research_control/tasks/RT-20260702-059/artifacts/matter_semantics_equivalence_theorem_smuggling_audit_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T04-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-SMUGGLING-AUDIT` | `3521b359ead752d615983aa942d6e93a302aeba6be8a882aed8dc5b513524820` | Source-purity audit with no detector, stress-energy, matter-action, Einstein-equation, or status-laundering import as written. |
| `src_p2_stress` | `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T05-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-REFUTER-STRESS` | `1be7ba5ac04095d7582612e0831fadcc55e58be0938ab25f2c7b7705da541182` | Certificate-gap witness and blocked overread stress result. |
| `src_gate_narrow_ms` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-NARROW-MS-CERT-EQ-GATE-CHAIR-REVIEW` | `34e2f86e377edc3d13513d6f0a9e8d3083829bda230d32309177a82879770ca7` | Gate Chair scoped evidence-status acceptance for `NarrowMSCertEq_v1` only. |
| `src_p3_primitives` | `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P3-T01-SOURCE-CERTIFICATE-ALGEBRA-PRIMITIVES` | `43d20536f39682c42743739715534096c06d5e445ae269378bab9db95e73fa1e` | Draft/control source certificate primitive vocabulary. |
| `src_p3_laws` | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS` | `2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986` | Draft/control source certificate operation laws and fail-closed branches. |
| `src_certificate_checklist` | `research_control/design/source_certificate_algebra_checklist.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-SOURCE-CERTIFICATE-ALGEBRA-CHECKLIST` | `158dee6549b691b82d2e31a3d8df0caafe9d8e0ce8ef62dd2213800cc11f91fa` | No-target and certificate checklist discipline. |
| `src_no_target_map` | `research_control/design/no_target_import_guard_map.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-NO-TARGET-IMPORT-GUARD-MAP` | `4c4e736a84bb59ae11710fa185788e86bd6de6de3176f748b2689d9fcda755ce` | No-target-import guard categories and process-laundering blocks. |
| `src_moratorium` | `research_control/design/matter_coupling_derivation_moratorium.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DERIVATION-MORATORIUM` | `435e92ca1340c5b69fae97895ffe2b3fe203087384864d13be30fa0890370e0c` | Direct universal matter-coupling derivation moratorium. |
| `src_pre_adoption` | `research_control/design/matter_coupling_pre_adoption_checklist.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-PRE-ADOPTION-CHECKLIST` | `7586f1ea939eb508a451498d0f15225308fc98127803d58e81fa1adbfd3e9d60` | Adoption-facing missing-law and protected-authority checklist. |
| `src_gate_rr_e` | `research_control/tasks/RT-20260701-030/artifacts/rr_e_transport_law_gate_chair_review_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V13-P5-FOLLOWUP-RR-E-TRANSPORT-LAW-GATE-CHAIR-REVIEW` | `de7a76b92d998e7c3798214bae8d5cd1fd7f27e643e56516d9f215dd0de509b3` | `RR_ETransportCompletenessOrInvarianceLaw_v1` scoped evidence/precondition only; no source-law adoption. |
| `src_gate_ms_stable` | `research_control/tasks/RT-20260630-056/artifacts/ms_stable_matter_semantics_bridge_source_extension_evidence_gate_chair_review_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V12-P7-T03-MS-STABLE-MATTER-SEMANTICS-BRIDGE-GATE-CHAIR-EVIDENCE-STATUS` | `a378610f3e22ecf7209788832fd7fe403e52e10cb31f269fb841993c34d3ee33` | `MSStableMatterSemanticsBridge_v1` scoped source-extension evidence/precondition only. |

## Populated Nodes

| Node ID | Label | Kind | Layer | Status | Source evidence path | Exact missing burden or promotion blocker | Forbidden overread guards |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `mc_m_src_scoped_source_object` | scoped source-only `M_src` object | `adopted_object` | `source_matter_semantics` | `adopted_scoped_source_object` | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | Scoped source-only object; not a target manifold, not a metric, not matter coupling, not Einstein equations, not benchmark promotion, and not completed derivation. | no_metricdata_e_adoption; no_geff_scope_expansion; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_source_matter_semantics_objects` | source-side matter-semantics objects | `evidence_precondition` | `source_matter_semantics` | `draft_control` | `research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex` | Matter-semantics adoption is absent; these are source-side objects and certificate classes only. | no_matter_semantics_adoption; no_detector_semantics; no_coupling_law_adoption; no_matter_coupling_derivation; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_source_matter_semantics_equivalence_theorem` | source-side matter-semantics equivalence theorem | `theorem` | `source_matter_semantics` | `conditional_source_side_theorem` | `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex` | Unconditional theorem, source-law adoption, matter-semantics adoption, detector semantics, and coupling-law adoption remain absent. | no_source_law_adoption; no_unrestricted_RR_E_theorem; no_matter_semantics_adoption; no_detector_semantics; no_coupling_law_adoption; no_matter_coupling_derivation; no_benchmark_promotion; no_completed_derivation |
| `mc_narrow_ms_cert_eq_gate_chair_scoped_status` | `NarrowMSCertEq_v1` scoped Gate Chair evidence-status | `evidence_precondition` | `source_matter_semantics` | `scoped_evidence_precondition` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` | Gate Chair accepted only scoped evidence-status; no source law, matter semantics, detector semantics, coupling law, matter coupling, stress-energy, matter action, Einstein equations, benchmark, or completed derivation. | no_source_law_adoption; no_matter_semantics_adoption; no_detector_semantics; no_coupling_law_adoption; no_matter_coupling_derivation; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_rr_e_certificate_boundary` | `RR_E` certificate boundary | `evidence_precondition` | `certificate_boundary` | `certificate_indexed_guard_or_fail_closed` | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | Missing, malformed, target-importing, detector-semantic, or benchmark-dependent certificates fail closed; no `RR_ETransportCompletenessOrInvarianceLaw_v1` source-law adoption or unrestricted `RR_E` theorem exists. | no_RR_ETransportCompletenessOrInvarianceLaw_v1_adoption; no_unrestricted_RR_E_theorem; no_source_law_adoption; no_matter_coupling_derivation; no_detector_semantics; no_benchmark_promotion; no_completed_derivation |
| `mc_source_certificate_algebra_controls` | source certificate algebra controls | `evidence_precondition` | `certificate_boundary` | `draft_control` | `research_control/design/source_certificate_algebra_checklist.md` | Checklist pass is workflow evidence only; concrete certificate records remain required and missing/malformed certificates fail closed. | no_source_law_adoption; no_RR_ETransportCompletenessOrInvarianceLaw_v1_adoption; no_matter_semantics_adoption; no_detector_semantics; no_matter_coupling_derivation; no_benchmark_promotion; no_completed_derivation |
| `mc_certificate_gap_obstruction` | certificate-gap witness obstruction | `obstruction` | `certificate_boundary` | `draft_control` | `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | Missing explicit valid source certificates block unconditional theorem and evidence-as-adoption readings. | no_unconditional_theorem; no_evidence_as_adoption; no_detector_semantics; no_matter_coupling_derivation; no_benchmark_promotion; no_completed_derivation |
| `mc_no_target_certificate_controls` | no-target certificate controls | `evidence_precondition` | `certificate_boundary` | `draft_control` | `research_control/design/no_target_import_guard_map.md` | No-target certificates prevent forbidden imports only; they do not provide positive matter theory. | no_target_import_as_positive_matter_theory; no_detector_semantics; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_detector_semantics_target` | detector-semantics target | `physical_target` | `detector_semantics` | `blocked` | `research_control/design/matter_coupling_derivation_moratorium.md` | Missing burden: detector semantics or an explicitly source-side replacement for detector semantics established under tracked authority. | no_detector_semantics_adoption; no_matter_semantics_as_detector_semantics; no_matter_coupling_derivation; no_stress_energy_semantics; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_coupling_law_target` | coupling-law target | `law` | `coupling_law` | `blocked` | `research_control/design/matter_coupling_pre_adoption_checklist.md` | Missing burden: coupling-law target or candidate plus protected authority for any adoption request. | no_coupling_law_adoption; no_matter_coupling_derivation; no_matter_coupling_adoption; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_stress_energy_semantics_target` | stress-energy semantics target | `physical_target` | `stress_energy_action` | `blocked` | `research_control/design/matter_coupling_derivation_moratorium.md` | Missing burden: stress-energy semantics or an explicit tracked reason stress-energy semantics are not needed. | no_stress_energy_semantics; no_stress_energy_tensor; no_matter_action; no_coupling_law_adoption; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_stress_energy_tensor_target` | stress-energy tensor target | `physical_target` | `stress_energy_action` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Missing burden: stress-energy tensor construction from tracked stress-energy semantics or equivalent authorized dynamics data. | no_stress_energy_tensor; no_stress_energy_semantics; no_matter_action; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_matter_action_target` | matter-action target | `physical_target` | `stress_energy_action` | `blocked` | `research_control/design/matter_coupling_derivation_moratorium.md` | Missing burden: matter action or explicit alternative dynamics path under tracked authority. | no_matter_action; no_stress_energy_semantics; no_stress_energy_tensor; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_universal_matter_coupling_derivation` | universal matter-coupling derivation | `physical_target` | `universal_matter_coupling` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Missing burden: matter semantics, detector semantics or replacement, coupling law, stress-energy/action path, `RR_E` handling, no-target hygiene, and protected adoption authority. | no_coupling_law_adoption; no_matter_coupling_derivation; no_matter_coupling_adoption; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_einstein_equation_dependency` | Einstein-equation dependency | `physical_target` | `einstein_equations` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Missing burden: dynamics, action or variation path, universal matter coupling, and field-equation derivation theorem. | no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_benchmark_promotion_dependency` | benchmark promotion dependency | `physical_target` | `benchmark_promotion` | `blocked_or_human_gated` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Missing burden: all upstream derivation burdens plus explicit protected Gate Chair benchmark authority. | no_benchmark_promotion; no_benchmark_gate_chair_closure; no_completed_derivation |

## Populated Edges

| Edge ID | Source | Edge kind | Target | Source evidence path | Summary | Forbidden overread guards |
| --- | --- | --- | --- | --- | --- | --- |
| `mc_edge_objects_to_theorem` | `mc_source_matter_semantics_objects` | `supports_as_evidence` | `mc_source_matter_semantics_equivalence_theorem` | `research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex` | Source objects and certificate classes support only the conditional theorem package. | no_evidence_as_adoption; no_matter_semantics_adoption; no_detector_semantics |
| `mc_edge_m_src_context_to_source_objects` | `mc_m_src_scoped_source_object` | `depends_on` | `mc_source_matter_semantics_objects` | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | Scoped source-only `M_src` is upstream context only and does not become target geometry, metric data, or matter coupling. | no_metricdata_e_adoption; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion |
| `mc_edge_rr_e_boundary_to_theorem` | `mc_rr_e_certificate_boundary` | `requires` | `mc_source_matter_semantics_equivalence_theorem` | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | The theorem remains certificate-indexed and fail-closed when certificates are missing, malformed, or target-importing. | no_unrestricted_RR_E_theorem; no_RR_ETransportCompletenessOrInvarianceLaw_v1_adoption; no_source_law_adoption |
| `mc_edge_gate_status_to_theorem` | `mc_narrow_ms_cert_eq_gate_chair_scoped_status` | `supports_as_evidence` | `mc_source_matter_semantics_equivalence_theorem` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` | Gate Chair status is scoped evidence/precondition only for later certificate algebra or dependency-control work. | no_source_law_adoption; no_matter_semantics_adoption; no_coupling_law_adoption; no_matter_coupling_derivation |
| `mc_edge_certificate_gap_blocks_unconditional_theorem` | `mc_certificate_gap_obstruction` | `blocks` | `mc_source_matter_semantics_equivalence_theorem` | `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | Certificate-gap witness blocks unconditional or adoption-style readings of the theorem. | no_unconditional_theorem; no_evidence_as_adoption; no_global_no_go |
| `mc_edge_no_target_forbids_layer_import` | `mc_no_target_certificate_controls` | `forbids_overread` | `mc_universal_matter_coupling_derivation` | `research_control/design/no_target_import_guard_map.md` | No-target certificates prevent target imports; they do not supply positive matter theory. | no_target_import_as_positive_matter_theory; no_matter_coupling_derivation; no_einstein_equations |
| `mc_edge_theorem_to_coupling_law` | `mc_source_matter_semantics_equivalence_theorem` | `supports_as_evidence` | `mc_coupling_law_target` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` | Conditional theorem and scoped evidence-status may support future coupling-law target work but do not adopt a coupling law. | no_coupling_law_adoption; no_matter_coupling_derivation; no_matter_coupling_adoption |
| `mc_edge_detector_to_universal` | `mc_detector_semantics_target` | `requires` | `mc_universal_matter_coupling_derivation` | `research_control/design/matter_coupling_derivation_moratorium.md` | Detector semantics or an authorized source-side replacement is a prerequisite for direct universal matter coupling. | no_detector_semantics_adoption; no_matter_coupling_derivation |
| `mc_edge_coupling_law_to_universal` | `mc_coupling_law_target` | `requires` | `mc_universal_matter_coupling_derivation` | `research_control/design/matter_coupling_pre_adoption_checklist.md` | Coupling-law target and adoption authority remain missing before universal coupling. | no_coupling_law_adoption; no_matter_coupling_derivation |
| `mc_edge_stress_semantics_to_tensor` | `mc_stress_energy_semantics_target` | `requires` | `mc_stress_energy_tensor_target` | `research_control/design/matter_coupling_derivation_moratorium.md` | Stress-energy tensor construction requires tracked stress-energy semantics or equivalent authorized dynamics data. | no_stress_energy_semantics; no_stress_energy_tensor |
| `mc_edge_tensor_to_action` | `mc_stress_energy_tensor_target` | `requires` | `mc_matter_action_target` | `registries/DISTANCE_TO_GR_LEDGER.csv` | A stress-energy tensor does not imply a matter action without separate tracked authority. | no_matter_action; no_einstein_equations |
| `mc_edge_action_to_einstein` | `mc_matter_action_target` | `requires` | `mc_einstein_equation_dependency` | `research_control/design/matter_coupling_derivation_moratorium.md` | Einstein-equation work requires a matter action or alternative dynamics path, not only source-side evidence. | no_einstein_equations; no_benchmark_promotion |
| `mc_edge_universal_to_einstein` | `mc_universal_matter_coupling_derivation` | `requires` | `mc_einstein_equation_dependency` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Universal matter coupling is necessary but not sufficient for Einstein equations; the field-equation derivation burden remains open. | no_einstein_equations; no_completed_derivation |
| `mc_edge_einstein_to_benchmark` | `mc_einstein_equation_dependency` | `requires` | `mc_benchmark_promotion_dependency` | `registries/DISTANCE_TO_GR_LEDGER.csv` | Benchmark promotion remains downstream of all derivation burdens and protected authority. | no_benchmark_promotion; no_benchmark_gate_chair_closure; no_completed_derivation |
| `mc_edge_moratorium_blocks_direct_route` | `mc_source_certificate_algebra_controls` | `blocks` | `mc_universal_matter_coupling_derivation` | `research_control/design/matter_coupling_derivation_moratorium.md` | Certificate discipline and scoped evidence do not lift the direct matter-coupling moratorium without all prerequisites. | no_matter_coupling_derivation; no_matter_coupling_adoption; no_completed_derivation |
| `mc_edge_pre_adoption_requires_gate` | `mc_coupling_law_target` | `requires_human_gate` | `mc_benchmark_promotion_dependency` | `research_control/design/matter_coupling_pre_adoption_checklist.md` | Adoption-facing matter-sector promotions require exact protected authority and cannot be inferred from P4-T02. | no_benchmark_promotion; no_completed_derivation |

## Blocked Node Burden Summary

| Node ID | Exact missing burden |
| --- | --- |
| `mc_detector_semantics_target` | Detector semantics or an explicitly source-side replacement for detector semantics established under tracked authority. |
| `mc_coupling_law_target` | Coupling-law target or candidate plus protected authority for any coupling-law adoption request. |
| `mc_stress_energy_semantics_target` | Stress-energy semantics or an explicit tracked reason stress-energy semantics are not needed. |
| `mc_stress_energy_tensor_target` | Stress-energy tensor construction from tracked stress-energy semantics or equivalent authorized dynamics data. |
| `mc_matter_action_target` | Matter action or explicit alternative dynamics path under tracked authority. |
| `mc_universal_matter_coupling_derivation` | Matter semantics, detector semantics or replacement, coupling law, stress-energy/action path, `RR_E` handling, no-target hygiene, and protected adoption authority. |
| `mc_einstein_equation_dependency` | Dynamics, action or variation path, universal matter coupling, and field-equation derivation theorem. |
| `mc_benchmark_promotion_dependency` | All upstream derivation burdens plus explicit protected Gate Chair benchmark authority. |

## Status Separation

- `NarrowMSCertEq_v1` is scoped evidence/precondition only.
- Source certificate algebra is draft/control certificate discipline only.
- The certificate-gap witness remains an obstruction to unconditional or
  adoption-style readings.
- No-target certificates are hygiene and import-prevention controls only.
- This DAG is not detector-semantics adoption and not matter-coupling derivation.
- Matter semantics, detector semantics, coupling law, stress-energy semantics,
  stress-energy tensor, matter action, Einstein equations, benchmark
  promotion, and completed derivation remain blocked.

## P4-T02 Completion Criteria

This P4-T02 packet may claim only that:

- the populated DAG artifact exists;
- every edge has a tracked source evidence path;
- every blocked node names the exact missing burden or protected authority;
- high-risk nodes avoid bare `accepted` status; and
- P4-T03 may create the later semantic-layer separation control note.

It may not claim matter-coupling derivation, adoption, downstream GR recovery,
benchmark promotion, or completed derivation.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling dependency
DAG schema v1* [Internal control source].
`research_control/design/matter_coupling_dependency_dag_schema_v1.md`

The AEther-Flow Research Project. (2026, July 2). *Current research frontier*
[Internal control report]. `research_control/current_frontier.md`

The AEther-Flow Research Project. (2026, July 2). *NarrowMSCertEq v1 scoped
evidence-status Gate Chair review* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex`

The AEther-Flow Research Project. (2026, July 2). *Source certificate
operation laws v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`
