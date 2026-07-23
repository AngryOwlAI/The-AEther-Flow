<!-- authority: control -->

# handoff-0841 — Content-address recovery passed; role-registry parity blocks checkpoint

`RT-20260723-008` completed the intended generation-75 content-address
recovery:

- one stale P10-T05 source binding now equals the current governed
  metrics-consumer SHA-256;
- the two P10-T05 deterministic receipts and exactly three current P10-T07
  identity outputs have zero drift;
- both historical `e22b…` and `cc7d…` content copies remain byte-identical;
  and
- event-store activation, policy, validator semantics, metric semantics, and
  scientific authority remain unchanged.

The architecture, identity, migration-readiness, cumulative P12-T05,
documentation, memory, claim-language, and working-tree research-control gates
passed. The single normal checkpoint then committed nothing because staged
research-control validation found one punctuation-only mismatch between the
RT-008 execution-role `authority_delta_summary` and
`ROLE_EXECUTION_REGISTRY.csv`. The checkpoint restored the entry index. It was
not retried, and legacy validation was not used.

The next bounded route remains P12-T05 through `improve-project-system`:
reconcile only that exact role-registry parity defect without changing
authority semantics, preserve the completed content-address repair, and invoke
at most one future normal checkpoint. P12-T06 remains blocked until a
checkpoint commits.

This handoff does not authorize a generation-75 checkpoint retry, legacy
validation, authority-semantics changes, P10-T05 or P10-T07 repair-output
rewrites, P12-T06 execution, event-store activation, private-data disclosure,
ontology adoption, scientific-ledger changes, physics promotion, proof
authority, publication, a completed substrate derivation, or a global no-go.
