# Project Overview Spec

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
- `Roles and skills`: registered roles, governed repo-local skills, and
  evidence-labeled support-skill associations.
- `Memory system`: CSV memory spine and derived wiki, Obsidian, semantic, and
  query surfaces.
- `Technical requirements`: tiered requirements for reading, validating,
  regenerating Mermaid HTML, using local retrieval, and refreshing PDFs.

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
- Hero: state the project as a dual physics-and-AI research program.
- Hub links: grouped drilldown cards for ontology, research system, role
  routing, claim gates, source authority, validation governance, roles and
  skills, memory system, and technical requirements.
- Group links by use case: understand the research idea, understand the agent
  workflow, understand authority and memory, and run or regenerate the system.
- High-level model: project purpose and the two co-developing tracks.
- Operational model: how the research system turns questions into bounded jobs
  and checked outputs.
- Low-level evidence model: source files, registry rows, generated artifacts,
  and validator receipts.
- All Source Materials section: complete source list with source-path evidence; claim-boundary metadata remains in the source spec.
- Claim-boundary panel: human-only, non-authoritative, no physics promotion.

## Required Diagrams

<!-- mermaid-diagram-id: research-atlas-hub -->
```mermaid
flowchart TD
  Hub["Project overview hub"] --> Ontology["Æther-flow ontology drilldown"]
  Hub --> ResearchSystem["Research system drilldown"]
  Hub --> RoleRouting["Role routing drilldown"]
  Hub --> ClaimGates["Claim gates drilldown"]
  Hub --> SourceAuthority["Source authority drilldown"]
  Hub --> Validation["Validation governance drilldown"]
  Hub --> RolesSkills["Roles and skills drilldown"]
  Hub --> MemorySystem["Memory system drilldown"]
  Hub --> Requirements["Technical requirements drilldown"]
  Ontology --> Burden["Open derivation burden"]
  ResearchSystem --> Jobs["Bounded AgentJobs"]
  RoleRouting --> Roles["Execution-role contract"]
  ClaimGates --> Boundaries["Claim-boundary registry"]
  SourceAuthority --> Registries["Source-first registries"]
  Validation --> Receipts["Validator receipts"]
  RolesSkills --> SkillContracts["Repo-local skill contracts"]
  MemorySystem --> Retrieval["Derived retrieval surfaces"]
  Requirements --> ToolTiers["Tiered tool requirements"]
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

## Source-Backed Summary

Summary heading: `Summary of Project Overview`

Summary text:

The project overview is the atlas for the AEther-Flow repository's human-
readable explainer set. Its function is to give readers a controlled entry
point into the two linked missions: preserving an exact-GR benchmark for the
physics program and maintaining a governed research-agent system for
theoretical work. Rather than acting as a source of new claims, the overview
routes readers to the ontology, research workflow, control system, role-
routing, claim-gate, source-authority, role-and-skill, memory-system, and
technical-requirements drilldowns. It matters because the project contains
persuasive generated pages, registries, role contracts, and research-control
records that can look equally authoritative to a newcomer. The atlas clarifies
where explanation ends and source authority begins, so readers can inspect the
right Markdown specs, registries, README guidance, or control documents before
relying on a statement.

Summary source basis:

- `README.md`
- `AGENTS.md`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `markdown/html-explainer-specs/research-control-system-explainer.md`

## Required Content Blocks

- subject_summary: Summarize the project overview atlas, its routing function across the explainer set, why it matters for source-first project understanding, and which declared sources ground the summary.
- atlas_navigation: A completed atlas section that routes readers by use case across the research idea, agent workflow, authority and memory system, and regeneration/validation path while preserving existing explainer URLs.
- research_idea: A documentation-grade explanation of the two-track program: exact-GR benchmark adoption, open first-principles Æther-flow derivation, claim-gate caution, and the ontology drilldowns that readers should use next.
- agent_workflow: A concrete overview of the staged-autonomy research harness: state, handoff, Director decision, bounded AgentJob, role execution, artifacts, validators, completion, and registries, with the boundary that it is not an autonomous proof engine.
- authority_memory: A source-first explanation of canonical TeX, registries, registered Markdown, generated HTML/wiki/PDF derivatives, and local retrieval surfaces, including why memory access does not create new authority.
- run_regenerate_system: A practical operator path for validating and regenerating the project: inspect sources, update specs, render HTML, preserve Mermaid parity, run bootstrap, run advisory depth lint, and use the technical-requirements drilldown.
