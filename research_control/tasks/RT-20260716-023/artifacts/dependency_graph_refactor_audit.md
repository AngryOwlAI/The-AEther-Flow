---
authority: control
task_id: "RT-20260716-023"
job_id: "AJ-RT-20260716-023-001"
plan_task_id: "P7-T01"
status: "REPAIR_REQUIRED"
scientific_claims_changed: false
---

# P7-T01 dependency-graph snapshot audit

## Result

The renderer now separates repository extraction from graph construction and
format rendering. One deeply immutable snapshot captures parsed registries,
program state, completions, handoffs, source hashes, and parse failures.
`build_graph()` accepts that snapshot, graph validation remains pure, and JSON,
Markdown, and DOT rendering performs no repository reads.

The implementation and renderer-equivalence evidence pass, but P7-T01 returns
`REPAIR_REQUIRED`. Compare-mode checkpoint planning classifies
`scripts/research_control/render_dependency_graph.py` as an unresolved governed
path and stops before staging. P7-T02 therefore remains locked until one
separately bounded classifier/shadow-parity repair and a P7-T01 rerun pass.

## Evidence

- The seven pre-existing tests passed at entry in 413.280 seconds.
- The ten focused tests passed after the refactor in 32.110 seconds.
- One measured build loaded 1,679 unique source paths exactly once, built one
  18,263-node and 64,537-edge graph, and rendered all three formats once.
- A patched-file-access test built from a captured snapshot and rendered each
  format twice without permitting `Path.read_bytes`, `Path.read_text`, or
  `Path.open`.
- The entry-commit renderer and refactored renderer produced equal graph
  objects and byte-identical JSON, Markdown, and DOT for the same live tracked
  state. Exact hashes are recorded in
  `dependency_graph_refactor_equivalence.json`.
- The clean entry checkpoint already had stale committed graph derivatives.
  That baseline drift predates this refactor and is synchronized through the
  governed generation path before checkpoint.
- The first compare-mode checkpoint attempt staged nothing and committed
  nothing. Its planner selected full fallback but retained the renderer in
  `unknown_paths`, which the final staged-acceptance contract correctly rejects.

## Boundaries

The graph schema, source hashes, node and edge ordering, authority notice,
route continuity, ordinary handoff `handoff-0740`, and legacy shadow authority
are unchanged. No cross-tree cache or P7-T02 shared test setup was added. This
operational validation work changes no physics claim, proof status, ontology,
benchmark status, Gate Chair authority, or Distance-to-GR burden.
