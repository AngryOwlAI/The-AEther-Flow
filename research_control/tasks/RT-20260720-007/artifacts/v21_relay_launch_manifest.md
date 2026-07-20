<!-- authority: control -->

# V21 P0-T04 continue-research-goal v4 production launch manifest

## Status and boundary

This is the tracked, human-readable reconstruction of the accepted active v4
relay contract for goal `crg-20260720T161354Z-96bc2664ce31bfe0`. It is draft/control orchestration
evidence only. P0-T04 did not call `initialize`, reserve a successor, create a
Codex task, or create a second runtime goal. The currently observed goal-file
inventory is `goal-crg-20260716T053715Z-47e6f6f5298bb427.md`, `goal-crg-20260718T155942Z-87dad29edca8ed6f.md`, `goal-crg-20260718T201217Z-0d83f05b0d0bb601.md`, `goal-crg-20260719T040950Z-8d47c339cfe1c178.md`, `goal-crg-20260720T161354Z-96bc2664ce31bfe0.md` and was unchanged by generation.

A future operator may use this packet only after the live relay is terminal,
all current capability and repository checks pass, every mutable source hash is
recomputed, and the exact goal plus `reasoning_effort: "max"` receive combined
confirmation. It is never authority for a parallel duplicate relay.

## Exact launcher input

```yaml
goal: |-
  Implement every included work item in implementations_plans/recommendations_implementation_plan_continue_task-v21.md in the exact dependency order and authority boundaries recorded by that plan. Use the continue-research-goal v4 recursive relay, one bounded worker invocation and at most one bounded AgentJob per generation. Preserve all source authority, claim boundaries, human gates, validation and checkpoint requirements, no-progress and repeated-state stops, repository identity, and no-scope-expansion rules. Complete, precisely obstruct, freeze, defer at a human gate, supersede, or mark conditionally not required every included work item using canonical tracked evidence, then produce the final v21 recommendation coverage, gate-consistency, provenance, no-overclaim, and status synthesis.
reasoning_effort: "max"
scope:
  mode: "multi_step"
  included_work_items: "Use the exact JSON contract below; 122 items, 183 dependency edges."
  dependency_source:
    path: "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
    sha256: "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"
  exclusions: "Use the exact JSON contract below."
  source_hashes: "Use the exact JSON contract below."
  allow_scope_expansion: false
max_continue_passes: null
deadline_at: null
```

The launcher must restate the complete goal and the separate exact line
`reasoning_effort: "max"`, then obtain one combined unambiguous confirmation
before capability preflight or state creation.

## Exact scope-contract candidate

- Scope-contract SHA-256: `d42e4db415c846892a991594e21da5d58202460f07f3b0325f3c3b6fa9f24eae`
- Work-item count: 122
- Dependency-edge count: 183
- Dependency source: `implementations_plans/recommendations_implementation_plan_continue_task-v21.md`

