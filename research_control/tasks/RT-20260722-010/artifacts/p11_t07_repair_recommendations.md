<!-- authority: control -->

# P11-T07 repair recommendations

## Disposition summary

The pilot found no blocking defect in the selector theorem or in the narrow
conditional assembly of the scoped `g_eff` source record. It did find one
task-local blind-packet omission during the first review round. The packet was
repaired in scope by adding the missing relation-image and formal-kernel
definitions, then deterministically rebuilt and re-reviewed once.

## Concrete follow-up items

1. P11-T08 should test blind packets for scientific self-containment in
   addition to process-metadata separation. The existing blind-packet builder
   correctly caught context leakage but did not know that a theorem excerpt
   named undefined objects.
2. P11-T08 should preserve the false-consensus warning: agreement between a
   blind same-model arm and a same-context role arm is useful internal review,
   not external human review or independent replication.
3. Selector-theorem documentation may later define the constant singleton
   functor explicitly and keep strict-extension, choice, relation-image, and
   bounded-formalization guards adjacent. No theorem repair is required by
   this pilot.
4. The scoped `g_eff` source record should remain draft/control. Any future
   physical-reading packet must supply exact slot types, a uniqueness or
   quotient result, derived naturality, dynamics, a source-side operational
   protocol/readout or response map, robustness evidence, and appropriately
   provenanced human-expert review or independent replication before a
   protected Gate B review can even be considered.

No recommendation edits a reviewed science source, changes a scientific
ledger, adopts an object, or authorizes physics promotion.
