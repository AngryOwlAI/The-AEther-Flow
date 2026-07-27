<!-- authority: control -->

# Validation Profile Policy v1

## Status and authority

- Policy ID: `validation-profile-policy-v1`
- Plan task: `P5-T07`
- Migration epoch: `shadow_planner`
- Permanent profiles: `fast`, `affected`, `checkpoint`, `full`, `doctor`
- Temporary modifier: `shadow`
- Default local profile: `fast`
- Execution authority: legacy commands remain authoritative
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims changed: `false`
- Physics, proof, ontology, benchmark, or Gate Chair authority created: `false`

This policy defines operational validation-profile semantics and the pure
planner contract. A profile name selects obligations; it is not validation
evidence and does not execute a command. Until a later authorized migration
packet activates an executor, the existing legacy commands and governed
checkpoint remain authoritative.

## Permanent profiles

Each permanent profile has exactly one purpose and one pure planner command.
The commands below explain a plan; they do not run the selected gates.

| Profile | Purpose | Scope | Relative cost | Default use | Planner command |
| --- | --- | --- | --- | --- | --- |
| `fast` | Run the lowest-cost local edit loop over changed operational surfaces. | Working-tree changed paths | Lowest | Default local development loop | `.venv/bin/python -m scripts.validation.cli plan --profile fast --paths <changed-path> --explain` |
| `affected` | Run fast checks plus blocking validators and focused integration tests affected by the classified change. | Working-tree affected dependency closure | Bounded | Precheckpoint implementation acceptance | `.venv/bin/python -m scripts.validation.cli plan --profile affected --paths <changed-path> --explain` |
| `checkpoint` | Generate governed derivatives and validate the final staged transaction before commit. | Generated working state and final staged tree | Transactional | One governed checkpoint transaction | `.venv/bin/python -m scripts.validation.cli plan --profile checkpoint --paths <staged-path> --explain` |
| `full` | Run every nontransactional blocking validation gate and every repository test shard without change-family filtering. | Repository and scheduled exhaustive coverage | Highest | Scheduled full coverage and explicit exhaustive review | `.venv/bin/python -m scripts.validation.cli plan --profile full --paths <changed-path> --explain` |
| `doctor` | Inspect local retrieval, route, environment, and other non-authoritative operational health. | Local-only and advisory diagnostics | Diagnostic | Explicit troubleshooting only | `.venv/bin/python -m scripts.validation.cli plan --profile doctor --scope local_retrieval --explain` |

`fast` owns classifier, syntax, changed-claim, whitespace, and affected-unit-test
capabilities. `affected` adds affected blocking validators and focused
integration tests. The manifest maps stable gates; P5-T08 owns the detailed
change-family-to-test matrix. A missing or unknown governed path therefore
falls back to unfiltered `full` rather than being silently omitted.

## Checkpoint boundary

`checkpoint` is the only permanent profile with repository acceptance
authority, and that authority exists only inside the governed checkpoint
transaction. It must preserve all of these obligations:

- `checkpoint_transaction`
- `final_staged_allowlist`
- `authority_validation`
- `residue_validation`
- `whitespace_validation`

Precheckpoint working-tree evidence never satisfies the final staged tree.
Profile selection never overrides a human gate. The checkpoint may generate
registered derivatives before staging, but acceptance is evaluated against the
actual staged transaction after generation.

When a checkpoint is invoked with an explicit AgentJob identity, that same
identity is propagated to both working-tree and staged
`research_control_diff` validation. The validator resolves that exact active
or completed job and fails closed when it is missing or ineligible. Only
standalone diff validation without an explicit identity retains the
latest-eligible-job fallback. A later unrelated AgentJob therefore cannot
silently replace the allowlist authority selected by the checkpoint.

## Repository-test checkpoint cadence

An ordinary checkpoint does not unconditionally run
`test_shard_repository`. The checkpoint helper adds that explicit blocking
obligation whenever the working transaction crosses a boundary of ten
completed scientific AgentJobs after
`AJ-RT-20260726-011-001`. The anchor is ordinal zero, so the first scheduled
repository shard occurs after ten later scientific jobs.

A research process for this cadence is one completed AgentJob whose registered
`role_kind` begins with `scientific_`. Project-system, documentation, routing,
and recovery AgentJobs do not advance the count. The helper compares the
working `AGENT_JOB_REGISTRY.csv` sequence with the sequence already committed
in `HEAD`. A recovery carrying an uncommitted tenth scientific job therefore
retains the repository-test obligation, while later project-system work does
not repeat it after that boundary is committed.

