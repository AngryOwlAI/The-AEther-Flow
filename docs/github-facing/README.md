<!-- authority: explanatory -->

# GitHub-Facing Documentation

This directory is the GitHub-facing Markdown entry layer for the AEther-Flow repository. It is written for humans and external AI agents browsing the project on GitHub.

Authority boundary: these files are canonical for GitHub-facing explanation. They are non-authoritative for physics claims and control decisions. Scientific authority remains in registered TeX and the relevant registries. Control authority remains in AGENTS guidance, research-control records, role contracts, skill contracts, validators, and registries.

## Reading Paths

Start here:

- [Start Here](start-here.md): the shortest route for a first-time reader.
- [Project Overview](project-overview.md): what the project is and how its two tracks fit together.
- [Source Authority](source-authority.md): which files define authority and which files are derivatives or local aids.

Understand the research system:

- [Research System](research-system.md): Director decisions, AgentJobs, validation, completions, handoffs, and project-system improvement.
- [Claim Gates](claim-gates.md): hypotheses, candidates, blocked promotions, negative results, and claim boundaries.
- [Roles and Skills](roles-and-skills.md): registered roles, task overlays, and repo-local skills.

Operate or inspect the project:

- [Technical Requirements](technical-requirements.md): setup tiers, validators, memory refresh, diagram rendering, local retrieval, and PDF refresh.
- [Source Manifest](SOURCE_MANIFEST.md): source-backed traceability for every page in this layer.

## System Map

<!-- mermaid-diagram-id: github-facing-docs-map -->
```mermaid
flowchart TD
  Hub["GitHub-facing docs"] --> Start["Start Here"]
  Hub --> Overview["Project Overview"]
  Hub --> Authority["Source Authority"]
  Hub --> Workflow["Research System"]
  Hub --> Gates["Claim Gates"]
  Hub --> Roles["Roles and Skills"]
  Hub --> Requirements["Technical Requirements"]
  Hub --> Manifest["Source Manifest"]
  Overview --> Physics["Physics track"]
  Overview --> AI["AI research-agent track"]
  Authority --> Sources["TeX, registries, Markdown, HTML, wiki, PDF, .local"]
  Workflow --> Jobs["Bounded AgentJobs"]
  Gates --> Boundaries["Claim boundaries"]
  Roles --> Skills["Repo-local skills"]
```

## Relationship to HTML Explainers

The HTML explainers under [../../html/](../../html/) are generated human-only derivatives backed by source specs under [../../markdown/html-explainer-specs/](../../markdown/html-explainer-specs/). This Markdown layer adapts those source-backed explanations for GitHub reading. It does not replace the source specs, the registries, or generated HTML.
