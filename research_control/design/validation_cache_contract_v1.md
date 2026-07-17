<!-- authority: control -->

# Validation cache contract v1

## Status and authority

- Contract ID: `validation-cache-contract-v1`
- Key schema ID: `validation_cache_key_v1`
- Entry schema ID: `validation_cache_entry_v1`
- Plan task: `P10-T02`
- Migration epoch: `shadow_planner`
- Status: `active-contract-runtime-disabled`
- Safe feature-switch state: `cache_mode=off`
- Storage root: `.local/validation-cache/`
- Current manifest policies changed: `false`
- Cache implementation or activation: `false`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims changed: `false`
- Physics, proof, benchmark, ontology, or Gate Chair authority created: `false`

This contract defines conservative identity, eligibility, storage, integrity,
invalidation, bypass, and rollback rules for later validation-cache work. It
does not implement cache storage or lookup, change a gate's live
`cache_policy`, integrate a cache into a validator, replace an execution, or
switch orchestration authority. Every gate in
`validation_gate_manifest_v1.yaml` remains `ineligible` until a later bounded
task changes and validates that manifest.

The cache is an optional optimization over exact duplicate operational
evidence. A cache miss, disabled cache, unreadable cache, corrupt entry, or
failed write must always fall back to the same uncached gate execution. Cache
availability must never be required for correctness or acceptance.

Normative `MUST`, `MUST NOT`, `SHOULD`, and `MAY` terms apply to later
implementations that claim conformance to this contract.

## Governing source contracts

This contract refines, but does not supersede:

- `validation_evidence_identity_policy_v1.md` for evidence identity and
  duplicate-evidence semantics;
- `validation_gate_manifest_schema_v1.md` and
  `validation_gate_manifest_v1.yaml` for gate metadata and cache-policy
  vocabulary;
- `validation_run_receipt_schema_v1.md` for `CACHE_HIT`, `cache_status`, result
  hashes, and non-authoritative receipts;
- `validation_environment_contract_v1.md` for the environment fingerprint and
  dependency-specification digest;
- `validation_orchestration_migration_and_rollback_policy_v1.md` for
  `cache_mode`, shadow comparison, rollback, and final uncached checkpoint
  evidence; and
- `scripts/validation/snapshot.py` for the P10-T01 exact working/staged
  repository snapshot identity.

Where an input, implementation, environment, configuration, scope, or
authority fact is incomplete or inconsistent, caching fails closed and the
gate runs uncached.

## Canonical cache key

### Serialization

The cache key is:

```text
cache_key = SHA-256(canonical_json(validation_cache_key_v1))
```

`canonical_json` is UTF-8 JSON with object keys sorted lexicographically,
separators `,` and `:`, JSON escaping, no non-finite numbers, and no trailing
newline in the hashed bytes. Set-like arrays are sorted and unique before
serialization. Hashes are algorithm-qualified in stored material. Unknown
fields, duplicate keys, missing fields, unsupported versions, or
non-canonical values make the key unresolved and force an uncached run.

### Required key material

A `validation_cache_key_v1` object contains exactly:

| Field | Requirement |
| --- | --- |
| `schema_id` | Exactly `validation_cache_key_v1`. |
| `schema_version` | Exactly `1`. |
| `contract_id` | Exactly `validation-cache-contract-v1`. |
| `gate_id` | Exact stable ID from the selected manifest gate. |
| `scope` | Exact normalized scope object defined below. |
| `tree_hash` | Algorithm-qualified exact P10-T01 tree fingerprint. |
| `base_ref` | Exact normalized base-reference object defined below. |
| `implementation_digest` | SHA-256 of the complete decision-relevant executable closure. |
| `manifest_digest` | SHA-256 of the complete canonical validation manifest. |
| `config_digest` | SHA-256 of the effective gate, planner, arguments, selection, and feature-switch configuration. |
| `environment_fingerprint` | Exact fingerprint from `validation_environment_v1`. |
| `dependency_lock_digest` | Exact dependency-specification digest from `validation_environment_v1`. |
| `receipt_schema` | Object containing exact gate-result and run-receipt schema IDs and versions. |

The normalized `scope` object contains exactly:

- `scope_kind`: one manifest scope from `working`, `staged`, `commit`,
  `repository`, or another future schema-versioned value;
- `tree_state`: one of `working`, `staged`, or `commit`, naming the concrete
  repository state used even when `scope_kind` is `repository`;
- `profile`: the selected validation profile;
- `mode`: `legacy`, `shadow`, or `planner`;
- `selection_digest`: SHA-256 of the ordered selected path set, selected gate
  set, and scope-affecting selectors; and
- `repository_identity_digest`: SHA-256 of the canonical repository root and
  Git common-directory identity.

