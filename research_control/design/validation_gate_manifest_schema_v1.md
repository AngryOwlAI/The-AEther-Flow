<!-- authority: control -->

# Validation gate manifest schema v1

## Status and authority

- Schema ID: `validation_gate_manifest_schema_v1`
- Manifest schema ID: `validation_gate_manifest_v1`
- Plan task: `P5-T01`
- Migration epoch: `shadow_planner`
- Status: `active-schema`
- Canonical seed: `research_control/design/validation_gate_manifest_v1.yaml`
- Legacy execution authority changed: `false`
- Planner authority activated: `false`
- Cache or supersedence activated: `false`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims or physics authority changed: `false`

This contract defines the machine-readable shape and fail-closed invariants for
the declarative validation-gate manifest. It does not populate the gate
inventory, select or execute gates, alter legacy command authority, activate
caching or supersedence, or authorize a scientific conclusion. P5-T02 owns the
first populated manifest.

## Serialization and manifest identity

The `.yaml` file uses a JSON object because JSON is a YAML 1.2 subset. This
keeps parsing dependency-free and prevents loader-specific YAML coercion.
Consumers must parse the complete file as UTF-8 JSON and reject duplicate keys,
trailing documents, comments inside the file, non-finite numbers, and unknown
fields.

The logical manifest identity is:

```text
manifest_hash = SHA-256(canonical_json(manifest))
```

`canonical_json` is UTF-8 JSON with object keys sorted lexicographically,
separators `,` and `:`, JSON escaping, no insignificant whitespace, and no
trailing newline in the hashed bytes. Array order is significant. Producers
must sort set-like arrays before serialization; consumers must not silently
repair non-deterministic input.

## Top-level manifest object

