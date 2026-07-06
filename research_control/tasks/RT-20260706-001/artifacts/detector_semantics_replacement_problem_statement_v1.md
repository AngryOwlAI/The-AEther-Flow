<!-- authority: control -->

# Detector-Semantics Replacement Problem Statement v1

## Control Status

```yaml
artifact_id: "detector_semantics_replacement_problem_statement_v1"
artifact_type: "detector_semantics_replacement_problem_statement"
task_id: "RT-20260706-001"
job_id: "AJ-RT-20260706-001-001"
role_id: "ontology-formalizer"
created_at: "2026-07-06T04:21:50Z"
plan_task_id: "P4-T01"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define the exact detector-semantics replacement burden for source-side coupling-law candidates."
selected_next_route: "constructive_replacement"
selected_next_plan_task_id: "P4-T02"
```

This artifact implements v17 P4-T01. It states the detector-semantics
replacement problem after accepted-status calibration. It does not adopt
detector semantics, does not adopt a source law, does not adopt a coupling law,
does not derive or adopt matter coupling, does not import stress-energy
semantics, does not construct a matter action, does not derive Einstein
equations, does not promote a benchmark, and does not claim a completed
derivation.

This artifact does not adopt detector semantics.

## 1. Question Defined

The P4 problem is:

```text
Given a source-side coupling-law candidate K_E whose detector component is
DetPlaceholder(E)=missing_and_blocked, what source-side object family could
replace the role normally played by detector semantics without importing an
empirical detector protocol, proper time, target metric, stress-energy
semantics, matter action, benchmark behavior, or validator/process authority?
```

The immediate output of P4-T01 is only this problem statement and route
selection. P4-T02 must attempt one constructive source-side replacement
candidate or record one scoped obstruction.

## 2. What Detector Semantics Would Normally Contribute

In an ordinary physical interpretation, detector semantics would normally
contribute at least five functions:

| Function | Ordinary contribution | P4 source-side replacement burden |
| --- | --- | --- |
| Readout domain | Identifies what counts as a detector event or reading. | Define a source-domain readout object using source records only. |
| Readout interface | Relates system state, interaction, and recorded outcome. | Define a source-side map or relation from source records to source readout tokens. |
| Calibration or normalization | Supplies scale, timing, or response standards. | Provide source-side normalization or explicitly fail closed without proper-time or target-metric import. |
| Equivalence of readings | Says when two readings count as the same relevant result. | Provide source-side certificates for readout equivalence, transport, restriction, or invariance. |
| Failure semantics | Distinguishes invalid, missing, malformed, or out-of-scope readings. | Define fail-closed branches for missing certificates, malformed readouts, target imports, or placeholder collapse. |

The source-side replacement is not a physical detector theory. It is a
controlled source-side interface and certificate burden sufficient for later
candidate, audit, stress, and selector packets.

## 3. Forbidden Target Or Empirical Imports

The replacement may not use the following as source premises:

- empirical detector protocol or measurement procedure;
- observed measurement outcome as a source object;
- detector calibration constants derived from empirical practice;
- target Lorentzian metric or metric signature;
- proper-time normalization;
- target atlas, target coordinate chart, or target smoothness assumption;
- stress-energy semantics or stress-energy tensor;
- matter action;
- Einstein equation;
- exact-GR benchmark fit or benchmark success;
- generated wiki, local cache, registry row, validator pass, role identity,
  handoff text, file order, checkpoint, or commit status as scientific proof.

If any of these appear in a candidate as a premise, the candidate must fail
closed or be routed to audit/repair rather than treated as detector semantics.

## 4. Source-Side Replacement Burden

The minimum source-side replacement target is:

```yaml
source_side_detector_replacement_burden:
  object_name: "SourceDetectorReplacement_v1(E)"
  required_fields:
    source_domain: "source records or finite/local source object family"
    readout_interface: "source-side relation or partial map from source records to source readout tokens"
    source_readout_tokens: "tokens internal to the declared source scope"
    certificate_family: "declared-scope preservation, equivalence, restriction, transport, or invariance certificates"
    fail_closed_rules: "missing, malformed, target-importing, or placeholder-collapsing branches fail closed"
    no_target_import_guard: true
    finite_local_witness: "one explicit finite/local instance or an obstruction"
  forbidden_premises:
    empirical_detector_protocol: true
    proper_time: true
    target_metric: true
    stress_energy_semantics: true
    matter_action: true
    benchmark_fit: true
```

In mathematical terms, a later constructive packet should attempt a finite or
local object of the form

```text
D_E^src = (Dom_D(E), Read_D(E), Cert_D(E), Fail_D(E))
```

where:

- `Dom_D(E)` is built from source records or source-side object families;
- `Read_D(E)` is a source-side readout relation or partial map;
- `Cert_D(E)` names the certificate family that preserves declared scope and
  rejects target imports;
- `Fail_D(E)` is the fail-closed branch structure.

No component may be justified by empirical detector behavior or target
spacetime structure.

## 5. Interaction With `DetPlaceholder(E)`

The existing `SourceCouplingLawCandidate_EStar_v1` uses:

```text
DetPlaceholder(E_*) = missing_and_blocked
```

P4 does not erase that boundary. It refines the lawful next question:

