<!-- authority: control -->

# P6-T01 Payload-Density Metrics Design

## Purpose

This artifact completes P6-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v11.md`.
It defines payload-density and route-orbit diagnostics for
`report_physics_progress_metrics.py`.

The design is a project-control contract for P6-T02. It does not implement the
metrics and does not change any physics claim status.

## Boundary

All metrics defined here are diagnostics. They measure research-control
workflow shape, payload density, and route-orbit risk. They do not prove a
theorem, adopt a source law, adopt `MetricData(E)`, construct or expand
`g_eff`, derive matter coupling, import stress-energy semantics, construct a
stress-energy tensor, import a matter action or detector semantics, derive
Einstein equations, promote benchmark status, or complete the derivation.

Warnings are advisory control signals only. They are not hard validation gates
unless a later bounded project-system task explicitly converts one into a
validator rule.

## Source Basis

P6-T02 should compute these metrics from tracked control state only:

- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/tasks/*/jobs/completions/*.yaml`
- `research_control/tasks/*/artifacts/*checker_report.json`

Generated wiki notes, Obsidian notes, semantic extracts, SQLite memory, and
`.local/` caches must not be input authority. They may only help locate the
tracked sources above.

## Output Contract

P6-T02 should extend the metrics JSON with these top-level metric sections
under `report["metrics"]`:

- `payload_density_metrics`
- `route_orbit_risk_metrics`
- `diagnostic_warnings`

The existing `operational_validation_metrics`, `scientific_progress_metrics`,
`claim_hygiene_metrics`, `agent_workflow_metrics`, and
`metric_separation_guard` sections must remain present.

`payload_density_metrics` and `route_orbit_risk_metrics` are operational
diagnostic sections. They may read science-result receipt fields, but their
values do not become scientific claims. They must not be merged into
`scientific_progress_metrics`.

Each `diagnostic_warnings` entry should use this shape:

```yaml
warning_id: "same_burden_repetition"
severity: "warning"
metric_key: "same_burden_repetition_count"
observed_value: 5
threshold: 4
evidence_paths:
  - "research_control/tasks/RT-..."
recommended_guard_action: "Require construction, obstruction, gate, freeze review, or a sharper target before another same-burden selector packet."
hard_gate: false
physics_claim_authority: false
```

## Ordering And Filters

P6-T02 should sort jobs by `(created_at, job_id)` using
`AGENT_JOB_REGISTRY.csv`.

A completion is a physics completion when the corresponding role row has
`authority_level` in `science_draft` or `human_gated`, or `role_kind` starts
with `scientific_`.

For each physics completion, extract:

- `task_id`, `job_id`, `role_id`, `completed_at`, and `completion_path`
- `physics_progress_status.status`
- `physics_progress_status.target_derivation_milestone`
- `physics_progress_status.milestone_burden`
- `distance_to_gr_delta.changed`
- `distance_to_gr_delta.burden_id`
- `distance_to_gr_delta.milestone`
- `mathematical_payload_manifest`
- legacy `new_mathematical_payload`
- `route_cycle_control.cycle_family`
- `route_cycle_control.current_cycle_step`
- `route_cycle_control.cycle_risk`
- `candidate_constructor_result.result_type`
- `bridge_attempt_status` when present
- `theoretical_decision_output.selected_next_packet_type`
- `freeze_criteria_status.repeated_burden`
- `freeze_criteria_status.freeze_evaluation_required`
- `freeze_criteria_status.freeze_decision`
- `obstruction_record.present`
- `obstruction_record.obstruction_id`
- `forbidden_conclusion_summary.physics_promotion_authorized`

If a field is absent, count it as absent. Do not infer a physics result from
validation status, role identity, handoff text, registry presence, commit
state, or generated artifacts.

## Payload Count Rules

`payload_count` for one completion is:

1. The number of items in `mathematical_payload_manifest`, when that field is a
   list.
2. Otherwise the number of items in legacy `new_mathematical_payload`, when
   that field is a list.
3. Otherwise `0`.

Do not count `documentation_or_control_only_no_physics_delta`,
`selector_only_no_distance_delta`, validator reports, checker reports,
handoffs, role records, or documentation-impact receipts as mathematical
payload.

## Required Payload-Density Metrics

### `tasks_since_last_distance_to_gr_delta`

Definition: number of physics completions after the latest physics completion
whose `distance_to_gr_delta.changed` is `true`.

Computation: scan the ordered physics completions and reset the counter to `0`
after each `changed: true`; increment for later physics completions. If no
physics completion has `changed: true`, return the number of physics
completions.

Diagnostic class: payload-density warning input.

### `tasks_since_last_burden_discharged`

Definition: number of physics completions after the latest physics completion
whose `physics_progress_status.status` is `burden_discharged`.

