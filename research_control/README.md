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
