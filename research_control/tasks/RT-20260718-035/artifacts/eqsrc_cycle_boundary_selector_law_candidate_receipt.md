# EqSrc Cycle–Boundary Selector Law Candidate Receipt

## Result

`RT-20260718-035` formalizes proposal-only
`EqSrcCycleBoundarySelectorLaw_src^cand,v1`. The result is
`candidate_formalized_pending_fresh_smuggling_audit`.

For a finite odd-oriented-marked source record \(S=(X,P)\), the proposal forms the
permutation module \(\mathbb F_2^X\), takes the fixed space under
\(\operatorname{Aut}(X,P)\) as \(A_S\), and takes the kernel of mark parity as
\(B_S\). The partial selector returns \((A_S,B_S)\) or a tagged failure before
the quotient and candidate relation are evaluated.

The mark first determines \(u_S=\mathbf1_{X\setminus P}\) and the affine
action \(a\mapsto a+\epsilon u_S\). Only afterward does the packet calculate
\(A_S\), prove \(B_S=\mathbb F_2u_S\), and form the relation. This ordering is
the candidate's formal non-circularity certificate; it does not prove that the
mark or its variations are physically admissible.

## Decisive Mathematical Payload

The packet proves:

- exact marked-source naturality and automorphism equivariance;
- uniqueness up to quotient-codomain bijection for every surjective
  discriminator with the same kernel pair;
- compatibility with any chain presentation having cycle space \(A_S\) and
  boundary image \(B_S\), without claiming presentation uniqueness; and
- robustness under every finite word of the pre-relation affine action.

The four-point witness with \(P=\{0\}\) has four selected states and two
two-element classes. Replacing the mark on the same carrier by
\(P'=\{1,2,3\}\) selects a different boundary subspace and relation. This
demonstrates fixed-carrier discrimination relative to explicit source data.
It is a structural mark mutation, not a robustness result. Marked-source
naturality is exact but limited to mark-preserving bijections, and
automorphism equivariance is weak because \(A_S\) is a fixed space.

## Claim and Authority Boundary

Current ontology does not derive the oriented unary mark, the marked-record
category, the parity selector, or their physical admissibility. Source
symmetry alone does not force this choice. The mark may merely expose rather
than solve the missing source-choice burden. The candidate remains
`proposal-only` source-extension data with
`blocked_adoption_open_continuation`.

No canonical ontology edit, source-law adoption, physical-admissibility
result, general EqSrc discharge, RetainH, GenH, M_src, g_eff, matter coupling,
Einstein equations, benchmark promotion, Gate Chair verdict, completed
derivation, future source-extension impossibility, or project-wide rejection conclusion
follows. The Distance-to-GR and metric-use ledgers are unchanged.

## Freeze and Next Route

The exact v3 construction–audit–stress route remains locally frozen. This
distinct marked-source route is `not_frozen` because it supplies a new partial
selector, theorem payload, explicit failure branches, and a relation-changing
same-carrier witness.

The next lawful packet is one fresh bounded `smuggling-auditor@0.2.0` audit of
this exact candidate. It must test mark provenance, hidden choice renaming,
target/process imports, physical-covariance overread, variation circularity,
and finite-witness generalization. It may not repair or adopt the candidate.

## Validation

Task-local validator:

```text
.venv/bin/python research_control/tasks/RT-20260718-035/artifacts/validate_eqsrc_cycle_boundary_selector_law_candidate.py --write-report --json
```

Expected status: `PASS`.
