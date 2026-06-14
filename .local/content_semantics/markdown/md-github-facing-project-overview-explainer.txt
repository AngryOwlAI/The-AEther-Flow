# Project Overview

This page is the GitHub-readable atlas for the Æther-Flow project. It maps the physics research lane, the AI research-agent lane, and the source-authority boundary before a reader opens detailed specs, registries, or task records.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/project-overview-explainer.md`
- **Related HTML:** `html/project-overview-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The project overview is the atlas for the Æther-Flow repository's human-readable explainer set. Its function is to give readers a controlled entry point into the two linked missions: preserving an exact-GR benchmark for the physics program and maintaining a governed research-agent system for theoretical work. Rather than acting as a source of new claims, the overview routes readers to the ontology, research workflow, control system, role-routing, claim-gate, source-authority, role-and-skill, memory-system, and technical-requirements drilldowns. It matters because the project contains persuasive generated pages, registries, role contracts, and research-control records that can look equally authoritative to a newcomer. The atlas clarifies where explanation ends and source authority begins, so readers can inspect the right Markdown specs, registries, README guidance, or control documents before relying on a statement.

## What This Feature Does

The overview explains the repository as two linked programs: a physics program that preserves ordinary exact general relativity as the observable benchmark while the first-principles Æther-flow derivation remains open, and an AI research-agent program that makes theoretical work bounded, inspectable, and validator-backed.

## Why The Project Needs It

A newcomer sees README prose, TeX, registries, source specs, generated HTML, wiki notes, and local retrieval surfaces. The overview prevents those surfaces from being read as equal authority. It gives a ten-minute path: start here, read ontology vocabulary, inspect claim gates before believing derivation language, read source authority before citing generated outputs, then read the research system before contributing.

## How It Works

The atlas routes by reader need rather than by directory order.

| Reader need | Start here | Then inspect |
| --- | --- | --- |
| Understand the idea | Project overview and ontology | `ontology/aether-and-aether-flow.md`, claim boundaries |
| Understand the workflow | Research system and role routing | `research_control/`, AgentJob and role registries |
| Understand authority | Source authority and memory system | format registries, generated-output rows |
| Run the system | Technical requirements | README commands, validators, bootstrap scripts |

The overview should not be used as proof text. It is a controlled map to source files and sibling explainers.

## What It Is Not

It is not a physics proof, not a claim-promotion mechanism, not a replacement for TeX or registries, and not a control decision. It may summarize the open derivation burden; it may not close it.

## Diagram Reading Guide

The first diagram is a hub map: arrows mean navigation from the atlas to drilldowns, not authority promotion. The second diagram is a two-track map: the physics track and the AI research-agent track both support the same disciplined research objective, but neither diagram says the substrate derivation has been completed.

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
  Program["Æther-flow<br/>research program"] --> Physics["Physics<br/>track"]
  Program --> AI["AI research-agent<br/>track"]
  Physics --> Ontology["Æther-flow<br/>ontology"]
  Physics --> Benchmark["Exact-GR benchmark<br/>adoption"]
  Physics --> OpenProof["Open first-principles<br/>derivation"]
  AI --> Routing["Director and<br/>role routing"]
  AI --> Validation["Validators and<br/>claim gates"]
  AI --> Memory["Source-first<br/>memory"]
  Ontology --> SharedTarget["Derive or hard-fail<br/>a valid path"]
  Routing --> SharedTarget
  Validation --> SharedTarget
  Memory --> SharedTarget
```

## Source Authority

Canonical support comes from `README.md`, `AGENTS.md`, the ontology Markdown source, research-control guidance, claim-boundary rows, and the registered explainer specs. The GitHub page is reader-facing orientation generated from that basis.

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

- Read `github-facing/aether-flow-ontology-explainer.md` for vocabulary.
- Read `github-facing/claim-gates-explainer.md` before accepting any derivation-status phrase.
- Read `github-facing/source-authority-explainer.md` before citing generated artifacts.
- Read `github-facing/research-agent-workflow-explainer.md` before making a controlled change.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `research_control/README.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `markdown/html-explainer-specs/aether-flow-ontology-explainer.md`
- `markdown/html-explainer-specs/research-agent-workflow-explainer.md`
- `markdown/html-explainer-specs/research-control-system-explainer.md`
- `markdown/html-explainer-specs/role-routing-explainer.md`
- `markdown/html-explainer-specs/claim-gates-explainer.md`
- `markdown/html-explainer-specs/source-authority-explainer.md`
- `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- `markdown/html-explainer-specs/memory-system-explainer.md`
- `markdown/html-explainer-specs/technical-requirements-explainer.md`
