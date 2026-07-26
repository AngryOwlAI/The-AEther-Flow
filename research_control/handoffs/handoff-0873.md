# Handoff 0873 — source-amplitude coarse-graining map complete

`handoff-0873` records the bounded P5-T06 result for the exact unchanged
P5-T03 cubic-amplitude source dynamics and preserves every P5-T04 structural
and P5-T05 background and phase finding.

For every dimensionless source-amplitude resolution `epsilon>0`, define

`N_epsilon(a)=epsilon sgn(a) floor(|a|/epsilon+1/2)`

with half-grid ties away from zero. The map
`C_epsilon(q_a)=N_epsilon(a)` takes the exact source family to
`O_epsilon=epsilon Z`, and `R_epsilon(c)=q_c` decodes a lattice code back to
the same source family.

The code round trip is exact. The source-state round trip has uniform
amplitude and `C0` error at most `epsilon/2`. The within-bin residual is lost,
and nonzero sign is lost inside the open zero bin. On `|a|<=A`, the source
functional `L=a^2/2` has error at most
`A epsilon/2+epsilon^2/8`.

The map is exactly equivariant under the explicit source reflection and
trivially covariant under identity-only declared redundancy. The exact source
flow is `1`-Lipschitz, giving raw coded-dynamics error at most `epsilon`,
requantized lattice error at most `3 epsilon/2`, and lattice semigroup defect
at most `3 epsilon/2`. The exact source flow remains authoritative.

At fixed resolution, the quantizer is piecewise constant and discontinuous at
half-grid thresholds. Its codomain is a discrete amplitude lattice, and its
decoded image remains the one-dimensional source family. `epsilon` is not
physical length, time, energy, detector resolution, renormalization scale, or
target-geometric scale.

`OBST-P5T06-QAMP-LOCAL-FIELD-RANK-001` records the decisive scoped
limitation. Every `C1` effective-coordinate map from `Q_amp` has differential
rank at most one. Together with P5-T04 patch rigidity and the P5-T05 absence
of a local reconstruction phase, the exact current family cannot supply
independent local field data, a characteristic operator, causal structure, or
geometry.

This does not rule out a conservative multi-mode, locally patchable, coupled,
stochastic, or other source extension and is not a global theory rejection.
The result remains `draft/control`, `proposal-only`, and `source-extension
data`.

The path to causal structure is explicit but unmet: independent local source
data and gluing, a source-defined operator on local variations, a
characteristic set and source-invariant cone theorem, and scale, regularity,
robustness, and operational-response semantics must precede any later
`M_src`, `g_eff`, or exact-GR recovery packet.

After the governed checkpoint commits, the next bounded route is P5-T07 under
`continue-research` with `smuggling-auditor@0.2.0`: audit and refuter-stress
the complete P5-T03 through P5-T06 source dynamics and reconstruction package
for target import, information creation, covariance and physical-scale
overread, error-bound defects, robustness, and claim-boundary smuggling.
P5-T07 is not executed by this handoff.
