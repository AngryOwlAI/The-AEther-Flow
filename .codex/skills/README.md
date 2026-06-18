<!-- authority: explanatory -->

# Repo-Local Skills

This folder contains project-local Codex skills. Skills define how agents
should perform recurring workflows inside this repository.

## Primary Skill Groups

- `continue-research/` routes one bounded physics or research-control
  continuation packet from tracked state.
- `improve-project-system/` routes one bounded project-system improvement
  packet.
- `project-memory-system/`, `markdown-wiki/`, `obsidian-wiki/`, `tex-wiki/`,
  and `pdf-derivative-build/` operate source-first memory, registry, wiki, and
  derivative surfaces.
- `html-visual-explainer/` and `visual-explainer/` support source-backed
  human-only visual explainers from publication briefs.
- `user-modified-project/` classifies human-made local edits before routing
  them into the correct controlled workflow.

## What Belongs Here

- `SKILL.md` files that define project-local workflow contracts.
- Skill subfolders and helper files when the skill owns them.

## What Does Not Belong Here

- Task-local outputs or receipts.
- Generated wiki notes, generated HTML, or local scratch caches.
- Physics derivations unless a skill explicitly owns a source-generation
  workflow.

## Authority Boundary

Skill contracts are project-control authority for how a recurring workflow is
performed. They do not promote scientific claims and do not override task
allowlists, role contracts, validators, or human gates.
