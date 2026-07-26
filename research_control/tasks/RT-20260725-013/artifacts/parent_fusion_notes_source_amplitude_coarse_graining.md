---
authority: science_draft
status: draft_control
task_id: RT-20260725-013
job_id: AJ-RT-20260725-013-001
plan_task_id: P5-T06
---

# P5-T06 parent fusion notes

## Fused map result

The two internal perspectives preserve the exact P5-T03 cubic-amplitude
candidate and define one controlled source-only resolution map. For
`epsilon>0`, the odd nearest-lattice quantizer

`N_epsilon(a)=epsilon sgn(a) floor(|a|/epsilon+1/2)`

maps the declared amplitude observable to `O_epsilon=epsilon Z`, with
half-grid ties away from zero. The coarse map is
`C_epsilon(q_a)=N_epsilon(a)`, and `R_epsilon(c)=q_c` decodes a lattice value
back to the same source family.

The code round trip is exact. The source-state round trip has amplitude and
`C0` error at most `epsilon/2`, uniformly for every real amplitude. On a
declared bounded region `|a|<=A`, the error in `L=a^2/2` is at most
`A epsilon/2+epsilon^2/8`.

## Information and covariance boundary

Each coarse code identifies a full amplitude bin. The within-bin residual is
lost, and nonzero sign is lost inside the open zero bin. No independent patch,
spatial, momentum, characteristic, causal, manifold, metric, or matter datum
survives because none exists in the input.

The quantizer is odd, so it is exactly covariant under the explicit source
reflection and trivially covariant under identity-only declared redundancy.
This does not establish target diffeomorphism covariance or covariance under
an undeclared source-isomorphism group.

## Dynamic error and smoothness boundary

The exact cubic-amplitude flow is `1`-Lipschitz in amplitude. The raw effective
evolution therefore has semiconjugacy error at most `epsilon`; requantizing it
to the amplitude lattice gives error at most `3 epsilon/2` and semigroup
defect at most `3 epsilon/2`. The exact source flow remains authoritative.

At fixed resolution, the quantizer is piecewise constant and discontinuous at
half-grid thresholds. Its codomain is a discrete lattice, and its decoded
image remains one-dimensional. Convergence as `epsilon` tends to zero is only
in the source amplitude and `C0` norms; it does not infer a physical dimension
or smooth geometry.

## Averaging and local-reconstruction boundary

Every linear source probe on `Q_amp` is proportional to the one amplitude. It
either recovers that same global scalar or collapses the family. Spatial
averaging cannot create independent local degrees.

`OBST-P5T06-QAMP-LOCAL-FIELD-RANK-001` is the decisive scoped obstruction.
Every `C1` effective-coordinate map from the one-dimensional `Q_amp` family
has differential rank at most one. Combined with P5-T04 patch rigidity and
the P5-T05 absence of a local reconstruction phase, the current family cannot
supply independent local field data, a characteristic operator, causal
structure, or geometry. This is not a global no-go theorem and does not close
conservative source-extension continuation.

## Path to causal structure and next route

A genuine path to causal structure would first require independently variable
local source data and gluing, then a source-defined operator on local
variations, a characteristic set and source-invariant cone theorem, and scale,
regularity, robustness, and operational-response semantics. Only later,
under separate burdens, could `M_src`, `g_eff`, matter coupling, and exact-GR
recovery be tested.

P5-T06 is complete at `draft/control`, `proposal-only`, and
`source-extension data` scope because the map, typing, scale, convergence,
information loss, surviving observables, covariance, dynamic error,
smoothness, examples, negative controls, local obstruction, and causal path
are explicit. After a governed checkpoint, P5-T07 should use
`smuggling-auditor@0.2.0` to audit and refuter-stress the source dynamics and
reconstruction package.

Canonical ontology or source-law adoption, physical scale, physical
coarse-graining, source manifold, causal structure, `g_eff`, matter coupling,
Einstein equations, exact-GR recovery, benchmark promotion, Gate Chair
closure, proof publication, push, completed derivation, global theory
rejection, and future source-extension impossibility remain blocked.
