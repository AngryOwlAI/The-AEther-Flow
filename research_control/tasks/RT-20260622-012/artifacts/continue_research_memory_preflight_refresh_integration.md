<!-- authority: control -->

# Continue-Research Memory Preflight Refresh Integration

## Summary

This packet integrates a deterministic local retrieval refresh step into
`/continue-research`.

The new helper is:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
```

It checks memory status, refreshes local Obsidian notes, raw mirrors, semantic
extracts, and the SQLite memory index only when local-cache warnings are
present, then reports the final receipt-ready status summary.

## Authority Boundary

The helper does not make Obsidian, SQLite, semantic extracts, or `.local`
authoritative. These surfaces remain retrieval support. Director routing and
claim language still require canonical source or source-registry inspection
after any memory hit that influences the decision.

## Verification Evidence

- Focused unit tests cover the refresh-needed and already-fresh paths.
- Live helper execution detected local retrieval drift and returned
  `after_local_retrieval_status: PASS`.
- The `/continue-research` skill contract and `research_control/README.md`
  now require the helper before targeted memory lookup or search.
- AgentJob and completion templates now include a standard
  `local_retrieval_refresh` receipt block.
