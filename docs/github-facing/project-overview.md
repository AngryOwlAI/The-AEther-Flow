<!-- authority: explanatory -->

# Project Overview

The AEther-Flow project is a dual physics-and-AI research program.

Authority boundary: this page adapts the source-backed project overview for GitHub reading. It does not promote physics claims, change claim boundaries, or alter project-control decisions.

## The Two Tracks

The physics track studies whether ordinary general relativity can be interpreted, and eventually derived, from a deeper four-dimensional `AEther` / `AEther-flow` ontology. The current public benchmark remains conservative: observable-scale physics is ordinary GR. A first-principles derivation from substrate structure remains open.

The AI research-agent track develops a governed theoretical-physics workflow: roles, routing, validation, claim gates, source-first memory, negative-result preservation, and controlled documentation systems.

These tracks are linked. The physics problem gives the agent system a real, difficult research environment. The agent system gives the physics program a disciplined way to explore, reject, preserve, and review ideas without overclaiming.

## Repository Shape

<!-- mermaid-diagram-id: github-facing-project-shape -->
```mermaid
flowchart TD
  Program["AEther-Flow research program"] --> Physics["Physics track"]
  Program --> Agents["AI research-agent track"]
  Physics --> Benchmark["Exact-GR benchmark"]
  Physics --> Ontology["AEther-flow ontology"]
  Physics --> Burden["Open derivation burden"]
  Agents --> Roles["Roles and routing"]
  Agents --> Jobs["Bounded AgentJobs"]
  Agents --> Memory["Source-first memory"]
  Agents --> Gates["Claim gates"]
  Benchmark --> Boundary["Do not confuse benchmark status with derivation success"]
  Jobs --> Boundary
  Gates --> Boundary
```

## Main Reader Routes

- Research idea: [Project Overview](project-overview.md), then [Claim Gates](claim-gates.md).
- Workflow: [Research System](research-system.md), then [Roles and Skills](roles-and-skills.md).
- Authority: [Source Authority](source-authority.md), then [Source Manifest](SOURCE_MANIFEST.md).
- Operation: [Technical Requirements](technical-requirements.md), then the root [../../README.md](../../README.md) validation commands.

## Generated Explainers

The tracked HTML explainers under [../../html/](../../html/) are human-only generated derivatives. They are useful for visual reading, but they are not independent authority. Their source specs live under [../../markdown/html-explainer-specs/](../../markdown/html-explainer-specs/).

This Markdown layer is different: it is hand-authored for GitHub reading and source-backed by those specs. The manifest keeps the traceability explicit.

## Source Basis

- [../../markdown/html-explainer-specs/project-overview-explainer.md](../../markdown/html-explainer-specs/project-overview-explainer.md)
- [../../README.md](../../README.md)
- [../../AGENTS.md](../../AGENTS.md)
- [../../registries/CLAIM_BOUNDARY_REGISTRY.csv](../../registries/CLAIM_BOUNDARY_REGISTRY.csv)
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)
