<!-- authority: explanatory -->

# Research-Control Scripts

This folder contains scripts that operate the tracked research-control state
machine.

## Main Tools

- `continue_research.py` resolves the next bounded continuation packet from
  tracked state.
- `resolve_latest_handoff.py` reads the latest handoff chain.
- `validate_research_control.py` validates task records, registries, handoffs,
  parent-child synthesis constraints, and diff allowlists.
- `report_physics_progress_metrics.py` reports operational AI-science and
  research-system health metrics from tracked completions and registries.
- `checkpoint_research_transaction.py` regenerates, validates, stages, and
  commits a bounded transaction. It conditionally accepts generated
  project-improvement sidecar YAML/Markdown pairs only when the active
  AgentJob already allows the changed source YAML that references the sidecar.
- `strict_yaml.py` provides deterministic YAML parsing for control records.

## What Belongs Here

- Scripts that read or validate tracked research-control authority.
- Checkpoint and continuation tools used by bounded AgentJobs.

## What Does Not Belong Here

- Project-control classifiers.
- Generated task artifacts.
- Scientific source files.

## Common Commands

```zsh
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py --format markdown
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <job_id>
```

## Authority Boundary

These scripts enforce tracked state. They do not replace Director decisions,
AgentJob allowlists, role contracts, or human gates. If validation fails, treat
the failure as evidence to repair the transaction rather than bypass the gate.
