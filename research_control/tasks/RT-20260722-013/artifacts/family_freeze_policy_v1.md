<!-- authority: control -->

# P12-T02 Family Freeze and Evidence-Based Reopening Policy

## Purpose

This task-local `draft/control` policy prevents another construction-audit-stress-
repair cycle from entering an already frozen EqSrc candidate family merely
under a new name. It is prospective and additive. It does not edit P1 or P10
history, prove a theorem, reject the broader theory, adopt a candidate, modify
ontology, or change the Distance-to-GR ledger.

## Match rule

A physics-facing route matches a frozen family when any of these exact
identities occurs in the historical seed:

1. `family_id`;
2. `family_identity_sha256`; or
3. any `assumption_sha256`.

The assumption digest catches a renamed family that preserves an inventoried
assumption basis. Display names, repository order, task count, validator PASS,
and generated derivatives are not identity evidence.

## Route dispositions

Candidate construction, audit, stress, or repair on a matched family fails
closed unless a tracked reopening record names one of four evidence classes:
`new_primitive`, `new_theorem`, `new_variation_class`, or
`protected_decision`. The evidence path and SHA-256 must already exist, the
opening scope must name the exact family, and automatic adoption must remain
false. A rename or repackaging route is always barred; after qualifying
evidence, the packet must declare the substantive route it will actually run.

A theorem, primitive, variation-class, source-acquisition, or precise-
obstruction investigation that is materially different may proceed as a
distinct branch while the family remains frozen. Such a packet must name its
branch identity, material difference, expected artifact, and state that it
does not reconstruct the frozen candidate. This prevents the policy from
blocking a materially different theorem or ontology branch.

## Reopening evidence

- `new_primitive` requires a distinct primitive identity and may record only a
  proposal-only source extension; it does not modify canonical ontology.
- `new_theorem` requires an exact theorem identity and a proposal-neutral
  mapping to the frozen family. Admission validates evidence shape and hash,
  not theorem truth.
- `new_variation_class` requires an exact variation identity, an independent
  physical-basis statement, and a material distinction from seeded
  assumptions.
- `protected_decision` requires an exact human-gate identity and an AgentJob
  that remains human-gated. It grants no broader or implicit promotion.

The earlier P1-T03 classes map conservatively: ontology derivation, general
selector theorems, and physical-irrelevance results are theorem or primitive
evidence; a material ledger delta qualifies only when it traces to one of the
three substantive evidence classes or an exact protected decision; human Gate
Chair authority maps only to `protected_decision`.

## Authority boundary

Every declaration preserves `local_family_freeze_preserved: true`,
`global_no_go_claimed: false`, `automatic_candidate_adoption: false`,
`theorem_truth_inferred: false`, `ontology_modified: false`, and
`physics_promotion_authorized: false`. The current ontology does not derive the
frozen selectors; that scoped statement is not a theorem of impossibility.

## Enforcement

`scripts/research_control/family_freeze_admission.py` evaluates future
physics-facing AgentJobs created after `2026-07-22T17:25:51Z`. Historical jobs
remain readable. Project-system jobs remain on their separate P12-T01 path.
The research-control validator hard-fails a nonconforming prospective route,
and the Director context exposes the same policy. Validator PASS is operational
evidence only.
