<!-- authority: control -->

# Frontier Theorem Inventory Schema v1

## Purpose

This control note defines the schema for a future canonical frontier theorem
inventory. It is a P2-T01 schema artifact only. It does not populate the full
inventory, does not state new theorem content, and does not promote any
ontology, source law, `MetricData(E)`, `g_eff`, matter-coupling,
stress-energy, Einstein-equation, benchmark, Gate Chair, or
completed-derivation claim.

The inventory exists to make the current theorem-like frontier externally
reviewable. Each row or item must say what the project has, what it does not
have, what source artifact supports the statement, what may be reused, and what
must not be overread into downstream GR recovery.

## Authority Model

The inventory is a compact source-backed control surface. It is not independent
scientific authority.

Source priority for an inventory item:

1. Registered TeX artifacts for physics statements, Gate Chair decisions,
   Refuter stress tests, and mathematical objects.
2. Registered control Markdown for control schemas, burden maps, current task
   routing, and implementation-plan status.
3. Registry rows for routing, provenance, generated-output tracking, and
   ledger state.
4. Generated current-frontier snapshots, generated wiki notes, generated graph
   files, PDFs, semantic extracts, Obsidian notes, and `.local` caches only as
   retrieval or reader aids paired with canonical sources.

An inventory item may cite `research_control/current_frontier.md` only as a
generated summary pointer. The item must still include a canonical
`source_artifact_path` or registry row. The current-frontier snapshot must not
be used as status authority by itself.

## Item Classes

`frontier_item_class` is recommended even though the P2 plan lists only the
required fields below. It gives validators and reviewers a direct way to check
that the schema distinguishes the objects P2 must distinguish.

Allowed initial classes:

- `theorem`: a theorem or theorem candidate with stated assumptions and a
  mathematical conclusion.
- `definition`: a definition-only or draft/control object.
- `witness`: a constructive, finite, local, or parameterized witness object.
- `obstruction`: a scoped obstruction, countermodel, missing-primitive result,
  or no-go result under declared assumptions.
- `gate_decision`: a human-gated or Gate Chair decision record.
- `source_extension_evidence`: source-extension data, source-extension law,
  selector data, metric-form data, or parameterized-witness evidence accepted
  only inside a declared scope.
- `accepted_scoped_object`: a scoped source-only or scoped source-extension
  object accepted under explicit non-conclusion guards.
- `frozen_negative_route`: a local frozen route that preserves its exact scope
  and does not imply global theory rejection.
- `missing_theorem`: an absent theorem, primitive, selector, discriminator, or
  derivation-critical source-side law.

An item may list more than one class when needed, for example
`gate_decision;accepted_scoped_object`.

## Required Fields

Every inventory item must contain these fields.

| Field | Required content |
| --- | --- |
| `frontier_item_id` | Stable lowercase identifier, preferably aligned with ledger burden IDs or object names. |
| `object_or_claim_name` | Human-readable name of the object, theorem-like claim, obstruction, gate decision, or missing primitive. |
| `status_layer_summary` | Compact copy or summary of the control, mathematical, physical, promotion, and overread-guard layers when a Distance-to-GR row applies. |
| `source_artifact_path` | Canonical source file or registry row path. Generated summaries are insufficient without a paired canonical source. |
| `source_authority_type` | Controlled source type, such as `registered_tex_artifact`, `registered_markdown_control`, `distance_to_gr_ledger_row`, `claim_boundary_registry_row`, `gate_chair_artifact`, `refuter_artifact`, or `generated_summary_paired_with_source`. |
| `assumptions` | Explicit assumptions, hypotheses, scope restrictions, source-extension inputs, or known absence of assumptions. |
| `definitions_used` | Definitions, named primitives, candidates, laws, or source-side objects used by the item. |
| `statement_or_decision` | The theorem statement, decision, obstruction statement, frozen-route statement, or missing-theorem statement. |
| `mathematical_conclusion` | What follows mathematically under the assumptions. Use `none_supplied` when the item records a missing theorem or open burden. |
| `physical_non_conclusions` | Required blocked physical readings, including downstream GR, matter coupling, stress-energy, Einstein equations, benchmark promotion, or completed derivation when applicable. |
| `allowed_reuse` | How later packets may reuse the item without promotion. |
| `blocked_reuse` | Reuses that would launder the item into a stronger claim or protected authority. |
| `dependency_items` | Upstream frontier item IDs, ledger rows, task IDs, or source artifacts needed to interpret the item. |
| `missing_theorem_or_primitive` | Missing theorem, primitive, selector, discriminator, source law, action, variation, or `none` if not applicable. |
| `candidate_next_task` | Bounded next task candidate, if one follows; otherwise `none`. |
| `overread_guard` | Semicolon-separated guard tokens aligned with P1 status layers. |
| `external_review_notes` | Short review-facing clarification of what an external reviewer should check or should not infer. |

