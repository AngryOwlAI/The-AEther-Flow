<!-- authority: control -->

# Research-Improvement Bridge Phase 0 Audit

## Analysis

Phase 0 from
`implementations_plans/research_improvement_bridge_plan.md` is read-only. It
requires inspection of the current improvement-signal machinery before any
project-improvement sidecar, template, generator, validator, resolver, skill,
role, or checkpoint implementation is introduced.

The current bridge is partial but coherent: research completions and normal
handoffs can emit `project_improvement_signals`; concrete signal rows are held
in `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`; and
`resolve_project_improvement.py` selects open registered signals before normal
project-system change routing when priority requires it. The missing structure
is the proposed durable sidecar queue. That is not implemented in Phase 0.

## Phase 0 Acceptance

| Requirement | Phase 0 status | Evidence |
| --- | --- | --- |
| Inspect current signal registries | Satisfied | `PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` and `PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` were inspected. The live collector reports 6 signals and 0 open signals. |
| Inspect latest normal handoff resolver | Satisfied | `resolve_latest_handoff.py` scans only `research_control/handoffs/handoff-*.yaml` and applies `HANDOFF_RE = handoff-(\\d{4})\\.yaml$`. |
| Inspect signal collection and resolver scripts | Satisfied | `collect_project_improvement_signals.py` scans completion YAML and normal `handoff-*.yaml` only. `resolve_project_improvement.py` selects high or critical open signals before normal project-system Git-change routing. |
| Identify templates that mention project-improvement signals | Satisfied | `research_control/templates/COMPLETION_TEMPLATE.yaml` and `research_control/templates/HANDOFF_TEMPLATE.yaml` contain `project_improvement_signals`; the completion template also contains `resolved_project_improvement_signals`. |
| Confirm registration model for handoffs and completions | Satisfied | Bootstrap source registries cover Markdown, TeX, PDF derivatives, and HTML explainers. Individual YAML handoffs and completions are treated as control transaction artifacts, not first-class source-registry objects. |

## Current Signal Registry Finding

The current signal type registry is sufficient for the bridge plan's sample
issue classes. No new signal type is required for Phase 1.

The concrete signal registry currently has no open signals. The most relevant
resolved rows are the four `RT-20260621-010` project-system signals:

| Signal | Type | Severity | Status |
| --- | --- | --- | --- |
| `PIS-RT-20260621-010-001` | `memory_retrieval_failure` | high | resolved |
| `PIS-RT-20260621-010-002` | `generated_artifact_drift` | medium | resolved |
| `PIS-RT-20260621-010-003` | `validator_gap` | medium | resolved |
| `PIS-RT-20260621-010-004` | `workflow_friction` | medium | resolved |

Conclusion: Phase 1 should use these rows as historical fixture guidance only.
It should not reopen them and should not infer that a bridge sidecar already
exists.

## Handoff Resolver Baseline

The latest-handoff resolver is correctly narrow. It searches
`research_control/handoffs/`, matches only filenames of the form
`handoff-####.yaml`, requires a Markdown mirror, and returns the latest normal
research handoff.

The live resolver returns `handoff-0128`, task `RT-20260614-086`, job
`AJ-RT-20260614-086-001`. Its next action is human-gated source-extension or
ontology adoption authority before treating stressed `GSC_src` as adopted
source law or making any downstream GR claim.

Conclusion: Phase 1 tests should pin this baseline. A future sidecar named
`improve-project-handoff_YYYYMMDD_NNN.yaml` must not live in
`research_control/handoffs/` and must not match `HANDOFF_RE`.

## Collection And Resolver Baseline

`collect_project_improvement_signals.py` currently reads:

- `research_control/tasks/*/jobs/completions/*.yaml`;
- `research_control/handoffs/handoff-*.yaml`;
- registered signal and signal-type registries;
- role execution rows for provisional-role recurrence detection.

It validates emitted nonblank signals against the concrete signal registry and
requires terminal signal evidence for resolved, completed, closed, or rejected
states.

`resolve_project_improvement.py` currently:

- classifies current Git paths;
- reads open registered signals;
- selects high or critical open signals first;
- then falls through to documentation or project-system Git-change routing;
- then selects backlog signals if no higher-priority boundary exists;
- remains advisory rather than a hard checkpoint gate.

Conclusion: Phase 2 and Phase 3 should extend this baseline rather than replace
it. The first extension point is sidecar discovery and parity validation, not a
second resolver.

## Template Baseline

The current template state is:

- `HANDOFF_TEMPLATE.yaml` contains `project_improvement_signals`.
- `COMPLETION_TEMPLATE.yaml` contains `resolved_project_improvement_signals`,
  `coherent_resolution_summary`, `resolver_snapshots`,
  `routing_delta_summary`, and `project_improvement_signals`.
