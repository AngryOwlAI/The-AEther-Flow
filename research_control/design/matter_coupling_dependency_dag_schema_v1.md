<!-- authority: control -->

# Matter-Coupling Dependency DAG Schema v1

## Purpose

This schema implements P4-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
It defines the machine-readable and human-readable contract for a future
matter-coupling dependency DAG.

The schema is a project-control artifact. It is not the populated DAG, not a
matter-coupling derivation, not a source-law adoption, not detector semantics,
not stress-energy semantics, not a matter action, not Einstein equations, not
benchmark promotion, and not a completed derivation.

Explicit boundary phrases for validators and future readers: not a matter-coupling derivation; not benchmark promotion.

P4-T02 may populate a DAG from tracked authority surfaces after this schema is
accepted by normal research-control validation. Until then, all node rows below
are schema templates and required minimum node classes only.

## Authority Boundary

The DAG is navigational control support only. Every populated node must point to
tracked authority: registered TeX, registered Markdown, registries, task
records, AgentJobs, completions, handoffs, approvals, or claim-boundary rows.
Generated wiki notes, local Obsidian notes, semantic extracts, SQLite memory,
PDFs, screenshots, validator output, commit status, and graph rendering are
supporting evidence only and cannot promote claims.

Any node that touches the matter sector must carry explicit forbidden-overread
guards. A populated DAG row may say that a target is blocked, human-gated,
draft/control, proposal-only, scoped evidence/precondition, adopted as a scoped
source object, or rejected. It must not silently convert one status into
another.

## Schema Shape

```yaml
schema_id: "matter_coupling_dependency_dag_v1"
authority_boundary:
  navigational_support_only: true
  physics_claim_authority: false
  proof_authority: false
  source_authority_required: true
  populated_dag_required_for_claim: false
sources: []
nodes: []
edges: []
warnings: []
```

Each `sources` item must include:

```yaml
path: ""
source_kind: ""
source_registry: ""
registry_object_id: ""
source_hash: ""
authority_status: ""
```

## Node Schema

Each node must use this shape:

```yaml
node_id: ""
label: ""
node_kind: ""
semantic_layer: ""
status: ""
authority_status: ""
source_path: ""
source_registry: ""
source_field: ""
evidence_basis: []
required_authority_before_promotion: []
forbidden_overread_guards: []
downstream_blocks: []
notes: ""
```

### Required Node Kinds

| Node kind | Use | Promotion rule |
| --- | --- | --- |
| `evidence_precondition` | Scoped evidence or prerequisite data that supports later work. | May not be rendered as an adopted object or physical target. |
| `adopted_object` | Object adopted only by explicit tracked authority and within that authority's scope. | Scope qualifiers and downstream blocks must remain visible. |
| `theorem` | Conditional theorem, theorem target, theorem candidate, or proved source-side theorem. | Must name hypotheses and cannot imply adoption unless the authority record says so. |
| `law` | Source law, target law, adoption-readiness law, or coupling law target. | Defaults to blocked or proposal-only unless an exact Gate Chair or human-gated authority adopts it. |
| `obstruction` | Named countermodel, missing-data branch, fail-closed branch, or underdetermination result. | May block adoption but does not prove global impossibility unless it is a scoped no-go theorem. |
| `physical_target` | Detector semantics, stress-energy semantics, stress-energy tensor, matter action, matter coupling, Einstein equations, or benchmark promotion. | Defaults to blocked until all prerequisites and protected authority are present. |

### Semantic Layers

The DAG must keep these layers separate:

| Layer | Meaning |
| --- | --- |
| `source_matter_semantics` | Source-side objects, certificates, equivalence classes, and theorem candidates. |
| `certificate_boundary` | `RR_E` transport, invariance, factorization, missing-certificate, and fail-closed certificate controls. |
| `detector_semantics` | Detector/readout semantics or an explicitly source-side replacement target. |
| `coupling_law` | Coupling-law target, candidate, adoption decision, or obstruction. |
| `stress_energy_action` | Stress-energy semantics, stress-energy tensor, matter action, or explicit alternative dynamics path. |
| `universal_matter_coupling` | Universal matter-coupling derivation or adoption target. |
| `einstein_equations` | Einstein-equation dependency target. |
| `benchmark_promotion` | Exact-GR benchmark promotion or completed-derivation gate. |

