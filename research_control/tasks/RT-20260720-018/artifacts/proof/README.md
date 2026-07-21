<!-- authority: task-local build instructions -->

# P2-T05 selector-kernel Lean build

Status: draft/control, proposal-only mathematical support.

This capsule checks only the finite-group core of
`EQSRC-NO-NATURAL-SELECTOR-NONUNIQUENESS-THEOREM-V1`. It defines group
actions, fixed points, invariant selectors, the empty-fixed and
multiple-fixed implications, the transitive-action obstruction, the preserved
`FX-RESP-XEMPTY-SIGN-SWAP` historical countermodel, and a trivial-action
multiple-fixed control.

The capsule has no package dependency beyond the Lean 4 core distribution.
The exact toolchain and official macOS ARM64 release archive are pinned in
`lean-toolchain` and `toolchain-lock.json`.

## Clean build

1. Obtain Lean 4.30.0 from the official release named in the lock file and
   verify the archive SHA-256 before extraction.
2. Create a new empty output directory outside the tracked task tree.
3. Run:

   ```sh
   sh build_proof.sh /absolute/path/to/lean /absolute/path/to/empty-output-dir
   ```

The build writes `SelectorKernel.olean`, the Lean version, dependency list,
kernel output including every `#print axioms` report, and SHA-256 files for the
source and proof object into the supplied output directory. The tracked source
must contain no `sorry`, `admit`, custom `axiom`, or unsafe declaration.

## Claim boundary

Kernel checking establishes only that the encoded propositions follow in
Lean from the declared definitions and hypotheses. It does not establish that
current ontology derives or adopts the proposal domain or selector, that a
structural automorphism is physical gauge, that the P2-T03 translation is
independently audited, or that general EqSrc or any downstream GR burden is
discharged.

## Reference

Lean FRO. (2026). *Lean 4.30.0* [Computer software]. GitHub.
https://github.com/leanprover/lean4/releases/tag/v4.30.0
