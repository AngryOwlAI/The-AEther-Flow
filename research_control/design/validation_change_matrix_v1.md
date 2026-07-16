<!-- authority: control -->

# Validation Change Matrix v1

## Status and authority

- Matrix ID: `validation-change-matrix-v1`
- Plan task: `P5-T08`
- Migration epoch: `shadow_planner`
- Execution authority: legacy commands remain authoritative
- Golden fixture: `tests/fixtures/validation_plans/change_matrix_v1.json`
- Focused test: `tests/test_validation_change_matrix.py`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims changed: `false`
- Physics, proof, ontology, benchmark, or Gate Chair authority created: `false`

This matrix converts the stable change-family taxonomy into executable golden
planner evidence. Each row states the representative input, selected profile,
important gates or generators, intentional skips, and the reason for the
selection. The fixture stores the complete sorted plan and explanation hashes;
the table is the human-readable control view.

The shadow planner explains obligations but does not execute them. Legacy execution remains authoritative,
including the existing commands and governed checkpoint transaction.
A selected blocking gate must retain a legacy adapter and command mapping.

## Representative change matrix

| Case | Representative input | Effective profile and path families | Required obligations and generators | Intentional skips | Selection reason |
| --- | --- | --- | --- | --- | --- |
| `pure_python_validator` | Python validator implementation | `affected`; `validator_code` | gates `classify_changes`, `documentation_impact`, `research_control_diff`, `spec_depth`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Validator behavior requires focused specification-depth and project-control checks; precheckpoint planning cannot authorize a commit. |
| `research_control_yaml` | Task control YAML | `affected`; `control_state`, `dependency_graph_input`, `task_index_input` | gates `research_control_diff`, `dependency_graph_freshness`, `task_index_freshness`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Tracked task state affects control validation and both generated routing indexes. |
| `registered_markdown` | Registered canonical Markdown | `affected`; `registered_markdown` | gates `documentation_impact`, `memory_sync`, `memory_core`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction`, `targeted_pdf_build` | Canonical Markdown requires documentation and memory parity, but no TeX-to-PDF obligation. |
| `tex_pdf_required` | Registered TeX with `pdf_required=true` | `affected`; `registered_tex`, `required_pdf` | gates `targeted_pdf_build`, `memory_sync`, `memory_core`; generators `continue_memory_preflight`, `memory_sync`, `targeted_pdf_build` | `checkpoint_transaction` | The TeX registry explicitly requires a targeted PDF derivative and memory refresh. |
| `tex_without_pdf` | Registered task-local TeX without a PDF obligation | `affected`; `control_state`, `dependency_graph_input`, `registered_tex`, `task_index_input` | gates `research_control_diff`, `dependency_graph_freshness`, `task_index_freshness`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction`, `targeted_pdf_build` | Registration alone does not create a PDF requirement; task-local control routing still requires graph and index freshness. |
| `html_spec_with_mermaid` | Registered HTML explainer spec plus Mermaid source | `affected`; `mermaid`, `publication_spec`, `registered_markdown` | gates `publication_validation`, `mermaid_sources`, `memory_sync`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction`, `targeted_pdf_build` | Source-backed publication and Mermaid parity apply without a TeX derivative. |
| `memory_code` | Project-memory implementation | `affected`; `memory_code` | gates `memory_sync`, `memory_core`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Memory implementation changes require regenerated-memory and core-system checks. |
| `dependency_graph_input` | Program state | `affected`; `control_state`, `dependency_graph_input` | gates `dependency_graph_freshness`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction`, `task_index_freshness` | Program state affects the dependency graph but is not itself a task-index input. |
| `task_index_input` | Research-task registry | `affected`; `control_state`, `dependency_graph_input`, `task_index_input` | gates `dependency_graph_freshness`, `task_index_freshness`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | The registry is an input to both generated routing surfaces. |
| `scientific_checker` | Support-formalization scientific checker | `affected`; `scientific_checker` | gates `test_shard_repository`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Checker code requires the repository test shard, without granting proof or scientific claim authority. |
| `local_retrieval_only` | Ignored local memory database under `.local/` | `doctor`; `local_retrieval` | gates `local_retrieval_sync`, `local_retrieval_lint`, `memory_status_diagnostic`; generator `local_retrieval_sync` | `checkpoint_transaction`, `research_control_diff` | Ignored retrieval state is diagnostic and non-authoritative; tracked control acceptance is irrelevant. |
| `ci_orchestration` | Project-control workflow | `affected`; `ci_orchestration` | gates `classify_changes`, `documentation_impact`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Orchestration changes require classifier, documentation-impact, and control-diff parity. |
| `deletion` | Deleted task control record | `affected`; `control_state`, `dependency_graph_input`, `task_index_input` | gates `dependency_graph_freshness`, `task_index_freshness`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | A deleted pre-change path remains classifiable and can invalidate both routing derivatives. |
| `rename` | Old and new validator-test paths | `affected`; `validator_code` | gates `spec_depth`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Both rename endpoints participate in classification, preserving focused validator coverage. |
| `mixed_change` | Markdown, planner code, and task control YAML | `affected`; union of `ci_orchestration`, `control_state`, `dependency_graph_input`, `mermaid`, `registered_markdown`, `task_index_input`, `validator_code` | gates `mermaid_sources`, `dependency_graph_freshness`, `task_index_freshness`, `research_control_diff`; generators `continue_memory_preflight`, `memory_sync` | `checkpoint_transaction` | Mixed inputs take the deterministic union of family obligations without dropping a blocking gate. |
| `unknown_governed_path` | Unrecognized tracked governed path | requested `affected`, effective `full`; `unknown_governed_path` | gates `profile_full_research_control`, `profile_ci_project_control`, `test_shard_repository`; generators `continue_memory_preflight`, `memory_sync`, `profile_validate_memory`, `targeted_pdf_build` | `checkpoint_transaction` | Unknown governed paths fail safe to exhaustive nontransactional coverage; they never produce silent `no_action`. |
| `irrelevant_local_retrieval` | Ignored `.local/` cache path in the fast loop | `fast`; `local_retrieval` | gates `classify_changes`, `git_diff_check`; generator `continue_memory_preflight` | `checkpoint_transaction`, `research_control_diff` | An irrelevant ignored cache path remains explicit in the explanation while tracked control validation is not selected. |

