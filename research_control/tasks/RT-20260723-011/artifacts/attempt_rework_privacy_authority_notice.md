---
authority: control
status: active
task_id: RT-20260723-011
plan_task_id: P12-T06
---

# Attempt and rework dashboard privacy and authority notice

## Permitted projection

The P12-T06 dashboard may expose only typed event identifiers, task
identifiers, registered role and work-kind identifiers, immutable
candidate-family identifiers, event and disposition counts, source paths, and
SHA-256 bindings. It may report operational ratios only when the numerator,
denominator, status, and limitation are explicit.

## Material that must remain excluded

The dashboard must not copy event summaries, user or system prompts, private
reasoning, credentials, tokens, personal contact data, or unregistered
free-text classifications. Its privacy validator rejects credential-shaped
strings and private-field names in the machine projection. Source artifacts
remain governed at their original paths and are not reproduced by this
dashboard.

## Freshness rule

Freshness is content-addressed rather than wall-clock inferred. The freshness
receipt binds every input used by the projection, the builder, this notice, and
the deterministic dashboard outputs. A mismatched or missing hash is stale and
must fail validation; silent regeneration cannot strengthen the source record.

## Authority boundary

Attempt, validation, audit, repair, abandonment, disposition, and PASS-like
counts are project-process observations in a bounded ledger. They are not
physics refutations, scientific proof, ontology evidence, exact-GR derivation,
Distance-to-GR progress, benchmark promotion, candidate adoption or rejection,
publication readiness, or Gate Chair authority. A zero observed count is not a
rate when the ledger lacks the required denominator.
