# Documentation Curator Teaching Loop

The Documentation Curator teaching loop uses reader questions and source-bound answers to make explainers clearer without making teaching packets or generated pages authoritative.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/documentation-curator-teaching-loop-explainer.md`
- **Related HTML:** `html/documentation-curator-teaching-loop-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The Documentation Curator teaching loop is the project's method for making source-backed explainers easier to understand without weakening authority boundaries. The Curator chooses a subject and source bundle, then uses a Documentation Student to ask plain reader-centered questions and a Documentation Teacher to answer those questions inside the declared source bundle. The Curator reviews the exchange, writes or updates a curated Teaching Q&A packet, and distills that packet into the Markdown source spec, GitHub-facing Markdown, and tracked human-only HTML derivative. The loop is subject-first: it must explain what the project component does, why the project needs it, how it works, what it can and cannot claim, and where a reader should go next. It does not let generated pages, teaching packets, Student questions, or Teacher answers become independent authority.

## What This Feature Does

The loop makes documentation more teachable. Student questions expose confusion, Teacher answers stay inside the source bundle, and the Curator turns the exchange into curated explanatory support. The final tracked outputs remain source specs, GitHub-facing Markdown, HTML derivatives, and documentation-impact records, all governed by the Curator's authority boundary.

## Why The Project Needs It

The project contains speculative physics, agent-control machinery, generated memory surfaces, and many authority distinctions. Readers can misunderstand those distinctions even when every file is technically correct. The teaching loop gives the Curator a structured way to find and repair confusion while preserving source authority.

## How It Works

The Curator selects one feature and source bundle. The Student asks reader-centered questions. The Teacher answers each question plainly, names source paths, marks gaps, and adds boundary notes. The Curator synthesizes a Teaching Q&A packet with required fields and sections, then distills the packet into source specs, GitHub-facing Markdown, and HTML. Validators check packet structure and source-bound behavior.

## Workflow Step Inspector

1. Select one subject and source bundle.
2. Ask reader-centered Student questions about purpose, operation, boundaries, examples, and confusion points.
3. Answer those questions through the Teacher inside the declared source boundary.
4. Have the Curator synthesize a teaching packet as explanatory support.
5. Distill the packet into the Markdown source spec.
6. Synchronize the GitHub-facing Markdown derivative.
7. Regenerate the tracked human-only HTML derivative.
8. Validate teaching QA, source specs, derivatives, documentation impact, and research-control state.

## What It Is Not

It is not a new source of project authority, not a role-authority expansion, not a schema or validator change by itself, and not a way for Student or Teacher outputs to write tracked documentation directly. Teaching packets support explanation; they do not change physics claims, routing, validators, role contracts, schemas, or generated-output boundaries.

## Diagram Reading Guide

No Mermaid diagram is required for this explainer. Read the process as a teaching lifecycle: source bundle, Student questions, Teacher answers, Curator synthesis, source-spec distillation, derivative refresh, and validation.

## Source Authority

Authority comes from the Documentation Curator role, Student and Teacher role contracts, the Teaching Q&A packet schema, the teaching explainer skills, the GitHub-facing explainer contract, curated packets, and validators. This derived Markdown is orientation only.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize the teaching loop for orientation
- identify the role contracts, schema, skills, packets, and validators to inspect
- distinguish explanatory support from authority

Before modifying project knowledge:
- inspect the selected source spec and source bundle
- inspect the Curator, Student, and Teacher contracts
- validate any teaching packet with `scripts/validate_teaching_qa.py --root .`
- update the source spec before refreshing generated derivatives

Do not:
- do not treat a Teaching Q&A packet as canonical authority
- do not let Student or Teacher outputs write tracked docs directly
- do not cite generated HTML, wiki notes, PDFs, or `.local/` output as authority
- do not use renderer format as a substitute for curator judgment about functionality coverage

## Where To Go Next

- Read roles and skills for the broader role catalog.
- Read source authority before citing generated surfaces.
- Read project overview for the subject-first documentation tone.
- Inspect existing teaching packets before adding another teaching-enabled explainer.

## All Source Materials

- `.agents/roles/research_ops/documentation-curator.v0.9.0.md`
- `.agents/roles/research_ops/documentation-student.v0.1.0.md`
- `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`
- `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`
- `.codex/skills/aether-teaching-explainer/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `research_control/design/github_facing_explainer_contract.md`
- `markdown/teaching-packets/project-overview.teaching-qa.md`
- `markdown/teaching-packets/role-routing.teaching-qa.md`
- `scripts/validate_teaching_qa.py`
