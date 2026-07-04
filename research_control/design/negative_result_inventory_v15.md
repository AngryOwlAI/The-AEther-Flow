<!-- authority: control -->

# Negative Result Inventory v15

Status: `draft/control`

Purpose: record frozen, obstructed, or failed routes as reusable research outputs without turning scoped failures into program-wide no-go claims.

## Inventory

```yaml
negative_results:
  - negative_result_id: "NR-V15-FINITE-TOY-METRIC-RESPONSE-FROZEN-001"
    source_artifact_path: "research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex"
    scope: "finite toy metric-response route with explicit tags under tag-removal and equivariant-totalization stress"
    failed_claim: "explicit-tag-only finite toy route supplies a reusable source-to-response metric analogue after tag erasure"
    minimal_countermodel: "tag-removal stress collapses the response relation for the finite toy route"
    what_it_blocks:
      - "reuse of the explicit-tag-only finite toy route as written"
      - "g_eff scope expansion from this toy route"
      - "matter-coupling, Einstein-equation, benchmark, or completed-derivation claims from this toy route"
    what_it_does_not_block:
      - "redesigned finite toy routes"
      - "future source-extension candidates"
      - "the research program as a whole"
    future_source_extension_impossibility_authorized: false
    global_theory_rejection_authorized: false
    allowed_reuse:
      - "negative-control obstruction"
      - "support-only formalization target"
      - "public-safe example of local route freeze"
    blocked_reuse:
      - "global no-go theorem"
      - "future source-extension impossibility"
      - "downstream GR derivation blocker beyond the stated local route"

  - negative_result_id: "NR-V15-RESP-LC-OLD-TUPLE-SELECTOR-OBSTRUCTION-001"
    source_artifact_path: "registries/DISTANCE_TO_GR_LEDGER.csv#resp_lc"
    scope: "old S_X / response-selector tuple route for Resp_lc sign, scale, and token semantics"
    failed_claim: "old tuple selector supplies downstream detector semantics, matter coupling, or completed response localization"
    minimal_countermodel: "none recorded as finite countermodel; obstruction is the still-valid selector-data gap noted in the Resp_lc ledger row"
    what_it_blocks:
      - "old selector route as matter-coupling support"
      - "detector-semantics or matter-coupling overreads from Resp_lc scoped source-extension evidence"
    what_it_does_not_block:
      - "accepted scoped Resp_lc source-extension data"
      - "same-milestone continuation through S_X^+"
      - "future source-side response selector laws"
    future_source_extension_impossibility_authorized: false
    global_theory_rejection_authorized: false
    allowed_reuse:
      - "Resp_lc status-boundary example"
      - "negative-control entry for public-safe scoped wording"
    blocked_reuse:
      - "detector semantics"
      - "matter coupling"
      - "program-wide no-go claim"

  - negative_result_id: "NR-V15-RR-E-UNDERDETERMINATION-001"
    source_artifact_path: "research_control/tasks/RT-20260701-023/artifacts/rr_e_irrelevance_theorem_attempt_or_obstruction_v1.tex"
    scope: "current-ontology RR_E theorem route under missing transport-completeness or invariance law"
    failed_claim: "current ontology derives unrestricted RR_E irrelevance theorem"
    minimal_countermodel: "finite separation witness is recorded separately as NR-V15-RR-E-FINITE-SEPARATION-WITNESS-001"
    what_it_blocks:
      - "unrestricted RR_E theorem under current premises"
      - "RR_E theorem as detector semantics or matter coupling"
    what_it_does_not_block:
      - "conservative source-side extension"
      - "certificate-indexed scoped evidence/precondition routes"
      - "future RR_E transport or invariance law proposals"
    future_source_extension_impossibility_authorized: false
    global_theory_rejection_authorized: false
    allowed_reuse:
      - "reason for ontology-law-research-packet routing"
      - "scoped obstruction language example"
    blocked_reuse:
      - "future source-extension impossibility"
      - "program-wide rejection overread"
      - "detector-semantics collapse"

  - negative_result_id: "NR-V15-RR-E-FINITE-SEPARATION-WITNESS-001"
    source_artifact_path: "research_control/tasks/RT-20260701-025/artifacts/rr_e_theorem_refuter_stress_v1.tex"
    scope: "finite two-record RR_E separation witness under the RR_E theorem stress route"
    failed_claim: "current evidence collapses finite RR_E separation into an unrestricted theorem"
    minimal_countermodel: "finite two-record separation witness"
    what_it_blocks:
      - "erasing RR_E separation without explicit source certificates"
      - "using the witness as matter coupling, detector semantics, or benchmark proof"
    what_it_does_not_block:
      - "future certificate-indexed RR_E transport, invariance, or factorization routes"
      - "scoped evidence/precondition status"
    future_source_extension_impossibility_authorized: false
    global_theory_rejection_authorized: false
    allowed_reuse:
      - "negative-control witness"
      - "claim-language linter example"
      - "support-only formalization boundary input"
    blocked_reuse:
      - "global impossibility"
      - "matter coupling"
      - "benchmark promotion"

  - negative_result_id: "NR-V15-P2-CERTIFICATE-GAP-WITNESS-001"
    source_artifact_path: "research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex"
    scope: "NarrowMSCertEq_v1 under missing or malformed explicit source certificates"
    failed_claim: "source-side matter-semantics equivalence theorem holds without explicit valid source transport, invariance, factorization, and no-target certificates"
    minimal_countermodel: "MC-NARROW-MS-CERT-EQ-CERT-GAP-001"
    what_it_blocks:
      - "unconditional theorem reading"
      - "scoped evidence as matter-semantics adoption"
      - "certificate-free matter-coupling derivation"
    what_it_does_not_block:
      - "conditional theorem under explicit valid certificates"
      - "future certificate construction"
      - "scoped Gate Chair evidence-status already recorded for the theorem"
    future_source_extension_impossibility_authorized: false
    global_theory_rejection_authorized: false
    allowed_reuse:
      - "minimal certificate-gap witness"
      - "source-certificate checklist example"
      - "red-team review target"
    blocked_reuse:
      - "global no-go"
      - "matter semantics adoption"
      - "matter-coupling derivation"
```

## Route-Orbit Note

P10 did not trigger a route-orbit freeze. No P17-T01 negative-result entry is created for a route-orbit freeze because the condition is absent in the tracked P10 handoffs. The route-orbit policy remains useful as process control, not as a scientific negative result.

## Claim Boundary

Every entry is scoped. No entry authorizes future source-extension impossibility, global theory rejection, benchmark promotion, or completed derivation. Source artifacts remain the authority.

## References

The AEther-Flow Research Project. (2026a). *Frontier theorem inventory* [Control inventory]. `research_control/design/frontier_theorem_inventory.md`.

The AEther-Flow Research Project. (2026b). *Distance-to-GR ledger* [Control registry]. `registries/DISTANCE_TO_GR_LEDGER.csv`.

The AEther-Flow Research Project. (2026c). *Matter-semantics equivalence theorem Refuter stress v1* [Research-control TeX artifact]. `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex`.
