<!-- authority: control -->

# Handoff 0874 — P5-T07 source-dynamics audit and stress

Status: `ready_after_checkpoint`.

`handoff-0874` records the bounded P5-T07 audit and stress result.

P5-T07 completed one bounded audit and refuter-style stress of the exact,
unchanged P5-T01 through P5-T06 source package.

## Result

The package passes the inspected textual no-target-import,
no-information-creation, and process-authority audits. Its candidate-specific
flow formulas, structural results, background analysis, and P5-T06 error
bounds survive.

The stronger provenance and geometry-robustness premise fails precisely:

- `da/dlambda = -gamma a^(2m+1)` for every integer `m >= 1` has the same
  relevant qualitative forward-semiflow, reflection, stationary-state,
  attraction, and backward-horizon properties, so those properties do not
  select the cubic exponent.
- Under `b=d a` and `lambda'=c lambda`,
  `gamma'=gamma/(c d^(2m))`.
- The P5-T06 quantizer obeys
  `N_(d epsilon)(d a)=d N_epsilon(a)`, so `epsilon` is amplitude-coordinate
  data absent a source-derived normalization.
- The one-dimensional candidate defines no transverse local dynamics or
  characteristic operator.

The precise obstruction is
`OBST-P5T07-QAMP-INTRINSIC-LAW-SCALE-ROBUSTNESS-001`.
The exact unchanged one-mode cubic-flow and fixed-resolution route is locally
frozen as support for geometry.

This is not a global no-go theorem, canonical ontology or source-law
adoption/rejection, physical scale or geometry result, future source-extension
impossibility, a broader framework verdict, downstream GR promotion, proof,
publication, push, or completed derivation.

## Next action

Run the one governed checkpoint for `AJ-RT-20260725-014-001`. Only after that
commit may one fresh bounded P5-T08 `ontology-formalizer@0.2.0` packet integrate
the surviving source-dynamics mathematics, scoped obstruction, local freeze,
and source-ontology milestone decision. P5-T08 must not repair or reopen the
frozen route.
