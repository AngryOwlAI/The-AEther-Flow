<!-- authority: control -->

# Research-Improvement Bridge Phase 4 Activation

## Analysis

Phase 4 activates the project-improvement handoff bridge in two controlled
ways. First, the sidecar generator can now update emitting source YAML records
with a generated `project_improvement_bridge` block when explicitly invoked
with `--update-source-bridge`. Second, the project-improvement resolver now
reports selected sidecar context and solution-plan status when an open signal
has a corresponding open sidecar.

## Changes

Updated:

- `scripts/project_control/generate_project_improvement_handoff.py`
- `scripts/project_control/resolve_project_improvement.py`
- `scripts/project_control/README.md`
- `tests/test_project_improvement_bridge.py`
- `tests/test_project_change_classifier.py`

The generator now:

- keeps dry-run and write behavior deterministic;
- adds `--update-source-bridge` as an explicit opt-in;
- writes source bridge references only for source YAML files that emitted
  nonblank project-improvement signal IDs;
- leaves blank placeholder handoff signal blocks untouched;
- reports source bridge updates in JSON and human output.

The resolver now:

- preserves existing high/critical open-signal priority;
- preserves current Git-change priority over low/medium backlog signals;
- emits `selected_signal_source`;
- emits `selected_improvement_handoff`;
- emits `open_improvement_handoffs`;
- emits normalized `solution_plan` context;
- routes sidecars with no executable plan to `project-system-director`;
- routes sidecars with a ready safe active-role plan to the named
  implementation role.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar instance was
created in this transaction.

No normal research handoff resolver behavior, checkpoint behavior, skill
contract, role contract, optional sidecar registry, canonical science source,
ontology source, benchmark source, Gate Chair authority, or physics claim
status changed.

## Verification Targets

The minimum targeted checks for this phase are:

- `.venv/bin/python -m unittest tests.test_project_improvement_bridge`
- `.venv/bin/python -m unittest tests.test_project_change_classifier`
- `.venv/bin/python -m py_compile scripts/project_control/generate_project_improvement_handoff.py scripts/project_control/resolve_project_improvement.py tests/test_project_improvement_bridge.py tests/test_project_change_classifier.py`
- `.venv/bin/python scripts/project_control/resolve_project_improvement.py --json`
- `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted --json`
- `.venv/bin/python scripts/project_control/generate_project_improvement_handoff.py --completion research_control/tasks/RT-20260622-004/jobs/completions/AJC-AJ-RT-20260622-004-001.yaml --dry-run --json`
- documentation-impact validation;
- memory bootstrap and validate-only;
- research-control validation and diff validation;
- `git diff --check`.

## Logical Next Step

Phase 5 should remain deferred unless the project explicitly authorizes skill
or role contract updates for automatic bridge generation in the normal
workflow. The present packet only provides controlled generator activation and
advisory resolver context.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 3 sidecar validation* [Project-control artifact].
`research_control/tasks/RT-20260622-004/artifacts/project_improvement_bridge_phase3_sidecar_validation.md`
