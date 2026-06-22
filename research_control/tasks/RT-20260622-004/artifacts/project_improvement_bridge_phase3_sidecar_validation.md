<!-- authority: control -->

# Research-Improvement Bridge Phase 3 Sidecar Validation

## Analysis

Phase 3 from `implementations_plans/research_improvement_bridge_plan.md`
adds deterministic sidecar schema and parity validation. The correct boundary
is prospective validation only. Historical signals remain valid without
backfilled sidecars, and the normal research handoff resolver remains
unchanged.

## Changes

Added:

- `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`
- `scripts/project_control/project_improvement_handoff_validation.py`

Updated:

- `.agents/schemas/README.md`
- `README.md`
- `scripts/project_control/README.md`
- `research_control/templates/COMPLETION_TEMPLATE.yaml`
- `research_control/templates/HANDOFF_TEMPLATE.yaml`
- `scripts/project_control/collect_project_improvement_signals.py`
- `scripts/research_control/validate_research_control.py`
- `tests/test_project_improvement_bridge.py`

The new validation checks:

- sidecar filename and `improvement_handoff_id` parity;
- allowed sidecar status and source kind;
- source completion and normal handoff paths;
- project-system-only boundary flags;
- signal-summary and issue signal parity;
- active signal type and concrete signal registry rows;
- sidecar signal provenance from the cited completion or regular handoff;
- solution-plan required fields and protected write-path hints;
- terminal sidecar evidence compatibility with signal terminal states;
- Markdown mirror presence and identity/signal/title parity;
- future source `project_improvement_bridge` references at or after
  `2026-06-22T04:00:00Z`.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar instance was
created in this transaction.

No resolver sidecar selection, checkpoint conditional allowlist, skill
contract edit, role contract edit, optional sidecar registry, canonical
science source, ontology source, benchmark source, Gate Chair authority, or
physics claim status changed.

## Verification Targets

The minimum targeted checks for this phase are:

- `.venv/bin/python -m unittest tests.test_project_improvement_bridge`
- `.venv/bin/python -m py_compile scripts/project_control/project_improvement_handoff_validation.py scripts/project_control/collect_project_improvement_signals.py scripts/research_control/validate_research_control.py`
- `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted --json`
- `.venv/bin/python -m unittest tests.test_research_control`
- `.venv/bin/python scripts/research_control/validate_research_control.py`
- documentation-impact validation;
- memory bootstrap and validate-only;
- research-control diff validation;
- `git diff --check`.

## Logical Next Step

Phase 4 should remain deferred unless the project explicitly wants
`resolve_project_improvement.py` to include selected sidecar context. That
later phase must preserve resolver advisory status and avoid turning sidecar
context into an unbounded checkpoint gate.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 2 generator* [Project-control artifact].
`research_control/tasks/RT-20260622-003/artifacts/project_improvement_bridge_phase2_generator.md`
