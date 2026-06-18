# Controlled Memory Preflight Audit

## Summary

Implemented a prospective memory preflight contract for future
`continue-research` and `improve-project-system` work. AgentJobs and
completions created after `2026-06-18T15:33:00Z` must now carry a
`memory_preflight` receipt that records memory status, targeted memory queries,
returned object IDs, and canonical source inspection evidence.

## Implementation Notes

- `validate_research_control.py` now validates `memory_preflight` on future
  AgentJob and completion records.
- The receipt validator requires a `query_memory.py status --json` command, at
  least one `lookup` or `search` query, nonempty returned object IDs, canonical
  inspection entries, source registry paths, canonical source paths, and source
  hashes matching both the registry row and current source bytes.
- `query_memory.py status --json` now exposes `freshness_status` and
  `freshness_warnings`.
- `bootstrap_memory_system.py --validate-only` warns when local retrieval
  surfaces are stale or missing, without treating `.local` as authority.
- Skill contracts, schema documentation, templates, and research-control
  documentation now describe the preflight rule.

## Authority Boundary

The implementation preserves the source-first authority hierarchy. Obsidian,
wiki notes, content-semantic extracts, the SQLite memory index, and `.local`
remain retrieval layers only. Registered source files and CSV registry rows
remain the verification surface for claims, routing, and project-control
changes.
