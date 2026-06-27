<!-- authority: control -->

# Research Control

This directory contains the tracked control spine for Director-led research
continuation.

## Authority Model

The Director writes a Director Decision Record. A role contract constrains the
selected execution context. An AgentJob defines allowed reads, writes, outputs,
validators, and claim boundaries. Validators enforce the boundaries. Human-gated
roles control promotion or closure.

Registered roles are stable templates for Director reasoning, not a rigid menu.
The execution-role record is the one-job authority contract. Use direct
`registered_role` only when the template fits without change; use
`task_overlay` when a registered role remains the correct identity but needs a
bounded task-specific delta; use `one_job_provisional_role` when the Director
needs a brand-new temporary role or a template-derived role with a distinct
one-job identity. Recurring provisional-role patterns are routed through
project-system improvement for possible human-authorized registration.

## One-Job Rule

`/continue-research` may set up or execute at most one bounded AgentJob per
invocation. Normal flow writes a completion record and handoff after execution.

Every new physics research AgentJob created after `2026-06-17T04:08:16Z` must
declare `role_decomposition.mode: "parent_child_parallel_synthesis"` before it
is executed. This does not relax the one-job rule. The parent and child
execution units inherit the same execution-role record, claim boundary, write
allowlist, source restrictions, validators, and stop conditions as the outer
AgentJob. Child outputs are supporting draft/control artifacts; the fused
output remains the old-style final artifact for downstream completion,
handoff, and registry references. A PASS completion is blocked when a declared
blocking parent-child conflict remains unresolved.

## Theoretical Continuation Gate

Future physics routing after `2026-06-17T04:29:31Z` must not use generic
controlled pause merely because a datum, experiment, witness, or theoretical
primitive is missing. This is a theoretical physics project; when the next step
is a choice among source-side selector primitives, source-side irrelevance
theorems, concrete `Resp_lc` witnesses, scoped no-go questions, or bounded
theoretical calculations, the Director routes one bounded
`theoretical-continuation-selector@0.1.0` AgentJob.

Pause-like routing is reserved for protected human-gated authority, especially
canonical ontology edit or ontology adoption. Future completions and handoffs
must record that route as `human_gated_ontology_change_required` or another
specific human-gated route, not as generic `controlled_pause`.

## Ontology-Law Research Packet Route

The named route `ontology-law-research-packet` is available only for
derivation-critical ontology underdetermination. Its trigger classification is
`derivation_critical_missing_source_law`: the current ontology does not derive
a required source-side law, selector, discriminator, transition rule,
robustness rule, or equivalent primitive needed by the active milestone.

This route is not for `ordinary_gap` or `workflow_inconvenience`. Ordinary gaps
include missing documentation, missing registry rows, generated derivative
drift, missing citations, missing computations available under existing
ontology, and proof-detail work under existing ontology. Workflow
inconvenience includes tedious casework, slow literature review, awkward
templates, and strict validation friction.

The route preserves same-milestone continuity. The AgentJob must name the
active `target_derivation_milestone` and `milestone_burden`; it must not open
an unrelated path merely because adoption is blocked. Use the status pair
`blocked_adoption_open_continuation` when current adoption is rejected but a
conservative source-side extension remains possible.

Allowed underdetermination language is "current ontology does not derive X."
Without a separate no-go theorem or scoped obstruction, do not write
"therefore X is impossible." Candidate outputs must use the controlled status
vocabulary `draft/control`, `proposal-only`, `source-extension data`,
`canonical-ontology candidate`, `adopted`, `rejected`, and `human-gated`.
Human-gated ontology adoption, exact requested ontology edits, benchmark
promotion, `M_src` adoption, downstream metric or coupling claims, and Gate
Chair verdicts remain blocked unless separately authorized.

Validator and fixture evidence for this route is operational receipt evidence
only. A PASS result can show that a completion preserved the route label,
trigger classification, blocked-adoption/open-continuation pair, exact-GR
recovery obligations, no-target-import audit scope, and human-gate boundary.
It does not prove that a candidate source-side law is mathematically correct,
source-complete, sufficient for exact-GR recovery, or adopted. Use task-local
Phase 4 and Phase 5 artifacts for validator and fixture audit evidence; use
registered physics sources plus explicit human-gated authority for scientific
promotion.

## GR Derivation Burden Map

Future physics AgentJobs after `2026-06-17T15:46:25Z` must name a
`target_derivation_milestone` and `milestone_burden` from
`research_control/design/gr_derivation_burden_map.md`. This separates
derivation planning from agent-routing planning: the role and validators say
who acts next, while the milestone says which physics object must exist next
for ordinary GR or the conservative exact-GR benchmark to become derivable.

`registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent Distance-to-GR ledger.
Future physics completions must include the expanded burden matrix and a
`new_mathematical_payload` item. Repeated-burden or scoped-obstruction
completions must evaluate `freeze_criteria_status`; `NDCL-RESP-LC-SELECTOR-UNDERDETERMINATION`
is the candidate freeze label for the current `Resp_lc` selector route.

Source extension is a controlled workflow category. It must distinguish a
derivation from current ontology, a conservative definitional extension, a new
ontology primitive, and a forbidden target-GR import. A finite toy
metric-response target is an allowed constructive packet before attempting a
full `M_src` or `g_eff` construction.

## Mathematical Decisiveness Contract

`research_control/design/mathematical_decisiveness_completion_contract.md`
defines the prospective contract for physics AgentJobs that opt into
mathematical-decisiveness enforcement. A `validation_status: "PASS"` completion
is operational receipt evidence only; it does not prove a theorem, adopt a
source-side law, construct `M_src`, define `g_eff`, derive coupling or Einstein
equations, promote the benchmark, or close a Gate Chair decision.

Opted-in physics completions must state the actual burden effect through
`physics_progress_status`, `distance_to_gr_delta`,
`mathematical_payload_manifest`, and `forbidden_conclusion_summary`.
Obstruction and repeated-burden completions add `obstruction_record`,
`freeze_criteria_status`, and `route_cycle_control` where applicable. Candidate
Constructor completions governed by
`.agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md` must end with one
decisive `candidate_constructor_result` rather than vague continuation
language.

The completion template in `research_control/templates/COMPLETION_TEMPLATE.yaml`
contains the active field shape. `scripts/research_control/report_physics_progress_metrics.py`
reports descriptive AI-system metrics from tracked completions and registries.
Those metrics are useful for research-system health, but they remain
non-promotional operational diagnostics.

## Local Cache Boundary

Tracked files under `research_control/` are authority. `.local/` prompts,
logs, previews, and run caches are optional convenience artifacts only.

## Memory Preflight

Future continuation and project-system decisions must use the memory system as
a disciplined navigation instrument before routing or AgentJob creation. For
`/continue-research`, the required first step is:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
```

That command runs the memory status check, refreshes the local Obsidian vault
notes, raw mirrors, semantic extracts, and SQLite retrieval index when
`local_retrieval_status` reports local-cache drift, then reports the final
status summary. The receipt-facing status command remains:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
```

followed by at least one targeted `lookup` or `search` query. Any memory hit
that influences routing, claim language, source selection, or project-control
changes must be verified by inspecting the named registered source file or CSV
registry row. AgentJobs and completions created after
`2026-06-18T15:33:00Z` must record the `memory_preflight` receipt: status
summary, query commands, returned object IDs, canonical source inspections,
source registries, canonical paths, and source hashes. If the local retrieval
refresh ran, the AgentJob or completion evidence should also record the refresh
command and before or after local-retrieval status.

Obsidian notes, wiki notes, content-semantic extracts, the SQLite memory index,
and `.local/` files remain retrieval layers only. Stale local retrieval state
is repaired before continuation routing when possible, but it remains a local
retrieval condition, not authority and not a physics or project-control claim.

## Novel Datum Acquisition

Many blockers in this project are expected to involve data, metrics, witness
families, calculations, or theoretical objects that are not already present in
the repository and are not supplied by the user. Local absence is therefore not
automatically final. If tracked state or explicit user instruction authorizes
research or construction, the Director may route one bounded AgentJob to:

- search external primary literature or official technical sources;
- design a source-acquisition packet or experiment;
- perform a bounded theoretical calculation or mathematical construction; or
- produce a draft/control datum from explicitly stated source-side assumptions.

The output remains noncanonical until it passes the relevant audit, refutation,
and human-gated claim-promotion sequence. Any external source must be cited,
and any new project construction must be labeled as new draft/control work.

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

Documentation impact is a receipt requirement and does not by itself select the
Documentation Curator. Explanatory documentation edits, Markdown explainer
specs, and spec-backed human-only HTML explainer regeneration belong to
Documentation Curator; skill contracts, role contracts, schema contracts,
control registries, and control-marked mixed Markdown belong to
Project-Control Maintainer unless a more specific validator or memory role owns
the change. When documentation impact is required, the transaction must include
either a source documentation update or a valid
`research_control/tasks/<task_id>/documentation_impact.yaml` no-op rationale:

improve-project-system is best understood as a project-system reliability and
governance perspective. It is closest to system engineer plus software
engineer plus process auditor. Documentation Curator is best understood as a
source-backed publication and technical-documentation perspective. It is
closest to technical editor, science communicator, information architect, and
provenance auditor. These descriptions orient maintainers and future agents;
they do not create new role semantics, role authority, routing behavior,
validator behavior, write permissions, checkpoint gates, or physics claim
authority.

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
