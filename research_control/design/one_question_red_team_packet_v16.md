<!-- authority: control -->

# One-Question Red-Team Packet v16

Status: `draft/control`

Plan task: `P13-T02`

Packet owner: `documentation-curator@2.0.0--RT-20260705-028`

External outreach performed: `false`

## Selected Question

The packet asks exactly one question:

```text
Does NarrowMSCertEq_v1 plus the source certificate algebra supply any nontrivial
source-side mathematical content beyond definitions, and does any hidden target-side
or detector-side import occur?
```

## Review Scope

This packet is usable for an internal pilot or for later external circulation
after a separate outreach decision. A reviewer should evaluate only the selected
question and should not review the whole repository.

The review has three precise targets:

1. distinguish definition unfolding from nontrivial source-side mathematical
   content;
2. test whether the certificate algebra and certificate instances carry the
   stated burden without hidden target-side, detector-side, empirical, or
   process-authority premises;
3. identify the smallest missing premise, counterexample, or repair route if
   the strongest scoped reading fails.

## Exact Source Artifacts

The reviewer should inspect these source artifacts directly. Generated wiki
notes, semantic extracts, Obsidian notes, PDFs, `.local` caches, validator
status, handoff state, and commit state are not independent source authority.

| Source artifact | Object ID | Source hash | Review use |
| --- | --- | --- | --- |
| `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` | `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V16` | `44daaa5e9f0159adaaa0f30e65d39c8080e410552d13adc374f95eda456c0bba` | P13 requirements and selected packet structure. |
| `research_control/tasks/RT-20260705-027/artifacts/one_question_red_team_question_selector_v16.md` | `MD-RESEARCH-CONTROL-TASKS-RT-20260705-027-ONE-QUESTION-RED-TEAM-QUESTION-SELECTOR-V16` | `76cdce10f91303fef1f9e712025197c9b6eb4291bdb3375523779822fac905d4` | Selected question, exact source bundle, and expected reviewer output. |
| `research_control/design/external_red_team_packet_template_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-EXTERNAL-RED-TEAM-PACKET-TEMPLATE-V1` | `b73c3750a4cf82a7b021a574964ee808e05b3a6eb460e25fd42ea3d593c23f4a` | Prior packet structure and non-authority warning. |
| `research_control/tasks/RT-20260705-023/artifacts/negative_result_integration_selector_v16.md` | `MD-RESEARCH-CONTROL-TASKS-RT-20260705-023-NEGATIVE-RESULT-INTEGRATION-SELECTOR-V16` | `b3315b843e9f63f3de12ed54a1451b3a114ed1f9c97715f4a70341387c9ac501` | Certificate-gap witness selected for later red-team reuse. |
| `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex` | `TEX-V15-P2-T03-NARROW-SOURCE-SIDE-MATTER-SEMANTICS-EQUIVALENCE-THEOREM` | `aca8af857f2a53bfcbdd775b147323dab9e8a814ec78409faace45eef61bc04b` | Conditional `NarrowMSCertEq_v1` theorem statement and premises. |
| `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | `TEX-V15-P2-T05-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-REFUTER-STRESS` | `1be7ba5ac04095d7582612e0831fadcc55e58be0938ab25f2c7b7705da541182` | Certificate-gap witness and fail-closed stress branches. |
| `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex` | `TEX-V15-P3-T01-SOURCE-CERTIFICATE-ALGEBRA-PRIMITIVES` | `43d20536f39682c42743739715534096c06d5e445ae269378bab9db95e73fa1e` | Certificate vocabulary, valid-record shape, and invalid branches. |
| `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | `TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS` | `2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986` | Conditional operation laws and target-import invalidity lemma. |
| `research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex` | `TEX-V16-P5-T01-EQMS-DEFINITION-THEOREM-CONTENT-SEPARATION-AUDIT` | `07883e3d0fcf891ecac629e2bc60d2c80c2a63881b5d2b3c2fa59188708bcf9b` | Definition/theorem-content separation and missing theorem obligations. |
| `research_control/design/semantic_layer_separation_control_note.md` | `MD-RESEARCH-CONTROL-DESIGN-SEMANTIC-LAYER-SEPARATION-CONTROL-NOTE` | `204e0b4a5d1ead0a86353676fff709eef7988bfefe89a17a4147d36265a50d85` | Separation between source semantics, detector semantics, and stress-energy/action semantics. |
| `research_control/design/matter_coupling_dependency_dag_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-V1` | `8cca047480ae21c3b0641a5221277ae43cd5fdf1eb688a9080a168e27b1e98c3` | Navigational blocked-overread context for matter-coupling dependencies. |

## Project Claim Boundary

Allowed review conclusions:

- accept the selected claim only as scoped source-side evidence or
  precondition-status, if the source artifacts support that reading;
- classify part of the theorem as definition unfolding under explicit valid
  certificates;
- identify nontrivial content in certificate existence, certificate operation
  laws, finite/local instances, fail-closed branches, or explicit obstruction
  records;
- require repair, formalization, Refuter stress, Smuggling Auditor review, or a
  bounded integration selector.

Forbidden conclusions:

- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem status;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor construction, or matter action;
- Einstein-equation derivation;
- benchmark promotion or closure;
- Gate Chair verdict;
- completed derivation;
- any unscoped conclusion that closes future source-extension continuation.

## Strongest Allowed Positive Reading

The strongest allowed positive reading is narrow:

`NarrowMSCertEq_v1` may be read as scoped evidence-status for a conditional
source-side theorem role under explicit valid source certificates. Under that
reading, the positive branch may be mostly definition unfolding after valid
certificate premises are supplied, while the nontrivial source-side burden
resides in certificate validity, existence, operation laws, compatible
composition, finite/local certificate instances, and fail-closed obstruction
handling.

