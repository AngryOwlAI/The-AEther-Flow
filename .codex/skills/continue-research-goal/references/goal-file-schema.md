<!-- authority: control -->

# Continue-Research Goal Record Schema v1

## Purpose and Authority

This schema governs the ignored local state used by
`continue-research-goal` and `continue-research-continue-goal`. A goal record
is an orchestration continuation token. It is not physics, ontology,
benchmark, project-control task state, scientific evidence, or claim authority.

Tracked `research_control/`, registered canonical sources, registries, Git,
validators, and checkpoints remain authoritative. Goal files, task prose,
`.local/`, generated wiki notes, PDFs, and HTML cannot prove research
completion by themselves.

The deterministic implementation is
`.codex/skills/continue-research-goal/scripts/goal_state.py`. It may validate
and mutate only the ignored state described here. It has no authority to call
task tools, invoke research, select an AgentJob, edit tracked research state,
commit, push, merge, or decide whether a scientific goal is complete.

## Filesystem Boundary

Tracked runtime sources are:

```text
.codex/skills/continue-research-goal/SKILL.md
.codex/skills/continue-research-goal/scripts/goal_state.py
.codex/skills/continue-research-goal/references/goal-file-schema.md
.codex/skills/continue-research-goal/goals/.gitignore
.codex/skills/continue-research-continue-goal/SKILL.md
```

Dynamic local files are restricted to:

```text
.codex/skills/continue-research-goal/goals/goal-*.md
.codex/skills/continue-research-goal/goals/goal-*.lock
.codex/skills/continue-research-goal/goals/goal-*.tmp
.codex/skills/continue-research-goal/goals/goal-*.dispatch-recovery.json
.codex/skills/continue-research-goal/goals/.relay-lease.json
.codex/skills/continue-research-goal/goals/.relay-lease.lock
```

The nested `.gitignore` contains `*` and `!.gitignore`. Dynamic files must stay
ignored, untracked, absent from Markdown registries, generated wiki outputs,
checkpoints, and promotion candidates, and retained until explicit cleanup.

A goal path must resolve to a regular, single-link, non-symlink direct child of
the exact goals directory. Its name is `goal-<goal_id>.md`; the embedded goal
ID and filename must match. Path traversal, a symlink, a hard-link alias, or a
different parent is corrupt state.

## Serialization

Each goal file contains JSON inside `---` YAML frontmatter delimiters, followed
by a derived Markdown completion-contract and journal rendering. JSON is a
YAML 1.2 subset and permits exact dependency-free string round-tripping. The
helper rejects any body or serialization drift by rendering the parsed record
again and comparing all bytes.

Canonical JSON uses UTF-8, lexicographically sorted keys, no insignificant
whitespace, and JSON separators `,` and `:` for hashing. Display JSON may be
indented. SHA-256 values are lowercase hexadecimal.

The user-supplied goal is canonicalized only by replacing CRLF and CR with LF.
It is not trimmed, dedented, Unicode-normalized, or given a helper-added final
newline. `goal_sha256` hashes those exact UTF-8 bytes. The frontmatter
`goal_text` field is the only canonical goal copy.

## Required Record

```yaml
schema_version: "continue-research-goal.v1"
goal_id: "crg-<YYYYMMDDTHHMMSSZ>-<random lowercase hex>"
goal_text: "<exact canonical user text>"
goal_sha256: "<sha256>"
completion_contract:
  interpretation: "<operational interpretation>"
  required_evidence:
    - "<canonical success evidence>"
  user_confirmed_when_ambiguous: false
completion_contract_sha256: "<canonical JSON sha256>"
amendments: []
created_at: "<UTC>"
deadline_at: "<UTC>"
guards:
  max_continue_passes: <positive integer>
  max_repeated_state_fingerprints: 1
  max_live_continuations: 1
  handoff_ready_timeout_seconds: 60
repository_binding:
  execution_profile: "acceptance_test | production_profile"
  root: "<resolved worktree root>"
  branch: "<non-main branch>"
  environment_mode: "local"
  git_common_dir: "<resolved Git common directory>"
  starting_head: "<commit>"
authorization:
  fresh_recursive_threads_explicitly_requested: true
state:
  revision: 1
  phase: "initialized"
  current_generation: 0
  passes_consumed: 0
  active_lease: <lease object or null>
  goal_evaluation: "unmet | met | indeterminate"
  last_canonical_fingerprint: "<sha256>"
  canonical_fingerprint_history:
    - "<initial sha256>"
  terminal_reason: null
generations: {}
handoff:
  status: "none"
  generation: 1
  token: null
  idempotency_key: null
  predecessor_thread_id: null
  successor_thread_id: null
journal: []
updated_at: "<UTC>"
```

