---
authority: science-audit
status: draft/control
task_id: RT-20260721-002
job_id: AJ-RT-20260721-002-001
plan_task_id: P4-T04
target_derivation_milestone: source_ontology
claim_status: proposal-only decision evidence
adoption_status: blocked_adoption_open_continuation
---

# P4-T04 comparative audit of the continuum-first and emergence-first ontology options

## Result

Neither fixed option scientifically dominates the other. Continuum-first is
the lower-risk near-term research scaffold; emergence-first is the higher-risk,
higher-explanatory-ambition branch. The baseline weighted comparison favors
continuum-first by only `0.100` on a 0–5 scale, while admissible priority
changes reverse the order. That margin is smaller than plausible scoring
uncertainty. The result is a conditional decision map, not an ontology
selection, adoption, rejection, or P4-T05 verdict.

## Authority and fixed evidence

This audit compares, but does not modify:

| Option | Fixed source | SHA-256 | Status |
|---|---|---|---|
| Continuum-first | P4-T02 premetric proposal | `7d408e527015f4e7c09df90277282c284f299fb705cbd4917a22e62ab3e0d1f8` | `draft/control`, `proposal-only` |
| Emergence-first | P4-T03 locally finite process-order proposal | `121e86bd8609863ca79fd21d1cf9b5ee855057bc5a0804927946911f1222d6f5` | `draft/control`, `proposal-only` |

P4-T02 supplies a four-dimensional smooth premetric arena, structural action,
bundle/configuration syntax, admissibility, and a structural groupoid. It does
not supply a physical metric, normalization, clocks, matter, coupling, source
dynamics, or GR recovery. P4-T03 supplies a nonempty finite or countable token
carrier, a locally finite strict partial order, and guarded finite-fragment
composition. It supplies no topology, dimension, smoothness, physical causal
order, metric, matter, dynamics, or continuum reconstruction.

## Comparison categories

The audit keeps four evidential categories separate:

- **Scientific evidence:** proved properties of the fixed artifacts and
  established external results whose hypotheses match.
- **Philosophical preference:** values assigned to primitive economy,
  explanatory ambition, and acceptable ontological debt.
- **Engineering compatibility:** near-term compatibility with the repository's
  current mathematical types and proof tooling.
- **Sunk investment:** existing artifact count or prior effort. This is excluded
  from scientific scoring and may enter resource planning only.

## Criteria scores and their meaning

Scores run from 0 to 5 and are auditable comparative judgments, not
probabilities or measurements of truth.

| Criterion | Continuum-first | Emergence-first | Audit basis |
|---|---:|---:|---|
| Assumption economy | 2.0 | 4.5 | Continuum-first openly assumes a 4D smooth arena and typed field syntax; emergence-first begins with order and local finiteness but still treats both as substantive primitives. |
| Formalization tractability | 4.5 | 2.0 | Mature smooth, bundle, and groupoid tools apply immediately to continuum-first; emergence-first must formalize several source-to-continuum layers before most current theorems are well-typed. |
| Explanatory power | 2.5 | 4.5 | Continuum-first cannot explain its arena primitives; emergence-first aims to explain them, but receives only conditional credit because no reconstruction is achieved. |
| Primary-literature maturity | 4.5 | 3.0 | Continuum reconstruction and locally covariant formalisms are theorem-rich under explicit assumptions; emergence literature supplies serious mechanisms, often conditional on faithful embedding, richer dynamics, or continuum approximation. |
| Downstream compatibility | 4.5 | 2.5 | Continuum-first can host current `M_src`/`g_eff`-shaped mathematics sooner; this is engineering compatibility only. |

With weights `(0.25, 0.20, 0.20, 0.15, 0.20)`, the totals are
`3.475` and `3.375`. The score difference is

\[
D(w)=-2.5w_A+2.5w_T-2.0w_E+1.5w_L+2.0w_D,
\]

where weights are nonnegative and sum to one. The tie surface `D(w)=0`
partitions the four-dimensional simplex of five criterion weights. Because the
difference vector has both positive and negative components, neither option
componentwise dominates the other. This is a formal result about the declared
score model, not a theorem about nature.

