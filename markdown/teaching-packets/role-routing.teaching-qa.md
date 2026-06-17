---
packet_id: "role-routing.teaching-qa.v0.1"
topic_slug: "role-routing"
source_spec: "markdown/html-explainer-specs/role-routing-explainer.md"
derived_outputs:
  - "html/role-routing-explainer.html"
  - "github-facing/role-routing-explainer.md"
audience_model: "layperson"
student_role: "documentation-student@0.1.0"
teacher_role: "documentation-teacher@0.1.0"
rounds: 2
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - ".agents/schemas/ROLE_SCHEMA.md"
claim_boundary: "Explanatory Q&A only. Does not change role authority, routing behavior, schemas, validators, or scientific claim status."
authority_status: "curated_explanatory_support"
---

# Teaching Q&A Packet: Role Routing

## Curator Feature Selection

Plain-language topic:
Role routing is how the project decides which kind of agent may do one bounded
task.

Why this feature needs teaching:
Readers can confuse a reusable role, a task-local execution-role record, a
task overlay, a one-job provisional role, and internal parent-child synthesis.
The explainer must repair that confusion without turning the teaching packet
into project authority.

## Round 1 Student Questions

### Q1
What is role routing in normal language?

### Q2
Why cannot the project use one smart helper for every task?

### Q3
What is the difference between a role and an execution-role record?

### Q4
What does a task overlay change?

### Q5
What is a one-job provisional role?

### Q6
Does parent-child synthesis create two jobs or extra authority?

### Q7
Who decides which role is selected?

### Q8
What should a reader inspect to verify a routing decision?

## Round 1 Teacher Answers

### A1
Plain answer:
Role routing is the project's way of choosing the right kind of helper for one
bounded job before any files are changed.

Technical anchor:
The routing path connects the request, Director decision, selected role,
execution-role record, AgentJob allowlists, validators, and stop conditions.

Source paths:
- README.md
- research_control/README.md
- registries/DIRECTOR_DECISION_REGISTRY.csv
- registries/ROLE_EXECUTION_REGISTRY.csv

Boundary note:
This answer does not change routing behavior or authorize any role to write
outside its AgentJob boundary.

Curator note:
The final docs should open with a plain-language model before naming the
registries.

### A2
Plain answer:
One generic helper would blur lanes that the project needs to keep separate:
physics drafting, refutation, documentation, validation, memory maintenance,
and project-control repair have different risks.

Technical anchor:
The root guidance separates physics claims, AI-methodology claims, tooling
claims, and human-facing explanations. Role rows and execution-role rows
preserve those distinctions for actual work.

Source paths:
- README.md
- AGENTS.md
- registries/AGENT_ROLE_REGISTRY.csv

Boundary note:
This answer does not create a new role or make existing roles interchangeable.

Curator note:
Use examples and non-examples to show why a Documentation Curator should not
silently become a Validator Engineer or Gate Chair.

### A3
Plain answer:
A role is a reusable job description. An execution-role record is the exact
one-job version of that description for a particular task.

Technical anchor:
`AGENT_ROLE_REGISTRY.csv` registers stable role versions. The execution-role
schema says the task-local record binds an AgentJob to the exact role semantics
used for that job, including allowed writes, deltas, and expiry.

Source paths:
- registries/AGENT_ROLE_REGISTRY.csv
- registries/ROLE_EXECUTION_REGISTRY.csv
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md

Boundary note:
This answer does not make a task-local execution-role record reusable policy.

Curator note:
The final explainer should include a glossary row for role, role version,
execution-role record, and AgentJob.

### A4
Plain answer:
A task overlay lets a registered role do a narrow task-specific variation while
preserving the base role identity.

Technical anchor:
The execution-role schema says a `task_overlay` is appropriate when the
selected role remains registered but needs task-specific constraints, removed
permissions, or a bounded non-promotional authority adjustment.

Source paths:
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md
- registries/ROLE_EXECUTION_REGISTRY.csv
- research_control/README.md

Boundary note:
This answer does not authorize protected authority expansion without a human
gate or outside the one-job allowlist.

Curator note:
Show a small overlay example and a non-example that would require a different
role or human gate.

### A5
Plain answer:
A one-job provisional role is a temporary role identity for a specific job. It
expires after that job and cannot become policy by habit.

