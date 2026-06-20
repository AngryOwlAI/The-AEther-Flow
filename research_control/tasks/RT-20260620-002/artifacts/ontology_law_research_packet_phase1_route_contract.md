<!-- authority: control -->

# Ontology-Law Research Packet Phase 1 Route Contract

## Analysis

Phase 1 implements the route-contract and vocabulary layer from
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`.
The route is now named in active control guidance as
`ontology-law-research-packet`.

The motivating current example is `RT-20260614-075`: the current ontology does
not derive the discriminator profiles, selector preorder, inverse checks,
cocycle checks, or finite-variation robustness needed for atlas-glue source
authority. That result blocks current adoption but does not prove future
source-extension impossibility.

## Route Contract

The route applies only when all of these are true:

- the active task is a physics derivation task;
- the AgentJob can name the active `target_derivation_milestone`;
- the AgentJob can name the active `milestone_burden`;
- the blocker is `derivation_critical_missing_source_law`;
- the missing object is a source-side law, selector, discriminator, transition
  rule, robustness rule, or equivalent primitive;
- current adoption remains blocked; and
- conservative same-milestone continuation remains possible.

The route does not apply to `ordinary_gap` or `workflow_inconvenience`.
Ordinary gaps include missing documentation, missing registry rows, generated
derivative drift, missing citations, computations available under the existing
ontology, and proof-detail work under existing ontology. Workflow
inconvenience includes tedious casework, slow literature review, awkward
templates, and strict validation friction.

## Controlled Vocabulary

| Term | Meaning |
| --- | --- |
| `derivation_critical_missing_source_law` | The active milestone is blocked because current ontology lacks a required source-side law or equivalent primitive. |
| `ordinary_gap` | Work is missing, but the missing work can be done without a new ontology law. |
| `workflow_inconvenience` | The issue is difficulty, friction, or process cost rather than ontology underdetermination. |
| `blocked_adoption_open_continuation` | Current adoption is blocked while same-milestone conservative source-side continuation remains open. |
| `draft/control` | Noncanonical controlled research or project-system artifact. |
| `proposal-only` | Candidate idea that is not adopted ontology or benchmark authority. |
| `source-extension data` | Admissible source-side extension data with no ontology promotion by itself. |
| `canonical-ontology candidate` | Candidate law prepared for human gate review but not adopted. |
| `adopted` | Status allowed only after the relevant explicit gate. |
| `rejected` | Current candidate or adoption route is not accepted at the relevant gate. |
| `human-gated` | Protected decision requiring explicit human authority. |

## Underdetermination Language

Allowed statement:

```text
current ontology does not derive X
```

Disallowed without a separate no-go theorem or scoped obstruction:

```text
therefore X is impossible
```

When a conservative extension remains possible, the control record must pair
blocked adoption with open continuation.

## Active Guidance Changes

Phase 1 updates these active control surfaces:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `research_control/README.md`
- `.codex/skills/continue-research/SKILL.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/roles/research_ops/director-of-research.v0.2.0.md`
- `.agents/roles/physics/theoretical-continuation-selector.v0.1.0.md`

The schema and selector text define the route vocabulary and the selector
packet value `ontology_law_research_packet`, mapped to route label
`ontology-law-research-packet`. Phase 2 remains responsible for a
machine-checkable receipt schema. Phase 4 remains responsible for validator
enforcement. Phase 5 remains responsible for fixtures.

## Receipt Hash Refresh

Bootstrap updated registry hashes for changed shared control surfaces. The
research-control validator requires current `memory_preflight` source hashes,
so this packet mechanically refreshed affected historical job and completion
receipt `source_hash` values only.

Those receipt changes do not alter historical decisions, objectives, verdicts,
role authority, claim-boundary text, physics claims, or task outcomes.

## Boundaries Preserved

This packet does not:

- edit canonical ontology TeX;
- modify benchmark sources;
- adopt `AtlasGlue_src^+`, `AtlasGlueDisc_src^+`, `M_src`, `g_eff`, matter
  coupling, or Einstein equations;
- issue a Gate Chair verdict;
- change validator behavior;
- add a receipt schema;
- create a physics research artifact; or
- alter historical decision authority or task conclusions; or
- hand-edit generated wiki notes, tracked HTML, generated PDFs, or generated
  registry sidecars.

## Verification

The packet passed project-change classification, project-improvement resolver
inspection, project-improvement signal validation, memory bootstrap,
bootstrap validate-only, documentation-impact validation, research-control
validation, research-control diff validation, and `git diff --check`.

Bootstrap reported pre-existing local retrieval freshness warnings for
Obsidian and memory mirrors. These warnings do not change canonical authority.

## Logical Next Step

Phase 2 should define the completion-level `ontology_law_research_packet`
receipt block and the exact required fields. Validator behavior should remain
deferred until the receipt schema is defined.

## Source Materials

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing PRD* [Internal proposal].
`PRDs/ontology_law_research_packet_routing_prd.md`

The AEther-Flow Research Project. (2026, June 20). *Ontology-law research
packet routing implementation plan* [Internal planning document].
`implementations_plans/ontology_law_research_packet_routing_implementation_plan.md`

The AEther-Flow Research Project. (2026, June 20). *Resp_lc current-ontology
AtlasGlue derivation attempt* [Internal research-control draft].
`research_control/tasks/RT-20260614-075/artifacts/116_RESP_LC_CURRENT_ONTOLOGY_ATLAS_GLUE_DERIVATION_ATTEMPT.tex`

The AEther-Flow Research Project. (2026, June 18). *Resp_lc source-extension
M_src bridge attempt* [Internal research-control draft].
`research_control/tasks/RT-20260614-061/artifacts/102_RESP_LC_SOURCE_EXTENSION_M_SRC_BRIDGE_ATTEMPT.tex`