The manifest is an object with exactly these fields:

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_id` | string | Exactly `validation_gate_manifest_v1`. |
| `schema_version` | integer | Exactly `1`. |
| `manifest_id` | string | Exactly `validation-gate-manifest-v1`. |
| `migration_epoch` | string | One of `legacy`, `legacy_consolidated`, `shadow_planner`, `planner_authoritative`, or `legacy_retired`. |
| `population_status` | string | One of `schema_seed_pending_p5_t02` or `populated`. |
| `execution_authority` | string | One of `legacy` or `manifest_planner`; the P5-T01 seed must use `legacy`. |
| `authority` | object | Exact non-promotion boundary below. |
| `gates` | array | Unique gate objects in deterministic manifest order. |

The P5-T01 seed is valid only when `population_status` is
`schema_seed_pending_p5_t02`, `execution_authority` is `legacy`, and `gates` is
empty. A manifest with `population_status: populated` must contain at least one
gate. Empty seed status must never be interpreted as complete gate coverage.

The required `authority` object is:

```json
{
  "benchmark_authority": false,
  "gate_chair_authority": false,
  "ontology_authority": false,
  "operational_validation_only": true,
  "physics_claim_authority": false,
  "proof_authority": false,
  "source_authoritative": false
}
```

Unknown authority fields or a different boolean value fail closed.

## Gate object

Every populated gate is an object with exactly these fields:

| Field | Type | Requirement |
| --- | --- | --- |
| `gate_id` | string | Stable lowercase catalog ID; unique in the manifest. |
| `description` | string | Nonblank bounded operational description. |
| `owner_role` | string | Nonblank versioned execution owner such as `validator-engineer@0.2.0`. |
| `adapter` | string | Nonblank registered or compatibility adapter identifier. |
| `command_compatibility` | array of strings | At least one current command or wrapper represented by the adapter. |
| `input_globs` | array of strings | Unique normalized repository-relative input selectors. |
| `output_globs` | array of strings | Unique normalized repository-relative output selectors. |
| `global_invariant_justification` | string or null | Required nonblank text when a repository-global glob such as `**` is used; otherwise null or bounded text. |
| `scopes` | array of strings | Nonempty subset of `working`, `staged`, `commit`, `repository`, and `local_retrieval`. |
| `severity` | string | One of `blocking`, `advisory`, or `local_only`. |
| `mutating` | boolean | Whether the adapter may change working files or generated outputs. |
| `cost_class` | string | One of `fast`, `medium`, or `slow`. |
| `prerequisites` | array of strings | Unique gate IDs that must precede this gate. |
| `supersedes` | array of objects | Conditional supersedence declarations below. |
| `satisfies_obligations` | array of strings | Unique stable obligation IDs satisfied by a conforming result. |
| `profiles` | array of strings | Nonempty subset of `fast`, `affected`, `checkpoint`, `full`, and `doctor`. |
| `path_tags` | array of strings | Unique stable classifier tags used for affected selection. |
| `selection` | object | Explicit selection predicate below. |
| `timeout_seconds` | integer | Positive and no greater than 86400. |
| `parallel_group` | string | Nonblank deterministic scheduling group. |
| `cache_policy` | string | One of `ineligible`, `exact_tree`, or `scheduled_bypass`. |
| `receipt_schema` | string | Exactly `validation_gate_result_v1`. |
| `test_shard` | string | Nonblank regression shard or `full_profile_acceptance` path. |

Profile membership and severity are independent fields. A blocking gate is not
implicitly in every blocking profile, and an advisory gate is not implicitly
excluded from `full`. Selection must use the declared profile and predicate,
not infer membership from severity.

### Selection predicate

`selection` contains exactly:

- `operator`: `all` or `any`; and
- `conditions`: one or more condition objects.

Each condition contains exactly `condition_id`, `kind`, and `values`.
`condition_id` is a stable nonblank lowercase identifier. `kind` is one of:

- `always`;
- `profile_selected`;
- `path_tag_any`;
- `path_tag_all`;
- `explicit_scope`;
- `changed_registered_tex_pdf_required`;
- `registered_mermaid_changed`;
- `publication_surface_changed`;
- `graph_inputs_changed`;
- `task_index_inputs_changed`;
- `traceability_inputs_changed`; or
- `scientific_checker_family`.

`values` is a unique string array. It must be empty for `always` and nonempty
for every other kind. These kinds provide explicit conditions for conditional
PDF, Mermaid, publication, graph, task-index, traceability, and scientific
checker selection without embedding executable code in the manifest.

### Supersedence declaration

Every `supersedes` item contains exactly:

- `gate_id`: a different gate ID present in the same manifest;
- `predicate_id`: a nonblank stable predicate from a tracked supersedence
  contract; and
- `status`: `policy_only_inactive` or `active`.

The schema records declarations only. A planner must not apply an active entry
until the separate supersedence and evidence-identity contracts authorize it.
Unknown targets, self-supersedence, duplicate targets, missing predicates, or
cycles in the prerequisite graph fail closed.

## Path and glob rules

1. Paths and globs are repository-relative, use `/`, and contain no absolute
   prefix, backslash, NUL, empty segment, `.` segment, or `..` segment.
2. Duplicate globs are invalid.
3. The global globs `**` and `**/...` require a nonblank
   `global_invariant_justification` naming the audited invariant.
4. A broad glob is never justified solely by convenience or performance.
5. Empty `output_globs` are valid for read-only validators. Empty
   `input_globs` are valid only when selection is explicit and the adapter has
   no repository input; the producer must still preserve a nonblank command
   compatibility entry.

## Graph and reference integrity

- Gate IDs are unique.
- Every prerequisite and supersedence target resolves within the manifest.
- Prerequisite edges are acyclic.
- Set-like arrays contain unique strings.
- `selection.conditions[*].condition_id` values are unique per gate.
- `satisfies_obligations`, `profiles`, `path_tags`, and `test_shard` are
  declarative metadata and do not create role or execution authority.
- Every blocking gate names a nonblank `test_shard`; this schema requires the
  field for all severities to make later severity changes fail closed.

## Unknown and malformed data

Consumers reject unknown top-level, authority, gate, selection, condition, and
supersedence fields. They also reject unknown enum values, wrong types, empty
required strings, nonpositive timeouts, duplicate IDs, unresolved references,
cycles, and unsupported schema versions. A failure is
`BLOCKED_CONFIGURATION`; consumers must not guess defaults or omit the gate.

## P5-T01 acceptance and deferred work

The focused contract test must validate:

- the canonical empty seed;
- representative good gate objects;
- duplicate IDs, prerequisite cycles, unknown prerequisites, invalid
  supersedence, unsupported scopes, missing test shards, and unjustified broad
  globs;
- deterministic canonical serialization and hashing; and
- representability of all 37 nodes in
  `v19_legacy_validation_invocation_graph.json` through the stable catalog map.

P5-T02 owns gate population and complete legacy coverage. P5-T03 and later own
classifier tags, planning, obligation compilation, deduplication, profiles,
execution, caching, and cutover. This schema does not authorize any of those
behaviors and creates no physics, ontology, proof, benchmark, or Gate Chair
authority.
