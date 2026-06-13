# The AEther-Flow Documentation Context

This glossary defines project-specific documentation language used when
designing human-facing explanatory surfaces.

## Language

**GitHub-facing Markdown System**:
A registered Markdown documentation layer under root `github-facing/` for readers and external AI agents browsing the repository on GitHub; it mirrors the body of the existing explainer specs without their YAML metadata headers, is canonical for GitHub-facing explanation, and is non-authoritative for physics claims and control decisions.
_Avoid_: Front-facing GitHub files, GitHub system, generated HTML explainer, generated mirror

**GitHub-facing Spec Mirror**:
The root `github-facing/*.md` files that preserve the readable body content of `markdown/html-explainer-specs/*.md` for GitHub browsing while leaving source-spec metadata, HTML generation, and authority tracking in the registered spec and registry layers.
_Avoid_: Source manifest, generated-output registry, HTML explainer registry

**Subject Summary**:
A source-backed summary section titled `Summary of [Subject]` that states what
the subject is, what functionality or role it has, why it matters to the
project, how it fits the surrounding research or project-control system, and
which declared source materials ground the summary before detailed explanation
begins.
_Avoid_: Reader orientation, description-only preface
