<!-- authority: control -->

# Documentation Curator Publication Process

## Purpose

This is the active public-documentation presentation standard. It treats each
GitHub-facing Markdown page and tracked HTML explainer as a source-backed
publication artifact: a technical article, visual brief, workflow guide,
reference catalog, boundary map, or operator guide designed for a specific
reader job.

## Authority Spine

The source hierarchy is unchanged:

1. Registered TeX files carry physics and derivational claims.
2. Registries carry routing, provenance, generated-output tracking, and
   agent-queryable memory.
3. Registered Markdown carries front-door guidance, source specs, publication
   briefs, role and skill contracts, and project-control notes.
4. GitHub-facing Markdown, tracked HTML, wiki notes, PDFs, semantic extracts,
   Obsidian notes, and `.local/` caches remain derivatives or retrieval aids.

Public documentation may orient, teach, and warn. It must not create physics,
ontology, routing, role, validator, benchmark, Gate Chair, write-permission, or
generated-output authority.

## Required Brief

Every migrated or new explainer needs a publication brief under
`markdown/publication-briefs/` and a registry row in
`registries/PUBLICATION_BRIEF_REGISTRY.csv`.

Required brief fields:

- subject;
- reader;
- reader job;
- intended reading experience;
- document type;
- narrative structure;
- visual strategy;
- source basis;
- claim and authority boundaries;
- output surfaces;
- page-specific acceptance criteria; and
- forbidden patterns.

The brief is a control surface for quality expectations. It is not a physics
source and does not promote generated derivatives to authority.

## Document Types

Use controlled document types, not controlled headings:

- overview article;
- concept explainer;
- workflow guide;
- decision or lifecycle guide;
- reference catalog;
- troubleshooting guide;
- visual brief;
- comparison or boundary map; and
- contributor or operator guide.

Headings are page-local editorial decisions. Repeated skeletons across
unrelated subjects require an explicit brief authorization. Otherwise,
duplicated section order is a publication-process failure.

## Visual Strategy

A page may omit diagrams. Allowed visual strategies include no diagram,
bespoke Mermaid diagram, annotated table, process timeline, source matrix, role
matrix, decision tree, state model, layered architecture, and custom HTML
visual. Every major visual must say what the reader learns from it and name its
source basis.

Generic diagrams that could appear on many unrelated pages fail review. A
stock flow from source bundle to validation is not sufficient.

## Output Synchronization

HTML and GitHub Markdown may diverge in visible structure. They must share the
same source basis, authority boundary, and core claims, but they should use the
medium's strengths:

- GitHub Markdown should read as a native article.
- HTML should use polished standalone layout, readable hierarchy, semantic
  headings, source grounding, and mobile-safe responsive behavior.

Tracked HTML must be single-file and no-network. It must not use NPX, CDN
scripts, remote fonts, remote CSS, external analytics, hosted comments,
browser-side Mermaid execution, localhost bridge artifacts, or network-required
assets.

## Pilot Rule

The publication process is pilot-first. One or two pages must be rebuilt,
reviewed, screenshot-verified, and accepted as the quality bar before any
corpus-wide migration. The default pilots are Project Overview and Source
Authority.

Corpus-wide regeneration requires explicit user approval after pilot review.
Until then, the registry must mark every page as migrated, reviewed, or
deferred.

## Validation

The active deterministic validator is:

```zsh
.venv/bin/python scripts/validate_publication_process.py --root .
```

It checks source integrity, authority boundary integrity, no external runtime,
publication brief conformance, duplicate section skeletons, generic visual
detection, retired universal headings for migrated pages, screenshot evidence
for pilots, migration status, and generated-output boundaries.

Warnings are advisory. Hard failures are reserved for authority, source sync,
runtime safety, brief mismatch, migration-state, and known anti-pattern
violations. Editorial quality still requires a human-facing review artifact.

## Rollback

If a publication migration fails, keep canonical source authority intact:

1. Restore the affected publication brief and source spec from version control.
2. Restore only the affected GitHub Markdown and tracked HTML derivatives.
3. Mark the page `deferred` in the registries.
4. Re-run bootstrap, publication validation, documentation-impact validation,
   and research-control validation.

Do not restore a retired universal-section process without an explicit
project-system decision.
