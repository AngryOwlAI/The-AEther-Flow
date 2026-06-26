# Rooted Tail-Branch Graph Translation

This support artifact translates the `RT-20260614-167` rooted tail-branch
candidate into finite directed graph language. It is not proof authority. The
TeX artifact controls mathematical claims.

| Source-side term | Graph-theoretic translation | Claim limit |
| --- | --- | --- |
| source package `B_n` | finite directed rooted tail-branch graph | not target topology |
| response token | directed edge or generated reachability relation | not physical propagation by itself |
| reachability preorder `R_C` | transitive closure preorder | not target causal cone |
| transition token `K_tau` | structure-preserving graph isomorphism or admitted relabeling | not atlas covariance |
| distinguishability `D_N` | strict reachability profile invariant | not Lorentzian nondegeneracy |
| finite variation `V_ML` | bounded graph edit with repair-or-bottom behavior | not variational dynamics |
| bottom table `B_src` | named failure map | not metric construction |

For the rooted tail-branch family `B_n`, `n >= 2`, the graph has vertices
`r`, `y`, and `x_1,...,x_n`. The directed source edges are `r -> x_1`,
`x_i -> x_{i+1}` for `1 <= i < n`, and `r -> y`. Reachability profiles omit
identities and therefore give:

```text
p(r) = (n+1, 0)
p(x_i) = (n-i, i)
p(y) = (0, 1)
```

For `n >= 2`, these profiles distinguish all declared sites. This supports
the TeX construction only for the declared rooted tail-branch family.

For the diamond pressure package with edges `(0,1)`, `(0,2)`, `(1,3)`,
`(2,3)`, the middle vertices still have identical profiles `(1,1)`. That
pressure remains a guard against arbitrary finite-DAG overread.
