<!-- authority: control -->

# Refuter Obstruction Schema v1

## Purpose

This control note completes P7-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
It defines the required record shape for future Refuter outputs that report an
obstruction, countermodel, certificate gap, local freeze, or blocked overread.

The schema is a project-control contract. It is not a physics theorem, not a
source-law adoption, not a Gate Chair verdict, and not proof authority. A
Refuter obstruction is local to its stated target, assumptions, and scope unless
a separate theorem and authorized gate prove a stronger claim.

Exact boundary phrases for validators: not a source-law adoption;
coupling-law adoption remains blocked; MetricData(E) adoption remains blocked.

## Authority Model

Future Refuter packets may use this schema to preserve negative results as
draft/control evidence. The record can support route selection, fixture design,
claim-language linting, and freeze review. It cannot by itself promote
canonical ontology, adopt source-extension data, derive matter coupling, derive
Einstein equations, promote benchmark status, or complete the derivation.

Historical Refuter artifacts remain governed by the contracts active when they
were created. A future backfill may map historical artifacts into this schema
only as metadata overlay and must preserve their original claim boundary.

## Required Record

Every future Refuter obstruction record must include the fields below. Empty
values are allowed only when the field definition explicitly permits them.

```yaml
refuter_obstruction_record:
  obstruction_id:
  target_claim:
  target_milestone:
  failed_premise:
  minimal_countermodel_available:
  countermodel_path:
  countermodel_scope:
  certificate_gap:
  source_extension_repair_possible:
  global_no_go_claim_authorized:
  future_source_extension_impossibility_authorized:
  freeze_criteria_status:
  route_cycle_control:
  forbidden_conclusions:
```

## Field Definitions

| Field | Required content |
| --- | --- |
| `obstruction_id` | Stable identifier for the negative result. Use a project-local token such as `OB-P7T01-CERT-GAP-001`. |
| `target_claim` | Exact claim, theorem target, candidate route, or overread being attacked. Vague statements such as "the proof needs work" are insufficient. |
| `target_milestone` | Roadmap milestone or `none` for control-only targets. Valid physics examples include `source_ontology`, `source_equivalence_eqsrc`, `response_localization_resp_lc`, `source_manifold_m_src`, `effective_metric_g_eff`, `matter_coupling`, `einstein_equations`, `benchmark_promotion`, and `finite_toy_metric_response`. |
| `failed_premise` | Minimal failed assumption, missing primitive, invalid certificate, target import, nonunique construction, malformed proof step, or unsupported transition rule. |
| `minimal_countermodel_available` | Boolean. `true` only when the artifact supplies or cites a minimal finite/local countermodel or witness. |
| `countermodel_path` | Canonical path to the countermodel artifact or fixture. Use an empty string only when `minimal_countermodel_available: false`. |
| `countermodel_scope` | Scope of the countermodel: `none`, `finite_local`, `exact_finite_branch`, `current_ontology_only`, `source_extension_candidate`, `general_source_cover`, `downstream_metric`, `matter_coupling`, `einstein_equations`, or `benchmark_promotion`. |
| `certificate_gap` | Certificate, provenance, witness, invariance, transport, factorization, detector-semantics, target-import, or proof-object gap. Use `none` only when no certificate-style gap is involved. |
| `source_extension_repair_possible` | Boolean or controlled string. `true` / `repair_possible` keeps same-milestone continuation open; `false` is allowed only for the scoped candidate under test and does not imply future source-extension impossibility. |
| `global_no_go_claim_authorized` | Boolean. Default `false`. May be `true` only when a separate no-go theorem plus required human-gated authority explicitly authorizes a global claim. |
| `future_source_extension_impossibility_authorized` | Boolean. Default `false`. May be `true` only when a separate theorem plus required human-gated authority proves future source-extension impossibility. |
| `freeze_criteria_status` | Structured freeze status following `research_control/design/obstruction_and_freeze_control.md`. It must state whether the route is `not_frozen`, `locally_frozen`, `freeze_review_required`, or `human_gate_required`. |
| `route_cycle_control` | Structured route-cycle record naming the cycle family, current step, prior related tasks, orbit risk, orbit-avoidance reason, and next role or stop condition. |
| `forbidden_conclusions` | Nonempty list of conclusions that must not be inferred from this record. It must include every relevant downstream overread blocked by the target scope. |

## Required Distinctions

The record must distinguish these four cases:

