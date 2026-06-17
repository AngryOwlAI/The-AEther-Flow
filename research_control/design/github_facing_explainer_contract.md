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

GitHub-facing pages must be subject-first. Their main prose should describe the
project component, workflow, role, authority boundary, or technical function
that the page is responsible for teaching. The page should not primarily
describe itself, its title, its renderer, its layout, its source spec, or its
status as a GitHub-facing file. Source binding and authority warnings remain
required, but they support the explanation rather than replacing it.

The authority ladder remains:

1. Registered TeX files define physics and derivational claims.
2. Registries define routing, provenance, generated-output tracking, and
   agent-queryable memory.
3. Registered Markdown defines front-door guidance, source specs, and
   project-control notes.
4. GitHub-facing Markdown, HTML explainers, wiki notes, PDFs, and local
   retrieval surfaces are derivative or orientation surfaces unless another
   registered source explicitly gives them narrower authority.

## Required Safety Contract

Each `github-facing/*.md` page must include:

- `## Source Binding` with `Derived from spec`, `Related HTML`, and
  `Authority status` fields.
- Every source material declared by the matching source spec.
- Every Mermaid block declared by the matching source spec, unless a later
  contract explicitly records a different synchronization rule.
- A visible non-authority boundary sufficient for humans and external AI to
  understand that the file is an explanatory derivative.
- A complete source-materials reading path.

The following are recommended reader devices, not canonical section law:

- what the subject does;
- why the project needs it;
- how it works;
- what it does not authorize;
- Student/Teacher-style questions and source-bound answers;
- workflow-step inspectors where the subject is a workflow or control process;
- diagram reading guidance;
- external-AI navigation guidance; and
- next-reading guidance.

The Documentation Curator decides which of these devices best teaches the
subject. A script may warn when a recommended device is absent, but absence of
one old section heading is not by itself a contract failure.

The following source-spec headings must not appear as reader-facing top-level
GitHub page sections:

- `Rendering Intent`
- `Required Visual Structure`
- `Required Content Blocks`

## Validator Binding

`scripts/project_control/audit_documentation_surfaces.py` owns the deterministic
checks for the safety contract. The audit must fail on source-spec absence,
related HTML absence, incorrect source binding declarations, missing source
materials, missing synchronized source-spec Mermaid blocks, renderer-only
source-spec headings made reader-visible, stale nested-path references, and
unsafe authority or physics-promotion phrasing.

The audit may emit guidance warnings for missing recommended section devices,
including workflow-step inspector sections or external-AI navigation markers.
Those warnings are not project authority over the Curator's prose or page
structure.

## Operational Rule

When a registered explainer spec changes, update the related GitHub-facing page
as a reader-facing derivative. Preserve the source-spec metadata and renderer
instructions in `markdown/html-explainer-specs/`; translate them into finished
explanatory prose in `github-facing/`.

When a GitHub-facing page has drifted into self-description or mechanical
template compliance, the correct operation is a source-backed reset: inspect
the registered spec and source bundle, use Student/Teacher-style questions to
identify what the reader needs to understand, ignore the old derivative prose
except as failure evidence, and write the page as a functional explanation of
the subject.