This reading does not derive physical matter semantics, detector semantics,
matter coupling, stress-energy, a matter action, Einstein equations, benchmark
recovery, or completed GR derivation.

## Strongest Forbidden Overreads

The reviewer should explicitly look for these overreads:

| Overread | Why forbidden |
| --- | --- |
| Definition unfolding is treated as a new theorem discharging matter coupling. | The P5 audit classifies theorem content under explicit premises and leaves downstream burdens open. |
| Valid source certificate language is treated as detector equivalence or empirical readout. | Detector semantics are a separate blocked layer. |
| Target metric, target topology, proper time, or benchmark behavior is used as a premise. | The selected question is source-side and must not import target-side structure. |
| No-target hygiene is treated as positive matter theory. | Negative import-prevention guards do not construct matter semantics. |
| Validator, role, handoff, registry, approval, generated derivative, local cache, or commit status is treated as proof authority. | Project-control evidence is routing and provenance support only. |
| A scoped negative result is treated as global rejection or future impossibility. | Only scoped obstruction or blocked-adoption/open-continuation language is authorized. |

## Reviewer Tasks

The reviewer should perform these tasks in order:

1. Restate the selected question in their own words.
2. Inspect the exact source artifacts listed in this packet.
3. Identify the strongest valid source-scoped positive reading.
4. Mark which steps are definition unfolding under supplied certificates.
5. Mark which steps are nontrivial mathematical content, if any.
6. Test for hidden target-side, detector-side, empirical, stress-energy,
   process-authority, or generated-derivative imports.
7. Provide the smallest missing premise, counterexample, or hidden import if
   the strongest reading fails.
8. Select exactly one recommendation from the allowed recommendation list.
9. Name the next integration route if repair or follow-up is required.

## Expected Output Template

Reviewer output should use this structure:

```yaml
reviewer_name_or_anonymous_id:
review_date:
reviewed_artifacts:
selected_question:
strongest_valid_reading:
strongest_overread_risk:
hidden_imports_detected:
smallest_counterexample_or_missing_premise:
recommendation:
  - accept_scoped_status
  - repair_required
  - reject_current_claim
  - request_formalization
  - route_refuter_stress
  - route_smuggling_audit
review_confidence:
notes:
```

Recommended optional fields:

```yaml
definition_unfolding_assessment:
nontrivial_content_assessment:
forbidden_overread_risks:
integration_route:
claim_boundary_warning_acknowledged: true
```

## Reviewer Scoring Rubric

| Score | Meaning | Decision consequence |
| --- | --- | --- |
| `0` | Unsupported or hidden-import dependent. | Route to repair, Refuter stress, or Smuggling Auditor review. |
| `1` | Mostly definition unfolding with important missing premise. | Request formalization or precise repair before any stronger route. |
| `2` | Scoped positive reading survives, but only as conditional source-side evidence. | Accept scoped status and preserve downstream blocks. |
| `3` | Strong scoped reading plus clear nontrivial source-side content. | Accept scoped status and name the next formalization or stress route; no adoption follows automatically. |

Rubric dimensions:

- source artifact coverage;
- definition/theorem-content separation;
- hidden-import detection;
- smallest missing premise or counterexample quality;
- claim-boundary discipline;
- integration-route specificity.

## Conflict-Of-Interest Note

Reviewers should disclose direct authorship of any reviewed artifact, prior
approval or Gate Chair authority over the claim, financial interest, personal
stake, dependency on a favorable result, or prior role in selecting the packet.
A conflict does not automatically invalidate a review, but the integration
route must record it and decide whether independent review is still needed.

## Findings Integration

This packet does not integrate findings by itself. Findings must enter tracked
research-control state through a later bounded task.

Default integration route:

1. run `P13-T03` as an internal one-question red-team pilot;
2. classify the finding as `accept_scoped_status`, `repair_required`,
   `reject_current_claim`, `request_formalization`, `route_refuter_stress`, or
   `route_smuggling_audit`;
3. create one completion record and one handoff selecting the next bounded
   route;
4. preserve all blocked downstream claims unless a later protected gate
   explicitly changes them.

Human outreach route:

- Hold for separate human outreach only if the Director or user explicitly
  selects external circulation after this packet. The present task performs no
  outreach and implies no reviewer contact.

## Non-Authority Warning

This packet is advisory infrastructure only. Writing it, sending it, receiving
comments, or citing a reviewer response does not adopt ontology, source laws,
matter semantics, detector semantics, coupling laws, matter coupling,
`MetricData(E)`, `g_eff` scope expansion, stress-energy semantics, a matter
action, Einstein equations, benchmark promotion, Gate Chair closure, completed
derivation, future source-extension impossibility, or program-wide rejection.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v16* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v16.md`

The AEther-Flow Research Project. (2026b). *One-question red-team question
selector v16* [Research-control artifact].
`research_control/tasks/RT-20260705-027/artifacts/one_question_red_team_question_selector_v16.md`

The AEther-Flow Research Project. (2026c). *External red-team packet template
v1* [Control template].
`research_control/design/external_red_team_packet_template_v1.md`

The AEther-Flow Research Project. (2026d). *Narrow source-side
matter-semantics equivalence theorem attempt v1* [Research-control TeX
artifact].
`research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex`

The AEther-Flow Research Project. (2026e). *Source certificate operation laws
and fail-closed lemma v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`

The AEther-Flow Research Project. (2026f). *EqMS definition/theorem-content
separation audit v16* [Research-control TeX artifact].
`research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex`
