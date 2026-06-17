# Role Routing

> Non-authoritative teaching explainer.
> Derived from `markdown/html-explainer-specs/role-routing-explainer.md`.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/role-routing-explainer.md`
- **Teaching packet:** `markdown/teaching-packets/role-routing.teaching-qa.md`
- **Related HTML:** `html/role-routing-explainer.html`
- **Authority status:** `generated_noncanonical`

## Start here in 90 seconds

Role routing is the project’s way of deciding which kind of agent may do one
bounded task. It happens before implementation. The routing decision connects a
request to an authority class, a selected role, a task-local execution-role
record, an AgentJob allowlist, required validators, and stop conditions.

The key idea is simple: a role is not a universal permission slip. A
Documentation Curator, Validator Engineer, Project-Control Maintainer, Refuter,
and Gate Chair exist for different authority problems. The execution-role
record says exactly how the selected role is being used for one job.

## The problem this feature solves

Without role routing, one helper could drift across boundaries: a documentation
task might become a validator change, a generated page might be treated as
authority, or a provisional role might become policy by repetition. Role
routing keeps work auditable by making the role choice itself inspectable.

## Plain-language model

Think of role routing as a dispatch desk with a logbook:

- The request arrives.
- The project classifies the kind of authority involved.
- The Director selects a role for one bounded job.
- The execution-role record records the exact one-job permissions and limits.
- The AgentJob carries the read paths, write paths, outputs, validators, and
  claim boundary.
- Completion records what happened and whether validation passed.

## Key terms

| Term | Plain meaning | Project meaning | Source paths |
|---|---|---|---|
| Role | A reusable job description. | A versioned contract registered in `AGENT_ROLE_REGISTRY.csv`. | `registries/AGENT_ROLE_REGISTRY.csv` |
| Role version | A stable edition of a role. | Historical versions remain registered while one active version is the default template. | `.agents/schemas/ROLE_SCHEMA.md` |
| Execution-role record | The one-job use of a role. | A task-local record binding exact role semantics to one AgentJob. | `registries/ROLE_EXECUTION_REGISTRY.csv`, `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |
| Task overlay | A narrow one-job adjustment. | A registered role with task-specific constraints, removed permissions, or bounded non-promotional expansion. | `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |
| One-job provisional role | A temporary role identity. | A non-reusable role that expires after the owning AgentJob unless later registered through human-authorized project-system work. | `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |
| Parent-child synthesis | Internal perspectives inside one job. | A decomposition mode that inherits the existing execution-role record and does not create extra authority. | `.agents/schemas/AGENT_JOB_SCHEMA.md` |
| Human gate | A protected approval boundary. | Required for protected authority expansion such as claim promotion, canonical ontology authority, benchmark authority, Gate Chair authority, or permanent role registration. | `.agents/schemas/ROLE_SCHEMA.md`, `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` |

## Walkthrough: from task request to selected role

1. A task request or handoff identifies work to be done.
2. The project classifies the work as science-bearing, project-control,
   documentation, validation, memory, or process repair.
3. The Director evaluates role-fit candidates.
4. The Director decision records the selected role, role version, AgentJob, and
   claim boundary.
5. The AgentJob lists allowed reads, allowed writes, generated paths, forbidden
   paths, required validators, expected outputs, and stop conditions.
6. The task-local execution-role record says whether the role is used directly,
   with a task overlay, or as a one-job provisional role.
7. If parent-child synthesis is present, it happens inside that same AgentJob
   and inherits the same boundaries.
8. The completion record reports outputs and validator results.

## Common questions

### Why can’t one general helper do every task?

Because the project separates different kinds of authority. Physics drafting,
refutation, documentation, validation, memory maintenance, and project-control
repair can have different write paths, validators, gates, and claim risks.
Collapsing them into one helper would make it easier to promote claims, edit
generated derivatives as if they were source, or change control behavior
without the right contract.

### What is an execution-role record?

