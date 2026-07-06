<!-- authority: control -->

# AI Research-Agent Metrics Taxonomy v1

## Status

Task: `RT-20260706-033`

Plan task: `P12-T01`

Role: `process-integrity-auditor@0.1.0`

Output type: project-control methodology taxonomy.

This taxonomy implements v17 P12-T01. It defines AI research-agent methodology
metrics for controlled theoretical research behavior. It is not a measurement
run, not an executable report extension, not a physics proof, not a source-law
adoption, not an ontology change, not benchmark promotion, and not a Gate Chair
verdict.

P12-T02 is responsible for extending the physics-progress metrics report and
populating derived metric outputs from this taxonomy.

## Purpose

The research-agent system should be evaluated as a scientific instrument by
whether it improves controlled theoretical research behavior:

- it catches overclaims before they become authority;
- it warns when positive scoped status is omitted;
- it scopes obstructions precisely instead of globalizing them;
- it exposes route orbit and repeated-burden cycles;
- it records candidate life-cycle attrition from construction to audit and
  stress survival;
- it measures protected human-gate load without treating authorization as a
  scientific verdict;
- it tracks whether mathematical payload is being produced relative to process
  receipts.

These metrics are diagnostic controls. They may inform routing, warning text,
dashboard summaries, manuscript methodology claims, and validator priorities.
They cannot promote any physics claim.

## Metric Families

| Family | Purpose | Included metric IDs |
| --- | --- | --- |
| Claim-boundary control | Detect overclaim and underclaim errors in agent outputs and summaries. | `overclaim_catch_rate`, `underclaim_warning_rate` |
| Obstruction quality | Measure whether negative results are scoped to their actual burden and object. | `obstruction_precision` |
| Route dynamics | Detect repeated-burden cycles without new payload. | `route_orbit_rate` |
| Candidate life cycle | Track attrition from construction through audit and stress survival. | `candidate_to_audit_conversion`, `audit_to_stress_survival`, `stress_survival_rate` |
| Governance load | Count protected authority requests by phase without treating them as verdicts. | `human_gate_load` |
| Payload balance | Compare mathematical payload artifacts with process receipts. | `proof_to_process_ratio` |

## Metric Definitions

| Metric ID | Definition | Numerator | Denominator | Primary evidence sources | Interpretation guardrail |
| --- | --- | --- | --- | --- | --- |
| `overclaim_catch_rate` | Fraction of seeded or real overclaim surfaces caught before checkpoint. | Count of overclaim surfaces flagged by validators, red-team review, claim-language review, role synthesis, or handoff boundary checks. | Count of seeded or real overclaim surfaces that were eligible for detection in the reviewed scope. | `CLAIM_BOUNDARY_REGISTRY.csv`, claim-language validator output, red-team artifacts, task-local validator reports, completion receipts. | A high rate means better boundary control; it does not prove any physics claim. |
| `underclaim_warning_rate` | Fraction of high-risk summaries missing positive scoped status that were warned or corrected. | Count of eligible summaries where a missing positive scoped status was flagged or corrected. | Count of high-risk summaries whose tracked evidence included scoped positive status and whose public or compact summary could omit it. | accepted-status calibration artifacts, current-frontier checks, claim graph checks, task-local receipts. | This metric prevents pessimistic status collapse; it does not promote scoped evidence into adoption. |
| `obstruction_precision` | Fraction of obstruction records scoped with a non-global boundary. | Count of obstruction or negative-result records naming object, assumptions, route, and downstream blocked claim without globalizing. | Count of obstruction or negative-result records produced or reviewed in the measurement window. | negative-result inventory, completion receipts, handoffs, dependency graph inputs, claim boundary rows. | A precise obstruction remains local unless a separate theorem and protected authority establish a stronger no-go result. |
| `route_orbit_rate` | Frequency of repeated-burden cycles without new payload. | Count of route cycles returning to the same burden or equivalent continuation family without new mathematical payload. | Count of bounded continuation packets in the measurement window. | `report_physics_progress_metrics.py` diagnostics, AgentJob completions, task index, handoffs. | This is a process-warning metric; it is advisory unless a separate validator or policy makes a gate. |
| `candidate_to_audit_conversion` | Fraction of candidate-constructor outputs that become eligible for audit. | Count of candidate-constructor outputs with enough declared scope, assumptions, and artifacts to route to smuggling audit or equivalent audit. | Count of candidate-constructor outputs in the window. | candidate construction artifacts, route selector artifacts, AgentJob completions, claim-boundary rows. | Eligibility for audit is not audit survival, adoption, or matter-coupling derivation. |
| `audit_to_stress_survival` | Fraction of audited candidates that reach stress. | Count of audited candidates routed to Refuter stress or equivalent stress packet. | Count of audited candidates with completed audit disposition. | smuggling-audit artifacts, route selectors, completion receipts, handoffs. | Reaching stress means the candidate remains testable; it does not mean the candidate is true or adopted. |
| `stress_survival_rate` | Fraction of stressed candidates that survive as `draft/control`. | Count of stressed candidates whose post-stress status remains `draft/control` or equivalent non-promotional survivor status. | Count of stressed candidates with completed stress disposition. | Refuter stress artifacts, selector artifacts, completion receipts, status ledgers. | Survival is a candidate-status result only; it does not authorize canonical ontology, source-law, metric, or coupling adoption. |
| `human_gate_load` | Number of protected authority requests per phase. | Count of human-gated authority requests, Gate Chair requests, or protected adoption requests in a phase. | Phase identifier rather than a fractional denominator; report as count per phase and optional count per completed packet. | program state, handoffs, DDRs, Gate Chair artifacts, human-authorization receipts. | Human authorization for a task is not a Gate Chair verdict unless the exact protected gate says so. |
| `proof_to_process_ratio` | Mathematical payload artifacts compared with process receipts. | Count of new mathematical payload artifacts: definitions, lemmas, theorems, countermodels, explicit witnesses, bridge candidates, dependency maps, or source-side calculations. | Count of process receipts: DDRs, AgentJobs, handoffs, validation reports, memory receipts, generated graphs, and task-local receipts. | AgentJob completions, task index, Distance-to-GR metadata, payload-density diagnostics, validator reports. | This ratio is a productivity and balance signal; neither numerator nor denominator creates proof authority by itself. |

