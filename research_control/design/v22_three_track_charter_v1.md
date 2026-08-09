<!-- authority: control -->

# V22 Three-Track Program Charter v1

## Purpose and authority

This charter makes four accounting classes independently accountable:

1. **Track A — exact-GR interpretation**;
2. **Track B — first-principles source reconstruction**;
3. **Track C — AI research-operating-system evaluation**; and
4. **Shared control — routing, validation, release control, and program
   synthesis that belongs to none of the three research tracks.**

It implements V22 P1-T01 as project-control governance. It changes no
scientific claim, source ontology, Distance-to-GR burden, Gate status,
benchmark result, review status, publication authority, or repository layout.

## Assignment invariant

Every V22 work package has exactly one `primary_track` chosen from `track_a`,
`track_b`, `track_c`, or `shared_control`. A package may name participating or
referenced tracks, but those links do not create a second primary assignment,
task-count credit, cost center, evidence credit, or authority owner. The exact
40-package assignment is controlled by
`v22_plan_task_track_assignments_v1.yaml`.

## Track charters

| Class | Purpose | Allowed success claims | Failure measures | Authority owner | Dashboard | Publication lane |
| --- | --- | --- | --- | --- | --- | --- |
| Track A | Explain the target-side exact-GR interpretation, congruence kinematics, established-GR agreement, and observer-relative philosophy. | Interpretive coherence, faithful target-side GR agreement, clear 1+3 comparison, and scoped external philosophical/GR review when actually obtained. | Ambiguous ontology language, target/source conflation, nonunique-flow overstatement, or missing source-status disclaimer. | Director of Research for routing; canonical source owners and separately authorized reviewers for content; no Gate authority. | `v22_track_a_dashboard_v1` | `track_a_interpretation_paper_d`; no source-derived-law claim. |
| Track B | Attempt a source-side derivation of operational Lorentzian geometry and, only after positive prerequisites, Einstein-leading dynamics; otherwise preserve scoped failure. | Source-side theorems, explicit candidates, robustness results, protected Gate evidence, independently replicated benchmarks, and scoped obstructions within their exact authority. | Missing primitive, target import, nonuniqueness, nonrobustness, Gate failure, benchmark failure, or budget-bounded scoped obstruction. | Director of Research for routing; task-selected scientific roles for construction; Gate Chair only under exact human-gated authority. | `v22_track_b_dashboard_v1` | Track-B Papers A, B, and E; any source-derived-GR paper remains locked until its explicit Gates are positive. |
| Track C | Evaluate the AI research operating system, including claim gates, provenance, role separation, negative-result memory, efficiency, and cost. | Descriptive results; causal methodology claims only after the preregistered comparative experiment and blinded adjudication support them. | Invalid-claim rate, defect-recall loss, false positives, unreproduced analysis, excessive control cost, or failed causal identification. | Project-System Director for system routing; task-selected methodology roles and separately authorized adjudicators for study results. | `v22_track_c_dashboard_v1` | `track_c_methodology_paper_c`; descriptive and causal claims remain explicitly separated. |
| Shared control | Maintain task routing, validation, provenance, release controls, cross-track status, and plan closure without taking research credit. | Conformance, traceability, freshness, bounded cost, and internally reproducible control state. | Ambiguous authority, stale projections, double counting, missing provenance, disproportionate overhead, or unauthorized external action. | Project-System Director and task-selected project-control roles; protected outward action remains human-gated. | `v22_shared_control_dashboard_v1` | Control/status artifacts only; it cannot merge A, B, or C claims into a publication conclusion. |

## Non-promotion rules

- Track A and Track C always carry `distance_to_gr_effect: none`.
- Shared-control completion, validation, checkpointing, or documentation always
  carries `distance_to_gr_effect: none`.
- Only Track B may propose a Distance-to-GR change, and only an authorized
  science completion plus the applicable protected Gate can enact it.
- Track B may not cite Track A interpretive coherence, exact target-side GR
  agreement, Track C methodology results, workflow conformance, validator
  PASS, checkpoint success, or control traceability as Gate evidence.
- Cross-track references use the typed contract in
  `v22_cross_track_reference_schema_v1.yaml`; every such link has
  `authority_effect: none`, `evidence_credit: none`, and
  `distance_to_gr_effect: none`.
- Review labels remain exact. Internal deterministic process checks are not
  external human review or independent scientific replication.

## Scorecard separation

Each class has a separate schema, metric namespace, dashboard ID, evidence
set, resource ledger, publication lane, and authority statement:

- `v22_track_a_scorecard_schema_v1.yaml`;
- `v22_track_b_scorecard_schema_v1.yaml`;
- `v22_track_c_scorecard_schema_v1.yaml`; and
- `v22_shared_control_scorecard_schema_v1.yaml`.

No aggregate dashboard may overwrite or infer a track-local status. A summary
may display the four scorecards side by side only when it preserves their
metric namespaces, denominators, evidence classes, and non-promotion flags.

## Resource accounting

Task count, elapsed effort, compute, and financial cost use four disjoint cost
centers defined in `v22_track_budget_allocation_v1.yaml`. Every task and every
measured resource event receives exactly one primary cost center. A cross-track
reference or dependency does not reallocate cost. Missing measurements remain
`not_measured`; they are never silently converted to zero.

## Repository-separation rule

The current decision is to retain the monorepo. A future split may be proposed
only from measured coupling, release-cadence divergence, access boundaries,
maintenance cost, and provenance-preservation evidence under
`v22_repository_separation_decision_v1.yaml`. Appearance, organizational
fashion, or track naming is never a sufficient reason. Executing a split
requires a separate human-authorized migration decision and is outside this
charter.

## Acceptance and non-authority

This charter is accepted operationally only when the assignment manifest has
40 unique packages, prohibited-promotion fixtures fail closed, scorecard and
dashboard namespaces are disjoint, budget totals do not double count, and the
process-integrity review reports no blocking control finding. Those checks do
not prove physics, validate the interpretation, establish methodology
superiority, complete external review, or authorize publication or release.
