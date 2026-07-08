<!-- authority: control -->

# Source Detector/Readout Candidate Setup v1

## Control Status

This artifact completes v18 P5-T03. It sets up exactly one bounded candidate
target for the later P5-T04 construction-or-obstruction packet.

It is not a constructed readout law, not detector-semantics adoption, not
matter-coupling derivation, not a Distance-to-GR ledger update, and not an
exact-GR benchmark result.

## Required Setup

```yaml
source_detector_readout_candidate_setup:
  candidate_name: "SourceReadoutCandidate_EStar_v1"
  source_domain: "SMScope(E_*)"
  readout_symbol: "Readout_src(E_*)"
  detector_symbol: "Det_src(E_*)"
  compatibility_target: "SourceCouplingLawCandidate_EStar_v1"
  finite_local_witness_required: true
  empirical_protocol_import_forbidden: true
  proper_time_import_forbidden: true
  target_metric_import_forbidden: true
  adoption_requested: false
```

## Branch Selection

```yaml
branch_selection:
  exactly_one_branch_named: true
  branch_type: "candidate_target"
  branch_name: "SourceReadoutCandidate_EStar_v1"
  obstruction_branch_named: false
  precise_obstruction_id: ""
  next_plan_task_id: "P5-T04"
```

The named branch is a candidate target only. It does not assert that
`Readout_src(E_*)` or `Det_src(E_*)` has already been constructed.

## Formal Envelope For P5-T04

P5-T04 must produce exactly one of the following:

- a source-side `SourceReadoutCandidate_EStar_v1` construction; or
- one precise scoped obstruction explaining why that construction fails under
  the current claim boundary.

A positive construction must stay inside `SMScope(E_*)` and define:

1. a source-side readable record family;
2. a source-side relation or partial map named `Readout_src(E_*)`;
3. a source-side record interface named `Det_src(E_*)`;
4. a certificate bundle or equivalent source-side check record;
5. a finite/local witness family;
6. a fail-closed rule for malformed, missing, ambiguous, or target-importing
   records; and
7. a compatibility statement with `SourceCouplingLawCandidate_EStar_v1` that
   does not treat that candidate as adopted.

## Import Guards

The P5-T04 construction must fail closed if it requires any of the following:

- empirical detector protocol authority;
- proper-time normalization;
- target metric structure;
- stress-energy semantics;
- stress-energy tensor construction;
- matter-action import;
- Einstein-equation premise;
- exact-GR benchmark behavior; or
- process or validation authority as physics authority.

## Distance-To-GR Effect

```yaml
distance_to_gr_delta:
  changed: false
  effect: "no_distance_delta"
  ledger_row_updated: false
  burden_id: "matter_coupling"
  rationale: "P5-T03 names a candidate target and construction envelope only; it does not construct or audit a readout law."
```

## Forbidden Conclusions

This setup does not establish:

- `Det_src` adoption;
- `Readout_src` adoption;
- detector-semantics adoption;
- source detector/readout semantics adoption;
- empirical detector protocol authority;
- proper-time normalization;
- target-metric authority;
- source-law adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- benchmark promotion;
- Gate Chair verdict;
- future source-extension impossibility;
- broad no-go conclusion; or
- completed derivation.

## Next Route

The next route is P5-T04: construct the source detector/readout candidate or
record one precise scoped obstruction.

## Source Materials

The Aether-Flow Research Project. (2026a). *Recommendations implementation
plan Continue Task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`

The Aether-Flow Research Project. (2026b). *Source detector/readout semantics
burden v1* [Internal control note].
`research_control/design/source_detector_readout_semantics_burden_v1.md`

The Aether-Flow Research Project. (2026c). *Source detector/readout DAG patch
proposal v1* [Internal task artifact].
`research_control/tasks/RT-20260708-008/artifacts/source_detector_readout_dag_patch_proposal_v1.md`
