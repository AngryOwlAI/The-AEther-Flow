<!-- authority: control -->

# Handoff 0832 — Exact-path policy complete, checkpoint planner blocked

`RT-20260722-023` adds four literal `.gitattributes` rules for the four
immutable P15-T01 files. Their SHA-256 identities remain unchanged, an adjacent
control path remains unclassified, and the isolated Git proof still reports
that control path for a new blank line at EOF. No wildcard or legacy validation
was used.

The P15-T01 package remains task-locally valid and the exact 171-test shard
passes. The one normal governed checkpoint invocation stopped before staging:
the validation classifier reports root `.gitattributes` as
`unknown_governed_path`, so the shadow checkpoint plan is not safe. Nothing was
staged or committed, and legacy validation was not used. This recovery changes
no scientific claim, ontology, ledger, Distance-to-GR status, external-review
status, publication authority, proof authority, or completed-derivation status.

The selected next route is one fresh bounded Validator Engineer recovery. It
may add one literal root `.gitattributes` classifier mapping to the existing
`ci_orchestration` validation family, add focused positive and fail-closed
negative regressions, preserve the four exact rules and protected hashes, and
invoke the normal checkpoint once. P15-T03 was not executed and remains
pending until that checkpoint commits.

- Handoff ID: `handoff-0832`
- Source task: `RT-20260722-023`
- Source job: `AJ-RT-20260722-023-001`
- Completion: `AJC-AJ-RT-20260722-023-001`
- Selected recovery plan task: `P15-T01`
- Selected worker skill: `improve-project-system`
- Blocker: `validation_blocker_checkpoint_planner_unknown_gitattributes_v1.yaml`
- Required recovery: exact root `.gitattributes` classifier admission, focused
  regressions, then one normal governed checkpoint without legacy validation
