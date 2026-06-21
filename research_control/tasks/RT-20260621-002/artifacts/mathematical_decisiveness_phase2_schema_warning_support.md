<!-- authority: control -->

# Mathematical Decisiveness Phase 2 Schema Warning Support

## Analysis

Phase 2 implements the schema/template layer for the mathematical-decisiveness
completion contract created in `RT-20260621-001`. The chosen architecture is a
dedicated schema file plus warning-only validator inspection for future physics
AgentJobs that explicitly opt in.

This packet is project-system work. It does not change scientific truth status,
does not promote a physics result, and does not alter canonical ontology.

## Schema Location

The authoritative allowed-value surface is:

- `.agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md`

The existing AgentJob schema now documents the opt-in fields:

- `mathematical_decisiveness_contract_active_after`
- `mathematical_decisiveness_schema`
- `mathematical_decisiveness_contract`

The completion template now provides practical scaffolding for:

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `obstruction_record`
- `candidate_constructor_result`
- `forbidden_conclusion_summary`
- `route_cycle_control`

## Registry Convention Decision

No new allowed-value registries are created in this phase. The schema file owns
the Phase 2 allowed values. Completion YAML remains the source of truth for
future pilots. This is the least invasive option and preserves old-task
compatibility.

If future query needs require registries, the next bounded task can add type
registries for physics progress statuses, obstruction scopes, obstruction
consequences, and Candidate Constructor result types.

## Warning-Only Validator Support

`scripts/research_control/validate_research_control.py` now has a narrow
warning-only inspector. It runs only when all of these are true:

1. The completion belongs to a physics role.
2. The AgentJob or completion opts into the mathematical-decisiveness schema.
3. The job or completion timestamp is at or after the declared active-after
   timestamp.

The inspector emits warnings for missing or malformed prospective fields. It
does not call `report.error`, does not invalidate historical tasks, and does
not convert operational validation into physics evidence.

## Focused Fixtures

Two focused test fixtures were added:

- opted-in future physics completion missing the new fields warns only;
- opted-in future physics completion with the scaffold emits no
  mathematical-decisiveness warnings.

These fixtures prove the Phase 2 behavior boundary: visible guidance without
hard enforcement.

## Boundaries Preserved

This packet does not:

- edit canonical ontology TeX;
- modify benchmark sources;
- adopt `MSL-MSRC-ATLASGLUE-LAW`;
- adopt `AtlasGlue_src^+` or `AtlasGlueDisc_src^+`;
- adopt or fully construct `M_src`;
- define `g_eff`;
- derive matter coupling or Einstein equations;
- promote benchmark status;
- issue a Gate Chair verdict;
- claim completed derivation;
- reject the global theory;
- change checkpoint behavior;
- change route behavior; or
- hand-edit generated wiki notes, tracked HTML, generated PDFs, or generated
  registry sidecars.

## Verification Target

The intended verification chain is:

- focused warning-path unit tests;
- project-memory bootstrap;
- Obsidian/memory-index sync;
- project-memory validate-only;
- project-improvement signal validation;
- documentation-impact validation;
- research-control validation;
- research-control diff validation;
- `git diff --check`.

## Logical Next Step

Phase 3 should review the warning output after one pilot physics completion and
decide which checks should become hard validator failures. That later phase
must keep operational PASS separate from physics progress.

## Source Materials

The AEther-Flow Research Project. (2026, June 21). *Mathematical decisiveness
completion contract* [Internal control note].
`research_control/design/mathematical_decisiveness_completion_contract.md`

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations
implementation plan* [Internal implementation plan].
`implementations_plans/aether_recommendations_implementation_plan.md`
