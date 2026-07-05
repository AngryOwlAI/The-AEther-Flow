<!-- authority: control -->

# Source Certificate Instance Library Index v1

## Status

This control index implements v16 P4-T06. It indexes the P4 certificate
instances created under the source certificate-instance schema and selects one
next route.

The index is a routing and retrieval aid for finite/local source-certificate
fixtures. It is not a source law, not an unrestricted `RR_E` theorem, not
matter semantics, not detector semantics, not a coupling law, not matter
coupling, not stress-energy semantics, not matter action, not Einstein
equations, not benchmark promotion, and not a completed derivation.

## Scope

The indexed instances are the P4 positive and negative fixtures:

- P4-T02 valid transport certificate: `SCI-TRANSPORT-001`.
- P4-T03 valid invariance certificate: `SCI-INVARIANCE-001`.
- P4-T04 valid factorization certificate: `SCI-FACTORIZATION-001`.
- P4-T05 negative certificate packet: eight fail-closed instances.

Generated wiki notes, validator output, commits, approvals, and local caches are
not certificate payload data. Reuse is allowed only inside the declared
finite/local source scope of each instance and under the no-target-import
guards in the source artifact.

## Instance Index

| Instance ID | Artifact path | Instance kind | Positive/negative status | Source objects | Certificate kind | Expected result | Allowed reuse | Blocked overreads | Formalization availability | Related model-zoo model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SCI-TRANSPORT-001` | `research_control/tasks/RT-20260704-026/artifacts/finite_local_transport_certificate_instance_v1.tex` | `valid_transport_certificate` | positive; `valid` | `A_src=(E_src,L,G,R,domain)` to `B_src=(E_src,L',G',R',codomain)` with `E_src={0,1,2}` | transport witness | `declared_equivalence_allowed` inside declared scope | finite/local transport fixture for later P5/P6/P10/P14/P15 source-side packets | no source-law adoption; no unrestricted `RR_E` theorem; no matter or detector semantics; no coupling law; no matter coupling; no stress-energy; no matter action; no Einstein equations; no benchmark promotion; no completed derivation | TeX draft/control source; not executable formalization | none registered; eligible as a future source model-zoo seed |
| `SCI-INVARIANCE-001` | `research_control/tasks/RT-20260704-027/artifacts/finite_local_invariance_certificate_instance_v1.tex` | `valid_invariance_certificate` | positive; `valid` | `A_src=(E_src,L,G,R,Q,cycle_domain)` to `A_src^sigma=(E_src,L^sigma,G^sigma,R^sigma,Q^sigma,cycle_codomain)` with `sigma=(0 1 2)` | invariance witness | `declared_equivalence_allowed` inside declared scope | finite/local relabeling-invariance fixture for later source-side packets | no empirical invariance; no detector invariance; no source-law adoption; no unrestricted `RR_E` theorem; no matter or detector semantics; no coupling law; no matter coupling; no stress-energy; no matter action; no Einstein equations; no benchmark promotion; no completed derivation | TeX draft/control source; not executable formalization | none registered; eligible as a future source model-zoo seed |
| `SCI-FACTORIZATION-001` | `research_control/tasks/RT-20260705-001/artifacts/finite_local_factorization_certificate_instance_v1.tex` | `valid_factorization_certificate` | positive; `valid` | `A_src=(E_src,L_A,G_A,R_A,factor_domain)` through `F_src={alpha,beta}` to `B_src=({b_0,b_1},L_B,G_B,R_B,factor_codomain)` | factorization witness | `declared_equivalence_allowed` inside declared scope | finite/local factorization fixture for later source-side theorem-content and formalization packets | no global `RR_E` collapse; no source-law adoption; no unrestricted `RR_E` theorem; no matter or detector semantics; no coupling law; no matter coupling; no stress-energy; no matter action; no Einstein equations; no benchmark promotion; no completed derivation | TeX draft/control source; not executable formalization | none registered; eligible as a future source model-zoo seed |
| `SCI-NEG-MISSING-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `missing_certificate_negative` | negative; `missing` | `A_src=(E_src,L_A,G_A,R_A,negative_domain)` with absent codomain/payload | missing transport certificate | `declared_equivalence_blocked` | fail-closed fixture for absence-of-payload tests | no declared equivalence from absent payload; no `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption; no unrestricted `RR_E` theorem; no matter coupling | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-MALFORMED-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `malformed_certificate_negative` | negative; `malformed` | `A_src` and `B_src` over `{0,1}` with candidate map leaving codomain | malformed transport candidate | `declared_equivalence_blocked` | fail-closed fixture for domain/codomain mismatch tests | no declared equivalence from malformed map; no source transport completeness; no benchmark recovery; no completed derivation | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-FACTOR-CHANGE-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `malformed_certificate_negative` | negative; `malformed` | `A_src` and `B_src` over `{0,1}` with changed middle factor object | changed factorization object | `declared_equivalence_blocked` | fail-closed fixture for factor-object identity tests | no factorization preservation after object substitution; no global `RR_E` collapse; no coupling-law adoption | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-TARGET-METRIC-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `target_import_rejected_certificate` | negative; `rejected_target_import` | `A_src` and `B_src` over `{0,1}` with target metric imported as witness | target-metric import rejection | `declared_equivalence_blocked` | fail-closed fixture for no-target-import tests | no source equivalence from target metric; no effective metric adoption; no matter coupling; no Einstein equations | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-DETECTOR-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `detector_semantics_rejected_certificate` | negative; `rejected_detector_semantics` | `A_src` and `B_src` over `{0,1}` with detector-event sameness imported | detector-semantics import rejection | `declared_equivalence_blocked` | fail-closed fixture for detector-semantics smuggling tests | no detector semantics adoption; no matter semantics; no stress-energy semantics; no benchmark status | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-STRESS-ENERGY-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `target_import_rejected_certificate` | negative; `fail_closed` | `A_src` and `B_src` over `{0,1}` with stress-energy shortcut imported | stress-energy shortcut rejection | `declared_equivalence_blocked` | fail-closed fixture for stress-energy shortcut tests | no stress-energy semantics; no matter action; no Einstein equations; no benchmark promotion | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-VALIDATOR-PASS-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `process_authority_rejected_certificate` | negative; `rejected_process_authority` | `A_src` and `B_src` over `{0,1}` with validator status imported | process-authority rejection | `declared_equivalence_blocked` | fail-closed fixture for validator-as-proof tests | no proof authority from tooling; no source-law adoption; no completed derivation; no Gate Chair verdict | TeX draft/control source; not executable formalization | none registered |
| `SCI-NEG-SCOPED-EVIDENCE-001` | `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` | `process_authority_rejected_certificate` | negative; `rejected_process_authority` | `A_src` and `B_src` over `{0,1}` with scoped evidence converted into adoption | scoped-evidence adoption rejection | `declared_equivalence_blocked` | fail-closed fixture for scope-expansion tests | no source-law adoption; no `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption; no unrestricted `RR_E` theorem; no matter coupling | TeX draft/control source; not executable formalization | none registered |

## Selector Evaluation

| Candidate next route | Disposition | Reason |
| --- | --- | --- |
| Equivalence/theorem separation refactor | selected | P4 fixtures are complete enough to support P5's definitional-equivalence versus theorem-content audit without immediate P4 repair. |
| Executable formalization of instances | deferred | The index records formalization availability as TeX draft/control only; executable formalization can be selected later from P6/P10/P15 if needed. |
| Source model zoo expansion | deferred | Positive fixtures are eligible model-zoo seeds, but P5 is the plan default after P4 when no repair is required. |
| Target-import attack suite | deferred | Negative fixtures already cover target metric, detector semantics, stress-energy, process authority, and scoped-evidence smuggling. |
| Coupling-law candidate construction | blocked for this handoff | P4 fixtures do not adopt source laws or matter-coupling semantics. A coupling-law candidate requires later authorized construction. |
| Freeze/review if instances fail | not selected | The index found no P4 completeness failure requiring a repair or freeze packet. |

## Selected Next Route

The selected next route is P5-T01, equivalence/theorem-content separation
audit. The route is selected by the P4-T06 default: no immediate repair is
needed, so the handoff proceeds to P5.

The next packet must remain bounded. It may audit and refactor theorem-target
structure, but it must not convert these fixtures into a source law, an
unrestricted `RR_E` theorem, matter semantics, detector semantics, a coupling
law, matter coupling, stress-energy semantics, matter action, Einstein
equations, benchmark promotion, or a completed derivation.

## Machine-Readable Summary

```yaml
index_id: "source_certificate_instance_library_index_v1"
implemented_plan_task: "P4-T06"
schema_source: "research_control/design/source_certificate_instance_library_schema_v1.md"
indexed_instance_count: 11
positive_instance_count: 3
negative_instance_count: 8
all_p4_instances_indexed: true
immediate_repair_needed: false
selected_next_route: "P5-T01 equivalence/theorem-content separation audit"
physics_delta: false
physics_promotion_authorized: false
formalization_availability:
  tex_draft_control_available: true
  executable_formalization_available: false
blocked_authority:
  - source_law_adoption
  - RR_ETransportCompletenessOrInvarianceLaw_v1_adoption
  - unrestricted_RR_E_theorem
  - matter_semantics_adoption
  - detector_semantics_adoption
  - coupling_law_adoption
  - matter_coupling_derivation_or_adoption
  - stress_energy_semantics
  - matter_action
  - Einstein_equations
  - benchmark_promotion
  - completed_derivation
```
