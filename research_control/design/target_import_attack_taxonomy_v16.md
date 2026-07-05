<!-- authority: control -->

# Target-Import Attack Taxonomy v16

## Status

This artifact implements v16 P14-T01. It is a project-control taxonomy for
adversarial target-import tests. It is not a theorem, not a source-law
adoption, not matter-semantics adoption, not detector-semantics adoption, not
coupling-law adoption, not matter-coupling derivation or adoption, not
stress-energy semantics, not a matter action, not Einstein equations, not
benchmark promotion, not proof authority, and not a completed derivation.

The taxonomy is support evidence for later fixture and validator packets. It
does not execute the fixture suite and does not change validator behavior.

## Operating Rule

A target-import attack is any statement, proof step, certificate field,
fixture, validator result, registry row, generated derivative, handoff, role,
or scoped-evidence status that is reused as a source-side mathematical
premise without an explicit tracked source-side object and claim boundary.

Every attack below must fail closed. A fail-closed response means:

1. mark the proof, certificate, fixture, or claim as invalid under the stated
   source-side scope;
2. preserve downstream blocks for detector semantics, stress-energy,
   matter action, matter coupling, Einstein equations, benchmark promotion,
   and completed derivation; and
3. route to a bounded repair, fixture, linter, smuggling-audit, Refuter, or
   selector packet rather than silently continuing.

## Source Rejection Surfaces

| Source ID | Path | Registry object | Use in this taxonomy |
| --- | --- | --- | --- |
| `src_no_target_map` | `research_control/design/no_target_import_guard_map.md` | `MD-RESEARCH-CONTROL-DESIGN-NO-TARGET-IMPORT-GUARD-MAP` | Defines target topology, target atlas, target metric, benchmark, generated derivative, registry, validator, role, handoff, and file-order laundering guards. |
| `src_semantic_layers` | `research_control/design/semantic_layer_separation_control_note.md` | `MD-RESEARCH-CONTROL-DESIGN-SEMANTIC-LAYER-SEPARATION-CONTROL-NOTE` | Separates source-side matter semantics, detector semantics, and stress-energy/action semantics. |
| `src_matter_dag` | `research_control/design/matter_coupling_dependency_dag_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-V1` | Names blocked matter-coupling, detector, stress-energy, action, Einstein-equation, and benchmark burdens. |
| `src_certificate_schema` | `research_control/design/source_certificate_instance_library_schema_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-SOURCE-CERTIFICATE-INSTANCE-LIBRARY-SCHEMA-V1` | Requires no-target guard fields and fail-closed certificate status discipline. |
| `src_certificate_index` | `research_control/design/source_certificate_instance_library_index_v1.md` | `MD-RESEARCH-CONTROL-DESIGN-SOURCE-CERTIFICATE-INSTANCE-LIBRARY-INDEX-V1` | Records existing negative certificate examples for target metric, detector semantics, stress-energy, validator, and scoped-evidence overread. |
| `src_claim_linter_taxonomy` | `research_control/design/claim_language_linter_taxonomy.yaml` | `MD-RESEARCH-CONTROL-DESIGN-CLAIM-LANGUAGE-LINTER-TAXONOMY` | Provides current wording classes and fixture-context discipline for later validator integration. |
| `src_eqms_audit` | `research_control/tasks/RT-20260705-004/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex` | `TEX-V16-P5-T01-EQMS-DEFINITION-THEOREM-CONTENT-SEPARATION-AUDIT` | Separates definition unfolding from theorem content and downstream physical claims. |
| `src_red_team_pilot` | `research_control/tasks/RT-20260705-029/artifacts/internal_one_question_red_team_pilot_v16.md` | `MD-RESEARCH-CONTROL-TASKS-RT-20260705-029-INTERNAL-ONE-QUESTION-RED-TEAM-PILOT-V16` | Confirms scoped status only and routes to this attack taxonomy. |

Generated wiki notes, Obsidian notes, semantic extracts, SQLite indexes,
PDFs, rendered graphs, validator output, git commits, and local cache
freshness are retrieval or operational surfaces only. They cannot serve as
scientific authority.