Computation: scan ordered physics completions and reset after each
`burden_discharged`. If none exists, return the number of physics completions.

Diagnostic class: payload-density warning input.

### `new_payload_items_per_physics_task`

Definition: total payload count divided by physics completion count.

Computation: `sum(payload_count) / physics_completions_read`, rounded to two
decimals. Return `0` when there are no physics completions.

Diagnostic class: payload-density trend.

### `new_payload_items_per_cycle`

Definition: average payload count per route cycle.

Computation: group physics completions by
`route_cycle_control.cycle_family` when present. For completions without a
cycle family, P6-T02 may assign a synthetic family from contiguous
construct-audit-stress-selector role runs. Count one cycle when a family has at
least two distinct cycle steps or one completed construct-audit-stress-selector
role sequence. Divide total payload items in grouped completions by cycle
count, rounded to two decimals. Return `0` when no cycle exists.

Diagnostic class: payload-density trend.

### `selector_cycles_without_new_payload`

Definition: count of selector completions that select or recommend another
route while contributing zero payload items and not immediately routing to a
construction, obstruction, freeze review, or Gate Chair packet.

Computation: for each `theoretical-continuation-selector` completion with
`payload_count == 0`, inspect `theoretical_decision_output` and the next
physics completion. Count the selector when the selected or next route is
another selector/control-only step, or when no next physics completion exists.
Do not count a selector that routes directly to Candidate Constructor, Refuter
obstruction/no-go, Gate Chair, or freeze review.

Diagnostic class: route-orbit warning input.

### `same_burden_repetition_count`

Definition: maximum consecutive physics completions sharing the same
milestone/burden pair without a payload count greater than zero or a
Distance-to-GR delta.

Computation: normalize each completion's burden key from
`physics_progress_status.target_derivation_milestone`,
`physics_progress_status.milestone_burden`,
`distance_to_gr_delta.milestone`, and `distance_to_gr_delta.burden_id`. Reset
the streak when the burden key changes, `payload_count > 0`, or
`distance_to_gr_delta.changed` is `true`. Return the maximum streak.

Diagnostic class: route-orbit warning input.

### `freeze_reviews_triggered_by_repetition`

Definition: count of completions whose `freeze_criteria_status` indicates
`repeated_burden: true` or `freeze_evaluation_required: true`.

Computation: count ordered physics completions with either boolean true.

Diagnostic class: route-orbit trend.

### `bridge_attempts_since_last_gate`

Definition: count of bridge-facing construction attempts after the latest Gate
Chair completion.

Computation: locate the latest physics completion with role `gate-chair`.
After that point, count Candidate Constructor completions whose
`candidate_constructor_result.result_type` is `constructed_candidate`, any
completion with `bridge_attempt_status.candidate_map` or equivalent nonempty
bridge attempt field, and source-extension candidate constructions. Return
`0` if the latest Gate Chair completion is the final physics completion.

Diagnostic class: gate-readiness trend.

### `obstructions_created`

Definition: count of unique nonblank `obstruction_record.obstruction_id` values
where `obstruction_record.present` is true.

Computation: count unique IDs from completion YAMLs. If a present obstruction
has an empty ID, count it separately under an auxiliary
`obstructions_created_missing_id` key and emit a warning.

Diagnostic class: negative-result preservation.

### `obstructions_reused`

Definition: count of obstruction IDs created in one completion and referenced
by a later completion.

Computation: preserve the existing search discipline in
`report_physics_progress_metrics.py`: for each created obstruction ID, scan
later completion text for the ID and count the obstruction once when it is
referenced.

Diagnostic class: negative-result reuse.

### `candidate_construct_audit_stress_selector_cycles`

Definition: count of complete route cycles with Candidate Constructor,
Smuggling Auditor, Refuter, and Theoretical Continuation Selector steps in
that order for the same cycle family or contiguous role sequence.

Computation: prefer `route_cycle_control.cycle_family` and
`current_cycle_step` when present. For legacy completions, count contiguous
role sequences:

`candidate-constructor -> smuggling-auditor -> refuter -> theoretical-continuation-selector`

Do not require the sequence to promote claims. The metric only tracks route
shape.

Diagnostic class: route-orbit trend.

### `gate_ready_cycles_without_gate_verdict`

Definition: count of route cycles that reach apparent gate-readiness but do
not receive a later Gate Chair completion before the next unrelated cycle
begins.

Computation: a cycle is gate-ready when a completion records
`physics_progress_status.status: candidate_stress_passed_pending_gate`, a
selector chooses a Gate Chair/evidence-status packet, or a handoff/completion
route field explicitly names Gate Chair as the next required packet. Count it
when the next physics completion before a new construction cycle is not
`gate-chair`.

Diagnostic class: gate-readiness warning input.

### `support_only_tooling_reports`

Definition: count of support-only checker reports consumed by operational
metrics.