```json
{
  "allow_scope_expansion": false,
  "dependency_source": {
    "path": "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "sha256": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"
  },
  "exclusions": [
    "No work item outside the 122 IDs in this plan.",
    "No canonical ontology edit without the exact human-gated work item and approval.",
    "No source-law, metric, matter-coupling, Einstein-equation, benchmark, or completed-derivation promotion by workflow status.",
    "No push, merge, rebase, pull request, external publication, reviewer contact, or public outreach without explicit authorization.",
    "No use of ignored goal files, local caches, generated views, validators, registries, role identity, or task status as scientific proof.",
    "No scope expansion, task repurposing, duplicate successor, concurrent relay, or rerun of a consumed generation.",
    "No private chain of thought, credentials, tokens, keys, or private prompts in tracked attempt or review records."
  ],
  "included_work_items": [
    {
      "depends_on": [],
      "objective": "Register this Markdown plan as the canonical draft/control dependency source for the v21 implementation program without changing scientific claim status.",
      "work_item_id": "P0-T01"
    },
    {
      "depends_on": [
        "P0-T01"
      ],
      "objective": "Create a machine-readable backlog that reproduces every phase, task, dependency, recommendation mapping, route class, gate, and stop condition in this plan.",
      "work_item_id": "P0-T02"
    },
    {
      "depends_on": [
        "P0-T02"
      ],
      "objective": "Capture a reproducible snapshot of the scientific frontier, task metrics, candidate families, active route, validators, repository identity, and relevant source hashes before implementation begins.",
      "work_item_id": "P0-T03"
    },
    {
      "depends_on": [
        "P0-T03"
      ],
      "objective": "Produce the exact human-readable launch packet for one immutable multi-step v21 relay, including exact goal text, reasoning effort, source hashes, included work items, exclusions, and completion contract.",
      "work_item_id": "P0-T04"
    },
    {
      "depends_on": [
        "P0-T04"
      ],
      "objective": "Perform an independent prelaunch audit of recommendation coverage, task dependencies, worker-skill boundaries, human gates, no-progress guards, and the exact relay manifest.",
      "work_item_id": "P0-T05"
    },
    {
      "depends_on": [
        "P0-T05"
      ],
      "objective": "Audit the exact EqSrcFlowGeneratedGradedOrbitRootLaw candidate for ordered-action provenance, positivity, component selection, grading, morphism and variation design, observer truncation, desired-relation circularity, and target or process imports.",
      "work_item_id": "P1-T01"
    },
    {
      "depends_on": [
        "P1-T01"
      ],
      "objective": "Group the recent response-token, orientation-line, root, partition, and grading candidates into stable families and record exact construction, audit, stress, repair, freeze, and supersession lineage.",
      "work_item_id": "P1-T02"
    },
    {
      "depends_on": [
        "P1-T02"
      ],
      "objective": "Determine whether the active and recent candidate cycles must be frozen at family level or whether one materially distinct theorem route remains.",
      "work_item_id": "P1-T03"
    },
    {
      "depends_on": [
        "P1-T03"
      ],
      "objective": "Write one proposal-neutral theorem target covering selectors of roots, lines, orientations, partitions, response tokens, normalizations, and analogous distinguished structures.",
      "work_item_id": "P1-T04"
    },
    {
      "depends_on": [
        "P1-T04"
      ],
      "objective": "Conduct a bounded primary-source review that identifies established theorems relevant to natural selectors and clearly separates literature results from new AEther-Flow claims.",
      "work_item_id": "P1-T05"
    },
    {
      "depends_on": [
        "P1-T05"
      ],
      "objective": "Construct the exact categorical or groupoid setting in which source-natural selectors and EqSrc invariants can be stated.",
      "work_item_id": "P2-T01"
    },
    {
      "depends_on": [
        "P2-T01"
      ],
      "objective": "Formalize deterministic source-natural selection as an equivariant or natural section and derive the necessary fixed-point condition.",
      "work_item_id": "P2-T02"
    },
    {
      "depends_on": [
        "P2-T02"
      ],
      "objective": "Complete a theorem-level proof that no deterministic source-natural selector exists without a fixed point and that naturality alone does not ensure uniqueness with multiple fixed points.",
      "work_item_id": "P2-T03"
    },
    {
      "depends_on": [
        "P2-T03"
      ],
      "objective": "Recast the response-tag, orientation-line, rooted-partition, and graded-orbit examples as explicit models or countermodels of the general theorem.",
      "work_item_id": "P2-T04"
    },
    {
      "depends_on": [
        "P2-T03"
      ],
      "objective": "Encode the finite-group or category-theoretic core of the selector obstruction in a proof assistant and export a reproducible proof receipt.",
      "work_item_id": "P2-T05"
    },
    {
      "depends_on": [
        "P2-T04",
        "P2-T05"
      ],
      "objective": "Perform a fresh Smuggling Auditor review of the general theorem, especially the definitions of source morphisms, automorphisms, and selection spaces.",
      "work_item_id": "P2-T06"
    },
    {
      "depends_on": [
        "P2-T06"
      ],
      "objective": "Stress the unchanged audited theorem under nonfaithful actions, partial morphisms, multiple components, stochastic selectors, added marks, and altered variation classes.",
      "work_item_id": "P2-T07"
    },
    {
      "depends_on": [
        "P2-T07"
      ],
      "objective": "Submit the theorem, assumptions, proof, formalization, and countermodels to a blind internal reviewer and an epistemically independent reviewer before project adoption.",
      "work_item_id": "P2-T08"
    },
    {
      "depends_on": [
        "P2-T08"
      ],
      "objective": "Create a normalized decision taxonomy for added source structure, representative irrelevance, dynamical symmetry breaking, probabilistic selection, and scoped obstruction.",
      "work_item_id": "P3-T01"
    },
    {
      "depends_on": [
        "P3-T01"
      ],
      "objective": "Order candidate additions such as roots, orientations, gradings, measures, states, boundary data, and dynamics by assumption strength and symmetry reduction.",
      "work_item_id": "P3-T02"
    },
    {
      "depends_on": [
        "P3-T01",
        "P3-T02"
      ],
      "objective": "Determine whether orientation, root, line, partition, or representative choices can be quotiented away because all admissible choices yield identical source observables.",
      "work_item_id": "P3-T03"
    },
    {
      "depends_on": [
        "P3-T02"
      ],
      "objective": "Define the exact additional structures required for source-defined probability measures or dynamical sector selection and test whether they provide lawful alternatives to deterministic selection.",
      "work_item_id": "P3-T04"
    },
    {
      "depends_on": [
        "P3-T03",
        "P3-T04"
      ],
      "objective": "Construct a candidate EqSrc relation using source invariants, groupoid orbits, or an invariant functor, with reflexivity, symmetry, transitivity, and compatibility with composition and variation.",
      "work_item_id": "P3-T05"
    },
    {
      "depends_on": [
        "P3-T05"
      ],
      "objective": "Perform source-provenance audit and bounded refuter stress of the unchanged quotient-based EqSrc candidate.",
      "work_item_id": "P3-T06"
    },
    {
      "depends_on": [
        "P3-T06"
      ],
      "objective": "Record which historical candidate families are subsumed, frozen, or still open after the selector theorem and quotient EqSrc work.",
      "work_item_id": "P3-T07"
    },
    {
      "depends_on": [
        "P3-T07"
      ],
      "objective": "Record the status and provenance of dimension, differentiability, topology, order, orientation, time direction, metric form, signature, scale, coupling, matter, covariance, and dynamics across every frontier object.",
      "work_item_id": "P4-T01"
    },
    {
      "depends_on": [
        "P4-T01"
      ],
      "objective": "Specify the strongest honest continuum-first theory in which a four-dimensional differentiable substrate is primitive and only metric, matter, and dynamics remain derivational targets.",
      "work_item_id": "P4-T02"
    },
    {
      "depends_on": [
        "P4-T01"
      ],
      "objective": "Specify a genuinely weaker source ontology based on order, process, category, algebra, or discrete dynamics from which dimension and continuum structure would have to be reconstructed.",
      "work_item_id": "P4-T03"
    },
    {
      "depends_on": [
        "P4-T02",
        "P4-T03"
      ],
      "objective": "Perform a bounded comparative analysis of the continuum-first and emergence-first options using assumption economy, tractability, explanatory power, known literature, and downstream compatibility.",
      "work_item_id": "P4-T04"
    },
    {
      "depends_on": [
        "P4-T04"
      ],
      "objective": "Under explicit protected human authority, select continuum-first, emergence-first, or a precisely stated rejection or redesign route and define the canonical ontology-edit boundary.",
      "work_item_id": "P4-T05"
    },
    {
      "depends_on": [
        "P4-T05"
      ],
      "objective": "Apply the protected decision to canonical ontology sources, public claim vocabulary, burden definitions, and task routing without broadening its authority.",
      "work_item_id": "P4-T06"
    },
    {
      "depends_on": [
        "P4-T06"
      ],
      "objective": "Define the selected ontology's source state space, gauge or symmetry structure, observables, admissible variations, dynamics slot, and reconstruction slot in one compact formal object.",
      "work_item_id": "P5-T01"
    },
    {
      "depends_on": [
        "P5-T01"
      ],
      "objective": "Determine whether Phi_lambda is a group, semigroup, category action, gauge flow, physical evolution, stochastic process, or emergent ordering relation, and prove the basic laws appropriate to that choice.",
      "work_item_id": "P5-T02"
    },
    {
      "depends_on": [
        "P5-T02"
      ],
      "objective": "Build one bounded source action, Hamiltonian, local update law, or source-history measure consistent with the selected ontology and Phi_lambda semantics.",
      "work_item_id": "P5-T03"
    },
    {
      "depends_on": [
        "P5-T03"
      ],
      "objective": "Analyze the unchanged source-dynamics candidate for local composition, constraints, conserved quantities, gauge generators, or probabilistic normalization.",
      "work_item_id": "P5-T04"
    },
    {
      "depends_on": [
        "P5-T04"
      ],
      "objective": "Find source backgrounds or phases suitable for continuum reconstruction and determine linearized modes, stability conditions, and symmetry-breaking structure.",
      "work_item_id": "P5-T05"
    },
    {
      "depends_on": [
        "P5-T05"
      ],
      "objective": "Construct a controlled map from microscopic or source states to effective fields, observables, or geometry with declared scale, approximation, and error.",
      "work_item_id": "P5-T06"
    },
    {
      "depends_on": [
        "P5-T06"
      ],
      "objective": "Perform fresh source-provenance audit and adversarial stress of the unchanged source-theory, dynamics, backgrounds, and reconstruction map.",
      "work_item_id": "P5-T07"
    },
    {
      "depends_on": [
        "P5-T07"
      ],
      "objective": "Produce the canonical source-dynamics manuscript or a definitive scoped obstruction manuscript and update the theorem inventory and next route.",
      "work_item_id": "P5-T08"
    },
    {
      "depends_on": [
        "P5-T08"
      ],
      "objective": "Define the exact causal, influence, or characteristic structure to be derived from source dynamics before any full metric claim.",
      "work_item_id": "P6-T01"
    },
    {
      "depends_on": [
        "P6-T01"
      ],
      "objective": "Use the source dynamics and reconstruction map to derive one characteristic relation, principal polynomial, or causal order, or return a precise obstruction.",
      "work_item_id": "P6-T02"
    },
    {
      "depends_on": [
        "P6-T02"
      ],
      "objective": "Determine whether the derived causal structure fixes an effective conformal class under declared regularity and causality assumptions.",
      "work_item_id": "P6-T03"
    },
    {
      "depends_on": [
        "P6-T03"
      ],
      "objective": "Construct source-defined operational or measure structures that fix the conformal scale and measured durations and lengths.",
      "work_item_id": "P6-T04"
    },
    {
      "depends_on": [
        "P6-T04"
      ],
      "objective": "Show that the reconstructed geometric object is nondegenerate, has Lorentzian signature, and transforms consistently under source-induced coordinate or frame changes.",
      "work_item_id": "P6-T05"
    },
    {
      "depends_on": [
        "P6-T05"
      ],
      "objective": "Determine whether the effective geometry is unique up to declared gauge, natural under source morphisms, robust under admissible variations, and physically tied to propagation and clocks.",
      "work_item_id": "P6-T06"
    },
    {
      "depends_on": [
        "P6-T06"
      ],
      "objective": "Align object names and status with what has actually been proved, replacing overread-prone g_eff language unless Gate B is fully satisfied.",
      "work_item_id": "P6-T07"
    },
    {
      "depends_on": [
        "P6-T07"
      ],
      "objective": "Review the full causal, conformal, scale, signature, covariance, and operational package and integrate it into the frontier or record the exact remaining burden.",
      "work_item_id": "P6-T08"
    },
    {
      "depends_on": [
        "P6-T08"
      ],
      "objective": "Specify explicit source-level matter degrees of freedom, sectors, excitations, defects, representations, currents, or operational observables compatible with the selected ontology.",
      "work_item_id": "P7-T01"
    },
    {
      "depends_on": [
        "P7-T01"
      ],
      "objective": "Build one explicit source matter action, evolution equation, or transition law and derive its basic conserved or constraint structure.",
      "work_item_id": "P7-T02"
    },
    {
      "depends_on": [
        "P7-T02"
      ],
      "objective": "Construct source-level operational devices and protocols whose effective behavior can test geometry and coupling universality.",
      "work_item_id": "P7-T03"
    },
    {
      "depends_on": [
        "P7-T02",
        "P7-T03"
      ],
      "objective": "Compute the principal symbols or source propagation relations of the matter sectors and determine whether they share one effective cone or metric structure.",
      "work_item_id": "P7-T04"
    },
    {
      "depends_on": [
        "P7-T04"
      ],
      "objective": "Derive a source-to-effective coupling map that applies to all admitted matter sectors and preserves the common geometry without target import.",
      "work_item_id": "P7-T05"
    },
    {
      "depends_on": [
        "P7-T05"
      ],
      "objective": "Construct the effective matter action and derive the stress-energy tensor or source-equivalent variational object and its conservation conditions.",
      "work_item_id": "P7-T06"
    },
    {
      "depends_on": [
        "P7-T06"
      ],
      "objective": "Perform source-provenance audit and adversarial stress across matter ontology, operational devices, common cones, coupling law, action, stress-energy, and conservation.",
      "work_item_id": "P7-T07"
    },
    {
      "depends_on": [
        "P7-T07"
      ],
      "objective": "Under explicit protected authority, decide whether the audited and stressed package may be adopted in its exact scope as matter coupling, detector semantics, matter action, and stress-energy input.",
      "work_item_id": "P7-T08"
    },
    {
      "depends_on": [
        "P7-T08"
      ],
      "objective": "Choose one explicit route from matter and effective geometry to gravitational dynamics, with exact hypotheses and decision consequences.",
      "work_item_id": "P8-T01"
    },
    {
      "depends_on": [
        "P8-T01"
      ],
      "objective": "State the exact theorem or derivation target connecting source-derived matter and geometry to an effective gravitational action or constraint algebra.",
      "work_item_id": "P8-T02"
    },
    {
      "depends_on": [
        "P8-T02"
      ],
      "objective": "Execute the chosen closure calculation and derive an effective gravitational action, Hamiltonian constraints, or equivalent dynamics from the admitted source and matter inputs.",
      "work_item_id": "P8-T03"
    },
    {
      "depends_on": [
        "P8-T03"
      ],
      "objective": "Vary or otherwise evolve the derived gravitational candidate to obtain field equations and verify compatibility with matter conservation.",
      "work_item_id": "P8-T04"
    },
    {
      "depends_on": [
        "P8-T04"
      ],
      "objective": "Determine physical degrees of freedom, gauge modes, constraints, characteristic speeds, ghosts, tachyons, gradient instabilities, and strong-coupling regions.",
      "work_item_id": "P8-T05"
    },
    {
      "depends_on": [
        "P8-T05"
      ],
      "objective": "Review the unchanged action, field-equation, correction, and stability package for target import, hidden assumptions, algebraic errors, and interpretation overread.",
      "work_item_id": "P8-T06"
    },
    {
      "depends_on": [
        "P8-T06"
      ],
      "objective": "Under explicit protected authority, decide whether the audited and independently reviewed package establishes Einstein equations in an exact or controlled effective regime.",
      "work_item_id": "P8-T07"
    },
    {
      "depends_on": [
        "P8-T07"
      ],
      "objective": "Specify benchmark cases, source-only inputs, intermediate objects, allowed approximations, forbidden target premises, output comparisons, and independent reproduction requirements.",
      "work_item_id": "P9-T01"
    },
    {
      "depends_on": [
        "P9-T01"
      ],
      "objective": "Construct or derive a source state whose effective geometry, matter vacuum, and perturbative behavior recover the Minkowski benchmark within declared scope.",
      "work_item_id": "P9-T02"
    },
    {
      "depends_on": [
        "P9-T02"
      ],
      "objective": "Derive weak-field potentials, free-fall acceleration, redshift, and clock-rate relations from source dynamics and operational devices.",
      "work_item_id": "P9-T03"
    },
    {
      "depends_on": [
        "P9-T03"
      ],
      "objective": "Test causal propagation, local Lorentz behavior, equivalence-principle observables, and common free-fall structure across matter sectors.",
      "work_item_id": "P9-T04"
    },
    {
      "depends_on": [
        "P9-T04"
      ],
      "objective": "Derive a homogeneous and isotropic effective cosmology, expansion law, matter evolution, and controlled dark-energy or cosmological-constant status from source inputs.",
      "work_item_id": "P9-T05"
    },
    {
      "depends_on": [
        "P9-T05"
      ],
      "objective": "Derive the radiative sector, polarizations, speed, damping, dispersion, and coupling to detectors from the source-derived field equations.",
      "work_item_id": "P9-T06"
    },
    {
      "depends_on": [
        "P9-T06"
      ],
      "objective": "Test nonlinear consistency through conservation, constraint propagation, and one nontrivial compact-source or strong-field solution.",
      "work_item_id": "P9-T07"
    },
    {
      "depends_on": [
        "P9-T07"
      ],
      "objective": "Audit all benchmark cases for target import, tuning, inconsistent assumptions, shared-code errors, and scope overread, then seek independent reproduction.",
      "work_item_id": "P9-T08"
    },
    {
      "depends_on": [
        "P9-T08"
      ],
      "objective": "Under explicit protected authority, decide benchmark promotion, exact or approximate GR recovery, and whether the project may claim a completed derivation.",
      "work_item_id": "P9-T09"
    },
    {
      "depends_on": [
        "P0-T05"
      ],
      "objective": "Create machine-readable schemas for assumption provenance and multidimensional scientific status, preserving historical vocabulary through mapped compatibility fields.",
      "work_item_id": "P10-T01"
    },
    {
      "depends_on": [
        "P10-T01"
      ],
      "objective": "Replace free-form task-type analytics with stable work_kind, milestone, candidate_family, result_kind, authority, and scope fields while preserving human-readable titles.",
      "work_item_id": "P10-T02"
    },
    {
      "depends_on": [
        "P10-T01",
        "P10-T02"
      ],
      "objective": "Implement candidate IDs, family IDs, statement hashes, assumption hashes, ontology hashes, stage transitions, and supersession edges.",
      "work_item_id": "P10-T03"
    },
    {
      "depends_on": [
        "P10-T02",
        "P10-T03"
      ],
      "objective": "Record initial failures, auditor findings, validator failures, repairs, abandoned attempts, supersessions, compute metadata, and final dispositions without replacing canonical scientific artifacts.",
      "work_item_id": "P10-T04"
    },
    {
      "depends_on": [
        "P10-T03",
        "P10-T04"
      ],
      "objective": "Specify an append-only canonical data model for task, decision, candidate, claim, validation, authority, and handoff events, with CSV and Markdown as generated views.",
      "work_item_id": "P10-T05"
    },
    {
      "depends_on": [
        "P10-T05"
      ],
      "objective": "Build a bounded pilot that ingests selected control events and regenerates equivalent registry and Markdown views without becoming authoritative.",
      "work_item_id": "P10-T06"
    },
    {
      "depends_on": [
        "P10-T05"
      ],
      "objective": "Design and implement short stable artifact paths, metadata titles, path-length linting, and content-addressed references for new artifacts while preserving historical paths.",
      "work_item_id": "P10-T07"
    },
    {
      "depends_on": [
        "P10-T05",
        "P10-T06"
      ],
      "objective": "Refactor the burden map so stable definitions and dependencies remain authored while current statuses and next actions are generated from authoritative state.",
      "work_item_id": "P10-T08"
    },
    {
      "depends_on": [
        "P10-T07",
        "P10-T08"
      ],
      "objective": "Perform a non-promotional systems audit of normalized schemas, lineage, attempt history, event-store pilot, path policy, and generated burden status.",
      "work_item_id": "P10-T09"
    },
    {
      "depends_on": [
        "P0-T05",
        "P10-T01"
      ],
      "objective": "Create a review protocol that strips task verdict, route history, validator status, and internal confidence from the theorem or candidate packet.",
      "work_item_id": "P11-T01"
    },
    {
      "depends_on": [
        "P11-T01"
      ],
      "objective": "Create normalized classifications for same-context role review, blind same-model review, different-model review, human expert review, and independent replication.",
      "work_item_id": "P11-T02"
    },
    {
      "depends_on": [
        "P2-T05",
        "P10-T01"
      ],
      "objective": "Define how theorem sources, proof objects, trusted foundations, builds, and hashes are registered without promoting physical interpretations.",
      "work_item_id": "P11-T03"
    },
    {
      "depends_on": [
        "P11-T01",
        "P11-T02"
      ],
      "objective": "Extend target-import checking beyond field-name fragments to aliases, split encodings, equivalent forms, misleading certificates, and prompt-level interpretations.",
      "work_item_id": "P11-T04"
    },
    {
      "depends_on": [
        "P10-T01",
        "P11-T04"
      ],
      "objective": "Require source derivation, uniqueness or quotient status, dynamics, operational interpretation, and robustness in addition to no-target purity before physical promotion.",
      "work_item_id": "P11-T05"
    },
    {
      "depends_on": [
        "P11-T02",
        "P11-T05"
      ],
      "objective": "Measure reviewer findings at theorem validity, assumptions, countermodels, physical interpretation, and claim scope, without treating consensus as proof.",
      "work_item_id": "P11-T06"
    },
    {
      "depends_on": [
        "P11-T03",
        "P11-T04",
        "P11-T05",
        "P11-T06"
      ],
      "objective": "Exercise blind packets, independence classification, proof evidence, semantic smuggling, and positive-provenance gates on real frontier objects.",
      "work_item_id": "P11-T07"
    },
    {
      "depends_on": [
        "P11-T07"
      ],
      "objective": "Verify that blind review, diversity labels, proof evidence, semantic fixtures, and positive-provenance gates preserve source authority and do not create new promotion shortcuts.",
      "work_item_id": "P11-T08"
    },
    {
      "depends_on": [
        "P10-T01",
        "P10-T02"
      ],
      "objective": "Require every new physics task to name a materially new theorem, proof step, countermodel, source law, external result, independent replication, or justified ledger delta.",
      "work_item_id": "P12-T01"
    },
    {
      "depends_on": [
        "P10-T03",
        "P12-T01"
      ],
      "objective": "Create machine-readable rules that freeze repeated candidate families and require a new primitive, theorem, variation class, or protected decision for reopening.",
      "work_item_id": "P12-T02"
    },
    {
      "depends_on": [
        "P10-T02",
        "P12-T01"
      ],
      "objective": "Create separate planning, reporting, and acceptance budgets for science-bearing work and project-system work.",
      "work_item_id": "P12-T03"
    },
    {
      "depends_on": [
        "P12-T03"
      ],
      "objective": "Require a physics-bearing ordinary task after three consecutive project-system tasks unless tracked evidence shows all science work is blocked by a control failure.",
      "work_item_id": "P12-T04"
    },
    {
      "depends_on": [
        "P10-T03",
        "P10-T04",
        "P11-T06",
        "P12-T03"
      ],
      "objective": "Measure assumption reduction, theorem generality, obstruction unification, independent survival, benchmark breadth, retraction, and ledger durability.",
      "work_item_id": "P12-T05"
    },
    {
      "depends_on": [
        "P10-T04",
        "P12-T05"
      ],
      "objective": "Render attempt history, repair rate, validation catches, audit objections, abandonment, and final dispositions without exposing secrets or treating failures as physics refutations.",
      "work_item_id": "P12-T06"
    },
    {
      "depends_on": [
        "P12-T02",
        "P12-T04",
        "P12-T06",
        "P11-T08"
      ],
      "objective": "Run ablations and route-history analyses to test whether payload gates, family freezes, dual budgets, reviewer diversity, and quality metrics improve research decisions.",
      "work_item_id": "P12-T07"
    },
    {
      "depends_on": [
        "P0-T05"
      ],
      "objective": "Compare legacy and planner validation on a fixed representative corpus and authorize cutover only after zero unexplained hard mismatches.",
      "work_item_id": "P13-T01"
    },
    {
      "depends_on": [
        "P13-T01"
      ],
      "objective": "Make the validated planner the single orchestration owner and retain scheduled full validation and rollback controls.",
      "work_item_id": "P13-T02"
    },
    {
      "depends_on": [
        "P0-T05"
      ],
      "objective": "Create one reproducible packaging and dependency contract for scripts, tests, validators, and proof tools.",
      "work_item_id": "P13-T03"
    },
    {
      "depends_on": [
        "P13-T03",
        "P10-T07"
      ],
      "objective": "Introduce ruff, mypy or pyright, Python and OS matrices, path-length linting, and a documented programmatic validator API.",
      "work_item_id": "P13-T04"
    },
    {
      "depends_on": [
        "P13-T03",
        "P13-T04",
        "P11-T04"
      ],
      "objective": "Measure test coverage and strengthen critical invariants with property-based tests, mutation tests, dependency scanning, and code security analysis.",
      "work_item_id": "P13-T05"
    },
    {
      "depends_on": [
        "P13-T03",
        "P13-T04"
      ],
      "objective": "Create a devcontainer, container, Nix flake, or equivalent fresh-machine environment for research-control, proof, and benchmark workflows.",
      "work_item_id": "P13-T06"
    },
    {
      "depends_on": [
        "P10-T08",
        "P13-T02"
      ],
      "objective": "Add source commit, hashes, task count, generation time, and maximum-lag policy to authoritative-facing generated reports and fail CI on stale views.",
      "work_item_id": "P13-T07"
    },
    {
      "depends_on": [
        "P13-T05",
        "P13-T06",
        "P13-T07"
      ],
      "objective": "Calibrate checker names and documentation, then run full software, CI, environment, freshness, security, and historical-compatibility validation.",
      "work_item_id": "P13-T08"
    },
    {
      "depends_on": [
        "P0-T05",
        "P10-T01"
      ],
      "objective": "Create canonical claim definitions for interpretive redescription, formal or categorical equivalence, genuine emergence, and empirical novelty.",
      "work_item_id": "P14-T01"
    },
    {
      "depends_on": [
        "P14-T01"
      ],
      "objective": "Specify assumption compression, unification, inevitability, explanatory depth, dimension or signature explanation, matter or quantum connection, and problem-solving fertility as explicit evaluative criteria.",
      "work_item_id": "P14-T02"
    },
    {
      "depends_on": [
        "P11-T05",
        "P14-T01"
      ],
      "objective": "Integrate the principle that source purity must be supplemented by positive provenance, dynamics, uniqueness or quotient status, operational meaning, and robustness.",
      "work_item_id": "P14-T03"
    },
    {
      "depends_on": [
        "P4-T05",
        "P5-T08",
        "P14-T03"
      ],
      "objective": "Under protected authority, decide whether the congruence is interpretive, gauge or representative structure, dynamically selected state, or an independent dynamical field.",
      "work_item_id": "P14-T04"
    },
    {
      "depends_on": [
        "P2-T08",
        "P3-T07",
        "P14-T03"
      ],
      "objective": "Define when a no-go theorem, obstruction, or minimum-extension theorem counts as a completed scientific result and how it affects route closure.",
      "work_item_id": "P14-T05"
    },
    {
      "depends_on": [
        "P14-T02",
        "P14-T03",
        "P14-T04",
        "P14-T05"
      ],
      "objective": "Update source-backed public documentation specifications so ontology, exact closure, formal equivalence, emergence, operational meaning, and empirical novelty are visibly distinct.",
      "work_item_id": "P14-T06"
    },
    {
      "depends_on": [
        "P14-T01",
        "P14-T02",
        "P14-T03"
      ],
      "objective": "Develop a publication-ready manuscript that clearly states exact operational identity with GR, the interpretive role of the ontology, and the absence of a completed substrate derivation or independent low-energy prediction.",
      "work_item_id": "P15-T01"
    },
    {
      "depends_on": [
        "P12-T07",
        "P13-T08"
      ],
      "objective": "Evaluate and document the role architecture, claim gates, negative-result memory, candidate cycles, lineage, attempt history, and v21 governance reforms with controlled baselines and ablations.",
      "work_item_id": "P15-T02"
    },
    {
      "depends_on": [
        "P2-T08",
        "P3-T07",
        "P14-T05"
      ],
      "objective": "Develop the general selector theorem, finite examples, extension lattice, quotient EqSrc implications, and foundations interpretation into a focused mathematics or philosophy-of-physics manuscript.",
      "work_item_id": "P15-T03"
    },
    {
      "depends_on": [
        "P6-T08"
      ],
      "objective": "Package P5 and P6 results or obstructions as a durable technical report with explicit ontology regime, source dynamics, reconstruction map, causal structure, and geometry status.",
      "work_item_id": "P15-T04"
    },
    {
      "depends_on": [
        "P9-T09"
      ],
      "objective": "If and only if Gate E authorizes it, assemble a derivation manuscript covering source ontology, dynamics, geometry, matter, closure, benchmarks, corrections, assumptions, and independent review.",
      "work_item_id": "P15-T05"
    },
    {
      "depends_on": [
        "P15-T01",
        "P15-T02",
        "P15-T03",
        "P15-T04"
      ],
      "objective": "Create stable, source-backed packages for manuscripts, proofs, benchmark cases, code, environments, assumption ledgers, and claim maps.",
      "work_item_id": "P15-T06"
    },
    {
      "depends_on": [
        "P15-T06"
      ],
      "objective": "Obtain explicit human approval for each manuscript submission, public release, external reviewer contact, or outreach action.",
      "work_item_id": "P15-T07"
    },
    {
      "depends_on": [
        "P9-T09",
        "P10-T09",
        "P11-T08",
        "P12-T07",
        "P13-T08",
        "P14-T06",
        "P15-T07"
      ],
      "objective": "Verify that every V21-R01 through V21-R72 recommendation has direct implementation evidence, validation evidence, and an explicit final status.",
      "work_item_id": "P16-T01"
    },
    {
      "depends_on": [
        "P16-T01"
      ],
      "objective": "Verify that source theory, effective geometry, matter coupling, field equations, and completed-derivation decisions follow the declared dependency chain and protected authorities.",
      "work_item_id": "P16-T02"
    },
    {
      "depends_on": [
        "P16-T01",
        "P10-T09",
        "P13-T08",
        "P15-T06"
      ],
      "objective": "Verify all source paths, candidate identities, event chains, generated-view freshness, proof objects, benchmark receipts, and publication packages.",
      "work_item_id": "P16-T03"
    },
    {
      "depends_on": [
        "P16-T02",
        "P16-T03"
      ],
      "objective": "Attack the final project state for hidden target imports, source-purity overread, internal review mislabeled as external, methodology-as-physics claims, and premature derivation language.",
      "work_item_id": "P16-T04"
    },
    {
      "depends_on": [
        "P16-T04"
      ],
      "objective": "Produce an answer-first synthesis of what was proved, adopted, obstructed, improved, human-gated, or left open across science and the research operating system.",
      "work_item_id": "P16-T05"
    },
    {
      "depends_on": [
        "P16-T05"
      ],
      "objective": "Use canonical evidence to mark the multi-step goal complete, continue with an exact repair, or terminalize with a precise human action when protected gates remain.",
      "work_item_id": "P16-T06"
    }
  ],
  "mode": "multi_step",
  "source_hashes": {
    ".codex/skills/continue-research-continue-goal/SKILL.md": "1c104985bb950cd1e1fe646f69dffce53d466a49b34f228c24f55efb58d0ac54",
    ".codex/skills/continue-research-goal/SKILL.md": "12e52f1cf5ef819814424b0b5811dc9ceba13c3bd2dd59e99569141a2ed89481",
    ".codex/skills/continue-research-goal/references/goal-file-schema.md": "35b1477ee973f268a7d2e7947a75b247a8294cbf6c4843f031f9f686e1c47018",
    ".codex/skills/continue-research/SKILL.md": "4ff16918097dd940bfed731f921acbe496b3e5a1d14f43a0fd352e74b7b0173f",
    "AGENTS.md": "0b6270b8eee144d65d6959c822a9bd6b5ba295bbe58d11833cbb44fbd211330f",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "research_control/AGENTS.md": "c93e14bb2cc6e7bbc5c299085f8843ca84d714cdaef99b2b78a46715b5b310ae",
    "research_control/handoffs/handoff-0772.yaml": "31374c85ee49e457a8b25eaf6d729a0d0e286f1dd53eac184a502044fdd8de0a",
    "research_control/program_state.yaml": "f0ba4ffcfed230f370fbb902f5bb8b32e3ec3f4a0c98163cdf810b585f8eb4c7"
  }
}
```

