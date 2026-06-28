<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
`RT-20260614-286` and `handoff-0319`. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | `RT-20260614-286` |
| Latest handoff ID | `handoff-0319` |
| Current status | `p1_t03_active_state_drift_validator_guard_completed_no_promotion` |
| Current route family | P1 active-state repair: current-frontier synchronization and validator guard completed; generated renderer still required |
| Target derivation milestone | none; this is project-control synchronization work |
| Current burden | none for physics derivation; the live control burden is P1-T04 generated current-state report command |
| Required next authority | one bounded P1-T04 generated current-state report packet under tracked continue-research state; no physics or Gate Chair authority is created here |
| Next recommended action | Run one bounded P1-T04 packet to add a deterministic current-frontier renderer before P8 final validation |

## Active Boundary

`current_frontier.md` is synchronized under the P1-T01 active-state authority
invariant. The precedence order remains:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger.
4. Task records, DDRs, AgentJobs, completions, claim-boundary rows, and
   role-execution rows provide transaction provenance.
5. This file is a synchronized snapshot only.

The P1-T03 validator guard now fails validation when this snapshot drifts from
tracked active-state authority. The P1-T04 generated frontier renderer remains
required. Until that renderer is complete, manual updates to this file remain
possible only under the invariant and must preserve this snapshot-only
boundary.

## Current Route Evidence

- `RT-20260614-283` completed the P8-T01 cross-phase audit and found that P2
  through P7 were complete while P1 active-state repair remained incomplete.
- `RT-20260614-284` completed P1-T01 by defining the active-state authority
  invariant and selecting Path A, a generated snapshot, as the target
  `current_frontier.md` policy.
- `RT-20260614-285` completes P1-T02 by synchronizing this file with live
  tracked state and the Distance-to-GR ledger context.
- `RT-20260614-286` completes P1-T03 by adding a deterministic
  active-state drift validator guard and focused regression tests.

Remaining P1 work:

- P1-T04 must add a deterministic current-frontier renderer.

## Matter-Coupling Boundary

The Distance-to-GR ledger currently records the `matter_coupling` burden row
as accepted only for scoped source-extension parameterized-witness evidence
and precondition status. That accepted evidence/precondition status must not
be read as coupling-law adoption, universal matter-coupling derivation,
matter-coupling adoption, stress-energy semantics, stress-energy tensor,
matter action, detector semantics, Einstein equations, benchmark promotion, or
completed derivation.

Universal matter coupling and downstream GR promotion remain blocked until a
separate tracked route and the required protected authorities establish them.

## Exact Blocked Claims

- [ ] canonical ontology edit
- [ ] source-law adoption
- [ ] `MetricData(E)` adoption
- [ ] `g_eff` adoption or scope expansion
- [ ] coupling-law adoption
- [ ] matter-coupling derivation
- [ ] matter-coupling adoption
- [ ] stress-energy semantics
- [ ] stress-energy tensor
- [ ] matter action
- [ ] detector semantics
- [ ] Einstein equations
- [ ] exact-GR benchmark promotion
- [ ] benchmark Gate Chair closure
- [ ] completed derivation
- [ ] future source-extension impossibility
- [ ] global theory rejection
- [ ] this snapshot as independent authority
- [ ] generated graph, checker, registry, validator, local cache, role,
  handoff, approval, or commit status as scientific proof

## Distance-To-GR Table

This table summarizes `registries/DISTANCE_TO_GR_LEDGER.csv`; the ledger
remains the authoritative source if this summary drifts.

