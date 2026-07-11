<!-- authority: control -->

# Continue-Research-Goal G5 Repaired Source-Candidate Receipt

## Entry evidence

```yaml
gate: G5
packet: repaired_source_only_selective_promotion_candidate
user_authorization: user-2026-07-11-g5-candidate-baseline-remediation-rebuild
approved_six_file_source_commit: 67dabfcb52c95e53cf68def3f06e2cb5f0d8d8a1
preserved_first_candidate_commit: d6fce5031d613e8357d52d00d9bae1e32b72e462
promotion_base_main: a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0
promotion_base_origin_main: a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0
promotion_branch: codex/continue-research-goal-promotion-rebuilt
source_candidate_commit: PENDING_CHECKPOINT
fresh_derivative_smoke_status: NOT_STARTED
```

## Non-accepting second-smoke evidence

The retained goal
`crg-20260711T152347Z-c9762ef5abdaf07b` is immutable. Its whole-file SHA-256
at remediation intake was
`fa25e3cd5a57e5259ce9346224a933aa2d492901d0e8603f841ccdfc6e688564`.
It records two consumed generations, one recursive edge, `goal_evaluation:
unmet`, final phase `terminal_guard_exhausted`, and terminal reason
`elapsed_limit`. That is valid smoke telemetry but not G5 acceptance: it is
not `terminal_complete` and does not prove a successful base case. The old
goal is not amended, relabeled, resumed, or rerun.

The smoke branch remains retained at
`e7f27aa1baf6acd555b9f97cdfc5155df419ea44`. The first source-only promotion
branch remains retained at `d6fce5031d613e8357d52d00d9bae1e32b72e462`.

## Independently isolated baseline repairs

The smoke commit `3bcd2bfddf1ff709f38507382b6c2a520af78899` cannot be
cherry-picked because its lineage contains disposable physics research and its
commit contains RT-003/004 smoke control records. Only these proven repair
surfaces are integrated:

1. RT-003 checkpoint final-index repair:
   `scripts/research_control/checkpoint_research_transaction.py` and
   `tests/test_research_control.py`.
2. RT-004 PDF-registry order-independence repair:
   `tests/test_memory_system.py`.

No `research_control/tasks/RT-20260711-002/**`, RT-003/004 smoke task record,
RT-005 physics record, handoff, program-state change, TeX source, registry row
for smoke research, or other smoke transaction is included.

## Approved six-file allowlist and hashes

| Path | SHA-256 |
| --- | --- |
| `.codex/skills/continue-research-goal/SKILL.md` | `f3f237b34e0dc4b6c8e0c9c5ef399b565abc374a3a9bf11d498c78107bb878ad` |
| `.codex/skills/continue-research-continue-goal/SKILL.md` | `ab53c52131ab0bc8296bc50c9795e3f26e6bbe723793733e56780d1623ceee08` |
| `.codex/skills/continue-research-goal/scripts/goal_state.py` | `a04d8b39cc768815dda79cf98fbc450a9b616d69c22ba26d87650dc3cfbc4823` |
| `.codex/skills/continue-research-goal/references/goal-file-schema.md` | `7593aae31da161ef5a777f39f39b0550657d23aa419b90c7f67119b6f7e7c19c` |
| `.codex/skills/continue-research-goal/goals/.gitignore` | `240a3e0d37d2e86b614063f5347eb02d4f99ca6c254de6b82871ff8d95532a7d` |
| `tests/test_continue_research_goal_state.py` | `b67b06c53d3289f2910fd4bf6ce2ade509ecbf541f336987297b0f2be240e438` |

Only `.gitignore` is eligible below the goals directory. Runtime goals,
locks, leases, temporary files, recovery sidecars, disposable research
transactions, and prior acceptance receipts are excluded.

## Binding and claim boundary

The state helper contains no hard-coded disposable root or branch. It persists
the selected root, Git common directory, non-`main` branch, execution profile,
and starting HEAD as immutable repository binding. The disposable path remains
only in the pre-promotion acceptance gate of the launcher contract.

This receipt records project-system remediation only. It changes no canonical
physics source, Distance-to-GR status, ontology, source law, metric, coupling,
Einstein-equation, benchmark, Gate Chair, or completed-derivation claim. It
authorizes no live test, push, merge, pull request, cleanup, or acceptance
verdict.
