<!-- authority: control -->

# Documentation Curator Visual Atlas Contract

## Purpose

This contract governs source-backed public explainers for AEther-Flow. It
borrows the explanatory discipline of visual planning and visual recap systems
without adopting NPX, Agent-Native Plans, hosted Plan tooling, localhost bridge
tooling, CDN-rendered diagrams, remote editor infrastructure, or any external
runtime dependency in the public documentation pipeline.

## Non-Negotiable Constraints

- Do not use NPX.
- Do not use `@agent-native/core`.
- Do not use hosted Plan MCP.
- Do not use localhost bridge artifacts.
- Do not require network access to read public docs.
- Do not import Mermaid in tracked HTML at browser runtime.
- Do not use CDN scripts, remote CSS, remote fonts, hosted plan links, remote
  analytics, or external commenting workflows in generated public docs.
- Do not treat generated HTML, GitHub-facing Markdown, wiki notes, PDFs,
  semantic extracts, Obsidian notes, or `.local/` caches as authority.

## Authority Spine

The authority path remains:

```text
registered TeX / registries / registered Markdown
    -> Markdown source spec
    -> GitHub-facing Markdown
    -> tracked standalone HTML
    -> generated wiki and retrieval derivatives
```

Source specs under `markdown/html-explainer-specs/` define the teaching
contract. GitHub-facing Markdown and tracked HTML are generated noncanonical
reader surfaces. Wiki notes and local retrieval outputs are navigation aids.

## Topic Registry

`registries/EXPLAINER_TOPIC_REGISTRY.csv` tracks first-class concepts that must
be explained. Required topics must name one source spec, one GitHub-facing
Markdown derivative, one tracked HTML derivative, primary source paths,
required visual IDs, required reader blocks, teaching-packet expectation,
claim-boundary ID, and owner role.

The registry validates concept coverage. It does not promote generated pages to
source authority.

## Required Reader Blocks

Required atlas topics must answer:

1. What this does.
2. Why AEther needs it.
3. System map.
4. How it works.
5. Objects and authority.
6. Example.
7. Non-example.
8. Common confusions.
9. What this does not authorize.
10. Source map.
11. Next reading path.

Source specs may add page-specific blocks, but required topics must keep this
recognizable reader model in both GitHub-facing Markdown and tracked HTML.

## Visual Requirements

GitHub-facing Markdown may use Mermaid fences with stable
`mermaid-diagram-id` markers. Tracked HTML must not execute Mermaid in the
browser; it must embed build-time inline SVG or local semantic diagram markup
and preserve source parity for registered Mermaid diagrams.

Every required visual in the topic registry must appear in the source spec,
GitHub Markdown, and HTML derivative under the same stable ID.

## Source Evidence

Every page must visibly cite source paths. Required output source maps must cite
all source paths declared by the source spec. Generated derivatives may cite
other generated derivatives only when the subject is generated derivatives
themselves; the cited source of authority remains the canonical source or
registry row.

## GitHub Markdown Standard

GitHub-facing Markdown must be native Markdown and must not rely on HTML-only
controls, CSS, or collapsible HTML for essential meaning. The preferred order
is title, functional summary, `What This Does`, `System Map`, `Source Binding`,
mechanism sections, examples, boundary, source map, and next reading path.

Source binding remains required, but it must not replace the functional
opening.

## Standalone HTML Standard

Tracked HTML explainers must be single-file no-network documents. They should
include a functional hero summary, section navigation, source chips, a visual
system map, workflow inspector where declared, authority boundary panel,
object/source footprint, examples and non-examples, common confusion cards,
source map, and next reading path.

Allowed JavaScript is limited to local reading enhancement such as active
section navigation, local search, copy source path, and pan/zoom for already
embedded inline SVG. Forbidden JavaScript includes remote imports,
browser-side Mermaid rendering, hosted Plan embeds, external analytics,
external comments, and runtime package fetching.

## Validation

The Visual Atlas v2 validator chain is:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/validate_explainer_topic_coverage.py --root .
.venv/bin/python scripts/validate_explainer_parity.py --root .
.venv/bin/python scripts/validate_standalone_html.py --root .
.venv/bin/python scripts/validate_reader_first_docs.py --root .
.venv/bin/python scripts/validate_explainer_diagrams.py --root .
.venv/bin/python scripts/spec_depth_lint.py --root .
.venv/bin/python scripts/validate_teaching_qa.py --root .
```

Bootstrap also exposes:

- `--docs-only`: refresh generated documentation registry/wiki surfaces and run
  documentation validators.
- `--docs-validate-only`: validate docs without writing.
- `--strict-docs`: fail supported docs validators on advisory reader-facing
  warnings.

## Boundary

The atlas improves explanatory quality and validation coverage. It does not
create new roles by convention, new write permissions, new routing authority,
new validator authority outside the scripts that implement it, scientific claim
promotion, ontology adoption, benchmark changes, Gate Chair decisions, or GR
derivation completion.
