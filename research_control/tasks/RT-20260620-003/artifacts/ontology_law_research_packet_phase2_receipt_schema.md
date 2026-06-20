<!-- authority: control -->

# Ontology-Law Research Packet Phase 2 Receipt Schema

## Analysis

Phase 2 implements the receipt-schema layer from
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`.
Phase 1 already defined the route label, trigger vocabulary, non-trigger
vocabulary, and blocked-adoption/open-continuation language. Phase 2 now
defines the completion-level `ontology_law_research_packet` block that future
validators can inspect.

This packet is not a physics research artifact. It does not propose a source
law, adopt ontology, promote benchmark status, or issue a Gate Chair verdict.

## Schema Location

The active schema contract is recorded in `.agents/schemas/AGENT_JOB_SCHEMA.md`
under `Ontology-Law Research Packet Completion Receipt`.

The practical scaffold is recorded in
`research_control/templates/COMPLETION_TEMPLATE.yaml` as a top-level
`ontology_law_research_packet` block.

## Required Receipt Fields

| Field | Requirement |
| --- | --- |
| `route` | Must be `ontology-law-research-packet`. |
| `trigger_classification` | Must be `derivation_critical_missing_source_law`. |
| `target_derivation_milestone` | Must name the active derivation milestone. |
| `milestone_burden` | Must name the active milestone burden. |
| `missing_source_law` | Must name the missing source law, selector, discriminator, transition rule, robustness rule, or equivalent primitive. |
| `underdetermination_statement` | Must state that current ontology does not derive the missing object without converting that into impossibility language. |
| `no_go_theorem_status` | Must state whether a no-go theorem or scoped obstruction exists. |
| `adoption_status` | Must preserve blocked current adoption and open same-milestone continuation where applicable. |
| `packet_payload_mode` | Must select one payload branch: candidate payload, comparison, refutation, or human-gate precondition. |
| `candidate_law_payload` | Must define source-side objects when the packet proposes a candidate law. |
| `candidate_law_comparison` | Must compare bounded candidates when the packet is comparative. |
| `candidate_law_refutation` | Must preserve failed candidate evidence when the packet refutes a candidate. |
| `human_gate_precondition` | Must explain why human authority is needed before a law can be proposed when applicable. |
| `exact_gr_recovery_obligations` | Must name recovery obligations and distance-to-GR links. |
| `no_target_import_audit_scope` | Must include target-atlas, target-metric, benchmark-success, generated-derivative, registry-metadata, role-authority, and validation-authority import classes. |
| `atlas_glue_obligations` | Must preserve profile, selector, transition, inverse, cocycle, and finite-variation obligations where relevant. |
| `failure_branches` | Must preserve collapse, nonuniqueness, inverse-defect, cocycle-defect, and variation-fragility branches. |
| `human_gate_request` | Must keep ontology adoption blocked until explicit human Gate Chair authority. |

## Machine-Checkable Shape

The schema is intentionally field-based rather than prose-only. Phase 4 can
therefore validate the presence and allowed values for:

- route label;
- trigger classification;
- active derivation milestone and burden;
- missing source-law name;
- blocked-adoption/open-continuation status pair;
- payload branch mode;
- candidate status label;
- exact-GR recovery checklist;
- no-target-import audit scope;
- human-gate requirement before adoption.

The schema does not ask validators to prove mathematical truth. It asks
validators to confirm that the receipt names the required burdens, boundaries,
labels, and audit scope.

## Deferred Enforcement

This packet does not modify `scripts/research_control/validate_research_control.py`,
does not add test fixtures, and does not reject historical packets. Validator
enforcement remains Phase 4. Tests and fixtures remain Phase 5.

## Memory Preflight Receipt

The memory status command returned `freshness_status: WARN` because local
retrieval derivatives under `.local/obsidian` and the SQLite memory index lag
current registered sources. This is not authority-bearing. Obsidian notes,
wiki notes, semantic extracts, SQLite memory, and `.local` files remain
retrieval layers only.

The targeted lookup
`.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-SCHEMA-AGENT-JOB-SCHEMA --json`
returned `MD-SCHEMA-AGENT-JOB-SCHEMA`. The canonical inspection used
`registries/MARKDOWN_SOURCE_REGISTRY.csv`, path
`.agents/schemas/AGENT_JOB_SCHEMA.md`, and source hash
`fcef395f0884cf85bfcd8cbd6da27aecf9ee40985dcb3f7fa4515a1d3e031720`.

## Boundaries Preserved

This packet does not:

- edit canonical ontology TeX;
- modify benchmark sources;
- adopt `AtlasGlue_src^+`, `AtlasGlueDisc_src^+`, `M_src`, `g_eff`, matter
  coupling, or Einstein equations;
- issue a Gate Chair verdict;
- change validator behavior;
- add test fixtures;
- change routing behavior;
- create a physics research artifact;
- promote a candidate law to adopted ontology; or
- hand-edit generated wiki notes, tracked HTML, generated PDFs, or generated
  registry sidecars.

## Verification

The packet is designed to pass project-change classification, project-improvement
resolver inspection, project-improvement signal validation, memory bootstrap,
bootstrap validate-only, documentation-impact validation, research-control
validation, research-control diff validation, and `git diff --check`.

Bootstrap may report pre-existing local retrieval freshness warnings for
Obsidian and memory mirrors. Those warnings do not change canonical authority.

## Logical Next Step

Phase 3 should integrate the route into Director and role guidance so future
research-control continuation can select and execute the packet while
preserving one outer AgentJob and parent-child synthesis.

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
