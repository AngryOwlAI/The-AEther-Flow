# Role Routing And Execution Contracts

AEther-Flow separates role identity from current job authority. A registered
role tells the Director what kind of work a role can normally perform. The
execution-role record and AgentJob allowlist decide what one job may actually
do.

This page is a generated noncanonical reader surface. It explains role
routing and execution contracts, but it does not register roles, expand role
authority, change schemas, change routing behavior, change AgentJob allowlists,
or authorize claim promotion.

## Template Versus Job Contract

The control spine uses three layers:

| Layer | Function | Boundary |
| --- | --- | --- |
| Registered role contract | Stable versioned template in `.agents/roles/` and `registries/AGENT_ROLE_REGISTRY.csv`. | Does not by itself grant current write permission. |
| Execution-role record | Task-local contract in `registries/ROLE_EXECUTION_REGISTRY.csv` and the task `roles/` file. | Binds one AgentJob to exact role semantics. |
| AgentJob allowlist | Executable read/write, output, validator, source-class, and claim-boundary contract. | Controls actual file access for that transaction. |

A role name is therefore not enough. To understand a job, inspect the
execution-role record and the AgentJob, not only the base role.

## Execution-Role Choices

| Kind | Use when | What it must not do |
| --- | --- | --- |
| `registered_role` | The registered role fits directly and no authority delta is needed. | Silently add permissions. |
| `task_overlay` | The base role remains correct but needs task-specific constraints or a bounded non-promotional adjustment. | Expand protected authority without a gate. |
| `one_job_provisional_role` | No registered role fits, or a template-derived one-job identity is needed. | Become reusable by convention. |

Recurring provisional-role patterns are not promoted informally. If the same
pattern recurs, the project-system improvement loop may route a review for
possible human-authorized registration. Until that happens, the provisional
role expires after its AgentJob.

## Active Role Families

| Family | Active examples | Authority level | Output form | Gate status |
| --- | --- | --- | --- | --- |
| Research routing | Director of Research, Project-System Director | routing or project control | Markdown | Not claim-promoting. |
| Physics drafts | Ontology Formalizer, Candidate Constructor, Refuter, Smuggling Auditor, Theoretical Continuation Selector | science draft | TeX or YAML | Autonomous within draft/control limits. |
| Scientific gate | Gate Chair | human gated | TeX | Defined but paused; execution and promotion need explicit tracked approval. |
| Project system | Project-Control Maintainer, Validator Engineer, Memory-System Maintainer | project control | Markdown or Python | Cannot promote physics claims. |
| Public documentation | Documentation Curator | project control | Markdown plus generated HTML | Cannot change source authority or role authority. |

The role registry records status, validators, output format, may/may-not
fields, and human-gate status. Historical superseded roles remain present so
old execution records stay interpretable.

## Authority Fields To Inspect

When reviewing a role route, check:

- `authority_level`;
- `may_execute_autonomously`;
- `may_create_outputs`;
- `may_modify_sources`;
- `may_promote_claims`;
- `requires_human_gate`;
- `allowed_source_classes`;
- `forbidden_source_classes`;
- default validators;
- the current AgentJob write allowlist.

The Gate Chair is the clearest example. Its role contract may promote claims,
but it is human-gated and paused. A normal Director route cannot execute it or
promote a claim without explicit tracked approval.

## Routing Mistakes

Common mistakes are avoidable:

- using a registered role as if it were a current write allowlist;
- treating a task overlay as a reusable role version;
- reusing a provisional role after its AgentJob expires;
- assuming parent-child synthesis creates child execution-role records;
- treating Documentation Curator output as source authority;
- treating validator PASS as physics proof or claim promotion.

The logical inspection order is role registry, role contract, execution-role
record, AgentJob, claim boundary, and completion evidence.

## Source Materials

- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv` [Agent role registry].
- AEther-Flow Project. (2026). `registries/ROLE_EXECUTION_REGISTRY.csv` [Execution-role registry].
- AEther-Flow Project. (2026). `.agents/schemas/ROLE_SCHEMA.md` [Role schema].
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` [Execution-role schema].
- AEther-Flow Project. (2026). `.agents/roles/` [Role contracts directory].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/role-routing-explainer.md`
- **Related HTML:** `html/role-routing-explainer.html`
- **Publication brief:** `markdown/publication-briefs/role-routing.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: registered roles are templates; execution-role records and
AgentJob allowlists define one-job authority; protected promotion remains
human-gated.

Unsafe summary: a role name alone grants permission, a provisional role becomes
reusable by habit, or a documentation page can register roles or promote
claims.
