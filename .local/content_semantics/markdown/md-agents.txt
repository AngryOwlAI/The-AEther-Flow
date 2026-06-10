<!-- authority: control -->

# AGENTS.md

Root project guidance for agents working in `The Æther-Flow Interpretation of Relativity Research Project`.

## Project Identity

This repository has two linked missions:

1. Physics research: maintain `The Æther-Flow Interpretation of Relativity` as
   an exact-GR benchmark while treating first-principles GR derivation from
   `Æther` / `Æther-flow` substrate structure as open until authorized gates
   establish it.
2. AI research-agent development: agentice theoretical physics workflow using routing, 
   refutation, novelty search, claim gates, manuscript memory, negative-result preservation.

## Authority Hierarchy

Use the repository memory system before making project-knowledge changes.

1. Registered `.tex` files are canonical for physics research and derivational claims.
2. Format-specific registries under `registries/` are canonical for routing, provenance, generated-output tracking, and agent-queryable memory.
3. Registered Markdown files are canonical for README/front-door material, agent guidance, and project-control notes.
4. PDFs, generated wiki notes, generated wiki indexes, `FILE_OBJECT_REGISTRY.csv`, `WIKI_ARTIFACT_REGISTRY.csv`, and HTML explainers are derivative artifacts.

Generated artifacts may be read by humans and agents, but they are not independent authority. Edit the canonical source and registry row, then regenerate.

## Research-Control Continuation

For research-control continuation, use `.codex/skills/continue-research/SKILL.md`
and tracked state under `research_control/`. The Director of Research may create
one bounded AgentJob per invocation after validation. Generated outputs and
`.local/` caches never override tracked control state.

## Project-System Improvement

For project-system repair, explanatory documentation synchronization,
control-markdown maintenance, validator work, memory-tooling updates, or
workflow clarification, use
`.codex/skills/improve-project-system/SKILL.md`. This workflow is separate
from physics continuation. It may process one project-improvement signal or
one deterministic classifier result per invocation, and it must not promote
physics claims or edit canonical science sources.

Use the deterministic classifier before deciding that documentation work is
needed:

```zsh
.venv/bin/python scripts/project_control/classify_project_changes.py --json
```

Documentation impact is a receipt requirement, not by itself a Documentation
Curator routing decision. If documentation impact is required, either update
the relevant canonical source documentation or write a valid
`research_control/tasks/<task_id>/documentation_impact.yaml` no-op rationale.

## Required Checks

Before changing repository knowledge, inspect the relevant source file and registry row. After changing source or registry material, regenerate and validate:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

For read-only validation, use:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Run smoke tests when changing memory-system scripts:

```zsh
.venv/bin/python -m unittest discover -s tests
```

Run the documentation-impact gate when changing project-system machinery:

```zsh
.venv/bin/python scripts/project_control/validate_documentation_impact.py
```

## Generated-Output Boundaries

- Do not hand-edit generated wiki notes under `wiki/`.
- Do not hand-edit generated master registries or generated registry metadata sidecars.
- Do not treat PDFs as independent scientific authority; they are human-reading derivatives from registered TeX.
- Do not add tracked HTML under `html/` unless it is generated from a registered
  Markdown source spec under `markdown/html-explainer-specs/`.
- Documentation Curator owns explanatory Markdown and source-backed human-only
  HTML visual explainers. Modify the source spec and regenerate the HTML;
  direct HTML-only edits remain blocked.
- Keep `.local/` for scratch builds, caches, previews, and experiments.