Computation: use `collect_support_only_checker_metrics` and report
`support_only_checker_reports_found`. Also include status counts and malformed
report parse errors under operational metrics.

Diagnostic class: tooling trend.

### `physics_promotion_authorized_true_count`

Definition: count of completions whose
`forbidden_conclusion_summary.physics_promotion_authorized` is true.

Computation: count explicit boolean true only. Do not infer true from Gate
Chair role identity or evidence acceptance.

Diagnostic class: claim-boundary hygiene.

### `physics_promotion_authorized_false_count`

Definition: count of completions with `forbidden_conclusion_summary` present
whose `physics_promotion_authorized` is not true.

Computation: `forbidden_conclusion_summary_count -
physics_promotion_authorized_true_count`, never below zero.

Diagnostic class: claim-boundary hygiene.

## Warning Policy

P6-T02 should emit warnings only. Warnings must not fail validation, alter
Distance-to-GR status, or route automatically unless a later handoff or
Director decision uses them as evidence.

Initial warning thresholds:

| Warning ID | Trigger | Recommended Action |
| --- | --- | --- |
| `same_burden_repetition` | `same_burden_repetition_count > 4` | Require construction, obstruction, gate, freeze review, or a sharper target before another same-burden selector/control-only packet. |
| `selector_without_payload_or_consequence` | `selector_cycles_without_new_payload > 2` | Prefer Candidate Constructor, Refuter obstruction/no-go, Gate Chair, or freeze review over another selector-only packet. |
| `post_gate_cycle_repeat` | A complete construct-audit-stress-selector cycle repeats after a Gate Chair accepted evidence/precondition and the next target is not materially harder. | Require a harder target, broader finite family, explicit bridge attempt, or freeze-review rationale. |
| `claimed_bridge_no_delta` | More than two completions in the same cycle contain route text claiming bridge progress while `distance_to_gr_delta.changed` remains false and `payload_count == 0`. | Require payload or narrow the claim language to control-only routing. |
| `candidate_missing_result` | Candidate Constructor completion lacks `candidate_constructor_result.result_type` and has no legacy equivalent. | Require a completion receipt repair or a future validator task to make the field mandatory. |
| `gate_ready_without_gate` | `gate_ready_cycles_without_gate_verdict > 0`. | Route the next packet to Gate Chair, explain why Gate Chair is not yet lawful, or withdraw gate-ready wording. |
| `obstruction_without_id` | Any present obstruction lacks a nonblank ID. | Repair future receipt templates; do not rewrite historical artifacts in this task. |
| `support_tooling_overread` | Any support-only checker report has forbidden overread flags, boundary mismatch, or nonblank `physics_obstruction`. | Treat as tooling or fixture-quality issue unless a later physics packet lawfully interprets it. |

## Separation Guard Requirements

P6-T02 must preserve the existing separation guard:

- Operational and diagnostic metrics must not be placed inside
  `scientific_progress_metrics`.
- `scientific_progress_metrics` remains a summary of explicitly tracked
  science-result fields.
- Payload-density metrics may read science-result fields but must be labeled
  diagnostic.
- Support-only checker metrics remain operational.
- Diagnostic warnings must carry `hard_gate: false` and
  `physics_claim_authority: false`.

If P6-T02 adds new diagnostic key tokens, it should update the metric
separation guard so accidental placement of those keys in
`scientific_progress_metrics` fails the focused test.

## P6-T02 Implementation Contract

P6-T02 should:

- Extend `scripts/research_control/report_physics_progress_metrics.py`.
- Add focused tests in `tests/test_research_control.py`.
- Preserve JSON output.
- Extend Markdown output with compact sections for payload-density metrics,
  route-orbit risk metrics, and diagnostic warnings when present.
- Avoid new runtime dependencies.
- Keep warning thresholds data-local and deterministic.
- Preserve all claim fences listed in this artifact.

P6-T02 should not:

- make any warning a hard validator gate;
- edit canonical science sources;
- change Distance-to-GR ledger rows;
- change `continue_research.py`; or
- implement P6-T03 route warning surfacing.

## P6-T01 Acceptance Review

The required P6-T01 metrics are all defined above. Each definition names the
source fields, computation rule, and diagnostic class. Thresholds are warning
only, and the implementation contract preserves operational/scientific metric
separation.

## Handoff

The logical next continue-research packet is P6-T02 with
`validator-engineer@0.2.0`, scoped only to implementing this design in
`report_physics_progress_metrics.py` and focused tests. P6-T02 must not
surface warnings in `continue_research.py`; that is P6-T03.

## References

The AEther-Flow Research Project. (2026, June 21). *Mathematical decisiveness
completion contract* [Internal control note].

The AEther-Flow Research Project. (2026, June 21). *Obstruction and freeze
control* [Internal control note].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0307* [Internal
control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
