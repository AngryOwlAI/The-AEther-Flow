<!-- authority: control -->

# Accepted Status Calibration Schema v1

## 1. Status

```yaml
schema_id: "accepted_status_calibration_schema_v1"
authority: "control"
status: "active"
created_at: "2026-07-06T01:33:43Z"
created_by_task_id: "RT-20260705-055"
created_by_job_id: "AJ-RT-20260705-055-001"
plan_task_id: "P3-T02"
physics_progress_status: "schema_update_no_physics_delta"
```

This schema defines the machine-readable status-calibration fields used by
`research_control/design/accepted_status_calibration_v1.yaml` and mirrored in
`research_control/design/distance_to_gr_status_aliases.yaml`.

It is a project-control schema. It is not a physics derivation, a Gate Chair
verdict, a source-law adoption, a matter-coupling result, an Einstein-equation
result, a benchmark decision, or proof authority.

## 2. Purpose

The schema implements the P3-T01 policy requirement that high-risk scoped
positive rows be reported in this sequence:

1. positive status;
2. exact scope;
3. blocked overread.

The schema also prevents the opposite failure mode: describing a scoped
positive or accepted evidence/precondition row as if it were "basically
nothing."

## 3. Root Object

The root YAML object is:

```yaml
accepted_status_calibration_v1:
  high_risk_objects:
    <object_id>:
      object_id: string
      ledger_burden_id: string
      status_family: string
      positive_status_sentence: string
      exact_scope_sentence: string
      allowed_use_sentence: string
      blocked_overread_sentence: string
      underclaim_guard: string
      overclaim_guard: string
      public_summary_max_blocked_items: integer
      full_control_blocked_items: list[string]
      evidence_source: string
      no_physics_delta: boolean
```

The P3-T02 required objects are:

```text
m_src
g_eff
matter_coupling
```

Future packets may add more objects, but they must preserve the authority
rules in this schema and in the Distance-to-GR ledger.

## 4. Field Requirements

| Field | Type | Requirement |
| --- | --- | --- |
| `object_id` | string | Must equal the enclosing key. |
| `ledger_burden_id` | string | Must name a row in `registries/DISTANCE_TO_GR_LEDGER.csv`. |
| `status_family` | string enum | Must use a value from Section 5. |
| `positive_status_sentence` | string | Must state the real scoped positive status before qualifications. |
| `exact_scope_sentence` | string | Must state the exact source-side, evidence, or continuation scope. |
| `allowed_use_sentence` | string | Must state the bounded use allowed by the current control state. |
| `blocked_overread_sentence` | string | Must state the blocked downstream reading without turning the row into "nothing happened." |
| `underclaim_guard` | string | Must forbid minimizing scoped positive status as negligible. |
| `overclaim_guard` | string | Must forbid adoption, derivation, benchmark, Gate Chair, or proof-authority overread. |
| `public_summary_max_blocked_items` | integer | Must be positive; it limits public-summary compression only. |
| `full_control_blocked_items` | list[string] | Must list the full blocked-overread items for control surfaces. |
| `evidence_source` | string | Must name the source surface for the positive status or calibration. |
| `no_physics_delta` | boolean | Must be `true` for this schema packet. |

## 5. Status Families

Allowed `status_family` values are:

| Value | Meaning |
| --- | --- |
| `scoped_source_object` | A source-only object is positive within a declared source-side scope only. |
| `scoped_source_extension_object` | A source-extension object is positive within a declared extension scope only. |
| `scoped_evidence_precondition` | Evidence or a precondition is accepted only for bounded continuation. |
| `draft_control` | The object is draft/control support only. |
| `blocked` | The object is blocked or not available for current use. |
| `frozen_negative` | A local route is frozen negative without a global no-go conclusion. |
| `not_started` | No positive derivation status is available. |

## 6. Alias-Map Integration

`research_control/design/distance_to_gr_status_aliases.yaml` may mirror a
calibration entry under:

```yaml
row_aliases:
  <object_id>:
    acceptance_calibration:
      ...
```

The existing `display_status`, `scoped_positive_term`, `required_qualifier`,
`forbidden_renderings`, and `required_blocked_phrase` fields remain valid.
The calibration block is a structured metadata layer for renderers and
linters. It does not override the Distance-to-GR ledger. If the calibration
block and the ledger conflict, the ledger governs and the packet must fail
closed.

## 7. Validation Rules

An implementation passes this schema when:

- every required P3-T02 object has all required fields;
- each object has `no_physics_delta: true`;
- each object states positive status before exact scope and blocked overread;
- `public_summary_max_blocked_items` is a positive integer;
- `full_control_blocked_items` is nonempty;
- the alias-map calibration block matches the source calibration YAML for
  `status_family`, `positive_status_sentence`, `exact_scope_sentence`,
  `allowed_use_sentence`, and `blocked_overread_sentence`;
- high-risk reader-facing aliases do not render bare `accepted`;
- no field claims canonical ontology adoption, source-law adoption,
  matter-semantics adoption, detector-semantics adoption, coupling-law
  adoption, matter-coupling derivation or adoption, stress-energy semantics,
  stress-energy tensor construction, matter-action construction,
  Einstein-equation derivation, benchmark promotion, Gate Chair verdict,
  completed derivation, future source-extension impossibility, or global
  theory rejection.

P3-T03 may add advisory underclaim-linter enforcement. This P3-T02 schema does
not create hard-fail linter behavior by itself.

## 8. Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.

The AEther-Flow Research Project. (2026b). *Accepted status calibration policy
v1* [Internal project-control policy].
`research_control/design/accepted_status_calibration_policy_v1.md`.

The AEther-Flow Research Project. (2026c). *Distance-to-GR status aliases v1*
[Internal project-control alias map].
`research_control/design/distance_to_gr_status_aliases.yaml`.
