<!-- authority: control -->

# Handoff handoff-0895: P7-T06 finite source variational object

## Completed scope

`RT-20260728-005` constructs a task-local, `draft/control`,
`proposal-only` variational surrogate from each separately declared finite
P7-T02 row kernel \(P\). With
\(C=(P+P^\mathsf{T})/2\), it defines
\[
  \mathcal V_{\rm src}(q)
  =\frac14\sum_{x,y}C_{xy}(q_y-q_x)^2
\]
on a dimensionless formal source probe \(q\). Its first variation is
\(L_Cq\), with \(L_C=\operatorname{Diag}(C\mathbf 1)-C\). The
antisymmetric source-edge record \(J_{xy}=C_{xy}(q_x-q_y)\) gives exact
closed-carrier cancellation and finite-cut identities.

The fixed P7-T02 forward kernel has nonsymmetric \(I-P\). Since the linear
part of a scalar-quadratic standard-coordinate gradient is symmetric, that
full directional residual cannot be such a gradient on the same variables.
This is `OBST-P7T06-DIRECTIONAL-KERNEL-NONVARIATIONAL-001`.

## Status boundary

The result is finite source algebra and a fixed-class obstruction only.
In general, \(L_C\neq\operatorname{Sym}(I-P)\): the restricted functional
discards directional residue, diagonal holding weights, and degree
imbalance. It is not dynamically equivalent to the P7-T02 update.

The probe \(q\) is not the P7-T01 charge chain or a physical field. The
functional is not a physical matter action, its first variation is not a
stress-energy tensor, and its source-edge cancellation is not physical
energy-momentum conservation. No physical coupling, geometry,
equivalence-principle behavior, Einstein equations, or exact-GR result
follows. Adoption remains `blocked_adoption_open_continuation`.

The obstruction does not exclude weighted, constrained, auxiliary,
nonscalar, nonlocal, or future source-side variational structures. It is not
a global no-go theorem, theory-wide rejection, or future-extension
impossibility result.

## Next bounded route

First run one governed checkpoint for `AJ-RT-20260728-005-001`. Only after it
commits may one fresh bounded `smuggling-auditor@0.2.0`
`ontology-law-research-packet` execute v21 P7-T07.

That packet must audit P7-T01 through P7-T06 for source provenance, target
imports, physical-semantic smuggling, scope inflation, and unsupported
adoption. It may report an exact audit verdict or precise repair obligation,
but it may not promote the proposal-only package into physical matter,
geometry, coupling, action, stress energy, conservation, or GR. This handoff
does not execute P7-T07.
