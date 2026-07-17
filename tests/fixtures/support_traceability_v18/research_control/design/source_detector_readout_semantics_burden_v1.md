<!-- authority: control -->

# Source Detector/Readout Semantics Burden v1

## Purpose

This control note defines `source_detector_readout_semantics` as a named
matter-coupling frontier burden for v18 P5. It records the lowest-authority
question that must be answered before detector/readout language can support
matter-coupling work:

Can the project define a source-side detector or readout interface without
importing empirical detector protocols, proper time, a target metric,
stress-energy semantics, a matter action, exact-GR benchmark behavior, or
process authority as physics?

This note is not a detector-semantics adoption, not a matter-coupling
derivation, and not a Distance-to-GR ledger update.

## Authority Status

This file is project-control and science-draft routing guidance. It may be
used by Directors, selectors, auditors, validators, and future task overlays to
route bounded source detector/readout work.

It does not change canonical ontology, source-law status, `MetricData(E)`,
`g_eff`, detector semantics, matter semantics, coupling-law status,
matter-coupling status, stress-energy status, matter-action status,
Einstein-equation status, benchmark status, Gate Chair status, or completed
derivation status.

## Burden Model

```yaml
burden_id: "source_detector_readout_semantics"
milestone: "matter_coupling"
required_object: "Det_src or Readout_src"
current_status: "proposal_burden_only"
blocking_burden: "source-side readout law without empirical detector, proper-time, target metric, stress-energy, matter-action, or benchmark import"
accept_criteria:
  - source-side readout law
  - no empirical detector protocol import
  - no proper-time import
  - no target metric import
  - finite/local witness
  - compatibility with SourceCouplingLawCandidate_EStar_v1
failure_or_freeze_criteria:
  - detector_semantics_requires_target_import
  - readout_law_requires_new_source_primitive
  - route_repeats_placeholder_without_new_payload
```

## Formal Burden Definition

Definition (proposal burden only). Let `E_*` be a bounded source event or
finite/local source situation in the source-side task context. A future
`Det_src(E_*)` or `Readout_src(E_*)` candidate may count as a source
detector/readout burden witness only if it supplies all of the following:

1. A source-side domain of readable source records, not target detector
   observations.
2. A readout relation or law whose inputs are source-side objects already
   admitted by the task boundary.
3. A fail-closed rule for malformed, missing, ambiguous, or target-importing
   readout records.
4. A finite/local witness family showing at least one nonempty readout case.
5. A compatibility statement with `SourceCouplingLawCandidate_EStar_v1` that
   does not treat that candidate as adopted.
6. A no-target-import certificate covering empirical detector protocol,
   proper-time normalization, target metric, benchmark behavior,
   stress-energy semantics, and matter-action language.

This definition is a burden target. It is not a constructed candidate and not
an adopted object.

## Relation To Existing Matter-Coupling Controls

The matter-coupling derivation moratorium already lists detector semantics or
an explicitly source-side replacement as a prerequisite for any direct
universal matter-coupling derivation. This note names that prerequisite as the
bounded burden `source_detector_readout_semantics`.

The existing matter-coupling DAG contains a blocked
`mc_detector_semantics_target` node. P5-T01 does not modify the DAG. It only
defines the question that P5-T02 may later ask about adding a DAG or ledger
surface without unauthorized promotion.

The Distance-to-GR ledger continues to control official milestone status.
This note requests no ledger row and performs no ledger status update.

## Allowed Future Routes

Lawful next routes after this note are narrow and non-promotional:

- P5-T02 project-control setup for a DAG or ledger-delta question;
- P5-T03 bounded source detector/readout candidate setup;
- a later candidate-constructor packet for `Det_src` or `Readout_src`;
- a later smuggling audit for target-import detection;
- a later Refuter stress packet for placeholder collapse, empirical
  substitution, and finite/local perturbation;
- a later selector deciding repair, freeze, or integration into a repaired
  coupling-law candidate.

No route may skip from this burden note to detector-semantics adoption,
coupling-law adoption, matter-coupling derivation, Einstein-equation
derivation, benchmark promotion, or completed derivation.

## Forbidden Overreads

No future packet may treat this note as establishing any of the following:

- `Det_src` adoption;
- `Readout_src` adoption;
- detector-semantics adoption;
- empirical detector protocol authority;
- proper-time normalization;
- target-metric authority;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- Einstein equations;
- exact-GR benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- future source-extension impossibility; or
- broad rejection of the theory.

## Validator Guidance

A future validator may check that detector/readout packets include the burden
model, preserve `current_status: proposal_burden_only` until a protected
authority changes it, and hard-fail claims that read a candidate, audit, or
validator pass as adopted detector semantics.

A validator PASS is only structure and claim-boundary evidence. It is never
proof of detector semantics, matter coupling, or downstream GR recovery.

## Source Materials

The Aether-Flow Research Project. (2026, July 7). *Recommendations
implementation plan Continue Task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`

The Aether-Flow Research Project. (2026, July 2). *Matter-coupling
derivation moratorium* [Internal control note].
`research_control/design/matter_coupling_derivation_moratorium.md`

The Aether-Flow Research Project. (2026, July 8). *Handoff 0699*
[Internal research-control handoff].
`research_control/handoffs/handoff-0699.yaml`
