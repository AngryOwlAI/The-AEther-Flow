<!-- authority: control -->

# GitHub-Facing Explainer Contract

## Purpose

The root `github-facing/*.md` files are noncanonical, source-backed reader
surfaces for humans and external AI reading the repository on GitHub. They are
paired with registered source specs under `markdown/html-explainer-specs/` and
may have tracked HTML derivatives under `html/`.

The active presentation model is the Documentation Curator Publication
Process. GitHub-facing pages must be written as native Markdown articles,
guides, references, or boundary maps designed from a page-specific publication
brief when the page has migrated.

## Authority

GitHub-facing Markdown may orient readers, summarize source-backed behavior,
name source files, and explain workflow boundaries. It must not define physics
claims, alter control behavior, replace registry rows, expand role authority,
or become independent source authority.

The authority ladder remains:

1. Registered TeX files define physics and derivational claims.
2. Registries define routing, provenance, generated-output tracking, and
   agent-queryable memory.
3. Registered Markdown defines front-door guidance, publication briefs, source
   specs, and project-control notes.
4. GitHub-facing Markdown, HTML explainers, wiki notes, PDFs, semantic
   extracts, Obsidian notes, and local retrieval surfaces are derivative or
   orientation surfaces.

## Required Safety Contract

Each active GitHub-facing page must include:

- a useful subject framing before source metadata;
- visible source grounding;
- a clear non-authority boundary;
- a complete source-material reading path; and
- page-specific navigation guidance for humans or external AI.

For migrated pages, the source basis and authority boundary must match the
publication brief and the paired source spec. The visible structure may differ
from the HTML derivative.

## Publication Standard

The Curator chooses the Markdown shape from the brief. A page may be an
overview article, concept explainer, workflow guide, lifecycle guide,
reference catalog, troubleshooting guide, visual brief, comparison map, or
operator guide.

Do not force every page into the same visible headings. The old universal
sequence `What This Does`, `Why AEther Needs It`, and `System Map` is forbidden
on migrated pages unless the publication brief explicitly authorizes an
individual heading.

If the Markdown includes a diagram, the surrounding prose must explain what
the reader should learn from it. Decorative or reusable stock diagrams fail
publication review.

## Teaching Loop Boundary

Teaching-loop packets may shape the Curator's synthesis. Raw
Student/Teacher transcript structures do not belong in public GitHub pages.

## Validator Binding

The active publication validator is:

```zsh
.venv/bin/python scripts/validate_publication_process.py --root .
```

It checks source sync, authority boundaries, no external runtime dependencies,
brief conformance, duplicate skeletons, generic visuals, forbidden migrated
headings, screenshot evidence for pilots, and migration status. Advisory
warnings remain advisory. Editorial quality requires a human-facing review
artifact.

## Operational Rule

When a migrated source spec or brief changes, update the related GitHub-facing
page as a reader-facing derivative. Inspect the source bundle first. Use old
generated prose only as failure evidence. Preserve source paths and claim
boundaries, but choose the section structure that best serves the brief.
