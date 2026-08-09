---
authority: draft_control_artifact
object_id: MD-V22-P3-T04-PARENT-FUSION-LINEAR-RESPONSE-V1
task_id: RT-20260809-016
job_id: AJ-RT-20260809-016-001
status: draft/control
---

# P3-T04 parent fusion: background and linear response

The fused result constructs the fixed-law pre-principal packet required by
P3-T04. The exact affine source background
`qbar=(s1-s0,s2-s0,0,0,0,3)` solves all six P3-T02 equations, has a positive
`q6` margin, and lies in the rank-two regular locus. Its selection rule is a
lexicographically fixed rational member of the already declared source
solution class, frozen before target access. It is not called Minkowski space,
a physical vacuum, or a canonical background.

For fixed coefficient datum `D`, the equation map is affine-linear and its
Fréchet derivative is exactly `L_D u=(X_1u1,...,X_6u6)`. There are no
algebraic field constraints and no internal field-gauge generators; passive
source-chart changes are representation changes, not physical gauge orbits.
Thus the declared perturbation quotient divides by the zero internal vertical
space. A separate centered-difference implementation reproduces all six
linearized channels with maximum error below `5.8e-11`.

The two-channel logistic response derivative has rank two on the selected
patch. This preserves the P2 verdict
`necessary_condition_met_not_sufficient` for the sealed B1 source-response
interface. It does not admit a physical geometry probe: detector, scale,
device, physical-gauge, cone, and metric typing remain absent. On uniform
periodic source grids, constant-coefficient upwind evolution commutes with the
backward difference. The inherited P3-T03 estimate therefore yields a bounded
`C1` source-chart comparison for `C3` perturbations. Both value and derivative
errors decrease over levels 24, 32, 48, and 64.

The Refuter counterfamily adds source-only cross-response terms that vanish on
the selected background. Its principal two-channel factor changes from
`xi(X1)xi(X2)` to
`xi(X1)xi(X2)-lambda^2 xi(X1-X2)^2`, and two explicit covectors prove that the
zero sets differ. Because this mutation changes the sealed P3-T02 source law,
it is not a within-candidate counterexample and proves no physical
inequivalence. It exposes source-law-selection debt and blocks any uniqueness
overread across unadopted laws while leaving the fixed-law principal
calculation ready for P4-T01.

All five parent conflicts are resolved without weakening limitations. The
decisive result is a constructed draft/control candidate for source-principal
analysis, not a source-law adoption or physical-geometry result. The frozen
one-amplitude and unchanged graph-decoder routes remain frozen. No physical
cone, Lorentzian signature, scale, effective metric, matter coupling, Einstein
equations, Gate verdict, benchmark result, or completed derivation is created.
