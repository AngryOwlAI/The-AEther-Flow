<!-- authority: control -->

# Durable Scientific-Quality Metric Taxonomy v1

## Status and Scope

This P12-T05 taxonomy defines eight advisory project-control diagnostics. It
does not define scientific truth, theorem validity, ontology status, benchmark
promotion, Gate Chair authority, proof authority, publication authority, or
Distance-to-GR progress. No aggregate scientific-truth score is permitted.

Each measured value has the form

`count(identity-bound qualifying members) / count(identity-bound eligible members)`.

The eligible population is part of the metric record, not an inferred global
universe. A denominator is `known` only when every eligible member is named by
an immutable identity and SHA-256 binding. If that population is unavailable,
the metric is `not_measured`; it is never zero-filled.

## Shared Identity Contract

Every eligible member contains:

- `identity`: a stable logical identity, not an artifact count;
- `identity_sha256`: a lowercase SHA-256 binding for that identity;
- `identity_kind`: the exact kind required by the metric;
- `source_path`: the tracked evidence path establishing eligibility.

Qualifying identities must be a subset of eligible identities. Duplicate
identities fail validation. Two identities sharing one binding fail the
anti-splitting guard because one logical result cannot earn multiple credit.
Artifacts may support an identity, but producing more artifacts does not
increase a numerator or denominator.

## Metric Families

### `assumption_reduction_rate`

- Identity kind: `candidate_or_theorem_comparison`.
- Denominator: prospectively eligible, identity-bound before/after comparisons
  with explicit assumption sets.
- Numerator: comparisons with at least one removed assumption and no
  unaccounted stronger replacement.
- Boundary: reduction is scoped to the comparison and does not prove the
  candidate, theorem, or physical interpretation.

### `theorem_generality_rate`

- Identity kind: `declared_theorem_application`.
- Denominator: a theorem's prospectively declared eligible application
  universe.
- Numerator: applications with explicit hypothesis-preserving subsumption.
- Boundary: shared-coordinate subsumption does not reopen, adopt, or prove an
  exact historical family.

### `countermodel_novelty_rate`

- Identity kind: `countermodel`.
- Denominator: identity-bound countermodels in a fixed comparison corpus.
- Numerator: countermodels with a distinct witness identity and a
  non-duplicate falsified-assumption set.
- Boundary: corpus-relative novelty is not a global no-go theorem, theory
  rejection, or future-extension impossibility.

### `obstruction_unification_and_reuse_rate`

- Identity kind: `obstruction`.
- Denominator: unique immutable obstruction identities in the measurement
  window.
- Numerator: obstructions explicitly cited by a later tracked result or
  explicitly subsumed by a stronger scoped obstruction.
- Boundary: later reuse preserves the earlier scope. Similar prose alone is
  not semantic unification.

### `independent_review_survival_rate`

- Identity kind: `reviewed_scientific_object`.
- Denominator: objects with an executed, provenance-qualified independent
  review and dispositionable findings.
- Numerator: reviewed objects that retain a non-promotional scoped result
  after all recorded findings are dispositioned.
- Boundary: same-context, same-model, synthetic, or merely human-labeled
  records are not silently counted as independent review. Survival is not
  replication, adoption, proof, or a Gate Chair verdict.

### `benchmark_breadth_rate`

- Identity kind: `benchmark_case`.
- Denominator: a prospectively fixed benchmark-case universe under one
  assumption contract.
- Numerator: cases with identity-bound, assumption-compatible results.
- Boundary: breadth is not benchmark recovery, physical adequacy, or
  promotion.

### `retraction_repair_visibility_rate`

- Identity kind: `attempt_event`.
- Denominator: failed, superseded, repaired, abandoned, or audit-finding
  events in the sealed attempt-ledger population.
- Numerator: those events retained as finalized immutable records with source
  references and valid event bindings.
- Boundary: visibility measures durable process memory, not scientific merit.

### `ledger_durability_rate`

- Identity kind: `attempt_event`.
- Denominator: all events in the sealed attempt-ledger population.
- Numerator: events whose sequence, payload hash, event hash, and predecessor
  binding validate.
- Boundary: ledger integrity does not make recorded scientific content true.

## Primary and Context Surfaces

These eight rows form the primary scientific-quality diagnostic surface. They
remain advisory and non-promotional. Raw packet, task, artifact, payload, and
validator counts may remain visible only as operational context. They cannot
substitute for an eligible-set quality diagnostic.

## Current Measurement Boundary

The current repository provides structured denominators for immutable
obstruction reuse, rework-event visibility, and attempt-ledger durability.
Other families remain `not_measured` until their authoritative eligible
populations are normalized. This is a data-availability statement, not a
negative scientific result.
