<!-- authority: science_draft -->

# Internal One-Question Red-Team Pilot v16

Task: `RT-20260705-029`

Plan task: `P13-T03`

Role: `refuter@0.2.0--RT-20260705-029`

Status: `draft/control`

External outreach performed: `false`

Physics promotion authorized: `false`

## Selected Question

```text
Does NarrowMSCertEq_v1 plus the source certificate algebra supply any nontrivial
source-side mathematical content beyond definitions, and does any hidden target-side
or detector-side import occur?
```

## Reviewed Artifacts

The internal pilot inspected the exact P13-T02 packet and its source bundle:

| Artifact | Object ID | Review use |
| --- | --- | --- |
| `research_control/design/one_question_red_team_packet_v16.md` | `MD-RESEARCH-CONTROL-DESIGN-ONE-QUESTION-RED-TEAM-PACKET-V16` | Review packet and claim boundary. |
| `research_control/tasks/RT-20260705-027/artifacts/one_question_red_team_question_selector_v16.md` | `MD-RESEARCH-CONTROL-TASKS-RT-20260705-027-ONE-QUESTION-RED-TEAM-QUESTION-SELECTOR-V16` | Selected question and source bundle. |
| `research_control/tasks/RT-20260705-023/artifacts/negative_result_integration_selector_v16.md` | `MD-RESEARCH-CONTROL-TASKS-RT-20260705-023-NEGATIVE-RESULT-INTEGRATION-SELECTOR-V16` | Certificate-gap witness integration route. |
| `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex` | `TEX-V15-P2-T03-NARROW-SOURCE-SIDE-MATTER-SEMANTICS-EQUIVALENCE-THEOREM` | Conditional theorem and fail-closed branches. |
| `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | `TEX-V15-P2-T05-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-REFUTER-STRESS` | Certificate-gap finite/local witness and blocked overreads. |
| `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex` | `TEX-V15-P3-T01-SOURCE-CERTIFICATE-ALGEBRA-PRIMITIVES` | Certificate record shape, missing or malformed states, and no-target guard. |
| `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | `TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS` | Conditional operation laws and target-import invalidity. |
| `research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex` | `TEX-V16-P5-T01-EQMS-DEFINITION-THEOREM-CONTENT-SEPARATION-AUDIT` | Definition-unfolding versus nontrivial content separation. |
| `research_control/design/semantic_layer_separation_control_note.md` | `MD-RESEARCH-CONTROL-DESIGN-SEMANTIC-LAYER-SEPARATION-CONTROL-NOTE` | Source, detector, and stress-energy/action layer separation. |
| `research_control/design/matter_coupling_dependency_dag_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-V1` | Blocked downstream dependency context. |

Generated wiki notes, semantic extracts, Obsidian notes, PDFs, validators,
registries, handoffs, local caches, commit state, and role identity were used
only as navigation or provenance support, not as mathematical premises.

## Internal Reviewer Output

```yaml
reviewer_name_or_anonymous_id: "internal_refuter_pilot"
review_date: "2026-07-05"
reviewed_artifacts:
  - "research_control/design/one_question_red_team_packet_v16.md"
  - "research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex"
  - "research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex"
  - "research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex"
  - "research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex"
  - "research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex"
selected_question: "Does NarrowMSCertEq_v1 plus the source certificate algebra supply any nontrivial source-side mathematical content beyond definitions and does any hidden target-side or detector-side import occur?"
strongest_valid_reading: "Scoped source-side evidence status survives only under explicit valid source certificates and no-target guards."
strongest_overread_risk: "Treating definition unfolding, no-target hygiene, scoped evidence, validator status, or finite/local examples as matter semantics, detector semantics, matter coupling, or theorem generality."
hidden_imports_detected: "No hidden target-side or detector-side mathematical premise was detected in the artifacts as written; the artifacts explicitly fail closed when such imports are attempted."
smallest_counterexample_or_missing_premise: "For any stronger reading, the smallest failed premise is an explicit valid source-certificate existence theorem or concrete certificate family for the claimed source-object scope. The existing MC-NARROW-MS-CERT-EQ-CERT-GAP-001 witness shows the deletion or malformation branch."
recommendation: "accept_scoped_status"
integration_route: "continue_to_p14_target_import_attack_taxonomy_v16"
review_confidence: "medium_high"
claim_boundary_warning_acknowledged: true
```

## Answer To Selected Question

`NarrowMSCertEq_v1` supplies mostly definition unfolding once explicit valid
source certificates are assumed. Its positive proof checks that the clauses of
`EqMS_src^cert` are satisfied: at least one permitted certificate exists, the
no-target certificate passes, declared-object indexing is consistent, and
fail-closed branches are inactive.

The source certificate algebra supplies nontrivial source-side mathematical
content beyond that definition unfolding, but the content is conditional and
scoped. The nontrivial portion is in:

- explicit certificate record fields and valid-record discipline;
- identity declared-scope preservation;
- compatible composition closure;
- source restriction closure;
- missing, malformed, and target-import invalidity lemmas;
- the finite/local certificate-gap witness used to block stronger readings.

No hidden target-side or detector-side mathematical premise was detected in
the source artifacts as written. The inspected artifacts repeatedly state that
target topology, target atlas, target metric, Lorentzian signature, proper
time, detector semantics, empirical calibration, benchmark behavior,
stress-energy semantics, matter action, validators, roles, handoffs, approval
state, generated derivatives, local caches, file order, and commit state
cannot be used as mathematical premises.