The normalized `base_ref` object contains:

- `name`: the exact requested base reference, or `none` when the gate has no
  comparison base; and
- `commit`: the resolved algorithm-qualified commit ID, or `none` only when
  `name` is `none`.

Name and resolved commit are both key material. Re-pointing a symbolic
reference invalidates the old key even when another field would otherwise mask
the change.

`receipt_schema` contains:

```json
{
  "gate_result_id": "validation_gate_result_v1",
  "gate_result_version": 1,
  "run_receipt_id": "validation_run_receipt_v1",
  "run_receipt_version": 1
}
```

An implementation MAY add a field only by introducing a new key-schema
version. It MUST NOT silently append, omit, or default key components within
version 1.

### Exact tree rules

- A staged key uses the P10-T01 staged fingerprint, which binds the resolved
  base commit and `git write-tree` result.
- A working key uses the P10-T01 working fingerprint, which binds the resolved
  base commit, binary full-index diff, and ignored-rule-respecting untracked
  file manifest.
- A commit key uses an algorithm-qualified immutable Git tree ID and resolved
  commit ID.
- A repository key uses `scope_kind=repository` and MUST still name the exact
  underlying working, staged, or commit `tree_state`; the word `repository` is
  not permission to omit concrete state identity.
- Working and staged scopes are different even when their visible bytes are
  equal. No equality shortcut or content-only promotion between them is
  permitted.
- The captured snapshot MUST be rechecked for freshness before lookup and
  immediately before accepting a hit. Any state change makes the lookup a
  miss.

### Implementation and input closure

`implementation_digest` covers the gate adapter, executable module, imported
decision-relevant helpers, command wrapper, and result-normalization logic.
Command text or a top-level file hash alone is insufficient.

`config_digest` covers the selected manifest gate object, normalized command
arguments, planner configuration, selection predicates, output policy, and
all documented environment variables or feature switches that can change
selection, findings, severity, or status. The complete manifest is hashed
separately so unrelated manifest changes remain conservative invalidators in
version 1.

Every cacheable execution produces a deterministic sorted source-fingerprint
manifest. Each decision-relevant input has a normalized path or synthetic
input ID, type, and algorithm-qualified digest. `input_fingerprint` in the gate
result is the SHA-256 of that canonical manifest. A glob, imported helper,
generated prerequisite, Git metadata query, external tool, or configuration
input whose closure cannot be enumerated makes the gate ineligible.

The dependency digest is retained as a separate key field even though the
environment fingerprint also incorporates it. This deliberate redundancy
makes dependency drift auditable and satisfies the stronger exact-key
contract; neither field may be omitted.

## Gate eligibility

### Fail-closed eligibility algorithm

A gate may be activated as `exact_tree` only when all of these conditions are
proved by a later tracked task:

1. The manifest explicitly sets that gate to `exact_tree` or
   `scheduled_bypass`.
2. The gate is read-only: `mutating` is `false` and execution does not change
   tracked, staged, ignored, external, or runtime state. Any declared
   `output_globs` are treated as checked input artifacts, are fingerprinted,
   and are proved unchanged before and after execution.
3. Its normalized outcome is deterministic for the complete key and declared
   input closure. Volatile run timestamps and elapsed durations are receipt
   metadata, not decision inputs.
4. Every decision-relevant repository, Git, implementation, configuration,
   environment, dependency, and tool input is declared and fingerprinted.
5. The execution begins and ends on the same fresh exact snapshot.
6. The original result is a complete `PASS` with zero errors, zero warnings,
   no truncated hard finding, and an integrity-checked full local receipt.
7. The gate is not a mutator, human visual review, protected human gate,
   nondeterminism experiment, local-retrieval query, wrapper-level aggregate,
   final residue check, index-integrity check, checkpoint transaction, or
   authority decision.
8. Cache disable, miss, rejection, and write failure paths have uncached
   finding and status parity.
9. Legacy and candidate execution on the same key have zero unexplained
   selected-path, hard-finding, authority, status, generated-state, or receipt
   mismatch.

Uncertainty at any step yields `ineligible`, not a guessed default. Only a
complete original `PASS` may be stored in v1. `FAIL`, `WARN`,
`BLOCKED_CONFIGURATION`, skip results, prior `CACHE_HIT` results, interrupted
runs, partial receipts, and results with missing source fingerprints are never
stored.

### Manifest policy meanings

- `ineligible`: no read or write attempt is permitted.
- `exact_tree`: a conforming lookup may occur after all eligibility checks.
- `scheduled_bypass`: the gate may use exact-tree caching during ordinary
  nonfinal runs but MUST run uncached in every mandatory bypass context.

`scheduled_bypass` is not weaker keying. It uses the identical complete key and
hit validation as `exact_tree`.

