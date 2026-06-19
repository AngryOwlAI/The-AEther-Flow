# Documentation Curator Publication Process

AEther-Flow public documentation is written through the Documentation Curator
Publication Process. The process exists because a structurally valid page can
still be weak documentation: it can repeat a template, hide the subject behind
metadata, add generic diagrams, or imply that generated reader surfaces carry
authority they do not have.

This page is a generated noncanonical reader surface. It explains how public
pages are planned, written, reviewed, and checked. It does not change role
authority, validator behavior, schemas, routing, checkpoint gates, source
authority, generated-output authority, corpus-migration approval, or physics
claim status.

## The Publication Job

The active process treats each GitHub-facing Markdown page and tracked HTML
explainer as a publication artifact with a specific reader job. A page might
be a workflow guide, reference catalog, boundary map, overview article, or
operator guide. The document type is chosen because it fits the subject, not
because every page must share a section skeleton.

The authority spine remains unchanged. Registered TeX carries physics and
derivational claims. Registries carry routing, provenance, generated-output
tracking, and memory metadata. Registered Markdown carries guidance, source
specs, briefs, role contracts, skill contracts, and control notes. GitHub
Markdown, tracked HTML, wiki notes, PDFs, semantic extracts, Obsidian notes,
and `.local` caches remain derivative or retrieval surfaces.

## Brief First

Every migrated or new public page starts with a publication brief under
`markdown/publication-briefs/` and a row in
`registries/PUBLICATION_BRIEF_REGISTRY.csv`. The brief defines the subject,
reader, reader job, document type, reading experience, narrative structure,
visual strategy, source basis, authority boundaries, output surfaces,
acceptance criteria, and forbidden patterns.

That brief is the quality-control surface. It is not a physics source, and it
does not make generated outputs authoritative. Its function is narrower and
more practical: it prevents a public page from being generated as a generic
transcript, a validator exercise, or a diagram with weak subject matter.

## Write For The Medium

GitHub Markdown and tracked HTML do not need identical section order. They do
need the same source basis, authority boundary, and core claims.

GitHub Markdown should read as a native technical article. It should open with
the subject and reader problem, use page-specific headings, cite source paths,
and avoid carrying HTML layout structure into Markdown.

Tracked HTML should use the medium's strengths: standalone layout, readable
hierarchy, responsive behavior, source grounding, and human-only visual
structure. It must be single-file and no-network. It must not rely on remote
scripts, remote fonts, analytics, browser-side Mermaid execution, local
server bridges, or package-runner artifacts.

## Visuals Are Reader Work

A visual strategy is optional. When a page uses a visual, the visual must
teach something concrete about that page's subject. A process timeline can
explain a lifecycle. A source matrix can show authority boundaries. A role
matrix can compare execution contracts. A decision tree can help an operator
choose the right lane.

A diagram that could be dropped into any unrelated page is a failure of the
publication process. The active Documentation Curator role explicitly rejects
diagram-for-validator behavior and old universal headings.

## Review Evidence

A reviewed publication page needs more than files. It needs evidence:

| Evidence | Purpose |
| --- | --- |
| Publication brief | Defines the reader job and acceptance criteria. |
| Source spec | Binds the derivative outputs to source materials and claim boundaries. |
| GitHub-facing Markdown | Provides a native public Markdown article. |
| Tracked HTML | Provides a standalone human visual derivative. |
| Desktop and mobile screenshots | Check that the HTML page is readable and responsive. |
| Before/after review | Explains what improved and what risks remain. |
| Publication validator | Checks mechanical process failures and known anti-patterns. |

`scripts/validate_publication_process.py` checks source integrity,
brief/spec/output consistency, visible source paths, authority-boundary
language, no-network HTML, screenshot evidence, duplicate section skeletons,
and retired-process patterns. It does not certify taste, clarity, or reader
value by itself. The before/after review remains necessary because editorial
quality is partly judgment-based.

## Retired Paths

The active publication process replaced the older Visual Atlas-style path. The
retired path must not return as a fallback.

Do not migrate this way:

- do not force every page into old universal section headings;
- do not use a topic registry as the active creation path;
- do not treat teaching packets as active public-page source;
- do not add a diagram because a script rewards diagrams;
- do not open public pages with source metadata before the subject;
- do not treat validator PASS as publication quality by itself; and
- do not treat generated HTML, GitHub Markdown, wiki notes, Obsidian notes,
  semantic extracts, or `.local` caches as authority.

The accepted pilot evidence in
`research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md`
shows the intended standard: Project Overview became a compact front door, and
Source Authority became a boundary map. They were not forced into the same
visible structure.

## Source Materials

- AEther-Flow Project. (2026). `research_control/design/documentation_curator_publication_process.md` [Publication process control note].
- AEther-Flow Project. (2026). `.agents/roles/research_ops/documentation-curator.v2.0.0.md` [Documentation Curator role contract].
- AEther-Flow Project. (2026). `markdown/publication-briefs/README.md` [Publication brief guidance].
- AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv` [Publication brief registry].
- AEther-Flow Project. (2026). `scripts/validate_publication_process.py` [Publication process validator].
- AEther-Flow Project. (2026). `research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md` [Requirement audit].
- AEther-Flow Project. (2026). `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md` [Pilot before/after review].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/documentation-curator-publication-process-explainer.md`
- **Related HTML:** `html/documentation-curator-publication-process-explainer.html`
- **Publication brief:** `markdown/publication-briefs/documentation-curator-publication-process.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: the Documentation Curator Publication Process starts from a
page-specific brief, writes for the chosen medium, grounds all outputs in
source paths, records screenshot and review evidence, and uses deterministic
checks as boundary protection rather than as a substitute for editorial
judgment.

Unsafe summary: public pages are generated from a universal template,
teaching-packet transcript, topic-registry recipe, or validator PASS alone.
