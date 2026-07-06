<!-- authority: control -->

# AI Research-Agent Methodology Evaluation v1

## Status

Task: `RT-20260706-035`

Plan task: `P12-T03`

Role: `process-integrity-auditor@0.1.0`

Output type: support-only AI methodology evaluation memo.

This memo evaluates the research-agent system as a controlled theoretical
research instrument. It does not evaluate the truth of any physics claim. It
does not promote source laws, ontology, metric status, matter coupling,
Einstein equations, benchmark status, Gate Chair verdicts, or completed
derivation claims.

## Research-Agent Purpose

The research-agent system is useful when it improves controlled theoretical
research behavior under explicit claim gates. In this repository that means:

- routing one bounded packet at a time;
- preserving a durable trail from analysis to response artifacts to handoff;
- detecting overclaim and underclaim risks before checkpoint;
- keeping negative results scoped to exact assumptions and burdens;
- tracking whether candidates move through construction, audit, stress, and
  selector stages without being silently promoted;
- distinguishing human authorization for work from protected scientific
  verdicts;
- separating mathematical payload from process receipts.

The system should therefore be assessed as an epistemic control mechanism. Its
success criterion is not "proves GR." Its success criterion is whether it makes
theoretical work more auditable, less overclaim-prone, and more explicit about
what remains blocked.

## Metrics Definitions

The P12-T01 taxonomy defines nine support-only diagnostics.

| Metric | Family | Definition summary | Guardrail |
| --- | --- | --- | --- |
| `overclaim_catch_rate` | Claim-boundary control | Fraction of eligible overclaim surfaces caught before checkpoint. | High values mean stronger boundary control, not physics proof. |
| `underclaim_warning_rate` | Claim-boundary control | Fraction of high-risk summaries with omitted positive scoped status that were warned or corrected. | Prevents pessimistic status collapse without promoting scoped evidence into adoption. |
| `obstruction_precision` | Obstruction quality | Fraction of obstruction records scoped with object, assumptions, route, and downstream blocked claim. | A precise obstruction remains local unless a separate no-go theorem and authority establish more. |
| `route_orbit_rate` | Route dynamics | Frequency of repeated-burden cycles without new payload. | Advisory process warning, not Distance-to-GR status. |
| `candidate_to_audit_conversion` | Candidate life cycle | Fraction of candidate-constructor outputs eligible for audit. | Audit eligibility is not audit survival or adoption. |
| `audit_to_stress_survival` | Candidate life cycle | Fraction of audited candidates that reach stress. | Reaching stress means still testable, not true. |
| `stress_survival_rate` | Candidate life cycle | Fraction of stressed candidates that survive as `draft/control`. | Survival is non-promotional candidate status only. |
| `human_gate_load` | Governance load | Protected authority requests per phase. | Human authorization is not a Gate Chair verdict unless the protected gate says so. |
| `proof_to_process_ratio` | Payload balance | Mathematical payload artifacts compared with process receipts. | A balance signal; neither side creates proof authority by itself. |

## Current Measured Values

The P12-T02 report currently marks the overall AI-methodology metric set as
`partial`: nine metrics are present, the separation guard passes, and three
advisory warnings identify incomplete extraction.

| Metric | Status | Current value | Evaluation |
| --- | --- | --- | --- |
| `overclaim_catch_rate` | `measured` | `0.9309` | Strong boundary-control signal. The system is frequently recording forbidden-conclusion or promotion blocks before checkpoint. |
| `underclaim_warning_rate` | `not_measured` | `null` | The method lacks a deterministic extraction rule for high-risk positive scoped-status omissions. This is the main measurement gap. |
| `obstruction_precision` | `measured` | `1.0` | The current proxy reports scoped obstruction records with adequate local context. This is a useful guard against global no-go overread. |
| `route_orbit_rate` | `measured` | `0.0` | The current repeated-burden streak proxy is not showing same-burden repetition in this window. Route-orbit warnings remain advisory. |
| `candidate_to_audit_conversion` | `measured` | `0.8269` | Many candidates become audit-eligible, suggesting the workflow is generating reviewable candidate surfaces rather than only prose intentions. |
| `audit_to_stress_survival` | `partial` | `1.0` | The value is an aggregate stage proxy, not candidate-linked lineage. It should not be used as a survival claim until transition IDs are normalized. |
| `stress_survival_rate` | `partial` | `0.4096` | The value indicates some non-promotional survivor outcomes, but historical receipt normalization is incomplete. |
| `human_gate_load` | `measured` | `null` | This is a governance workload diagnostic rather than a scalar truth score. It must remain phase/count based. |
| `proof_to_process_ratio` | `measured` | `1.5696` | The current payload/process balance is evidence that the system is producing mathematical artifacts as well as receipts. It is not proof authority. |