| Current placeholder state | P4-T01 interpretation | Later P4-T02 success condition |
| --- | --- | --- |
| `missing_and_blocked` | No detector semantics are available as a premise. | A source-side replacement candidate supplies `source_domain`, `readout_interface`, `certificate`, and finite/local witness fields. |
| `missing_and_blocked` | The placeholder is not a detector object. | Candidate remains `supplied_source_placeholder` rather than adopted detector semantics. |
| `missing_and_blocked` | The coupling-law candidate cannot derive matter coupling through detector overread. | Audit and stress must still check empirical protocol, proper time, target metric, and placeholder collapse. |

Thus the placeholder remains a block until a later packet either supplies a
source-side replacement candidate or records a precise obstruction.

## 6. Constructive Witness Floor

A constructive witness in P4-T02 must include:

```yaml
constructive_witness_floor:
  source_domain: "nonempty finite or local source-record domain"
  readout_interface: "explicit source-side map or relation"
  source_readout_tokens: "tokens not defined by empirical detector outcomes"
  certificate: "certificate family for declared scope and no-target preservation"
  fail_closed_rules: "missing or malformed data cannot silently pass"
  no_empirical_protocol_import: true
  no_proper_time_import: true
  no_target_metric_import: true
  finite_local_witness: "explicit example or finite/local instance"
```

A minimal positive example would be a finite source record family with a
source readout-token relation and certificate family that remains invariant
under declared source relabelings. The result would still be draft/control and
would not adopt detector semantics.

## 7. Scoped Obstruction Floor

If P4-T02 cannot construct the replacement, the obstruction must have this
shape:

```yaml
detector_replacement_obstruction:
  obstruction_id: "OB-V17-DET-<short-label>"
  exact_missing_burden: "the precise source-side field or law not supplied"
  scoped_to_current_route: true
  global_no_go_claimed: false
  current_ontology_implication: "current ontology does not derive the named burden"
  same_milestone_continuation_open: true
```

The obstruction may say that the current route lacks a required source-side
readout interface, certificate family, normalization rule, transition rule, or
robustness rule. It may not claim that future source extensions are impossible
unless a separate no-go theorem proves that stronger claim.

## 8. Ontology-Law Selector Condition

An ontology-law research packet is required only if P4-T02 or a later selector
finds a derivation-critical missing source-side law. Examples include:

- the current ontology does not derive any source-side readout-interface law;
- the current ontology does not derive a source-side readout-token equivalence
  or transport rule required by the matter-coupling milestone;
- the current ontology does not derive a discriminator between valid source
  readouts and empirical detector-protocol imports;
- the current ontology does not derive a robustness rule for finite/local
  readout perturbations.

Ordinary gaps do not qualify. Missing documentation, missing registry rows,
slow casework, awkward templates, missing citations, or computations available
under the existing ontology must not be promoted into an ontology-law route.

## 9. Route Selection

```yaml
p4_t01_route_selection:
  selected_route_class: "constructive_replacement"
  selected_next_plan_task_id: "P4-T02"
  selected_next_task_type: "detector_semantics_replacement_candidate_or_obstruction"
  selected_next_role_family: "candidate-constructor@0.2.0"
  obstruction_branch_preserved: true
  ontology_law_selector_deferred: true
  reason: "The problem statement identifies a constructive finite/local replacement floor and no present obstruction theorem or derivation-critical missing source-law selector has yet been established."
```

The logical next step is one bounded P4-T02 packet. It should attempt exactly
one source-side detector replacement candidate. If that attempt cannot meet
the constructive witness floor, it must record one precise scoped obstruction.

## 10. Non-Conclusions

This artifact does not authorize:

- detector-semantics adoption;
- source-law adoption;
- matter-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor construction;
- matter action;
- `MetricData(E)` adoption;
- `g_eff` scope expansion or physical metric use;
- Einstein-equation derivation;
- benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- future source-extension impossibility;
- program-wide no-go conclusion;
- generated derivative, validator, registry, role, handoff, approval, cache,
  checkpoint, commit, or current-frontier rendering as proof authority.

## Parent-Child Synthesis

```yaml
parent_child_synthesis:
  mode: "parent_child_parallel_synthesis"
  child_outputs:
    - "research_control/tasks/RT-20260706-001/artifacts/child_phys_math_detector_semantics_replacement_problem.yaml"
    - "research_control/tasks/RT-20260706-001/artifacts/child_phys_phil_detector_semantics_replacement_problem.yaml"
  conflict_review: "research_control/tasks/RT-20260706-001/artifacts/parent_conflict_review_detector_semantics_replacement_problem.yaml"
  fusion_notes: "research_control/tasks/RT-20260706-001/artifacts/parent_fusion_notes_detector_semantics_replacement_problem.md"
  unresolved_conflicts: []
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`

The AEther-Flow Research Project. (2026b). *Source-side coupling-law candidate
K_EStar v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260705-047/artifacts/source_side_coupling_law_candidate_v1.tex`

The AEther-Flow Research Project. (2026c). *Matter-coupling dependency DAG
v1* [Research-control design artifact].
`research_control/design/matter_coupling_dependency_dag_v1.md`

The AEther-Flow Research Project. (2026d). *No-target-import guard map*
[Research-control design artifact].
`research_control/design/no_target_import_guard_map.md`

The AEther-Flow Research Project. (2026e). *Accepted status calibration policy
v1* [Research-control design artifact].
`research_control/design/accepted_status_calibration_policy_v1.md`
