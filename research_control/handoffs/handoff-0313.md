# Handoff 0313

## Summary

P7-T02 implemented the deterministic dependency graph extractor and generated
the JSON, Markdown, and DOT graph artifacts from tracked state.

## Authority Boundary

The generated graph is navigational support only. It is not physics authority,
not proof authority, not claim-promotion authority, and not a substitute for
registered sources, completion records, handoffs, Gate Chair records, or
control registries.

No Distance-to-GR ledger row, source-law adoption, `MetricData(E)` adoption,
`g_eff` adoption or scope expansion, coupling-law adoption, matter-coupling
derivation, stress-energy semantics, Einstein equations, benchmark promotion,
or completed derivation was promoted.

## Output

- `scripts/research_control/render_dependency_graph.py`
- `output/research_dependency_graph.json`
- `wiki/indexes/research_dependency_graph.md`
- `output/research_dependency_graph.dot`
- `tests/test_render_dependency_graph.py`

## Next Action

Run one bounded P7-T03 `validator-engineer@0.2.0` packet to add graph freshness
validation for generated graph artifacts while preserving graph-as-navigation
only.
