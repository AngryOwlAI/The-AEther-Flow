# The AEther-Flow Documentation Context

This glossary defines project-specific documentation language used when
designing human-facing explanatory surfaces.

## Language

**GitHub-facing Markdown System**:
A generated, source-backed Markdown documentation layer under root
`github-facing/` for readers and external AI agents browsing the repository on
GitHub. Each page is derived from a registered source spec under
`markdown/html-explainer-specs/` and is noncanonical: it orients readers, but
it is not authority for physics claims, control decisions, routing,
validators, role contracts, schemas, or registries.
_Avoid_: Front-facing GitHub files, GitHub system, generated HTML explainer, generated mirror

**GitHub-facing Explainer**:
The root `github-facing/*.md` files that provide reader-facing explanations
derived from `markdown/html-explainer-specs/*.md` for GitHub browsing. They
are allowed to be clearer than a body-only spec mirror when Curator judgment
requires it, but source-spec metadata, HTML generation, and authority tracking
remain in the registered spec and registry layers.
_Avoid_: Source manifest, generated-output registry, HTML explainer registry

**Advisory Formatting Guidance**:
Renderer templates, spec-depth lint, HTML audit, and GitHub-facing structure
checks guide consistency, depth, source evidence, and derivative validation.
They are quality controls, not canonical content law. The Documentation
Curator decides which project functionality needs coverage inside the bounded
AgentJob and source-authority constraints.
_Avoid_: Canonical format law, template authority, script-owned content

**Subject Summary**:
A source-backed summary section titled `Summary of [Subject]` that states what
the subject is, what functionality or role it has, why it matters to the
project, how it fits the surrounding research or project-control system, and
which declared source materials ground the summary before detailed explanation
begins.
_Avoid_: Reader orientation, description-only preface
