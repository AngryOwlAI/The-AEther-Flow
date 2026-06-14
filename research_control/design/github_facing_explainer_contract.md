<!-- authority: control -->

# GitHub-Facing Explainer Contract

## Purpose

The root `github-facing/*.md` files are source-backed Markdown explainers for
humans and external AI reading the repository on GitHub. They are derived from
registered explainer specs under `markdown/html-explainer-specs/` and point to
the related tracked HTML derivative under `html/`, but they are not body-only
copies of source specs.

## Authority

The GitHub-facing layer is generated noncanonical. It may orient readers,
summarize feature behavior, identify source files, and explain workflow
boundaries. It must not define physics claims, alter control behavior, replace
registry rows, or become independent source authority.

The authority ladder remains:

1. Registered TeX files define physics and derivational claims.
2. Registries define routing, provenance, generated-output tracking, and
   agent-queryable memory.
3. Registered Markdown defines front-door guidance, source specs, and
   project-control notes.
4. GitHub-facing Markdown, HTML explainers, wiki notes, PDFs, and local
   retrieval surfaces are derivative or orientation surfaces unless another
   registered source explicitly gives them narrower authority.

## Required Page Contract

Each `github-facing/*.md` page must include:

- `## Source Binding` with `Derived from spec`, `Related HTML`, and
  `Authority status` fields.
- Reader sections for what the feature does, why the project needs it, how it
  works, what it is not, diagram reading guidance, source authority, external
  AI navigation, next steps, and all source materials.
- Every source material declared by the matching source spec.
- Every Mermaid block declared by the matching source spec, unless a later
  contract explicitly records a different synchronization rule.
- A compact external-AI navigation card that states safe uses, pre-modification
  inspection requirements, and forbidden uses.

The following source-spec headings must not appear as reader-facing top-level
GitHub page sections:

- `Rendering Intent`
- `Required Visual Structure`
- `Required Content Blocks`

## Validator Binding

`scripts/project_control/audit_documentation_surfaces.py` owns the deterministic
checks for this contract. The audit must verify source-spec existence, related
HTML existence, source binding declarations, required reader sections, source
material coverage, Mermaid synchronization, external-AI navigation markers,
stale nested-path references, and unsafe authority or physics-promotion
phrasing.

## Operational Rule

When a registered explainer spec changes, update the related GitHub-facing page
as a reader-facing derivative. Preserve the source-spec metadata and renderer
instructions in `markdown/html-explainer-specs/`; translate them into finished
explanatory prose in `github-facing/`.
