# GR Derivation Roadmap Recommendation Audit

Reference: Project review memo. (2026, June 17). *Review project goal
06-17-2026* [Internal project review].

## Scope

This audit verifies project-system implementation of all recommendations from
`reviews/review_project_goal_06-17-2026.md`. It does not execute a physics
AgentJob and does not promote any physics claim.

## Recommendation Coverage

| Review Item | Implementation Evidence | Verification Evidence |
| --- | --- | --- |
| Recommendation 1: Add a global derivation roadmap | `research_control/design/gr_derivation_burden_map.md` defines the milestone chain, accept criteria, and freeze criteria. | `scripts/research_control/validate_research_control.py` exposes `gr_derivation_roadmap_policy`; tests assert the policy appears in continuation status. |
| Recommendation 2: Force every next task to name its target milestone | Future physics AgentJobs after `2026-06-17T15:46:25Z` must declare `target_derivation_milestone` and `milestone_burden`; schema and templates were updated. | `test_roadmap_future_physics_job_requires_target_milestone` and `test_roadmap_future_physics_job_accepts_target_milestone`. |
| Recommendation 3: Create a Distance-to-GR Ledger | `registries/DISTANCE_TO_GR_LEDGER.csv` records required burdens, statuses, evidence paths, and blockers. | `validate_distance_to_gr_ledger` and `test_distance_to_gr_ledger_is_static_validated`. |
| Recommendation 4: Stop choosing new no-go questions until a constructive attempt is made | Theoretical Selector role now prefers constructive packets; validator requires `decision_consequence` and `new_payload_novelty` for future `distinct_scoped_no_go_question`. | `test_roadmap_selector_rejects_no_go_without_novelty_and_consequence`. |
| Recommendation 5: Add hard freeze criteria | Future repeated-burden or scoped-obstruction completions require `freeze_criteria_status`; roadmap names `NDCL-RESP-LC-SELECTOR-UNDERDETERMINATION`. | `test_roadmap_refuter_scoped_obstruction_requires_freeze_status` and `test_roadmap_refuter_accepts_freeze_status`. |
| Recommendation 6: Require new mathematical payload per physics task | Future physics completions require `new_mathematical_payload`; active physics roles and completion template were updated. | `test_roadmap_future_physics_completion_requires_new_payload`. |
| Recommendation 7: Separate derivation planning from agent-routing planning | Roadmap and ledger define derivation milestones separately from role routing; continuation JSON exposes `gr_derivation_roadmap_policy`. | `test_continue_research_reports_director_context_packet`. |
| Recommendation 8: Build a finite toy model target | Roadmap defines `finite_toy_metric_response`; Theoretical Selector packet type `finite_toy_metric_response_model` requires finite source set, response relation, metric analogue, and invariance checks. | `test_roadmap_selector_accepts_finite_toy_model_target`. |
| Recommendation 9: Make source extension an explicit controlled category | Theoretical Selector packet types include source-extension candidate, audit, stress, and human-gate routes; roadmap defines the adopted-or-rejected category. | `test_roadmap_selector_accepts_source_extension_category`. |

## Recommended Next Three Physics Moves

The review's suggested next physics moves were implemented as routing
constraints, not executed as science work:

| Review Move | Project-System Implementation |
| --- | --- |
| Move 1: Selector chooses minimal source-side selector primitive | Constructive packet priority in `theoretical-continuation-selector@0.1.0` and schema allows `source_side_selector_primitive`. |
| Move 2: Smuggling Auditor attacks selector data | Source-extension and selector packets remain draft/control and must pass audit/refutation before promotion. |
| Move 3: Refuter finite countermodel or witness | Future payload types include finite models, countermodels, explicit witnesses, and finite toy model target. |

## Boundary Check

No canonical ontology source, benchmark source, science draft, generated HTML,
PDF, or generated wiki note was hand-edited. The implementation is validator
and control-contract work only.
