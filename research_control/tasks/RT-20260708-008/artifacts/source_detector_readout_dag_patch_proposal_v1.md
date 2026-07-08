<!-- authority: control -->

# Source Detector/Readout DAG Patch Proposal v1

## Purpose

This artifact completes the DAG side of v18 P5-T02. It is a patch proposal only.
It does not edit
`research_control/design/matter_coupling_dependency_dag_v1.md` and it does not
update `registries/DISTANCE_TO_GR_LEDGER.csv`.

The question is:

Should a later bounded, explicitly authorized packet add
`source_detector_readout_semantics` as a proposal-only support node that
clarifies the already-blocked detector-semantics target?

## Existing DAG Context

The current DAG has the blocked node:

```yaml
node_id: "mc_detector_semantics_target"
label: "detector-semantics target"
node_kind: "physical_target"
semantic_layer: "detector_semantics"
status: "blocked"
```

The missing burden recorded there is detector semantics or an explicitly
source-side replacement for detector semantics established under tracked
authority. P5-T01 named `source_detector_readout_semantics` as such a possible
source-side burden, but only with status `proposal_burden_only`.

## Proposed Future DAG Node

The following node is not applied by this task. It is the proposed shape a
later protected or explicitly authorized project-control packet may consider:

```yaml
node_id: "mc_source_detector_readout_semantics_burden"
label: "source detector/readout semantics burden"
node_kind: "evidence_precondition"
semantic_layer: "detector_semantics"
status: "proposal_only"
authority_status: "question_only_until_later_authorized_update"
source_path: "research_control/design/source_detector_readout_semantics_burden_v1.md"
source_registry: "MARKDOWN_SOURCE_REGISTRY.csv"
source_field: "burden_id: source_detector_readout_semantics"
evidence_basis:
  - "P5-T01 defined source_detector_readout_semantics as proposal_burden_only."
  - "The matter-coupling moratorium requires detector semantics or an explicitly source-side replacement before direct universal matter-coupling work."
required_authority_before_promotion:
  - "A later bounded DAG or ledger update AgentJob explicitly allowlisting the target path."
  - "A later candidate-constructor packet producing Det_src or Readout_src candidate evidence."
  - "Smuggling audit and Refuter stress before any adoption-facing read."
forbidden_overread_guards:
  - "no_Det_src_adoption"
  - "no_Readout_src_adoption"
  - "no_detector_semantics_adoption"
  - "no_empirical_detector_protocol_authority"
  - "no_proper_time_normalization"
  - "no_target_metric_authority"
  - "no_matter_coupling_derivation"
  - "no_stress_energy_semantics"
  - "no_matter_action"
  - "no_Einstein_equations"
  - "no_benchmark_promotion"
  - "no_completed_derivation"
downstream_blocks:
  - "mc_universal_matter_coupling_derivation"
  - "mc_einstein_equation_dependency"
  - "mc_benchmark_promotion_dependency"
notes: "Proposal-only burden surface; not detector semantics and not matter coupling."
```

## Proposed Future Edge

The following edge is not applied by this task:

```yaml
edge_id: "mc_edge_source_detector_readout_burden_to_detector_target"
source_id: "mc_source_detector_readout_semantics_burden"
target_id: "mc_detector_semantics_target"
edge_kind: "supports_as_evidence"
source_path: "research_control/design/source_detector_readout_semantics_burden_v1.md"
source_field: "Allowed Future Routes"
summary: "A proposal-only source detector/readout burden may support later candidate setup, but it does not discharge detector semantics."
forbidden_overread_guards:
  - "no_evidence_as_adoption"
  - "no_detector_semantics_adoption"
  - "no_matter_coupling_derivation"
  - "no_benchmark_promotion"
```

## Ledger Delta Question

P5-T02 asks whether a later protected packet should represent this burden in
the Distance-to-GR ledger. The answer is not executed here. If represented
later, the only safe initial status is equivalent to:

```yaml
proposed_burden_id: "source_detector_readout_semantics"
proposed_status: "proposal_burden_only"
proposed_control_status: "burden_proposed_not_adopted"
proposed_mathematical_status: "readout_law_missing"
proposed_physical_status: "not_detector_semantics_not_matter_coupling"
promotion_status: "none"
requires_protected_authority_to_update_ledger: true
update_performed_in_this_task: false
```

## Done Criteria

- The DAG patch is a proposal only.
- No populated DAG edit is performed in P5-T02.
- No Distance-to-GR ledger update is performed in P5-T02.
- The next route is P5-T03: source detector/readout candidate setup.

## Source Materials

The Aether-Flow Research Project. (2026, July 7). *Recommendations
implementation plan Continue Task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`

The Aether-Flow Research Project. (2026, July 8). *Source detector/readout
semantics burden v1* [Internal control note].
`research_control/design/source_detector_readout_semantics_burden_v1.md`

The Aether-Flow Research Project. (2026, July 2). *Matter-coupling dependency
DAG v1* [Internal control note].
`research_control/design/matter_coupling_dependency_dag_v1.md`