### Mandatory uncached contexts

Regardless of manifest policy, no cached result may satisfy:

- the final staged-tree checkpoint comparison;
- final staged residue, whitespace, index-integrity, or index-restoration
  safeguards;
- a scheduled-full validation or authoritative CI full validation;
- the first run after cache-contract, key-schema, manifest-schema,
  receipt-schema, environment-contract, or gate-implementation change;
- a nondeterminism, failure-injection, corruption, rollback, or cache-parity
  experiment;
- a protected human review or human gate;
- an execution following a mutation until a fresh exact snapshot is captured;
  or
- an explicit operator or tracked policy bypass.

`git_diff_check` and `checkpoint_transaction` are unconditionally ineligible,
not merely scheduled bypasses.

## Provisional all-gate review

P10-T02 reviewed all 37 entries in the current manifest. The authoritative
row-level reasons and activation prerequisites are in
`research_control/tasks/RT-20260717-021/artifacts/cache_contract_review.yaml`.
This review is policy evidence only and does not alter the live manifest.

The provisional groups are:

- `exact_tree` candidate: `classify_changes`,
  `resolve_project_improvement`, `project_improvement_signals`,
  `documentation_impact`, `documentation_surface_audit`, `spec_depth`,
  `publication_validation`, `current_frontier_freshness`,
  `compact_frontier_freshness`, `dependency_graph_freshness`,
  `task_index_freshness`, `claim_graph_validation`, and `mermaid_sources`;
- `scheduled_bypass` candidate: `memory_core`, `research_control_core`,
  `research_control_diff`, `test_shard_repository`, and
  `claim_language_changed`; and
- `ineligible`: every other current gate.

The five scheduled-bypass candidates require periodic or final uncached
execution because they protect broad or changed-state invariants whose
undeclared-input and implementation-closure risk deserves repeated live
sampling. Their classification does not authorize a hit in checkpoint,
scheduled-full, or authoritative CI contexts.

Every candidate remains subject to later implementation-level closure tests.
If a declared input, transitive implementation, deterministic normalization,
or parity proof is incomplete, the later task MUST leave that row
`ineligible`.

## Cache entry and storage

### Local non-authoritative placement

Conforming entries are stored only below:

```text
.local/validation-cache/v1/objects/<first-two-key-hex>/<cache-key>.json
```

The root is ignored local state. It must not be added to a tracked registry,
used as committed transaction evidence, or treated as a canonical source.
Implementations reject symlinked roots, symlinked parent components, path
traversal, nonregular entry files, wrong ownership where detectable, and paths
whose normalized location escapes the configured root.

### Required entry fields

A `validation_cache_entry_v1` object contains:

- schema ID and version;
- contract ID;
- full canonical key material and `cache_key`;
- gate ID and original `PASS` result;
- `result_hash`, computed from the canonical complete original gate result;
- `created_at` in UTC;
- cache-writer tool name and exact version;
- full source-fingerprint manifest and its hash;
- original full-receipt local path and content hash;
- byte size;
- exact operational-only authority object; and
- no secret, token, credential, raw environment dump, or unbounded raw output.

The authority object must state:

```json
{
  "operational_validation_only": true,
  "source_authoritative": false,
  "full_receipts_authoritative": false,
  "physics_claim_authority": false,
  "ontology_authority": false,
  "proof_authority": false,
  "benchmark_authority": false,
  "gate_chair_authority": false
}
```

A cache entry is immutable after atomic publication. Writers create a regular
temporary file in the destination directory, flush and synchronize it, verify
its size and content hash, then atomically rename it to the key path. A
collision with different bytes is corruption and disables cache reads for the
invocation.

### Size and eviction

Version 1 limits are:

- maximum entry size: 16 MiB;
- maximum entry count: 2,048; and
- maximum aggregate entry size: 512 MiB.

An entry over the per-entry limit is not stored. After a successful atomic
write, maintenance removes invalid or unsupported entries first, then removes
the oldest `created_at` entries until both aggregate limits are satisfied.
Ties are resolved by ascending cache key. Access does not rewrite an immutable
entry. Failure to measure or evict safely skips the cache write and preserves
the uncached result.

Eviction changes performance only. It never changes validation status,
authority, or the underlying receipt.

## Lookup and hit validation

A reader performs these steps in order:

1. Confirm `cache_mode` is not `off`, the gate policy permits lookup, and no
   mandatory bypass applies.
2. Capture and freshness-check the exact repository snapshot.
3. Recompute every key component and the canonical cache key.
4. Resolve the bounded regular-file path without following symlinks.
5. Reject an oversized, partial, duplicate-key, unknown-field, unsupported,
   or malformed entry.
