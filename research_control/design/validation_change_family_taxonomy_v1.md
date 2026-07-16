<!-- authority: control -->

# Validation Change-Family Taxonomy v1

## Purpose

This document defines the stable path-family output of
`scripts/project_control/classify_project_changes.py` for the v19 shadow
planner. The classifier remains a pure selector input: it may inspect Git path
state and bounded registry metadata, but it does not launch validators,
generators, planners, or checkpoint operations.

The taxonomy supplements the classifier's existing documentation-impact
contract. Existing fields, reason codes, recommended roles, generated-direct-
edit blocks, and `.local/` handling remain compatible.

## Output contract

The classifier returns these deterministic additions:

- `path_family_tags`: sorted union of stable family tags.
- `path_family_reasons`: sorted union of registry and path-rule reasons.
- `canonical_paths`: sorted canonical source or control inputs affected by the
  changed paths.
- `generated_derivatives`: sorted derivative paths associated with the change.
- `affected_source_object_ids`: sorted canonical source IDs from the Markdown
  or TeX source registries.
- `path_family_details`: one path-sorted record containing the same evidence
  for each changed path.
- `recommended_validation_profile`: `affected` for recognized governed
  changes, `full` for an unknown governed path, and blank when only ignored
  local-retrieval state changed.

These fields contain no validation verdict. They are selection evidence for a
later planner and cannot satisfy a blocking gate by themselves.

## Stable families

| Tag | Deterministic evidence | Planner meaning |
| --- | --- | --- |
| `control_state` | Task, handoff, program-state, project-improvement handoff, or control-registry path. | Control-state invariants may be affected. |
| `role_or_schema_contract` | Registered role/schema/policy metadata or a role, schema, or skill-contract path. | Role, schema, permission, or workflow contract checks may be affected. |
| `validator_code` | Project-control, validation-adapter, research validator, or test path. | Validator behavior or its focused shard may be affected. |
| `memory_code` | Project-memory-system or explicit memory/local-retrieval implementation path. | Memory synchronization or core behavior may be affected. |
| `registered_markdown` | Exact path or generated output resolved through `MARKDOWN_SOURCE_REGISTRY.csv`. | A canonical registered Markdown source or derivative is affected. |
| `registered_tex` | Exact path or generated output resolved through `TEX_SOURCE_REGISTRY.csv`. | A registered TeX source or derivative is affected. |
| `required_pdf` | A TeX registry row has `pdf_required=true`, or the changed path is that row's registered PDF. | The targeted TeX-to-PDF obligation may be affected. |
| `publication_spec` | Registered `html_explainer_source_spec` metadata or the governed spec directory. | Publication-spec and source-backed HTML parity may be affected. |
| `html` | Registered or governed HTML output path. | Generated HTML validation may be affected; HTML is not source authority. |
| `mermaid` | Registered Markdown metadata has `contains_mermaid=true`. | Mermaid source/render validation may be affected. |
| `dependency_graph_input` | Tracked task/handoff/program state, graph registries, or dependency-graph outputs. | Dependency-graph freshness may be affected. |
| `task_index_input` | Task records or the research-task/AgentJob registries and task-index outputs. | Task-index freshness may be affected. |
| `claim_graph_input` | Claim, claim-boundary, relationship, claim-graph, or claim-graph tool path. | Claim-graph validation may be affected. |
| `traceability` | Formalization traceability registry, tool, test, or contract path. | Support-only traceability checks may be affected. |
| `scientific_checker` | Explicit research checker or support-formalization checker path. | A scientific checker shard may be affected without granting proof authority. |
| `local_retrieval` | Ignored `.local/` state or an explicit local-retrieval path. | Local retrieval remains non-authoritative and normally advisory. |
| `ci_orchestration` | Workflow, Make entrypoint, validation orchestration, checkpoint, continuation, or full-runner path. | CI/orchestration parity may be affected. |
| `unknown_governed_path` | Non-ignored, non-generated path with neither registry nor existing classifier-rule coverage. | Select `full`; never silently return no validation action. |

## Registry resolution

The classifier reads only bounded CSV metadata from:

- `registries/MARKDOWN_SOURCE_REGISTRY.csv`;
- `registries/TEX_SOURCE_REGISTRY.csv`; and
- `registries/HTML_EXPLAINER_REGISTRY.csv`.

For a registered source it returns the source object ID, source path, declared
generated outputs, and the `contains_mermaid` or `pdf_required` metadata when
present. For a registered derivative it resolves back to the canonical
Markdown or TeX source. HTML registry `source_basis` metadata resolves a
generated HTML output to its registered Markdown publication spec.

The classifier does not read large artifact bodies to infer families. Existing
mixed-Markdown authority inspection remains limited to the changed lines and
continues to govern documentation-role routing.

## Git state semantics

- Working mode includes staged, unstaged, deleted, renamed, and untracked
  paths relative to the selected base ref.
- Staged-only mode includes only index changes.
- Both old and new names of a detected rename or copy are classified.
- A deletion is classified from its tracked pre-deletion path.
- `--no-untracked` excludes untracked paths without changing tracked results.
- Inputs and output arrays are sorted and deduplicated.

## Failure and authority boundaries

An unregistered generated derivative remains blocked by the existing
`direct_generated_derivative_edit` rule. A known generated derivative never
becomes canonical authority. An unknown governed canonical path selects the
`full` profile and records `unknown_governed_path`; it does not silently skip
validation.

The classifier does not decide that a gate passed, apply manifest
supersedence, activate cache reuse, change execution authority, edit canonical
physics sources, promote a claim, or alter ordinary research handoff
`handoff-0740`.
