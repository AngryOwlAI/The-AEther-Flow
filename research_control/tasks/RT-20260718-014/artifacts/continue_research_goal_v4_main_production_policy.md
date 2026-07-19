---
authority: control
object_id: "MD-CONTINUE-RESEARCH-GOAL-V4-MAIN-PRODUCTION-POLICY"
task_id: "RT-20260718-014"
decision_id: "DDR-20260718-014"
job_id: "AJ-RT-20260718-014-001"
status: "completed"
created_at: "2026-07-19T03:27:25Z"
updated_at: "2026-07-19T03:35:50Z"
owner_skill: "continue-research-goal"
claim_boundary_id: "CB-CONTINUE-RESEARCH-GOAL-V4-MAIN-PRODUCTION-001"
---

# Continue-Research Goal v4 Main-Production Policy

## Human policy decision

The user explicitly directed removal of the production `main` prohibition.
This packet implements that decision as a profile- and schema-specific change
instead of treating branch identity as a general safeguard bypass.

## Binding matrix

| Record | Profile | `main` | `codex/*` | Other branch |
|---|---|---:|---:|---:|
| New v4 | `production_profile` | allowed | allowed | rejected by the production launcher/worker contract |
| New v4 | `acceptance_test` | rejected | only the exact disposable acceptance branch | rejected |
| Retained v1-v3 | either retained profile | rejected | validation and summary only | governed by the retained contract |

The state helper mechanically allows `main` only when both
`schema_version == continue-research-goal.v4` and
`execution_profile == production_profile`. Initialization applies the same
rule.

## Preserved relay safeguards

Production `main` still requires the exact saved project, repository root, Git
common directory, immutable branch and starting HEAD, local environment mode,
clean validated checkpoint, combined goal-and-reasoning acceptance, supported
reasoning metadata, immutable scope and discussion contracts, lease parity,
one routed AgentJob per frame, deterministic recovery, and zero-or-one-child
dispatch.

The change does not authorize the launcher or worker to push, merge, rebase,
open a pull request, publish, install a controller, bypass validation, weaken a
human gate, or alter external systems.

## Compatibility

Existing v4 production records on `codex/*` remain valid. The acceptance
profile remains fixed to its disposable project and branch. Retained v1-v3
records remain byte-preserved validation-and-summary-only history and gain no
new ability to bind or resume on `main`.

## Research and claim boundary

This is project-control runtime policy. It does not launch a relay, modify
`program_state` or `handoff-0740`, change canonical physics or ontology,
advance a Distance-to-GR milestone, promote the exact-GR benchmark, or supply
proof authority.

## Verification contract

Focused tests and the task-local validator must prove:

1. v4 `production_profile + main` initializes and round-trips;
2. v4 `production_profile + codex/*` remains valid;
3. `acceptance_test + main` fails before state creation;
4. retained v1-v3 records bound to `main` fail validation;
5. all five runtime/test surfaces state the same binding policy; and
6. RT-20260718-013 plus ordinary research state remain unchanged.
