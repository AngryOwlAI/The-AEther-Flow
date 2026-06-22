<!-- authority: control -->

# Research-Improvement Bridge Phase 2 Generator

## Analysis

Phase 2 from `implementations_plans/research_improvement_bridge_plan.md`
introduces the deterministic generator for project-improvement handoff
sidecars. The correct boundary is generator plus focused tests. The bridge is
not yet a hard validator requirement and the project-improvement resolver does
not yet consume sidecar context.

## Changes

Added:

- `scripts/project_control/generate_project_improvement_handoff.py`

The generator:

- accepts `--completion` and/or `--source-handoff`;
- supports `--dry-run`, `--write`, and `--json`;
- extracts nonblank `project_improvement_signals`;
- treats blank placeholder signal entries as no-op state;
- requires existing concrete rows in
  `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`;
- validates active signal types against
  `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`;
- selects the highest-priority signal by severity, creation time, and signal
  ID;
- renders deterministic YAML and Markdown sidecar content from one data
  object;
- writes only under `research_control/project_improvement_handoffs/` when
  `--write` is supplied.

Extended `tests/test_project_improvement_bridge.py` with focused coverage for:

- dry-run reporting without writes;
- write-mode YAML and Markdown creation in a temporary repository;
- blank signal placeholder no-op behavior;
- missing signal-registry row rejection.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar instance was
created in this transaction.

No signal collector sidecar validation, research-control validator enforcement,
resolver sidecar selection, checkpoint conditional allowlist, skill contract,
role contract, schema contract, optional handoff registry, canonical science
source, ontology source, benchmark source, Gate Chair authority, or physics
claim status changed.

## Verification Targets

The minimum targeted checks for this phase are:

- `.venv/bin/python -m unittest tests.test_project_improvement_bridge`
- `.venv/bin/python scripts/project_control/generate_project_improvement_handoff.py --completion research_control/tasks/RT-20260622-002/jobs/completions/AJC-AJ-RT-20260622-002-001.yaml --dry-run --json`
- `.venv/bin/python -m py_compile scripts/project_control/generate_project_improvement_handoff.py`
- project-improvement signal validation;
- documentation-impact validation;
- research-control validation and diff validation;
- memory bootstrap and validate-only.

## Logical Next Step

Phase 3 should add sidecar schema and parity validation to signal collection
and research-control validators with an activation boundary, while preserving
normal latest-handoff behavior.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 1 templates and tests* [Project-control artifact].
`research_control/tasks/RT-20260622-002/artifacts/project_improvement_bridge_phase1_templates_tests.md`
