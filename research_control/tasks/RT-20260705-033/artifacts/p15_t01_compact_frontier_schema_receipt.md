<!-- authority: control -->

# P15-T01 Compact Frontier Schema Receipt

Task: `RT-20260705-033`

Job: `AJ-RT-20260705-033-001`

## Result

`research_control/design/compact_current_frontier_schema_v16.md` defines the
`compact_current_frontier_v16` schema.

The schema:

- marks compact output as snapshot-only and not authority;
- names `research_control/program_state.yaml`, the latest handoff,
  `registries/DISTANCE_TO_GR_LEDGER.csv`, and
  `research_control/current_frontier.md` as required source inputs;
- blocks generated wiki, Obsidian, semantic extracts, SQLite memory, `.local`
  cache state, validator PASS, dependency graphs, and commits from becoming
  authority;
- requires high-risk Distance-to-GR rows for `m_src`, `g_eff`,
  `matter_coupling`, `einstein_equations`, and `benchmark_promotion`;
- preserves blocked claims for source-law adoption, matter-coupling derivation
  or adoption, Einstein equations, benchmark promotion, proof authority, and
  completed derivation.

## Validation

Task-local validation command:

```zsh
.venv/bin/python research_control/tasks/RT-20260705-033/artifacts/validate_p15_t01_compact_frontier_schema.py --output research_control/tasks/RT-20260705-033/artifacts/p15_t01_compact_frontier_schema_report.json --json
```

Expected status: `PASS`.

## Boundary

This completion implements a bounded v16 task. It does not authorize
source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption,
unrestricted `RR_E` theorem status, matter-semantics adoption,
detector-semantics adoption, coupling-law adoption, matter-coupling derivation
or adoption, stress-energy semantics, stress-energy tensor construction,
matter action, Einstein equations, benchmark promotion, or completed
derivation.
