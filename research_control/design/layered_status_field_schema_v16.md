<!-- authority: control -->

# Layered Status Field Schema v16

## Purpose

This note defines future-facing authorization and status fields for
research-control task records, AgentJob completions, handoffs, and related
project-control summaries. It generalizes the earlier Distance-to-GR status
layer work from ledger rows to transaction records.

The schema is project-control only. It does not change canonical ontology,
scientific claims, source-law status, matter-coupling status,
Einstein-equation status, benchmark status, Gate Chair status, or completed
derivation status.

## Problem Statement

Historical records sometimes use broad fields such as
`physics_promotion_authorized: true`, `scientific_claims_changed: true`, or
`promotion_authority_path`. Those fields can be safe when read with nearby
claim-boundary context, but they are too broad for future records. A scoped
evidence-status change can be misread as downstream physics promotion if the
field does not name the exact layer being authorized.

P8-T02 therefore defines explicit authorization layers. Future packets should
prefer these fields over broad raw fields. Historical records remain
interpreted through their claim-boundary context unless a validator later
identifies a specific unsafe record.

## Required Field Model

Future high-risk research-control records should include this model whenever a
task can affect scientific, source-object, gate, or promotion-facing status:

```yaml
scoped_evidence_status_change_authorized: false
source_object_status_change_authorized: false
source_extension_object_status_change_authorized: false
source_law_adoption_authorized: false
matter_semantics_adoption_authorized: false
detector_semantics_adoption_authorized: false
coupling_law_adoption_authorized: false
matter_coupling_derivation_authorized: false
matter_coupling_adoption_authorized: false
stress_energy_semantics_authorized: false
matter_action_authorized: false
einstein_equation_derivation_authorized: false
benchmark_promotion_authorized: false
completed_derivation_authorized: false
downstream_physics_promotion_authorized: false
```

The default value is `false`. A field may be set to `true` only when the task
records the exact authority path, scope, and blocked downstream conclusions.

## Layer Definitions

| Field | Authorized layer | Required true-value evidence | Forbidden overread |
| --- | --- | --- | --- |
| `scoped_evidence_status_change_authorized` | A bounded evidence or precondition status may change. | Gate or control authority plus object and scope. | Source-law adoption, object adoption, matter coupling, benchmark promotion. |
| `source_object_status_change_authorized` | A source-side object status may change. | Object id, source-side scope, authority path. | Physical target manifold, metric, matter coupling, Einstein equations. |
| `source_extension_object_status_change_authorized` | A source-extension object may change status inside a bounded extension. | Extension name, bounded scope, approval path if protected. | Canonical ontology edit or unscoped downstream GR premise. |
| `source_law_adoption_authorized` | A source-side law may be adopted. | Protected authority path and exact law id. | Matter-sector adoption or benchmark promotion. |
| `matter_semantics_adoption_authorized` | Matter semantics may be adopted. | Protected authority path and exact semantics object. | Detector semantics, action principle, stress-energy tensor, Einstein equations. |
| `detector_semantics_adoption_authorized` | Detector semantics may be adopted. | Protected authority path and exact detector semantics object. | Matter action, stress-energy, Einstein equations. |
| `coupling_law_adoption_authorized` | A coupling law may be adopted. | Protected authority path and exact coupling law id. | Derived matter coupling unless separately authorized. |
| `matter_coupling_derivation_authorized` | A task may claim derivation progress for matter coupling. | Derivation target, assumptions, proof path, and authority. | Adoption or benchmark promotion. |
| `matter_coupling_adoption_authorized` | Matter coupling may be adopted as project status. | Protected authority path and exact adoption scope. | Einstein equations or benchmark promotion. |
| `stress_energy_semantics_authorized` | Stress-energy semantics may change. | Exact semantics target and authority path. | Tensor construction or matter action unless separately authorized. |
| `matter_action_authorized` | Matter action status may change. | Exact action target and authority path. | Einstein-equation derivation unless separately authorized. |
| `einstein_equation_derivation_authorized` | Einstein-equation derivation may be claimed. | Derivation artifact and authority path. | Benchmark promotion or completed derivation. |
| `benchmark_promotion_authorized` | Benchmark status may be promoted. | Protected benchmark authority path. | Completed derivation unless separately authorized. |
| `completed_derivation_authorized` | Completed derivation may be claimed. | Protected authority path and complete proof/benchmark basis. | Any broader claim outside the exact authorized derivation. |
| `downstream_physics_promotion_authorized` | Any downstream physical promotion may occur. | Exact layer map plus protected authority path. | Unspecified or implicit promotion. |

