<!-- authority: control -->

# External Red-Team Reviewer Role Design

## Purpose

This design artifact was created for P7-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v12.md`
and reconciled by v14 P9-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v14.md`.
It records the stable `external-red-team-reviewer@0.1.0` role identifier and
the review artifact template for skeptical-review packets.

The role exists to add an internal adversarial outside-reader perspective. It
does not create external provenance, proof authority, or physics promotion
authority.

## Current V21 Label Contract

The current display name is `Internal Skeptical Reviewer` and the current role
kind is `scientific_adversarial_internal_review`. The older
`external-red-team-reviewer@0.1.0` spelling is a stable legacy identifier only;
it remains unchanged so historical task IDs, artifacts, completions, registry
references, and hashes remain resolvable.

A same-context AI review is internal. A blind packet or different model may
change the structured review-context classification, but neither establishes
external human review or independent replication. Those labels are reserved
for the evidence-qualified `human_expert_review` and
`independent_replication` classes defined by the review-context contract.

## Boundary Statement

The internal skeptical reviewer has `may_promote_claims=false`. It is critique
and routing authority only. It is not Gate Chair authority, not Smuggling
Auditor replacement, not Refuter replacement, not canonical ontology adoption,
not source-law adoption, not source-extension data adoption, not `MetricData(E)`
adoption, not `g_eff` adoption or scope expansion, not coupling-law adoption,
not matter coupling, not stress-energy semantics, not a stress-energy tensor,
not detector semantics, not a matter action, not Einstein equations, not
benchmark promotion, and not completed derivation.

## Role Placement

The registered role contract is:

```text
.agents/roles/physics/external-red-team-reviewer.v0.1.0.md
```

The role is placed under `.agents/roles/physics/` because it reviews
science-facing mathematical objects and interpretation boundaries. Its
authority remains `science_draft`; it cannot modify science sources and cannot
promote claims.

Permanent role registration is protected by the role schema. This packet uses
tracked one-time approval
`research_control/approvals/approval-20260630-004.yaml` only for the
non-promotional registration of `external-red-team-reviewer@0.1.0` and its
template. The approval does not authorize Gate Chair power, source-law
adoption, or downstream GR promotion.

The v14 P9-T01 reconciliation uses
`research_control/approvals/approval-20260702-001.yaml` only for a
non-promotional contract update. That update adds explicit checks for
process-authority laundering, evidence-as-adoption laundering, no-target
certificate overread, `RR_E` separation collapse, and authorized literature
comparison. The approval does not authorize a role-version authority increase,
Gate Chair power, source-law adoption, benchmark promotion, or downstream GR
promotion.

## Mandate

The reviewer must ignore workflow success and validator success as evidence.
It must inspect definitions, assumptions, theorem statements, proof skeletons,
circularity, hidden target imports, process-authority laundering,
evidence-as-adoption laundering, no-target certificate overread, `RR_E`
separation collapse, overloaded notation, unproven equivalences, and
mismatches between mathematical conclusion and physical interpretation.

When possible, the reviewer should produce a minimal countermodel or a
not-enough-assumptions theorem sketch. When that is not possible inside the
packet scope, the reviewer should name the missing assumption, unavailable
object, or next review route. Permitted recommendations include repair,
obstruction, freeze, literature review, selector, continuation, or no action,
subject to the owning AgentJob's allowlist.

## Complementarity

The Internal Skeptical Reviewer complements existing adversarial roles:

- Smuggling Auditor checks whether a candidate imports forbidden target
  structure.
- Refuter stress-tests a candidate under defined failure modes.
- Internal Skeptical Reviewer challenges whether the object itself would be
  legible and defensible from a skeptical perspective even after internal
  workflow success. This perspective does not establish external provenance.
- Gate Chair remains the only human-gated promotion, closure, or suspension
  authority.

Therefore a red-team pass is not adoption, and a red-team finding is not by
itself a global no-go theorem. Findings route repair, obstruction review,
freeze review, literature comparison, selector review, continuation, or
external review.

## Review Artifact Template

The historical task added:

```text
research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml
```

The current template carries the internal display name and role kind while
retaining its legacy path and schema identifier. It requires the future
reviewer to state that workflow and validator
success were disregarded as evidence; enumerate findings; classify
countermodels or not-enough-assumptions results when available; recommend a
repair or review route; and preserve all claim-promotion blocks.

P7-T02 should convert this template into a stricter artifact schema and
validator. P7-T01 intentionally does not implement P7-T02 validator
enforcement.

V14 P9-T02 should update the review template and schema surfaces so future
review artifacts explicitly test process-authority laundering,
evidence-as-adoption laundering, no-target certificate overread, and `RR_E`
separation collapse when in scope.

## Acceptance Check

P7-T01 and v14 P9-T01 acceptance criteria are met when:

- the role contract exists and has `may_promote_claims: false`;
- the role is registered in `registries/AGENT_ROLE_REGISTRY.csv`;
- the current role name and kind identify internal skeptical review while the
  stable legacy role ID remains unchanged;
- current task-index projection displays the internal name alongside the
  legacy ID rather than presenting the ID as external provenance;
- external human review and independent replication remain available only
  through taxonomy-qualified evidence;
- the role states that it does not duplicate Gate Chair authority;
- the role states that it complements, but does not replace, Smuggling Auditor
  and Refuter authority;
- the review template exists;
- v14-specific attack surfaces are explicit in the role contract;
- authorized literature comparison is conditional on the owning AgentJob;
- the role cannot adopt or reject physics objects, override canonical sources,
  claim a global no-go theorem without a routed theorem artifact, or create
  permanent role authority;
- validation passes.

## Handoff

The logical next continue-research packet is P7-T02: create a red-team review
artifact schema and validator. That packet should use
`validator-engineer@0.2.0` or `project-control-maintainer@0.2.0`, preserve
`may_promote_claims=false`, and validate the P7-T01 template without running a
pilot review.

## References

The AEther-Flow Research Project. (2026, June 30). *Handoff 0382* [Internal
research-control handoff].

The AEther-Flow Research Project. (2026, June 30). *Recommendations
implementation plan continue task v12* [Internal implementation plan].