## Attack Classes

| Attack ID | Forbidden import | Typical smuggled premise | Expected fail-closed response | Rejection surface |
| --- | --- | --- | --- | --- |
| `TIA-TARGET-METRIC` | target metric import | Treating a target Lorentzian metric, `g_eff`, or metric resemblance as a source certificate. | Reject as target-metric import; require an explicit source-side certificate record and preserve `g_eff` and matter-coupling blocks. | `src_no_target_map`; `src_matter_dag`; `src_certificate_schema` |
| `TIA-LORENTZIAN-SIGNATURE` | Lorentzian signature import | Treating signature `(-,+,+,+)` or any Lorentzian signature declaration as source-side validity. | Reject as target-metric/signature import; do not infer source validity, `MetricData(E)`, or `g_eff`. | `src_no_target_map`; `src_eqms_audit` |
| `TIA-TARGET-TOPOLOGY-ATLAS` | target topology or atlas import | Using target open sets, charts, differentiability, or atlas compatibility as source topology/regularity. | Reject as target topology/atlas import; route to source-side topology or chart-support construction if needed. | `src_no_target_map`; `src_matter_dag` |
| `TIA-PROPER-TIME` | proper-time import | Using clock time, proper time, or timelike interval language as a source readout. | Reject as target metric or empirical observer import; require source-side response/readout tokens under tracked scope. | `src_no_target_map`; `src_semantic_layers` |
| `TIA-DETECTOR-CALIBRATION` | detector calibration import | Treating detector calibration constants, measurement settings, or empirical protocol as a source label. | Reject as detector-semantics import; preserve detector semantics as blocked unless separately derived or authorized. | `src_semantic_layers`; `src_matter_dag`; `src_certificate_index` |
| `TIA-EMPIRICAL-READOUT` | empirical readout import | Treating observations, readouts, or measurement outcomes as source-object equivalence data. | Reject as empirical observer import; distinguish source readout tokens from detector semantics. | `src_no_target_map`; `src_semantic_layers` |
| `TIA-STRESS-ENERGY-SHORTCUT` | stress-energy tensor shortcut | Using stress-energy tensor notation or conservation as a source proof of matter semantics. | Reject as stress-energy shortcut; preserve stress-energy semantics and tensor construction as blocked downstream burdens. | `src_semantic_layers`; `src_matter_dag`; `src_certificate_index` |
| `TIA-MATTER-ACTION-SHORTCUT` | matter action shortcut | Using a matter action, Lagrangian, or variational principle as a source-side coupling proof. | Reject as matter-action shortcut; route only to a future action/dynamics target if authorized. | `src_semantic_layers`; `src_matter_dag` |
| `TIA-EINSTEIN-PREMISE` | Einstein-equation premise shortcut | Using Einstein equations, field-equation form, or GR recovery as an upstream source premise. | Reject as Einstein-equation premise import; preserve Einstein-equation work as downstream and blocked. | `src_matter_dag`; `src_claim_linter_taxonomy` |
| `TIA-BENCHMARK-FIT` | benchmark fit shortcut | Treating agreement with exact-GR benchmarks or known physics as source evidence. | Reject as benchmark-success import; require source-side derivation before benchmark promotion can even be considered. | `src_no_target_map`; `src_matter_dag` |
| `TIA-GATE-PROCESS-PROOF` | Gate Chair or process authority as proof | Treating Gate Chair status, role identity, DDRs, AgentJobs, handoffs, approvals, commits, or recency as mathematical proof. | Reject as process-authority laundering; cite process surface only for authority scope, not scientific content. | `src_no_target_map`; `src_claim_linter_taxonomy` |
| `TIA-VALIDATOR-PASS-PROOF` | validator PASS as proof | Treating linter, validator, unit-test, or checkpoint PASS as theorem evidence. | Reject as validator laundering; validators check structure and wording only. | `src_no_target_map`; `src_certificate_index` |
| `TIA-GENERATED-DERIVATIVE-PROOF` | generated derivative as proof | Treating wiki, PDF, HTML, Obsidian, semantic extract, graph, or local cache as independent authority. | Reject as generated-derivative authority; inspect canonical source and registry row instead. | `src_no_target_map` |
| `TIA-SCOPED-EVIDENCE-AS-ADOPTION` | scoped evidence as adoption | Treating scoped evidence/precondition status as source-law, matter-semantics, detector-semantics, or coupling-law adoption. | Reject as scope expansion; preserve exact scoped status and route to protected review only if the adopted object is explicitly requested. | `src_semantic_layers`; `src_matter_dag`; `src_red_team_pilot` |
| `TIA-FINITE-LOCAL-GLOBAL` | finite/local-to-global overread | Treating a finite/local witness or fixture as a universal matter-coupling theorem or completed derivation. | Reject as finite/local overread; record bounded fixture scope and require a separate general theorem or selector decision. | `src_certificate_schema`; `src_certificate_index`; `src_red_team_pilot` |

