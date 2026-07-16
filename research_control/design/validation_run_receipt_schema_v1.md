<!-- authority: control -->

# Validation Run Receipt Schema v1

## Status and authority

This document is the canonical project-control contract for compact validation
run receipts and per-gate results. It defines operational evidence only. It does
not define scientific truth, prove a physics claim, modify ontology, promote a
benchmark, or exercise Gate Chair authority.

The normative schema identifiers are:

- `validation_run_receipt_v1` for one validation invocation;
- `validation_gate_result_v1` for one selected gate result;
- `validation_finding_v1` for one shown finding; and
- `validation_artifact_reference_v1` for an artifact reference.

Unknown schema identifiers or versions fail closed. Consumers must reject an
unsupported version instead of guessing compatibility or silently dropping
fields.

## Design boundary

The receipt is intentionally compact. It carries deterministic identifiers,
counts, fingerprints, bounded shown findings, and references to fuller local
evidence. It must not embed raw command stdout, raw command stderr, secrets,
tokens, credentials, or complete source-file contents. Full validation receipts
remain local and non-authoritative unless a later tracked packet establishes a
different explicit boundary.

The schema supports `legacy`, `shadow`, and `planner` execution modes so that a
single evidence shape can be emitted while orchestration evolves. This contract
does not implement or switch those modes.

## Run receipt

A `validation_run_receipt_v1` object is a JSON object with the following
required fields. Additional fields are not permitted unless a later schema
version names them.

| Field | Type | Requirement |
|---|---|---|
| `schema_id` | string | Exactly `validation_run_receipt_v1`. |
| `schema_version` | integer | Exactly `1`. |
| `run_id` | string | Stable nonblank identifier for this invocation. |
| `mode` | string | One of `legacy`, `shadow`, or `planner`. |
| `profile` | string | Nonblank validation profile name. |
| `scope` | string | Nonblank human-readable execution scope. |
| `base_ref` | string | Nonblank comparison reference such as `HEAD`. |
| `tree_hash` | string | Algorithm-qualified Git tree hash. |
| `planner_version` | string | Nonblank planner or compatibility-adapter version. |
| `manifest_hash` | string | Algorithm-qualified digest of the selected manifest or compatibility manifest. |
| `environment_fingerprint` | string | Algorithm-qualified digest of the bounded environment contract. |
| `started_at` | string | UTC RFC 3339 timestamp ending in `Z`. |
| `finished_at` | string | UTC RFC 3339 timestamp ending in `Z`. |
| `duration_ms` | integer | Nonnegative elapsed milliseconds. |
| `status` | string | Aggregated status from the exact status vocabulary below. |
| `authority` | object | Exact operational authority boundary below. |
| `output_policy` | object | Bounded finding-display policy below. |
| `selected_gate_ids` | array of strings | Unique gates in deterministic planner or compatibility-manifest order. |
| `executed_gate_ids` | array of strings | Unique executed gates, in the order represented by `gate_results`. |
| `superseded_gate_ids` | array of strings | Unique selected gates skipped through an explicit supersedence rule. |
| `counts` | object | Aggregate gate, finding, error, warning, and status counts. |
| `gate_results` | array | One `validation_gate_result_v1` object per executed gate. |
| `artifacts` | array | Zero or more `validation_artifact_reference_v1` objects. |

`selected_gate_ids`, `executed_gate_ids`, and `superseded_gate_ids` must contain
no duplicates. Executed and superseded gates must be selected, and those two
sets must be disjoint. `gate_results[*].gate_id` must exactly equal
`executed_gate_ids` in the same order.

### Run authority

The required `authority` object is:

```json
{
  "scope": "operational_validation_only",
  "source_authoritative": false,
  "full_receipts_authoritative": false,
  "physics_claim_authority": false,
  "ontology_authority": false,
  "benchmark_authority": false,
  "gate_chair_authority": false
}
```

All boolean values above must remain `false` in schema v1. A receipt that omits
the boundary or sets any authority flag to `true` is invalid.

### Output policy

The required `output_policy` object has:

- `default_shown_findings_per_gate`: integer from 0 through 5;
- `hard_max_shown_findings_per_gate`: integer from 1 through 10 and not less
  than the default; and
- `raw_stdout_stderr_embedded`: exactly `false`.

Writers should show no more than the default. A receipt is invalid if any gate
exceeds the hard maximum. Full finding counts and a local full-receipt reference
are still mandatory even when no findings are shown.

### Aggregate counts

The required `counts` object has:

- `selected_gate_count`, `executed_gate_count`, and
  `superseded_gate_count`;
- `error_count`, `warning_count`, and `finding_count`; and
- `status_counts`, containing every exact status key with a nonnegative integer
  value.

Each count must equal the value derived from the arrays and gate results. The
run status is aggregated in this priority order:

1. `BLOCKED_CONFIGURATION` when any gate has that status;
2. `FAIL` when any gate fails and none is blocked by configuration;
3. `WARN` when any gate warns and none fails or is blocked; and
4. `PASS` for an otherwise successful mixture of `PASS`, `CACHE_HIT`, and
   applicable skip statuses.

An empty execution is `BLOCKED_CONFIGURATION` unless an explicit future schema
version defines another result.

## Gate result

A `validation_gate_result_v1` object has these required fields:

