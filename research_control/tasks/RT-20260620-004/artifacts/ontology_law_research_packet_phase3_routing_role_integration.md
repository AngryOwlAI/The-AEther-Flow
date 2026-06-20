<!-- authority: control -->

# Ontology-Law Research Packet Phase 3 Routing And Role Integration

## Analysis

Phase 3 implements the routing-and-role integration layer from
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`.
Phase 1 defined the route label and vocabulary. Phase 2 defined the receipt
schema. Phase 3 now makes the route operationally reachable from Director,
continue-research, selector, and active physics role guidance.

This packet is not a physics research artifact. It does not propose a source
law, adopt ontology, promote benchmark status, implement validator behavior,
add fixtures, or issue a Gate Chair verdict.

## Active Guidance Changes

Phase 3 updates these control surfaces:

- `.agents/roles/research_ops/director-of-research.v0.2.0.md`
- `.codex/skills/continue-research/SKILL.md`
- `.agents/roles/physics/theoretical-continuation-selector.v0.1.0.md`
- `.agents/roles/physics/ontology-formalizer.v0.2.0.md`
- `.agents/roles/physics/candidate-constructor.v0.2.0.md`
- `.agents/roles/physics/smuggling-auditor.v0.2.0.md`
- `.agents/roles/physics/refuter.v0.2.0.md`

The route remains `ontology-law-research-packet`, with selector packet value
`ontology_law_research_packet`. The trigger remains
`derivation_critical_missing_source_law`.

## Director And Continue-Research Integration

The Director and continue-research guidance now state that this route:

- remains one outer physics AgentJob per invocation;
- is not a permanent role and not independent authority;
- binds to existing active roles through the normal execution-role record;
- uses task overlays for route-specific constraints;
- does not create child AgentJobs, child execution-role records, extra write
  paths, or independent claim boundaries; and
- preserves `parent_child_parallel_synthesis`.

The routing family is explicit:

| Immediate payload | Role family |
| --- | --- |
| Packet-selection decision | `theoretical-continuation-selector@0.1.0` |
| Source-law definition, formal objects, domains, maps, proof obligations | `ontology-formalizer@0.2.0` |
| Bounded finite or local source-side witness | `candidate-constructor@0.2.0` |
| Hidden target-import audit | `smuggling-auditor@0.2.0` |
| Collapse, nonuniqueness, inverse, cocycle, or finite-variation stress | `refuter@0.2.0` |

Permanent role registration remains outside this route. It must go through the
project-system improvement loop after repeated evidence, not through Director
habit or route naming.

## Parent-Child Synthesis Boundary

For ontology-law physics AgentJobs, the required parent-child decomposition is
preserved inside the single outer AgentJob:

- the Physicist-Mathematician child defines formal objects, domains, maps, and
  proof obligations;
- the Physicist-Philosopher child separates ontology, mathematical model,
  empirical recovery, and benchmark status; and
- the parent preserves consensus, unique contributions, and unresolved
  conflicts in one fused output.

The child perspectives inherit the outer execution-role record, write-path
allowlist, source restrictions, validators, stop conditions, and claim
boundary.

## Role Guidance Integration

The active physics role contracts now include ontology-law packet usage notes:

- Ontology Formalizer may formalize missing source-side law candidates while
  keeping them draft/control, proposal-only, source-extension data, or
  canonical-ontology candidates.
- Candidate Constructor may build bounded finite or local witnesses from
  explicit source-side assumptions while leaving exact-GR obligations visible.
- Smuggling Auditor audits target atlas, target metric, benchmark success,
  generated derivative, registry metadata, role authority, and validation
  authority imports.
- Refuter stress-tests collapse, nonuniqueness, inverse defects, cocycle
  defects, and finite-variation fragility while preserving local-scope
  negative results.

## Boundaries Preserved

This packet does not:

- edit canonical ontology TeX;
- modify benchmark sources;
- adopt `AtlasGlue_src^+`, `AtlasGlueDisc_src^+`, `M_src`, `g_eff`, matter
  coupling, or Einstein equations;
- issue a Gate Chair verdict;
- change validator behavior;
- add test fixtures;
- create a physics research artifact;
- register a new permanent ontology-law role;
- promote a candidate law to adopted ontology; or
- hand-edit generated wiki notes, tracked HTML, generated PDFs, or generated
  registry sidecars.

## Memory Preflight Receipt

The memory status command returned `freshness_status: WARN` because local
retrieval derivatives under `.local/obsidian` and the SQLite memory index lag
current registered sources. These retrieval layers are not authority-bearing.

The hyphenated search
`.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "ontology-law research packet Phase 3 Director role guidance" --limit 10 --json`
failed with `sqlite3.OperationalError: no such column: law`. The safer
underscore search for `ontology_law_research_packet` returned no hits. The
successful targeted lookups used these object IDs:

- `MD-ROLE-AGENTS-ROLES-RESEARCH-OPS-DIRECTOR-OF-RESEARCH-V0-2-0-MD`
- `MD-SKILL-CONTINUE-RESEARCH`

The canonical inspections used `registries/MARKDOWN_SOURCE_REGISTRY.csv` and
the live source files named above. Source hashes were refreshed after edits by
the approved bootstrap path.

## Verification

The packet is designed to pass project-change classification,
project-improvement resolver inspection, project-improvement signal
validation, memory bootstrap, bootstrap validate-only,
documentation-impact validation, research-control validation, research-control
diff validation, and `git diff --check`.

Bootstrap may report pre-existing local retrieval freshness warnings for
Obsidian and memory mirrors. Those warnings do not change canonical authority.

## Logical Next Step

Phase 4 should implement deterministic validator enforcement for the
`ontology_law_research_packet` completion receipt. That phase should check
fields, labels, and forbidden-claim boundaries without pretending to prove the
physics.

## Source Materials

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing PRD* [Internal proposal].
`PRDs/ontology_law_research_packet_routing_prd.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing implementation plan* [Internal planning document].
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet Phase 1 route contract* [Internal control artifact].
`research_control/tasks/RT-20260620-002/artifacts/ontology_law_research_packet_phase1_route_contract.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet Phase 2 receipt schema* [Internal control artifact].
`research_control/tasks/RT-20260620-003/artifacts/ontology_law_research_packet_phase2_receipt_schema.md`