## Compatibility Rule

Historical fields must be interpreted through claim-boundary context. Do not
rewrite old records unless validators require remediation. Add alias or
renderer interpretation first.

Compatibility interpretation is:

1. `physics_promotion_authorized: false` remains a safe no-promotion summary.
2. `physics_promotion_authorized: true` is not sufficient by itself. Read it
   through `authorized_scope`, `promotion_authority_path`, the local claim
   boundary, and forbidden-conclusion summaries.
3. `scientific_claims_changed: true` means only that a scientific-facing field
   changed. It does not identify the layer until the surrounding record does.
4. Bare `accepted`, `adopted`, and `completed` must not be rendered without
   layer context in high-risk rows.
5. Generated wiki notes, renderer output, validator PASS, commits, and
   dependency graphs do not supply independent physics authority.

## Future Record Shape

Future high-risk completions should place layered fields under an
`authorization_layers` map:

```yaml
authorization_layers:
  scoped_evidence_status_change_authorized: false
  source_object_status_change_authorized: false
  source_extension_object_status_change_authorized: false
  source_law_adoption_authorized: false
  matter_semantics_adoption_authorized: false
  detector_semantics_adoption_authorized: false
  coupling_law_adoption_authorized: false
  matter_coupling_derivation_authorized: false
  matter_coupling_adoption_authorized: false
  stress_energy_semantics_authorized: false
  matter_action_authorized: false
  einstein_equation_derivation_authorized: false
  benchmark_promotion_authorized: false
  completed_derivation_authorized: false
  downstream_physics_promotion_authorized: false
  authority_scope: ""
  authority_source_path: ""
  blocked_downstream_claims: []
```

If any authorization field is `true`, `authority_scope`,
`authority_source_path`, and `blocked_downstream_claims` must be nonempty. The
blocked list must explicitly include every stronger layer that is not
authorized.

## Migration Guidance

Use additive migration only.

1. Leave historical raw fields in place.
2. Add renderer aliases before data rewrites.
3. Let validators warn on historical broad fields when adequate scope exists.
4. Fail future records that set a broad field to `true` without exact layered
   status and authority.
5. Do not infer adoption from `accepted`, validator PASS, generated artifacts,
   or route status.
6. Do not infer completed derivation from task, job, handoff, or checkpoint
   completion.

Recommended historical aliases:

| Historical phrase or field | Compatibility alias |
| --- | --- |
| `physics_promotion_authorized: true` with scoped source-extension approval | `scoped_evidence_status_change_authorized` or `source_extension_object_status_change_authorized` as indicated by the local record |
| `scientific_claims_changed: true` | Requires exact layer before future reuse |
| `Gate Chair accepted X only as scoped evidence/precondition` | `scoped_evidence_status_change_authorized` |
| `source-extension-law adoption` | `source_law_adoption_authorized` only for the named source law and no downstream GR layer |
| `status: "completed"` | `control_status: completed`; not completed derivation |
| `completed derivation` | `completed_derivation_authorized` only with explicit protected authority |

## Validator Requirements for P8-T03

P8-T03 should add future-facing checks:

1. Any future `physics_promotion_authorized: true` must also specify the exact
   layer and downstream status fields.
2. Scoped evidence-status changes must not set downstream promotion fields.
3. Gate Chair scoped evidence acceptance must not imply source-law adoption.
4. Bare `accepted` must not render for high-risk rows.
5. `scientific_claims_changed: true` must state which layer changed.
6. Historical safe contexts should warn at most unless a record lacks both
   scope and authority context.

## Acceptance Check

This schema distinguishes scoped evidence from downstream promotion and gives
future validators exact fields to enforce. It preserves historical records as
contextual control evidence and routes enforcement to P8-T03. No physics delta
is created.

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` [Internal project control plan].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260705-014/artifacts/risky_status_field_audit_v16.md` [Internal project-control audit].

The Aether-Flow Research Project. (2026). `research_control/design/distance_to_gr_status_layers_v1.md` [Internal project control schema note].
