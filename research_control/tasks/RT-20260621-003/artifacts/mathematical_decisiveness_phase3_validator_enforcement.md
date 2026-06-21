<!-- authority: control -->

# Mathematical Decisiveness Phase 3 Validator Enforcement Review

## Scope

Phase 3 reviewed the Phase 2 warning-only pilot and selected the checks that
should become hard validator failures for future opted-in physics completions.
The enforcement boundary is narrow: historical tasks remain valid and
non-physics project-system completions are unaffected.

## Pilot Finding

The Phase 2 pilot showed that missing mathematical-decisiveness fields are
detectable without touching physics sources. The warning-bearing fixture lacked
the fields that make a completion terminally informative:

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`

Those fields are now hard requirements for opted-in future physics completions.

## Hard-Enforced Checks

Phase 3 converts these checks to errors:

- Missing core mathematical-decisiveness fields.
- Malformed `physics_progress_status`, including unknown status values.
- Unauthorized physics promotion when no human-gated authority path is cited.
- Empty or malformed `mathematical_payload_manifest` payload entries.
- Obstruction statuses without an `obstruction_record`.
- Obstruction receipts missing scope, failed object, exact failure,
  consequence, or forbidden-overread text.
- Scoped obstruction or route freeze without `freeze_criteria_status`.
- Candidate Constructor completions without `candidate_constructor_result`.
- Vague Candidate Constructor results that omit `no_fog_summary`.
- Downstream GR unlocks without promotion authority.
- Forbidden-conclusion summaries that fail to preserve the downstream claim
  blocks.

## Compatibility

The validator remains prospective and opt-in. It activates only when a future
physics AgentJob or completion names the mathematical-decisiveness schema or
contract and the relevant timestamp is at or after the active boundary.

Project-system jobs may still cite or edit the schema without needing physics
completion fields.

## Claim Boundary

This packet improves operational decisiveness. It does not prove a theorem,
construct `M_src`, define `g_eff`, couple matter, derive Einstein equations,
promote benchmark status, issue a Gate Chair verdict, authorize ontology
adoption, or reject the theory globally.

Validator PASS remains control evidence only. Physics progress remains in the
registered physics sources and gated completion receipts.
