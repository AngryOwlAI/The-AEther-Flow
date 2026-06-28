<!-- authority: control -->

# Handoff 0309

## Analysis

P6-T02 implemented payload-density and route-orbit diagnostics in
`scripts/research_control/report_physics_progress_metrics.py` and added
focused tests in `tests/test_research_control.py`.

The implementation emits:

- `payload_density_metrics`
- `route_orbit_risk_metrics`
- `diagnostic_warnings`

Diagnostic warnings are advisory only. They carry `hard_gate: false` and
`physics_claim_authority: false`. They are not Distance-to-GR evidence and do
not appear in `scientific_progress_metrics`.

## Verification

- `tests.test_research_control`: PASS
- `report_physics_progress_metrics.py`: PASS
- Markdown rendering includes payload-density, route-orbit, and warning
  sections.
- Metric separation guard: PASS

## Boundary

No canonical ontology edit, source-law adoption, `MetricData(E)` adoption,
`g_eff` adoption or scope expansion, coupling-law adoption, matter-coupling
derivation, stress-energy semantics, Einstein equations, benchmark promotion,
or completed-derivation claim is authorized or implied.

## Logical Next Step

Run one bounded P6-T03 `validator-engineer@0.2.0` packet to surface advisory
payload-density and route-orbit warnings in `continue_research.py` context
packets. Do not make warnings hard validation gates.