The three current warnings are:

| Warning | Metric | Status | Hard gate | Physics authority | Interpretation |
| --- | --- | --- | --- | --- | --- |
| `underclaim_warning_rate_not_measured` | `underclaim_warning_rate` | `not_measured` | `false` | `false` | Needs a future extraction rule for omitted positive scoped status. |
| `audit_to_stress_survival_partial` | `audit_to_stress_survival` | `partial` | `false` | `false` | Current receipts count stage occurrences, not candidate-linked transitions. |
| `stress_survival_rate_partial` | `stress_survival_rate` | `partial` | `false` | `false` | Historical survivor lineage is not fully normalized. |

## Strengths

The system has a strong claim-boundary architecture. High overclaim-catch
performance, explicit forbidden-conclusion summaries, claim-boundary rows, and
handoff boundaries reduce the chance that local success is overread as source
law, matter coupling, benchmark promotion, or completed derivation.

The system preserves negative-result precision. The obstruction-precision
proxy reports that tracked obstruction records are locally scoped rather than
globalized. This is essential for speculative theoretical physics, where a
failed route must not become an unsupported impossibility theorem.

The candidate life-cycle is visible enough to support governance. The
candidate-to-audit conversion value indicates that many candidates are written
with enough structure to enter audit lanes. This makes the workflow more
falsifiable than a purely narrative research log.

The separation guard is functioning. AI-system diagnostics are kept outside
scientific progress metrics, and the report states that methodology metrics do
not create physics proof authority.

## Failure Modes

The underclaim-warning metric is not yet measured. The repository can warn
against overclaim more deterministically than it can detect omitted positive
scoped status. This creates a possible conservative-bias failure mode:
readers may see only blocked status and miss the exact positive scoped result.

Candidate lineage is not fully normalized across audit and stress. The current
`audit_to_stress_survival` and `stress_survival_rate` values are useful as
aggregate proxies, but they do not yet prove candidate-by-candidate transition
quality. This limits dashboard and threshold use.

The route-orbit warnings remain policy-sensitive. The current route-orbit rate
is zero for the measured proxy, while advisory diagnostics still report
gate-ready-without-gate pressure elsewhere. The system must avoid treating
either warning stream as a physics verdict.

The proof-to-process ratio can be misread. A high ratio can mean useful
mathematical payload, but it can also hide uneven quality if payload classes
are not reviewed by burden. A low ratio can mean administrative drag, but it
can also reflect necessary safety work. The metric needs context.

## Recommendations

1. Add a deterministic underclaim extraction rule before using
   `underclaim_warning_rate` for any threshold or dashboard signal.
2. Add candidate-transition identifiers that connect construction, audit,
   stress, selector, and survivor/disposition records.
3. In P12-T04, render AI-methodology dashboard values with explicit
   support-only labels and show warning status next to every partial or
   not-measured metric.
4. Keep route-orbit warnings advisory unless a separate control policy makes a
   hard gate.
5. Split proof-to-process reporting by payload class and burden before drawing
   productivity conclusions.
6. Preserve the analysis to response artifact to handoff loop as a core
   methodology invariant. It is the system's main protection against a single
   discussion run absorbing multiple unreviewed phases.

## Physics Claim Boundary

This memo creates no Distance-to-GR delta. It records no source-law adoption,
no canonical ontology edit, no `MetricData(E)` adoption, no `g_eff` scope
expansion, no matter-coupling derivation, no stress-energy semantics, no
matter action, no Einstein-equation derivation, no benchmark promotion, no
Gate Chair verdict, and no completed derivation.

The current methodology metrics are support-only diagnostics. They may guide
future routing, dashboard design, validator priorities, and manuscript
methodology discussion. They may not be cited as proof that the AEther-flow
substrate derives GR or any protected downstream physics object.

Boundary flags:

```yaml
physics_claim_authority_created: false
physics_promotion_authorized: false
gate_chair_verdict_created: false
benchmark_promotion_authorized: false
completed_derivation_authorized: false
distance_to_gr_delta: "none"
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.

The AEther-Flow Research Project. (2026b). *AI research-agent metrics taxonomy
v1* [Internal control document].
`research_control/design/ai_research_agent_metrics_taxonomy_v1.md`.

The AEther-Flow Research Project. (2026c). *Research-control metrics
separation report* [Generated support-only report].
`output/physics_progress_metrics.md`.

The AEther-Flow Research Project. (2026d). *Handoff 0666* [Research-control
handoff]. `research_control/handoffs/handoff-0666.md`.