| Field | Type | Requirement |
|---|---|---|
| `schema_id` | string | Exactly `validation_gate_result_v1`. |
| `gate_id` | string | Stable ID from the registered gate catalog. |
| `severity` | string | One of `blocking`, `advisory`, or `diagnostic`. |
| `status` | string | One exact status value below. |
| `cache_status` | string | One of `NOT_ELIGIBLE`, `MISS`, `HIT`, or `BYPASSED`. |
| `input_fingerprint` | string | Algorithm-qualified digest of declared inputs. |
| `implementation_fingerprint` | string | Algorithm-qualified digest of validator implementation. |
| `started_at` | string | UTC RFC 3339 timestamp ending in `Z`. |
| `finished_at` | string | UTC RFC 3339 timestamp ending in `Z`. |
| `duration_ms` | integer | Nonnegative elapsed milliseconds. |
| `error_count` | integer | Nonnegative full error count. |
| `warning_count` | integer | Nonnegative full warning count. |
| `finding_count` | integer | Nonnegative full finding count. |
| `shown_finding_count` | integer | Exact length of `shown_findings`. |
| `findings_truncated` | boolean | True exactly when the full count exceeds the shown count. |
| `shown_findings` | array | Bounded `validation_finding_v1` objects. |
| `full_receipt` | object | Local, non-authoritative artifact reference for the full gate evidence. |
| `satisfied_obligation_ids` | array of strings | Unique stable obligation IDs satisfied by this result. |
| `child_gate_ids` | array of strings | Unique stable child-gate IDs, empty when none. |
| `mutated_paths` | array of strings | Unique repository-relative paths actually mutated, empty for read-only gates. |
| `artifact_refs` | array of strings | Unique artifact IDs resolved through the run `artifacts` array. |

The exact result status vocabulary is:

- `PASS`
- `FAIL`
- `WARN`
- `SKIP_NOT_APPLICABLE`
- `SKIP_SUPERSEDED`
- `CACHE_HIT`
- `BLOCKED_CONFIGURATION`

No synonym is valid. `CACHE_HIT` requires `cache_status: HIT`; a non-cached
result must not report `HIT`. `SKIP_SUPERSEDED` requires the gate ID to appear
in `superseded_gate_ids`. The full receipt is required for every gate and must
set both `local_only: true` and `authoritative: false`.

## Finding

A shown `validation_finding_v1` object requires:

- `schema_id`: exactly `validation_finding_v1`;
- `finding_id`: a stable uppercase identifier matching
  `[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+`;
- `level`: one of `ERROR`, `WARN`, or `INFO`;
- `code`: a stable nonblank machine code;
- `message`: a bounded, nonblank summary without raw output; and
- `artifact_ref`: an artifact ID or `null`.

Finding IDs must be unique across the run. Reordering or truncating shown
findings must not change an existing finding ID. Writers must derive IDs from a
stable rule such as gate ID, finding code, evidence location, and occurrence
key; array position alone is insufficient.

## Artifact reference

A run artifact object requires:

- `schema_id`: exactly `validation_artifact_reference_v1`;
- `artifact_id`: unique stable identifier;
- `kind`: nonblank artifact kind;
- `path`: normalized repository-relative or `.local/`-relative path without
  traversal;
- `content_hash`: an algorithm-qualified digest;
- `local_only`: boolean;
- `authoritative`: exactly `false` in schema v1; and
- `description`: bounded nonblank text.

The gate-local `full_receipt` object uses `artifact_id`, `path`, `content_hash`,
`local_only`, and `authoritative` with the same constraints. An artifact may be
tracked as a durable task receipt, but that does not make its validation claims
scientific or canonical authority.

## Determinism and safety rules

1. All timestamps use UTC and `Z`; durations are nonnegative and consistent
   with the timestamp interval to millisecond precision.
2. Hashes name their algorithm, for example `sha256:<64 lowercase hex>` or
   `git-tree-sha1:<40 lowercase hex>`.
3. Arrays representing sets are unique and use deterministic producer order.
4. Paths are relative, normalized, and contain no `..` traversal.
5. The top-level keys `stdout`, `stderr`, `stdout_tail`, and `stderr_tail` are
   forbidden. Finding messages must summarize rather than quote raw streams.
6. Secret material, tokens, credentials, environment dumps, and complete source
   files are forbidden at every level.
7. Counts describe full evidence even when `shown_findings` is truncated.
8. Consumers reject unknown schema IDs, versions, statuses, or authority fields
   fail closed.
9. Receipts are evidence about validator execution, not independent authority
   for source truth, physics, ontology, benchmark acceptance, or role decisions.

## Evidence identity and catalog linkage

Gate IDs, implementation fingerprints, input fingerprints, cache status, and
supersedence must follow
`research_control/design/validation_evidence_identity_policy_v1.md`. Registered
gate IDs and severities come from
`research_control/design/validation_gate_id_catalog_v1.md`. Environment
fingerprints follow
`research_control/design/validation_environment_contract_v1.md`, and compact
display limits remain bounded by
`research_control/design/v19_validation_output_budgets.md`.

The conforming control example is
`research_control/design/validation_run_receipt_example_v1.json`. The task-local
review and malformed-fixture validator provide implementation evidence for this
contract; they do not create runtime reporter authority.
