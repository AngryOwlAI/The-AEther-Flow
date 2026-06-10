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

Every state-changing project-system AgentJob must include
`research_control/tasks/<task_id>/documentation_impact.yaml`. A source
documentation update by itself is sufficient only for plain documentation edits
outside a project-system AgentJob. Documentation-impact records are
mechanically checked against the live transaction: source changes, generated
derivatives, classifier reason codes, and required validators must be covered.

Completions and handoffs may emit `project_improvement_signals`. Signal types
are defined in `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`;
concrete signal instances are recorded in
`registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` and are processed by
`.codex/skills/improve-project-system/SKILL.md`, one bounded AgentJob at a
time. The type registry owns allowed signal kinds and default routing metadata;
severity remains on the concrete signal instance because the same signal type
can carry different urgency in different transactions. Registered high/critical
signals are routed before current Git-change work. Registered low/medium
signals remain backlog unless no current project-system action is pending.
Signal rows that leave the open backlog by moving to `resolved`, `completed`,
`closed`, or `rejected` must include `resolved_by_job_id`,
`resolution_evidence_path`, and `resolved_at` so resolution is tied to a
bounded AgentJob receipt. For `resolved`, `completed`, and `closed`, the
evidence path must be a completion YAML with `validation_status: "PASS"` and a
matching `job_id`. For `rejected`, the evidence path may instead be a Director
decision record that names the signal and explains the rejection. Signal rows
do not duplicate validator command strings; the referenced completion record
owns command evidence through `command_results`.
One bounded AgentJob may close multiple project-improvement signals only when
its `objective` names every closed signal ID and its completion record lists
the same IDs in `resolved_project_improvement_signals` with a nonblank
`coherent_resolution_summary`. For shared closures, every signal row must use
the resolving job's canonical `completion_path` from
`registries/AGENT_JOB_REGISTRY.csv` as `resolution_evidence_path`.

`scripts/project_control/resolve_project_improvement.py` is advisory routing
state. Checkpoint blocking is defined by validator failures and concrete
authority-boundary violations, not by the resolver seeing future work.
Completion records do not need a fresh resolver snapshot merely because high
or critical signals remain open; resolver snapshots are optional handoff
context unless the AgentJob sets `resolves_signal_routing: true`.
Routing-resolution completions must preserve repo-relative
`resolver_snapshots.before` and `resolver_snapshots.after` paths to JSON output
from `resolve_project_improvement.py --json` and include nonblank
`routing_delta_summary`. The validator checks only summary presence and
minimal resolver-shape fields: the advisory flags, checkpoint gate source,
selected signal, open signals, and change classification. Ordinary validator
and documentation jobs do not inherit that burden.

Use the signal validator to ensure emitted signals are not stranded outside the
canonical registry:

```zsh
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
```

Signal detection is structural. Completion and handoff YAML files are parsed
for nonblank `project_improvement_signals` entries; free-text mentions of
signal terms do not create project-improvement routing state. Classifier,
resolver, and signal validation behavior read the allowed signal-type
vocabulary from the canonical type registry.
