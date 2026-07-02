<!-- authority: control -->

# P8-T03 Route-Orbit Validator Receipt

## Scope

This receipt covers the v14 P8-T03 route-orbit validator packet only.

## Implemented Tooling

- Added `scripts/research_control/validate_route_orbits.py`.
- Extended `scripts/research_control/extract_route_history.py` with
  non-comparison metadata used by warnings:
  `source_created_at` and `route_cycle_control_present`.
- Added `tests/test_route_orbit_validator.py`.
- Generated
  `research_control/tasks/RT-20260702-020/artifacts/p8_t03_route_orbit_validator_sample.json`.

## Validator Semantics

- Hard-fail candidate:
  same milestone, same burden, same missing primitive, same route shape, no new
  mathematical payload, no repair, no obstruction, no freeze evaluation, no
  boundary synchronization, and no new source evidence.
- Warning candidate:
  same burden with new payload and no `route_cycle_control`, Gate Chair scoped
  result followed by construction before boundary synchronization, or selector
  same-shape replay without `route_cycle_control`.
- The command is standalone and does not promote physics claims or freeze a
  route by itself.

## Focused Evidence

- `tests.test_route_history_extractor` and `tests.test_route_orbit_validator`
  passed together.
- The recent matter-coupling/`RR_E` sample produced:
  `status=PASS`, `signature_count=22`, `hard_failure_count=0`,
  `warning_count=0`.
- The task-local validator script confirms a synthetic no-progress repeated
  route emits one hard-fail candidate.

## Hashes

- route-orbit validator:
  `54c50c1f170ddab17cea686e36985ba198d86de8503765a64c6a49a35455a1c6`
- route-history extractor:
  `b01e9b9e4a216e6c5ca8c86e91d2d77e043539d24b76aa8cd7951c1d350536f4`
- route-orbit tests:
  `6b394fef45aa5498230a9b0ffff330fb0fb40a190fef47910698e460b1cd2b7f`
- sample report:
  `89ca8467bd4945b4bf7aa8b8a8409ccd36c897de299a58e296607ee3585d115d`

## Boundary

This packet creates operational validator tooling only. It does not authorize
canonical ontology edits, source-law adoption, matter-coupling derivation or
adoption, stress-energy semantics, matter action, Einstein equations,
benchmark promotion, route freezing, or completed derivation.
