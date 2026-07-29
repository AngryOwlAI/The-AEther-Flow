<!-- authority: science-draft -->

# P8-T01 gravitational-closure route-selection receipt

## Decision

P8-T01 selects
`conditional_source_to_local_effective_action_closure_v1`, labeled
`local-effective-action-closure`, for formalization in P8-T02.

Selection status is `selected_for_formalization_only`. No effective action,
geometry, metric, or field equation has been constructed.

## Why this route is selected

The selected route has the closest declared interface to the available
source-side record:

- P5 supplies controlled source-response structure but not an effective
  gravitational geometry.
- P6 supplies only `ScopedMetricStructureRecord_src` and a negative Gate B
  result; bare `g_eff` remains unresolved.
- P7 supplies a human-adopted finite source matter action, variation,
  source-side response precursor, and componentwise conservation within its
  exact source scope.

Those facts make an action-closure target the clearest next object to
formalize. They do not satisfy that target. The route still lacks a lawful
source-to-unscoped-geometry map, a source-to-effective-matter map, a local
measure and derivative expansion, a derived invariance principle or
replacement, physical scale and coarse-graining control, variational boundary
data, an effective conservation bridge, and a theorem deriving an
Einstein-leading regime.

## Compared and frozen alternatives

The comparison records four routes:

1. `conditional_source_to_local_effective_action_closure_v1` — selected for
   P8-T02 formalization.
2. `hypersurface_deformation_closure_v1` — frozen until a source-derived
   canonical phase space, bracket, constraints, and deformation algebra
   exist.
3. `gravitational_closure_from_matter_v1` — frozen until an effective matter
   response object, response-to-geometry map, and conservation/gauge
   consistency bridge exist.
4. `thermodynamic_gravity_closure_v1` — frozen until a source-derived causal
   boundary, temperature, entropy, heat-flow, equilibrium, and integrability
   dictionary exists.

Every freeze is local and reversible under its stated thaw criteria. No route
is rejected globally.

## P8-T02 theorem target

The next bounded packet must formalize
`LocalEffectiveActionClosureTarget_v1` through
`ontology-formalizer@0.2.0` on the
`ontology-law-research-packet` route. The trigger classification is
`derivation_critical_missing_source_law`.

The target must state exact types and failure branches for:

- source-to-effective carrier, geometry, and matter maps;
- locality, measure, derivative expansion, and controlled corrections;
- source-derived symmetry or an explicit replacement principle;
- scale, coarse-graining, and coupling data;
- variational boundary conditions and equivalence under boundary terms or
  field redefinitions;
- source-to-effective conservation; and
- the conditions under which an Einstein-leading term could be derived.

The Einstein-Hilbert action, Einstein equations, target metric, and exact-GR
benchmark success are forbidden as source premises.

## Distance-to-GR and authority boundary

This selector contributes a typed route-dependency comparison and a frozen
alternative ledger. It records no positive Distance-to-GR delta:
`einstein_equations` remains `not_started`.

It does not modify canonical ontology, adopt a source law, construct
`g_eff`, construct a local effective action or target
stress-energy tensor, establish or refute the equivalence principle, derive
Einstein equations, prove exact-GR recovery, promote the benchmark, state a
global no-go, publish, or push.

## Internal source basis

- `implementations_plans/recommendations_implementation_plan_continue_task-v21.md`
- `research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex`
- `research_control/tasks/RT-20260726-001/artifacts/p6_geometry_input_contract_v1.yaml`
- `research_control/tasks/RT-20260726-011/artifacts/metric_object_naming_decision_v1.yaml`
- `research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml`
- `research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml`
- `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex`
- `ontology/tex/aether_flow_dynamics.tex` and
  `ontology/tex/aether_flow_consistency.tex`, read only as benchmark-boundary
  sources and never as closure premises.
