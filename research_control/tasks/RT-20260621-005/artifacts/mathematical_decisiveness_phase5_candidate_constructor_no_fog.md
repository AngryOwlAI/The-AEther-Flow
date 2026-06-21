<!-- authority: control -->

# Mathematical Decisiveness Phase 5 Candidate Constructor No-Fog Review

## Scope

Phase 5 adds no-fog output rules for future opted-in Candidate Constructor
physics completions. It is a project-system control packet, not a physics
derivation packet.

## Role Guidance Updated

The active Candidate Constructor role contract now requires future opted-in
physics AgentJobs to end with exactly one decisive
`candidate_constructor_result.result_type`:

- `constructed_candidate`
- `minimal_countermodel`
- `precise_obstruction`
- `invalid_under_claim_boundary`

The primary result cannot be only vague continuation language such as "more
work required", "candidate remains open", "future work should explore",
"insufficient time", "controlled pause", "selector should decide next", or
"generalization not attempted".

## Schema And Template Changes

The physics completion decisiveness schema and completion template now use the
explicit Phase 5 fields:

- `constructed_candidate_path`
- `minimal_countermodel_path`
- `obstruction_id`
- `formal_objects`
- `maps`
- `proof_obligations`
- `failed_components`
- `next_required_role`
- `no_fog_check`
- `no_fog_explanation`
- `claim_boundary_citation`

## Validator Changes

For opted-in future Candidate Constructor physics completions, the validator
now checks:

- `candidate_constructor_result` exists;
- `result_type` uses the allowed vocabulary;
- `no_fog_check` is true;
- `no_fog_explanation` is nonblank and does not use a fog-only primary result
  phrase;
- `next_required_role` is concrete;
- constructed candidates name artifact path, formal objects, maps, and proof
  obligations;
- minimal countermodels name countermodel path and failed components;
- precise obstructions name obstruction ID, failed components, and a present
  obstruction record;
- invalid-under-claim-boundary results name failed components and cite a claim
  boundary;
- `claim_boundary_preserved` remains true.

## Focused Tests

The focused test set covers:

- valid constructed Candidate Constructor result;
- valid Candidate Constructor precise obstruction result;
- invalid vague no-fog explanation;
- invalid constructed candidate missing formal objects.

## Claim Boundary

This packet does not construct `M_src`, define `g_eff`, couple matter, derive
Einstein equations, promote benchmark status, issue a Gate Chair verdict,
authorize ontology adoption, or reject the theory globally.

The rule forces decisive task closure language. It does not require success:
a countermodel, precise obstruction, or invalid-under-claim-boundary result is
allowed when that is the honest result.
