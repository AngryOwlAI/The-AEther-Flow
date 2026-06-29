<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
`RT-20260629-030` and `handoff-0325`.
It is generated from tracked control state. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | `RT-20260629-030` |
| Latest handoff ID | `handoff-0325` |
| Current status | `v12_p0_t02_baseline_snapshot_completed_no_promotion` |
| Current route family | v12 p0 t02 baseline snapshot completed next memory bootstrap |
| Target derivation milestone | none; this is project-control tooling work |
| Current burden | none for physics derivation; live control burden follows the next action: Run P0-T03 as one bounded continue-research transaction to ensure the v12 plan and baseline snapshot are discoverable through source-first memory before P1 work. |
| Required next authority | P0-T03 memory/bootstrap discoverability only |
| Next recommended action | Run P0-T03 as one bounded continue-research transaction to ensure the v12 plan and baseline snapshot are discoverable through source-first memory before P1 work. |

## Active Boundary

`current_frontier.md` is a generated snapshot under the P1 active-state
authority invariant. The precedence order remains:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger.
4. Task records, DDRs, AgentJobs, completions, claim-boundary rows, and
   role-execution rows provide transaction provenance.
5. This file is a generated synchronized snapshot only.

The P1-T03 validator guard fails validation when this snapshot drifts from
tracked active-state authority. The P1-T04 renderer now provides a deterministic
repair command:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --write
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_current_frontier.py --json
```

## Current Route Evidence

- Active task path: `research_control/tasks/RT-20260629-030/00_TASK.yaml`.
- Active task objective: Create the v12 P0-T02 post-v11 baseline authority snapshot from tracked state after P0-T01 intake without changing physics state.
- Latest handoff path: `research_control/handoffs/handoff-0325.yaml`.
- Latest handoff summary: V12 P0-T02 baseline authority snapshot completed. The packet records handoff-0323 as the post-v11 closure baseline and handoff-0324 as current routing authority after P0-T01, with no physics claim promotion.
- Current route family: v12 p0 t02 baseline snapshot completed next memory bootstrap.
- Next recommended action: Run P0-T03 as one bounded continue-research transaction to ensure the v12 plan and baseline snapshot are discoverable through source-first memory before P1 work.

## Matter-Coupling Boundary

The Distance-to-GR ledger currently records the `matter_coupling` burden row as `accepted`. Its blocking burden is: ParamFiniteLocalWitness_v1(E) BridgeSlot_n(E) and NoTargetImport_n accepted only as scoped source-extension parameterized-witness evidence/precondition for Matter-Coupling Bridge Target v1 while no source-law adoption coupling-law adoption matter-coupling derivation stress-energy semantics stress-energy tensor matter action detector semantics MetricData(E) adoption g_eff scope expansion Einstein-equation premise benchmark fit or downstream promotion is imported. The last evidence path is `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex`.

This ledger status must not be read as coupling-law adoption, universal matter-coupling derivation, matter-coupling adoption, stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, or completed derivation.

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
- [ ] generated graph, checker, registry, validator, local cache, role, handoff, approval, or commit status as scientific proof

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
| `m_src` | `source_manifold_m_src` | accepted | Scoped source-only M_src adoption granted for audited and stressed M_src^{GSC-cand}(E) under H1-H13 and fail-closed no-target-import discipline | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` |
| `g_eff` | `effective_metric_g_eff` | accepted | Scoped source-extension g_eff object adopted under declared source-side scope but downstream matter coupling Einstein equations benchmark promotion and completed derivation remain blocked | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` |
| `matter_coupling` | `matter_coupling` | accepted | ParamFiniteLocalWitness_v1(E) BridgeSlot_n(E) and NoTargetImport_n accepted only as scoped source-extension parameterized-witness evidence/precondition for Matter-Coupling Bridge Target v1 while no source-law adoption coupling-law adoption matter-coupling derivation stress-energy semantics stress-energy tensor matter action detector semantics MetricData(E) adoption g_eff scope expansion Einstein-equation premise benchmark fit or downstream promotion is imported | `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex` |
| `einstein_equations` | `einstein_equations` | not started | dynamics action or variation | `research_control/program_state.yaml` |
| `finite_variation_robustness` | `source_equivalence_eqsrc` | Refuter stress passed | arbitrary finite-variation preservation beyond fail-closed proposal-only FVR_src^GSC interface | `research_control/tasks/RT-20260614-101/artifacts/142_RESP_LC_M_SRC_GSC_FINITE_VARIATION_ROBUSTNESS_LAW_REFUTER_STRESS_TEST.tex` |
| `benchmark_promotion` | `benchmark_promotion` | blocked by missing primitive | all upstream derivation burdens | `research_control/program_state.yaml` |
| `gate_chair_status` | `benchmark_promotion` | human-gated | protected verdict authority | `research_control/approvals/README.md` |
| `finite_toy_metric_response` | `finite_toy_metric_response` | frozen negative | minimal finite response analogue | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` |

## Exact Next Route

The immediate next route is:

```text
Run P0-T03 as one bounded continue-research transaction to ensure the v12 plan and baseline snapshot are discoverable through source-first memory before P1 work.
```

The next route must be executed through tracked continue-research state. This
snapshot does not create physics authority, Gate Chair authority, benchmark
authority, or completed-derivation authority.

## Validation Status

Latest tracked state records:

- active task: `RT-20260629-030`;
- latest handoff: `handoff-0325`;
- current status: `v12_p0_t02_baseline_snapshot_completed_no_promotion`;
- renderer source: `scripts/research_control/render_current_frontier.py`;
- renderer policy: tracked-state snapshot only, not authority;
- claim boundary: no ontology edit, no source-law adoption, no `MetricData(E)` adoption, no `g_eff` scope expansion, no coupling-law adoption, no matter-coupling derivation or adoption, no stress-energy semantics, no Einstein equations, no benchmark promotion, no completed derivation, and no downstream GR promotion.
- latest handoff validation `blocking_drift_detected`: False;
- latest handoff validation `p0_t02_snapshot`: created;

## Retrieval Warning Status

This renderer reads only tracked control sources:

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0325.yaml`
- `research_control/tasks/RT-20260629-030/00_TASK.yaml`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

Memory, wiki notes, semantic extracts, Obsidian notes, PDFs, generated HTML,
SQLite indexes, and `.local/` caches remain retrieval or reader layers only.
They are not scientific authority and are not inputs to this rendered state.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 28). *Current research frontier*
[Generated internal control snapshot].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0325*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
