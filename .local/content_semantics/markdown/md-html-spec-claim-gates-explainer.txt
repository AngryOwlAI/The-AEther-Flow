---
title: "Claim Gates"
purpose: "Explain how the project prevents hypotheses, candidates, workflow progress, blocked claims, and negative results from being confused with accepted physics."
audience: "Technical but human-readable: reviewers and agents who need to understand claim status before reading or producing research artifacts."
output_path: "html/claim-gates-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/RESEARCH_TASK_REGISTRY.csv"
  - ".agents/roles/physics/gate-chair.v0.1.0.md"
claim_boundary: "Human-only claim-gates visualization. It explains existing claim-boundary and negative-result preservation behavior without promoting, rejecting, or changing any scientific claim."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "claim_boundary_map"
layout_intent: "Use a claim-boundary map with state diagrams, status panels, negative-result loops, and source-backed guardrail callouts."
required_controls:
  - "section_toc"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "claim_status_ladder"
  - "gate_review_path"
  - "negative_result_preservation"
  - "forbidden_promotion_boundary"
mermaid_diagrams:
  required: true
  ids:
    - "claim-gate-state-machine"
    - "negative-result-preservation-loop"
---

# Claim Gates Spec

## Rendering Intent

Create a tracked HTML drilldown for claim gates. The page should explain how
the project separates:

- ontology framing,
- exact-GR benchmark adoption,
- candidate derivation work,
- smuggling audits,
- refutations and obstructions,
- negative-result preservation,
- Gate Chair or human-gated promotion.

The page must make it clear that workflow completion is not scientific
acceptance.

## Required Visual Structure

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Adaptive diagram fit: diagram-backed boxes must read the rendered
  SVG viewBox, set the box height from diagram aspect ratio and available
  width within bounded min/max limits, and make Fit recompute that best-fit
  geometry so horizontal diagrams do not collapse to intrinsic SVG width.
- Three-layer readability: stack the high-level, operational, and evidence
  layer sections vertically; cards inside each layer must auto-fit at a
  readable minimum width rather than nesting fixed three-column grids.
- High-level model: why claim gates exist.
- Operational model: how a candidate can remain proposed, repaired, refuted,
  blocked, preserved as a negative result, or held for human-gated review.
- Low-level evidence model: claim-boundary rows, task artifacts, TeX registry
  rows, completion records, and role authority.
- Workflow step inspector for claim states.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

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

## Source-Backed Summary

Summary heading: `Summary of Claim Gates`

Summary text:

Claim gates are the project's control mechanism for deciding when a physics
statement may move from framing, proposal, repair, audit, or explanation into
a stronger accepted status. Their role is to keep exact-GR benchmark adoption
separate from unproven substrate derivation claims by requiring source
evidence, explicit claim-boundary records, routed review, Gate Chair or human-
gated authority when needed, and registry updates before promotion. They
matter because the explainer pages and workflow artifacts can make candidate
ideas look more settled than they are; a visual explanation, completed task,
or preserved repair packet cannot by itself authorize science claims or weaken
unresolved derivation burdens. Within the project, claim gates protect both
positive progress and negative results by preserving why a route is accepted,
blocked, refuted, or still conjectural.

Summary source basis:

- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/README.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `.agents/roles/physics/gate-chair.v0.1.0.md`

## Required Content Blocks

- subject_summary: Summarize claim gates, their scientific acceptance function, why workflow completion is not claim promotion, and which declared sources ground the summary.
- claim_status_ladder: A human-readable claim-status ladder defining ontology framing, benchmark adoption, candidate, audit, repair, refutation, blocked promotion, negative result, and accepted status with source-backed examples.
- gate_review_path: A completed review-path section showing how Gate Chair or human-gated review differs from ordinary workflow validation and what evidence a promotion request would need.
- negative_result_preservation: A source-backed explanation of how obstructions, refutations, blocked promotions, failed derivations, and repair notes are preserved as research memory rather than erased.
- forbidden_promotion_boundary: A visible boundary section contrasting what generated explainers, task completions, validators, and Gate Chair decisions may say about scientific status.
