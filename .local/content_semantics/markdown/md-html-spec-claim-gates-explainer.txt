---
title: "Claim Gates Explainer"
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
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
  - "workflow_step_inspector"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
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

# Claim Gates Explainer Spec

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

- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Adaptive diagram fit: governed Mermaid diagram boxes must read the rendered
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
- Source drilldowns and claim-boundary inspection.

## Required Governed Mermaid Diagrams

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