6. Verify entry key equality, gate ID, result hash, full-receipt hash, source
   fingerprints, tool version, schema versions, authority booleans, original
   `PASS`, and zero error/warning counts.
7. Recheck snapshot freshness immediately before accepting the hit.
8. Emit a new `validation_gate_result_v1` with `status: CACHE_HIT` and
   `cache_status: HIT`, preserving the original finding counts, obligation
   IDs, fingerprints, and full-receipt reference.

The new hit receipt records current lookup timestamps and duration. It does not
rewrite the original result, count as an independent execution, or add an
independent PASS. Under the evidence-identity policy it is a reference to
duplicate deterministic evidence.

Any rejection is a miss followed by uncached execution. A corrupt entry also
sets cache reads off for the rest of that invocation, records a bounded local
diagnostic, and must not change the gate's eventual status except through the
uncached result.

## Invalidation and cross-scope prohibitions

Key changes provide immutable invalidation. A new key is mandatory when any of
these changes:

- gate ID;
- working, staged, commit, or repository scope;
- selected profile, mode, selected paths, gate set, or selectors;
- exact tree fingerprint;
- base-reference name or resolved commit;
- implementation closure;
- manifest or effective configuration;
- environment fingerprint;
- dependency-specification digest;
- receipt schema; or
- cache-contract key schema.

No alias, fallback, fuzzy match, prefix match, newest-entry search, or
content-similarity rule may bridge keys. Specifically:

- working evidence cannot satisfy staged, commit, or repository evidence;
- staged evidence cannot satisfy working, commit, or another staged tree;
- one base reference cannot satisfy another;
- one profile or selected-path set cannot satisfy another;
- one environment or dependency surface cannot satisfy another;
- one implementation or manifest/configuration cannot satisfy another; and
- one repository identity cannot satisfy another even when Git tree bytes are
  equal.

Manual deletion of `.local/validation-cache/` is always safe. No tracked
record, scientific state, or transaction history may depend on an entry's
continued existence.

## Threat analysis

The required threat cases and fail-closed responses are:

| Threat | Required discriminator | Required response |
| --- | --- | --- |
| Working result offered to staged lookup | `scope.tree_state` and exact tree differ | Different key; uncached staged execution |
| Base reference moves | Resolved base commit differs | Different key |
| Environment or dependency drift | Environment or dependency digest differs | Different key |
| Gate implementation or helper changes | Implementation digest differs | Different key |
| Manifest, arguments, selectors, or switches change | Manifest or config digest differs | Different key |
| Input changes during lookup | Pre-hit freshness recheck fails | Reject hit and recapture |
| Missing or undeclared input | Complete source closure cannot be proved | Gate remains ineligible |
| Partial write or corrupt JSON | Schema, size, or result hash fails | Disable reads for invocation and run uncached |
| Cached receipt is missing or altered | Full-receipt hash fails | Reject hit and run uncached |
| Symlink or traversal attempts | Safe-root resolution fails | Reject path and run uncached |
| Cached FAIL, WARN, skip, or prior hit | Original status is not clean `PASS` | Reject entry |
| Nondeterministic or human decision | Eligibility rule fails | Gate remains ineligible |

The positive and negative canonical-key fixtures and the row-level threat
outcomes are recorded in the P10-T02 review artifact. Performance improvement
never compensates for a lost finding, wrong tree, wrong scope, authority-field
change, or unexplained legacy/planner mismatch.

## Feature switch, disable, and rollback

The only logical switch is `cache_mode` with values `off`, `read_only`, and
`read_write`. Its safe value is `off`.

- `off`: perform no lookup and no write.
- `read_only`: permit conforming reads but never publish an entry.
- `read_write`: permit conforming reads and atomic writes.

No environment variable, configuration file, wrapper default, Make target, or
CI input is defined by P10-T02. P10-T03 or later must implement exactly one
documented control surface and keep its default `off` until separately
authorized.

Rollback is:

1. set `cache_mode=off`;
2. delete `.local/validation-cache/`;
3. execute the affected gate and required profile uncached; and
4. compare status, selected paths, hard findings, authority fields, generated
   state, and receipts with the authoritative path.

Cross-tree, cross-scope, cross-environment, cross-implementation, missing
finding, corrupt-receipt acceptance, or wrong-staged-tree reuse is immediately
blocking and requires rollback. Rollback never edits completed task history,
canonical science, ontology, manuscripts, physics registries, ordinary
handoff `handoff-0740`, or the EqSrc ordinary route.

## Deferred implementation

P10-T03 owns storage, lookup, integrity, and eviction implementation. P10-T04
owns limited gate integration and parity testing. P10-T05 owns adversarial
cache review. No P10-T02 text, review row, receipt, or PASS changes those task
boundaries or activates a manifest policy.
