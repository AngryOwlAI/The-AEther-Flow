<!-- authority: control -->

# Mathematical Decisiveness Phase 1 Contract Audit

## Decision

The first implementation slice is Phase 1 from
`implementations_plans/aether_recommendations_implementation_plan.md`: create
the mathematical-decisiveness completion contract before schema or validator
enforcement.

## Reasoning

The implementation plan recommends starting with Option A: future completion
YAML fields as the source of truth. This is the smallest reversible change. It
lets future physics tasks cite a concrete contract without forcing historical
tasks into a new schema and without converting validator warnings into hard
failures before fixtures exist.

## Contract Location

- `research_control/design/mathematical_decisiveness_completion_contract.md`

This is a registered control design note. The design README lists it as a
current subject.

## Deferred Work

The following work is intentionally deferred:

- completion template or schema updates;
- prospective validator warnings;
- validator hard failures;
- new progress registries;
- role guidance updates;
- backfill metadata overlays;
- the next Candidate Constructor physics task.

## Claim Boundary

This task does not authorize canonical ontology edits, adoption of
`MSL-MSRC-ATLASGLUE-LAW`, adoption of `AtlasGlue_src^+` or
`AtlasGlueDisc_src^+`, adoption or full construction of `M_src`, `g_eff`,
matter coupling, Einstein equations, benchmark promotion, Gate Chair closure,
completed-derivation language, future source-extension impossibility, global
theory rejection, validator enforcement, or physics artifact creation.
