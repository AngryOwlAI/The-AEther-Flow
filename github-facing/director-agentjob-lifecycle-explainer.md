# Director Decisions And AgentJob Lifecycle

AEther-Flow records controlled work as a durable chain: task, Director
Decision Record, AgentJob, execution-role record, completion, handoff when
needed, and registry rows. That chain gives future maintainers a way to answer
four questions without guessing: what was authorized, what was allowed, what
was checked, and what remains blocked or next.

Each record narrows authority. The Director Decision Record explains the
route. The AgentJob turns that route into an executable contract. The
execution-role record binds role semantics to exactly one job. The completion
records outputs and command evidence for that transaction. Registry rows make
the record discoverable and checkable. If a record was wrong or later becomes
obsolete, the correction is a superseding packet, not silent mutation of the
old evidence.

## Lifecycle State Map

The reader learns which record narrows the next one and why corrections move
through supersession rather than historical mutation.

| State | Narrows into | Control rule |
| --- | --- | --- |
| Task | Director Decision Record | The task names objective, status, parent, and next route. |
| Director Decision Record | AgentJob | The Director selects one role path and records rejected alternatives. |
| AgentJob | Execution-role record and work surface | The job defines allowed paths, outputs, validators, and claim boundary. |
| Execution-role record | One job's role authority | The role template becomes task-local authority only through the record. |
| Work | Completion | Changes must remain inside the allowlist. |
| Completion | Handoff and registry rows | Evidence closes or hands off one bounded transaction. |

## Record Chain

| Record | Purpose | Primary source |
| --- | --- | --- |
| Task | Names objective, status, current decision, current job, parent task, closure, and next recommendation. | `research_control/tasks/<task_id>/00_TASK.yaml` |
| Director Decision Record | Explains role selection, rejected alternatives, claim boundary, and required checks. | `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` |
| AgentJob | Defines allowed reads, allowed writes, generated paths, forbidden paths, source classes, commands, outputs, and claim boundary. | `.agents/schemas/AGENT_JOB_SCHEMA.md` |
| Execution-role record | Binds selected role semantics to exactly one AgentJob. | `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |
| Completion | Records outputs, command results, verdict, uncertainty, and next recommendation. | Job-local completion YAML |
| Handoff | Names a future route when continuation is needed. | Tracked handoff record when in scope |
| Registry row | Makes the record discoverable and validator-checkable. | `registries/*.csv` |

The practical rule is that downstream records do not broaden the original
authority. They bind it to paths, roles, checks, outputs, and evidence.

## Immutable Evidence

`research_control/AGENTS.md` gives the editing rule: keep Director decisions,
AgentJobs, completions, approvals, and handoffs immutable after activation or
creation. Supersede rather than rewrite.

That rule preserves the factual trail. A failed or incomplete job can be
followed by a repair packet. A changed route can be recorded in a new Director
decision. A better explanation can point to the old record and explain why it
was superseded. The old record should not be edited into a cleaner story.

## Allowlists And Stop Conditions

An AgentJob is the executable boundary. Its allowlist says where the job may
write. Its forbidden paths and source classes say what remains outside scope.
Its expected outputs and validators define what completion must account for.

Common stop conditions include:

- required write path outside the allowlist;
- canonical ontology or science-source edits without the required gate;
- role, schema, validator, routing, permission, or checkpoint behavior changes
  without a matching project-system boundary;
- mutation of historical control records instead of supersession;
- protected authority such as Gate Chair verdict, benchmark promotion, or
  ontology adoption.

The safe response is to stop, create a new bounded packet, or route to the
appropriate human-gated decision.

## Transaction Evidence

A completion record is strong evidence for one bounded transaction. It can
state which files changed, which commands ran, which checks passed, which
outputs exist, and what next step was recommended.

It cannot by itself prove a broader theorem, promote a physics claim, adopt
ontology, register a permanent role, change a schema, or authorize generated
outputs as source authority. Those actions require their own authority paths.

## Operator Mistakes

| Mistake | Why it is unsafe | Correct action |
| --- | --- | --- |
| Editing an activated AgentJob to fit new work. | It rewrites the old authority boundary. | Supersede with a new decision and job. |
| Treating a role template as permission for the current task. | The task-local execution-role record controls actual authority. | Inspect the execution-role record and allowlist. |
| Adding generated HTML without a publication brief and source spec. | It creates an orphan public surface. | Route a Documentation Curator publication packet. |
| Using validator success as physics evidence. | Checks only enforce repository boundaries. | Inspect scientific sources and claim gates. |
| Folding multiple objectives into one transaction. | It breaks the one-job boundary. | Split into bounded packets. |

## Reader Scope

Reader scope: lifecycle orientation only. This explanation cannot edit
schemas, change task behavior, alter routing, expand role authority, mutate
historical records, or treat completion evidence as broad proof.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/director-agentjob-lifecycle-explainer.md`
- **Related HTML:** `html/director-agentjob-lifecycle-explainer.html`
- **Publication brief:** `markdown/publication-briefs/director-agentjob-lifecycle.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains the record
lifecycle, but it does not edit schemas, change task behavior, alter routing,
expand role authority, mutate historical records, or treat completion evidence
as broad proof.

## Source Materials

- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` [Director decision schema].
- AEther-Flow Project. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md` [AgentJob schema].
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` [Execution-role schema].
- AEther-Flow Project. (2026). `registries/DIRECTOR_DECISION_REGISTRY.csv` [Director decision registry].
- AEther-Flow Project. (2026). `registries/AGENT_JOB_REGISTRY.csv` [AgentJob registry].
- AEther-Flow Project. (2026). `registries/ROLE_EXECUTION_REGISTRY.csv` [Role execution registry].

## Safe Operating Summary

Safe summary: the Director/AgentJob lifecycle creates a narrow, inspectable
record chain for one bounded transaction and preserves corrections through
supersession.

Unsafe summary: historical control records can be edited for convenience,
completion evidence proves broader claims, allowlists are reusable general
permissions, or generated documentation changes authority.
