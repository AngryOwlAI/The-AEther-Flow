<!-- authority: control -->

# CI Validation Shard Policy v1

## Purpose and authority

This policy defines the `P11-T01` target topology for manifest-driven CI. It
assigns every live validation gate to one primary responsibility shard and
specifies how a plan-producing job feeds future shard execution.

The active migration epoch is `shadow_planner`. The two existing workflow jobs,
`validate_project_control` and `validate_memory_read_only`, remain the only
authoritative CI acceptance jobs. The new `validation_plan_shadow` job is
fail-open, uploads operational planning evidence, and does not execute planned
gates. This policy does not implement the P11-T02 shard runners, create a
scheduled workflow, change branch protection, activate planner execution
authority, change checkpoint behavior, or change scientific authority.

## Planning-job contract

The `validation-plan` responsibility is implemented in shadow form by
`validation_plan_shadow` in
`.github/workflows/project-control-validation.yml`. It must:

1. check out complete comparison history;
2. provision the repository's declared Python environment;
3. derive a deterministic, sorted path set from the pull-request base, push
   predecessor, or a bounded one-parent fallback;
4. run `scripts.validation.cli plan --profile affected` so manifest loading and
   validation occur before a plan is emitted;
5. upload the base SHA, changed paths, and `validation_plan_v1` JSON as one
   short-retention operational artifact; and
6. remain `continue-on-error: true` throughout shadow design and rollout.

The plan is non-authoritative operational evidence. Its
`planner_executes_commands` field remains false and its execution authority
remains the live manifest value, currently `legacy`.

## Primary shard topology

Primary ownership is an accounting rule, not an execution grant. Future shard
runners must consume selected gate IDs and entries from the plan artifact.
They must not carry independent hidden command lists.

| Primary shard | Responsibility | Current gate ownership |
| --- | --- | --- |
| `policy-fast` | Pure policy, classifier, signal, claim-language, and residue checks | `classify_changes`, `resolve_project_improvement`, `project_improvement_signals`, `documentation_impact`, `claim_language_changed`, `git_diff_check` |
| `research-control-integration` | Live research-control acceptance, freshness, continuation, and the governed local-only checkpoint boundary | `research_control_core`, `research_control_diff`, `current_frontier_freshness`, `compact_frontier_freshness`, `task_index_freshness`, `continue_memory_preflight`, `continue_context_resolution`, `checkpoint_transaction` |
| `dependency-graph` | One graph lifecycle and freshness result | `dependency_graph_freshness` |
| `memory-core` | Tracked memory synchronization, validation, and compatibility profile | `memory_sync`, `memory_core`, `profile_validate_memory` |
| `publication` | Documentation, spec, publication, HTML, Mermaid, and surface-audit checks | `documentation_surface_audit`, `spec_depth`, `publication_validation`, `profile_validate_html_explainers`, `profile_audit_documentation_surfaces`, `mermaid_sources` |
| `scientific-support` | Repository test shard, claim graph, and targeted scientific derivative checks | `test_shard_repository`, `claim_graph_validation`, `targeted_pdf_build` |
| `local-retrieval` | Local-only retrieval synchronization and diagnostic health | `local_retrieval_sync`, `local_retrieval_lint`, `memory_status_diagnostic`, `memory_lookup_diagnostic`, `memory_search_diagnostic`, `route_orbit_diagnostic` |
| `orchestration-equivalence` | Route-signature and legacy-versus-planner/profile compatibility evidence | `route_signature_diagnostic`, `profile_validate_project_control`, `profile_full_research_control`, `profile_ci_project_control` |

`validation-plan` owns plan production and no gate execution.
`scheduled-full` owns composition and no primary gates. Therefore every live
manifest gate has exactly one primary owner even when a scheduled run composes
all applicable shards.

## Gate and test-shard accounting

The live manifest currently associates all gates with the legacy coverage
fixture
`tests/fixtures/validation_manifest/legacy_gate_coverage_v1.json`. That field
proves catalog coverage; it is not an executable CI shard list.

P11-T02 must derive executable test selection from manifest plan entries and
the following responsibility boundary:

