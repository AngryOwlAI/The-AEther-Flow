# Claim Gates

This page explains how the project prevents ontology framing, exact-GR benchmark adoption, candidate derivation work, workflow completion, and accepted science claims from being confused.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/claim-gates-explainer.md`
- **Related HTML:** `html/claim-gates-explainer.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

Claim gates define the status ladder from ontology framing through benchmark adoption, candidate derivation, audit, repair, refutation, blocked promotion, negative result, and accepted claim.

## Why The Project Needs It

Speculative physics work can sound complete before it is mathematically established. Claim gates protect the project by requiring source evidence, boundary rows, authorized review, and negative-result preservation before a statement can be strengthened.

## How It Works

Status ladder:

| Status | May say | Must not say |
| --- | --- | --- |
| Ontology framing | conceptual vocabulary guides interpretation | the substrate is established physics |
| Benchmark adoption | ordinary exact GR is the observable benchmark | GR has been derived from the substrate |
| Candidate derivation | a bounded construction is proposed | promotion is automatic |
| Audit or repair | defects are being checked or fixed | validation equals acceptance |
| Refutation or blocked promotion | an obstruction or gate failure is preserved | the failure disappears because a task closed |
| Negative result | the route should not be replayed blindly | global theory rejection unless authorized |
| Accepted claim | a gate-authorized claim may be cited | authority beyond the recorded scope |

## What It Is Not

It is not a validator-only process, not a visual badge, not a way for generated explainers to promote claims, and not a replacement for Gate Chair or human-gated authority when required.

## Diagram Reading Guide

The state diagram distinguishes candidate, audit, repair, refutation, gate review, accepted, blocked, and negative-result states. The preservation loop shows why a failed route becomes memory rather than being erased.

<!-- mermaid-diagram-id: claim-gate-state-machine -->
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

<!-- mermaid-diagram-id: negative-result-preservation-loop -->
```mermaid
flowchart TD
  Attempt["Candidate derivation attempt"] --> Test["Refutation or smuggling test"]
  Test --> Finding["Obstruction identified"]
  Finding --> Boundary["Claim-boundary row"]
  Boundary --> Artifact["Registered task artifact"]
  Artifact --> Handoff["Handoff preserves next state"]
  Handoff --> Future["Future work avoids replaying failure"]
  Future --> Attempt
```

## Source Authority

The claim-boundary registry, research-control README, TeX registry, research task registry, and Gate Chair role contract provide the evidence. This page summarizes their function without changing claim status.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Read this page before using words such as derived, accepted, blocked, or refuted.
- Inspect `registries/CLAIM_BOUNDARY_REGISTRY.csv` for task-specific boundaries.
- Inspect registered TeX before citing scientific status.
- Preserve negative results rather than deleting failed routes.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `.agents/roles/physics/gate-chair.v0.1.0.md`
