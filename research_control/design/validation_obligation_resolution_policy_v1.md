<!-- authority: control -->

# Validation Obligation Resolution Policy v1

## Purpose and authority

This policy defines how project-control skills and role declarations name
validation obligations without multiplying command executions. It centralizes
the current compatibility recipes for the `legacy_consolidated` epoch and
preserves the evidence-identity, supersedence, rollback, and checkpoint rules
already registered by v19.

An obligation declaration is not an execution request. When a role, skill,
task, or checkpoint names the same gate ID for the same transaction scope, the
transaction owes one valid evidence result, not one process invocation per
declaration. A second execution is required only when evidence identity differs,
including a different tree state, base ref, path set, configuration, or
generation state.

This policy changes control wording only. It does not change validator code,
role permissions, human gates, claim taxonomy, CI, Make targets, checkpoint
behavior, ordinary research routing, or physics authority.

## Named obligations and compatibility recipes

The canonical gate catalog owns gate identities. These recipes are the current
direct compatibility entry points when a narrow precheckpoint execution is
useful:

| Gate obligation | Current compatibility recipe |
| --- | --- |
| `memory_sync` | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py` |
| `memory_core` | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only` |
| `project_improvement_signals` | `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted` |
| `documentation_impact` | `.venv/bin/python scripts/project_control/validate_documentation_impact.py` |
| `research_control_core` | `.venv/bin/python scripts/research_control/validate_research_control.py` |
| `research_control_diff` | `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff` |
| `claim_language_changed` | `.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json` |
| `git_diff_check` | `git diff --check` |
| `checkpoint_transaction` | `.venv/bin/python scripts/research_control/checkpoint_research_transaction.py [--job-id <job-id>]` |

Task-selected test shards remain explicit in the owning AgentJob because their
scope is task-specific. A role registry label such as
`validate_documentation_impact`, `validate_research_control`, or `unittest`
declares the corresponding obligation family; it does not require another
standalone execution when valid same-identity evidence already exists.

## Resolution rules

1. Match evidence by the registered identity components before reusing it.
   Similar command text or a shared wrapper name is insufficient.
2. `memory_sync` is a mutator. Its receipt cannot satisfy `memory_core`,
   publication validation, or another post-generation validation obligation.
3. `research_control_diff` may satisfy `research_control_core` only when
   `rc_diff_satisfies_core_same_scope_v1` holds. It may satisfy
   `claim_language_changed` only when
   `rc_diff_satisfies_claim_language_same_scope_v1` holds. The integrated
   result must preserve raw failures and normalized finding identities.
4. Directly consolidated legacy chains record the integrated gate as executed
   and the same-scope target gate as satisfied or superseded. This bounded
   orchestration fact does not activate global planner supersedence or relax a
   fail-closed predicate.
5. Working-tree evidence and staged-tree evidence are distinct. A working
   result never satisfies a staged obligation, and a pre-generation result
   never satisfies a post-generation obligation.
6. Advisory diagnostics cannot satisfy blocking obligations. Local retrieval
   health cannot satisfy tracked-state acceptance.
7. Memory preflight and canonical source inspection are knowledge-retrieval
   requirements, not duplicated acceptance gates. Their commands and receipts
   remain explicit in the owning workflow.

## Checkpoint ownership

The governed checkpoint owns `checkpoint_transaction` and final staged
acceptance. It captures the transaction boundary, synchronizes generated state,
reclassifies the resulting paths, stages only allowed files, and validates the
actual index before commit.

Precheckpoint compatibility commands are editing aids. Their results may catch
defects early and may satisfy a named same-identity working obligation, but they
do not waive the final staged checkpoint or authorize a commit independently.
If the checkpoint changes the evidence identity or detects a hard failure, the
earlier result is not acceptance evidence for the staged tree.

## Skill and role contract rule

Skills should name the obligations their transaction must resolve and link to
this policy instead of repeating the recipe table. Role default-validator
labels remain auditable declarations of required evidence families. Neither
surface changes invocation count, authority, or acceptance semantics merely by
naming the same obligation.

The current active `project-control-maintainer@0.2.0` registry semantics remain
unchanged: it may modify authorized project-control sources, may not promote
claims, requires no default human gate, and retains the default validator labels
`validate_documentation_impact;validate_research_control;unittest`.

## Stop and rollback conditions

- Stop if wording makes final staged acceptance optional.
- Stop if a working result is offered as staged evidence.
- Stop if satisfaction is claimed without the registered same-scope predicate.
- Stop if a mutator or advisory result is offered as blocking validation.
- Roll back to explicit legacy obligation wording if skill authority markers,
  role semantics, documentation impact, or research-control validation fails.
- Validation evidence, tests, receipts, and checkpoint commits are not physics
  proof and cannot promote scientific claims.
