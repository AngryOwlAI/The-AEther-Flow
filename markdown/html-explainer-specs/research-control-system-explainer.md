---
title: "Research-Control System Explainer"
purpose: "Provide the validation-governance drilldown for authority boundaries, project-system improvement, documentation-impact receipts, and source-backed HTML governance."
audience: "Technical but human-readable: maintainers, research agents, and reviewers who need the control-system validation model."
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
  - "scripts/project_control/validate_documentation_impact.py"
  - "scripts/research_control/validate_research_control.py"
  - ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"
claim_boundary: "Human-only project-system visualization. It explains existing authority boundaries and validator behavior without changing physics claims, control contracts, routing decisions, validator behavior, or registry authority."
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
    - "control-boundary-map"
---

# Research-Control System Explainer Spec

## Rendering Intent

Create a tracked HTML drilldown for validation governance. The page should
explain how control-system changes remain bounded: classification, resolver
state, documentation-impact accounting, source-backed HTML rules, Mermaid
parity, bootstrap refresh, research-control validation, diff boundary checks,
and tests.

Keep source authority details summarized here and send deep authority-ladder
content to `source-authority-explainer.html`.

## Required Visual Structure

- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- High-level model: the control system exists to preserve authority boundaries
  while improving the project machinery.
- Operational model: change classification, bounded AgentJob, documentation
  impact, generated-derivative refresh, validators, and checkpoint boundary.
- Low-level evidence model: validator scripts, completion receipts, registry
  rows, source specs, and generated HTML metadata.
- Documentation Curator panel: source-spec-first tracked HTML generation.
- Workflow step inspector for the validation chain.
- Source drilldowns and claim-boundary inspection.

## Required Governed Mermaid Diagrams

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

<!-- mermaid-diagram-id: control-boundary-map -->
```mermaid
flowchart TD
  Change["Proposed project-system change"] --> Classifier["Change classifier"]
  Classifier --> Role["Recommended role boundary"]
  Role --> Job["One bounded AgentJob"]
  Job --> Allowed["Allowed writes"]
  Job --> Forbidden["Forbidden authority surfaces"]
  Allowed --> Validators["Required validators"]
  Forbidden --> Stop["Stop condition"]
  Validators --> Receipt["Completion and documentation-impact receipts"]
  Receipt --> Registry["Control registries updated"]
```

## Required Analysis Capsules

### Source-Backed HTML Governance

- premise: Tracked HTML explainers are valid only when backed by registered
  Markdown source specs.
- mechanism: The Markdown spec declares title, purpose, source material, claim
  boundary, interaction model, required controls, source drilldowns, Mermaid
  diagrams, and analysis capsules; generated HTML carries marker and source
  metadata evidence.
- source_basis: `.codex/skills/html-visual-explainer/SKILL.md`,
  `.codex/skills/visual-explainer/SKILL.md`, the Mermaid Documentation
  subskill, and `registries/HTML_EXPLAINER_REGISTRY.csv`.
- authority_status: Project-control explanation of generated derivative
  governance.
- uncertainty: Visual design quality still requires human or browser review;
  the validator checks structural evidence and source parity.
- validation_or_test: Run Mermaid validation, memory bootstrap validation, and
  confirm declared controls have matching HTML markers.
- next_step: Modify the Markdown source spec first, regenerate HTML, render
  Mermaid inline SVG, then validate.

### Documentation-Impact Boundary

- premise: Documentation impact is a receipt requirement, not automatic source
  ownership by Documentation Curator.
- mechanism: Classifier output identifies documentation impact; the selected
  role depends on source authority class; project-system AgentJobs must record
  documentation-impact coverage.
- source_basis: `research_control/README.md`,
  `.codex/skills/improve-project-system/SKILL.md`, and
  `scripts/project_control/validate_documentation_impact.py`.
- authority_status: Control-system explanation.
- uncertainty: Resolver output is advisory; hard stops come from validators and
  authority-boundary violations.
- validation_or_test: Use classification, documentation-impact validation,
  signal validation, research-control validation, and diff checks.
- next_step: Keep explanatory HTML work inside Documentation Curator authority
  and route validator or contract changes to the proper roles.

## Non-Goals

- Do not introduce physics claims.
- Do not change project-control rules.
- Do not present generated HTML as an authority source.
- Do not use external images or network-dependent assets.
