<!-- authority: control -->

# P3-T04 Positive-First Status-Card Renderer Receipt

## Scope

`RT-20260705-057` implements v17 P3-T04 as a project-control renderer update.

The packet updates the current-frontier and compact-frontier renderers so
high-risk accepted rows expose status cards in this order:

```markdown
**Positive status:** ...
**Scope:** ...
**Allowed use:** ...
**Blocked overread:** ...
```

The compact frontier also exposes matching machine-readable cards under
`high_risk_status_cards` and nested `high_risk_status_card` values on each
high-risk row.

## Changed Control Surfaces

```text
scripts/research_control/render_current_frontier.py
scripts/research_control/render_compact_current_frontier_v16.py
scripts/research_control/validate_compact_current_frontier_v16.py
tests/test_render_current_frontier.py
tests/test_render_compact_current_frontier_v16.py
tests/test_validate_compact_current_frontier_v16.py
research_control/current_frontier.md
output/compact_current_frontier_v16.yaml
output/compact_current_frontier_v16.json
wiki/indexes/compact_current_frontier_v16.md
```

## Claim Boundary

This receipt records renderer behavior only.

It does not adopt a source law, detector semantics, coupling law, matter
coupling, stress-energy semantics, stress-energy tensor, matter action,
Einstein equations, benchmark promotion, Gate Chair verdict, or completed
derivation.

## Verification

The task-local validator is:

```text
research_control/tasks/RT-20260705-057/artifacts/validate_p3_t04_positive_first_status_cards.py
```

Its report path is:

```text
research_control/tasks/RT-20260705-057/artifacts/p3_t04_positive_first_status_card_renderer_report.json
```

The broader verification set is recorded in
`AJC-AJ-RT-20260705-057-001.yaml`.

## Next Route

The immediate v17 continuation is P3-T05: public-facing documentation
calibration pass.
