<!-- authority: control -->

# V21 terminal scientific baseline freeze policy

Status: internal release-control policy for the immutable baseline at
`233e5dd7024fc068032d0afe86d85dc25e2246e9` / tree `a7d9c9448de8e204643b093878ba4d84bd58f020`. This policy does not create a
Git tag, public release, publication decision, scientific promotion, or
permission for outward action.

## Frozen lineage

The original terminal commit, tree, release manifest, archive, and receipts
remain immutable. A later correction must never rewrite, replace, amend, or
silently regenerate the frozen baseline under the same identity.

## Only qualifying exception

A baseline-lineage change may be proposed only for a demonstrated security or
reproducibility defect. Scientific disagreement, revised interpretation,
new evidence, prose preference, formatting drift, convenience, or a desired
positive result is not a freeze exception.

A qualifying repair requires all of the following:

1. a tracked defect record with exact affected paths and hashes;
2. reproducible evidence of the security or reproducibility defect;
3. a distinct superseding release record with a new identity and manifest;
4. an explicit mapping from every changed byte to the defect;
5. preservation of the original baseline and its negative scientific status;
6. the normal governed validation and checkpoint transaction; and
7. separate human authority before any tag or public-release execution.

The superseding record may state that it repairs a defect. It may not imply
that V21 derived GR, passed a benchmark, acquired independent replication,
completed external review, or gained publication authority.
