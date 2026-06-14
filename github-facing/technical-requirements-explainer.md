# Technical Requirements

This page turns setup into workflow tiers so readers know which tools are required for inspection, validation, regeneration, local retrieval, diagram rendering, and PDF refresh.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/technical-requirements-explainer.md`
- **Related HTML:** `html/technical-requirements-explainer.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

The requirements page separates project requirements from operator environment aids. It tells readers what is needed for read-only inspection, Python validators, memory/wiki regeneration, Mermaid-backed HTML, optional local retrieval, and conditional PDF builds.

## Why The Project Needs It

Not every reader needs every tool. Missing Obsidian should not invalidate the project, while missing Python dependencies can block validators. Tiering prevents optional conveniences from being mistaken for repository requirements.

## How It Works

Requirement tiers:

| Tier | Needed for | Tools | Failure meaning |
| --- | --- | --- | --- |
| 1. Read-only inspection | reading sources | Git, editor, browser or Markdown viewer | does not affect project validity |
| 2. Validators and memory scripts | deterministic checks | Python `.venv`, `requirements.txt` | blocks validation if unavailable |
| 3. Memory/wiki regeneration | source-to-registry refresh | project-memory-system scripts | generated surfaces may be stale |
| 4. Mermaid-backed HTML | inline-SVG tracked explainers | Node.js, npm, pinned Mermaid, Playwright Chromium | HTML diagram refresh may be blocked |
| 5. Local retrieval | optional reader/search aids | Obsidian, SQLite, `.local/` extracts | operator aid unavailable, not source invalid |
| 6. PDF refresh | TeX derivatives | LaTeX/PDF build tooling | only blocks in-scope PDF derivative work |

## What It Is Not

It is not a new dependency policy, not a guarantee every optional local aid exists, not permission to treat global plugins as project authority, and not a physics or control claim.

## Diagram Reading Guide

The current source spec does not declare a Mermaid diagram. Read the tier matrix as the controlling visual model: each tier states tools, commands, need, failure meaning, and authority status.

No Mermaid diagram is declared in the current registered source spec for this page.

## Source Authority

The requirements are grounded in `README.md`, `requirements.txt`, `Makefile`, project-memory-system, Obsidian, PDF derivative, HTML visual explainer, and Mermaid documentation scripts.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- For reading, start with Markdown and registries.
- For validation, use the Python `.venv` and README commands.
- For HTML diagram refresh, inspect Mermaid package files and rendering scripts.
- For PDFs, refresh only when TeX derivative work is in scope.

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
