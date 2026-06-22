<!-- authority: control -->

# Research-Improvement Bridge Phase 6 Checkpoint Allowlist Governance

## Analysis

Phase 6 implements the deferred checkpoint governance for project-improvement
sidecar paths. The required rule is not a broad directory exception. The rule
is conditional: a generated sidecar YAML/Markdown pair can pass checkpoint and
diff validation only when a changed source YAML already allowed by the active
AgentJob points to that exact sidecar through `project_improvement_bridge`.

## Changes

Updated:

- `scripts/project_control/project_improvement_handoff_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/project_control/README.md`
- `scripts/research_control/README.md`
- `tests/test_project_improvement_bridge.py`
- `tests/test_research_control.py`

The shared helper `conditional_checkpoint_sidecar_paths` now derives eligible
sidecar paths from a changed, AgentJob-allowed source YAML. It requires:

- a completion or regular handoff YAML source path;
- a nonblank `project_improvement_signals` source signal;
- `project_improvement_bridge.required: true`;
- `project_improvement_bridge.bridge_status: "generated"`;
- an exact sidecar YAML path under
  `research_control/project_improvement_handoffs/`;
- a sidecar that points back to the source and carries the emitted signal IDs;
- project-system-only boundary flags.

The checkpoint script calls the helper before preflight allowlist rejection and
again before final post-sync allowlist rejection. The research-control
`--check-diff` validator calls the same helper before checking changed paths.

## Negative Controls

The focused tests confirm that:

- a valid bridge-referenced sidecar YAML/Markdown pair is accepted;
- an unreferenced sidecar pair is not accepted;
- checkpoint allowlist extension does not admit unrelated sidecar paths;
- `validate_research_control.py --check-diff` accepts the same valid pair
  through the shared rule.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar instance was
created in this transaction.

No normal research handoff resolver behavior, sidecar registry, skill
contract, role contract, canonical science source, ontology source, benchmark
source, Gate Chair authority, or physics claim status changed.

The change is intentionally a checkpoint and validator behavior change, and it
is limited to the conditional sidecar-path rule described above.

## Verification Targets

The minimum targeted checks for this phase are:

- `.venv/bin/python -m unittest tests.test_project_improvement_bridge`
- `.venv/bin/python -m unittest tests.test_research_control`
- `.venv/bin/python -m py_compile scripts/project_control/project_improvement_handoff_validation.py scripts/research_control/checkpoint_research_transaction.py scripts/research_control/validate_research_control.py tests/test_project_improvement_bridge.py tests/test_research_control.py`
- project-improvement signal validation;
- latest handoff resolution;
- documentation-impact validation;
- memory bootstrap and validate-only;
- research-control validation and diff validation;
- `git diff --check`.

## Logical Next Step

Use the bridge in a future qualifying research completion. Any optional
sidecar registry, broader policy expansion, or resolver hard-gate behavior
remains a separate explicit approval boundary.

## References

The AEther-Flow Research Project. (2026, June 22). *Project improvement
handoff schema* [Project-control schema].
`.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 5 contract integration* [Project-control artifact].
`research_control/tasks/RT-20260622-006/artifacts/project_improvement_bridge_phase5_contract_integration.md`
