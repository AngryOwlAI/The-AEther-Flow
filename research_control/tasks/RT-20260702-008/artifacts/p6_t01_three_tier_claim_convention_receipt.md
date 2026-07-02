<!-- authority: control -->

# P6-T01 Three-Tier Claim Convention Receipt

## Scope

This receipt records one bounded v14 P6-T01 claim-convention policy packet. It
creates the canonical three-tier claim convention policy and does not update
completion templates, handoff templates, current-frontier renderer behavior,
public surfaces, generated HTML, or scientific status.

## Deliverable

| Deliverable | Path | Result |
| --- | --- | --- |
| Canonical three-tier claim convention policy | `research_control/design/three_tier_claim_convention.md` | PASS |

## Required Tier Coverage

The policy defines all required v14 P6-T01 tiers:

- adopted objects;
- accepted evidence/preconditions;
- open or blocked physical targets.

## Required Surface Coverage

The policy applies the convention to all required summary surfaces:

- completions;
- handoffs;
- `research_control/current_frontier.md`;
- public status surfaces;
- final audits.

## Required Example Coverage

The policy covers the required examples:

- `M_src` as a scoped source-only object;
- `g_eff` as a scoped source-extension object;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` as scoped readiness evidence/precondition or proposal-only law target unless a later gate changes status;
- `PositiveMSProfile_v1` as accepted only as scoped positive source-semantics evidence/precondition;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` as accepted only as certificate-indexed evidence/precondition;
- stable matter-semantics bridge evidence/precondition;
- MCPA evidence/precondition;
- coupling-law-candidate evidence/precondition;
- matter semantics, detector semantics, universal coupling, stress-energy semantics, stress-energy tensor, matter action, Einstein equations, benchmark promotion, and completed derivation as open or blocked physical targets.

## Validation Receipts

| Check | Result | Evidence |
| --- | --- | --- |
| Memory preflight | PASS | `core_validation_status=PASS`, `freshness_status=PASS`, `local_retrieval_status=PASS`, `refresh_performed=false` |
| Targeted memory query | PASS | Lookup inspected the v14 plan and public status source spec; search returned current frontier and v14 plan for P6-T01 routing context. |
| Continue-research route | PASS | Resolver selected `handoff-0460` next action: one bounded v14 P6-T01 policy packet. |
| Policy hash | PASS | `cfd78be2af42249b44c7cd131c7f6613425df778a4c6aa280ce4293a7492f1aa` |
| Policy claim-language gate | PASS | `validate_claim_language.py --json --paths research_control/design/three_tier_claim_convention.md` reported zero findings. |

## Interpretation Boundary

P6-T01 is a documentation-control policy packet. It does not establish or
change the physics status of any row. It does not authorize ontology edits,
source-law adoption, `MetricData(E)` adoption, `g_eff` scope expansion,
matter-coupling derivation, stress-energy semantics, matter action, Einstein
equations, benchmark promotion, or completed derivation.

## Next Route

The logical next packet is v14 P6-T02 completion and handoff template update.
The current-frontier three-tier pilot, P6 phase validation, and downstream
physics routes remain blocked until their own tracked packets authorize them.
