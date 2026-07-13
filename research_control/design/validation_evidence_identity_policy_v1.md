<!-- authority: control -->

# Validation evidence identity policy v1

## Status and scope

- Policy ID: `validation-evidence-identity-policy-v1`
- Plan task: `P1-T01`
- Migration epoch: `legacy`
- Status: `active-policy`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims changed: `false`
- Physics or proof authority created: `false`

This policy defines when validation executions are duplicate evidence, distinct
cross-state confirmation, or candidates for independent evidence. It does not
change any validator, invocation owner, checkpoint command, CI workflow, or
scientific acceptance gate. The P0-T04 legacy invocation graph remains the
execution inventory while later v19 tasks define canonical gate IDs and
supersedence contracts.

## Evidence identity

For schema version `v1`, an execution's evidence identity is:

```text
evidence_identity = SHA-256(canonical_json({
  "gate_id": gate_id,
  "implementation_digest": implementation_digest,
  "environment_digest": environment_digest,
  "config_digest": config_digest,
  "scope": scope,
  "tree_hash": tree_hash
}))
```

`canonical_json` is UTF-8 JSON with keys in the order shown, no insignificant
whitespace, and JSON string escaping. Every digest is algorithm-qualified.
Missing or unresolved components make the identity unresolved and therefore
non-deduplicable.

### Component rules

- `gate_id` identifies the semantic gate contract. Until P1-T02 establishes
  canonical IDs, the `LVG-*` IDs from the P0-T04 graph are provisional but
  usable within the legacy epoch.
- `implementation_digest` covers the executable implementation and every
  decision-relevant imported helper. Similar names, wrappers, or command text
  do not establish implementation equivalence.
- `environment_digest` covers the runtime, operating system, architecture, and
  dependency versions that can affect the result.
- `config_digest` covers arguments, environment variables, policy inputs, and
  configuration files that can affect the result.
- `scope` is a normalized object encoded as a string. It names the checked
  surface and includes `tree_state=working`, `tree_state=index`,
  `tree_state=commit`, or another explicit state kind.
- `tree_hash` identifies the exact input snapshot. A staged-tree identity uses
  the Git index tree. A working-tree identity uses a deterministic content
  manifest digest and the `tree_state=working` scope tag. Hash type prefixes
  are mandatory.

A working-tree PASS never satisfies a staged-tree gate. Even if file content is
temporarily equal, the two executions have different `scope.tree_state`
semantics and must retain separate evidence identities.

## Classification algorithm

1. If any identity component is missing or its provenance is unresolved,
   classify the pair as `unresolved_non_deduplicable`.
2. If all six components are equal, classify deterministic repetitions as
   `duplicate_evidence`. Repetition adds no independent deterministic evidence.
3. A declared nondeterminism experiment may repeat one identity to estimate a
   distribution. It must name an experiment ID, trial plan, controlled random
   inputs, and stopping rule. Those trials are sampling evidence for that
   experiment, not independent correctness evidence for the gate.
4. If `tree_hash`, `scope`, `environment_digest`, or `config_digest` differs,
   classify the pair as `legitimate_cross_state_confirmation` with the changed
   component named. Distinct state does not by itself imply independent logic.
5. If `gate_id` is equal and `implementation_digest` differs, classify the pair
   as `distinct_implementation_identity`. It is independent evidence only when
   an audit also establishes separate decision-relevant implementation lineage;
   a wrapper around the same helper is not independent.
6. If `gate_id` differs, do not infer equivalence from similar names. A later
   supersedence contract must prove same-scope coverage before either result can
   replace the other.

Direct duplicates may be removed without weakening evidence only when the
retained execution preserves the same identity, raw failure visibility,
required receipt, and transaction boundary. Performance gains never compensate
for a lost invariant or different staged-tree check.

## Epistemic classes

Each current provisional gate has exactly one primary epistemic class. A
wrapper's class describes its primary decision role; nested gates retain their
own identities and do not become new evidence merely because a wrapper reports
their status.

### Protected transaction integrity

These gates protect repository/control invariants and checkpoint boundaries:

`LVG-001`, `LVG-003`, `LVG-004`, `LVG-015`, `LVG-016`, `LVG-023`,
`LVG-026`, `LVG-028`, `LVG-030`, `LVG-031`, `LVG-035`, `LVG-036`.

Their PASS means only that the declared operational integrity contract passed
for the recorded identity. It is not scientific proof.

### Derived-surface freshness

These gates verify or generate registered derivatives, documentation, memory,
or presentation surfaces:

`LVG-005`, `LVG-006`, `LVG-007`, `LVG-008`, `LVG-009`, `LVG-013`,
`LVG-014`, `LVG-018`, `LVG-020`, `LVG-021`, `LVG-027`, `LVG-032`,
`LVG-033`, `LVG-034`, `LVG-037`.

Freshness evidence never overrides the canonical source or registry row.

### Scientific artifact verification

These gates can inspect artifacts that contain scientific or claim-structure
material without granting promotion authority:

`LVG-017`, `LVG-019`, `LVG-022`.

A PASS establishes only the checked property for the recorded inputs. It does
not establish ontology adoption, physical truth, theorem proof, benchmark
promotion, or a Gate Chair verdict.

### Operational diagnostics

These gates provide routing, retrieval, or optimization information:

`LVG-002`, `LVG-010`, `LVG-011`, `LVG-012`, `LVG-024`, `LVG-025`,
`LVG-029`.

Diagnostic output may guide the next bounded action but cannot replace a
blocking validator or protected human decision.

## Authority levels and execution effects

Authority and mutation are orthogonal. Every execution records one decision
authority and one execution effect.

- `blocking`: failure blocks the declared transaction and scope.
- `advisory`: informs action but cannot independently block or satisfy a gate.
- `local-only`: concerns ignored local retrieval/cache state and cannot govern
  tracked repository authority.
- `human-review`: requires a named protected human decision; automation may
  prepare evidence but cannot emit the verdict.
- `scheduled-only`: runs only under an explicit periodic or scheduled profile
  and cannot be silently added to a normal transaction.
- `mutating`: execution may change working files or generated derivatives.
  After mutation, earlier tree identities cannot validate the new state; the
  relevant non-mutating or staged gate must run against a recomputed identity.

`mutating` is an execution-effect tag, not a substitute for decision authority.
Non-mutating is the default effect when `mutating` is absent.

Legacy graph values map as follows: `blocking`, `advisory`, and `local_only`
map directly; `diagnostic` and `routing` map to advisory operational
diagnostics; `nested` inherits its containing gate's decision authority and
does not create independent evidence. No current `LVG-*` gate is assigned
`human-review` or `scheduled-only`; those values are reserved for explicit
future manifest entries.

## Operational evidence boundary

Generated receipts, cache hits, CI status badges, summaries, dashboards, and
wrapper exit codes are operational evidence only. They may locate the
underlying execution, but they do not become an additional independent PASS.
An underlying run is countable only when its identity components, raw outcome,
and provenance are auditable.

The same rule applies to memory generation: the mutating bootstrap result and
the post-generation validate-only result have different tree identities. The
second is legitimate cross-state confirmation, not a duplicate. Checkpoint
working-tree and staged-tree validations remain separate because the Git index
is the protected commit candidate.

## Rollback and ambiguity

- Unresolved identity remains non-deduplicable.
- The legacy invocation graph remains authoritative for execution inventory
  until later v19 tasks activate a replacement manifest.
- Any failed same-scope proof restores all affected legacy invocations.
- This policy can be superseded only by a tracked project-system decision with
  preserved failure-mode coverage and updated fixtures.

