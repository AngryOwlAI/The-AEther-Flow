<!-- authority: control -->

# Agent Validation-Output Consumption Policy v1

## Purpose and Authority

This policy defines how local agents consume operational validator output. It
is a project-control context-management contract. It does not change validator
selection, decision rules, severities, finding taxonomies, exit codes, receipt
schemas, checkpoint gates, or scientific authority.

Validation evidence remains operational only. A compact summary, full receipt,
or PASS result is not source authority, physics proof, ontology authority,
benchmark authority, Gate Chair authority, or a completed-derivation claim.

## Summary-First Sequence

1. Request or retain the compact summary first.
2. Read status, gate IDs, counts, the receipt path, and the tree or input
   fingerprint when present.
3. For PASS, stop output inspection unless a named audit, parity check, schema
   validation, or checkpoint contract requires receipt-level evidence.
4. For WARN, FAIL, or BLOCKED_CONFIGURATION, select only the failed or warning
   gate group and the relevant finding IDs.
5. Expand only the selected structured receipt section. If the evidence is
   line-oriented, read a bounded tail of at most 200 lines and narrow further
   before requesting more.
6. Stop expanding when the selected finding is explained or a distinct bounded
   hypothesis requires another section.

Agents must not open, print, embed, or retransmit the entire full receipt by
default. Full JSON is an exception for a named audit or compatibility check,
not the routine PASS path.

## Polling and Long-Running Commands

When a command yields, wait or poll only when the process may have produced new
state. Preserve the last observed revision, chunk, or output marker when the
tool supports one. Do not repeatedly poll when that would retransmit unchanged
output. Prefer a 30-to-60-second bounded wait for a known long-running gate,
then inspect only newly returned output.

## Failure Expansion

Failure diagnosis begins from stable gate and finding IDs. Expand evidence in
this order:

1. the compact gate group;
2. the named finding IDs and their bounded messages;
3. the referenced receipt section or artifact;
4. a bounded raw-output tail only when the structured evidence is insufficient.

Do not broaden from one failing gate to unrelated PASS gates. Do not repeat a
validator merely to obtain the same full output. A retry requires a changed
condition, a new hypothesis, or a missing evidence field that the retry is
expected to produce.

## Completion Evidence

Task completions record compact references rather than full logs. Each relevant
gate entry must include:

```yaml
gate_id: "<stable gate id>"
status: "<PASS WARN FAIL or BLOCKED_CONFIGURATION>"
receipt_path: "<repo-relative or .local-relative path>"
content_hash: "sha256:<64 lowercase hex>"
counts:
  error_count: 0
  warning_count: 0
  finding_count: 0
relevant_finding_ids: []
tree_fingerprint: "<algorithm-qualified digest when available>"
```

The completion may summarize the command and outcome, but it must not embed
full stdout, stderr, environment dumps, or complete receipt JSON. When no
finding is relevant, `relevant_finding_ids` is an explicit empty list.

## Local Full-Receipt Boundary

`.local/validation-receipts` is the default local full-receipt store. It is
untracked, non-authoritative cache and diagnostic state. It may be regenerated
or removed without changing canonical project knowledge. Its files must not be
registered as canonical sources, committed as transaction evidence, or used to
override tracked source, registry, task, handoff, validator, or checkpoint
state.

A task may preserve a compact tracked review or audit report that references a
local receipt by path and hash. That reference does not promote the local file
to authority.

## Audit Exceptions

Receipt-level inspection is allowed when a task explicitly requires schema
validation, legacy/planner shadow comparison, failure-mode equivalence,
incident diagnosis, or checkpoint audit. Even then, agents should select
bounded fields or sections first and keep complete raw data on disk rather than
in the completion or conversation.

## Stop Conditions

Stop and report the narrow blocker when:

- the compact summary cannot identify the failing gate or receipt;
- the receipt path or content hash is missing for a required audit;
- bounded expansion cannot recover the relevant finding evidence;
- receipt evidence conflicts with the represented exit status or staged tree;
- the only proposed workaround is unbounded output ingestion or repeated
  unchanged polling; or
- validation output is being treated as source or scientific authority.
