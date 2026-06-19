# Project-System Improvement Loop

AEther-Flow separates physics continuation from project-system improvement.
Physics continuation advances source-side research under claim gates.
Project-system improvement repairs or clarifies the machinery around the
research: documentation drift, control-contract drift, validator gaps, memory
retrieval issues, and routing ambiguity.

This page is a generated noncanonical reader surface. It explains the
project-system improvement loop, but it does not create signals, resolve
signals, change validators, change routing behavior, expand role authority,
change AgentJob allowlists, or authorize physics claim promotion.

## The Work Lane

Project-system improvement is the lane for work on the research system itself:
roles, schemas, validators, control-marked Markdown, memory tooling, trigger
logic, generated-document pipelines, and operational reliability. It is not the
lane for canonical ontology edits, science drafts, benchmark promotion, or Gate
Chair decisions.

One invocation may execute at most one bounded AgentJob. The job must name its
allowed reads, allowed writes, forbidden paths, source classes, expected
outputs, claim boundary, commands, and required checks. Generated outputs and
`.local` retrieval layers remain non-authority.

## Classify Before Routing

The first mechanical question is whether the current working tree already
contains a project-system or documentation-impact change.

`scripts/project_control/classify_project_changes.py` reads changed paths and
classifies them into reason codes. A plain documentation-surface change may
route to Documentation Curator. A role contract, schema, validator, control
registry, or control-marked mixed Markdown change routes to a more specific
project-system role unless the task overlay authorizes explanatory Markdown
work.

Classification is evidence for routing. It is not a claim that the change is
correct.

## Diff Or Signal

There are two normal sources of project-system work:

| Source | What it means | Routing consequence |
| --- | --- | --- |
| Current Git diff | The working tree has paths that affect documentation impact or project-system machinery. | Classifier output suggests the role and required receipt surfaces. |
| Registered open signal | A completion or handoff emitted a concrete project-improvement signal that is represented in `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`. | High or critical open signals take priority; lower severity signals remain backlog unless no current diff work is pending. |

The signal type registry and signal instance registry serve different roles.
`registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` defines allowed
signal types and default routing metadata. `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`
records concrete instances with severity, status, evidence, and resolution
fields.

## Resolver Is Advisory

`scripts/project_control/resolve_project_improvement.py` compares open signals
with current Git-change classification. It selects the next recommended
project-system boundary, but its output is advisory routing state.

Checkpoint blocking comes from validator failures and concrete
authority-boundary violations, not from the resolver merely seeing future
work. Ordinary documentation and validator jobs do not inherit resolver
snapshot requirements unless the AgentJob explicitly sets
`resolves_signal_routing: true`.

## Evidence To Close A Signal

A signal row that moves to `resolved`, `completed`, or `closed` needs:

| Field | Required content |
| --- | --- |
| `resolved_by_job_id` | The bounded AgentJob that resolved the signal. |
| `resolution_evidence_path` | A completion YAML with `validation_status: "PASS"` and a matching `job_id`. |
| `resolved_at` | The timestamp for the resolution record. |

For `rejected`, the evidence path may instead be a Director decision record
that names the signal and explains the rejection. A signal row should not
duplicate command strings; the completion record owns command evidence through
`command_results`.

## Documentation Impact Receipts

Every state-changing project-system AgentJob needs
`research_control/tasks/<task_id>/documentation_impact.yaml`. The receipt must
cover changed paths, reason codes, source surfaces inspected, source docs
updated or no-op rationale, registries, generated derivatives, and checks run.

A source documentation edit alone is sufficient only for plain documentation
edits outside a project-system AgentJob. Once the work is a project-system
AgentJob, the receipt is mandatory.

## Failure Modes

The common failures are concrete:

- closing a signal without PASS completion evidence or an explicit rejection
  decision;
- treating an unregistered free-text signal term as a routed signal;
- treating resolver output as a hard checkpoint gate by itself;
- omitting a documentation-impact receipt for a state-changing project-system
  AgentJob;
- treating generated HTML, wiki notes, Obsidian notes, semantic extracts, or
  `.local` caches as authority;
- using project-system improvement to alter physics claim status.

The safe pattern is state first, one bounded AgentJob, source-backed receipt,
then checks.

## Source Materials

- AEther-Flow Project. (2026). `AGENTS.md` [Root agent guidance].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system improvement skill].
- AEther-Flow Project. (2026). `scripts/project_control/classify_project_changes.py` [Project change classifier].
- AEther-Flow Project. (2026). `scripts/project_control/resolve_project_improvement.py` [Project-improvement resolver].
- AEther-Flow Project. (2026). `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` [Signal type registry].
- AEther-Flow Project. (2026). `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` [Signal instance registry].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/project-system-improvement-explainer.md`
- **Related HTML:** `html/project-system-improvement-explainer.html`
- **Publication brief:** `markdown/publication-briefs/project-system-improvement.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: project-system improvement classifies current diffs, inspects
registered signals, routes one bounded AgentJob, records documentation impact,
and closes signals only with explicit evidence.

Unsafe summary: project-system improvement is physics continuation, resolver
output alone blocks checkpointing, or a signal can be closed without a PASS
completion or rejection decision.
