<!-- authority: control -->

# Research-Improvement Bridge Phase 1 Templates And Tests

## Analysis

Phase 1 from `implementations_plans/research_improvement_bridge_plan.md`
introduces the bridge shape without activating the bridge. The correct
boundary is templates and focused tests only. The normal research handoff
resolver remains the controlling mechanism for `/continue-research`.

## Changes

Added the inert machine-readable sidecar template:

- `research_control/templates/IMPROVE_PROJECT_HANDOFF_TEMPLATE.yaml`

Added the operator-facing Markdown mirror template:

- `research_control/templates/IMPROVE_PROJECT_HANDOFF_TEMPLATE.md`

Added resolved historical sidecar fixtures under tests only:

- `tests/fixtures/project_improvement_bridge/improve-project-handoff_20260622_001.yaml`
- `tests/fixtures/project_improvement_bridge/improve-project-handoff_20260622_001.md`

Added focused tests:

- template YAML parses under the strict YAML parser;
- resolved fixture YAML preserves project-system and non-physics boundaries;
- `resolve_latest_handoff.py` ignores `improve-project-handoff_*` files and
  malformed `handoff-*` sidecar-like names while selecting only normal
  `handoff-####.yaml` records.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar queue was
created. No generator, signal collector, resolver output, checkpoint
governance, skill contract, role contract, schema contract, or validator
enforcement was changed.

No canonical science source, ontology source, benchmark source, Gate Chair
authority, or physics claim status changed.

## Verification Targets

The minimum targeted checks for this phase are:

- `.venv/bin/python -m unittest tests.test_project_improvement_bridge`
- `.venv/bin/python -m unittest tests.test_research_control`
- `.venv/bin/python scripts/research_control/resolve_latest_handoff.py --json`
- project-improvement signal validation;
- documentation-impact validation;
- research-control validation and diff validation;
- memory bootstrap and validate-only.

## Logical Next Step

Phase 2 should implement the deterministic project-improvement handoff
generator with `--dry-run`, `--write`, and `--json` modes. It should still
avoid validator hard enforcement and resolver integration unless that phase is
explicitly expanded.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 0 audit* [Project-control artifact].
`research_control/tasks/RT-20260622-001/artifacts/project_improvement_bridge_audit.md`
