# Technical Requirements

Technical requirements separate the tools needed to read, validate, regenerate, render, retrieve, and refresh derivatives.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/technical-requirements-explainer.md`
- **Related HTML:** `html/technical-requirements-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The technical requirements explainer describes the local runtime, package, validation, rendering, retrieval, and derivative-build requirements needed to inspect or regenerate project surfaces safely. Its function is to separate read-only inspection, Python validator execution, memory and wiki regeneration, governed Mermaid inline-SVG rendering, local Obsidian or semantic retrieval, and LaTeX/PDF refresh into distinct tiers. This matters because not every reader needs every tool, and optional operator aids such as Obsidian or global Codex plugins should not be mistaken for project authority. The requirements map turns setup files and skill contracts into a practical dependency model for maintainers who need repeatable validation without changing dependency policy or scientific claims.

## What This Feature Does

Technical requirements define which tools are needed for each workflow tier.

## Why The Project Needs It

The project needs tiers because reading, validating, regenerating HTML, querying memory, and refreshing PDFs require different environments.

## How It Works

Use read-only tools for inspection, Python for validators and memory scripts, Node/Mermaid tooling for diagram-backed HTML, optional local tools for retrieval, and LaTeX only for PDF refresh.

## What It Is Not

It is not a dependency-policy change, not proof that optional tools are authority, and not a requirement that every reader install every aid.

## Diagram Reading Guide

The important visual model is the tier matrix: read, validate, regenerate memory, render diagrams, retrieve locally, refresh PDFs, and separate project requirements from operator aids.

## Source Authority

Authority comes from README setup guidance, requirements, Makefile targets, and repo-local skill contracts.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize the feature for orientation
- identify source files to inspect next
- explain workflow boundaries in plain language

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this derivative as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Install Python requirements before running validators.
- Install diagram tooling only when regenerating diagram-backed HTML.
- Use source authority when local tools disagree with tracked state.

## All Source Materials

- `README.md`
- `requirements.txt`
- `Makefile`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`
- `.codex/skills/pdf-derivative-build/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package.json`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package-lock.json`
