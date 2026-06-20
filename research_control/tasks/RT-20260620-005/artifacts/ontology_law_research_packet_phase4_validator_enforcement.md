<!-- authority: control -->

# Ontology-Law Research Packet Phase 4 Validator Enforcement

## Analysis

Phase 4 implements the deterministic validator-enforcement layer from
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`.
The validator now recognizes `ontology_law_research_packet` as an allowed
Theoretical Continuation Selector packet type and validates the
`ontology_law_research_packet` completion receipt when a physics completion
selects the route or when a completion supplies the receipt block.

This packet is not a physics research artifact. It does not propose a source
law, adopt ontology, promote benchmark status, issue a Gate Chair verdict, or
create a physics AgentJob.

## Validator Behavior Added

The validator now checks that an ontology-law route completion includes:

- `route: "ontology-law-research-packet"`;
- `trigger_classification: "derivation_critical_missing_source_law"`;
- a registered `target_derivation_milestone`;
- a nonblank `milestone_burden`;
- a nonblank `missing_source_law`;
- underdetermination language stating that current ontology does not derive
  the missing law;
- `blocked_adoption_open_continuation` with blocked current adoption and open
  continuation;
- one allowed payload mode;
- controlled candidate-law status labels;
- exact-GR recovery obligations and Distance-to-GR links;
- no-target-import audit scope for target atlas, target metric, benchmark
  success, generated derivative, registry metadata authority, role authority,
  and validation authority;
- human-gate requirement before adoption.

The validator rejects ordinary gaps, workflow inconvenience triggers,
target-GR import definitions, and premature impossibility claims unless a
no-go theorem or scoped obstruction is explicitly present.

## Test Coverage

Focused unit tests were added for:

- selector output requiring an ontology-law receipt;
- acceptance of a valid candidate-law receipt;
- rejection of `ordinary_gap` as a trigger;
- rejection of candidate definitions from target metric or target atlas data;
- rejection of premature impossibility language without no-go evidence.

These are Phase 4 regression tests, not the full Phase 5 fixture suite. Phase 5
should still add broader route fixtures, including the motivating AtlasGlue
underdetermination packet and additional target-import/human-gate cases.

## Boundaries Preserved

This packet does not:

- edit canonical ontology TeX;
- modify benchmark sources;
- adopt `AtlasGlue_src^+`, `AtlasGlueDisc_src^+`, `M_src`, `g_eff`, matter
  coupling, or Einstein equations;
- issue a Gate Chair verdict;
- create a physics research artifact;
- register a new permanent ontology-law role;
- modify checkpoint behavior; or
- hand-edit generated wiki notes, tracked HTML, generated PDFs, or generated
  registry sidecars.

## Verification

The focused ontology-law validator tests passed. Full validation is recorded in
the completion receipt after bootstrap, documentation-impact, research-control,
diff, and unit-test gates.

Bootstrap may report pre-existing local retrieval freshness warnings for
Obsidian and memory mirrors. Those warnings do not change canonical authority.

## Logical Next Step

Phase 5 should add the broader ontology-law research packet fixture suite. The
fixtures should prove behavior at the research-control surface without treating
the validator as a physics proof engine.

## Source Materials

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing PRD* [Internal proposal].
`PRDs/ontology_law_research_packet_routing_prd.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing implementation plan* [Internal planning document].
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet Phase 2 receipt schema* [Internal control artifact].
`research_control/tasks/RT-20260620-003/artifacts/ontology_law_research_packet_phase2_receipt_schema.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet Phase 3 routing and role integration* [Internal control artifact].
`research_control/tasks/RT-20260620-004/artifacts/ontology_law_research_packet_phase3_routing_role_integration.md`
