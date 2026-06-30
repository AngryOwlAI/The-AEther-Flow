# Handoff 0384

RT-20260630-032 completed one bounded P7-T02 external red-team review
schema-validator packet.

The packet added `.agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md`,
`scripts/research_control/validate_red_team_review_artifact.py`, focused
fixtures under `tests/fixtures/research_control/red_team_review/`, focused unit
tests, and aligned `research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml`
with the enforced schema.

The validator requires all P7-T02 artifact fields, restricts verdicts to the
approved vocabulary, rejects generated/cache source paths in
`reviewed_source_paths`, and requires `physics_promotion_authorized: false`.

No pilot review was run. No Gate Chair authority, proof authority, source-law
adoption, `MetricData(E)` adoption, `g_eff` adoption or scope expansion,
coupling-law adoption, matter-coupling derivation or adoption, stress-energy
semantics, stress-energy tensor, detector semantics, matter action, Einstein
equations, benchmark promotion, or completed-derivation claim was created.

The logical next packet is P7-T03: run one pilot external red-team review using
`external-red-team-reviewer@0.1.0`, emit one schema-valid artifact, and keep
`physics_promotion_authorized: false`.
