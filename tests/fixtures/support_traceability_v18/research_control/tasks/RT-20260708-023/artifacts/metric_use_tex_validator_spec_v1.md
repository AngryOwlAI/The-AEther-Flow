<!-- authority: control -->

# Metric-Use Ledger TeX Validator Spec v1

## Purpose

This artifact specifies the v18 P7-T05
`metric_use_ledger_tex_validator_support_only` implementation. The validator
scans configured TeX artifacts for high-risk metric-adjacent references and
checks that each detected class is covered by `registries/METRIC_USE_LEDGER.csv`
or by an explicit task-local `metric-use-ledger: no-use-justification` comment.

The validator is support-only project-control tooling. It is not proof
authority, not source-law adoption, not target metric import, not
`MetricData(E)` adoption, not `g_eff` adoption or scope expansion, not
matter-coupling derivation, not stress-energy or matter-action import, not
Einstein-equation derivation, not benchmark promotion, not a Gate Chair verdict,
and not a completed derivation.

## Configured Scope

By default, the validator scans `.tex` artifact paths already named in
`registries/METRIC_USE_LEDGER.csv`. Operators may pass `--paths` for an
explicit bounded TeX scope.

TeX declaration lines such as `\newcommand`, `\renewcommand`,
`\providecommand`, `\def`, and `\DeclareMathOperator` are treated as declaration
surface rather than semantic body references. Body references remain in scope.

## Required High-Risk Classes

The validator must detect these v18 P7-T05 classes:

- `g_eff`
- `metricdata_e`
- `proper_time`
- `detector_calibration`
- `stress_energy`
- `matter_action`

## Coverage Rule

For each configured TeX artifact, a detected class passes only when at least one
of these conditions is true:

- a row for the same artifact path in `registries/METRIC_USE_LEDGER.csv`
  contains class-specific evidence in `object_used`, `use_category`,
  `declared_scope`, `allowed_use`, or `notes`;
- the TeX artifact contains an explicit
  `metric-use-ledger: no-use-justification` comment covering the class.

Otherwise, the validator emits an `unledgered_reference` or
`missing_class_ledger_coverage` finding.

## Integration Policy

The script supports two enforcement modes:

- `--failure-mode hard-fail`: findings produce `status: FAIL` and exit code 1.
- `--failure-mode warn`: findings produce `status: WARN` and exit code 0.

This exposes the warning-or-hard-fail integration surface required by P7-T05
without changing the repository's full validation policy in this packet.

## Done Criteria

- Focused unit tests pass.
- The live configured TeX scope passes with zero findings.
- Synthetic unledgered references to all six high-risk classes fail in
  `hard-fail` mode.
- The same synthetic references return `WARN` and exit zero in warning mode.
- The next route is P7-T06
  `detector_placeholder_collapse_checker_support_only`.