## Status Layer Summary

When an item is linked to `registries/DISTANCE_TO_GR_LEDGER.csv`,
`status_layer_summary` should include these subfields:

- `control_status`
- `mathematical_status`
- `physical_status`
- `promotion_status`
- `overread_guard`

The stored values should copy the ledger when the inventory item represents a
ledger row. If the item is not a ledger row, the item should still use the same
conceptual split: governance state, mathematical object state, physical
interpretation boundary, protected promotion state, and machine-checkable
overread guard.

## Overread Guard Rule

The `overread_guard` field should use semicolon-separated lowercase tokens.
Initial tokens are inherited from the P1 layered status design and ledger
migration:

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

High-risk items must include the relevant explicit non-conclusions in both
`physical_non_conclusions` and `overread_guard`. This duplication is
intentional: the first field is review-facing prose, and the second is
machine-checkable.

## Source Authority Types

Allowed initial `source_authority_type` values:

- `registered_tex_artifact`: a registered TeX source artifact.
- `gate_chair_artifact`: a registered TeX artifact whose role is a Gate Chair
  decision.
- `refuter_artifact`: a registered TeX artifact whose role is a Refuter stress
  test.
- `registered_markdown_control`: a registered Markdown control source.
- `distance_to_gr_ledger_row`: a row in `registries/DISTANCE_TO_GR_LEDGER.csv`.
- `claim_boundary_registry_row`: a row in
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- `research_task_registry_row`: a row in
  `registries/RESEARCH_TASK_REGISTRY.csv`.
- `generated_summary_paired_with_source`: a generated reader or retrieval
  surface cited only alongside canonical source evidence.

If an item needs a generated derivative for navigation, list that derivative in
`external_review_notes` or a separate optional navigation field. Do not put it
in `source_artifact_path` unless it is paired with the canonical source.

## Representability Checks

This table is not the populated inventory. It proves that the schema can
represent the required frontier cases without promoting them.

| Case | Recommended class | Required source basis | Required non-conclusion guards |
| --- | --- | --- | --- |
| `Resp_lc` source-extension data | `source_extension_evidence;accepted_scoped_object` | `research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex`; `registries/DISTANCE_TO_GR_LEDGER.csv` row `resp_lc` | no canonical ontology edit; no matter-coupling derivation; no detector semantics; no Einstein equations; no benchmark promotion; no completed derivation |
| `M_src` scoped source-only object | `gate_decision;accepted_scoped_object` | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex`; ledger row `m_src` | no `MetricData(E)` adoption; no `g_eff` scope expansion; no matter-coupling derivation; no Einstein equations; no benchmark promotion; no completed derivation |
| `g_eff` scoped source-extension object | `gate_decision;accepted_scoped_object` | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex`; ledger row `g_eff` | no source-law adoption; no `MetricData(E)` adoption; no unscoped `g_eff` adoption; no matter-coupling derivation; no Einstein equations; no benchmark promotion; no completed derivation |
| Matter-coupling precondition evidence | `source_extension_evidence;witness` | `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex`; ledger row `matter_coupling` | no source-law adoption; no `MetricData(E)` adoption; no `g_eff` scope expansion; no coupling-law adoption; no matter-coupling derivation or adoption; no stress-energy semantics; no stress-energy tensor; no matter action; no detector semantics; no Einstein equations; no benchmark promotion; no completed derivation |
| Finite toy metric-response frozen negative | `obstruction;frozen_negative_route` | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`; ledger row `finite_toy_metric_response` | no `g_eff` scope expansion; no matter-coupling derivation; no Einstein equations; no benchmark promotion; no completed derivation; no global theory rejection; no future source-extension impossibility |
| Open Einstein-equation burden | `missing_theorem` | `research_control/design/gr_derivation_burden_map.md`; ledger row `einstein_equations` | no Einstein equations; no benchmark promotion; no completed derivation |

## Inventory Item Template

Future populated inventory entries may use Markdown, YAML, or CSV, but the
semantic shape must match this template.

```yaml
frontier_item_id: ""
frontier_item_class: ""
object_or_claim_name: ""
status_layer_summary:
  control_status: ""
  mathematical_status: ""
  physical_status: ""
  promotion_status: ""
  overread_guard: ""