## Strongest Valid Reading

The strongest valid reading is:

`NarrowMSCertEq_v1` is scoped source-side evidence for a conditional theorem
role under explicit valid source certificates. It may support later route
selection and certificate-discipline work. It does not by itself construct a
general source-certificate existence theorem, matter semantics, detector
semantics, a coupling law, matter coupling, stress-energy semantics, a matter
action, Einstein equations, benchmark promotion, or completed derivation.

## Definition-Unfolding Assessment

Definition unfolding:

- the transport, invariance, and factorization cases in the positive
  `NarrowMSCertEq_v1` proof;
- the use of `EqMS_src^cert` once at least one explicit certificate and all
  guards are assumed;
- the no-target branch as negative hygiene.

Nontrivial source-side content:

- operation laws for identity, compatible composition, and restriction;
- fail-closed lemmas for missing, malformed, and imported certificates;
- object-indexed validity requirements for certificates;
- the finite/local certificate-gap witness against unconditional overread.

## Hidden-Import Assessment

No hidden target-side, detector-side, empirical, stress-energy, process,
generated-derivative, or validator-status import was detected in the reviewed
sources as written.

The result is not that such imports are impossible. The result is narrower:
the current artifacts name those imports as invalid or fail-closed branches.
Future packets can still accidentally import them through wording or fixture
design, so P14 should create a target-import attack taxonomy and fixture suite.

## Smallest Counterexample Or Missing Premise

For a stronger-than-scoped reading, the smallest failed premise is:

```yaml
failed_premise: "explicit valid source-certificate existence theorem or concrete certificate family for the claimed source-object scope"
countermodel_path: "research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex"
countermodel_id: "MC-NARROW-MS-CERT-EQ-CERT-GAP-001"
countermodel_scope: "finite/local certificate deletion or malformation branch"
```

This is not a countermodel to the conditional theorem as stated. It is a
countermodel to any unconditional, adoption-style, detector-semantic,
matter-coupling, or finite/local-to-global overread.

## Parent-Child Synthesis

### Child A: Physicist-Mathematician

Child A found that the positive theorem branch is valid only after explicit
certificate premises are supplied. The nontrivial mathematical content is in
the certificate algebra and fail-closed lemmas, not in a general existence
claim for certificates.

### Child B: Physicist-Philosopher

Child B found that the source-side theorem role is ontologically and
semantically separate from detector semantics, physical matter semantics,
stress-energy/action semantics, and benchmark recovery. The artifact language
does not authorize treating scoped evidence as adoption.

### Parent Fusion

The children agree. The internal pilot accepts scoped status and rejects
stronger overreads. No blocking conflict remains. The next route should
increase automated and semi-automated pressure against hidden imports by
running P14-T01.

## Refuter Obstruction Record

```yaml
obstruction_id: "P13T03-OB-STRONGER-CERT-EXISTENCE-MISSING-001"
obstruction_type: "stronger_than_scoped_reading_failed_premise"
scope: "P13-T03 internal one-question red-team pilot"
failed_premise: "explicit valid source-certificate existence theorem or concrete certificate family for the claimed source-object scope"
minimal_countermodel_available: true
countermodel_path: "research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex"
countermodel_id: "MC-NARROW-MS-CERT-EQ-CERT-GAP-001"
countermodel_scope: "finite/local certificate deletion or malformation branch"
claim_boundary_preserved: true
global_no_go_claim_authorized: false
future_source_extension_impossibility_authorized: false
```

## Recommendation And Integration Route

Recommendation: `accept_scoped_status`.

Exactly one integration route is selected:

```yaml
selected_integration_route: "continue_to_p14_target_import_attack_taxonomy_v16"
next_plan_task_id: "P14-T01"
next_task_type: "target_import_attack_taxonomy_v16"
recommended_role: "smuggling-auditor@0.2.0"
```

Rationale: the scoped status survives, but the highest remaining operational
risk is hidden target-side, detector-side, process-authority, generated-output,
validator-status, and finite/local-to-global import. P14 directly implements
that pressure without promoting any physics claim.

## Non-Conclusions

This internal pilot does not adopt a source law, adopt
`RR_ETransportCompletenessOrInvarianceLaw_v1`, prove unrestricted `RR_E`
status, adopt matter semantics, adopt detector semantics, adopt a coupling
law, derive or adopt matter coupling, introduce stress-energy semantics,
construct a stress-energy tensor, introduce a matter action, derive Einstein
equations, promote benchmark status, issue a Gate Chair verdict, close future
source-extension continuation, or claim completed derivation.

## References

The AEther-Flow Research Project. (2026a). *One-question red-team packet v16*
[Internal control packet].
`research_control/design/one_question_red_team_packet_v16.md`

The AEther-Flow Research Project. (2026b). *Narrow source-side
matter-semantics equivalence theorem attempt v1* [Research-control TeX
artifact].
`research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex`

The AEther-Flow Research Project. (2026c). *Matter-semantics equivalence
theorem Refuter stress v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex`

The AEther-Flow Research Project. (2026d). *Source certificate operation laws
and fail-closed lemma v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`

The AEther-Flow Research Project. (2026e). *EqMS definition/theorem-content
separation audit v16* [Research-control TeX artifact].
`research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex`
