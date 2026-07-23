<!-- authority: control -->

# handoff-0834 — P10-T07 content-address identity recovery required

`RT-20260723-001` completed both repairs authorized by generation 66:

- `RT-20260722-022` through `RT-20260722-024` now use the existing valid
  `benchmark_or_recovery` / `not_applicable` taxonomy values.
- The design-only P10-T05 architecture packet now binds the current governed
  `report_physics_progress_metrics.py` SHA-256, and its validation and compact
  receipt deterministically pass.

All event-store activation and authority flags remain unchanged. The exact-path
Git policy and protected P15-T01 package remain byte-preserved, and the
P15-T01 package still passes all 161 checks.

The pre-checkpoint P10 migration-readiness test exposed a distinct deterministic
projection dependency: P10-T07 still contains the predecessor P10-T05 contract
identity. Its validator reports exactly three drift paths—the artifact manifest,
the new `cc7d6783…` content-addressed copy, and the compact receipt—with zero
semantic check failures. Those paths were outside the immutable generation-66
AgentJob write set, so no checkpoint, staging, commit, or legacy-validation
fallback was attempted.

The next bounded recovery is
`reseal_p10_t07_content_addressed_identity_after_p10_t05_v1`. It may regenerate
only the current contract copy and deterministic P10-T07 identity outputs,
must retain the predecessor `e22bde41…` copy, must prove P10 migration
readiness, and may then invoke one normal checkpoint. P15-T03 remains
dependency-ready in the ordinary route but is not execution-ready until that
checkpoint commits.

No scientific status, Distance-to-GR ledger, ontology, source law, benchmark,
publication authority, proof authority, physical interpretation, or completed
derivation claim changes in this handoff.
