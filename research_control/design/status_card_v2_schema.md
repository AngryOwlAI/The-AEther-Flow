<!-- authority: control -->

# Status Card v2 Schema

## 1. Status

```yaml
schema_id: "status_card_v2_schema"
authority: "control"
status: "active"
created_at: "2026-07-08T18:20:24Z"
created_by_task_id: "RT-20260708-032"
created_by_job_id: "AJ-RT-20260708-032-001"
plan_task_id: "P9-T01"
physics_progress_status: "schema_update_no_physics_delta"
```

This schema defines the status-card v2 fields used by
`research_control/design/accepted_status_calibration_v2.yaml` and mirrored in
`research_control/design/distance_to_gr_status_aliases.yaml`.

It is a project-control schema. It is not a physics derivation, a Gate Chair
verdict, a source-law adoption, a matter-coupling result, an Einstein-equation
result, a benchmark decision, or proof authority.

## 2. Purpose

Status-card v2 keeps the existing positive-first order while reducing public
cognitive load. The required order is:

1. positive status;
2. exact scope;
3. allowed use;
4. blocked overread;
5. next burden;
6. next lawful route;
7. public summary;
8. full control non-conclusions.

The schema adds `next_burden`, `next_lawful_route`, `public_summary`, and
`full_control_non_conclusions` without changing Distance-to-GR ledger status
or authorizing any scientific promotion.

## 3. Root Object

The root YAML object is:

```yaml
accepted_status_calibration_v2:
  high_risk_objects:
    <object_id>:
      object_id: string
      status_card_v2:
        object_id: string
        positive_status: string
        exact_scope: string
        allowed_use: string
        blocked_overread: list[string]
        next_burden: string
        next_lawful_route: string
        public_summary: string
        full_control_non_conclusions: list[string]
```

The P9-T01 required high-risk objects are:

```text
m_src
g_eff
matter_coupling
einstein_equations
benchmark_promotion
```

Future packets may add additional high-risk rows, but they must preserve the
authority rules in this schema, in the Distance-to-GR ledger, and in
`research_control/design/distance_to_gr_status_aliases.yaml`.

## 4. Required Fields

| Field | Type | Requirement |
| --- | --- | --- |
| `object_id` | string | Must equal the enclosing key. |
| `positive_status` | string | Must state the real scoped positive or blocked status before qualifications. |
| `exact_scope` | string | Must state the exact source-side, evidence, obstruction, or continuation scope. |
| `allowed_use` | string | Must state the bounded use allowed by the current control state. |
| `blocked_overread` | list[string] | Must list public-facing blocked overreads without turning the row into "nothing happened." |
| `next_burden` | string | Must state the next honest burden needed before downstream promotion. |
| `next_lawful_route` | string | Must name the lawful route type or next bounded packet class. |
| `public_summary` | string | Must be short, positive-first, exact, non-promotional, and suitable for reader-facing surfaces. |
| `full_control_non_conclusions` | list[string] | Must list the full control-level non-conclusions for audit surfaces. |

## 5. Authority Rules

Status-card v2 is a structured rendering contract only.

- It does not override `registries/DISTANCE_TO_GR_LEDGER.csv`.
- It does not decide the next research route by itself.
- It does not create proof authority, physics truth ranking, benchmark status,
  or Gate Chair authority.
- It does not adopt source laws, detector semantics, matter semantics,
  coupling laws, matter coupling, stress-energy semantics, matter action,
  Einstein equations, benchmark promotion, or completed derivation.
- It does not turn a scoped obstruction into a global no-go theorem or future
  source-extension impossibility claim.
- It preserves positive-first order for high-risk rows and requires
  `next_burden` for those rows.

## 6. Alias-Map Integration

`research_control/design/distance_to_gr_status_aliases.yaml` may mirror a
status-card v2 entry under:

```yaml
row_aliases:
  <object_id>:
    status_card_v2:
      ...
```

The existing `display_status`, `scoped_positive_term`, `required_qualifier`,
`forbidden_renderings`, `required_blocked_phrase`, and
`acceptance_calibration` fields remain valid. The v2 card is a structured
metadata layer for later renderers and linters. It does not override the
Distance-to-GR ledger. If the card and ledger conflict, the ledger governs and
the packet must fail closed.

P9-T02 may integrate this schema into current-frontier and compact-frontier
renderers. P9-T04 may add claim-language linter tests. P9-T01 does not make
those integration changes.

## 7. Validation Rules

An implementation passes this schema when:

- each required P9-T01 high-risk object has a `status_card_v2` block;
- every `status_card_v2` block has all required fields in positive-first
  order;
- `next_burden` is present and nonempty for each required high-risk row;
- `blocked_overread` and `full_control_non_conclusions` are nonempty lists;
- the alias-map `status_card_v2` block matches the source calibration YAML for
  the required fields;
- the public summary is concise and does not render bare `accepted`;
- the schema preserves all no-proof, no-ledger-override, no-routing-authority,
  no-physics-delta, and no-promotion authority rules.

## 8. Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.

The AEther-Flow Research Project. (2026b). *Handoff 0724* [Internal
research-control handoff]. `research_control/handoffs/handoff-0724.yaml`.

The AEther-Flow Research Project. (2026c). *Accepted status calibration schema
v1* [Internal project-control schema].
`research_control/design/accepted_status_calibration_schema_v1.md`.

The AEther-Flow Research Project. (2026d). *Distance-to-GR status aliases v1*
[Internal project-control alias map].
`research_control/design/distance_to_gr_status_aliases.yaml`.
