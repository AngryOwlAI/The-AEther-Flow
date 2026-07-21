<!-- authority: task-local proof receipt -->

# P2-T05 EqSrc selector formal-proof receipt

Task `RT-20260720-018`, AgentJob `AJ-RT-20260720-018-001`, completed only
v21 work item `P2-T05` under `ontology-formalizer@0.2.0`.

## Result

The task-local Lean 4 source machine-checks six named results over explicitly
declared minimal group and action structures:

1. empty fixed locus iff no invariant selector;
2. uniqueness of a fixed choice under transitivity;
3. no invariant selector for a transitive action with two distinct choices;
4. two distinct fixed choices give two distinct selectors;
5. the preserved `FX-RESP-XEMPTY-SIGN-SWAP` C2 countermodel has no selector;
6. the trivial two-choice action has multiple selectors.

This is the bounded finite-group theorem core requested by P2-T05. The full
P2-T03 connected-component product classification, relation-image theorem,
and noninvertible-arrow equalizer guard are not claimed as mechanized here.

## Reproducibility evidence

- Official tool: Lean 4.30.0, release commit
  `d024af099ca4bf2c86f649261ebf59565dc8c622`.
- Official macOS ARM64 archive SHA-256, published and observed:
  `072dca4a38fbc0d3cedb96fea886cc243b424f2bd16247596200b9a9ab93f0f5`.
- Tracked source SHA-256:
  `6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356`.
- Two independent empty-output builds produced byte-identical `.olean` files.
- Proof-object SHA-256:
  `3fff7e0bff2e331400ba52305a2f34e3deb93f2b85ac1e3850a1625ef6bd468a`.
- The only reported dependency is Lean core `Init.olean`.
- Six `#print axioms` reports each state that the named theorem does not
  depend on any axioms.
- The source contains no `sorry`, `admit`, custom `axiom`, or unsafe
  declaration.

## Source identity

- P2-T03 theorem SHA-256:
  `d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae`.
- P2-T04 fixtures SHA-256:
  `e8ced96541fa941e5a3b4ceaa8d7b48204acf7ca8ec342ac6b23dbbf5c470a73`.
- Historical fixture identity preserved exactly:
  `FX-RESP-XEMPTY-SIGN-SWAP`.

## Claim boundary

The result is `draft/control` and `proposal-only` mathematical support.
Machine checking does not show that current ontology derives or adopts the
encoded domain or selector, does not make structural automorphisms physical
gauge, does not independently audit translation fidelity, does not discharge
general EqSrc, and does not change the Distance-to-GR or metric-use ledgers.
P2-T06 retains independent Smuggling Auditor ownership and P2-T07 retains
independent Refuter ownership. No promotion, publication, Gate Chair verdict,
or completed derivation is authorized.

## Reference

Lean FRO. (2026). *Lean 4.30.0* [Computer software]. GitHub.
https://github.com/leanprover/lean4/releases/tag/v4.30.0
