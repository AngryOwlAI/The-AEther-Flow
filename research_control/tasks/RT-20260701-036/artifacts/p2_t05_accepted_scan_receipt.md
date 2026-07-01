<!-- authority: control -->

# P2-T05 Accepted-Wording Scan Receipt

## Scope

This receipt records the required P2-T05 search for unqualified high-risk
`accepted` wording in current docs and generated current-frontier surfaces.
The scan is a control-language check only.

## Commands

```zsh
rg -n "\baccepted\b" research_control/current_frontier.md research_control/design/scoped_positive_claim_vocabulary.md research_control/design/distance_to_gr_status_aliases.yaml research_control/design/scoped_claim_language_examples.md wiki/markdown/md-research-control-current-frontier.md
```

```zsh
rg -n "matter coupling is accepted|matter_coupling.*\baccepted\b|\baccepted\b.*matter_coupling|RR_ETransportCompletenessOrInvarianceLaw_v1 is.*accepted|PositiveMSProfile_v1 is.*accepted|g_eff.*accepted|M_src.*accepted" research_control/current_frontier.md research_control/design/scoped_positive_claim_vocabulary.md research_control/design/distance_to_gr_status_aliases.yaml research_control/design/scoped_claim_language_examples.md wiki/markdown/md-research-control-current-frontier.md
```

## Classification

The scan found four allowed classes:

1. Explicit policy language forbidding bare high-risk `accepted`.
2. Scoped-positive wording such as `accepted only as scoped source-extension evidence/precondition`.
3. Legacy-status table cells explicitly paired with reader-facing status, control status, mathematical status, physical status, promotion status, and overread guards.
4. Intentional bad-wording examples in the P2-T04 examples pack.

## Required Current-Frontier Checks

- `matter_coupling` renders as `accepted only as scoped source-extension evidence/precondition`.
- `PositiveMSProfile_v1` renders as scoped positive source-semantics evidence/precondition only.
- `RR_ETransportCompletenessOrInvarianceLaw_v1` renders as certificate-indexed transport-completeness or invariance evidence/precondition only.
- `m_src` and `g_eff` retain real scoped-positive status without being rendered as matter coupling, Einstein equations, benchmark promotion, or completed derivation.
- Legacy `accepted` fields remain visible only as legacy columns and are surrounded by scoped status layers and overread guards.

## Verdict

No unqualified high-risk `accepted` wording requiring P2 remediation was found
in `research_control/current_frontier.md` or the P2 control sources. The
remaining high-risk phrases are either scoped, legacy-labeled, or intentional
negative examples for future linter fixtures.