## Included work items

| Work item | Dependencies | Objective |
| --- | --- | --- |
| `P0-T01` | none | Register this Markdown plan as the canonical draft/control dependency source for the v21 implementation program without changing scientific claim status. |
| `P0-T02` | `P0-T01` | Create a machine-readable backlog that reproduces every phase, task, dependency, recommendation mapping, route class, gate, and stop condition in this plan. |
| `P0-T03` | `P0-T02` | Capture a reproducible snapshot of the scientific frontier, task metrics, candidate families, active route, validators, repository identity, and relevant source hashes before implementation begins. |
| `P0-T04` | `P0-T03` | Produce the exact human-readable launch packet for one immutable multi-step v21 relay, including exact goal text, reasoning effort, source hashes, included work items, exclusions, and completion contract. |
| `P0-T05` | `P0-T04` | Perform an independent prelaunch audit of recommendation coverage, task dependencies, worker-skill boundaries, human gates, no-progress guards, and the exact relay manifest. |
| `P1-T01` | `P0-T05` | Audit the exact EqSrcFlowGeneratedGradedOrbitRootLaw candidate for ordered-action provenance, positivity, component selection, grading, morphism and variation design, observer truncation, desired-relation circularity, and target or process imports. |
| `P1-T02` | `P1-T01` | Group the recent response-token, orientation-line, root, partition, and grading candidates into stable families and record exact construction, audit, stress, repair, freeze, and supersession lineage. |
| `P1-T03` | `P1-T02` | Determine whether the active and recent candidate cycles must be frozen at family level or whether one materially distinct theorem route remains. |
| `P1-T04` | `P1-T03` | Write one proposal-neutral theorem target covering selectors of roots, lines, orientations, partitions, response tokens, normalizations, and analogous distinguished structures. |
| `P1-T05` | `P1-T04` | Conduct a bounded primary-source review that identifies established theorems relevant to natural selectors and clearly separates literature results from new AEther-Flow claims. |
| `P2-T01` | `P1-T05` | Construct the exact categorical or groupoid setting in which source-natural selectors and EqSrc invariants can be stated. |
| `P2-T02` | `P2-T01` | Formalize deterministic source-natural selection as an equivariant or natural section and derive the necessary fixed-point condition. |
| `P2-T03` | `P2-T02` | Complete a theorem-level proof that no deterministic source-natural selector exists without a fixed point and that naturality alone does not ensure uniqueness with multiple fixed points. |
| `P2-T04` | `P2-T03` | Recast the response-tag, orientation-line, rooted-partition, and graded-orbit examples as explicit models or countermodels of the general theorem. |
| `P2-T05` | `P2-T03` | Encode the finite-group or category-theoretic core of the selector obstruction in a proof assistant and export a reproducible proof receipt. |
| `P2-T06` | `P2-T04`, `P2-T05` | Perform a fresh Smuggling Auditor review of the general theorem, especially the definitions of source morphisms, automorphisms, and selection spaces. |
| `P2-T07` | `P2-T06` | Stress the unchanged audited theorem under nonfaithful actions, partial morphisms, multiple components, stochastic selectors, added marks, and altered variation classes. |
| `P2-T08` | `P2-T07` | Submit the theorem, assumptions, proof, formalization, and countermodels to a blind internal reviewer and an epistemically independent reviewer before project adoption. |
| `P3-T01` | `P2-T08` | Create a normalized decision taxonomy for added source structure, representative irrelevance, dynamical symmetry breaking, probabilistic selection, and scoped obstruction. |
| `P3-T02` | `P3-T01` | Order candidate additions such as roots, orientations, gradings, measures, states, boundary data, and dynamics by assumption strength and symmetry reduction. |
| `P3-T03` | `P3-T01`, `P3-T02` | Determine whether orientation, root, line, partition, or representative choices can be quotiented away because all admissible choices yield identical source observables. |
| `P3-T04` | `P3-T02` | Define the exact additional structures required for source-defined probability measures or dynamical sector selection and test whether they provide lawful alternatives to deterministic selection. |
| `P3-T05` | `P3-T03`, `P3-T04` | Construct a candidate EqSrc relation using source invariants, groupoid orbits, or an invariant functor, with reflexivity, symmetry, transitivity, and compatibility with composition and variation. |
| `P3-T06` | `P3-T05` | Perform source-provenance audit and bounded refuter stress of the unchanged quotient-based EqSrc candidate. |
| `P3-T07` | `P3-T06` | Record which historical candidate families are subsumed, frozen, or still open after the selector theorem and quotient EqSrc work. |
| `P4-T01` | `P3-T07` | Record the status and provenance of dimension, differentiability, topology, order, orientation, time direction, metric form, signature, scale, coupling, matter, covariance, and dynamics across every frontier object. |
| `P4-T02` | `P4-T01` | Specify the strongest honest continuum-first theory in which a four-dimensional differentiable substrate is primitive and only metric, matter, and dynamics remain derivational targets. |
| `P4-T03` | `P4-T01` | Specify a genuinely weaker source ontology based on order, process, category, algebra, or discrete dynamics from which dimension and continuum structure would have to be reconstructed. |
| `P4-T04` | `P4-T02`, `P4-T03` | Perform a bounded comparative analysis of the continuum-first and emergence-first options using assumption economy, tractability, explanatory power, known literature, and downstream compatibility. |
| `P4-T05` | `P4-T04` | Under explicit protected human authority, select continuum-first, emergence-first, or a precisely stated rejection or redesign route and define the canonical ontology-edit boundary. |
| `P4-T06` | `P4-T05` | Apply the protected decision to canonical ontology sources, public claim vocabulary, burden definitions, and task routing without broadening its authority. |
| `P5-T01` | `P4-T06` | Define the selected ontology's source state space, gauge or symmetry structure, observables, admissible variations, dynamics slot, and reconstruction slot in one compact formal object. |
| `P5-T02` | `P5-T01` | Determine whether Phi_lambda is a group, semigroup, category action, gauge flow, physical evolution, stochastic process, or emergent ordering relation, and prove the basic laws appropriate to that choice. |
| `P5-T03` | `P5-T02` | Build one bounded source action, Hamiltonian, local update law, or source-history measure consistent with the selected ontology and Phi_lambda semantics. |
| `P5-T04` | `P5-T03` | Analyze the unchanged source-dynamics candidate for local composition, constraints, conserved quantities, gauge generators, or probabilistic normalization. |
| `P5-T05` | `P5-T04` | Find source backgrounds or phases suitable for continuum reconstruction and determine linearized modes, stability conditions, and symmetry-breaking structure. |
| `P5-T06` | `P5-T05` | Construct a controlled map from microscopic or source states to effective fields, observables, or geometry with declared scale, approximation, and error. |
| `P5-T07` | `P5-T06` | Perform fresh source-provenance audit and adversarial stress of the unchanged source-theory, dynamics, backgrounds, and reconstruction map. |
| `P5-T08` | `P5-T07` | Produce the canonical source-dynamics manuscript or a definitive scoped obstruction manuscript and update the theorem inventory and next route. |
| `P6-T01` | `P5-T08` | Define the exact causal, influence, or characteristic structure to be derived from source dynamics before any full metric claim. |
| `P6-T02` | `P6-T01` | Use the source dynamics and reconstruction map to derive one characteristic relation, principal polynomial, or causal order, or return a precise obstruction. |
| `P6-T03` | `P6-T02` | Determine whether the derived causal structure fixes an effective conformal class under declared regularity and causality assumptions. |
| `P6-T04` | `P6-T03` | Construct source-defined operational or measure structures that fix the conformal scale and measured durations and lengths. |
| `P6-T05` | `P6-T04` | Show that the reconstructed geometric object is nondegenerate, has Lorentzian signature, and transforms consistently under source-induced coordinate or frame changes. |
| `P6-T06` | `P6-T05` | Determine whether the effective geometry is unique up to declared gauge, natural under source morphisms, robust under admissible variations, and physically tied to propagation and clocks. |
| `P6-T07` | `P6-T06` | Align object names and status with what has actually been proved, replacing overread-prone g_eff language unless Gate B is fully satisfied. |
| `P6-T08` | `P6-T07` | Review the full causal, conformal, scale, signature, covariance, and operational package and integrate it into the frontier or record the exact remaining burden. |
| `P7-T01` | `P6-T08` | Specify explicit source-level matter degrees of freedom, sectors, excitations, defects, representations, currents, or operational observables compatible with the selected ontology. |
| `P7-T02` | `P7-T01` | Build one explicit source matter action, evolution equation, or transition law and derive its basic conserved or constraint structure. |
| `P7-T03` | `P7-T02` | Construct source-level operational devices and protocols whose effective behavior can test geometry and coupling universality. |
| `P7-T04` | `P7-T02`, `P7-T03` | Compute the principal symbols or source propagation relations of the matter sectors and determine whether they share one effective cone or metric structure. |
| `P7-T05` | `P7-T04` | Derive a source-to-effective coupling map that applies to all admitted matter sectors and preserves the common geometry without target import. |
| `P7-T06` | `P7-T05` | Construct the effective matter action and derive the stress-energy tensor or source-equivalent variational object and its conservation conditions. |
| `P7-T07` | `P7-T06` | Perform source-provenance audit and adversarial stress across matter ontology, operational devices, common cones, coupling law, action, stress-energy, and conservation. |
| `P7-T08` | `P7-T07` | Under explicit protected authority, decide whether the audited and stressed package may be adopted in its exact scope as matter coupling, detector semantics, matter action, and stress-energy input. |
| `P8-T01` | `P7-T08` | Choose one explicit route from matter and effective geometry to gravitational dynamics, with exact hypotheses and decision consequences. |
| `P8-T02` | `P8-T01` | State the exact theorem or derivation target connecting source-derived matter and geometry to an effective gravitational action or constraint algebra. |
| `P8-T03` | `P8-T02` | Execute the chosen closure calculation and derive an effective gravitational action, Hamiltonian constraints, or equivalent dynamics from the admitted source and matter inputs. |
| `P8-T04` | `P8-T03` | Vary or otherwise evolve the derived gravitational candidate to obtain field equations and verify compatibility with matter conservation. |
| `P8-T05` | `P8-T04` | Determine physical degrees of freedom, gauge modes, constraints, characteristic speeds, ghosts, tachyons, gradient instabilities, and strong-coupling regions. |
| `P8-T06` | `P8-T05` | Review the unchanged action, field-equation, correction, and stability package for target import, hidden assumptions, algebraic errors, and interpretation overread. |
| `P8-T07` | `P8-T06` | Under explicit protected authority, decide whether the audited and independently reviewed package establishes Einstein equations in an exact or controlled effective regime. |
| `P9-T01` | `P8-T07` | Specify benchmark cases, source-only inputs, intermediate objects, allowed approximations, forbidden target premises, output comparisons, and independent reproduction requirements. |
| `P9-T02` | `P9-T01` | Construct or derive a source state whose effective geometry, matter vacuum, and perturbative behavior recover the Minkowski benchmark within declared scope. |
| `P9-T03` | `P9-T02` | Derive weak-field potentials, free-fall acceleration, redshift, and clock-rate relations from source dynamics and operational devices. |
| `P9-T04` | `P9-T03` | Test causal propagation, local Lorentz behavior, equivalence-principle observables, and common free-fall structure across matter sectors. |
| `P9-T05` | `P9-T04` | Derive a homogeneous and isotropic effective cosmology, expansion law, matter evolution, and controlled dark-energy or cosmological-constant status from source inputs. |
| `P9-T06` | `P9-T05` | Derive the radiative sector, polarizations, speed, damping, dispersion, and coupling to detectors from the source-derived field equations. |
| `P9-T07` | `P9-T06` | Test nonlinear consistency through conservation, constraint propagation, and one nontrivial compact-source or strong-field solution. |
| `P9-T08` | `P9-T07` | Audit all benchmark cases for target import, tuning, inconsistent assumptions, shared-code errors, and scope overread, then seek independent reproduction. |
| `P9-T09` | `P9-T08` | Under explicit protected authority, decide benchmark promotion, exact or approximate GR recovery, and whether the project may claim a completed derivation. |
| `P10-T01` | `P0-T05` | Create machine-readable schemas for assumption provenance and multidimensional scientific status, preserving historical vocabulary through mapped compatibility fields. |
| `P10-T02` | `P10-T01` | Replace free-form task-type analytics with stable work_kind, milestone, candidate_family, result_kind, authority, and scope fields while preserving human-readable titles. |
| `P10-T03` | `P10-T01`, `P10-T02` | Implement candidate IDs, family IDs, statement hashes, assumption hashes, ontology hashes, stage transitions, and supersession edges. |
| `P10-T04` | `P10-T02`, `P10-T03` | Record initial failures, auditor findings, validator failures, repairs, abandoned attempts, supersessions, compute metadata, and final dispositions without replacing canonical scientific artifacts. |
| `P10-T05` | `P10-T03`, `P10-T04` | Specify an append-only canonical data model for task, decision, candidate, claim, validation, authority, and handoff events, with CSV and Markdown as generated views. |
| `P10-T06` | `P10-T05` | Build a bounded pilot that ingests selected control events and regenerates equivalent registry and Markdown views without becoming authoritative. |
| `P10-T07` | `P10-T05` | Design and implement short stable artifact paths, metadata titles, path-length linting, and content-addressed references for new artifacts while preserving historical paths. |
| `P10-T08` | `P10-T05`, `P10-T06` | Refactor the burden map so stable definitions and dependencies remain authored while current statuses and next actions are generated from authoritative state. |
| `P10-T09` | `P10-T07`, `P10-T08` | Perform a non-promotional systems audit of normalized schemas, lineage, attempt history, event-store pilot, path policy, and generated burden status. |
| `P11-T01` | `P0-T05`, `P10-T01` | Create a review protocol that strips task verdict, route history, validator status, and internal confidence from the theorem or candidate packet. |
| `P11-T02` | `P11-T01` | Create normalized classifications for same-context role review, blind same-model review, different-model review, human expert review, and independent replication. |
| `P11-T03` | `P2-T05`, `P10-T01` | Define how theorem sources, proof objects, trusted foundations, builds, and hashes are registered without promoting physical interpretations. |
| `P11-T04` | `P11-T01`, `P11-T02` | Extend target-import checking beyond field-name fragments to aliases, split encodings, equivalent forms, misleading certificates, and prompt-level interpretations. |
| `P11-T05` | `P10-T01`, `P11-T04` | Require source derivation, uniqueness or quotient status, dynamics, operational interpretation, and robustness in addition to no-target purity before physical promotion. |
| `P11-T06` | `P11-T02`, `P11-T05` | Measure reviewer findings at theorem validity, assumptions, countermodels, physical interpretation, and claim scope, without treating consensus as proof. |
| `P11-T07` | `P11-T03`, `P11-T04`, `P11-T05`, `P11-T06` | Exercise blind packets, independence classification, proof evidence, semantic smuggling, and positive-provenance gates on real frontier objects. |
| `P11-T08` | `P11-T07` | Verify that blind review, diversity labels, proof evidence, semantic fixtures, and positive-provenance gates preserve source authority and do not create new promotion shortcuts. |
| `P12-T01` | `P10-T01`, `P10-T02` | Require every new physics task to name a materially new theorem, proof step, countermodel, source law, external result, independent replication, or justified ledger delta. |
| `P12-T02` | `P10-T03`, `P12-T01` | Create machine-readable rules that freeze repeated candidate families and require a new primitive, theorem, variation class, or protected decision for reopening. |
| `P12-T03` | `P10-T02`, `P12-T01` | Create separate planning, reporting, and acceptance budgets for science-bearing work and project-system work. |
| `P12-T04` | `P12-T03` | Require a physics-bearing ordinary task after three consecutive project-system tasks unless tracked evidence shows all science work is blocked by a control failure. |
| `P12-T05` | `P10-T03`, `P10-T04`, `P11-T06`, `P12-T03` | Measure assumption reduction, theorem generality, obstruction unification, independent survival, benchmark breadth, retraction, and ledger durability. |
| `P12-T06` | `P10-T04`, `P12-T05` | Render attempt history, repair rate, validation catches, audit objections, abandonment, and final dispositions without exposing secrets or treating failures as physics refutations. |
| `P12-T07` | `P12-T02`, `P12-T04`, `P12-T06`, `P11-T08` | Run ablations and route-history analyses to test whether payload gates, family freezes, dual budgets, reviewer diversity, and quality metrics improve research decisions. |
| `P13-T01` | `P0-T05` | Compare legacy and planner validation on a fixed representative corpus and authorize cutover only after zero unexplained hard mismatches. |
| `P13-T02` | `P13-T01` | Make the validated planner the single orchestration owner and retain scheduled full validation and rollback controls. |
| `P13-T03` | `P0-T05` | Create one reproducible packaging and dependency contract for scripts, tests, validators, and proof tools. |
| `P13-T04` | `P13-T03`, `P10-T07` | Introduce ruff, mypy or pyright, Python and OS matrices, path-length linting, and a documented programmatic validator API. |
| `P13-T05` | `P13-T03`, `P13-T04`, `P11-T04` | Measure test coverage and strengthen critical invariants with property-based tests, mutation tests, dependency scanning, and code security analysis. |
| `P13-T06` | `P13-T03`, `P13-T04` | Create a devcontainer, container, Nix flake, or equivalent fresh-machine environment for research-control, proof, and benchmark workflows. |
| `P13-T07` | `P10-T08`, `P13-T02` | Add source commit, hashes, task count, generation time, and maximum-lag policy to authoritative-facing generated reports and fail CI on stale views. |
| `P13-T08` | `P13-T05`, `P13-T06`, `P13-T07` | Calibrate checker names and documentation, then run full software, CI, environment, freshness, security, and historical-compatibility validation. |
| `P14-T01` | `P0-T05`, `P10-T01` | Create canonical claim definitions for interpretive redescription, formal or categorical equivalence, genuine emergence, and empirical novelty. |
| `P14-T02` | `P14-T01` | Specify assumption compression, unification, inevitability, explanatory depth, dimension or signature explanation, matter or quantum connection, and problem-solving fertility as explicit evaluative criteria. |
| `P14-T03` | `P11-T05`, `P14-T01` | Integrate the principle that source purity must be supplemented by positive provenance, dynamics, uniqueness or quotient status, operational meaning, and robustness. |
| `P14-T04` | `P4-T05`, `P5-T08`, `P14-T03` | Under protected authority, decide whether the congruence is interpretive, gauge or representative structure, dynamically selected state, or an independent dynamical field. |
| `P14-T05` | `P2-T08`, `P3-T07`, `P14-T03` | Define when a no-go theorem, obstruction, or minimum-extension theorem counts as a completed scientific result and how it affects route closure. |
| `P14-T06` | `P14-T02`, `P14-T03`, `P14-T04`, `P14-T05` | Update source-backed public documentation specifications so ontology, exact closure, formal equivalence, emergence, operational meaning, and empirical novelty are visibly distinct. |
| `P15-T01` | `P14-T01`, `P14-T02`, `P14-T03` | Develop a publication-ready manuscript that clearly states exact operational identity with GR, the interpretive role of the ontology, and the absence of a completed substrate derivation or independent low-energy prediction. |
| `P15-T02` | `P12-T07`, `P13-T08` | Evaluate and document the role architecture, claim gates, negative-result memory, candidate cycles, lineage, attempt history, and v21 governance reforms with controlled baselines and ablations. |
| `P15-T03` | `P2-T08`, `P3-T07`, `P14-T05` | Develop the general selector theorem, finite examples, extension lattice, quotient EqSrc implications, and foundations interpretation into a focused mathematics or philosophy-of-physics manuscript. |
| `P15-T04` | `P6-T08` | Package P5 and P6 results or obstructions as a durable technical report with explicit ontology regime, source dynamics, reconstruction map, causal structure, and geometry status. |
| `P15-T05` | `P9-T09` | If and only if Gate E authorizes it, assemble a derivation manuscript covering source ontology, dynamics, geometry, matter, closure, benchmarks, corrections, assumptions, and independent review. |
| `P15-T06` | `P15-T01`, `P15-T02`, `P15-T03`, `P15-T04` | Create stable, source-backed packages for manuscripts, proofs, benchmark cases, code, environments, assumption ledgers, and claim maps. |
| `P15-T07` | `P15-T06` | Obtain explicit human approval for each manuscript submission, public release, external reviewer contact, or outreach action. |
| `P16-T01` | `P9-T09`, `P10-T09`, `P11-T08`, `P12-T07`, `P13-T08`, `P14-T06`, `P15-T07` | Verify that every V21-R01 through V21-R72 recommendation has direct implementation evidence, validation evidence, and an explicit final status. |
| `P16-T02` | `P16-T01` | Verify that source theory, effective geometry, matter coupling, field equations, and completed-derivation decisions follow the declared dependency chain and protected authorities. |
| `P16-T03` | `P16-T01`, `P10-T09`, `P13-T08`, `P15-T06` | Verify all source paths, candidate identities, event chains, generated-view freshness, proof objects, benchmark receipts, and publication packages. |
| `P16-T04` | `P16-T02`, `P16-T03` | Attack the final project state for hidden target imports, source-purity overread, internal review mislabeled as external, methodology-as-physics claims, and premature derivation language. |
| `P16-T05` | `P16-T04` | Produce an answer-first synthesis of what was proved, adopted, obstructed, improved, human-gated, or left open across science and the research operating system. |
| `P16-T06` | `P16-T05` | Use canonical evidence to mark the multi-step goal complete, continue with an exact repair, or terminalize with a precise human action when protected gates remain. |

