# P6-T06 Skill Profile Wrapper Audit

## Outcome

The four principal repo-local skill contracts now select validation through one
identical shared planner command surface. They no longer own a duplicated
precheckpoint full-acceptance recipe. Final staged acceptance remains owned by
the governed checkpoint, and planner output remains selection-only while
legacy execution is authoritative during `shadow_planner`.

## Contract Surface

| Skill | Profile wrapper | Routing and source inspection preserved | Final acceptance |
| --- | --- | --- | --- |
| `continue-research` | `fast`, `affected`, `checkpoint`, `full`, `doctor` | memory preflight, targeted query, canonical inspection, Director context | governed checkpoint only |
| `improve-project-system` | `fast`, `affected`, `checkpoint`, `full`, `doctor` | memory preflight, classification, signal resolution and validation | governed checkpoint only |
| `user-modified-project` | `fast`, `affected`, `checkpoint`, `full`, `doctor` | human intent, Git inspection, classification, routed workflow preflight and source inspection | governed checkpoint only |
| `project-memory-system` | `fast`, `affected`, `checkpoint`, `full`, `doctor` | synchronization, memory-core validation, local retrieval and canonical inspection remain distinct operations | caller-owned governed checkpoint only |

All four contracts expose exactly these planner templates:

```text
.venv/bin/python -m scripts.validation.cli plan --profile <fast|affected|full> --paths <changed-path> --explain
.venv/bin/python -m scripts.validation.cli plan --profile checkpoint --staged --explain
.venv/bin/python -m scripts.validation.cli plan --profile doctor --scope local_retrieval --explain
```

`fast` is the cheapest edit loop. `affected` is bounded precheckpoint feedback.
`checkpoint` is selected only inside the final governed transaction. `full` is
explicit exhaustive or scheduled coverage. `doctor` is local or advisory and
cannot satisfy blocking or checkpoint obligations.

## Plan-Only Examples

The research, project-system, and user-modified examples each resolved the
`affected` profile to the same 12 selected gates at manifest hash
`7d9f04c5b06e7a5385cf7e101dbbdf4cc265f9ab1ee3a0307b2b435f5657747b`:

- `classify_changes`
- `resolve_project_improvement`
- `documentation_impact`
- `memory_sync`
- `memory_core`
- `spec_depth`
- `research_control_diff`
- `current_frontier_freshness`
- `compact_frontier_freshness`
- `claim_graph_validation`
- `git_diff_check`
- `continue_memory_preflight`

Every example returned `READY`, `planner_executes_commands=false`, and
`execution_authority=legacy`. None selected `checkpoint_transaction`.

The profile membership audit compared all 11 affected blocking gates with the
legacy-compatible set and reported no missing or unexplained gate mismatch.
The advisory resolver gate is intentionally absent from that blocking-only
comparison. `doctor` has no blocking gate or checkpoint-obligation overlap,
and `full` omits no nontransactional blocking gate.

## Retired Chain and Receipt Review

- No skill contains the retired documentation-impact, research-control,
  memory-core, full-test, and whitespace command chain as a local recipe.
- The memory skill retains direct operation targets only when selected by the
  shared plan or AgentJob. Its legacy `validate-memory` aliases are migration
  notes rather than embedded commands.
- Every skill requires compact profile, gate, status, receipt path and hash,
  count, and tree identity evidence.
- PASS output is not expanded without an audit requirement. Non-PASS output is
  expanded only by the relevant failed or warning finding group.
- Profile selection, receipts, tests, and checkpoint commits remain operational
  evidence only and have no physics, ontology, proof, benchmark, or Gate Chair
  authority.

## Source Hashes

| Path | SHA-256 |
| --- | --- |
| `.codex/skills/continue-research/SKILL.md` | `4ff16918097dd940bfed731f921acbe496b3e5a1d14f43a0fd352e74b7b0173f` |
| `.codex/skills/improve-project-system/SKILL.md` | `09396af30259f10892734eb12d00d89c1a68495f7ebfb01a67eb7f6af936e8f2` |
| `.codex/skills/user-modified-project/SKILL.md` | `f55704281bb111baae1cd9e63cecd584c2aa0ee15d99bd8d30ea23309469ce61` |
| `.codex/skills/project-memory-system/SKILL.md` | `b80f0a24d79e1ab630d89e7d27c5aaaf40da476b110d81740d3dbbe6f8e3f02c` |
| `tests/test_skill_validation_profile_wrappers.py` | `9e19d114353f63c4ee0ee26334f6f6184f93406fd97b6016a64232e47147c033` |

## Validation Summary

- 6 focused P6-T06 wrapper tests: PASS.
- 34 combined wrapper, profile, summary-consumption, and obligation-resolution tests: PASS.
- Profile membership audit: PASS with zero unexplained affected blocking-gate mismatches.
- Scientific claims changed: false.
- Ordinary research handoff preserved: `handoff-0740`.