Technical anchor:
The execution-role schema requires provisional roles to name a justification,
set `non_reusable_until_registered: true`, and expire after the owning
AgentJob. Repeated provisional patterns route to project-system review.

Source paths:
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md
- research_control/README.md
- registries/ROLE_EXECUTION_REGISTRY.csv

Boundary note:
This answer does not register a permanent role or bypass the role registry.

Curator note:
The final docs should make repeated provisional-role use a common
misunderstanding, not an obscure footnote.

### A6
Plain answer:
No. Parent-child synthesis creates internal perspectives inside one selected
AgentJob. It does not create two jobs, two roles, or a new permission lane.

Technical anchor:
The AgentJob schema states that parent and child execution units inherit the
outer execution-role authority, claim boundary, source restrictions, forbidden
paths, validators, and write-path allowlist.

Source paths:
- .agents/schemas/AGENT_JOB_SCHEMA.md
- README.md
- research_control/README.md

Boundary note:
This answer does not authorize role decomposition to add write paths, role IDs,
claim boundaries, or human-gate exemptions.

Curator note:
Use a diagram callout that places decomposition after the execution-role record,
not before it.

### A7
Plain answer:
The Director decision selects the role for the bounded job.

Technical anchor:
The Director decision registry records decision IDs, selected role IDs, role
versions, AgentJob IDs, status, and validation state. The AgentJob then carries
the executable contract.

Source paths:
- registries/DIRECTOR_DECISION_REGISTRY.csv
- .agents/schemas/AGENT_JOB_SCHEMA.md
- research_control/README.md

Boundary note:
This answer does not let the selected role exceed the AgentJob's allowed paths,
validators, or claim boundary.

Curator note:
The final docs should show the chain from request to Director decision to
AgentJob to completion.

### A8
Plain answer:
Read the role registry, Director decision row, execution-role row, AgentJob
YAML, and task-local role record.

Technical anchor:
Those surfaces show the reusable role, selected one-job semantics, write
allowlist, required validators, expected outputs, and expiry.

Source paths:
- registries/AGENT_ROLE_REGISTRY.csv
- registries/DIRECTOR_DECISION_REGISTRY.csv
- registries/ROLE_EXECUTION_REGISTRY.csv
- .agents/schemas/AGENT_JOB_SCHEMA.md
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md

Boundary note:
This answer does not make generated HTML, wiki notes, PDFs, or `.local/` caches
verification authority.

Curator note:
End the final explainer with a source-backed reading path.

## Round 2 Student Follow-up Questions

### Q1
Why is documentation work still project-control sensitive?

### Q2
How do generated HTML and GitHub-facing Markdown stay non-authoritative?

### Q3
What would count as authority drift in role routing?

### Q4
What does the human gate protect?

### Q5
What is the smallest safe example of a task overlay?

## Round 2 Teacher Answers

### A1
Plain answer:
Documentation can change how readers and agents understand the project, so it
must stay tied to source specs, registries, validators, and documentation-impact
receipts.

Technical anchor:
Root guidance says Documentation Curator may improve explanatory Markdown and
source-backed visual explainers, but it must not change control contracts,
validators, role authority, or scientific claim status.

Source paths:
- README.md
- AGENTS.md
- research_control/README.md

Boundary note:
This answer does not make explanatory documentation a control-contract editor.

Curator note:
The final docs should include a short explanation of why "just docs" can still
need project-system routing.

### A2
Plain answer:
They stay non-authoritative because the source spec and registries define their
source basis, and generated outputs are treated as derivatives for humans.

Technical anchor:
The root guidance says generated artifacts may be read by humans and agents but
are not independent authority. The README applies that rule to tracked HTML and
GitHub-facing explainers.

Source paths:
- AGENTS.md
- README.md
- research_control/README.md

Boundary note:
This answer does not let generated HTML or GitHub-facing Markdown override
source specs, registries, or role contracts.

Curator note:
Add an explicit "what this page does not claim" section near the reader-facing
Q&A.

### A3
Plain answer:
Authority drift happens when an explanation starts acting like permission: for
example, treating a provisional role as permanent or using decomposition as a
second AgentJob.

