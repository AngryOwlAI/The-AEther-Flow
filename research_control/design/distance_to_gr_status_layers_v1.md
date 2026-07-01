<!-- authority: control -->

# Distance-to-GR Status Layers v1

## Purpose

This design note defines an additive status-layer taxonomy for
`registries/DISTANCE_TO_GR_LEDGER.csv`. It is a P1-T01 project-control design
artifact only. It does not change any ledger row, scientific status, ontology,
source law, `MetricData(E)` status, `g_eff` scope, matter-coupling status,
Einstein-equation status, benchmark status, Gate Chair status, or completed
derivation status.

## Problem Statement

The current Distance-to-GR ledger uses one `current_status` field for multiple
meanings. This is too coarse for rows such as `resp_lc`, `m_src`, `g_eff`, and
`matter_coupling`, where a protected control decision may accept a scoped
source object or scoped evidence while explicitly blocking downstream physical
readings.

The logical next step is an additive schema split. P1-T02 should preserve all
existing columns and add explicit layers so a row can say, for example:

- governance: scoped evidence accepted;
- mathematics: parameterized finite/local witness precondition exists;
- physics: not matter coupling, not stress energy, not Einstein equations;
- promotion: no downstream GR promotion;
- guard: no overread into blocked conclusions.

## Proposed Additive Columns

P1-T02 should append these columns after `current_status` or after the existing
ledger columns by a documented migration. The migration must preserve all
existing column names and cell values.

| Column | Meaning | Required |
| --- | --- | --- |
| `control_status` | Governance state of evidence, review, task completion, or row handling. | yes |
| `mathematical_status` | Mathematical object type actually supplied: theorem, witness, construction, countermodel, obstruction, source-extension object, or missing object. | yes |
| `physical_status` | Physical interpretation boundary, especially whether a GR-relevant physical burden remains blocked. | yes |
| `promotion_status` | Whether any protected authority promoted the claim beyond draft/control, scoped evidence, or scoped source object status. | yes |
| `overread_guard` | Semicolon-separated machine-checkable tokens naming conclusions that must not be drawn. | yes |

The existing `current_status` remains a legacy summary until downstream tools no
longer require it. It must not be interpreted as physical status by itself.

## Controlled Vocabulary

### `control_status`

- `not_started`
- `draft_control_object_exists`
- `construction_recorded`
- `audit_passed`
- `refuter_stress_passed`
- `gate_review_completed`
- `accepted_as_scoped_evidence`
- `accepted_as_scoped_source_object`
- `frozen_negative`
- `human_gated`
- `blocked`

### `mathematical_status`

- `no_mathematical_object`
- `definition_only`
- `conditional_theorem_candidate`
- `constructive_witness`
- `finite_local_witness`
- `parameterized_witness_precondition`
- `scoped_source_extension_object`
- `source_only_adopted_object`
- `countermodel`
- `scoped_obstruction`
- `general_theorem_missing`

### `physical_status`

- `no_physical_interpretation_authorized`
- `benchmark_compatible_interpretive_boundary_only`
- `not_matter_coupling`
- `not_stress_energy`
- `not_einstein_equations`
- `not_benchmark_promotion`
- `downstream_gr_blocked`
- `human_gate_required_before_physical_reading`

### `promotion_status`

- `none`
- `draft_control_only`
- `scoped_source_evidence_only`
- `scoped_source_object_only`
- `human_gate_required`
- `frozen_negative_no_promotion`
- `no_downstream_gr_promotion`

### `overread_guard`

`overread_guard` should be a semicolon-separated list of lowercase tokens.
Permitted initial tokens are:

- `no_canonical_ontology_edit`
- `no_source_law_adoption`
- `no_metricdata_e_adoption`
- `no_geff_scope_expansion`
- `no_unscoped_geff_adoption`
- `no_coupling_law_adoption`
- `no_matter_coupling_derivation`
- `no_matter_coupling_adoption`
- `no_stress_energy_semantics`
- `no_stress_energy_tensor`
- `no_matter_action`
- `no_detector_semantics`
- `no_einstein_equations`
- `no_benchmark_promotion`
- `no_benchmark_gate_chair_closure`
- `no_completed_derivation`
- `no_future_source_extension_impossibility`
- `no_global_theory_rejection`