This cadence does not suppress affected validation. Changes tagged as tests,
test shards, traceability inputs, proof-normal-form checks, metric-use TeX, or
scientific checkers still select the repository shard immediately. Explicit
`full`, scheduled-full composition, and unknown-path fail-safe selection also
remain unchanged. Missing anchor, role-kind, committed-registry, or sequence
parity evidence fails safe by selecting the repository shard.

## Full and scheduled coverage

`full` is unfiltered across all nontransactional blocking validation gates and
includes the repository test shard plus scheduled project-control coverage.
The `checkpoint_transaction` gate is intentionally excluded from `full`: it is
a commit-producing transaction, not an exhaustive validator. Exhaustive review
does not authorize a commit.

Conditional changed-path gates remain present in the manifest, but the profile
resolver supplies their blocking obligations when `full` is requested. This
prevents an empty diff or narrow path set from filtering exhaustive coverage.
Performance budgets cannot remove a blocking gate, test shard, or scheduled
coverage obligation from `full`.

## Doctor separation

`doctor` contains only advisory or local-only operational diagnostics. It may
inspect local retrieval, route signatures and orbits, environment health, and
other troubleshooting state. Its results:

- cannot satisfy checkpoint obligations;
- cannot establish tracked-repository acceptance;
- cannot replace a blocking validator or protected human review;
- cannot block physics or repository authority unless a separate explicit
  maintenance task opts into a named blocking obligation;
- cannot become canonical source, proof, ontology, benchmark, or Gate Chair
  evidence.

If a doctor request encounters an unknown governed tracked path, the planner
fails safe to `full`; it does not treat the path as diagnostic-only.

## Temporary shadow modifier

`shadow` is a modifier, not a sixth profile. It requests a legacy/planner
comparison receipt for the same profile plan. Applying `shadow` must not change
the profile, gate membership, prerequisites, evidence identity, scope, tree
state, exit status, or authority. An unexplained comparison mismatch is
blocking and restores the legacy result as authoritative.

The modifier is temporary. Removing it after an authorized migration changes
comparison behavior only; it does not delete or rename the five permanent
profiles.

## Membership and evidence rules

1. The five names are closed. Unknown names and `shadow` as a profile fail
   configuration validation.
2. Profile membership is deterministic from the registered manifest and
   explicit obligations.
3. `full` includes every nontransactional blocking gate and the repository
   test shard. `checkpoint` includes all final staged safeguards.
4. `doctor` contains no blocking gate and has no checkpoint-obligation overlap.
5. Advisory and local-only results cannot satisfy blocking obligations.
6. Working, staged, commit, repository, and local-retrieval scopes remain
   distinct evidence identities.
7. A mutating result cannot validate its own post-mutation state.
8. Cache, compact output, wrapper success, and profile selection are not
   independent evidence.
9. Unknown governed paths and unexplained legacy/planner mismatches fail safe.
10. No profile can expand a role, skill, human gate, claim, or physics authority.

## Audit contract

`scripts/validation/profiles.py audit --json` emits the deterministic
`validation_profile_membership_audit_v1` record. It includes the manifest hash,
profile definitions and membership, obligation coverage, representative empty
and changed-path scenarios, full and checkpoint safeguards, doctor separation,
and affected blocking-gate legacy compatibility.

The task-local durable copy is
`research_control/tasks/RT-20260716-013/artifacts/profile_membership_audit.json`.
It is operational control evidence only. Raw validator logs remain in their
own receipts and are not embedded into the compact profile audit.

## Stop and rollback conditions

- Stop if `affected` can omit an unknown governed path.
- Stop if `full` can filter a nontransactional blocking gate or repository test
  shard.
- Stop if `checkpoint` omits final staged allowlist, authority, residue,
  whitespace, or transaction checks.
- Stop if `doctor` contains a blocking gate or satisfies checkpoint evidence.
- Stop if `shadow` changes gate membership or evidence identity.
- Stop on a missing hard finding, wrong staged tree, unexplained comparison
  mismatch, human-gate bypass, or write outside the authorized task allowlist.
- Roll back rollout defaults without deleting these definitions if a later
  executor migration fails.
- Performance improvement never compensates for lost failure-mode coverage.

This policy defines no scientific result. Validation PASS cannot establish
physical truth, proof, ontology adoption, source-law adoption, benchmark
promotion, a Gate Chair verdict, or completion of a derivation.
