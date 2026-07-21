<!-- authority: task-local blind review input -->

# Context-stripped review packet: natural selectors on a groupoid

Packet ID: `EQSRC-SELECTOR-THEOREM-BLIND-PACKET-V1`

Status: `review_input`, `draft/control`, `proposal-only`.

## Reviewer protocol

Review only the mathematical material in this packet. Do not inspect repository
history, task records, prior verdicts, validator reports, or route decisions.
Re-derive each material step and attempt a minimal countermodel under the
declared hypotheses. Report assumptions you would add, delete, or weaken.

This is a blinded internal review input. It does not claim that the reviewer is
human, external to the project, statistically independent, or an independent
replication. Reviewer provenance must be stated in the response.

## Fixed input integrity

The packet was transcribed from six fixed inputs. The labels below are opaque
for review; their SHA-256 values allow later provenance checking without
disclosing prior conclusions.

| Input | Contents | SHA-256 |
|---|---|---|
| A | theorem and proofs | `d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae` |
| B | finite countermodel atlas | `4a7c84ecf769b19e92b2b2dffd7224ddd4e1e02e4cc93cff797d01fa0e1bc62b` |
| C | bounded Lean source | `6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356` |
| D | Lean build receipt | `a37add9b420c502a344401ba2ad36737ff70add99fa114272735aae8e4f834d3` |
| E | semantic audit source | `d093d7b0afbe322cf537644de54f17156ea2427fcc0988f4fc8fb305e93a0f76` |
| F | altered-domain stress source | `d519bcc9534af3b2ca3e3d44604bd56bf72c425e0d06322c33cc7e66abfd2b49` |

No prior verdict, route status, validator status, or internal confidence score
is included below.

## Objects and notation

Let \(\mathcal G\) be a small groupoid and let
\(S:\mathcal G\to\mathbf{Set}\) be a covariant functor. Let
\(I=\pi_0(\mathcal G)\) be a set. For each \(i\in I\), supply a representative
\(r_i\), and for each object \(X\) in component \(i=[X]\), supply an
isomorphism \(\tau_X:r_i\to X\) with \(\tau_{r_i}=1_{r_i}\).

Define

\[
H_i:=\operatorname{Aut}_{\mathcal G}(r_i),\qquad
F_i:=S(r_i)^{H_i},\qquad
\operatorname{Sel}(\mathcal G):=\operatorname{Nat}(1_{\mathcal G},S).
\]

When relation images are discussed, additionally supply a functor
\(E:\mathcal G\to\mathbf{Set}\) and a natural transformation
\(K:S\Rightarrow E\). Define

\[
K_*:\operatorname{Sel}(\mathcal G)\to
\operatorname{Nat}(1_{\mathcal G},E),\qquad K_*(\sigma)=K\circ\sigma,
\]

and \(R_i:=K_{r_i}(F_i)\).

## Declared assumptions

1. `A01`: \(\mathcal G\) is the fixed small wide certified-isomorphism core.
2. `A02`: \(S\) is the fixed covariant eligible-choice functor.
3. `A03`: \(I\) is a set and the representatives and transports above are
   supplied as proof coordinates. They are not source marks.
4. `A04`: For a converse from factorwise nonemptiness to global existence,
   \(I\) is finite, a product tuple is supplied, or a suitable choice principle
   is explicitly assumed.
5. `A05`: Relation-image claims additionally assume the functor \(E\) and
   natural transformation \(K\).
6. `A06`: Full-category claims additionally assume a specified functor
   extension over every noninvertible arrow.
7. `A07`: A selector is deterministic, total on the declared domain, and
   point-valued.
8. `A08`: Objects, arrows, eligibility, actions, and \(K\) are fixed before
   selector existence or uniqueness is evaluated.
9. `A09`: Automorphisms are structural symmetries of the proposal signature;
   no physical-gauge interpretation is assumed.
10. `A10`: The category, functor, \(K\), selector, proof coordinates, and any
    source extension are proposal inputs rather than ontology-derived objects.

