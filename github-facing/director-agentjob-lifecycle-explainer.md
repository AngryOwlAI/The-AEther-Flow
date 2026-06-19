# Director Decisions And AgentJob Lifecycle

AEther-Flow records research-control work as a durable chain: task, Director
Decision Record, AgentJob, execution-role record, completion, handoff, and
registry rows. The chain lets future maintainers inspect what was authorized,
what was done, what was checked, and what remains blocked or next.

This page is a generated noncanonical reader surface. It explains the record
lifecycle, but it does not edit schemas, change task behavior, alter routing,
expand role authority, mutate historical records, or treat completion evidence
as broad proof.

## Record Chain

| Record | Purpose | Primary source |
| --- | --- | --- |
| Task | Names the objective, status, current decision, current job, parent task, closure, and next recommendation. | `research_control/tasks/<task_id>/00_TASK.yaml` |
| Director Decision Record | Explains role selection, rejected alternatives, claim boundary, and required checks. | `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` |
| AgentJob | Defines allowed reads, allowed writes, generated paths, forbidden paths, source classes, commands, outputs, and claim boundary. | `.agents/schemas/AGENT_JOB_SCHEMA.md` |
| Execution-role record | Binds the selected role semantics to exactly one AgentJob. | `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |
| Completion | Records outputs, command results, verdict, remaining uncertainty, and next recommendation. | Job-local completion YAML |
| Handoff | Names the next route when future continuation is needed. | Tracked handoff record when in scope |
| Registry row | Makes the record discoverable and checkable by validators and future agents. | `registries/*.csv` |

The practical rule is that every downstream record narrows the allowed work.
It does not broaden the original authority.

## Lifecycle States

A healthy transaction moves through a small state model:

1. Task exists or is created from explicit authorization.
2. Director chooses a role and writes a decision.
3. AgentJob defines the bounded executable contract.
4. Execution-role record binds role semantics for that job.
5. Work happens inside the allowlist.
6. Completion records outputs and command evidence.
7. Registries, generated derivatives, and required receipts are refreshed.
8. The task closes or hands off a precise next route.

For physics jobs, additional fields may be required, such as derivation
milestone, milestone burden, or parent-child synthesis. For documentation
jobs, the relevant boundary is usually publication brief, source spec,
generated noncanonical surfaces, review evidence, and documentation-impact
receipt.

## Mutable Versus Immutable

`research_control/AGENTS.md` gives the editing rule: keep Director decisions,
AgentJobs, completions, approvals, and handoffs immutable after activation or
creation. Supersede rather than rewrite.

That rule protects evidence. If a job was wrong, incomplete, or superseded,
the correction should create a new bounded record or a new repair packet. It
should not silently mutate the old record into a cleaner story.

Registries may be updated as part of a valid transaction because they are the
tracking layer. Historical task artifacts still need to preserve what was
actually decided and executed.

## Allowlists And Stop Conditions

An AgentJob is not a suggestion. Its write allowlist decides where the job may
change files. Its forbidden paths and source classes say what must remain out
of scope.

Common stop conditions include:

- required write path is outside the allowlist;
- requested work would edit canonical ontology or science sources without the
  required gate;
- requested work would change role, schema, validator, routing, permission, or
  checkpoint behavior without a matching project-system boundary;
- a historical control record would need mutation instead of supersession;
- protected authority such as Gate Chair verdict, benchmark promotion, or
  ontology adoption is required.

The safe response is to stop, create a new bounded packet, or route to the
appropriate human-gated decision. It is not to widen the current job by
convention.

## Transaction Evidence

A completion record is strong evidence for one bounded transaction. It can say
which files changed, which commands ran, which checks passed, which outputs
exist, and what next step was recommended.

It cannot, by itself, prove a broader theorem, promote a physics claim, adopt
ontology, register a permanent role, change a schema, or authorize generated
outputs as source authority. Those actions require their own authority paths.

The registries make the evidence inspectable:

- `registries/DIRECTOR_DECISION_REGISTRY.csv` records decision provenance.
- `registries/AGENT_JOB_REGISTRY.csv` records job provenance, completion path,
  allowed writes, outputs, status, and check status.
- `registries/ROLE_EXECUTION_REGISTRY.csv` records the execution-role contract
  actually used for the job.

## Operator Mistakes

| Mistake | Why it is unsafe | Correct action |
| --- | --- | --- |
| Editing an activated AgentJob to fit new work. | It rewrites the old authority boundary. | Supersede with a new decision and job. |
| Treating a role template as permission for the current task. | The task-local execution-role record controls actual authority. | Inspect the execution-role record and allowlist. |
| Adding generated HTML without a publication brief and source spec. | It creates an orphan public surface. | Route a Documentation Curator publication packet. |
| Using validator success as physics evidence. | Checks only enforce repository boundaries. | Inspect scientific sources and claim gates. |
| Folding multiple objectives into one transaction. | It breaks the one-job boundary. | Split into bounded packets. |

## Source Materials

- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` [Director decision schema].
- AEther-Flow Project. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md` [AgentJob schema].
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` [Execution role schema].
- AEther-Flow Project. (2026). `registries/DIRECTOR_DECISION_REGISTRY.csv` [Director decision registry].
- AEther-Flow Project. (2026). `registries/AGENT_JOB_REGISTRY.csv` [AgentJob registry].
- AEther-Flow Project. (2026). `registries/ROLE_EXECUTION_REGISTRY.csv` [Role execution registry].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/director-agentjob-lifecycle-explainer.md`
- **Related HTML:** `html/director-agentjob-lifecycle-explainer.html`
- **Publication brief:** `markdown/publication-briefs/director-agentjob-lifecycle.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Operating Summary

Safe summary: the Director/AgentJob lifecycle creates a narrow, inspectable
record chain for one bounded transaction and preserves corrections through
supersession.

Unsafe summary: historical control records can be edited for convenience,
completion evidence proves broader claims, allowlists are reusable general
permissions, or generated documentation changes authority.
