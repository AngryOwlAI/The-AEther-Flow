# Handoff 0312

## Status

P7-T01 is complete. `research_control/design/research_dependency_graph_schema.md`
defines the dependency graph schema as a project-control design note.

## Result

The schema defines:

- JSON, Markdown, and DOT output contracts;
- required node classes, including source ontology objects, source-extension
  evidence/preconditions, draft/control candidates, accepted scoped objects,
  human-gated objects, blocked burdens, frozen negatives, obstructions, Gate
  Chair verdicts, tasks, AgentJobs, artifacts, handoffs, ledger rows, and claim
  boundaries;
- required edge classes, including `requires`, `constructs`, `audits`,
  `stress_tests`, `selects_next`, `accepts_as_evidence`, `adopts_scoped`,
  `rejects`, `blocks`, `freezes`, `forbids_overread`, `depends_on`,
  `updates_ledger`, `handoffs_to`, and `requires_human_gate`;
- required state labels such as `canonical_source`, `draft_control`,
  `source_extension_evidence`, `accepted_scoped`, `human_gated`, `blocked`,
  `frozen_negative`, and `support_only`;
- direct mappings from existing registries, completion fields, handoff fields,
  and ledger rows;
- current frontier representation rules for `Resp_lc`, `M_src`, scoped
  `g_eff`, `B_E^{rec}`, `BridgeCert`, `SEI-MC`, `SEI_src^{cand}`, matter
  coupling, Einstein equations, benchmark promotion, and the frozen finite toy
  metric response route.

## Claim Boundary

This was project-control schema design only. The graph is navigational support,
not physics authority. This packet did not adopt a source law, adopt
`MetricData(E)`, adopt or expand `g_eff`, derive or adopt matter coupling,
import stress-energy semantics, construct a stress-energy tensor, import matter
action or detector semantics, derive Einstein equations, promote the benchmark,
or complete the derivation.

## Next Action

Run one bounded P7-T02 `memory-system-maintainer@0.2.0` packet to implement the
deterministic dependency graph extractor and generated graph artifacts from
tracked state.

## Validation

- Schema artifact created: PASS
