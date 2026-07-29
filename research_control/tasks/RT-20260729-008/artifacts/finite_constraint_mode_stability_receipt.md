<!-- authority: control -->

# P8-T05 finite constraint and dynamical-viability receipt

Status: `PASS_SCOPED_OBSTRUCTION_READY_FOR_CHECKPOINT`.

## Result

The exact P8-T04 system has a complete algebraic classification. For
\(n=|\Omega|\) and \(c=|\Pi_C|\), it has \(c\) component-shift redundancies,
\(n-c\) quotient coordinates, \(n-c\) independent algebraic equations, and
zero free homogeneous quotient-response modes after the fixed-source equation
is imposed. Its quotient Hessian is positive definite for \(\alpha>0\).

That result is static. The candidate contains no time derivative, kinetic
form, Hamiltonian or symplectic structure, mass matrix, Lorentzian background,
covector-dependent principal symbol, or nonlinear interaction. Physical
degrees of freedom, characteristic speeds, hyperbolicity, ghosts, tachyons,
gradient instabilities, and a strong-coupling scale are therefore undefined
in the exact candidate.

`OBST-P8T05-STATIC-FINITE-CONSTRAINT-DYNAMICS-UNDEFINED-001` is a precise
candidate-scoped obstruction. A minimal pair of task-local dynamical
completions shares the exact static equation but yields incompatible healthy
and pathological dynamics. This blocks any unique dynamical-viability
inference from the static equation without adopting either countermodel.

## Fixed sources

- P8-T04 equation SHA-256:
  `12a1cfae87cd673241aefe88144ab974b49fc3bad284a81baff90b2e806d5168`
- P8-T03 candidate SHA-256:
  `82dd10d8e91be3781ca4f21e7f9fbf2ce1a9108ae7191db22fed9dfe6086f2fa`
- P8-T03 specification SHA-256:
  `8840b205e8aa12d73f3e782ec6936eb96385bb5694c298b1bf41a2bdfe472626`
- P8-T03 coefficient ledger SHA-256:
  `5948e1ab75e42f622e5cc7309c9a6598720021ff2c893126f93c6b0bc21b7372`
- P8-T03 controls SHA-256:
  `b91f240487fd22b9b95b7c7752e429128d20ccb59b3a202c3430ffbbd2922b6e`
- P8-T02 closure target SHA-256:
  `13402c3d80f114b643a0216484b0ba775a2f02d1f0733f33d8cf86044e6add96`
- P7-T06 source action SHA-256:
  `386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7`
- P7-T08 protected decision SHA-256:
  `85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827`
- P6-T08 Gate B certificate SHA-256:
  `f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b`

## Durable evidence

- Constraint, mode, and stability report:
  `finite_constraint_dynamical_viability_stress_v1.tex`
- Minimal dynamical-completion countermodels:
  `finite_constraint_dynamic_completion_countermodels_v1.yaml`
- Stability phase diagram:
  `finite_constraint_stability_phase_diagram_v1.yaml`
- Task controls:
  `finite_constraint_mode_stability_controls_v1.yaml`
- Deterministic validation receipt:
  `finite_constraint_mode_stability_validation_v1.json`

The task-local validator ID is
`validate_finite_constraint_mode_stability_v1`. Validator and TeX-build
success are operational evidence only.

## Freeze and next route

The unchanged finite equation is locally frozen against reinterpretation as
evidence of physical dynamical viability or a healthy GR limit. Materially
new source-side dynamics and a new kinetic or continuum construction remain
open. After a qualifying checkpoint, P8-T06 may independently audit the
unchanged P8-T03 through P8-T05 closure record.

## Claim boundary

The packet remains `draft/control`, `proposal-only`, with
`blocked_adoption_open_continuation`. It does not construct physical time,
target geometry, a target stress-energy tensor, an Einstein equation, or a
healthy GR limit. It does not authorize canonical ontology or source-law
adoption, exact-GR recovery, benchmark promotion, proof, publication, push,
global no-go, future source-extension impossibility, or completed derivation.