## Common Calculation Rules

1. Count only tracked artifacts or registry rows. Generated wiki notes,
   Obsidian notes, `.local/` caches, rendered graphs, and dashboard outputs may
   navigate to evidence but are not independent sources.
2. Use bounded measurement windows: by plan phase, by date range, by task-id
   interval, or by v17 continuation segment.
3. Treat missing denominator data as `not_measured`, not as zero, unless the
   measurement contract explicitly defines zero eligible items.
4. Preserve exact status labels such as `draft/control`, `proposal-only`,
   `accepted_scoped`, `blocked`, `human-gated`, and `frozen_negative`.
5. Record uncertainty when a numerator item depends on interpretation rather
   than deterministic validator output.
6. Do not mix physics-progress metrics with method-system diagnostics without
   a field that states `physics_claim_authority_created: false`.

## P12-T02 Reporting Contract

P12-T02 should extend the progress metrics report with a support-only
`ai_research_agent_methodology_metrics` object that preserves this taxonomy.
At minimum, each metric record should include:

```yaml
metric_id: "<one of the nine required IDs>"
family: "<metric family>"
status: "measured | not_measured | partial"
definition: "<taxonomy definition>"
numerator:
  value: null
  evidence_paths: []
denominator:
  value: null
  evidence_paths: []
calculation_window: ""
diagnostic_interpretation: ""
authority_boundary:
  physics_claim_authority_created: false
  physics_promotion_authorized: false
  gate_chair_verdict_created: false
  benchmark_promotion_authorized: false
```

The first report implementation may populate `not_measured` or `partial`
records when source extraction is not deterministic yet. That is preferable to
inventing unsupported values.

## Boundary and Forbidden Conclusions

This taxonomy permits only methodology diagnostics. It forbids the following
conclusions:

- metric success as physics proof;
- metric success as autonomous scientific authority;
- validation PASS as source-law adoption;
- candidate survival as canonical ontology adoption;
- candidate survival as matter-coupling derivation;
- route-orbit reduction as Einstein-equation derivation;
- human authorization as Gate Chair verdict unless the protected gate itself
  states that verdict;
- dashboard rendering as benchmark promotion;
- proof-to-process balance as completed derivation.

## No-Delta Receipt

- Scientific claims changed: false.
- Distance-to-GR ledger changed: false.
- Physics promotion authorized: false.
- Proof authority changed: false.
- Source-law adoption authorized: false.
- Matter-coupling derivation authorized: false.
- Einstein-equation derivation authorized: false.
- Benchmark promotion authorized: false.
- Gate Chair verdict created: false.
- Completed derivation authorized: false.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.

The AEther-Flow Research Project. (2026b). *Current research-control frontier*
[Project-control report]. `research_control/current_frontier.md`.

The AEther-Flow Research Project. (2026c). *V17 recommendation backlog*
[Project-control backlog]. `research_control/design/v17_recommendation_backlog.yaml`.
