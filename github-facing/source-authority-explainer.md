# Source Authority

This page is the law-of-the-land guide for deciding which files define project truth and which files are generated aids.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/source-authority-explainer.md`
- **Related HTML:** `html/source-authority-explainer.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

Source authority ranks registered TeX, registries, registered Markdown, generated HTML, generated wiki notes, PDFs, local retrieval surfaces, and scratch caches by what each file type may support.

## Why The Project Needs It

The easiest surface to read is often not the authoritative one. A polished HTML page, wiki note, PDF, or local Obsidian note can be useful while still being derivative. The project needs this distinction to keep scientific claims and control behavior reproducible.

## How It Works

Authority matrix:

| Lane | Primary use | Authority status | Update rule |
| --- | --- | --- | --- |
| `.tex` | physics and derivational claims | canonical when registered | edit source, register, validate |
| `.csv` registries | routing, provenance, generated-output tracking | canonical for registry facts | update rows through bounded transactions |
| registered `.md` | README, guidance, source specs, design notes | canonical for its lane | edit source before derivatives |
| `github-facing/*.md` | public reader orientation | generated noncanonical | derive from matching source spec |
| `html/*.html` | human visual explanation | generated noncanonical | regenerate from registered spec |
| `wiki/` | navigation and metadata notes | generated noncanonical | regenerate through bootstrap |
| PDFs | human reading from TeX | generated derivative | rebuild from TeX |
| `.local/` | scratch, cache, retrieval | local nonauthority | never override tracked state |

## What It Is Not

It is not a convenience ranking, not an invitation to edit generated derivatives by hand, not a way to cite a wiki note as physics authority, and not a permission expansion for local tools.

## Diagram Reading Guide

The authority ladder diagram moves from registered TeX and registries to Markdown and generated derivatives. The generation-flow diagram shows that arrows mean provenance and regeneration, not promotion of derivative authority.

<!-- mermaid-diagram-id: source-authority-ladder -->
```mermaid
flowchart TD
  Tex["Registered TeX<br/>scientific authority"] --> Registries["Format registries<br/>routing and provenance authority"]
  Registries --> Markdown["Registered Markdown<br/>front door and specs"]
  Markdown --> Html["Tracked HTML explainers<br/>human-only generated derivatives"]
  Tex --> Pdf["PDF derivatives<br/>human reading"]
  Registries --> Wiki["Generated wiki and indexes<br/>metadata retrieval"]
  Wiki --> Local["Local Obsidian and .local caches<br/>scratch or retrieval"]
  Html --> Local
```

<!-- mermaid-diagram-id: derivative-generation-flow -->
```mermaid
flowchart TD
  Source["Authoritative source edit"] --> Registry["Registry row and source hash"]
  Registry --> Bootstrap["Memory bootstrap"]
  Bootstrap --> Wiki["Generated wiki notes"]
  Bootstrap --> Html["Generated HTML derivative"]
  Bootstrap --> Pdf["Generated PDF derivative"]
  Html --> Metadata["Source-basis metadata"]
  Wiki --> Banner["Non-authority banner"]
  Pdf --> Link["PDF registry row"]
  Metadata --> Validate["Validate source parity"]
  Banner --> Validate
  Link --> Validate
```

## Source Authority

Root agent guidance, the project-memory-system skill, HTML explainer registry, Markdown registry, wiki registry, PDF registry, and file object registry ground this page.

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

- Inspect source and registry rows before changing project knowledge.
- Regenerate derivatives after source edits.
- Use documentation-impact receipts when project-system machinery changes.
- Use GitHub-facing pages for orientation, not citation authority.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/WIKI_ARTIFACT_REGISTRY.csv`
- `registries/PDF_DERIVATIVE_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`
- `research_control/design/html_explainer_flexible_presentation_contract.md`