| Burden ID | Milestone | Current status | Blocking burden | Last evidence |
| --- | --- | --- | --- | --- |
| `source_ontology_primitives` | `source_ontology` | draft object exists | canonical adoption rules | `AGENTS.md` |
| `source_equivalence_eqsrc` | `source_equivalence_eqsrc` | draft object exists | general equivalence under variations | `research_control/program_state.yaml` |
| `retain_h` | `source_equivalence_eqsrc` | blocked by missing primitive | canonical retention proof | `research_control/program_state.yaml` |
| `gen_h` | `source_equivalence_eqsrc` | blocked by missing primitive | canonical generator proof | `research_control/program_state.yaml` |
| `obsloc_lc` | `source_localization_obsloc_lc` | constructive witness exists | robustness and exact-branch limits | `research_control/tasks/RT-20260614-037/artifacts/58_LOCALIZATION_SOURCE_BASIS_AXIOM_SELECTOR_DOMAIN_EQSRC_ALTERNATIVE_BRANCH_FAMILY_GUARD_STABILITY_SOURCE_PACKET_SMUGGLING_AUDIT.tex` |
| `resp_lc` | `response_localization_resp_lc` | accepted | response selector sign scale and token semantics | `research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex` |
| `m_src` | `source_manifold_m_src` | accepted | scoped source-only `M_src` adoption is bounded and does not construct downstream GR objects | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` |
| `g_eff` | `effective_metric_g_eff` | accepted | scoped source-extension `g_eff` object is adopted only under declared source-side scope; downstream matter coupling, Einstein equations, benchmark promotion, and completed derivation remain blocked | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` |
| `matter_coupling` | `matter_coupling` | accepted scoped evidence/precondition only | no source-law adoption, coupling-law adoption, matter-coupling derivation, stress-energy semantics, stress-energy tensor, matter action, detector semantics, `MetricData(E)` adoption, `g_eff` scope expansion, Einstein-equation premise, benchmark fit, or downstream promotion is imported | `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex` |
| `einstein_equations` | `einstein_equations` | not started | dynamics action or variation | `research_control/program_state.yaml` |
| `finite_variation_robustness` | `source_equivalence_eqsrc` | Refuter stress passed | arbitrary finite-variation preservation beyond fail-closed proposal-only `FVR_src^GSC` interface | `research_control/tasks/RT-20260614-101/artifacts/142_RESP_LC_M_SRC_GSC_FINITE_VARIATION_ROBUSTNESS_LAW_REFUTER_STRESS_TEST.tex` |
| `benchmark_promotion` | `benchmark_promotion` | blocked by missing primitive | all upstream derivation burdens | `research_control/program_state.yaml` |
| `gate_chair_status` | `benchmark_promotion` | human-gated | protected verdict authority | `research_control/approvals/README.md` |
| `finite_toy_metric_response` | `finite_toy_metric_response` | frozen negative | minimal finite response analogue | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` |

## Exact Next Route

The immediate next route is:

```text
one bounded P1-T04 generated current-state report packet
```

The P1-T04 packet should add a deterministic command that renders this
snapshot from `research_control/program_state.yaml`, the latest handoff named
by that file, the active task folder, and
`registries/DISTANCE_TO_GR_LEDGER.csv`.

P1-T04 remains project-control tooling work only. It must not promote
physics claims or treat validator output as scientific proof.

## Validation Status

Latest completed packet `RT-20260614-286` records:

- selected route: `p1_t03_active_state_drift_validator_guard`;
- current-frontier policy: snapshot-only, not authority;
- current-frontier status: synchronized to `program_state.yaml`,
  `handoff-0319`, and Distance-to-GR ledger context;
- validator status: active-state drift guard implemented in
  `scripts/research_control/validate_research_control.py`;
- regression status: synchronized fixture passes, stale active-task snapshot
  fails, and stale active-burden status fails;
- next route: P1-T04 generated current-state report command;
- claim boundary: no ontology edit, no source-law adoption, no
  `MetricData(E)` adoption, no `g_eff` scope expansion, no coupling-law
  adoption, no matter-coupling derivation or adoption, no stress-energy
  semantics, no Einstein equations, no benchmark promotion, no completed
  derivation, and no downstream GR promotion.

## Retrieval Warning Status

Memory preflight before this update returned:

- `core_validation_status: PASS`
- `freshness_status: PASS`
- `local_retrieval_status: PASS`
- no blocking, local-cache-only, or non-blocking freshness warnings.

After this source edit, the local retrieval layer briefly reported local-cache
freshness warnings for the Obsidian raw mirror and SQLite memory index. The
post-sync refresh resolved those warnings and returned
`local_retrieval_status: PASS`.

Retrieval status is hygiene information only. It is not scientific authority.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 28). *Active-state authority
invariant* [Internal control artifact].

The AEther-Flow Research Project. (2026, June 28). *Active-state drift
validator guard* [Internal control artifact].

The AEther-Flow Research Project. (2026, June 28). *Current frontier
synchronization review* [Internal control artifact].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0319* [Internal
research-control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
