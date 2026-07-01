<!-- authority: control -->

# V13 Recommendation Trace Matrix

Task: `RT-20260701-005`  
Plan task: `P0-T03`  
Status: `control aid only`

## Scope

This matrix links v13 recommendation IDs to phases, plan tasks, expected
artifacts, validators, dependencies, and claim boundaries. It is a
research-control aid. It is not a physics proof, source-law adoption, Gate
Chair verdict, benchmark promotion, or completed-derivation claim.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `completed_prior` | Completed by tracked state before this packet. |
| `completed_this_packet` | Completed by `RT-20260701-005`. |
| `pending_after_p0_t04` | Requires P0-T04 execution-gate selection before execution. |
| `pending_selector_dependent` | Requires a future selector or stress result before exact execution. |
| `pending_final_audit` | Requires broad v13 implementation evidence first. |

## Recommendation Matrix

| Rec | Summary | Phase(s) | Task IDs | Task type | Required role | Expected artifacts | Physics milestone affected | Promotion allowed | Validators | Status | Dependency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R1` | Stop using bare `accepted`. | P1, P8, P14 | P1-T01..P1-T05; P8-T01..P8-T05; P14-T01..P14-T05 | control/docs/prompts | documentation/control plus project-system tooling if validators change | vocabulary control note; status alias map; examples; public table updates; wording updates | none | No | bootstrap; documentation-impact; research-control; linter/tests when added | pending_after_p0_t04 | P0-T04 selects ordering; P1 normally precedes public propagation. |
| `R2` | Stress `SourceMatterSemanticsAdoptionReadinessLaw_v1` as immediate research priority. | P2 | P2-T01..P2-T03 | physics stress and boundary update | `refuter@0.2.0`, then selector/control | stress artifact; post-stress route selector; boundary update | `matter_coupling` | No automatic promotion | physics completion validators; Distance-to-GR status; research-control; bootstrap | pending_after_p0_t04 | Deferred by handoff-0411 until P0-T04 confirms route. |
| `R3` | After stress, route a selector rather than leaping to matter coupling. | P3 | P3-T01..P3-T04 | physics/control route discipline | selector/control roles | no-leap route rule; selector checklist; route template; pilot | `matter_coupling` | No | research-control; route-cycle checks; bootstrap | pending_selector_dependent | Requires P2 stress result or P0-T04 route decision. |
| `R4` | Build positive source-side matter semantics, not only anti-smuggling guards. | P4 | P4-T01..P4-T06 | physics source-law target/candidate/audit/stress chain | ontology-formalizer, candidate-constructor, smuggling-auditor, refuter, selector | target packet; candidate packet; audit; stress; selector; boundary update | `matter_coupling` | No automatic promotion | physics completion validators; source-extension category; research-control | pending_selector_dependent | Sequenced by post-stress selector; no adoption without gate. |
| `R5` | Treat `RR_E` as a mathematical fault line. | P5 | P5-T01..P5-T06 | physics theorem/obstruction chain | ontology-formalizer, candidate-constructor, smuggling-auditor, refuter, selector | theorem target; irrelevance theorem or obstruction; audit; stress; selector/freeze; boundary update | `matter_coupling` | No automatic promotion | physics validators; obstruction/freeze status; research-control | pending_selector_dependent | Sequenced by selector output, not plan inertia. |
| `R6` | Add a claim-language linter. | P6 | P6-T01..P6-T05 | tooling/control | project-system tooling/validator role | forbidden phrase taxonomy; linter; validation integration; remediations; handoff | none | No | unittest; documentation-impact; research-control; bootstrap | pending_after_p0_t04 | Can run before later physics if drift risk is high. |
| `R7` | Reconcile validation-status drift. | P7 | P7-T01..P7-T05 | tooling/control | project-system tooling/control | validation inventory; schema split; renderer/handoff update; backfill; validation | none | No | unittest if scripts change; documentation-impact; research-control; bootstrap | pending_after_p0_t04 | Best after P6 unless P0-T04 selects earlier repair. |
| `R8` | Keep the status-layer split and make it public-facing. | P8 | P8-T01..P8-T05 | docs/control | documentation-curator/control | public status table spec; README/docs updates; HTML source spec update; regeneration; validation | none | No | bootstrap; documentation-impact; public-doc validators; linter when available | pending_after_p0_t04 | Depends on P1 vocabulary and P7 schema clarity when possible. |
| `R9` | Add a three-tier claim convention to all summaries. | P9 | P9-T01..P9-T04 | control/docs/templates | project-control/documentation | claim convention policy; completion template; current frontier pilot; validation | none | No | research-control; documentation-impact; bootstrap | pending_after_p0_t04 | Should align with P1 and P7 status vocabulary. |
| `R10` | Create a compact frontier theorem inventory. | P10 | P10-T01..P10-T05 | control/science-facing inventory | project-control/science-facing support | schema; populated inventory; registry integration; renderer; validation | selected frontier objects only | No | bootstrap; registry validation; research-control | pending_after_p0_t04 | Requires stable claim vocabulary to avoid overread. |
| `R11` | Build support-only formalization without proof authority. | P11 | P11-T01..P11-T06 | tooling/support formalization | support/tooling role | lane design; enums; fail-closed maps; readiness skeleton; tests; boundary docs | none unless theorem attempt is separately routed | No | unittest; research-control; documentation-impact; bootstrap | pending_after_p0_t04 | Must preserve support-only/no proof-authority boundary. |
| `R12` | Prepare an external red-team packet. | P12 | P12-T01..P12-T05 | review/control | external-red-team-reviewer/control | role contract; review template; pilot; findings selector; validation | selected scoped objects | No | research-control; documentation-impact; bootstrap | pending_after_p0_t04 | May be moved earlier by P0-T04 or later selector need. |
| `R13` | Freeze repeated route orbits earlier. | P3, P13 | P3-T01..P3-T04; P13-T01..P13-T05 | route rule and tooling/control | selector/control plus project-system tooling | no-leap rule; route signature; history extractor; validator; pilot; validation | route-orbit risk only | No | route-orbit metrics; unittest if scripts change; research-control | pending_after_p0_t04 | Informs P3 selector discipline and P13 tooling hardening. |
| `R14` | Update local AI instructions with exact replacement wording. | P1, P14 | P1-T01..P1-T05; P14-T01..P14-T05 | prompts/docs/tests | project-control/documentation | exact wording blocks; role examples; negative examples/tests; summary audit; validation | none | No | documentation-impact; research-control; linter/tests when added | pending_after_p0_t04 | Should reuse P1 vocabulary and P9 three-tier convention. |
| `R15` | Add literature comparison and final audit. | P15, P16 | P15-T01..P15-T04; P16-T01..P16-T05 | review/literature and final audit | literature/review/control | scope selector; comparison packet; route selector; public boundary; coverage audit; metrics; frontier refresh; final validation; handoff | selected comparison targets only | No | APA 7 source discipline; bootstrap; research-control; metrics; final validators | pending_final_audit | P16 requires broad v13 evidence; P15 may move earlier only if selector requires external constraints. |

## Task Coverage Matrix

| Task | Name | Recommendation(s) | Status | Dependency | Claim boundary |
| --- | --- | --- | --- | --- | --- |
| P0-T01 | Plan intake transaction | all | completed_prior | none; completed in `RT-20260701-003` | control only; no physics claim change |
| P0-T02 | Live baseline reconciliation | all | completed_prior | P0-T01; completed in `RT-20260701-004` | control only; no physics claim change |
| P0-T03 | Recommendation trace matrix | all | completed_this_packet | P0-T02 | control aid only; no execution gate |
| P0-T04 | V13 execution gate | all | pending_after_p0_t04 | P0-T02 and P0-T03 artifacts | selects exactly one next task; no global authorization |
| P1-T01 | Scoped-positive claim vocabulary control note | R1, R8, R14 | pending_after_p0_t04 | P0-T04 | vocabulary only; no physics promotion |
| P1-T02 | Status alias map for high-risk burdens | R1, R8 | pending_after_p0_t04 | P1-T01 | status-language aid only |
| P1-T03 | Current-frontier wording pilot | R1, R8, R14 | pending_after_p0_t04 | P1-T01/P1-T02 | generated/current-frontier wording only |
| P1-T04 | Claim-language examples pack | R1, R14 | pending_after_p0_t04 | P1-T01 | examples only; no authority expansion |
| P1-T05 | P1 integration validation | R1, R8, R14 | pending_after_p0_t04 | P1-T01..P1-T04 | validation only |
| P2-T01 | Refuter stress of `SourceMatterSemanticsAdoptionReadinessLaw_v1` | R2 | pending_after_p0_t04 | P0-T04 must select it if route remains current | stress only; no adoption or promotion |
| P2-T02 | Post-stress route selector | R2, R3 | pending_selector_dependent | P2-T01 result | selector only; no leap to coupling |
| P2-T03 | P2 scientific boundary update | R2, R3 | pending_selector_dependent | P2-T01/P2-T02 | boundary update only |
| P3-T01 | No-leap route rule formalization | R3, R13 | pending_selector_dependent | P2 selector context | route rule only |
| P3-T02 | Selector checklist update | R3, R13 | pending_selector_dependent | P3-T01 | checklist only |
| P3-T03 | Post-stress route template | R3, R13 | pending_selector_dependent | P3-T01/P3-T02 | template only |
| P3-T04 | P3 validation and pilot | R3, R13 | pending_selector_dependent | P3-T01..P3-T03 | validation/pilot only |
| P4-T01 | Positive source-matter-semantics target formalizer | R4 | pending_selector_dependent | selector must choose positive semantics route | proposal-only target |
| P4-T02 | Positive source-matter-semantics candidate constructor | R4 | pending_selector_dependent | P4-T01 | proposal-only candidate |
| P4-T03 | Positive source-matter-semantics smuggling audit | R4 | pending_selector_dependent | P4-T02 | audit only; no adoption |
| P4-T04 | Positive source-matter-semantics Refuter stress | R4 | pending_selector_dependent | P4-T03 | stress only |
| P4-T05 | Positive source-matter-semantics post-stress selector | R4 | pending_selector_dependent | P4-T04 | selector only |
| P4-T06 | P4 boundary update | R4 | pending_selector_dependent | P4-T05 | boundary update only |
| P5-T01 | `RR_E` theorem target formalizer | R5 | pending_selector_dependent | selector must choose `RR_E` route | theorem target only |
| P5-T02 | `RR_E` irrelevance theorem attempt or obstruction | R5 | pending_selector_dependent | P5-T01 | theorem/obstruction draft only |
| P5-T03 | `RR_E` smuggling audit | R5 | pending_selector_dependent | P5-T02 | audit only |
| P5-T04 | `RR_E` Refuter stress | R5 | pending_selector_dependent | P5-T03 | stress only |
| P5-T05 | `RR_E` post-stress selector or freeze | R5, R13 | pending_selector_dependent | P5-T04 | selector/freeze only |
| P5-T06 | `RR_E` boundary update | R5 | pending_selector_dependent | P5-T05 | boundary update only |
| P6-T01 | Forbidden phrase taxonomy | R6 | pending_after_p0_t04 | P0-T04 | taxonomy only |
| P6-T02 | Claim-language linter implementation | R6 | pending_after_p0_t04 | P6-T01 | tooling only |
| P6-T03 | Integrate linter into validation workflow | R6 | pending_after_p0_t04 | P6-T02 | validator integration only |
| P6-T04 | Remediate linter findings | R6, R1, R8, R14 | pending_after_p0_t04 | P6-T03 | wording repair only |
| P6-T05 | P6 validation and handoff | R6 | pending_after_p0_t04 | P6-T01..P6-T04 | validation only |
| P7-T01 | Validation-field inventory | R7 | pending_after_p0_t04 | P0-T04 | inventory only |
| P7-T02 | Validation-status schema split | R7 | pending_after_p0_t04 | P7-T01 | schema/control only |
| P7-T03 | Renderer and handoff update | R7 | pending_after_p0_t04 | P7-T02 | renderer/handoff only |
| P7-T04 | Backfill latest active state | R7 | pending_after_p0_t04 | P7-T03 | backfill only |
| P7-T05 | P7 validation | R7 | pending_after_p0_t04 | P7-T01..P7-T04 | validation only |
| P8-T01 | Public status table source spec | R8, R1 | pending_after_p0_t04 | P1/P7 preferred | public spec only |
| P8-T02 | README and GitHub-facing status update | R8, R1 | pending_after_p0_t04 | P8-T01 | public docs only |
| P8-T03 | HTML explainer source-spec update | R8 | pending_after_p0_t04 | P8-T01 | source spec only |
| P8-T04 | Public status regeneration | R8 | pending_after_p0_t04 | P8-T02/P8-T03 | generated outputs only |
| P8-T05 | Public status claim-language validation | R8, R1, R6 | pending_after_p0_t04 | P8-T04 | validation only |
| P9-T01 | Three-tier claim convention policy | R9 | pending_after_p0_t04 | P1 preferred | policy only |
| P9-T02 | Completion template update | R9 | pending_after_p0_t04 | P9-T01 | template only |
| P9-T03 | Current frontier three-tier pilot | R9 | pending_after_p0_t04 | P9-T01/P9-T02 | pilot only |
| P9-T04 | P9 validation | R9 | pending_after_p0_t04 | P9-T01..P9-T03 | validation only |
| P10-T01 | Inventory schema | R10 | pending_after_p0_t04 | P1/P9 preferred | schema only |
| P10-T02 | Populate core inventory | R10 | pending_after_p0_t04 | P10-T01 | inventory entries only |
| P10-T03 | Inventory registry integration | R10 | pending_after_p0_t04 | P10-T02 | registry integration only |
| P10-T04 | Inventory renderer | R10 | pending_after_p0_t04 | P10-T03 | renderer only |
| P10-T05 | P10 validation | R10 | pending_after_p0_t04 | P10-T01..P10-T04 | validation only |
| P11-T01 | Formalization lane design | R11 | pending_after_p0_t04 | P0-T04 | support-only design |
| P11-T02 | Status enum formalization | R11, R1, R9 | pending_after_p0_t04 | P11-T01 | enums only |
| P11-T03 | Fail-closed map formalization | R11 | pending_after_p0_t04 | P11-T01 | support-only map |
| P11-T04 | Readiness map skeleton | R11, R2 | pending_after_p0_t04 | P11-T01 | skeleton only |
| P11-T05 | Formalization tests | R11 | pending_after_p0_t04 | P11-T02..P11-T04 | tests only |
| P11-T06 | Support-only boundary docs | R11 | pending_after_p0_t04 | P11-T01..P11-T05 | no proof-authority boundary |
| P12-T01 | External red-team role contract | R12 | pending_after_p0_t04 | P0-T04 | role contract only |
| P12-T02 | Red-team review template | R12 | pending_after_p0_t04 | P12-T01 | template only |
| P12-T03 | Red-team pilot on `M_src`, `g_eff`, and matter bridge | R12 | pending_after_p0_t04 | P12-T02 | review only; no promotion |
| P12-T04 | Red-team findings selector | R12 | pending_after_p0_t04 | P12-T03 | selector only |
| P12-T05 | P12 validation | R12 | pending_after_p0_t04 | P12-T01..P12-T04 | validation only |
| P13-T01 | Route signature definition | R13 | pending_after_p0_t04 | P0-T04 | definition only |
| P13-T02 | Route history extractor | R13 | pending_after_p0_t04 | P13-T01 | tooling only |
| P13-T03 | Route-orbit validator | R13 | pending_after_p0_t04 | P13-T02 | validator only |
| P13-T04 | Matter-semantics route orbit pilot | R13, R2, R4, R5 | pending_after_p0_t04 | P13-T03 | pilot only |
| P13-T05 | P13 validation | R13 | pending_after_p0_t04 | P13-T01..P13-T04 | validation only |
| P14-T01 | Continue Research prompt wording update | R14, R1 | pending_after_p0_t04 | P1 preferred | wording update only |
| P14-T02 | Role-specific wording examples | R14, R1 | pending_after_p0_t04 | P14-T01 | examples only |
| P14-T03 | Negative examples and correction tests | R14, R6 | pending_after_p0_t04 | P14-T02 | tests/examples only |
| P14-T04 | Generated summaries audit | R14, R1, R8 | pending_after_p0_t04 | P14-T03 | audit only |
| P14-T05 | P14 validation | R14 | pending_after_p0_t04 | P14-T01..P14-T04 | validation only |
| P15-T01 | Literature comparison scope selector | R15 | pending_after_p0_t04 | May move earlier only by selector need | scope selector only |
| P15-T02 | Literature comparison packet | R15 | pending_after_p0_t04 | P15-T01 | APA 7 comparison only |
| P15-T03 | Literature findings route selector | R15 | pending_after_p0_t04 | P15-T02 | selector only |
| P15-T04 | Literature comparison public boundary | R15, R8 | pending_after_p0_t04 | P15-T03 | public boundary only |
| P16-T01 | V13 coverage audit | all, R15 | pending_final_audit | Requires implemented or deferred prior phases | audit only |
| P16-T02 | Physics-progress metrics report | all, R15 | pending_final_audit | P16-T01 | metrics report only |
| P16-T03 | Current frontier final refresh | all, R15 | pending_final_audit | P16-T02 | generated frontier refresh |
| P16-T04 | V13 final validation | all, R15 | pending_final_audit | P16-T01..P16-T03 | final validators |
| P16-T05 | Ordinary research continuation handoff | all, R15 | pending_final_audit | P16-T04 | exactly one next route |

## Validator Map

| Change family | Default validators |
| --- | --- |
| Control-only task, DDR, handoff, registries | `bootstrap_memory_system.py`; `validate_documentation_impact.py`; `validate_research_control.py`; `validate_research_control.py --check-diff`; `render_current_frontier.py --check`; `git diff --check` |
| Physics task | Control validators plus physics completion fields, Distance-to-GR status, mathematical payload manifest, parent-child synthesis, route-cycle/freeze fields when applicable |
| Tooling or validator task | Control validators plus `python -m unittest discover -s tests` |
| Public documentation or generated surfaces | Control validators plus bootstrap regeneration and claim-language/linter validation when available |
| Literature comparison | Control validators plus APA 7 source discipline and explicit established-vs-project-construction separation |

## Acceptance Criteria Check

| Criterion | Status | Evidence |
| --- | --- | --- |
| Every Section 3 recommendation maps to at least one task | Pass | Recommendation matrix covers `R1` through `R15`. |
| Every task maps to at least one recommendation | Pass | Task coverage matrix maps all P0 through P16 tasks to recommendation IDs or all-phase control scope. |
| No task is orphaned | Pass | Every plan task heading from P0-T01 through P16-T05 has a row. |
| Matrix can be updated as phases complete | Pass | Status vocabulary separates completed prior, this packet, pending after gate, selector-dependent, and final-audit states. |
| Control-only boundary recorded | Pass | Scope and claim-boundary sections state no physics authority. |

## No-Promotion Boundary

This matrix does not change physics state. It does not adopt
`SourceMatterSemanticsAdoptionReadinessLaw_v1`, source-extension data, matter
semantics, detector semantics, a coupling law, matter coupling, stress-energy
semantics, a stress-energy tensor, a matter action, `MetricData(E)`, `g_eff`,
Einstein equations, benchmark status, benchmark Gate Chair closure, completed
derivation, future source-extension impossibility, or global theory rejection.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Handoff 0413*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v13* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 1). *V13 baseline reconciliation*
[Internal research-control artifact].