## Edge Schema

Each edge must use this shape:

```yaml
edge_id: ""
source_id: ""
target_id: ""
edge_kind: ""
source_path: ""
source_field: ""
summary: ""
forbidden_overread_guards: []
```

### Required Edge Kinds

| Edge kind | Meaning |
| --- | --- |
| `requires` | Target cannot be considered without the source node. |
| `supports_as_evidence` | Source node is evidence or precondition only. |
| `constructs` | Task or artifact constructs a draft/control object. |
| `proves_conditionally` | Theorem proves a statement only under named hypotheses. |
| `blocks` | Source node blocks or fails closed against the target. |
| `forbids_overread` | Source node explicitly prevents a stronger reading. |
| `requires_human_gate` | Target needs Gate Chair or human-gated authority. |
| `separates_layer` | Edge records that two semantic layers must not collapse. |
| `depends_on` | General non-promotional dependency relation. |

## Required Minimum Nodes

The populated P4-T02 DAG must include at least the following node templates.
Each template lists its required kind, layer, default status, and guards.

| Node ID | Label | Kind | Layer | Default status | Required guards |
| --- | --- | --- | --- | --- | --- |
| `mc_source_matter_semantics_objects` | source-side matter-semantics objects | `evidence_precondition` | `source_matter_semantics` | `draft_control_or_scoped_evidence_precondition` | no_matter_semantics_adoption; no_detector_semantics; no_coupling_law_adoption; no_matter_coupling_derivation; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_source_matter_semantics_equivalence_theorem` | source-side matter-semantics equivalence theorem | `theorem` | `source_matter_semantics` | `conditional_source_side_theorem_or_evidence_status_only` | no_source_law_adoption; no_unrestricted_RR_E_theorem; no_matter_semantics_adoption; no_detector_semantics; no_coupling_law_adoption; no_matter_coupling_derivation; no_benchmark_promotion; no_completed_derivation |
| `mc_rr_e_certificate_boundary` | `RR_E` certificate boundary | `evidence_precondition` | `certificate_boundary` | `certificate_indexed_guard_or_fail_closed` | no_RR_ETransportCompletenessOrInvarianceLaw_v1_adoption; no_unrestricted_RR_E_theorem; no_source_law_adoption; no_matter_coupling_derivation; no_detector_semantics; no_benchmark_promotion; no_completed_derivation |
| `mc_detector_semantics_target` | detector-semantics target | `physical_target` | `detector_semantics` | `blocked` | no_detector_semantics_adoption; no_matter_semantics_as_detector_semantics; no_matter_coupling_derivation; no_stress_energy_semantics; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_coupling_law_target` | coupling-law target | `law` | `coupling_law` | `blocked` | no_coupling_law_adoption; no_matter_coupling_derivation; no_matter_coupling_adoption; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_stress_energy_semantics_target` | stress-energy semantics target | `physical_target` | `stress_energy_action` | `blocked` | no_stress_energy_semantics; no_stress_energy_tensor; no_matter_action; no_coupling_law_adoption; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_stress_energy_tensor_target` | stress-energy tensor target | `physical_target` | `stress_energy_action` | `blocked` | no_stress_energy_tensor; no_stress_energy_semantics; no_matter_action; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_matter_action_target` | matter-action target | `physical_target` | `stress_energy_action` | `blocked` | no_matter_action; no_stress_energy_semantics; no_stress_energy_tensor; no_matter_coupling_derivation; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_universal_matter_coupling_derivation` | universal matter-coupling derivation | `physical_target` | `universal_matter_coupling` | `blocked` | no_coupling_law_adoption; no_matter_coupling_derivation; no_matter_coupling_adoption; no_stress_energy_semantics; no_matter_action; no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_einstein_equation_dependency` | Einstein-equation dependency | `physical_target` | `einstein_equations` | `blocked` | no_einstein_equations; no_benchmark_promotion; no_completed_derivation |
| `mc_benchmark_promotion_dependency` | benchmark promotion dependency | `physical_target` | `benchmark_promotion` | `blocked_or_human_gated` | no_benchmark_promotion; no_benchmark_gate_chair_closure; no_completed_derivation |

## Required Minimum Edges

P4-T02 must instantiate edges equivalent to:

| Source | Edge | Target | Required boundary |
| --- | --- | --- | --- |
| `mc_source_matter_semantics_objects` | `supports_as_evidence` | `mc_source_matter_semantics_equivalence_theorem` | evidence only; not adoption |
| `mc_rr_e_certificate_boundary` | `requires` | `mc_source_matter_semantics_equivalence_theorem` | certificate-indexed or fail-closed |
| `mc_source_matter_semantics_equivalence_theorem` | `supports_as_evidence` | `mc_coupling_law_target` | theorem status is not coupling-law adoption |
| `mc_detector_semantics_target` | `requires` | `mc_universal_matter_coupling_derivation` | detector layer remains distinct |
| `mc_coupling_law_target` | `requires` | `mc_universal_matter_coupling_derivation` | coupling law remains blocked unless adopted separately |
| `mc_stress_energy_semantics_target` | `requires` | `mc_stress_energy_tensor_target` | semantics and tensor construction remain distinct |
| `mc_stress_energy_tensor_target` | `requires` | `mc_matter_action_target` | tensor does not imply action without tracked authority |
| `mc_matter_action_target` | `requires` | `mc_einstein_equation_dependency` | action/dynamics path remains missing unless established separately |
| `mc_universal_matter_coupling_derivation` | `requires` | `mc_einstein_equation_dependency` | matter coupling is necessary but not sufficient for Einstein equations |
| `mc_einstein_equation_dependency` | `requires` | `mc_benchmark_promotion_dependency` | benchmark promotion remains protected and downstream |

## Status Vocabulary

Allowed status values:

- `adopted_scoped_source_object`
- `scoped_evidence_precondition`
- `draft_control`
- `proposal_only`
- `conditional_source_side_theorem`
- `certificate_indexed_guard_or_fail_closed`
- `blocked`
- `blocked_or_human_gated`
- `human_gated`
- `rejected`
- `frozen_negative`

Any new status value must be added by a later project-control schema update and
must preserve the same claim-boundary separation.

## Promotion Gate Requirements

A node may change from `blocked`, `proposal_only`, `draft_control`, or
`scoped_evidence_precondition` to an adopted or promoted status only when the
populated DAG cites exact tracked authority for that transition. The required
authority must name the object, version, source path, task, AgentJob,
completion, and Gate Chair or human-gated decision when applicable.

Human authorization to continue implementation-plan packets is sufficient to
run schema, audit, selector, or draft/control construction work. It is not by
itself source-law adoption, matter-semantics adoption, detector-semantics
adoption, coupling-law adoption, stress-energy adoption, matter-action
authority, Einstein-equation derivation, benchmark promotion, or completed
derivation.

## P4-T01 Completion Criteria

A P4-T01 completion may claim only that:

- the schema file exists;
- required node kinds distinguish evidence, adopted object, theorem, law,
  obstruction, and physical target;
- all minimum high-risk node templates are present;
- each high-risk node template has forbidden-overread guards; and
- P4-T02 may populate the DAG in a later bounded transaction.

It may not claim that the DAG has been populated or that any downstream
physics target is established.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling derivation
moratorium* [Internal control source].
`research_control/design/matter_coupling_derivation_moratorium.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling
pre-adoption checklist* [Internal control source].
`research_control/design/matter_coupling_pre_adoption_checklist.md`

The AEther-Flow Research Project. (2026, July 2). *Handoff 0518*
[Internal research-control handoff]. `research_control/handoffs/handoff-0518.yaml`
