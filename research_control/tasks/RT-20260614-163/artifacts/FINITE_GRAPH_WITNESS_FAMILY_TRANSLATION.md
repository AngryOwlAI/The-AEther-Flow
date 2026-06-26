# Finite Graph Witness-Family Translation

This support artifact translates the `RT-20260614-163` chain-family candidate
into finite directed graph language. It is not proof authority. The TeX
artifact controls mathematical claims.

| Source-side term | Graph-theoretic translation | Claim limit |
| --- | --- | --- |
| source package `E` | finite directed graph plus marked source structure | not target topology |
| response token | directed edge or generated reachability relation | not physical propagation by itself |
| reachability preorder `R_C` | transitive closure preorder | not target causal cone |
| transition token `K_tau` | structure-preserving graph isomorphism or admitted relabeling | not atlas covariance |
| distinguishability `D_N` | node-profile invariant | not Lorentzian nondegeneracy |
| finite variation `V_ML` | bounded graph edit with repair-or-bottom behavior | not variational dynamics |
| bottom table `B_src` | named failure map | not metric construction |

For the chain family `E_n`, the graph has vertices `0,...,n` and directed
edges `(i, i+1)` for `0 <= i < n`. Reachability profiles omit identities and
therefore give node `i` the profile `(n-i, i)`.

For the diamond pressure package with edges `(0,1)`, `(0,2)`, `(1,3)`,
`(2,3)`, the middle vertices have identical profiles `(1,1)`. This supports
the TeX limitation: the simple chain-family profile schema is not an arbitrary
finite-DAG witness theorem.
