<!-- authority: control -->

# P6-T08 aggregate receipt audit

## Result

`scripts/validation/aggregate.py` implements the bounded P6-T08 evidence
reducer. It consumes existing classification, plan, execution, artifact,
generator, residue, rollback, and shadow-comparison evidence. It does not
select gates, execute commands, change child status, or replace the
legacy-authoritative validation path during `shadow_planner`.

The focused aggregate suite passes 16 scenarios. The relevant compatibility
set passes 77 tests across aggregation, orchestration, planner, profile, and
checkpoint behavior.

## Receipt coverage

The aggregate receipt records:

- classifier paths, path-family tags, blocked paths, and a classifier hash;
- plan reasons, selected, executed, skipped, superseded, and unaccounted gates;
- deterministic gate results in planner order regardless of completion order;
- role, skill, profile, and checkpoint obligation coverage;
- generator changes, staged tree identity, residue, and rollback state;
- duration, output bytes, subprocess count, and cache hit/miss counts;
- canonical child-receipt hashes and streamed raw-artifact hashes without
  embedding either payload;
- a bounded console summary plus complete deterministic JSON; and
- explicit operational-only and no-physics-authority fields.

## Fail-closed behavior

The aggregate becomes `BLOCKED_CONFIGURATION` when selected gates lack result
evidence, child and derived status disagree, an applicable obligation lacks a
`PASS` or `CACHE_HIT` provider, a skipped gate claims satisfaction without a
proven-false condition, raw artifact references are missing, residue is not
clean, required rollback is absent, or affected blocking shadow gates do not
match. A blocking child cannot be converted to aggregate PASS.

Unknown child schemas and versions, embedded raw stream fields, path traversal,
duplicate identities, and inconsistent selected/skipped/superseded plan sets
are rejected before aggregation rather than repaired.

## Compatibility and authority

The module is not wired into executor, checkpoint, manifest, profile, wrapper,
or CI authority in this packet. Existing execution and checkpoint behavior is
unchanged. The task-local shadow fixture proves the aggregate status rules
produce matching legacy/planner results for the affected blocking scenario and
block an unexplained mismatch.

No ordinary-research state, handoff, canonical ontology, physics source,
benchmark status, proof authority, or Gate Chair authority changed.
