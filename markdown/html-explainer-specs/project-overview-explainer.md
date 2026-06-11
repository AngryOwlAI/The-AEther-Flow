---
title: "Project Overview Explainer"
purpose: "Provide the research-atlas hub for the Æther-flow ontology, exact-GR benchmark boundary, research-agent system, role routing, claim gates, and source authority."
audience: "Technical but human-readable: maintainers, research agents, and reviewers who need a clear project map before inspecting source files and registries."
output_path: "html/project-overview-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "research_control/README.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "markdown/html-explainer-specs/aether-flow-ontology-explainer.md"
  - "markdown/html-explainer-specs/research-agent-workflow-explainer.md"
  - "markdown/html-explainer-specs/research-control-system-explainer.md"
  - "markdown/html-explainer-specs/role-routing-explainer.md"
  - "markdown/html-explainer-specs/claim-gates-explainer.md"
  - "markdown/html-explainer-specs/source-authority-explainer.md"
claim_boundary: "Human-only project atlas hub. It summarizes the existing dual-track project identity, exact-GR benchmark/open-derivation boundary, research-control system, and source authority without changing physics claims, control contracts, routing decisions, validator behavior, or registry authority."
human_visual_only: true
explainer_kind: "project_overview"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "research_control/README.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
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
    - "research-atlas-hub"
    - "dual-track-map"
---

# Project Overview Explainer Spec

## Rendering Intent

Create a self-contained tracked HTML hub for the research-atlas explainer set.
The page must orient a technical reader to the project without requiring prior
repository knowledge. It should show the project as a dual physics-and-AI
research program, then route readers to focused drilldowns:

- `Æther-flow ontology`: high-level substrate model plus low-level readout and
  derivation burden.
- `Research system`: Director, AgentJobs, validation, completions, and
  handoffs.
- `Role routing`: how roles are selected and constrained for one job.
- `Claim gates`: how hypotheses, candidates, refutations, blocked claims, and
  negative results are handled.
- `Source authority`: how TeX, registries, Markdown, generated wiki/PDF/HTML,
  and `.local/` scratch layers relate.

The page should stop explaining what an ontology is in general. It should
explain what this project means by the `Æther-flow ontology`.

## Shared Research-Atlas Visual System

Use one visual language across this hub and every drilldown page:

- Authority color: canonical sources and registries.
- Physics color: ontology, benchmark, derivation burden, and claim gates.
- Workflow color: Director decisions, AgentJobs, roles, validation, completion,
  and handoff.
- Generated-derivative color: HTML, wiki notes, PDFs, and local retrieval
  surfaces.
- Warning/open-burden color: unresolved derivation steps, blocked promotion,
  and no-go or negative-result preservation.
- Validation color: passing checks, source parity, and successful receipts.

Mermaid diagrams must use the governed build-time inline-SVG path and should
visually match the HTML palette and typography.

## Required Visual Structure

- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Hero: state the project as a dual physics-and-AI research program.
- Hub links: six drilldown cards for ontology, research system, role routing,
  claim gates, source authority, and validation governance.
- High-level model: project purpose and the two co-developing tracks.
- Operational model: how the research system turns questions into bounded jobs
  and checked outputs.
- Low-level evidence model: source files, registry rows, generated artifacts,
  and validator receipts.
- Source drilldowns: why each source matters and what boundary it checks.
- Claim-boundary panel: human-only, non-authoritative, no physics promotion.

## Required Governed Mermaid Diagrams

<!-- mermaid-diagram-id: research-atlas-hub -->
```mermaid
flowchart TD
  Hub["Project overview hub"] --> Ontology["Æther-flow ontology drilldown"]
  Hub --> ResearchSystem["Research system drilldown"]
  Hub --> RoleRouting["Role routing drilldown"]
  Hub --> ClaimGates["Claim gates drilldown"]
  Hub --> SourceAuthority["Source authority drilldown"]
  Hub --> Validation["Validation governance drilldown"]
  Ontology --> Burden["Open derivation burden"]
  ResearchSystem --> Jobs["Bounded AgentJobs"]
  RoleRouting --> Roles["Execution-role contract"]
  ClaimGates --> Boundaries["Claim-boundary registry"]
  SourceAuthority --> Registries["Source-first registries"]
  Validation --> Receipts["Validator receipts"]
```

<!-- mermaid-diagram-id: dual-track-map -->
```mermaid
flowchart TD
  Program["Æther-flow research program"] --> Physics["Physics track"]
  Program --> AI["AI research-agent track"]
  Physics --> Ontology["Æther-flow ontology"]
  Physics --> Benchmark["Exact-GR benchmark adoption"]
  Physics --> OpenProof["Open first-principles derivation"]
  AI --> Routing["Director and role routing"]
  AI --> Validation["Validators and claim gates"]
  AI --> Memory["Source-first memory"]
  Ontology --> SharedTarget["Derive or hard-fail a valid path"]
  Routing --> SharedTarget
  Validation --> SharedTarget
  Memory --> SharedTarget
```

## Required Analysis Capsules

### The Project As Research Atlas

- premise: The project is a dual physics-and-AI research program centered on
  the `Æther-flow ontology` and a human-accountable research-agent system.
- mechanism: The hub should show the two tracks, then route readers to
  drilldowns that explain the ontology, workflow, role routing, claim gates, and
  source authority at increasing depth.
- source_basis: `README.md`, `AGENTS.md`, `ontology/aether-and-aether-flow.md`,
  and the registered explainer source specs.
- authority_status: Human-only overview; source specs and registries carry
  project documentation authority, while registered TeX carries scientific
  authority.
- uncertainty: The first-principles derivation of the exact-GR benchmark from
  substrate structure remains open.
- validation_or_test: Verify that every drilldown has a source spec,
  source-basis metadata, governed Mermaid parity, and a registered HTML row.
- next_step: Use the ontology drilldown to inspect the project-specific
  substrate/readout burden before evaluating any candidate derivation.

### Workflow Is Not Physics Proof

- premise: The research-agent system organizes work; it does not by itself
  establish a scientific result.
- mechanism: Director decisions, AgentJobs, role contracts, registries,
  validators, completions, and handoffs make progress auditable and bounded.
- source_basis: `research_control/README.md`, `AGENTS.md`, and control
  registries.
- authority_status: Project-control explanation only.
- uncertainty: A completed task may produce progress, obstruction, a repair
  packet, or a negative result without proving the broader theory.
- validation_or_test: Check completion records, claim-boundary rows, and
  generated-output boundaries before treating any workflow step as accepted
  knowledge.
- next_step: Use the research-system and claim-gates drilldowns to inspect the
  actual transaction model.

## Non-Goals

- Do not introduce new physics claims.
- Do not imply that GR has been derived from the `Æther-flow ontology`.
- Do not change project-control rules, role authority, validators, or routing.
- Do not use external images or network-dependent assets.
