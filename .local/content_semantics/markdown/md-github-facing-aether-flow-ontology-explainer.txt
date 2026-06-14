# Æther-flow Ontology

This page explains the project-specific ontology: `Æther`, `Æther-flow`, observed three-dimensional space, `S-time`, observed expansion, and the open burden of deriving the exact-GR benchmark from source-defined substrate structure.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/aether-flow-ontology-explainer.md`
- **Related HTML:** `html/aether-flow-ontology-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The Æther-flow ontology is the project's conceptual vocabulary for a proposed deeper four-dimensional substrate, its intrinsic ordered motion, and the observer-accessible appearance of space, time-order, expansion, and gravity. Its role is not to replace general relativity or claim a completed derivation; it frames exact GR as the observable benchmark that any future substrate law must recover. The ontology matters because it keeps the research program's intuitive picture disciplined: observed three-dimensional space is treated as a local experiential slice, S-time as the experienced order of change, and gravity as a heuristic matter-shaped reorganization of the deeper flow. At the project level, the explainer helps readers separate ontology, mathematical model, benchmark adoption, and open derivation burden before reading diagrams or candidate arguments.

## What This Feature Does

The ontology page is the conceptual flagship. It gives a glossary, an adoption-versus-derivation bridge, an anti-smuggling checklist, and a derivation-burden map for readers who need the vocabulary before reading science drafts or registries.

## Why The Project Needs It

The ontology is useful only if it stays separate from the mathematical model and from empirical claim status. It can guide interpretation, but only a source-defined substrate derivation that recovers Lorentzian geometry, clocks, causal structure, same-metric matter coupling, invariance, and closure could promote it beyond interpretation.

## How It Works

Key distinctions:

| Term | Reader-safe meaning | Boundary |
| --- | --- | --- |
| `Æther` | proposed deeper four-dimensional substrate vocabulary | not canonical proof of physical substrate |
| `Æther-flow` | intrinsic ordered motion used to interpret observed phenomena | not a completed derivation of GR |
| Observed space | local experiential slice/readout | not a primitive target structure smuggled into the source |
| `S-time` | experienced order of change | must still be recovered coherently, not assumed |
| Exact-GR benchmark | ordinary GR retained as observable target behavior | adoption is not first-principles derivation |

The anti-smuggling rule is simple: a candidate cannot import target metric, clock, locality, matter-coupling, or favorable observer structure as a source primitive and then call recovery successful.

## What It Is Not

It is not a replacement for registered TeX, not an accepted new physics theory, not a new empirical prediction, and not evidence that the Æther-flow derivation is complete. It does not authorize candidate reconstruction or Gate Chair promotion.

## Diagram Reading Guide

The ontology-stack diagram reads downward from substrate vocabulary to observed benchmark behavior. The burden-map diagram reads as obligations: each arrow names a recovery step that must be derived or blocked by evidence, and the anti-smuggling node constrains the route.

<!-- mermaid-diagram-id: aether-flow-ontology-stack -->
```mermaid
flowchart TD
  Aether["Æther<br/>four-dimensional substrate"] --> Flow["Æther-flow<br/>intrinsic ordered motion"]
  Flow --> Slice["Observed three-dimensional space<br/>local experiential slice"]
  Flow --> STime["S-time<br/>experienced order of change"]
  Flow --> Expansion["Observed expansion<br/>appearance of deeper motion"]
  Matter["Matter and light"] --> STime
  Matter --> Gravity["Gravity as mass-shaped<br/>Æther-flow reorganization"]
  Slice --> Benchmark["Observable benchmark<br/>ordinary exact GR"]
  STime --> Benchmark
  Gravity --> Benchmark
```

<!-- mermaid-diagram-id: derivation-burden-map -->
```mermaid
flowchart TD
  SourceData["Source-defined substrate data"] --> Readout["Observer normal/readout orbit"]
  Readout --> Metric["Effective Lorentzian metric"]
  Metric --> Causal["Causal structure and clocks"]
  Causal --> Matter["Universal same-metric matter coupling"]
  Matter --> Closure["S-time and Einsteinian closure"]
  Closure --> ExactGR["Exact-GR benchmark recovered"]
  SourceData --> AntiSmuggling["Anti-smuggling constraints"]
  AntiSmuggling --> Metric
  AntiSmuggling --> Matter
  AntiSmuggling --> Closure
  ExactGR --> Gate["Promotion requires claim gate"]
```

## Source Authority

The glossary and boundaries are grounded in `ontology/aether-and-aether-flow.md`, `ontology/aether_flow_interpretation-lemen.md`, root guidance, and claim-boundary registry rows. Registered TeX remains the authority for scientific claims.

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

- Use this page for vocabulary, then inspect the ontology Markdown sources.
- Use claim gates before interpreting any candidate derivation.
- Use source authority to distinguish Markdown explanation from TeX authority.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `ontology/aether_flow_interpretation-lemen.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