Display renderers may translate these tokens back to project vocabulary such as
`no MetricData(E) adoption`, `no g_eff scope expansion`, and `no downstream GR
promotion`. The stored field should remain simple enough for validator checks.

## Migration Plan for Current Rows

This mapping is descriptive and additive. It does not change scientific
meaning. P1-T02 should apply it row-by-row and produce a migration report
showing the before/after meaning for every ledger row.

| burden_id | control_status | mathematical_status | physical_status | promotion_status | overread_guard |
| --- | --- | --- | --- | --- | --- |
| `source_ontology_primitives` | `draft_control_object_exists` | `definition_only` | `no_physical_interpretation_authorized` | `draft_control_only` | `no_canonical_ontology_edit;no_benchmark_promotion;no_completed_derivation` |
| `source_equivalence_eqsrc` | `draft_control_object_exists` | `general_theorem_missing` | `downstream_gr_blocked` | `draft_control_only` | `no_source_law_adoption;no_benchmark_promotion;no_completed_derivation` |
| `retain_h` | `blocked` | `general_theorem_missing` | `downstream_gr_blocked` | `none` | `no_source_law_adoption;no_benchmark_promotion;no_completed_derivation` |
| `gen_h` | `blocked` | `general_theorem_missing` | `downstream_gr_blocked` | `none` | `no_source_law_adoption;no_benchmark_promotion;no_completed_derivation` |
| `obsloc_lc` | `construction_recorded` | `constructive_witness` | `downstream_gr_blocked` | `draft_control_only` | `no_source_law_adoption;no_matter_coupling_derivation;no_benchmark_promotion;no_completed_derivation` |
| `resp_lc` | `accepted_as_scoped_source_object` | `scoped_source_extension_object` | `downstream_gr_blocked` | `scoped_source_object_only` | `no_canonical_ontology_edit;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation` |
| `m_src` | `accepted_as_scoped_source_object` | `source_only_adopted_object` | `downstream_gr_blocked` | `scoped_source_object_only` | `no_metricdata_e_adoption;no_geff_scope_expansion;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation` |
| `g_eff` | `accepted_as_scoped_source_object` | `scoped_source_extension_object` | `not_matter_coupling` | `scoped_source_object_only` | `no_source_law_adoption;no_metricdata_e_adoption;no_unscoped_geff_adoption;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation` |
| `matter_coupling` | `accepted_as_scoped_evidence` | `parameterized_witness_precondition` | `not_matter_coupling` | `scoped_source_evidence_only` | `no_source_law_adoption;no_metricdata_e_adoption;no_geff_scope_expansion;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_stress_energy_tensor;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation` |
| `einstein_equations` | `not_started` | `no_mathematical_object` | `not_einstein_equations` | `none` | `no_einstein_equations;no_benchmark_promotion;no_completed_derivation` |
| `finite_variation_robustness` | `refuter_stress_passed` | `conditional_theorem_candidate` | `downstream_gr_blocked` | `draft_control_only` | `no_source_law_adoption;no_matter_coupling_derivation;no_benchmark_promotion;no_completed_derivation` |
| `benchmark_promotion` | `blocked` | `general_theorem_missing` | `not_benchmark_promotion` | `none` | `no_benchmark_promotion;no_benchmark_gate_chair_closure;no_completed_derivation` |
| `gate_chair_status` | `human_gated` | `no_mathematical_object` | `human_gate_required_before_physical_reading` | `human_gate_required` | `no_benchmark_gate_chair_closure;no_benchmark_promotion;no_completed_derivation` |
| `finite_toy_metric_response` | `frozen_negative` | `scoped_obstruction` | `downstream_gr_blocked` | `frozen_negative_no_promotion` | `no_geff_scope_expansion;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_global_theory_rejection` |

## Row-Specific Reasoning

