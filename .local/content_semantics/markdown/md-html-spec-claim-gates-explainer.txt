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
  - "expandable_analysis_panels"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "claim_status_ladder"
  - "gate_review_path"
  - "negative_result_preservation"
  - "forbidden_promotion_boundary"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
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

- subject_summary: Summarize claim gates, their claim-status protection function, why they matter before accepting explanatory or derivational claims, and which declared sources ground the summary.
- claim_status_ladder: Explain ontology framing, benchmark adoption, candidate
  work, audit, repair, refutation, blocked promotion, and accepted status as
  distinct states.
- gate_review_path: Explain Gate Chair or human-gated review without implying
  that workflow completion is scientific acceptance.
- negative_result_preservation: Explain how obstructions, refutations,
  task artifacts, completions, and handoffs preserve failed routes.
- forbidden_promotion_boundary: State what the page cannot promote, reject, or
  modify and which sources must be inspected for claim authority.

## Required Analysis Capsules

### Claim Boundary As Guardrail

- premise: Claim boundaries prevent explanatory, workflow, or candidate status
  from being mistaken for accepted physics.
- mechanism: Each task records allowed claims, forbidden claims, required gates,
  and an authority source path; validators and completion records preserve that
  boundary.
- source_basis: `registries/CLAIM_BOUNDARY_REGISTRY.csv`, `AGENTS.md`, and
  `research_control/README.md`.
- authority_status: Human-only explanation of existing claim-boundary behavior.
- uncertainty: A candidate may be useful even when it cannot be promoted.
- validation_or_test: Inspect the claim-boundary row before accepting any
  statement about derivation, obstruction, or benchmark status.
- next_step: Check whether the claim requires Gate Chair or human-gated review.

### Negative Results Are Knowledge

- premise: Refutations and obstruction records are preserved because they
  protect the project from repeating failed routes.
- mechanism: A failed or blocked candidate can become a registered artifact,
  claim-boundary row, completion receipt, and handoff constraint.
- source_basis: `registries/TEX_SOURCE_REGISTRY.csv`,
  `registries/RESEARCH_TASK_REGISTRY.csv`, and
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- authority_status: Explanation of negative-result preservation, not a global
  theory verdict.
- uncertainty: A local refutation may block one route without rejecting the
  whole research program.
- validation_or_test: Verify scope, task path, authority source, forbidden
  promotions, and handoff constraints.
- next_step: Use the source-authority explainer to inspect where the negative
  result is registered and how generated notes remain derivative.

## Non-Goals

- Do not promote, reject, or alter any scientific claim.
- Do not create a Gate Chair verdict.
- Do not edit canonical TeX.
- Do not use external images or network-dependent assets.