## Explanation contract

Every golden row must produce deterministic, bounded explanation output that
states the requested and effective profiles, readiness status, legacy
execution authority, selected gates, generators, test shards, ignored or
unknown paths, and skipped gates with their policy reasons. Repeating the same
input must reproduce the same canonical-plan and explanation hashes.

The fixture records exact hashes for all 17 rows. A hash change is blocking
until the matrix, fixture, and authorized policy change are reviewed together.
The explanation must remain within the command-output bound enforced by the
focused test.

## Failure-path and mutation coverage

The focused test removes one required CI gate-to-command mapping from an
in-memory manifest copy. The planner must then classify the affected
orchestration path as unknown and select `full`; it must not return
`no_action`, silently omit the gate, or acquire execution authority.

The same test also checks:

- every selected blocking gate has a legacy adapter and at least one command;
- all matrix plans are deterministic across repeated evaluation;
- selected test shards resolve to tracked paths;
- local-retrieval inputs remain explicit, ignored, and non-authoritative;
- deletion and rename cases preserve the supplied path identities; and
- the human-readable matrix and machine-readable fixture have identical case
  coverage.

## Migration boundary

This packet adds no executor, cache-reuse authority, profile promotion,
manifest gate, CI enforcement, or checkpoint behavior. It changes no canonical
physics source and promotes no ontology, coupling, metric, benchmark, proof, or
scientific claim. A later authorized packet may consume this evidence when it
decides whether planner output can affect execution.
