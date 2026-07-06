<!-- authority: control -->

# Metric-Use Ledger Schema v1

## Purpose

This project-control schema defines the required ledger surface for tracking
uses of `g_eff`, `MetricData(E)`, and nearby metric-language references in
matter-coupling work. It implements v17 P5-T01 only.

The ledger prevents a scoped source-extension object from being silently read
as a physical Lorentzian metric, proper-time normalizer, detector calibration object,
stress-energy premise, matter-action premise, Einstein-equation premise, or
benchmark-fit premise.

## Authority Boundary

The schema is project-control infrastructure. It does not populate the ledger,
revise physics sources, adopt `MetricData(E)`, expand `g_eff`, establish
detector semantics, import stress-energy semantics, define a matter action,
derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or
claim completed derivation.

P5-T02 is responsible for ledger population. This P5-T01 schema packet only
creates the schema document and registry header.

## Registry

Canonical registry path:

```text
registries/METRIC_USE_LEDGER.csv
```

Required header:

```csv
use_id,task_id,artifact_path,object_used,use_category,declared_scope,allowed_use,forbidden_interpretations,no_target_guard_path,audit_status,stress_status,created_at,notes
```

## Required Columns

| Column | Required meaning | Valid value rule |
| --- | --- | --- |
| `use_id` | Stable ledger row identifier. | Unique nonblank value, preferably `MUL-<task-id>-<ordinal>`. |
| `task_id` | Research-control task associated with the reference. | Existing or planned task identifier, or `SCHEMA` only for a schema marker row. |
| `artifact_path` | Repository-relative path containing the relevant reference. | Nonblank path for populated rows. |
| `object_used` | Object or token being controlled. | Examples: `g_eff`, `MetricData(E)`, `proper_time`, `Lorentzian_metric`. |
| `use_category` | Ledger category for the reference. | Must be one of the allowed use categories below. |
| `declared_scope` | Exact project-control scope of the use. | Must state the local scope without widening authority. |
| `allowed_use` | What the reference may support. | Must be positive and scoped. |
| `forbidden_interpretations` | Overreads blocked for this reference. | Must include every relevant forbidden metric use below. |
| `no_target_guard_path` | Source path or control artifact that blocks target-physics import. | Nonblank for populated rows when a guard exists. |
| `audit_status` | Hidden-import audit status. | Recommended values: `not_audited`, `audited_clean`, `forbidden_import_detected`, `blocked_by_scope`. |
| `stress_status` | Refuter/stress status if applicable. | Recommended values: `not_stressed`, `stress_survived`, `repair_required`, `scoped_obstruction`, `not_applicable`. |
| `created_at` | UTC creation timestamp. | ISO 8601 UTC timestamp. |
| `notes` | Brief receipt note. | Must not promote physics claims. |

## Allowed Use Categories

```yaml
allowed_use_categories:
  - scoped_source_extension_context
  - source_side_relation_input_candidate
  - finite_local_witness_context
  - blocked_physical_metric_use
  - forbidden_import_detected
```

Interpretation:

- `scoped_source_extension_context`: the reference is used only as scoped
  source-extension context under an already recorded boundary.
- `source_side_relation_input_candidate`: the reference is an input candidate
  for a source-side relation and does not itself become target metric data.
- `finite_local_witness_context`: the reference appears only in finite/local
  witness or support-only context.
- `blocked_physical_metric_use`: the reference is present because a physical
  metric overread is explicitly blocked.
- `forbidden_import_detected`: the reference records a detected forbidden
  import or suspected import that must fail closed until repaired.

## Forbidden Metric Uses

```yaml
forbidden_metric_uses:
  - physical_lorentzian_metric
  - proper_time_normalization
  - detector_calibration
  - stress_energy_semantics
  - matter_action_premise
  - Einstein_equation_premise
  - benchmark_fit_premise
```

Any populated row whose local context implies one of these categories must
either classify the use as `blocked_physical_metric_use` or
`forbidden_import_detected`, name the guard path, and preserve fail-closed
status until a later authorized route repairs or rejects it.

## P5-T02 Population Rule

P5-T02 must inspect the high-risk matter-route artifacts named in the v17 plan
and add one ledger row for each relevant `g_eff`, `MetricData(E)`, proper-time,
metric, or Lorentzian reference, unless the artifact has an explicit no-use
justification.

No populated row may convert scoped source-extension context into target
metric authority.