The schema may add fail-closed diagnostic fields. It may not omit or weaken the
semantics above.

## Immutable and Append-Only Data

The following original values never change in place:

- `goal_text` and `goal_sha256`;
- `completion_contract` and `completion_contract_sha256`;
- `guards`;
- `repository_binding`; and
- every finalized journal entry and receipt.

An explicit human-authorized completion-contract or guard amendment appends:

```yaml
kind: "completion_contract | guards"
user_authorization: "<exact instruction or approval reference>"
created_at: "<UTC>"
prior_effective_sha256: "<hash>"
new_value: <new contract or allowed guard fields>
new_sha256: "<effective-value hash>"
```

Contract amendments replace only the effective completion contract. Guard
amendments may only extend `max_continue_passes` or `deadline_at`; they cannot
weaken human-gate, validation, authority, identity, duplicate, or branch stops.
Changing the goal itself always requires a new goal record.

## Generation Record

Every `generations["N"]` entry persists permanently and contains at least:

```yaml
generation: N
handoff_token: "<random token>"
idempotency_key: "<goal_id>:N"
phase: "<generation phase>"
lease_token: "<current generation holder token>"
invocation_consumed: false
invocation_state: "not_authorized | authorized | returned | unknown"
consumed_at: null
returned_at: null
before_fingerprint: "<sha256>"
after_fingerprint: null
pending_step_result: null
finalized_receipt_hash: null
terminal_or_successor_outcome: null
claimed_at: null
successor_thread_id: null
```

`invocation_consumed=true` is irreversible and increments
`state.passes_consumed` once before research. It proves at-most-once
authorization, not a returned invocation. Only `invocation_state=returned`
plus direct execution evidence supports receipt count `1`. An unresolved
consumption/call crash gap uses `unknown`, never a guessed exact count.

No generation is deleted, reset, or reused when the generation counter
advances. One generation may link to at most one finalized step receipt and one
successor ID.

## Cooperative Lease Pair

`.relay-lease.json` contains:

```yaml
schema_version: "continue-research-goal-worktree-lease.v1"
repository_fingerprint: "<hash of root and Git common directory>"
goal_id: "<owner>"
generation: <nonnegative integer>
holder_kind: "launcher | continuation | successor_reserved"
holder_token: "<opaque token>"
transaction_id: "<shared transaction nonce>"
acquired_at: "<UTC>"
heartbeat_at: "<UTC>"
expires_at: "<diagnostic UTC only>"
```

`state.active_lease` uses the same identity, generation, holder, token,
transaction, and timestamps. Under `.relay-lease.lock`, a state change writes a
shared transaction nonce to the goal and global lease, fsyncs each atomic
replacement and the directory, then verifies parity. This is a recoverable
logical two-file transaction, not a claim of impossible multi-file atomicity.

A mismatch blocks every conforming writer. Expiry is diagnostic and never
permits lease stealing. A crash-created mismatch, missing side, or quarantine
requires explicit recovery using terminal-holder and canonical repository
evidence. Initialization scans for unreconciled per-goal leases even when the
global lease is absent.

## Journal Chain

Every journal entry contains:

```yaml
sequence: <one-based integer>
kind: "<event or step_receipt>"
payload: <canonical event object>
prior_hash: "<prior entry hash or null for genesis>"
entry_hash: "<sha256 of kind, payload, prior_hash, sequence>"
```

