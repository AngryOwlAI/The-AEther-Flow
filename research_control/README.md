# Research Control

This directory contains the tracked control spine for Director-led research
continuation.

## Authority Model

The Director writes a Director Decision Record. A role contract constrains the
selected execution context. An AgentJob defines allowed reads, writes, outputs,
validators, and claim boundaries. Validators enforce the boundaries. Human-gated
roles control promotion or closure.

## One-Job Rule

`/continue-research` may set up or execute at most one bounded AgentJob per
invocation. Normal flow writes a completion record and handoff after execution.

## Local Cache Boundary

Tracked files under `research_control/` are authority. `.local/` prompts,
logs, previews, and run caches are optional convenience artifacts only.

## Validation

```zsh
.venv/bin/python scripts/research_control/validate_research_control.py
```

Optional write-path diff validation:

```zsh
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
```

## Documentation Impact

Project-system changes use a separate documentation-impact gate. The
classifier decides whether changed paths affect how future humans or agents
understand, operate, validate, route, or extend the system:

```zsh
.venv/bin/python scripts/project_control/classify_project_changes.py --json
```

When documentation impact is required, the transaction must include either a
source documentation update or a valid
`research_control/tasks/<task_id>/documentation_impact.yaml` no-op rationale:

```zsh
.venv/bin/python scripts/project_control/validate_documentation_impact.py
```

Completions and handoffs may emit `project_improvement_signals`. Those signals
are recorded in `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` and are
processed by `.codex/skills/improve-project-system/SKILL.md`, one bounded
AgentJob at a time.
