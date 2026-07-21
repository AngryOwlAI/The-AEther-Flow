<!-- authority: science-draft -->

# EqSrc naturality: bounded primary-literature review

Status: `draft/control`; `proposal-only`; literature basis, not project proof.

## Question and boundary

Which established results can sharpen the registered
`EQSRC-CANONICAL-SELECTION-NATURALITY-TARGET-V1`, and which steps remain new
Æther-Flow obligations? The review compares eight primary sources against the
target’s source groupoid, carrier functor, choice-space functor, natural
choice-to-relation map, and natural-selector interface.

Every literature result below retains its own hypotheses. Similarity selects
a research route only. It is not proof of the project theorem, physical
covariance, ontology authority, general EqSrc, or Distance-to-GR progress.

## Established results and exact transfer limits

### 1. Naturality is coherence across declared mappings

Eilenberg and Mac Lane formalize categories, functors, and transformations
whose components satisfy a mapping-wise naturality condition. Their opening
vector-space example also separates an objectwise isomorphism from a natural
one: a basis-dependent comparison can exist object by object while failing
coherence over the admitted maps (Eilenberg & Mac Lane, 1945).

Reusable: the project should state its selector as a natural transformation
only after defining the source objects and every admissible morphism.
Still new: the literature does not identify the Æther-Flow source category,
choice functor, relation map, or ontology derivation.

### 2. Anonymous election isolates symmetry and added resources

Angluin studies networks of locally identical processors without
network-specific identity knowledge and uses covering/indistinguishability
structure to constrain guaranteed global functions, including leader-style
choices (Angluin, 1980). Itai and Rodeh make the selector analogy explicit for
anonymous rings: deterministic unique election is unavailable under their
symmetric assumptions, whereas independent randomness and stated knowledge
support probabilistic algorithms with bounded expected costs (Itai & Rodeh,
1981).

Reusable: distinguish an invariant selector from a procedure that succeeds
only after adding names, randomness, orientation, size, or scheduling data.
Still new: a graph-cover or anonymous-process theorem is not a theorem about
the project source functor. The exact action and information boundary must be
proved before transfer.

### 3. Local slices do not imply a global natural section

Palais proves local slice structure for Lie-group actions under Cartan/proper
action hypotheses, including compact isotropy and the paper’s local-action
conditions (Palais, 1961). This is a constructive local result, not a unique
global representative theorem.

Singer proves a complementary obstruction in a specific gauge setting:
connections over the four-sphere with compact nonabelian structure group do
not admit a continuous one-per-orbit global gauge choice (Singer, 1978).

Reusable: split local existence, overlap compatibility, and global section
existence into separate proof obligations.
Still new: the project has not established a matching Lie-group action,
bundle topology, regularity class, or gauge-orbit identification. Singer’s
scoped obstruction therefore does not prove a global EqSrc no-go.

### 4. Quotient-first construction can avoid representatives

Marsden and Weinstein construct reduced symplectic structures from systems
with symmetries under their reduction hypotheses (Marsden & Weinstein, 1974).
The important structural option is quotient-first: the invariant reduced
object need not be defined by choosing a preferred member of every orbit.

Reusable: investigate whether the relation image `K(X(U))`, or a quotient by
the declared source action, carries the structure actually needed downstream.
Still new: the project must derive the action, quotient, regularity, and
relation-image uniqueness; symplectic reduction neither supplies EqSrc nor
establishes metric recovery.

### 5. Physical symmetry breaking requires state and dynamics

Goldstone, Salam, and Weinberg prove, in their quantum-field-theoretic
setting, that a continuous Lagrangian symmetry not shared by the vacuum leads
to massless spin-zero excitations under the paper’s assumptions (Goldstone et
al., 1962).

Reusable: label a broken-symmetry choice as state- and dynamics-dependent,
rather than silently calling it canonical.
Still new: current Æther-Flow ontology does not supply the required vacuum,
dynamics, or selection mechanism, and this theorem is not a source-natural
representative construction.

### 6. Canonical reconstruction uses enriched invariant data

Tannaka’s duality theorem reconstructs a bicompact noncommutative group from
the compatible total representation structure specified in the paper
(Tannaka, 1939). The reconstruction is powerful precisely because the input is
not a bare orbit set: it includes sufficiently rich representations and their
compatibilities.

Reusable: test whether a derived invariant-data functor separates the source
objects and has enough compatibility to support reconstruction.
Still new: current ontology does not provide such enriched data, and
reconstruction is not the same operation as selecting an orbit representative.

## Terminology controls

- `natural` means coherent relative to a declared category and maps; it does
  not by itself mean physically preferred or ontology-derived.
- `canonical` is always relative to supplied structure and a uniqueness or
  universal-property statement.
- `symmetry breaking` may name random operational asymmetry or a non-invariant
  physical state; those are distinct mechanisms.
- `gauge choice` requires a specified orbit space and regularity class; it is
  not automatically the project’s source-equivalence relation.
- `reconstruction` requires adequate invariant data; it is not representative
  choice from a bare quotient.

## P2 route selected

The narrowest justified next step is v21 `P2-T01`: define the source category,
admissible morphisms, and automorphism actions. That packet should expose four
separate branches for later proof:

1. natural-selector existence as a fixed-point and coherence problem;
2. relation-image uniqueness or choice irrelevance even when selectors are
   absent or nonunique;
3. local slice hypotheses, overlap/gluing, and global-section obstruction; and
4. quotient or invariant reconstruction without representative selection.

This route preserves the P1-T03 family freeze and the P1-T04 theorem target.
It neither proves the broader theorem nor changes the `source_equivalence_eqsrc`
Distance-to-GR status.

## References

Angluin, D. (1980). Local and global properties in networks of processors
(Extended abstract). In *Proceedings of the twelfth annual ACM symposium on
Theory of computing* (pp. 82–93). Association for Computing Machinery.
https://doi.org/10.1145/800141.804655

Eilenberg, S., & Mac Lane, S. (1945). General theory of natural equivalences.
*Transactions of the American Mathematical Society, 58*, 231–294.
https://doi.org/10.1090/S0002-9947-1945-0013131-6

Goldstone, J., Salam, A., & Weinberg, S. (1962). Broken symmetries. *Physical
Review, 127*(3), 965–970. https://doi.org/10.1103/PhysRev.127.965

Itai, A., & Rodeh, M. (1981). Symmetry breaking in distributive networks. In
*22nd Annual Symposium on Foundations of Computer Science* (pp. 150–158).
IEEE. https://doi.org/10.1109/SFCS.1981.41

Marsden, J. E., & Weinstein, A. (1974). Reduction of symplectic manifolds with
symmetry. *Reports on Mathematical Physics, 5*(1), 121–130.
https://doi.org/10.1016/0034-4877(74)90021-4

Palais, R. S. (1961). On the existence of slices for actions of non-compact
Lie groups. *Annals of Mathematics, 73*(2), 295–323.
https://doi.org/10.2307/1970335

Singer, I. M. (1978). Some remarks on the Gribov ambiguity. *Communications in
Mathematical Physics, 60*, 7–12. https://doi.org/10.1007/BF01609471

Tannaka, T. (1939). Über den Dualitätssatz der nichtkommutativen topologischen
Gruppen. *Tohoku Mathematical Journal, 45*, 1–12.
https://www.jstage.jst.go.jp/article/tmj1911/45/0/45_0_1/_article
