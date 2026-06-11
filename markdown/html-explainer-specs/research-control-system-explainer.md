---
title: "Research-Control System Explainer"
purpose: "Provide a human-readable visual overview of the project authority chain, research-control loop, project-system improvement loop, and Documentation Curator v0.2.0 source-backed HTML boundary."
audience: "Project maintainers, research agents, and reviewers who need a compact mental model of the control system."
output_path: "html/research-control-system-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "AGENTS.md"
  - "README.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md"
  - ".agents/roles/research_ops/documentation-curator.v0.2.0.md"
  - "scripts/research_control/validate_research_control.py"
  - ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"
claim_boundary: "Human-only project-system visualization. It explains existing authority boundaries and validator behavior without changing physics claims, control contracts, routing decisions, or registry authority."
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
  - "AGENTS.md"
  - "README.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
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
    - "research-control-validation-flow"
---

# Research-Control System Explainer Spec

## Rendering Intent

Create a self-contained HTML explainer for the repository control system. The
page should emphasize the source-first authority hierarchy, the separation
between physics continuation and project-system improvement, and the
Documentation Curator v0.2.0 rule that tracked HTML is valid only when backed
by this Markdown source spec.

## Required Visual Structure

- An authority ladder showing canonical sources, registries, Markdown specs,
  and generated derivatives.
- A two-lane workflow view separating `continue-research` from
  `improve-project-system`.
- A Documentation Curator v0.2.0 panel showing spec-first HTML generation.
- A validator gate panel listing bootstrap, documentation-impact validation,
  research-control validation, project-improvement signal validation, tests,
  and diff checks.
- Expandable source drilldowns that state why each cited source matters and
  what authority, governance, or validation boundary it checks.
- A claim-boundary notice stating that the page is human-only and
  non-authoritative.
- Deep-first progressive-disclosure controls for expandable analysis capsules,
  source drilldowns, claim-boundary inspection, and a workflow step inspector.

## Required Governed Mermaid Diagram

The generated HTML derivative must render this diagram through the governed
Mermaid visual-explainer shell. The diagram is explanatory only: it shows the
validation order for a source-backed documentation change and does not create a
new control rule.

<!-- mermaid-diagram-id: research-control-validation-flow -->
```mermaid
flowchart TD
  Spec["Markdown source spec update"] --> Html["Generated HTML derivative"]
  Html --> Mermaid["Mermaid source parity validation"]
  Mermaid --> Bootstrap["Memory bootstrap and registry refresh"]
  Bootstrap --> DocsImpact["Documentation-impact gate"]
  DocsImpact --> ResearchControl["Research-control validation"]
  ResearchControl --> DiffGate["Diff and authority boundary gate"]
  DiffGate --> Checkpoint["Local checkpoint commit"]
```

## Required Analysis Capsules

### Source-Backed HTML Governance

- premise: Tracked HTML explainers are valid only when backed by registered
  Markdown source specs.
- mechanism: The Markdown spec declares title, purpose, source material, claim
  boundary, interaction model, required controls, source drilldowns, and the
  analysis capsule schema; generated HTML carries marker evidence.
- source_basis: `.codex/skills/html-visual-explainer/SKILL.md`,
  `.codex/skills/visual-explainer/SKILL.md`, and
  `registries/HTML_EXPLAINER_REGISTRY.csv`.
- authority_status: Project-control explanation of generated derivative
  governance.
- uncertainty: Visual design quality still requires human or browser review;
  the validator checks structural evidence only.
- validation_or_test: Run memory bootstrap validation and confirm each declared
  control has a matching `data-explainer-control` marker.
- next_step: Modify the Markdown source spec first, regenerate HTML, then
  validate.

### Project-System Improvement Loop

- premise: Project-system improvement is separate from physics continuation.
- mechanism: A bounded AgentJob updates roles, validators, skill contracts,
  docs, or memory tooling while documentation-impact and research-control
  validators preserve the authority boundary.
- source_basis: `AGENTS.md`, `research_control/README.md`, and
  `.codex/skills/improve-project-system/SKILL.md`.
- authority_status: Control-system explanation; it does not promote scientific
  claims.
- uncertainty: Resolver output is advisory; validator failures and authority
  violations are the hard stop conditions.
- validation_or_test: Use classification, resolver output, signal validation,
  documentation-impact validation, research-control validation, and tests.
- next_step: Keep future interactive-explainer improvements inside one bounded
  project-system job.

## Non-Goals

- Do not introduce physics claims.
- Do not change project-control rules.
- Do not present generated HTML as an authority source.
- Do not use external images or network-dependent assets.
