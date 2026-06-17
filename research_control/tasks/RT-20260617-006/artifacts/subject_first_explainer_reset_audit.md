# Subject-First Explainer Reset Audit

## Scope

`RT-20260617-006` corrected a systematic documentation failure in which
GitHub-facing Markdown and tracked HTML derivatives explained their own page
structure more than the project functionality they were meant to teach.

## System Changes

- Superseded `documentation-curator@0.8.0` and registered
  `documentation-curator@0.9.0`.
- Added a subject-first rule to Documentation Curator, teaching-loop, HTML
  explainer, and GitHub-facing Markdown contracts.
- Added advisory depth-lint checks for self-referential explainer prose.
- Updated reader-layer search copy from self-referential search wording to
  subject-neutral content search wording.

## Content Changes

- Reset all ten registered HTML source specs around direct project
  functionality.
- Rewrote all ten root `github-facing/*.md` pages as subject-first reader
  explainers.
- Re-rendered all ten tracked `html/*.html` derivatives with concrete
  content-block prose.
- Added `markdown/teaching-packets/project-overview.teaching-qa.md` and linked
  it from the project-overview source spec.

## Boundaries Preserved

- No canonical ontology source changed.
- No science draft changed.
- No physics claim was promoted.
- No Gate Chair verdict was issued.
- Generated HTML and GitHub-facing Markdown remain noncanonical derivatives.
- Teaching packets remain explanatory support only.