## Claim 1: certified-core selector classification

Evaluation at component representatives is claimed to be a bijection

\[
\operatorname{ev}:\operatorname{Sel}(\mathcal G)
\xrightarrow{\cong}\prod_{i\in I}F_i,
\qquad \sigma\mapsto(\sigma_{r_i})_{i\in I}.
\]

The claimed inverse sends a tuple \(x=(x_i)\) to

\[
\sigma^x_X:=S(\tau_X)(x_{[X]}).
\]

The stated consequences are:

1. \(\operatorname{Sel}(\mathcal G)=\varnothing\) iff
   \(\prod_iF_i=\varnothing\).
2. Any empty factor \(F_i\) obstructs a global selector.
3. If every factor is nonempty, a selector exists exactly when a product
   element is available. Finite \(I\), a supplied tuple, or a suitable choice
   principle is sufficient.
4. The selector set is a singleton iff every \(F_i\) is a singleton.
5. It has at least two elements iff some \(F_i\) has at least two elements and
   the complementary product \(\prod_{j\ne i}F_j\) is nonempty.

### Proof supplied for Claim 1

If \(\sigma:1_{\mathcal G}\Rightarrow S\) is natural and \(h\in H_i\),
naturality at \(h:r_i\to r_i\) gives
\(S(h)(\sigma_{r_i})=\sigma_{r_i}\), so evaluation lands in the product.

Conversely, for \(x\in\prod_iF_i\), define \(\sigma^x\) by the formula above.
For \(f:X\to Y\) in the groupoid, let
\(a=\tau_Y^{-1}f\tau_X\in H_i\). Then

\[
S(f)\sigma^x_X=S(f\tau_X)x_i
=S(\tau_Ya)x_i=S(\tau_Y)x_i=\sigma^x_Y.
\]

At representatives, identity transports recover \(x_i\). Conversely,
naturality of \(\sigma\) at \(\tau_X\) gives
\(\sigma_X=S(\tau_X)(\sigma_{r_i})\). Thus the two constructions are inverse.
The cardinality consequences are then obtained by coordinate replacement,
with the stated product-choice qualification.

## Claim 2: relation-image uniqueness

Assume \(\operatorname{Sel}(\mathcal G)\ne\varnothing\). The claim is

\[
|\operatorname{im}K_*|=1
\quad\Longleftrightarrow\quad
\text{every }R_i\text{ is a singleton}.
\]

If two points of one \(F_i\) have distinct \(K_{r_i}\)-images, then two
global selectors induce different natural relation sections, provided a
baseline global selector supplies all complementary coordinates. If each
\(R_i\) is a singleton, selector multiplicity is relation-level choice
irrelevance rather than relation nonuniqueness.

### Proof supplied for Claim 2

Naturality of \(K\) and \(\sigma\) makes their composite natural. Fix one
global selector as a baseline. If every \(R_i\) is a singleton, any two
selector tuples have identical \(K\)-images at representatives and therefore
at all objects. Conversely, replace the \(i\)-coordinate of the baseline tuple
by a second point with different \(K_{r_i}\)-image and reconstruct the two
selectors using Claim 1.

The claim does not assert \(\operatorname{im}K_*=\prod_iR_i\) for an arbitrary
infinite family without simultaneous fibre choices. It does not assert that
every natural section of \(E\) lies in the image. When the selector set is
empty, its image is empty rather than uniquely selected.

## Claim 3: full-category equalizer guard

Conditionally assume that \(S\) extends to a functor
\(\overline S:\mathcal C\to\mathbf{Set}\) on a category whose wide core is
\(\mathcal G\). Restriction is claimed to be injective and to identify
\(\operatorname{Nat}(1_{\mathcal C},\overline S)\) with the tuples in
\(\prod_iF_i\) satisfying

\[
\overline S(f)\bigl(S(\tau_X)x_{[X]}\bigr)
=S(\tau_Y)x_{[Y]}
\]