The independent physicist-mathematician scoring track obtained a nearby
baseline difference of `+0.125` with a different but equally mixed-sign
difference vector. Its baseline flips after moving only `0.025` weight from
downstream compatibility to assumption economy. The parent scenarios likewise
rank continuum-first under near-term delivery priorities and emergence-first
under assumption-economy/explanatory-ambition priorities. The detailed
arithmetic is recorded in the sensitivity artifact.

## Primary-literature audit

### Continuum-first evidence

Ehlers, Pirani, and Schild show how light and free-fall structures constrain
conformal and projective geometry on an already four-dimensional differentiable
event manifold. This directly supports constructive continuum axiomatics, but
not derivation of the manifold primitives or source dynamics (Ehlers et al.,
1972/2012). Hawking, King, and McCarthy and Malament establish strong links
among causal paths, topology, differentiability, and conformal structure under
continuum spacetime hypotheses. Those results show information recoverability
inside a mature spacetime setting; they do not make a bare order manifoldlike
(Hawking et al., 1976; Malament, 1977).

Connes proves a reconstruction theorem from a rich commutative spectral triple
to a compact oriented smooth Riemannian spin manifold. It demonstrates both the
power of enriched algebraic reconstruction and the strength of the assumptions
required; it is not a Lorentzian or dynamical emergence theorem (Connes, 2013).
Brunetti, Fredenhagen, and Verch formulate locally covariant quantum field
theory as functors on globally hyperbolic spacetimes. That framework is useful
for downstream matter compatibility once the background category is supplied,
not for deriving that background or AEther-Flow matter semantics (Brunetti et
al., 2003).

### Emergence-first evidence

Bombelli et al. introduce a locally finite partial order as a microscopic
spacetime proposal and analyze manifold approximation, scale-dependent
dimension, and possible dynamics. The paper establishes a serious research
programme, not the P4-T03 reconstruction or GR limit (Bombelli et al., 1987).
Rideout and Sorkin derive a family of classical stochastic sequential-growth
laws under explicit causality and covariance conditions. This shows that
source-side dynamics can be nontrivial, while leaving quantum and exact-GR
recovery open (Rideout & Sorkin, 2000).

Major, Rideout, and Surya recover continuum homology using thickened antichains
when a causal set is already faithfully embedded at sufficient density into a
globally hyperbolic spacetime. The result is a concrete conditional bridge, not
a source-internal manifoldlikeness selector (Major et al., 2007). Benincasa and
Dowker construct operators approximating the continuum d'Alembertian and
curvature term for causal sets well approximated by four-dimensional
spacetimes. Again, continuum approximation is a hypothesis rather than the
conclusion needed by P4-T03 (Benincasa & Dowker, 2010). Ambjørn, Jurkiewicz,
and Loll report numerical evidence for a macroscopic four-dimensional universe
within a specified four-dimensional causal dynamical triangulations model.
That richer model does not show that bare locally finite order selects four
dimensions (Ambjørn et al., 2004).

## Downstream compatibility and open burdens

| Downstream object | Continuum-first | Emergence-first | Shared boundary |
|---|---|---|---|
| `M_src` | A smooth carrier can type an `M_src`-like object sooner, but no authorized identification or source-to-target relation follows. | A manifold must be reconstructed and shown unique/stable before an `M_src`-like object is source-derived. | Neither option establishes physical spacetime. |
| `g_eff` | Tensor and bundle syntax is available, but the fixed normalization theorem leaves physical scale and uniqueness open. | Topology, dimension, tangent structure, measure, and scale precede a well-typed effective metric. | Neither derives a physical Lorentzian metric. |
| Matter | Bundles supply mathematical slots for fields but not matter semantics, stress energy, detectors, or universal coupling. | Stable localized sectors, observables, fields, and coupling must be reconstructed from order/process data. | Neither supplies matter or universal coupling. |
| Dynamics | Admissibility and ordered action do not define action, evolution, conservation, or physical time. | Order and finite composition do not define growth, amplitudes, measure, covariance, or typicality. | Source dynamics is absent and potentially decision-changing. |
| Formalization | Mature smooth proof tools are available; target-import auditing remains critical. | Finite combinatorics is exact at the base; limits, approximation, typicality, and reconstructed semantics require new frameworks. | No end-to-end derivation certificate exists. |
| Exact GR | The arena-reconstruction layer is shorter, but metric, clocks, matter, coupling, conservation, Einstein dynamics, and noncircular recovery remain. | All continuum reconstruction layers precede the same metric, matter, coupling, dynamics, and recovery burdens. | Exact GR remains a target benchmark, not a derived consequence. |

