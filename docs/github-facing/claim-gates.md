<!-- authority: explanatory -->

# Claim Gates

Claim gates keep hypotheses, candidates, workflow progress, blocked claims, and negative results from being confused with accepted physics.

Authority boundary: this page explains claim-gate behavior. It does not accept, reject, promote, or weaken any physics claim.

## Claim Discipline

The project separates:

- Ontology framing.
- Exact-GR benchmark adoption.
- Candidate derivation work.
- Smuggling audits and consistency checks.
- Repairs.
- Refutations and obstructions.
- Negative-result preservation.
- Gate Chair or human-gated promotion.

Workflow completion is not scientific acceptance. A completed task can preserve a candidate, a repair, a no-go result, or a boundary clarification without making the underlying physics true.

## Claim State Sketch

<!-- mermaid-diagram-id: github-facing-claim-gates -->
```mermaid
stateDiagram-v2
  [*] --> Framing
  Framing --> Candidate: bounded proposal
  Candidate --> Audit: smuggling or consistency check
  Audit --> Repair: fixable defect
  Audit --> Refutation: defect or underdetermination
  Repair --> Candidate: revised packet
  Refutation --> NegativeResult: preserved obstruction
  Candidate --> GateReview: promotion requested
  GateReview --> Accepted: authorized gate passes
  GateReview --> Blocked: gate not passed
  Blocked --> NegativeResult
  Accepted --> [*]
  NegativeResult --> [*]
```

## Negative Results

Negative results are not noise. They preserve failed routes, blocked promotions, smuggling findings, and reproducible obstructions so future work does not replay the same failure as novelty.

The current public benchmark can remain exact GR while the first-principles substrate derivation remains open. That distinction is central to the repository.

## Source Basis

- [../../markdown/html-explainer-specs/claim-gates-explainer.md](../../markdown/html-explainer-specs/claim-gates-explainer.md)
- [../../registries/CLAIM_BOUNDARY_REGISTRY.csv](../../registries/CLAIM_BOUNDARY_REGISTRY.csv)
- [../../registries/TEX_SOURCE_REGISTRY.csv](../../registries/TEX_SOURCE_REGISTRY.csv)
- [../../research_control/README.md](../../research_control/README.md)
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)
