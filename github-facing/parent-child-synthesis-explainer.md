# Parent-Child Parallel Synthesis

Parent-child parallel synthesis is an internal perspective structure inside
one future physics AgentJob. It does not create extra jobs. It does not create
child execution-role records. It keeps the external control invariant fixed:
one Director decision, one outer AgentJob, one execution-role record, one
completion record, and one fused output.

The mode exists because some physics packets need more than one analytical
view before a final artifact is honest. Child outputs can surface different
mathematical, physical, or philosophical pressures, but they inherit the same
claim boundary, source restrictions, write allowlist, validators, and stop
conditions as the outer job. Child outputs are supporting `draft/control`
artifacts. A declared blocking conflict must be reviewed and resolved, or the
job cannot receive PASS completion. This mode is scoped to future physics
research AgentJobs; it is not a rule that all project-system or documentation
tasks use parent-child decomposition.

## Single Outer Frame

The reader learns how internal perspective decomposition improves review
coverage without adding AgentJobs, write authority, role records, or claim
authority.

| Inside the one outer AgentJob | Function | Authority result |
| --- | --- | --- |
| Parent review and fusion | Enforces the shared claim boundary, reviews child outputs, and fuses the final artifact. | No extra role record. |
| Child draft/control outputs | Surface analytical perspectives under the same source restrictions and validators. | No independent authority. |
| Conflict review | Preserves disagreement long enough to inspect it. | Unresolved declared blocking conflict prevents PASS completion. |
| Fused output | Carries the final old-style output for completion and handoff. | One completion record and one downstream reference path. |

## External Invariant

| External record | What remains singular | Why it matters |
| --- | --- | --- |
| Director decision | One routing decision selects the job. | The Director still authorizes one bounded action. |
| Outer AgentJob | One executable contract owns reads, writes, validators, and expected outputs. | Child units cannot add write paths or source classes. |
| Execution-role record | One task-local role contract constrains the job. | Child perspectives do not become separate role records. |
| Completion record | One validation and verdict receipt closes the transaction. | A child note cannot independently certify PASS. |
| Fused output | One final artifact is used for downstream handoff and registry references. | Supporting drafts do not replace the final source artifact. |

## Internal Units

The parent unit enforces the shared claim boundary, reviews child outputs for
conflicts, requests bounded conflict resolution when needed, and fuses the
final output. The child units are analytical perspectives. Their labels
describe what each perspective should notice; they do not create permissions,
roles, claim boundaries, or validators.

Child output paths, conflict-review paths, fusion notes, and the fused output
must all sit inside the outer AgentJob write allowlist. The fused output is
the old-style final artifact for completion, handoff, and registry use.

## Inherited Authority

Everything important is inherited from the outer job:

- the execution-role record;
- the claim boundary;
- allowed read and write paths;
- forbidden paths;
- source restrictions;
- validators;
- human-gate status; and
- stop conditions.

If a task needs actual authority expansion, parent-child synthesis is the
wrong mechanism. The project must route through the ordinary execution-role
paths first: `registered_role`, `task_overlay`, or
`one_job_provisional_role`, with any protected expansion human-gated.

## Conflict Handling

Parallel perspectives are useful only if disagreement is preserved long enough
to be inspected. The AgentJob schema requires a conflict policy. A declared
blocking conflict must be reviewed, resolved within the stated resolution
limit, or leave the job blocked. A PASS completion is not valid while a
blocking parent-child conflict remains unresolved.

This makes the mode stricter than a normal single-voice draft. It does not let
a parent select the convenient child and ignore the other. It requires the
fused output to preserve shared consensus, unique contributions, and
unresolved limitations.

## Reader Scope

Reader scope: concept orientation only. This explanation cannot change the
one-job rule, AgentJob schema, execution-role schema, validators, routing
behavior, role authority, write permissions, or physics claim status.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/parent-child-synthesis-explainer.md`
- **Related HTML:** `html/parent-child-synthesis-explainer.html`
- **Publication brief:** `markdown/publication-briefs/parent-child-synthesis.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains the mode,
but it does not change the one-job rule, AgentJob schema, execution-role
schema, validators, routing behavior, role authority, write permissions, or
physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door].
- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md` [AgentJob schema].
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` [Execution-role schema].
- AEther-Flow Project. (2026). `registries/AGENT_JOB_REGISTRY.csv` [AgentJob registry].

## Safe Summary

Safe summary: parent-child synthesis is an internal perspective structure
inside one physics AgentJob; child outputs support parent review, and only the
fused output enters completion and downstream references.

Unsafe summary: parent-child synthesis creates extra jobs, extra role records,
extra write authority, independent child verdicts, a path around conflict
review, or a mandatory mode for all non-physics work.