Entries are append-only. Recovery, amendments, launcher handoffs, and child
wait diagnostics are non-step events. Exactly one `step_receipt` may exist per
execution generation. A rejected frame that never claims a generation appends
no receipt. The generation's `finalized_receipt_hash` must equal the matching
journal entry hash.

## Required Step Receipt

A finalized execution receipt contains:

- goal ID and generation;
- handoff token and idempotency key;
- predecessor and successor discussion IDs when known;
- start and finish timestamps;
- repository root, branch, before HEAD, and after HEAD;
- before and after canonical fingerprints;
- `continue-research` invocation count `0`, `1`, or `unknown`;
- AgentJob ID or an explicit valid zero-AgentJob reason;
- active task ID, latest handoff ID, checkpoint commit, and relevant hashes;
- validator command outcomes;
- goal evaluation `unmet`, `met`, or `indeterminate`;
- progress summary and remaining work;
- recursive or terminal decision; and
- the hash-linked journal entry hash and prior hash.

A recursive step keeps its receipt pending through `continuation_required` and
`successor_intent`. Confirmed successor recording atomically adds the successor
ID, finalizes that one receipt, transitions to `successor_created`, and
transfers both leases. A definitive or ambiguous dispatch result instead
finalizes the same pending receipt with the mapped terminal outcome.

The uncertain-invocation edge is the sole terminal exception: it appends an
`invocation_uncertain` event, leaves the receipt pending, and quarantines both
leases. Only explicit recovery after terminal-holder proof may finalize the
one receipt as `1` or `unknown`.

## Phases

Nonterminal phases are:

```text
initialized
successor_intent
successor_created
step_active
step_verifying
step_verified
continuation_required
recovery_pending
```

The success base case is `terminal_complete`.

Non-success terminals are:

```text
terminal_awaiting_human
terminal_capability_blocked
terminal_guard_exhausted
terminal_no_progress
terminal_validation_failed
terminal_handoff_ambiguous
terminal_handoff_timeout
terminal_duplicate_detected
terminal_corrupt_state
terminal_failed
terminal_cancelled
```

Terminal phases have no automatic outgoing edge. `terminal_complete`,
`terminal_duplicate_detected`, `terminal_corrupt_state`, and
`terminal_cancelled` are absorbing. Other terminals may enter
`recovery_pending` only through explicit human-authorized recovery and
canonical/lease reconciliation.

## Normal Transitions

Only these normal edges are legal:

```text
absent -> initialized
initialized -> successor_intent
successor_intent -> successor_created
successor_intent -> terminal_failed
successor_intent -> terminal_handoff_ambiguous
successor_intent -> terminal_duplicate_detected
successor_intent -> terminal_handoff_timeout
successor_created -> step_active
step_active -> step_active (one irreversible invocation consumption)
step_active -> step_verifying (directly observed return)
step_active -> terminal_awaiting_human (uncertain return; leases quarantined)
step_active -> mapped pre-execution terminal (zero-invocation receipt)
step_verifying -> step_verified
step_verified -> terminal_complete
step_verified -> mapped protected terminal
step_verified -> continuation_required
continuation_required -> successor_intent
```

Every unlisted normal edge is rejected without mutation. In particular, a
stale, duplicate, claimed, or consumed generation cannot re-enter
`step_active`, and no terminal automatically resumes.

## Recovery Transitions

Only these explicit edges are legal:

```text
selected recoverable terminal -> recovery_pending
recovery_pending -> successor_created (adopt one uniquely proven live child)
recovery_pending -> successor_intent (new generation and token)
recovery_pending -> mapped terminal (reconciled consumed result)
recovery_pending -> continuation_required (returned result directly proven)
recovery_pending -> terminal_cancelled
```

Recovery discussions execute zero research. They append a hash-linked event
naming exact authorization, prior terminal phase, canonical evidence, old/new
revisions, and selected edge. They never erase a terminal reason from history,
rewrite a receipt, reuse a consumed generation, or add a second receipt.

