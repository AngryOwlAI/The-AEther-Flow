# EqSrc Intrinsic Discriminator v2 Smuggling Audit Receipt

## Result

`RT-20260718-030` independently audits exact proposal-only
`EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v2`.

The exact result is
`source_pure_as_written_with_precise_repairable_chain_map_reflection_scope_obstruction`.
No explicit target or process-authority premise is detected. The
quotient-factorization, translation-classification, linear-stabilizer,
corrected \(e_2\), ambient-\(L\), and forward naturality results survive within
their stated hypotheses.

## Exact Obstruction

`OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001` records a local
typing and claim-scope defect.

For a typed chain map \(F:E\to E'\), relation reflection is equivalent to
injectivity of
\[
H_1(F):H_1(E)\longrightarrow H_1(E').
\]
The candidate states this correct criterion through quotient factorization,
but its fail-closed item 5 rejects reflection whenever the chain map itself is
noninvertible. Invertibility is sufficient, not necessary.

The candidate also defines its relation predicates only for endomaps of one
\(A_E\), while its naturality proposition uses \(F_1:A_E\to A_{E'}\). The
intended theorem needs explicit cross-complex preservation and reflection
predicates.

## Minimal Counterexample

Let
\[
C_2=\mathbb F_2\langle f\rangle,\quad
C_1=\mathbb F_2\langle a,b\rangle,\quad C_0=0,\qquad
\partial_2f=a.
\]
Define \(F_2=0\), \(F_1(a)=0\), and \(F_1(b)=b\). This is a noninvertible
self-chain-map. Its induced map on
\(H_1=C_1/\langle a\rangle\) is the identity, so it preserves and reflects the
candidate relation. Exhaustive enumeration gives zero mismatches across all
16 ordered pairs.

## New Mathematical Payload

The audit supplies:

- the exact induced-\(H_1\) injectivity criterion for cross-complex relation
  reflection;
- a four-state noninvertible reflecting chain-map counterexample;
- a census of all 512 \(E_\star\) linear endomorphisms: 128 preserve the
  relation, 168 are invertible, and 24 are invertible relation automorphisms;
  and
- the mismatch formula \(2q^n(q^k-q^r)\) for invertible linear maps, which
  specializes to 16 for the displayed ambient \(L\).

These results audit the candidate. They do not repair it.

## Primitive Selection and Physical Scope

Once a finite chain package is supplied, its cycles, boundaries, homology,
quotient map, and kernel pair are standard derived objects. Current ontology
does not select the chain-package family, its differential, or boundary moves
as physically admissible variations.

Both the quotient kernel and admitted moves depend on the same supplied
differential. This shared root is mathematically transparent, but formal
non-reference does not establish independent physical selection or
admissibility.

Chain-map naturality is not physical covariance. Codomain relabeling is not an
adopted physical gauge. The finite witnesses do not establish ontology-wide,
continuous, empirical, or exact-GR applicability.

## Source-Extension Classification

The packet remains a `proposal-only` `new_ontology_primitive_candidate` with
`blocked_adoption_open_continuation`. No source-law or canonical-ontology
adoption is requested.

The Distance-to-GR and metric-use ledgers are unchanged.

## Next Route

Run one bounded `ontology-formalizer@0.2.0`
`ontology-law-research-packet` to:

1. define typed cross-complex relation preservation and reflection;
2. replace the noninvertibility fail-closed rule with injectivity of the
   induced \(H_1\) map; and
3. retain chain isomorphism as a sufficient, not necessary, condition.

A fresh Smuggling Auditor review must precede Refuter stress. The repair may
not adopt or promote the candidate.

## Forbidden Overreads

This receipt does not authorize canonical ontology modification, candidate
repair inside the completed audit, source-law adoption, physical
admissibility, physical covariance, general `EqSrc`, RetainH, GenH, or
\(M_{\rm src}\) adoption, \(g_{\rm eff}\), matter coupling, Einstein
equations, unrestricted robustness, Distance-to-GR or metric-use ledger
change, benchmark promotion, Gate Chair verdict, completed derivation, future
source-extension impossibility, program-level no-go, or global theory
rejection.

## Validation

Task-local validator:

```text
.venv/bin/python research_control/tasks/RT-20260718-030/artifacts/validate_eqsrc_intrinsic_discriminator_admissibility_law_v2_smuggling_audit.py --write-report --json
```

Expected status: `PASS`.
