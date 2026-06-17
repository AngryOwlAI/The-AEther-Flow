---
name: aether-teaching-explainer
description: Use when enriching AEther Flow source-backed explainers with a Documentation Curator teaching loop, including lay Student questions, expert Teacher answers, curated teaching packets, Markdown explainer specs, GitHub-facing Markdown, and tracked human-only HTML. Do not use for canonical physics claims, role/schema/validator changes outside an authorized project-system AgentJob, or generated HTML as authority.
---

# Aether Teaching Explainer

Use this skill only inside a bounded Documentation Curator or authorized
project-system AgentJob.

## Inputs

- Selected feature slug.
- Source spec path under `markdown/html-explainer-specs/`.
- Allowed source materials from that spec.
- Claim boundary.
- Target teaching packet, GitHub-facing Markdown, and HTML output paths.

## Workflow

1. Curator selects the feature and source bundle.
2. Run Documentation Student Round 1 for lay-reader questions.
3. Run Documentation Teacher Round 1 for source-bound answers.
4. Run Documentation Student Round 2 using the Round 1 answers as context.
5. Run Documentation Teacher Round 2 for follow-up answers.
6. Curator creates or updates `markdown/teaching-packets/<slug>.teaching-qa.md`.
7. Curator updates the Markdown explainer spec.
8. Curator regenerates the tracked HTML explainer from the spec.
9. Curator updates the GitHub-facing Markdown explainer.
10. Curator runs validators and writes documentation-impact evidence.

Use the Student and Teacher sequentially. Round 2 depends on Round 1 answers.

For revamp work, treat existing generated HTML and GitHub-facing Markdown as
derivative evidence of what may be stale or confusing. Do not let their titles,
section names, or old prose decide what should be taught. The Curator should
start from the project component, its source bundle, its functionality, and the
reader problem the explanation must solve.

## Student Contract

The Student asks questions only. It may not answer, summarize, modify files,
introduce external facts, or treat generated docs as authority.

Student questions should target the project subject, not the future page. Ask
what the subject does, why the project needs it, how it works, where confusion
or misuse is likely, what examples and non-examples clarify it, and what
authority boundary protects the reader.

## Teacher Contract

The Teacher answers only from the selected source bundle. Each answer must
include:

- Plain answer.
- Technical anchor.
- Source paths used.
- Boundary note.
- Curator note.

If a source does not answer a question, write `Source gap: not answered by the
selected source bundle.`

Teacher answers should answer the functional project question directly. Do not
answer by saying what an explainer page will contain, how a renderer will lay it
out, or what the page is called.

## Curator Synthesis

Teaching packets are explanatory support only. The Curator distills them into
finished reader-facing documentation. Do not paste raw Q&A verbatim unless that
is the clearest format for the page.

The Curator synthesis must be subject-first. The first explanatory block should
describe the actual project component and its role in the physics research
system or AI research-agent system. Source-binding and nonauthority warnings
should support the explanation, not replace it.

For teaching-enabled specs, include a `teaching_loop` frontmatter block and a
`## Teaching Q&A Basis` section naming the packet path and non-authority rule.

## Non-Authority Rule

Teaching packets never override source materials, registries, schemas, role
contracts, validators, routing, canonical science, or generated-output
boundaries. They are curated explanatory support.

## Validation

Run:

```zsh
.venv/bin/python scripts/validate_teaching_qa.py --root .
.venv/bin/python scripts/spec_depth_lint.py --root .
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```
