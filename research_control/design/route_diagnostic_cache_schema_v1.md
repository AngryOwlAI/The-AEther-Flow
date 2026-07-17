<!-- authority: control -->

# Route diagnostic cache schema v1

## Status and authority

- Schema ID: `route_diagnostic_cache_v1`
- Plan task: `P8-T07`
- Migration epoch: `shadow_planner`
- Default cache path:
  `.local/route_diagnostics/route_diagnostic_cache_v1.json`
- Canonical source authority changed: `false`
- Checkpoint authority created: `false`
- Route-freeze authority created: `false`
- Physics claim authority created: `false`

The cache is ignored local operational support. It is not a tracked
transaction receipt, a scientific source, a validator PASS, a route freeze, a
Gate Chair verdict, or a checkpoint substitute. Tracked task, job,
completion, handoff, policy, and registry records remain authoritative.

## Source fingerprint

The renderer builds a deterministic source manifest from:

1. task, job, decision, role, and claim-boundary registries;
2. each registered task record, job contract, completion record, and decision;
3. tracked research handoffs and routing-frontier records;
4. route-signature, route-orbit, payload-density, and methodology policies;
5. the direct diagnostic implementations and this schema; and
6. support-only checker reports consumed by the metrics implementation.

Each manifest entry contains a normalized repository-relative path, `present`
or `missing` status, and SHA-256 content hash when present. The source
fingerprint is SHA-256 over canonical JSON for the ordered entry list.
Canonical JSON uses sorted object keys, compact separators, UTF-8, and no
insignificant whitespace.

A cache hit requires exact equality between the cached fingerprint and a live
fingerprint. Timestamp, path subset, or Git status similarity is insufficient.
A changed, added, removed, or newly missing input makes the cache stale.

## Cache object

The JSON object contains exactly:

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_id` | string | Exactly `route_diagnostic_cache_v1`. |
| `schema_version` | integer | Exactly `1`. |
| `generated_at` | string | UTC generation time. |
| `source_fingerprint` | string | Lowercase SHA-256 of the live source manifest. |
| `source_file_count` | integer | Nonnegative manifest-entry count. |
| `missing_source_count` | integer | Nonnegative missing-entry count. |
| `warning_count` | integer | Sum of compact metric, signature, and orbit warning counts. |
| `warning_ids` | array | Sorted unique warning IDs. |
| `counts` | object | Nonnegative metric, extraction-error, warning, and legacy-candidate counts. |
| `diagnostics` | object | Compact routing warning bundle consumed by Continue Research. |
| `route_signature_summary` | object | Compact direct legacy signature comparison. |
| `route_orbit_summary` | object | Compact direct legacy orbit comparison. |
| `authority_boundary` | object | Exact non-authority values below. |

The cache deliberately excludes the full route history, full signatures,
individual warning messages, raw completion contents, and unbounded task-ID
lists. Full diagnostic receipts remain available through the direct legacy
commands.

## Required authority boundary

```json
{
  "advisory_only": true,
  "checkpoint_authority": false,
  "hard_gate_created": false,
  "physics_claim_authority": false,
  "physics_promotion_authorized": false,
  "route_freeze_authorized": false,
  "source_records_remain_authority": true,
  "support_only": true
}
```

Every warning record nested under `diagnostics` must also declare:

- `advisory_only: true`;
- `hard_gate: false`; and
- `physics_claim_authority: false`.

The signature and orbit summaries must declare the same advisory, no-hard-gate,
no-route-freeze, and no-physics-authority boundary. A cache that violates any
boundary field is invalid and its findings must not be consumed.

## Freshness states

Continue Research recognizes:

- `fresh`: schema-valid and exact source-fingerprint match;
- `missing`: no cache file;
- `stale`: valid cache with a different live source fingerprint;
- `parse_error`: unreadable or malformed JSON; and
- `invalid`: JSON that violates this schema or authority boundary.

Only `fresh` findings may be surfaced. Every other state produces a compact
advisory freshness notice with empty warning findings. Missing, stale,
malformed, or invalid cache state cannot block routing and cannot silently
fall back to an expensive historical scan.

The explicit refresh command is:

```zsh
.venv/bin/python scripts/research_control/render_route_diagnostics.py \
  --refresh --summary
```

The read-only freshness command is:

```zsh
.venv/bin/python scripts/research_control/render_route_diagnostics.py \
  --check --summary
```

Refresh uses an atomic same-directory temporary file, `fsync`, and
`os.replace`. A failed computation or write leaves the previous cache intact.

## Validation-profile boundary

Ordinary `full` profile selection does not select direct route-signature or
route-orbit diagnostics. Doctor selection remains explicit and advisory.
Affected route-policy work may select the cache-freshness diagnostic through
existing classifier tags. Scheduled or human-requested exhaustive diagnostics
may select the legacy gates through explicit role obligations.

During `shadow_planner`, the manifest remains selection metadata and legacy
execution remains authoritative. Cache freshness never satisfies checkpoint
or full-acceptance obligations.

## Required tests

P8-T07 requires:

1. warning and no-warning cache builds;
2. missing, stale, malformed, and schema-invalid cache reads;
3. exact fingerprint invalidation for task, job, completion, handoff, and
   policy changes;
4. parity between cached compact findings and direct legacy computation;
5. explicit proof that no route warning becomes a hard gate; and
6. ordinary-full exclusion with Doctor and explicit-obligation selection.