Source dynamics is the common decisive absence. It could reverse a ranking
based only on primitive economy, familiar mathematics, or kinematic bridge
length.

## Symmetric failure modes

Continuum-first must not receive truth credit from familiar mathematics,
shorter interface distance, or current repository compatibility. It risks
identity-by-fiat and hidden target import if the source-to-target bridge merely
renames a four-dimensional smooth manifold. Emergence-first must not receive
truth credit from primitive austerity or explanatory ambition. It risks
circular manifoldlikeness criteria, nonunique continuum realizations,
dynamically rare manifoldlike histories, and a burden-relocation move in which
deleted primitives return inside an unconstrained reconstruction law.

For both options, “current ontology does not derive X” is an open-burden
statement. It is not a theorem that X is impossible. Validation, registry
status, role authority, artifact count, and literature resemblance are not
scientific proof.

## Conditional recommendation and uncertainty

The current record supports a dual-track decision posture:

1. Treat continuum-first as a conservative comparison scaffold when the goal
   is near-term formalization and calibrated interface work. Do not treat it as
   presumptive ontology.
2. Treat emergence-first as an explanatory-stress branch with explicit
   reconstruction, uniqueness, typicality, and dynamics milestones. Do not
   treat its austerity as established fundamentality.
3. Before a strong preference, run one matched no-target-import bridge
   challenge under both options—such as constructing a scoped clock/scale or
   metric interface—and require an explicit source dynamics plus failure
   criterion for each.
4. Present criterion weights and uncertainty to the protected decision-maker,
   with repository cost separated from scientific merit.

This packet makes P4-T05 evidence-ready but does not execute it. Regime
selection, rejection, redesign, adoption, or canonical ontology change remains
human-gated. The Distance-to-GR ledger and every downstream status remain
unchanged.

## References

Ambjørn, J., Jurkiewicz, J., & Loll, R. (2004). Emergence of a 4D world from
causal quantum gravity. *Physical Review Letters, 93*(13), 131301.
https://doi.org/10.1103/PhysRevLett.93.131301

Benincasa, D. M. T., & Dowker, F. (2010). The scalar curvature of a causal
set. *Physical Review Letters, 104*(18), 181301.
https://doi.org/10.1103/PhysRevLett.104.181301

Bombelli, L., Lee, J., Meyer, D., & Sorkin, R. D. (1987). Space-time as a
causal set. *Physical Review Letters, 59*(5), 521–524.
https://doi.org/10.1103/PhysRevLett.59.521

Brunetti, R., Fredenhagen, K., & Verch, R. (2003). The generally covariant
locality principle—A new paradigm for local quantum physics. *Communications
in Mathematical Physics, 237*, 31–68. https://arxiv.org/abs/math-ph/0112041

Connes, A. (2013). On the spectral characterization of manifolds. *Journal of
Noncommutative Geometry, 7*(1), 1–82. https://doi.org/10.4171/JNCG/108

Ehlers, J., Pirani, F. A. E., & Schild, A. (2012). Republication of: The
geometry of free fall and light propagation. *General Relativity and
Gravitation, 44*, 1587–1609. https://doi.org/10.1007/s10714-012-1353-4
(Original work published 1972)

Hawking, S. W., King, A. R., & McCarthy, P. J. (1976). A new topology for
curved space-time which incorporates the causal, differential, and conformal
structures. *Journal of Mathematical Physics, 17*(2), 174–181.
https://doi.org/10.1063/1.522874

Major, S., Rideout, D., & Surya, S. (2007). On recovering continuum topology
from a causal set. *Journal of Mathematical Physics, 48*(3), 032501.
https://doi.org/10.1063/1.2435599

Malament, D. B. (1977). The class of continuous timelike curves determines the
topology of spacetime. *Journal of Mathematical Physics, 18*(7), 1399–1404.
https://doi.org/10.1063/1.523436

Rideout, D. P., & Sorkin, R. D. (2000). A classical sequential growth dynamics
for causal sets. *Physical Review D, 61*(2), 024002.
https://doi.org/10.1103/PhysRevD.61.024002