for every arrow \(f:X\to Y\) of \(\mathcal C\), including noninvertible
arrows. The supplied proof uses wideness for injectivity, Claim 1 for the core
coordinates, and the displayed equations as exactly the remaining naturality
conditions.

## Bounded formalization evidence

A Lean 4 core-only capsule encodes only the one-object finite-group fragment:
group actions, fixed points, invariant point selectors, empty-fixed and
multiple-fixed implications, the transitive-action obstruction, one two-point
swap example, and one trivial-action multiple-fixed control. It does not encode
the multi-component product classification, arbitrary choice qualification,
\(K_*\), full-category equalizers, ontology derivation, or physical meaning.

Reviewers should treat the formalization as a translation of this bounded
fragment, not as independent validation of the full theorem package.

## Raw boundary cases

The following data are supplied without a verdict.

1. A Klein-four action on \(\{0,1\}\) has two group elements acting trivially
   and two acting by swap. Its action kernel is the trivial-action pair. Both
   the full action and the faithful quotient have empty fixed locus.
2. A partial map with domain \(\{0\}\) sends \(0\mapsto1\) on carrier
   \(\{0,1\}\). It is not a total set map and has no groupoid inverse.
3. Finite component factor profiles \((2,0)\) and \((2,1)\) have Cartesian
   product sizes \(0\) and \(2\), respectively.
4. The cyclic three-point action \(0\mapsto1\mapsto2\mapsto0\) has no fixed
   point and has invariant probability vector \((1/3,1/3,1/3)\).
5. A two-point swap has empty fixed locus. After adding a mark at \(0\) and
   restricting to mark-preserving automorphisms, the eligible singleton
   \(\{0\}\) is fixed.
6. For the two-point swap group \(G\) and identity subgroup \(H\),
   \(D^G=\varnothing\), \(D^H=D\), and generally \(D^G\subseteq D^H\) when
   \(H\subseteq G\).

## Required review questions

1. Are all objects and natural transformations well typed?
2. Is the classification proof correct without silently assuming connectedness
   or a global choice function?
3. Are the uniqueness and nonuniqueness iff-statements exactly quantified?
4. Does Claim 2 distinguish selector multiplicity from relation-section
   multiplicity and preserve its baseline-selector requirement?
5. Does Claim 3 characterize the full-category naturality equalizer without
   presupposing an extension that has not been supplied?
6. Do any definitions or proof steps import target topology, a target metric,
   physical-gauge semantics, empirical detector semantics, or desired benchmark
   behavior?
7. Are any notation pairs overloaded, especially raw \(K(D)\),
   \(\operatorname{im}K_*\), an action kernel, and an individual element's
   stabilizer?
8. Can a minimal countermodel be found while retaining every declared
   assumption and the deterministic total point-valued selector codomain?
9. Which conclusions fail when the codomain becomes probabilistic, the arrows
   become partial, source marks are added, or the admitted variation group is
   changed?
10. What is the narrowest defensible verdict and next route?

## Explicit nonclaims

No material in this packet establishes ontology adoption, a source-law or
selector-law adoption, physical gauge or covariance, a general `EqSrc`
derivation, `M_src`, `g_eff`, matter coupling, Einstein equations, exact-GR
recovery, benchmark promotion, a Gate Chair verdict, publication authority,
global theory rejection, future source-extension impossibility, or completed
derivation. A clean review or validator result would not create those claims.

## Response contract

Return strict YAML. Include:

- reviewer provenance: model family, human status, context inheritance, files
  accessed, declared conflicts, and independence limitations;
- assumptions read, definitions read, and proof steps checked;
- circularity, hidden-import, notation-overload, and unproven-equivalence
  findings, using empty lists when none are found;
- one minimal-countermodel attempt;
- assumption deltas and scope-overread findings;
- one verdict from the active external-red-team vocabulary;
- one recommended next route; and
- `physics_promotion_authorized: false`.
