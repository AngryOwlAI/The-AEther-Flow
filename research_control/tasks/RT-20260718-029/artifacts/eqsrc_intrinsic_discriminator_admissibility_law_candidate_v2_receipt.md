# EqSrc Intrinsic Discriminator and Admissibility Law Candidate v2 Receipt

## Result

`RT-20260718-029` produces proposal-only
`EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v2`.

The exact result is
`candidate_repaired_pending_fresh_smuggling_audit`. It addresses
`OBST-EQSRC-INTRINSIC-DISCRIMINATOR-RELATION-LABEL-001` by defining
pointwise discriminator-label fixing separately from kernel-pair relation
preservation and reflection.

## New Mathematical Payload

Let \(A=Z_1(E)\), \(B=B_1(E)\), \(K=A/B\), and
\(\chi:A\rightarrow K\). A map \(V:A\rightarrow A\) preserves the kernel-pair
relation exactly when it induces a unique map
\(\bar V:K\rightarrow K\) with \(\chi V=\bar V\chi\). Relation reflection is
injectivity of \(\bar V\), while pointwise label fixing is the stronger
condition \(\bar V=\mathrm{id}_K\).

For every translation \(\tau_c(z)=z+c\),
\[
\chi(\tau_cz)=\chi(z)+[c].
\]
Thus \(\tau_c\) fixes labels pointwise exactly when \(c\in B\), but every
translation preserves and reflects the relation. Boundary translations are
therefore exactly the pointwise-label-fixing translations, not the entire
translation group of relation automorphisms.

For a linear map \(L:A\rightarrow A\), relation preservation is equivalent to
\(L(B)\subseteq B\). For invertible \(L\), relation automorphism is equivalent
to \(L(B)=B\).

## Corrected Finite Witness

In the eight-state \(E_\star\) model, translation by \(e_2\):

- changes all eight pointwise quotient values;
- preserves all 64 ordered-pair relation tests; and
- induces the quotient permutation \([z]\mapsto[z]+[e_2]\).

It is a pointwise-label sharpness witness and a relation automorphism. It is
not a relation-changing witness.

The packet retains one stronger ambient algebraic contrast:
\[
L(e_0)=e_0,\qquad L(e_1)=e_0+e_2,\qquad L(e_2)=e_1.
\]
This map is invertible and sends the boundary generator \(e_0+e_1\) to
\(e_2\notin B\), producing 16 relation mismatches across 64 ordered pairs.
It is neither a boundary move nor an admitted chain map, and it is not
established as physically admissible.

## Surviving Conditional Core

The v1 chain-map naturality, conditional quotient-uniqueness, and finite
boundary-move pointwise robustness results remain valid under their displayed
hypotheses. Chain isomorphisms preserve and reflect the relation; general
chain maps supply forward preservation only.

Codomain gauge denotes mathematical bijective relabeling in this packet. It
does not establish a physical gauge symmetry. Chain-map naturality does not
establish physical covariance.

## Primitive Selection and Adoption

Current ontology does not derive the finite chain-package family, select its
differential, select homology as a physical discriminator, or establish
boundary moves as physically admissible variations. These remain
proposal-only source-extension burdens.

The candidate remains a `new_ontology_primitive_candidate` with
`blocked_adoption_open_continuation`. No adoption is requested. General
`EqSrc` remains undischarged, and the Distance-to-GR and metric-use ledgers are
unchanged.

## Next Route

Run one bounded fresh `smuggling-auditor@0.2.0`
`ontology-law-research-packet` against exact v2. It must audit the separate
stabilizer definitions, \(e_2\) reclassification, ambient \(L\) scope,
shared-differential primitive selection, physical-admissibility and covariance
overreads, conditional theorem scopes, and finite generalization.

Refuter stress may not bypass the fresh audit. The audit may not repair, adopt,
stress-test, or promote the candidate.

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
.venv/bin/python research_control/tasks/RT-20260718-029/artifacts/validate_eqsrc_intrinsic_discriminator_admissibility_law_candidate_v2.py --write-report --json
```

Expected status: `PASS`.
