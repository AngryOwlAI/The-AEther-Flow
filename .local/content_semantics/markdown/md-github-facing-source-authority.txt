<!-- authority: explanatory -->

# Source Authority

Source authority is the rule for deciding which files can define project truth and which files are aids for reading, retrieval, validation, or publication.

Authority boundary: this page explains the existing authority ladder. It does not change registry status, scientific authority, or control authority.

## Authority Ladder

1. Registered `.tex` files are canonical for physics research and derivational claims.
2. Format-specific registries under [../../registries/](../../registries/) are canonical for routing, provenance, generated-output tracking, and agent-queryable memory.
3. Registered Markdown files are canonical for front-door material, agent guidance, project-control notes, and explainer source specs.
4. PDFs, generated wiki notes, generated indexes, generated HTML explainers, local Obsidian files, and `.local` caches are derivative or scratch surfaces.

<!-- mermaid-diagram-id: github-facing-source-authority -->
```mermaid
flowchart TD
  Tex["Registered TeX: scientific authority"] --> Registries["Registries: routing and provenance authority"]
  Registries --> Markdown["Registered Markdown: front-door, agent guidance, specs"]
  Markdown --> Html["HTML explainers: generated human-only derivatives"]
  Tex --> Pdf["PDFs: generated human-reading derivatives"]
  Registries --> Wiki["Wiki and indexes: generated retrieval aids"]
  Wiki --> Local[".local and Obsidian: local scratch or retrieval"]
  Html --> Local
```

## Format Use

| Surface | Main use | Authority status |
| --- | --- | --- |
| `.tex` | Physics sources, derivations, benchmark claims. | Scientific authority when registered. |
| `.csv` registries | Provenance, routing, source status, generated-output tracking. | Registry authority. |
| `.md` registered Markdown | GitHub explanation, agent guidance, control notes, explainer specs. | Markdown authority for its lane. |
| `.yaml` control records | Tasks, decisions, AgentJobs, completions, handoffs, approvals. | Control authority when tracked. |
| `html/*.html` | Human visual explainers. | Generated noncanonical derivative. |
| PDFs | Human reading of TeX outputs. | Generated noncanonical derivative. |
| `wiki/` | Generated metadata notes and indexes. | Generated noncanonical derivative. |
| `.local/` | Scratch, caches, local retrieval, previews. | No authority. |

## Practical Rule

When a generated surface looks persuasive, follow it back to its source path and registry row. Edit the canonical source, then regenerate and validate. Do not hand-edit generated wiki notes or generated HTML as independent authority.

## Source Basis

- [../../markdown/html-explainer-specs/source-authority-explainer.md](../../markdown/html-explainer-specs/source-authority-explainer.md)
- [../../AGENTS.md](../../AGENTS.md)
- [../../registries/TEX_SOURCE_REGISTRY.csv](../../registries/TEX_SOURCE_REGISTRY.csv)
- [../../registries/MARKDOWN_SOURCE_REGISTRY.csv](../../registries/MARKDOWN_SOURCE_REGISTRY.csv)
- [../../registries/HTML_EXPLAINER_REGISTRY.csv](../../registries/HTML_EXPLAINER_REGISTRY.csv)
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)
