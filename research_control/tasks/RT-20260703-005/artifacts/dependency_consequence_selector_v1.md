<!-- authority: science_draft -->

# P5-T02 Dependency Consequence Selector v1

## Control Status

| Field | Value |
| --- | --- |
| Task | `RT-20260703-005` |
| Job | `AJ-RT-20260703-005-001` |
| Role | `theoretical-continuation-selector@0.1.0` |
| Plan | `recommendations_implementation_plan_continue_task-v15.md` |
| Plan task | `P5-T02` |
| Target milestone | `matter_coupling` |
| Selector status | draft/control route decision only |
| Gate verdict issued | false |
| Physics promotion authorized | false |

This artifact implements one bounded v15 P5-T02 dependency consequence
selector after the P5-T01 upstream dependency audit. It selects exactly one
next route and does not execute that future route.

## Evidence Basis

| Source | Selector use |
| --- | --- |
| `handoff-0523` | Authorizes one bounded P5-T02 dependency consequence selector. |
| P5-T01 audit | Classifies `EqSrc`, `RetainH`, and `GenH` as not required for current P2 scope and conditionally required for broader matter-sector continuation. |
| v15 plan | Lists P5-T02 candidate routes and places P6 source-extension classification after P5. |
| GR burden map | Requires physics packets to preserve distance-to-GR burdens and avoid promotion by route mechanics. |

The P5-T01 audit result is used only as dependency evidence. It is not a
general `EqSrc` theorem, not `RetainH`, not `GenH`, and not source-law
adoption.

## Candidate Route Matrix

| P5-T02 route | Disposition | Reason |
| --- | --- | --- |
| Continue current matter-semantics route with dependency boundary note | not selected | The current scoped theorem route already has the P5-T01 boundary note; the next unresolved v15 control need is source-extension classification enforcement. |
| Narrow `EqSrc` theorem packet | not selected | P5-T01 found general `EqSrc` not required for the current explicit-certificate theorem scope. A broader EqSrc route remains possible later if a future packet removes certificate premises or seeks family-wide source equivalence. |
| Narrow `RetainH` primitive/theorem packet | not selected | P5-T01 found no current H-retention quantification. A RetainH route remains conditional for future retention-preservation work. |
| Narrow `GenH` primitive/theorem packet | not selected | P5-T01 found no current H-generated source-family construction. A GenH route remains conditional for future H-indexed source-family work. |
| Source-extension classification | selected | This is the next v15 phase and directly prevents scoped source-extension success from being overread as derivation, adoption, matter coupling, or benchmark progress. |
| Protected human-gated ontology authority request | not selected | The current step needs classification discipline, not canonical ontology edit or ontology adoption. |
| Freeze packet | not selected | No repeated missing primitive blocks the current scoped route; P5-T01 explicitly did not trigger freeze. |

## Selected Route

Exactly one route is selected:

```text
P6-T01 source-extension classification checklist
```

The selected next role family is:

```text
project-control-maintainer@0.2.0 with ontology-formalizer consultation if needed
```

The selected next packet should create
`research_control/design/source_extension_classification_checklist_v1.md` and
classify source-extension objects using the v15-required categories:

- `derived_from_current_ontology`;
- `conservative_definitional_extension`;
- `new_ontology_primitive_candidate`;
- `forbidden_target_import`;
- `status_boundary_evidence_only`;
- `blocked_adoption_open_continuation`.

## Theoretical Decision Output

| Field | Value |
| --- | --- |
| `selected_next_packet_type` | `source_extension_candidate` |
| `selected_next_route_family` | `source_extension_classification` |
| `selected_next_role_family` | `project-control-maintainer@0.2.0` |
| `selected_next_task_id` | `P6-T01` |
| `decision_basis` | P5-T01 dependency audit, v15 phase order, no current-scope requirement for general `EqSrc`, `RetainH`, or `GenH`, and no freeze trigger. |
| `theoretical_method` | Compare each P5-T02 candidate route against P5-T01 dependency classifications, current theorem scope, Distance-to-GR burden status, source-extension control requirements, and promotion blocks. |
| `preserves_claim_blocks` | true |
| `requires_human_gate` | false |
| `human_gate_reason` | No protected ontology edit, adoption verdict, benchmark closure, or completed-derivation authority is required for P6-T01. |
| `source_extension_category` | `source_extension_candidate` |
| `source_extension_import_classification` | The next packet is a control checklist for classifying future source-extension objects; it is not itself source-extension adoption, matter coupling, or a proof of derivation. |

## Route-Orbit Advisory Handling

The current resolver reports advisory route-orbit warnings
`candidate_missing_result` and `gate_ready_without_gate`. These warnings do
not hard-gate P5-T02. P5-T02 does not select a Gate Chair packet because
P5-T01 produced dependency-audit evidence, not a protected adoption question.
It also does not repair historical candidate-result metadata. The selected
P6-T01 route addresses status-control risk directly without widening the
scientific claim surface.

## Distance-To-GR Effect

This selector changes no Distance-to-GR ledger row. It narrows the next lawful
packet to source-extension classification enforcement.

| Burden | Status after selector |
| --- | --- |
| Source equivalence `EqSrc` | no change; general theorem still not discharged |
| `RetainH` | no change; primitive/theorem still not adopted |
| `GenH` | no change; primitive/theorem still not adopted |
| matter coupling | no derivation or adoption |
| Einstein equations | blocked |
| benchmark promotion | blocked |
| completed derivation | blocked |

## Forbidden Conclusions

This selector is not:

- a general `EqSrc` theorem;
- `RetainH` adoption;
- `GenH` adoption;
- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem authority;
- `PositiveMSProfile_v1` adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- stress-energy semantics, stress-energy tensor, or matter action;
- Einstein-equation derivation;
- benchmark promotion;
- a Gate Chair verdict; or
- completed derivation.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 3). *V15 P5-T01 upstream
dependency audit for EqSrc, RetainH, and GenH* [Internal science draft].

The AEther-Flow Research Project. (2026, July 3). *Handoff-0523* [Internal
research-control handoff].