## Exact completion contract

- Completion-contract SHA-256: `2afe005a4943e5d899efc27e102e8958bdf4f45380a0a41ce6be25d176943685`

```json
{
  "interpretation": "Execute all 122 work items explicitly included by the corrected v21 plan in their immutable dependency graph, one bounded worker frame and at most one outer AgentJob per generation. Preserve scientific and project-system authority boundaries, exact source identity, fixed guards, human gates, and canonical tracked dispositions. The goal is met only when every included item and every V21 recommendation has final canonical evidence and the final synthesis and relay terminal evidence validate.",
  "required_evidence": [
    "Every included work item has one finalized canonical disposition: completed, precise_obstruction, frozen, superseded, conditionally_not_required, or an explicitly resolved human-gated result.",
    "No required work item remains merely planned, pending, active, indeterminate, or deferred behind unresolved human action.",
    "Every V21 recommendation has direct implementation evidence and final audit coverage.",
    "Every state-changing task passes its required validation and governed checkpoint.",
    "Every candidate and theorem uses immutable identity and source hashes wherever the relevant v21 system is available.",
    "Gates A through E have internally consistent evidence and authority, whether passed, failed, obstructed, or human-denied.",
    "Final provenance, freshness, no-target, no-overclaim, and external-independence audits have no unresolved blocking finding.",
    "The final synthesis separates science, philosophy, methodology, software, publication, and open human actions.",
    "The v4 goal record, generation receipts, leases, successor state, and terminal summary validate; a positive GR derivation is not required, while an unresolved protected human gate requires the deterministic human-action terminal."
  ],
  "user_confirmed_when_ambiguous": false
}
```

