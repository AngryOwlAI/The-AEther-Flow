<!-- authority: science_draft -->

# P7-T03 source operational-device suite receipt

## Result

`RT-20260728-002` constructs
`SourceOperationalDeviceSuiteCandidate_v1` as one task-local
`draft/control`, `proposal-only` finite source protocol suite.  Its protocol
type is
\[
  {\cal D}=({\cal C},P,I,A,r,S,F),
\]
with finite source preparations, declared intervention labels, finite formal
token alphabets, a total single-valued source-history readout, a declared
success subset, and a fail-closed classifier.

The suite defines guarded `Clock_src`, `Rod_src`, `Signal_src`,
`Detector_src`, and `FreeFall_src` roles.  Each role has explicit source
objects, preparations, readout rules, success conditions, and failure
branches.  These names are syntactic role labels only.

## Exact candidate-relative mathematics

`P7T03-THM-FINITE-TOKEN-RESPONSE-CLOSURE-001` proves that every formal token
response is a finite nonnegative rational, that a total readout partitions
the finite bookkeeping mass, and that equal-mass intervention differences
sum to zero.  `P7T03-THM-SOURCE-PRESENTATION-NATURALITY-001` proves that
transport of the entire protocol tuple intertwines token responses and
intervention differences under a compatible source-presentation
isomorphism.

The bounded controls include:

- a two-state cycle token with exact response `1/4`;
- a three-address endpoint token with exact response `1/4`;
- a three-address arrival token with exact response `1/4`;
- an explicitly bijected trigger token with the same exact response `1/4`;
- a baseline/intervention contrast `(1/2,-1/2)`;
- a disjoint clock–signal joint cell
  `1/16=(1/4)(1/4)`;
- a valid no-event branch;
- malformed partial-readout, out-of-alphabet, and target-import branches;
- an underdetermined missing-readout branch; and
- an early-trigger cross-device inconsistency with responses `1/4` and
  `3/4`.

The task-local deterministic validator passes 86 of 86 checks.  A scratch
LaTeX build renders seven pages with references resolved.  Two internal
same-context child perspectives were fused in one parent review: thirteen
differences were resolved and zero blocking conflicts remain.

## Status boundary

The response coefficients are formal bookkeeping values, not physical
probabilities.  The composition horizon is not physical time.  Tick,
endpoint, arrival, trigger, and baseline tokens do not establish a physical
clock, rod, length, signal, causal cone, detector, observation, free fall,
geodesic, or equivalence principle.

Current ontology does not derive or uniquely select the preparations,
interventions, token alphabets, readout maps, success subsets, failure
classifiers, or cross-device identifications.  The result does not adopt
`M_src`, `g_eff`, a source law, operational semantics, matter coupling,
stress energy, an Einstein equation, benchmark recovery, or a completed
derivation.  It creates no proof, publication, Gate Chair, or physics
promotion authority.  Adoption remains
`blocked_adoption_open_continuation`.

## Next bounded route

After one successful governed checkpoint for
`AJ-RT-20260728-002-001`, one fresh bounded P7-T04 packet may analyze common
formal source propagation across the constructed protocols.  P7-T04 is not
executed here.  Any common formal propagation relation would still require
separate authority and derivation before it could be read as physical
causality, effective geometry, universal coupling, or GR behavior.