`matter_coupling` is the critical ambiguity. The current ledger says
`accepted`, but the evidence accepts only `ParamFiniteLocalWitness_v1(E)`,
`BridgeSlot_n(E)`, and `NoTargetImport_n(E)` as scoped source-extension
parameterized-witness evidence/precondition. The layered row must therefore
read as:

- `control_status`: `accepted_as_scoped_evidence`;
- `mathematical_status`: `parameterized_witness_precondition`;
- `physical_status`: `not_matter_coupling`;
- `promotion_status`: `scoped_source_evidence_only`;
- `overread_guard`: must include no source-law adoption, no coupling-law
  adoption, no matter-coupling derivation or adoption, no stress-energy
  semantics, no stress-energy tensor, no matter action, no detector semantics,
  no Einstein equations, no benchmark promotion, and no completed derivation.

`g_eff` is also not physical downstream GR. It may be represented as an adopted
scoped source-extension `g_eff` object only under its declared source-side
scope. Its physical layer must prevent overread into unscoped Lorentzian metric,
matter coupling, Einstein equations, benchmark recovery, or completed
derivation.

`M_src` is a scoped source-only adopted object under H1-H13 and fail-closed
discipline. Its physical layer must preserve that this is not a metric, not
matter coupling, not Einstein equations, not benchmark promotion, and not
ordinary GR recovery.

The finite toy metric-response row remains a local frozen negative for the
explicit-tag-only toy route. It is not a global theory rejection and not proof
of future source-extension impossibility.

## Validator Requirements for P1-T02 and P1-T03

P1-T02 migration should keep validation green by making schema and renderer
changes in the same bounded transaction if needed. P1-T03 should then harden
the validator. The required validator behavior is:

1. The ledger must contain all five new fields for every row.
2. Each field must be nonblank.
3. `control_status`, `mathematical_status`, `physical_status`, and
   `promotion_status` must use the controlled vocabularies above.
4. `overread_guard` must be semicolon-separated lowercase tokens from the
   allowed set.
5. `matter_coupling` must not have a physical status that can be read as matter
   coupling derivation, matter-coupling adoption, stress-energy semantics,
   stress-energy tensor construction, matter action import, detector semantics,
   Einstein equations, benchmark promotion, or completed derivation.
6. A row whose `current_status` is `accepted` but whose physical burden remains
   blocked must have `promotion_status` equal to `scoped_source_evidence_only`
   or `scoped_source_object_only`, and an `overread_guard` containing the
   relevant negations.
7. Rows with `promotion_status: human_gate_required` must point to protected
   authority evidence and must not imply the protected verdict already occurred.
8. Rows with `frozen_negative_no_promotion` must distinguish local route freeze
   from broad rejection of the theory.
9. `render_current_frontier.py` should display the layered fields for every row
   once the CSV migration lands, and should preserve the explicit
   matter-coupling boundary paragraph.
10. No validator, renderer, generated wiki note, local cache, graph, commit, or
   checker output may be treated as scientific proof.

## Acceptance Check

The table covers all current ledger rows. The mapping preserves the existing
scientific meaning while making the ambiguous cases machine-visible:

- `matter_coupling` no longer reads as physical matter-coupling derivation;
- `g_eff` remains a scoped source-extension object with downstream GR blocked;
- `M_src` remains a scoped source-only adopted object with no metric or GR
  derivation;
- the finite toy route remains locally frozen, not globally rejected.

## Next Packet

P1-T02 should implement the additive ledger schema migration using this design.
It should not alter historical scientific artifacts. It should produce a
migration report and update validators or renderers only as needed to keep the
existing tools parseable and claim boundaries explicit.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 18). *Resp_lc source-extension
human-gate adoption decision* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 18). *Resp_lc finite toy
metric-response model Refuter stress test* [Internal research-control TeX
artifact].

The AEther-Flow Research Project. (2026, June 24). *Gate Chair review of the
integrated source-only M_src adoption theorem candidate* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 27). *Gate Chair review of scoped
g_eff adoption status* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 28). *Gate Chair review of
scoped parameterized finite/local witness evidence* [Internal research-control
TeX artifact].