## Fail-Closed Response Matrix

| Attack family | Minimum receipt field | Allowed result values | Required next-route discipline |
| --- | --- | --- | --- |
| target geometry imports | `target_import_audit.target_geometry` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, route to source-side construction, fixture repair, or Refuter stress. |
| empirical or detector imports | `target_import_audit.detector_empirical` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, route to detector-semantics target-formalization or linter fixture. |
| stress-energy or action imports | `target_import_audit.stress_action` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, preserve stress/action burdens and route to future authorized target work only. |
| Einstein-equation or benchmark imports | `target_import_audit.downstream_gr` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, preserve downstream GR and benchmark blocks. |
| process-authority laundering | `target_import_audit.process_authority` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, inspect canonical source; do not use process metadata as proof. |
| finite/local scope overread | `target_import_audit.scope_overread` | `pass`, `fail_closed`, `blocked`, `not_applicable` | If failed, preserve finite/local scope and route to selector or general-theorem construction. |

The result `pass` is only an audit result under the stated text or fixture
scope. It does not prove source adequacy, matter coupling, Einstein equations,
benchmark recovery, or completed derivation.

## Fixture and Validator Implications

P14-T02 should use this taxonomy to build bad and good fixtures. Bad fixtures
should instantiate each required attack class. Good fixtures should preserve
source-side wording, scoped evidence/precondition wording, target-import
fail-closed wording, detector blocked wording, Einstein-equation blocked
wording, and benchmark protected wording.

P14-T03 may integrate this taxonomy into claim-language, smuggling-audit, or
research-control validation. P14-T03 should treat this artifact as a source of
test categories, not as proof that existing validators are complete.

## Machine-Readable Summary

```yaml
target_import_attack_taxonomy_v16:
  schema_id: "target_import_attack_taxonomy_v16"
  authority_status: "project_control"
  plan_task_id: "P14-T01"
  task_type: "target_import_attack_taxonomy_v16"
  physics_promotion_authorized: false
  proof_authority: false
  validator_behavior_changed: false
  attack_class_count: 15
  required_fail_closed: true
  next_plan_task: "P14-T02"
  next_artifact: "research_control/design/target_import_attack_fixture_catalog_v16.md"
  downstream_blocks_preserved:
    - "source-law adoption"
    - "matter-semantics adoption"
    - "detector-semantics adoption"
    - "coupling-law adoption"
    - "matter-coupling derivation or adoption"
    - "stress-energy semantics"
    - "matter action"
    - "Einstein equations"
    - "benchmark promotion"
    - "completed derivation"
```

## Source Materials

The AEther-Flow Research Project. (2026, June 23). *No-target-import guard map*
[Internal project-control design note].
`research_control/design/no_target_import_guard_map.md`

The AEther-Flow Research Project. (2026, July 2). *Semantic-layer separation
control note* [Internal project-control design note].
`research_control/design/semantic_layer_separation_control_note.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling dependency
DAG v1* [Internal project-control design note].
`research_control/design/matter_coupling_dependency_dag_v1.md`

The AEther-Flow Research Project. (2026, July 5). *Internal one-question
red-team pilot v16* [Internal research-control artifact].
`research_control/tasks/RT-20260705-029/artifacts/internal_one_question_red_team_pilot_v16.md`