An active unconsumed generation may be abandoned only after direct proof that
the prior holder is terminal. It receives one zero-invocation receipt and
releases both leases. A consumed generation is never rerun. Reconciliation
finalizes count `1` only with direct returned-invocation evidence; otherwise it
uses `unknown` and stops.

## Deterministic Stop Mapping

```text
goal met                                      -> terminal_complete
human gate or indeterminate evaluation       -> terminal_awaiting_human
missing or changed capability                 -> terminal_capability_blocked
pass, elapsed, repetition, or budget guard    -> terminal_guard_exhausted
no action, no progress, or repeated state     -> terminal_no_progress
validator, checkpoint, or dirty-state failure -> terminal_validation_failed
ambiguous dispatch                            -> terminal_handoff_ambiguous
child timeout or ended-unclaimed child        -> terminal_handoff_timeout
multiple successors or competing claims       -> terminal_duplicate_detected
schema, hash, journal, path, or symlink fault  -> terminal_corrupt_state
branch/repository mismatch or interruption    -> terminal_failed
explicit cancellation                         -> terminal_cancelled
```

A guard or protected stop is never relabeled as successful completion.

## Canonical Repository Fingerprint

Hash one canonical JSON object using UTF-8, lexicographically sorted keys,
deterministic list ordering, and no timestamps. It includes:

- resolved worktree root, Git common directory, and branch;
- HEAD and exact `git status --porcelain`;
- `research_control/program_state.yaml` hash plus active task, active AgentJob,
  status, latest handoff, and next action;
- latest handoff ID and YAML/Markdown hashes;
- active task and AgentJob IDs resolved from tracked files and registries;
- normalized `continue_research.py` boundary and reason;
- required validator names and pass/fail outcomes; and
- checkpoint outcome and commit when present.

Exclude discussion prose, task titles, goal/native-goal state, relay runtime
files, locks, temporary files, recovery sidecars, `.local/`, generated wiki
notes, timestamps, and other non-authoritative telemetry.

Store the complete history. A candidate equal to the most recent fingerprint
is `unchanged`; a candidate equal to any earlier fingerprint is `repeated`.
Both block recursion, including an `A -> B -> A` cycle.

## Crash Windows

- Intent before create: do not claim; recovery proves whether a child exists.
- Create before ID record: retry only the idempotent record-only operation;
  never call create again.
- ID record before predecessor exit: successor may claim; predecessor performs
  no calls after the record operation.
- Claim before consumption: after terminal-holder proof, mark
  `abandoned_unconsumed`, finalize count `0`, and use a new generation only
  after explicit recovery.
- Consumption before research or uncertain call boundary: never rerun; record
  `unknown` unless a returned invocation is directly proved.
- Research return before receipt: reconcile canonical evidence and finalize the
  existing generation once without executing research again.

If a concrete created task ID cannot be persisted after bounded record-only
retries, write an ignored `goal-*.dispatch-recovery.json` containing goal ID,
generation, token, idempotency key, returned ID, expected revision, error, and
timestamp. The child remains unauthorized and times out. Never store a secret
in this sidecar.

## CLI Operations

All helper calls use:

```text
.venv/bin/python .codex/skills/continue-research-goal/scripts/goal_state.py \
  --goals-dir .codex/skills/continue-research-goal/goals <subcommand>
```

Normal subcommands are `initialize`, `validate`, `reserve-successor`,
`record-successor`, `claim`, `consume`, `returned`, `uncertain`,
`verify-step`, `decide-step`, and `dispatch-failure`. Recovery subcommands are
`begin-recovery`, `amend-contract`, `amend-guards`, and `cancel`; the Python API
also exposes terminal-holder-proof operations for abandoned or consumed crash
reconciliation.

Every state-changing call requires `expected_revision` after initialization.
Conflicts return a blocked error and make no mutation. The helper never calls a
discussion API or research skill.

## Security and Privacy

Goal records are retained in plaintext locally and can be force-added by a
human. Do not store credentials, tokens, private keys, private personal data,
or other secrets. The helper rejects common secret forms, but the invoking
skill must perform the semantic redaction check before initialization.
