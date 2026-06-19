# Parent-Child Parallel Synthesis

Parent-child parallel synthesis is an internal perspective structure for
future physics AgentJobs. It lets the project compare two child perspectives
under a parent review without breaking the external control invariant: one
Director decision, one outer AgentJob, one execution-role record, one
completion record, and one final fused output.

This page is a generated noncanonical reader surface. It explains the mode,
but it does not change the one-job rule, AgentJob schema, execution-role
schema, validators, routing behavior, role authority, write permissions, or
physics claim status.

## The Invariant

The mode is named `parent_child_parallel_synthesis`. Its purpose is analytical
coverage, not extra authority.

| External record | What remains singular | Why it matters |
| --- | --- | --- |
| Director decision | One routing decision selects the job. | The Director still authorizes one bounded action. |
| Outer AgentJob | One executable contract owns reads, writes, validators, and expected outputs. | Child units cannot add write paths or source classes. |
| Execution-role record | One task-local role contract constrains the job. | Child perspectives do not become separate role records. |
| Completion record | One validation and verdict receipt closes the transaction. | A child note cannot independently certify PASS. |
| Fused output | One final artifact is used for downstream handoff and registry references. | Supporting drafts do not replace the final source artifact. |

For physics jobs created after the activation point recorded in
`research_control/README.md` and `.agents/schemas/AGENT_JOB_SCHEMA.md`, the
decomposition is mandatory. That requirement is scoped to future physics
research AgentJobs. It is not a claim that all project-system or documentation
work must use this mode.

## Internal Units

The parent unit enforces the shared claim boundary, reviews child outputs for
conflicts, requests bounded conflict resolution when needed, and fuses the
final output.

The child units are analytical perspectives. The schema names common
perspectives such as a physicist-mathematician child and a
physicist-philosopher child. Those labels describe what each child should
notice. They do not create new permissions, roles, claim boundaries, or
validators.

Child output paths, conflict-review paths, fusion notes, and the fused output
must all sit inside the outer AgentJob write allowlist. The fused output is the
old-style final artifact for completion, handoff, and registry use. Child
outputs are supporting draft/control artifacts.

## Inherited Authority

Everything important is inherited from the outer job:

- the execution-role record;
- the claim boundary;
- allowed read and write paths;
- forbidden paths;
- source restrictions;
- validators;
- human-gate status;
- stop conditions.

If a task needs actual authority expansion, parent-child synthesis is the
wrong mechanism. The project must route through the ordinary execution-role
paths first: `registered_role`, `task_overlay`, or
`one_job_provisional_role`, with any protected expansion human-gated.

## Conflict Handling

Parallel perspectives are useful only if disagreement is preserved long enough
to be inspected.

The AgentJob schema requires a conflict policy. A declared blocking conflict
must be reviewed, resolved within the stated resolution limit, or leave the job
blocked. A PASS completion is not valid while a blocking parent-child conflict
remains unresolved.

This makes the mode stricter than a normal single-voice draft. It does not let
a parent select the convenient child and ignore the other. It requires the
fused output to preserve shared consensus, unique contributions, and unresolved
limitations.

## What The Mode Is Not

Parent-child synthesis is not:

- multiple AgentJobs inside one invocation;
- a way to add child write paths;
- a way to create child execution-role records;
- a way to bypass a Smuggling Auditor, Refuter, or Gate Chair boundary;
- a source of benchmark promotion, ontology adoption, or completed-derivation
  language;
- a rule for all non-physics project-system work.

The mode improves review geometry. It does not change authority.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door].
- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md` [AgentJob schema].
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` [Execution-role schema].
- AEther-Flow Project. (2026). `registries/AGENT_JOB_REGISTRY.csv` [AgentJob registry].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/parent-child-synthesis-explainer.md`
- **Related HTML:** `html/parent-child-synthesis-explainer.html`
- **Publication brief:** `markdown/publication-briefs/parent-child-synthesis.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: parent-child synthesis is an internal perspective structure
inside one physics AgentJob; child outputs support parent review, and only the
fused output enters completion and downstream references.

Unsafe summary: parent-child synthesis creates extra jobs, extra role records,
extra write authority, independent child verdicts, or a path around conflict
review.
