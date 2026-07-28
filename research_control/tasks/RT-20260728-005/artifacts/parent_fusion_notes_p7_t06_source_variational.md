<!-- authority: science_draft -->

# P7-T06 parent fusion: finite source variational object and directional obstruction

Status: `draft/control`, `proposal-only`, `source-extension data`.
Adoption: `blocked_adoption_open_continuation`.
Claim boundary: `CB-V21-P7-T06-SOURCE-VARIATIONAL-OBJECT-001`.

## Fused result

The two child reviews agree on a constructive result and a distinct scoped
obstruction. For every separately declared finite rational P7-T02 row kernel
\(P\), the task-local split
\[
C=(P+P^\mathsf T)/2,\qquad A=(P-P^\mathsf T)/2
\]
defines a symmetric nonnegative edge-weight record and a directional residue.
For a new dimensionless source test coordinate \(q\)—explicitly not the P7-T01
charge-chain record \(q(\Psi)\)—the finite functional
\[
\mathcal V_{\rm src}(q)
=\frac14\sum_{x,y}C_{xy}(q_y-q_x)^2
\]
has exact first variation
\[
\mathcal D_{\rm src}(q)=L_Cq,\qquad
L_C=\operatorname{Diag}(C\mathbf1)-C.
\]

The edge record
\(\mathcal J_{{\rm src},xy}=C_{xy}(q_x-q_y)\) is antisymmetric. Its total
divergence cancels on a finite carrier, and summing over a subset leaves
exactly the crossing-edge sum. These are finite source-edge algebra identities,
not a physical current, physical conservation law, spacetime boundary
formula, or Noether result.

For the fixed P7-T02 forward kernel
\[
P_{\rm fwd}=\begin{pmatrix}1/2&1/2\\0&1\end{pmatrix},
\]
\(I-P_{\rm fwd}\) is nonsymmetric. A scalar quadratic under the declared
standard coordinate pairing has a symmetric Hessian. Consequently, the full
directional operator is not the gradient of a scalar quadratic on the same
two probe variables in this fixed class. Weighted pairings, proper constraint
subspaces, auxiliary variables, doubled or nonscalar principles, nonlocal
functionals, and future source extensions remain open. This is not a global
no-go theorem.

## Parent conflict resolutions

The mathematical child supplied exact rational checks and identified the
crucial distinction between the candidate Laplacian and the symmetric update
residual. The philosophical child exposed eight blocking notation, semantics,
and scope hazards. The parent resolved all ten fused conflicts in one review
round; none required a child rewrite.

The most important guard is:
\[
(I-P)-L_C=I-\operatorname{Diag}(C\mathbf1)-A.
\]
Therefore the functional loses more than the directional residue in the
general row-stochastic case. It ignores diagonal holding weights and can
differ from \(\operatorname{Sym}(I-P)=I-C\) through degree imbalance.
\(L_C=\operatorname{Sym}(I-P)\) only when \(C\mathbf1=\mathbf1\), which is
not true for the fixed forward control. The phrase “source-equivalent” is
therefore only the v21 plan label for a kernel-derived symmetric-conductance
source variational surrogate. It is not information equivalence, dynamical
equivalence to P7-T02, or equivalence to a physical matter action.

The matrix convention is also explicit: \(P_{xy}\) uses source rows and target
columns, while the P7-T02 column-bookkeeping update matrix is \(P^\mathsf T\).
The symmetric \(C\) is unchanged by transpose, and both \(I-P\) and
\(I-P^\mathsf T\) are nonsymmetric for the forward control.

## What survives fusion

The fused candidate preserves:

- one exact nonnegative finite source quadratic;
- one reproducible first variation and symmetric graph Laplacian;
- one antisymmetric finite source-edge flux record;
- one exact closed-carrier cancellation identity;
- one exact finite-cut boundary formula;
- one zero-total compatibility condition for an added algebraic residual;
- one fixed-control scalar-quadratic representability obstruction; and
- identity, symmetric, forward, directional-cycle, malformed, boundary, and
  anomaly controls for deterministic validation.

It preserves the P7-T05 obstruction as well: current sector data do not derive
one universal control, equipment, or variational-law selector. The present
construction is conditional on each separately declared kernel and does not
repair that missing law.

## Claims that do not survive

No child or parent result establishes a physical matter variable, matter
action, stress-energy tensor, physical flux, energy-momentum or charge
conservation, equations of motion, locality, causal structure, characteristic
cone, metric, geometry, universal matter coupling, equivalence-principle
behavior, Einstein equations, exact-GR recovery, ontology adoption, proof,
publication, benchmark promotion, or completed derivation.

The functional’s nonnegativity is not physical energy positivity. Its shift
null direction is not gauge symmetry. Its stationary points are not physical
equations of motion. The directional residue is not an arrow of time,
dissipation, entropy production, or force. Validation, same-context child
review, registries, generated derivatives, and checkpoint state are process
evidence only.

## P7-T06 disposition and next route

The parent classifies the exact result as
`precise_obstruction_with_constructive_restricted_variational_object`.
This materially advances the proposal-only source formalization burden, but
the physical matter-coupling milestone remains open. The plan-authorized next
packet is P7-T07: one `smuggling-auditor@0.2.0`
`ontology-law-research-packet` using
`audit_source_variational_matter_package_v1`, and only after the P7-T06
governed checkpoint succeeds.