| Case | Meaning | Required indicators |
| --- | --- | --- |
| Scoped obstruction | A named premise, source object, certificate, or route fails under declared assumptions. | `failed_premise`, scoped `countermodel_scope`, forbidden global overreads. |
| Finite countermodel | A minimal finite/local object shows a target claim fails in that finite scope. | `minimal_countermodel_available: true` and a nonempty `countermodel_path`. |
| Global no-go | A theorem blocks a target class globally. | `global_no_go_claim_authorized: true` plus external theorem and authorization evidence. |
| Freeze | A repeated route or failure should pause or narrow under route-cycle controls. | structured `freeze_criteria_status` and `route_cycle_control`. |

If neither a global no-go theorem nor future-source-extension impossibility
authority is present, both protected authorization fields must remain false.
Allowed language is "current ontology does not derive X" or "this candidate
fails under scope S." Disallowed language is "therefore X is impossible" unless
the separate proof and gate authority are recorded.

## Minimal Valid Example

```yaml
refuter_obstruction_record:
  obstruction_id: "OB-P7T01-CERT-GAP-001"
  target_claim: "Unconditional matter-semantics equivalence without explicit source certificates"
  target_milestone: "matter_coupling"
  failed_premise: "The completion does not provide valid source certificates for every declared object."
  minimal_countermodel_available: true
  countermodel_path: "research_control/tasks/RT-EXAMPLE/artifacts/certificate_gap_fixture.yaml"
  countermodel_scope: "finite_local"
  certificate_gap: "missing declared source certificate for at least one object"
  source_extension_repair_possible: true
  global_no_go_claim_authorized: false
  future_source_extension_impossibility_authorized: false
  freeze_criteria_status:
    freeze_decision: "not_frozen"
    decision_reason: "A repair candidate with explicit certificates remains possible."
    next_allowed_route: "candidate_constructor"
  route_cycle_control:
    cycle_family: "matter_semantics_certificate"
    current_cycle_step: "refuter"
    prior_related_tasks: []
    cycle_risk: "low"
    orbit_avoidance_reason: "The record names a concrete certificate gap and a finite fixture."
    next_role_consequence: "candidate_constructor"
  forbidden_conclusions:
    - "No source-law adoption follows."
    - "No matter semantics or detector semantics adoption follows."
    - "No matter-coupling derivation follows."
    - "No Einstein-equation derivation follows."
    - "No benchmark promotion follows."
    - "No completed derivation follows."
    - "No program-wide no-go conclusion follows."
    - "No future source-extension impossibility follows."
```

## Validation Expectations

A future validator or claim-language linter should fail a new Refuter
obstruction record when:

- a required field is absent;
- `minimal_countermodel_available: true` has no `countermodel_path`;
- `minimal_countermodel_available: false` still claims a finite countermodel;
- a scoped obstruction is described as a global no-go with
  `global_no_go_claim_authorized: false`;
- future source-extension impossibility is claimed while
  `future_source_extension_impossibility_authorized: false`;
- `forbidden_conclusions` is empty or omits downstream blocks relevant to the
  target milestone;
- `freeze_criteria_status` omits the freeze decision; or
- `route_cycle_control` omits the route-cycle family or orbit-avoidance reason.

## Claim Boundary

This schema is support-only project-control evidence. It authorizes future
Refuter completions to be more formal. It does not authorize canonical ontology
edits, source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1`
adoption, unrestricted `RR_E` theorem authority, `PositiveMSProfile_v1`
adoption, `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption,
source-extension data adoption beyond exact scoped evidence/precondition
status, matter-semantics adoption, detector-semantics adoption, coupling-law
adoption, matter-coupling derivation or adoption, `MetricData(E)` adoption,
`g_eff` scope expansion, stress-energy semantics, a stress-energy tensor, a
matter action, Einstein equations, benchmark promotion, a Gate Chair verdict,
completed derivation, a program-wide no-go conclusion, or future
source-extension impossibility.

## Next Route

The logical next P7 packet is P7-T02, a minimal countermodel fixture library.
That future packet may use this schema but must create its own bounded
Continue Research transaction and claim-boundary receipt.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, June 21). *Obstruction and freeze
control* [Internal project-control note].
`research_control/design/obstruction_and_freeze_control.md`

The AEther-Flow Research Project. (2026, July 3). *Matter-coupling dependency
DAG v1* [Internal project-control note].
`research_control/design/matter_coupling_dependency_dag_v1.md`