## Scheduling and fixed guards

- `max_continue_passes`: `null`
- `deadline_at`: `null`
- `max_repeated_state_fingerprints`: `1`
- `max_live_continuations`: `1`
- `handoff_ready_timeout_seconds`: `60`
- Every stop-on-human-gate, validation, checkpoint, unexpected-dirty-state,
  no-progress, repeated-state, capability-loss, and repository-mismatch guard
  remains `true`.

Unlimited scheduling changes only the count and elapsed-time horizons. It does
not expand the one-worker/one-AgentJob frame, weaken leases or validators,
bypass protected authority, broaden scope, or permit a consumed generation to
run twice.

## Production repository binding

- Execution profile: `production_profile`
- Root: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`
- Git common directory: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.git`
- Branch policy: `main` or `codex/*`; the accepted active contract records `main`.
- Environment mode: `local`
- Accepted starting HEAD: `044c2ac9d75c9e0886dac82c31b8c21c03cc994b`

Before any future launch, rediscover the saved project, task-tool contracts,
active model and effort metadata, root, Git common directory, branch, HEAD,
porcelain, tracked research state, and global relay lease. Never substitute a
fork, hook, controller, plugin, or default reasoning effort.

## Source-hash evidence

The baseline manifest records both the immutable launch hash and the frozen
P0-T03 baseline hash. Their one known mismatch is tracked control-state
evolution, not permission to rewrite the active immutable scope. A future
operator must separately recompute every live mutable hash before launch.

