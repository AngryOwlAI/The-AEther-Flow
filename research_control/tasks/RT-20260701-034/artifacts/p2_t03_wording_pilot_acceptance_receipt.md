<!-- authority: control -->

# P2-T03 Wording Pilot Acceptance Receipt

## Acceptance Criteria

| Criterion | Result | Evidence |
| --- | --- | --- |
| Inspect `render_current_frontier.py`. | PASS | `p2_t03_renderer_source_inventory.md` records renderer inspection. |
| Determine source of wording. | PASS | Renderer wording came from ledger fields plus handoff/task state; alias-map loading was absent. |
| Update the appropriate source, not generated output by hand. | PASS | Updated `scripts/research_control/render_current_frontier.py`, `scripts/research_control/validate_research_control.py`, `tests/test_render_current_frontier.py`, and alias-map integration metadata. |
| Regenerate current frontier. | PASS | `render_current_frontier.py --write` rendered hash `60ce1840dfc7cd46bb4af3007ddf72970ecfa317cc97f3aa01942fe6ec0d6d4f`. |
| Validate renderer check. | PASS | `render_current_frontier.py --check` returned status `pass`. |
| Confirm P5-T06 synchronization remains reflected. | PASS | Current frontier retains post-`RR_ETransportCompletenessOrInvarianceLaw_v1` scoped evidence/precondition boundary and routes to P2-T04 only. |
| `M_src`, `g_eff`, `matter_coupling`, `PositiveMSProfile_v1`, and `RR_ETransportCompletenessOrInvarianceLaw_v1` are distinguishable at a glance. | PASS | The generated frontier includes high-risk burden aliases and `matter_coupling` object aliases. |
| Frontier does not imply `matter_coupling` is solved. | PASS | `matter_coupling` renders as accepted only as scoped source-extension evidence/precondition, with matter coupling not derived and not adopted. |
| Frontier does not underclaim `M_src` or scoped `g_eff`. | PASS | `M_src` renders as adopted only as scoped source-only object; `g_eff` renders as adopted only as scoped source-extension object. |
| Frontier does not overclaim `RR_ETransportCompletenessOrInvarianceLaw_v1` as a source law. | PASS | Object alias renders it only as certificate-indexed `RR_E` transport-completeness or invariance evidence/precondition, not source-law adoption. |

## Renderer Payload

`render_current_frontier.py --json` reported:

- `status_alias_integration`: `reader_facing_status_column`
- `status_alias_path`: `research_control/design/distance_to_gr_status_aliases.yaml`
- `status_alias_row_count`: `11`
- `physics_claim_authority`: `false`
- `snapshot_only_not_authority`: `true`

## Scope

This receipt proves only P2-T03 current-frontier wording integration. It does
not prove P2-T04 examples, P2-T05 validation, P3 linter work, public status
propagation, matter-coupling derivation, Einstein-equation derivation,
benchmark promotion, or completed derivation.