source_artifact_path: ""
source_authority_type: ""
assumptions: []
definitions_used: []
statement_or_decision: ""
mathematical_conclusion: ""
physical_non_conclusions: []
allowed_reuse: []
blocked_reuse: []
dependency_items: []
missing_theorem_or_primitive: ""
candidate_next_task: ""
overread_guard: ""
external_review_notes: ""
```

If CSV is used, list array fields as semicolon-separated values and keep the
top-level `overread_guard` semicolon-separated. If Markdown is used, each item
must still expose the field names exactly so a future validator can parse or
lint them.

## Validator Forward Contract

P2-T04 should add or extend a validator to check at least:

1. The populated inventory source exists and is registered.
2. Every item includes all required fields.
3. `frontier_item_class` uses the controlled item classes above.
4. `source_artifact_path` points to a canonical source or registry row.
5. Generated derivatives are not used as independent authority.
6. `assumptions`, `definitions_used`, `statement_or_decision`,
   `mathematical_conclusion`, and `missing_theorem_or_primitive` are nonblank
   or explicitly `none` where appropriate.
7. `physical_non_conclusions` is nonblank for every physics-adjacent item.
8. Items containing `matter`, `coupling`, `stress-energy`, `Einstein`,
   `benchmark`, `g_eff`, `MetricData`, or frozen-route language include
   explicit overread guards.
9. Frozen negative items distinguish local route freeze from global theory
   rejection and future source-extension impossibility.
10. Gate decision items do not imply benchmark Gate Chair closure unless the
    cited artifact actually supplies that protected verdict.

## Completion Boundary

P2-T01 is complete when this schema is registered, regenerated into retrieval
surfaces, and validated as a control design artifact. This completion does not
populate the inventory and does not alter the Distance-to-GR ledger. It does
not adopt new theorem statements, source laws, source-extension data, scoped
objects, `MetricData(E)`, unscoped `g_eff`, matter coupling, stress-energy
semantics, Einstein equations, benchmark promotion, Gate Chair closure, or a
completed derivation.

## APA 7 Source Materials

The AEther-Flow Research Project. (2026, June 18). *Resp_lc source-extension
human-gate adoption decision* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 18). *Resp_lc finite toy
metric-response model Refuter stress test* [Internal research-control TeX
artifact].

The AEther-Flow Research Project. (2026, June 24). *Gate Chair review of the
integrated source-only M_src adoption theorem candidate* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 27). *Gate Chair review of
scoped g_eff adoption status* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 28). *Gate Chair review of
scoped parameterized finite/local witness evidence* [Internal research-control
TeX artifact].

The AEther-Flow Research Project. (2026, June 29). *Distance-to-GR layered
status migration report* [Internal control artifact].

The AEther-Flow Research Project. (2026, June 29). *Distance-to-GR status
layers v1* [Internal control design note].

The AEther-Flow Research Project. (2026, June 29). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 29). *Recommendations
implementation plan continue task v12* [Internal implementation plan].
