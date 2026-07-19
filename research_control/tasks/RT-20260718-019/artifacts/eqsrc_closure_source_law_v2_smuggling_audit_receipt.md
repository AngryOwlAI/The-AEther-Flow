# EqSrc Closure Source-Law Candidate v2 Smuggling Audit Receipt

## Result

`RT-20260718-019` independently audits proposal-only
`EqSrcClosureLaw_src^cand v2`. No explicit target or process-authority import
is detected, and the repaired accepted identity, inverse, and composition
quantifiers make the conditional equivalence proof valid. The advertised
closed source grammar is nevertheless incomplete. The result is
`closed_grammar_repair_required_before_refuter_stress`.

## Exact Finding

The declared source signature contains a proxy domain but does not declare the
proxy terms or functions used by accepted identity, inverse, and composition
witnesses. It declares only ledger congruence, while the certificate clause
refers to additional proxy, negative-outcome, and provenance congruences.
Finally, `NegPass_n` is said to use only preceding domains but is applied to a
later-defined certificate, and no acyclic dependency rule excludes a
definition through `Accept_src`.

These defects are `OBST-EQSRC-CLOSURE-SIGNATURE-001`, a scoped and repairable
obstruction to the v2 `closed_and_target_free_by_construction` claim. They do
not undo the accepted-totality repair, detect a target-GR import, establish a
global no-go theorem, or reject the theory.

## New Mathematical Payload

The audit supplies:

- a declaration-closure proof showing that `p_inv(w)` and `p_comp(v,w)` are
  not terms of the declared source language as written;
- a source-only two-fixed-point witness showing why `NegPass_n` must be
  explicitly independent of `Accept_src`; and
- a repairability model showing that the accepted-totality core is consistent
  once the missing declarations and dependency order are supplied.

## Source-Purity and Authority

No explicit target atlas, target metric, detector, benchmark, registry, role,
validator, generated derivative, handoff, checkpoint, or approval premise is
detected. Those workflow surfaces remain provenance only. Candidate-witness
acceptance is not ontology adoption.

The candidate remains `proposal-only` source-extension data with
`blocked_adoption_open_continuation`. If later offered for adoption, it would
be a new ontology primitive requiring protected human authority.

## Next Route

Run one bounded `ontology-formalizer@0.2.0` proposal-only v3 repair that:

- declares or existentially binds every proxy witness constructor;
- declares all component and certificate congruences with typed domains;
- types negative-control predicates on a displayed domain; and
- gives an acyclic acceptance dependency order excluding target data, process
  authority, and `Accept_src` recursion.

The repair must preserve the v2 accepted-totality clauses. Refuter stress
follows only after a fresh audit of the repaired specification.

## Forbidden Overreads

This receipt does not authorize canonical ontology modification, source-law
adoption, general `EqSrc` discharge, RetainH or GenH adoption, Distance-to-GR
ledger change, downstream GR progress, benchmark promotion, Gate Chair
verdict, completed derivation, future source-extension impossibility, or
global theory rejection.

## Validation

Task-local validator:

```text
.venv/bin/python research_control/tasks/RT-20260718-019/artifacts/validate_eqsrc_closure_source_law_v2_smuggling_audit.py --write-report --json
```

Expected status: `PASS`.