- Neither template has a `project_improvement_bridge` block yet.
- No `IMPROVE_PROJECT_HANDOFF_TEMPLATE.yaml` or
  `IMPROVE_PROJECT_HANDOFF_TEMPLATE.md` exists.

Conclusion: Phase 1 should add only the sidecar templates and focused tests.
Adding `project_improvement_bridge` to completion and handoff templates should
remain a separate phase unless the tests require an explicit fixture shape.

## Memory Registration Finding

`bootstrap_memory_system.py` defines source registry names for:

- `MARKDOWN_SOURCE_REGISTRY.csv`;
- `TEX_SOURCE_REGISTRY.csv`;
- `PDF_DERIVATIVE_REGISTRY.csv`;
- `HTML_EXPLAINER_REGISTRY.csv`.

Its Markdown discovery includes root guidance, selected project Markdown files,
folder READMEs, role contracts, schema contracts, Codex skill contracts,
GitHub-facing Markdown, `research_control/design/*.md`, `ontology/*.md`,
`legacy_ontology/**/*.md`, and `markdown/**/*.md`.

Individual YAML task, job, completion, and handoff files are tracked control
transaction records. They are not registered as first-class source objects in
the memory source registries. Individual task-local Markdown artifacts are also
not automatically registered by current Markdown discovery.

Conclusion: the proposed sidecar YAML instances should be treated as tracked
control transaction artifacts unless a later phase explicitly changes bootstrap
registration. If the sidecar Markdown template is added under
`research_control/templates/`, it will not automatically enter the Markdown
source registry unless template discovery or explicit registration changes.

## Phase 1 Recommendation

The logical next phase is Phase 1 from the implementation plan:

1. Add `research_control/templates/IMPROVE_PROJECT_HANDOFF_TEMPLATE.yaml`.
2. Add `research_control/templates/IMPROVE_PROJECT_HANDOFF_TEMPLATE.md`.
3. Add focused test fixtures proving that normal latest-handoff resolution
   ignores sidecar-like names.
4. Add failing tests for missing sidecar after activation, but keep validator
   enforcement deferred until the implementation phase that owns it.

The safer split is to avoid updating checkpoint governance, resolver output,
skill contracts, or role contracts in Phase 1. Those surfaces have separate
phase labels in the plan and should remain separate bounded packets.

## Boundary Findings

1. No project-improvement sidecar directory exists yet.
2. No `PROJECT_IMPROVEMENT_HANDOFF_REGISTRY.csv` exists yet.
3. Phase 0 did not create either artifact.
4. No canonical science source, benchmark source, ontology source, handoff,
   program state, validator, resolver, skill contract, or role contract was
   modified.
5. The plan remains a local planning reference rather than an independent
   authority source.

## Memory Preflight Receipt

The memory status command returned `freshness_status: PASS` with 314 source
objects, an existing SQLite memory index, and an existing local Obsidian vault.
These retrieval layers were used only for navigation.

The targeted search
`.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "research improvement bridge" --limit 10 --json`
returned `MD-SKILL-CONTINUE-RESEARCH` among the registered control sources.
The targeted lookup for `MD-SKILL-CONTINUE-RESEARCH` confirmed
`.codex/skills/continue-research/SKILL.md` as the canonical source with source
hash `ff63af2258cf7a39ea54f374352c0c6e05da6b45f48dfc94d31e844a7a7bf350`.

The lookup for
`implementations_plans/research_improvement_bridge_plan.md` returned no
registered memory object. The file was inspected directly as a local planning
reference, with current source hash
`6f0e37c1d681b12f284818f6c923763bf2efd3c9a5ded1cb3b4d835663bb7d91`.

## Recommendation

Proceed to Phase 1 only after this Phase 0 packet validates. The Phase 1 packet
should be owned by Project-Control Maintainer with Validator Engineer review
scope, because it introduces templates and tests but should still avoid live
resolver, checkpoint, and skill-contract behavior changes.

## Can It Be Improved?

An improvement will be to make the future sidecar schema explicitly declare
whether the Markdown mirror is a tracked control transaction artifact or a
registered Markdown source. That decision should be made when Phase 1 adds the
templates and test fixtures, not retroactively in this audit.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026). *Continue Research skill contract*
[Repository control contract]. `.codex/skills/continue-research/SKILL.md`

The AEther-Flow Research Project. (2026). *Improve Project System skill
contract* [Repository control contract].
`.codex/skills/improve-project-system/SKILL.md`

The AEther-Flow Research Project. (2026). *Project-improvement signal
registry* [Control registry].
`registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`

The AEther-Flow Research Project. (2026). *Resolve latest research-control
handoff script* [Repository tool].
`scripts/research_control/resolve_latest_handoff.py`
