---
authority: control
task_id: "RT-20260705-014"
artifact_id: "risky_status_field_audit_v16"
status: "completed"
created_at: "2026-07-05T04:49:00Z"
---

# Risky Status-Field Audit v16

## Analysis

P8-T01 audited ambiguous field names before future schema layering. The audit
used a read-only aggregation over 7,138 tracked control files under task
records, completions, role records, handoffs, and selected registries.

The result is a compatibility finding, not a physics finding. Historical
records usually include nearby claim-boundary text that blocks downstream
overread. The risk is that future readers or validators can misread raw fields
such as `physics_promotion_authorized: true`, bare `accepted`, or `completed`
as downstream physics promotion without the surrounding scope.

## Count Summary

| Token or field | Matches | Main surfaces | Audit classification |
| --- | ---: | --- | --- |
| `physics_promotion_authorized` | 1510 | completions, handoffs, task records | `needs_schema_update`; historical false values are `safe_contextual_raw_field`; historical true values need `needs_alias_only` |
| `physics_promotion_authorized: true` | 62 | completions, task records, handoffs | `needs_schema_update`; `needs_linter_warning`; no immediate `unsafe_requires_remediation` found because examples carry scope and authority paths |
| `scientific_claims_changed` | 281 | task records, jobs, handoffs | false values are `safe_contextual_raw_field`; true values need `needs_schema_update` |
| `scientific_claims_changed: true` | 42 | task records, jobs, handoffs | `needs_schema_update`; future records should state the exact changed layer |
| `accepted` | 5485 | artifacts, completions, decisions, handoffs, registries | `needs_linter_warning`; high-risk reader-facing contexts need `needs_reader_facing_renderer_fix` unless scoped immediately |
| `adopted` | 2529 | artifacts, completions, handoffs, registries | `needs_schema_update`; source-extension use needs `needs_alias_only` to separate source-object status from downstream physics promotion |
| `promotion_authority_path` | 532 | completions, task records, artifacts | empty values are `safe_contextual_raw_field`; nonempty values need layer-specific schema fields |
| nonempty `promotion_authority_path` | 61 | completions, task records, handoffs | `needs_schema_update`; future records must bind authority path to exact scope |
| `source_extension_data_adopted` | 225 | handoffs, task records, artifacts, completions | `needs_alias_only`; future schema should replace the raw adopted wording with source-extension object status |
| `gate_review_completed` | 23 | artifacts, completions, decisions, task records | `needs_alias_only`; review completion must not imply benchmark or derivation closure |
| `Gate Chair accepted` | 228 | artifacts, registries, handoffs, task records | `needs_linter_warning`; reader-facing summaries should render scoped acceptance |
| `completed` | 20302 | registries, handoffs, completions, decisions, task records | control-status uses are `safe_contextual_raw_field`; phrase-level uses near derivation or benchmark need linter warnings |
| `downstream_physics_promotion_authorized` | 290 | completions, handoffs, jobs | `safe_contextual_raw_field`; keep as future explicit layer |
| `benchmark_promotion_authorized` | 402 | completions, handoffs, jobs | `safe_contextual_raw_field`; keep as future explicit layer |
| `completed_derivation_authorized` | 398 | completions, handoffs, jobs | `safe_contextual_raw_field`; keep as future explicit layer |

## Representative Evidence

| Evidence | Interpretation | Classification |
| --- | --- | --- |
| `research_control/tasks/RT-20260614-087/jobs/completions/AJC-AJ-RT-20260614-087-001.yaml` uses `physics_promotion_authorized: true` with `authorized_scope: "GSC_src source-extension-law adoption only"` and downstream blocks. | Historical scoped source-extension authorization. It is not downstream GR promotion. | `needs_alias_only`; `needs_schema_update` |
| `research_control/tasks/RT-20260614-269/00_TASK.yaml` uses `physics_promotion_authorized: true` and says Gate Chair accepted finite/local parameterized-witness evidence only. | Historical scoped evidence acceptance. The field name is too broad for future records. | `needs_schema_update`; `needs_linter_warning` |
| `research_control/tasks/RT-20260701-035/jobs/completions/AJC-AJ-RT-20260701-035-001.yaml` records `old_status: "accepted"` and `new_status: "accepted"` with `physics_promotion_authorized: false`. | Safe historical ledger status when read with surrounding no-promotion text. | `safe_contextual_raw_field`; `needs_reader_facing_renderer_fix` if rendered bare |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` and role registries contain many "Gate Chair accepted" snippets. | Registry text must remain scoped because CSV rows lack layered structure. | `needs_linter_warning`; `needs_alias_only` |
| Routine task/job/completion `status: "completed"` fields are common. | Control completion is not completed derivation. | `safe_contextual_raw_field`; future schemas should use explicit `control_status` |

## Classification by Risk Type

`safe_contextual_raw_field`:

- Routine control statuses such as `status: "completed"`.
- Explicit false authorization fields.
- Existing downstream-specific false fields such as
  `downstream_physics_promotion_authorized: false`.

`needs_alias_only`:

- Historical source-extension acceptance or adoption records that are already
  bounded by approvals and forbidden-conclusion summaries.
- `gate_review_completed` and `Gate Chair accepted` when the local text already
  says scoped evidence or precondition only.

`needs_schema_update`:

- Future use of `physics_promotion_authorized: true`.
- Future use of `scientific_claims_changed: true`.
- Future use of `promotion_authority_path` without a layer-specific authority
  target.
- Future source-extension adoption fields that do not separate source-object
  status from downstream physics promotion.

`needs_linter_warning`:

- Bare `accepted` in high-risk rows.
- Bare `adopted` near matter coupling, benchmark, Einstein-equation, or
  completed-derivation language.
- `Gate Chair accepted` when a sentence lacks immediate scoped acceptance
  language.

`needs_reader_facing_renderer_fix`:

- Any reader-facing rendering of `accepted`, `adopted`, or `completed` without
  nearby layer labels.
- Distance-to-GR rows or generated summaries that expose raw status without
  source-object, evidence, benchmark, and derivation layers.

`unsafe_requires_remediation`:

- None found in this bounded audit. The audit did not find a historical
  occurrence that both lacks claim-boundary context and changes physics status.

## Required Future Schema Work

P8-T02 should define explicit layered fields for scoped evidence status, source
object status, source-law adoption, matter-sector adoption, matter-coupling
derivation or adoption, benchmark promotion, completed derivation, and
downstream physics promotion.

P8-T03 should add future-facing validation rules:

- `physics_promotion_authorized: true` requires exact layer and scope.
- `scientific_claims_changed: true` requires exact layer.
- Scoped Gate Chair evidence acceptance must not imply source-law adoption.
- Bare high-risk `accepted` and `adopted` should warn or fail according to the
  schema context.
- Historical safe contexts should warn at most unless a record lacks both
  scope and authority.

## Conclusion

The logical next step is P8-T02. Define a layered status schema and compatibility
rule. Do not rewrite historical records unless a later validator identifies a
specific unsafe record with no scope or authority context.

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` [Internal project control plan].

The Aether-Flow Research Project. (2026). `research_control/design/scoped_positive_claim_vocabulary.md` [Internal project control vocabulary].

The Aether-Flow Research Project. (2026). `research_control/design/distance_to_gr_status_layers_v1.md` [Internal project control schema note].