| Path | Immutable launch SHA-256 | P0-T03 baseline SHA-256 |
| --- | --- | --- |
| `.codex/skills/continue-research-continue-goal/SKILL.md` | `1c104985bb950cd1e1fe646f69dffce53d466a49b34f228c24f55efb58d0ac54` | `1c104985bb950cd1e1fe646f69dffce53d466a49b34f228c24f55efb58d0ac54` |
| `.codex/skills/continue-research-goal/SKILL.md` | `12e52f1cf5ef819814424b0b5811dc9ceba13c3bd2dd59e99569141a2ed89481` | `12e52f1cf5ef819814424b0b5811dc9ceba13c3bd2dd59e99569141a2ed89481` |
| `.codex/skills/continue-research-goal/references/goal-file-schema.md` | `35b1477ee973f268a7d2e7947a75b247a8294cbf6c4843f031f9f686e1c47018` | `35b1477ee973f268a7d2e7947a75b247a8294cbf6c4843f031f9f686e1c47018` |
| `.codex/skills/continue-research/SKILL.md` | `4ff16918097dd940bfed731f921acbe496b3e5a1d14f43a0fd352e74b7b0173f` | `4ff16918097dd940bfed731f921acbe496b3e5a1d14f43a0fd352e74b7b0173f` |
| `AGENTS.md` | `0b6270b8eee144d65d6959c822a9bd6b5ba295bbe58d11833cbb44fbd211330f` | `0b6270b8eee144d65d6959c822a9bd6b5ba295bbe58d11833cbb44fbd211330f` |
| `implementations_plans/recommendations_implementation_plan_continue_task-v21.md` | `4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087` | `4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087` |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | `0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61` | `0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61` |
| `research_control/AGENTS.md` | `c93e14bb2cc6e7bbc5c299085f8843ca84d714cdaef99b2b78a46715b5b310ae` | `c93e14bb2cc6e7bbc5c299085f8843ca84d714cdaef99b2b78a46715b5b310ae` |
| `research_control/handoffs/handoff-0772.yaml` | `31374c85ee49e457a8b25eaf6d729a0d0e286f1dd53eac184a502044fdd8de0a` | `31374c85ee49e457a8b25eaf6d729a0d0e286f1dd53eac184a502044fdd8de0a` |
| `research_control/program_state.yaml` | `f0ba4ffcfed230f370fbb902f5bb8b32e3ec3f4a0c98163cdf810b585f8eb4c7` | `b4c042eebd3ff9017496eaa7dbb3a589b578dcca7d520ad5668693d6173ab70f` |

## Explicit non-authority

This manifest is not physics proof, canonical ontology, source-law adoption,
EqSrc discharge, effective metric or coupling derivation, Einstein equations,
benchmark promotion, Gate Chair authority, publication authority, or a
completed derivation. Generated views, validators, registries, tasks, and goal
state remain operational evidence only within their declared authority.
