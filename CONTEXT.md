# The AEther-Flow Documentation Context

This glossary defines project-specific documentation language used when
designing human-facing explanatory surfaces.

## Language

**GitHub-facing Markdown System**:
A registered, hand-authored Markdown documentation layer under `docs/github-facing/` for readers and external AI agents browsing the repository on GitHub; it is canonical for GitHub-facing explanation, non-authoritative for physics claims and control decisions, source-backed by existing explainer specs, and tracked by a manifest.
_Avoid_: Front-facing GitHub files, GitHub system, generated HTML explainer, generated mirror

**GitHub-facing Source Manifest**:
The `docs/github-facing/SOURCE_MANIFEST.md` traceability file that maps each GitHub-facing Markdown page to its source materials, source-backed scope, and authority boundary.
_Avoid_: Mirror manifest, generated-output registry, HTML explainer registry

**Subject Summary**:
A source-backed summary section titled `Summary of [Subject]` that states what
the subject is, what functionality or role it has, why it matters to the
project, how it fits the surrounding research or project-control system, and
which declared source materials ground the summary before detailed explanation
begins.
_Avoid_: Reader orientation, description-only preface
