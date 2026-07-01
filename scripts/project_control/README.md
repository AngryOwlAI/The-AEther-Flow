<!-- authority: explanatory -->

# Project-Control Scripts

This folder contains scripts for classifying, routing, auditing, and validating
project-system changes.

## Main Tools

- `classify_project_changes.py` classifies current or staged Git changes for
  documentation impact and project-system improvement routing.
- `resolve_project_improvement.py` reports advisory project-improvement
  routing state, including selected sidecar context when an open signal has a
  project-improvement handoff.
- `collect_project_improvement_signals.py` validates emitted project-
  improvement signals against the signal registries.
- `generate_project_improvement_handoff.py` creates deterministic project-
  improvement sidecar YAML/Markdown pairs and, when explicitly requested,
  updates emitting source YAML with the generated bridge reference.
- `validate_documentation_impact.py` checks documentation-impact receipts.
- `validate_claim_language.py` checks claim-language gate surfaces against the
  P3 taxonomy. The default scan is a full diagnostic; `--changed` and
  `--staged` are checkpoint gates for changed public/current surfaces.
- `audit_documentation_surfaces.py` checks source-backed documentation
  surfaces.
- `project_improvement_handoff_validation.py` supplies sidecar schema and
  parity checks used by project-improvement signal validation, the global
  research-control validator, and checkpoint conditional sidecar allowlists.
- `project_signal_types.py` reads the registered signal-type vocabulary.

## What Belongs Here

- Project-control tooling that reasons about documentation impact, signals,
  registered surfaces, and project-system routing.
- Tests for these scripts belong under `tests/`.

## What Does Not Belong Here

- Research continuation logic.
- Generated reports.
- Task-local receipts.

## Common Commands

```zsh
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/resolve_project_improvement.py --json
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
.venv/bin/python scripts/project_control/generate_project_improvement_handoff.py --completion <completion.yaml> --source-handoff <handoff.yaml> --write --update-source-bridge --json
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/project_control/validate_claim_language.py --json --changed
```

## Authority Boundary

Classifier and resolver output is routing evidence, not final authority.
Checkpoint validity is decided by validators, task receipts, allowlists, and
the checkpoint gate. Project-improvement sidecar files are not globally
allowlisted; checkpoint and diff validation allow only the exact sidecar
YAML/Markdown pair referenced by a changed, AgentJob-allowed source YAML
through a generated `project_improvement_bridge` block.
