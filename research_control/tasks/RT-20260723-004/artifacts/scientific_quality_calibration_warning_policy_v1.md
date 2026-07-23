<!-- authority: control -->

# Scientific-Quality Calibration and Warning Policy v1

## Purpose

This P12-T05 policy makes missing data, identity defects, range defects, and
anti-splitting defects visible without converting project-control diagnostics
into scientific authority.

## Status Rules

- `measured`: the denominator is known and nonempty, every eligible identity
  has a valid immutable binding, and every qualifying identity is eligible.
- `not_measured`: the denominator is unknown or known-empty. The value is
  `null`, never zero.
- `invalid`: identity, subset, binding, range, or reported-value integrity
  fails.

The complete eight-metric report is `PASS` when no metric is invalid.
`not_measured` is an honest supported state and does not fail the report.
Validator `PASS` is operational evidence only.

## Warning Classes

| Code | Trigger | Result |
| --- | --- | --- |
| `unknown_denominator` | No authoritative eligible population exists. | `not_measured`; value remains `null`. |
| `empty_eligible_set` | The eligible population is known and empty. | `not_measured`; value remains `null`. |
| `duplicate_identity` | One logical identity appears more than once. | `invalid`; hard project-control gate. |
| `duplicate_qualifying_identity` | One numerator identity appears more than once. | `invalid`; hard project-control gate. |
| `artifact_splitting_or_alias` | Distinct IDs share one immutable binding. | `invalid`; hard project-control gate. |
| `numerator_outside_denominator` | A qualifying identity is not eligible. | `invalid`; hard project-control gate. |
| `logical_range_violation` | A reported value is outside `[0, 1]`. | `invalid`; hard project-control gate. |
| `reported_value_mismatch` | A reported value differs from the identity-derived value. | `invalid`; hard project-control gate. |
| `computed_range_violation` | An implementation produces a value outside `[0, 1]`. | `invalid`; hard project-control gate. |

Hard gates in this table govern metric-record integrity only. They do not
reject a scientific theory, change a candidate's status, establish a theorem,
or create protected authority.

## Calibration Rules

1. Compute values from identity sets; do not accept a free scalar as evidence.
2. Round computed ratios to six decimal places.
3. Retain the numerator identities, denominator identities, source paths, and
   bindings in the record.
4. Do not compare values across incompatible eligibility contracts.
5. Do not reward an artifact split, renamed duplicate, or alias.
6. Do not treat missing denominators as zero performance.
7. Do not combine the eight values into a scientific-truth score.
8. Keep raw volume in a separately labeled operational-context surface.
9. Keep all claim, ontology, benchmark, proof, Gate Chair, publication, and
   Distance-to-GR authority flags false.

## Dashboard Rule

The durable-quality rows appear before raw payload- and packet-volume
diagnostics in the primary dashboard reading order. Raw volume is operational
context only. A metric warning or `PASS` cannot be read as physics proof or
promotion.
