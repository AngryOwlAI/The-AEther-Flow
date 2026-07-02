<!-- authority: control -->

# Matter-Coupling Pre-Adoption Checklist

## Purpose

This checklist implements v14 P11-T02. It is required before any future route
requests adoption of matter semantics, detector semantics, a coupling-law
candidate, or matter-coupling status.

The checklist is an intake and boundary-control surface. It does not adopt an
object, prove a theorem, authorize matter coupling, authorize stress-energy
semantics, authorize a matter action, derive Einstein equations, promote a
benchmark, or complete a derivation.

## When Required

Use this checklist for any task that asks to adopt, gate, promote, or treat as
settled any of the following:

- matter semantics;
- detector semantics or a source-side replacement for detector semantics;
- coupling-law target or coupling-law candidate;
- matter-coupling precondition as more than scoped evidence/precondition;
- matter-coupling derivation or adoption;
- stress-energy semantics or matter action as downstream matter-sector
  structure.

If the task only constructs a proposal, theorem target, stress packet,
smuggling audit, red-team review, or selector artifact, the checklist may be
used in abbreviated form. The packet must still state that no adoption occurs.

## Required Checklist

Every adoption-facing packet must answer the following sections in a tracked
artifact or completion receipt.

| Section | Required content |
| --- | --- |
| Exact object proposed for adoption | Name the exact object, notation, version, source path, task id, job id, and completion path. Do not replace it with a stronger adjacent object. |
| Status before adoption request | State whether the object is `proposal-only`, `draft/control`, `source-extension data`, `accepted_as_scoped_evidence_precondition`, `canonical-ontology candidate`, `adopted`, `rejected`, or `human-gated`. |
| Source files inspected | List canonical source files and registry rows inspected. Generated wiki, HTML, PDF, local cache, validator output, role identity, and handoff text are support only. |
| Accepted evidence/preconditions used | Cite exact scoped evidence/preconditions and their authority limits. State whether each is evidence, precondition, proposal, or adopted source. |
| Missing laws or semantics | List missing matter semantics, detector semantics, coupling law, stress-energy semantics, matter action, dynamics path, source transport rule, invariance rule, or adoption law. |
| No-target certificate hygiene check | Confirm that no-target, no-detector, no-stress-energy, no-action, no-benchmark, and no-process-authority certificates prevent imports only and do not provide positive matter theory. |
| `RR_E` separation check | State whether the object needs `RR_E` separation, transport, invariance, or factorization certificates. If absent, the route must fail closed or remain non-adoptive. |
| Stress/audit history | List smuggling audits, Refuter stress tests, route-orbit checks, freeze evaluations, and unresolved objections. |
| Red-team status | State whether external red-team review exists and whether findings are resolved, deferred, or blocking. |
| Literature comparison status | State whether literature comparison exists and whether it is background only. External resemblance must not be treated as validation. |
| Required Gate Chair authority | Name the exact protected Gate Chair or human-gated decision required for adoption, or state why the packet remains non-adoptive. |
| Forbidden adjacent promotions | Explicitly block adjacent promotions not requested or not established. |

## Required YAML Shape

Adoption-facing packets should include a machine-checkable block equivalent to:

```yaml
matter_coupling_pre_adoption_checklist:
  checklist_version: "v14_p11_t02"
  exact_object:
    name: ""
    version: ""
    source_path: ""
    task_id: ""
    job_id: ""
    completion_path: ""
  status_before_adoption_request: ""
  source_files_inspected: []
  accepted_evidence_preconditions_used: []
  missing_laws_or_semantics: []
  no_target_certificate_hygiene_check:
    status: "pending"
    notes: ""
  rr_e_separation_check:
    status: "pending"
    required_certificates: []
    missing_certificates: []
  stress_audit_history:
    smuggling_audits: []
    refuter_stress_tests: []
    route_orbit_or_freeze_checks: []
    unresolved_objections: []
  red_team_status:
    status: "not_started"
    findings: []
  literature_comparison_status:
    status: "not_started"
    background_only: true
    external_resemblance_as_validation: false
  required_gate_chair_authority:
    required: true
    scope: ""
    authority_path: ""
  forbidden_adjacent_promotions: []
  adoption_verdict_after_packet: "not_adopted"
```

Allowed `status` values for no-target and `RR_E` checks are `pass`, `fail`,
`blocked`, `not_applicable`, and `pending`. A `pass` value means the checklist
item was structurally addressed under the packet scope. It is not a theorem or
adoption decision.

## Forbidden Adjacent Promotions

Unless a separate protected authority explicitly establishes the exact claim, a
checklist-bearing packet must forbid:

- canonical ontology edit;
- source-law adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption;
- `PositiveMSProfile_v1` adoption as matter semantics;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption as a source law;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- coupling-law adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor, or matter action;
- Einstein equations;
- benchmark promotion;
- completed derivation;
- future source-extension impossibility; and
- broad theory rejection.

## Gate Discipline

An adoption request must identify the exact protected Gate Chair or human-gated
decision requested. If the request cannot name a protected authority scope, the
route must be reclassified as proposal-only, draft/control, selector,
audit/stress, or scoped-obstruction work.

Human authorization to run implementation-plan packets does not by itself
convert scoped evidence/preconditions into adopted physics objects. Adoption
still requires the exact tracked authority record named in the checklist.

## Continuation

The logical next v14 route after this checklist is P11-T03: narrow theorem
target selector. The selector should use the P11-T01 moratorium and this
checklist to choose a lower-authority theorem, precondition, target
formalization, or obstruction route rather than direct matter-coupling
derivation.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan for `/continue-research`, v14* [Internal implementation
plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v14.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling derivation
moratorium* [Internal control source].
`research_control/design/matter_coupling_derivation_moratorium.md`

The AEther-Flow Research Project. (2026, July 2). *Handoff 0487*
[Internal research-control handoff]. `research_control/handoffs/handoff-0487.yaml`