Technical anchor:
The execution-role schema requires provisional roles to expire, and the
AgentJob schema says internal decomposition cannot add role IDs, allowlists,
claim boundaries, or protected permissions.

Source paths:
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md
- .agents/schemas/AGENT_JOB_SCHEMA.md
- research_control/README.md

Boundary note:
This answer does not create a new validator rule beyond the registered schemas;
it explains the existing boundary.

Curator note:
Use misconception cards for "provisional means permanent" and "child means
separate job."

### A4
Plain answer:
The human gate protects decisions that would expand protected authority, such
as claim promotion, canonical ontology authority, benchmark status authority,
Gate Chair authority, or permanent role registration.

Technical anchor:
The execution-role schema identifies protected expansions and says they require
a human gate. The role schema also states protected authority expansion needs
human approval.

Source paths:
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md
- .agents/schemas/ROLE_SCHEMA.md
- research_control/README.md

Boundary note:
This answer does not grant human-gated authority; it identifies when the system
must stop for that authority.

Curator note:
Keep this as an authority note, not a legalistic warning after every paragraph.

### A5
Plain answer:
A safe overlay might let Project-Control Maintainer update a narrow validator
and matching documentation in one bounded task, while listing exact write paths
and validators.

Technical anchor:
Task overlays can add constraints or bounded non-promotional permissions for
one AgentJob. The AgentJob and execution-role record must carry the allowlist,
expanded permissions, required validators, expiry, and claim boundary.

Source paths:
- .agents/schemas/EXECUTION_ROLE_SCHEMA.md
- .agents/schemas/AGENT_JOB_SCHEMA.md
- registries/ROLE_EXECUTION_REGISTRY.csv

Boundary note:
This answer does not authorize editing canonical science sources, promoting
claims, or reusing the overlay after the job expires.

Curator note:
Use this as the walkthrough scenario in both HTML and GitHub-facing Markdown.

## Curator Synthesis Notes

### Concepts that must appear in the HTML explainer

- Role routing is authority selection before implementation.
- A reusable role and a task-local execution-role record are different.
- Registered roles, task overlays, one-job provisional roles, and
  parent-child decomposition are separate concepts.
- Generated docs explain; they do not authorize.
- The human gate protects protected authority expansion.

### Concepts that must appear in GitHub-facing Markdown

- Start-here summary in plain language.
- Key terms table.
- Walkthrough from request to role selection.
- Common questions from both rounds.
- Examples and non-examples.
- Common misunderstandings.
- What the page does not claim.
- Source-backed next reading path.

### Glossary candidates

- Role: a reusable versioned job contract.
- Execution-role record: the exact task-local role semantics for one AgentJob.
- Task overlay: a bounded one-job delta on a registered role.
- One-job provisional role: a temporary non-reusable role identity.
- Parent-child synthesis: internal perspectives inside one AgentJob.
- Human gate: required approval for protected authority expansion.

### Common confusions to repair

- A generated explainer is not authority.
- A provisional role is not a permanent role.
- A task overlay is not a reusable policy change.
- Parent-child synthesis does not create child AgentJobs.
- Documentation work can still require project-system routing.

### Examples and non-examples

- Example: a Director selects Documentation Curator for an explainer update
  with exact source specs and validators.
- Example: a task overlay grants Project-Control Maintainer a one-job validator
  plus documentation synchronization boundary.
- Non-example: a generated HTML page silently expands role authority.
- Non-example: a repeated provisional role becomes policy without registration.
- Non-example: a child perspective writes outside the parent AgentJob allowlist.

### Next reading notes

- Read `AGENTS.md` for the authority hierarchy.
- Read `research_control/README.md` for project-system improvement and
  documentation-impact rules.
- Read `registries/AGENT_ROLE_REGISTRY.csv` for active role versions.
- Read `registries/ROLE_EXECUTION_REGISTRY.csv` for task-local role semantics.
- Read `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` for overlays and provisional
  roles.
- Read `.agents/schemas/AGENT_JOB_SCHEMA.md` for AgentJob and decomposition
  constraints.

### Source gaps

- No source gap for the selected role-routing teaching scope.

### Claims intentionally not made

- No physics claim is changed.
- No role authority is expanded.
- No routing behavior is changed.
- No validator behavior is changed.
- No schema requirement is changed.
- No generated output becomes authoritative.
