# GitHub-Facing Markdown Reset Audit

## Objective

Reset the root `github-facing/*.md` layer so it functions as source-backed
reader documentation instead of a rigid template mirror. The reset covers all
13 registered GitHub-facing explainers and the validator contract that had
been enforcing old section headings as hard law.

## Contract Change

The hard audit contract now keeps the safety-critical checks:

- matching source spec exists;
- related tracked HTML path exists;
- `Source Binding` declares the correct source spec, related HTML, and
  `generated_noncanonical` authority status;
- every source material declared by the source spec is present in the
  GitHub-facing source-materials section;
- every Mermaid block declared by the source spec is synchronized into the
  GitHub-facing page;
- renderer-only source-spec headings are not exposed as reader-facing
  GitHub headings;
- stale `docs/github-facing` references remain blocked; and
- unsafe authority or physics-promotion phrases remain blocked.

The old fixed reader-section template and exact external-AI card markers are
now guidance warnings. Missing an old section name is not a transaction
failure when the Documentation Curator has chosen a different source-backed
teaching shape.

## Document Rebuild

All 13 root GitHub-facing Markdown documents were deleted and replaced with
new files at the same paths:

- `github-facing/project-overview-explainer.md`
- `github-facing/aether-flow-ontology-explainer.md`
- `github-facing/research-agent-workflow-explainer.md`
- `github-facing/role-routing-explainer.md`
- `github-facing/claim-gates-explainer.md`
- `github-facing/source-authority-explainer.md`
- `github-facing/research-control-system-explainer.md`
- `github-facing/memory-system-explainer.md`
- `github-facing/roles-and-skills-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`
- `github-facing/project-system-improvement-explainer.md`
- `github-facing/documentation-curator-teaching-loop-explainer.md`
- `github-facing/technical-requirements-explainer.md`

The replacement pages use subject-first explanations, Student/Teacher-style
questions and source-bound answers, source-backed diagrams, workflow step
inspectors where the source subject is a workflow or control process, and
explicit GitHub-reader/AI-agent boundaries.

## Boundary

No canonical ontology, benchmark source, science draft, role contract, schema
contract, routing behavior, or tracked HTML derivative was edited. Generated
GitHub-facing Markdown remains noncanonical and explanatory only.
