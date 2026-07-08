<!-- authority: control -->

# P6-T01 Parent Fusion Notes

Both child execution units agree that P6-T01 should specify a relation-based
finite toy target rather than a tag-readout target.

## Consensus

- The finite source set is `S_v2 = {a,b,c}` with path relation
  `A_v2 = {{a,b},{b,c}}`.
- The response relation is induced by source graph distance and orbit class:
  `R_v2({x,y}) = d_A(x,y)`.
- The automorphism structure of the path supplies the relabeling invariance
  check.
- Removing presentation labels does not erase the source relation, so the
  induced response relation remains defined on the unlabeled path.
- `SourceReadoutCandidate_EStar_v1` is retained only as a nonadopted
  draft/control candidate placeholder in `detector_readout_status`.

## Frozen-Route Distinction

The older explicit-tag toy route failed because response components were
carried by tags. The P6-T01 target instead carries response information in the
finite source relation and its orbit structure. This is only a source
specification for a future P6-T02 construction or obstruction; it is not
adoption, `g_eff`, matter coupling, or benchmark evidence.

## Claim Boundary

The fused output does not authorize canonical ontology edit, `Det_src`
adoption, `Readout_src` adoption, detector semantics adoption, source
detector/readout semantics adoption, source-law adoption, coupling-law
adoption, matter-coupling derivation or adoption, `g_eff` construction,
stress-energy semantics, matter action, Einstein equations, benchmark
promotion, Gate Chair verdict, completed derivation, future source-extension
impossibility, or program-wide no-go conclusion.

## Next Route

The next v18 route is P6-T02: construct the finite toy response v2 model or
record a precise obstruction from this source specification.
