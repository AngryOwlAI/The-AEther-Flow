# EqSrc Intrinsic Discriminator and Admissibility Law Candidate v3 Receipt

## Result

`RT-20260718-031` produces proposal-only
`EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v3`.

The exact result is
`candidate_repaired_pending_fresh_smuggling_audit`. It addresses
`OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001` at the
candidate level by typing relation preservation and reflection between two
supplied source packages and aligning the reflection rule with injectivity of
the induced \(H_1\) map.

The obstruction is `addressed_in_candidate_not_independently_cleared`.

## New Mathematical Payload

For \(G:A_E\rightarrow A_{E'}\), relation preservation is equivalent to a
unique factorization
\[
\chi_{E'}G=\bar G\chi_E,\qquad \bar G:K_E\rightarrow K_{E'}.
\]
Under this factorization, relation reflection is equivalent to injectivity of
\(\bar G\).

For a chain map \(F:E\rightarrow E'\), the chain equations map cycles to
cycles and boundaries into boundaries. Therefore \(F_1|_{A_E}\) always
preserves the relation, its induced quotient map is \(H_1(F)\), and
\[
\operatorname{RelRefl}_{E,E'}(F_1|_{A_E})
\Longleftrightarrow H_1(F)\text{ is injective}.
\]
Equivalently,
\[
(F_1|_{A_E})^{-1}(B_{E'})=B_E.
\]

A chain isomorphism is sufficient because it induces a homology isomorphism.
It is not necessary.

## Exact Noninvertible Witness

For
\[
C_2=\mathbb F_2\langle f\rangle,\quad
C_1=\mathbb F_2\langle a,b\rangle,\quad C_0=0,\qquad
\partial_2f=a,
\]
define \(F_2=0\), \(F_1(a)=0\), and \(F_1(b)=b\).

The degree-one map has image and kernel of size two, so it is noninvertible.
It induces identity on \(H_1\cong\mathbb F_2\langle[b]\rangle\). Exhaustive
enumeration gives four states, 16 ordered relation tests, eight related pairs,
eight unrelated pairs, and zero mismatches.

This proves that whole-chain or degree-one invertibility is not necessary for
relation reflection. It does not establish physical reversibility or physical
admissibility.

## Repaired Fail-Closed Rule

- Proved noninjectivity of the induced quotient map falsifies reflection.
- If injectivity is not established, withhold the reflection certificate
  without asserting noninjectivity.
- Mere noninvertibility of \(F\), \(F_1\), or the chain package is
  inconclusive.
- Failure closes only the named map or candidate instance, not general EqSrc
  or future source-extension work.

## Surviving v2 Core

The quotient-label versus relation distinction, exact translation theorem,
linear stabilizer criterion, corrected \(e_2\) result, ambient \(L\) contrast,
conditional quotient uniqueness, and finite boundary-move robustness remain
valid under their displayed hypotheses.

Cross-complex pointwise label fixing is not introduced without a separately
typed comparison between quotient codomains.

## Primitive Selection and Adoption

Both \(E\) and \(E'\) are supplied candidate source packages. Current ontology
does not derive the finite chain-package family, field, truncation,
differentials, homology degree, homology discriminator, boundary variations,
or category of physically admissible chain maps.

Algebraic naturality is not physical covariance. Relation reflection is not
physical reversibility. Homology classes are not established observables.

The candidate remains a `new_ontology_primitive_candidate` with
`blocked_adoption_open_continuation`. General `EqSrc` remains undischarged,
and the Distance-to-GR and metric-use ledgers are unchanged.

## Next Route

Run one bounded fresh `smuggling-auditor@0.2.0`
`ontology-law-research-packet` against exact v3. It must audit the typed
predicates, quotient factorization, induced-\(H_1\) reflection theorem,
noninvertible witness, surviving v2 core, shared-differential primitive
selection, and physical or process overreads.

Refuter stress may not bypass the fresh audit. The audit may not repair,
adopt, stress-test, or promote the candidate.

## Forbidden Overreads

This receipt does not authorize canonical ontology modification, source-law
adoption, physical admissibility, physical covariance, general `EqSrc`,
RetainH, GenH, or `M_src` adoption, `g_eff`, matter coupling, Einstein
equations, unrestricted robustness, Distance-to-GR or metric-use ledger
change, benchmark promotion, Gate Chair verdict, completed derivation, future
source-extension impossibility, program-level no-go, or global theory
rejection.

## Validation

Task-local validator:

```text
.venv/bin/python research_control/tasks/RT-20260718-031/artifacts/validate_eqsrc_intrinsic_discriminator_admissibility_law_candidate_v3.py --write-report --json
```

Expected status: `PASS`.