It is the exact task-local role contract for one AgentJob. A registered role is
the reusable template; the execution-role record says how that template is
being used now, including allowed writes, removed permissions, expanded
permissions, expiry, and validation status.

### What is the difference between a task overlay and a provisional role?

A task overlay keeps the registered role identity but adds a bounded one-job
delta. A one-job provisional role creates a temporary one-job identity and must
not become reusable until registered. Repeated provisional-role patterns should
route to project-system review rather than silently becoming policy.

### Does parent-child synthesis create new authority?

No. Parent-child synthesis creates internal analytical perspectives inside one
selected AgentJob. Parent and child units inherit the same execution-role
record, write-path allowlist, claim boundary, validators, and stop conditions.

### Who decides which role is selected?

The Director decision selects the role for the bounded job. The decision row,
AgentJob YAML, and execution-role record are the inspection path for that
choice.

### What should I inspect before trusting a routing explanation?

Read the role registry, Director decision row, execution-role registry row,
task-local role YAML, AgentJob YAML, and completion record. Generated HTML,
GitHub-facing Markdown, wiki notes, PDFs, and `.local/` caches can orient you,
but they are not authority.

## Examples and non-examples

| Case | Classification | Why |
|---|---|---|
| A Documentation Curator updates a source spec, regenerates tracked HTML, and writes documentation-impact evidence. | Example | The work stays in explanatory documentation and source-backed derivative generation. |
| Project-Control Maintainer receives a one-job overlay to update a validator and matching README guidance. | Example | The overlay is explicit, bounded, and validator-backed. |
| A generated HTML page says a role can write a new registry path. | Non-example | Generated HTML explains; it does not authorize. |
| A one-job provisional role is reused repeatedly without registration. | Non-example | Repetition should trigger project-system review, not silent policy. |
| A child perspective writes outside the parent AgentJob allowlist. | Non-example | Decomposition inherits the existing execution-role boundary. |

## Common misunderstandings

### “Generated docs are enough to authorize work.”

Generated docs are orientation surfaces. Authority remains with source files,
registries, role contracts, schemas, AgentJobs, and validators.

### “A provisional role becomes real if it works.”

A provisional role expires after its job. Permanent registration requires the
registered role contract and registry update path.

### “A task overlay is a role rewrite.”

A task overlay is task-local. It can add bounded constraints or permissions for
one job, but it does not permanently change the base role.

### “Parent-child synthesis means multiple AgentJobs.”

It does not. Parent and child execution units are internal perspectives inside
one outer AgentJob.

## What this page does not claim

- It does not change role authority.
- It does not change routing behavior.
- It does not change schemas or validators.
- It does not authorize protected authority expansion.
- It does not promote physics claims.
- It does not make generated HTML, GitHub-facing Markdown, wiki notes, PDFs, or
  `.local/` caches authoritative.

## Check your understanding

1. Which file tells you the reusable active role versions?
2. Which task-local record tells you whether a role was used directly, as an
   overlay, or as a provisional role?
3. Why does parent-child synthesis not create extra authority?
4. What would you inspect before saying a role was allowed to write a path?
5. What kind of change requires a human gate?

## Source authority

The role registry, execution-role registry, Director decision registry,
research-control guidance, AgentJob schema, execution-role schema, and role
schema define the authority evidence. This page teaches those surfaces; it
does not amend them.

## Where to go next

- Read `AGENTS.md` for the authority hierarchy.
- Read `research_control/README.md` for project-system improvement and
  documentation-impact rules.
- Read `registries/AGENT_ROLE_REGISTRY.csv` for active role status.
- Read `registries/ROLE_EXECUTION_REGISTRY.csv` for task-local role semantics.
- Read `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` for overlays and provisional
  roles.
- Read `.agents/schemas/AGENT_JOB_SCHEMA.md` for AgentJob and decomposition
  constraints.

## All source materials

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/schemas/ROLE_SCHEMA.md`