- policy and planner tests follow `policy-fast`;
- research-control and checkpoint integration tests follow
  `research-control-integration`;
- dependency lifecycle tests follow `dependency-graph`;
- memory and tracked-memory integration tests follow `memory-core`;
- publication, HTML, Mermaid, and documentation tests follow `publication`;
- packet-specific checkers and the repository test shard follow
  `scientific-support`;
- ignored local-retrieval diagnostics follow `local-retrieval`; and
- legacy/planner equivalence fixtures follow `orchestration-equivalence`.

A test may exercise multiple gates, but it has one primary CI owner. Another
shard may consume its existing receipt only when the evidence-identity and
obligation-resolution policies permit reuse. It may not rerun the test merely
because a second responsibility names the same obligation.

## Full and scheduled composition

`scheduled-full` composes the unfiltered `full` profile, the explicit doctor
health surface, live determinism, and cache-bypass auditing. It does not acquire
primary ownership of the composed gates.

The `full` profile union is the planner-resolved set of nontransactional
blocking gates plus the profile's advisory and diagnostic members.
`checkpoint_transaction` remains inventoried under
`research-control-integration` but is never executed in hosted CI; it is owned
by the governed local staged checkpoint. Local-only doctor gates are scheduled
in an environment that can represent local retrieval honestly or return an
explicit applicable skip.

Deduplication precedes sharding. A composed run executes each selected gate
once per evidence identity, after prerequisites, and records any satisfied or
superseded obligation rather than launching a second compatibility recipe.

## Required and optional checks

During P11-T01 and the later shadow rollout:

- `Validate project-control gates` remains required and authoritative;
- `Validate generated memory surfaces` remains required and authoritative;
- `Plan validation shards (shadow)` is optional and fail-open;
- individual future responsibility shards must not become branch-protection
  required checks while path filtering could make their check names disappear;
  and
- `local-retrieval` is optional on ordinary pull requests, required only when
  the plan selects affected local-retrieval work in a capable environment, and
  included in scheduled doctor health.

A stable aggregate check name may become required only in a separately
authorized cutover task after it consumes every selected shard receipt and
fails closed on missing required evidence. This packet does not create that
aggregate.

## Inapplicable shard contract

A future shard with zero selected primary gates must still start and publish a
compact receipt. It returns process success with:

- `status: PASS`;
- one result per planned-but-inapplicable gate using
  `SKIP_NOT_APPLICABLE`, when such results are represented;
- `selected_gate_count: 0`;
- the plan hash and shard ID;
- the deterministic selection reason; and
- no command execution, mutation, cache hit, or source-authority claim.

The shard must not disappear through job-level path filters. The plan controls
applicability inside a stable job identity.

## Concurrency, timeouts, and failure behavior

The workflow-level concurrency group and `cancel-in-progress: true` remain
unchanged. The shadow planner has a 15-minute timeout. Existing legacy
project-control and memory jobs retain their 45-minute and 20-minute timeouts.
Future shard timeouts must be bounded by the maximum selected gate timeout plus
setup allowance and must be implemented only in P11-T02 or a later authorized
task.

Manifest, schema, plan-generation, or artifact-publication failure is visible
in the shadow job but cannot replace or weaken legacy acceptance. Unknown
governed paths continue to escalate the affected request to `full`. No
performance result compensates for a missing hard finding, wrong tree, missing
required receipt, or unexplained legacy/planner mismatch.

## Migration and rollback

P11-T02 may implement the stable shard jobs from this policy while retaining
the legacy jobs. Cutover requires the migration policy's comparison and
rollback evidence. Before that cutover:

- plan artifacts are observation only;
- legacy outcomes decide CI acceptance;
- no branch-protection requirement moves to a path-filtered shard;
- no manifest gate changes execution authority; and
- deleting or disabling the shadow planner restores the pre-P11-T01 workflow
  without changing validation semantics.

Workflow success, shard coverage, and validation receipts are operational
evidence only. They are not physics proof, ontology authority, benchmark
authority, Gate Chair authority, or Distance-to-GR progress.
