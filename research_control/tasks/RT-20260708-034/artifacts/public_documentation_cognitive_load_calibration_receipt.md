<!-- authority: control -->

# P9-T03 Public Documentation Cognitive-Load Calibration Receipt

## Scope

Task `RT-20260708-034` implements v18 `P9-T03` for recommendation `V18-R09`.
The packet updates public-facing Markdown, paired source specs, and publication
briefs to use status-card v2 wording:

1. positive status;
2. exact scope;
3. blocked overread;
4. next burden.

The packet does not regenerate generated HTML prose or layout. Because paired
source specs changed, the established explainer validation pipeline required
metadata-only synchronization of the affected generated HTML source-basis hash
fields. The generated HTML surfaces remain tracked derivatives and should be
fully regenerated only by a bounded publication or renderer packet that
explicitly authorizes that output class.

The packet also extends the research-control validator's mutable
memory-preflight public-doc allowlist for the remaining P9-T03 public surfaces.
This preserves historical AgentJob receipts while allowing governed public
documentation source hashes to move under a bounded documentation packet.

## Public Surfaces Updated

- `README.md`
- `github-facing/project-overview-explainer.md`
- `github-facing/proof-state-dashboard-explainer.md`
- `github-facing/source-authority-explainer.md`
- `github-facing/aether-flow-physics-program-explainer.md`
- `github-facing/aether-flow-ontology-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`
- `github-facing/claim-gates-explainer.md`
- `github-facing/negative-results-and-obstructions-explainer.md`

## Source Specs And Briefs Updated

The corresponding source specs and publication briefs now cite
`research_control/design/status_card_v2_schema.md` and
`research_control/design/accepted_status_calibration_v2.yaml` where the public
page uses status-card v2 language.

## Generated HTML Metadata Synchronized

Only the `aether-flow-source-basis-hash` metadata was synchronized for these
generated derivatives:

- `html/project-overview-explainer.html`
- `html/proof-state-dashboard-explainer.html`
- `html/source-authority-explainer.html`
- `html/aether-flow-physics-program-explainer.html`
- `html/aether-flow-ontology-explainer.html`
- `html/gr-derivation-roadmap-explainer.html`
- `html/claim-gates-explainer.html`
- `html/negative-results-and-obstructions-explainer.html`

## Result

The public docs now state scoped positive status first, then exact scope,
blocked overread, and next burden. The changes reduce caveat-wall density
without relaxing the claim boundary. Public pages still state that they do not
derive matter coupling, derive Einstein equations, promote benchmark status,
issue a Gate Chair verdict, or complete the derivation.

## Validation

Task-local validation passed:

```zsh
.venv/bin/python research_control/tasks/RT-20260708-034/artifacts/validate_p9_t03_public_docs_status_cards.py --write-report --json
```

Report:
`research_control/tasks/RT-20260708-034/artifacts/p9_t03_public_docs_status_cards_report.json`

## Claim Boundary

This documentation update is not proof authority, source-law adoption,
detector-semantics adoption, matter-semantics adoption, coupling-law adoption,
matter-coupling derivation, stress-energy semantics, matter action,
Einstein-equation derivation, benchmark promotion, Gate Chair verdict,
completed derivation, future source-extension impossibility, or program-wide
no-go conclusion.

## Next Route

The next route is v18 `P9-T04`: status-card v2 linter tests.
