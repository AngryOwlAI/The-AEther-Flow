<!-- authority: control -->

# Validation gate ID catalog v1

## Status and boundary

- Catalog ID: `validation-gate-id-catalog-v1`
- Plan task: `P1-T02`
- Migration epoch: `legacy`
- Status: `active-policy`
- Execution authority changed: `false`
- Deduplication activated: `false`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims or physics authority changed: `false`

This catalog assigns stable semantic IDs to the 37 provisional gates in the
P0-T04 legacy invocation graph. It is a naming and contract source for later
planner work. Existing commands remain authoritative during the `legacy`
epoch; this document does not remove, reorder, cache, or supersede an
invocation.

## ID rules

1. A gate ID names one semantic contract and one implementation mode.
2. Different modes with different path selection, mutation, authority, or tree
   semantics receive different IDs.
3. Command spelling, wrapper name, or profile membership does not establish
   equivalence.
4. A legacy invocation resolves through its provisional `LVG-*` ID to exactly
   one canonical ID in the machine-readable contract file.
5. Unknown or ambiguous mappings fail closed and remain non-deduplicable.
6. The obligation name is stable vocabulary for roles and skills; it is not a
   command alias and does not create an additional execution.

## Canonical catalog

| Canonical gate ID | Legacy gate | Stable obligation | Execution class |
| --- | --- | --- | --- |
| `classify_changes` | `LVG-001` | `classify_changes` | blocking validator |
| `resolve_project_improvement` | `LVG-002` | `resolve_project_improvement` | advisory diagnostic |
| `project_improvement_signals` | `LVG-003` | `project_improvement_signals` | blocking validator |
| `documentation_impact` | `LVG-004` | `documentation_impact` | blocking validator |
| `documentation_surface_audit` | `LVG-005` | `documentation_surface_audit` | blocking validator |
| `memory_sync` | `LVG-006` | `memory_sync` | blocking mutator plus compatibility validation report |
| `memory_core` | `LVG-007` | `memory_core` | blocking validator |
| `local_retrieval_sync` | `LVG-008` | `local_retrieval_sync` | local-only mutator |
| `local_retrieval_lint` | `LVG-009` | `local_retrieval_health` | local-only validator |
| `memory_status_diagnostic` | `LVG-010` | `memory_status_diagnostic` | advisory diagnostic |
| `memory_lookup_diagnostic` | `LVG-011` | `memory_lookup_diagnostic` | advisory diagnostic |
| `memory_search_diagnostic` | `LVG-012` | `memory_search_diagnostic` | advisory diagnostic |
| `spec_depth` | `LVG-013` | `spec_depth` | blocking validator |
| `publication_validation` | `LVG-014` | `publication_validation` | blocking validator |
| `research_control_core` | `LVG-015` | `research_control_core` | blocking validator |
| `research_control_diff` | `LVG-016` | `research_control_diff` | blocking superset validator |
| `test_shard_repository` | `LVG-017` | `test_shard:repository` | blocking test shard |
| `current_frontier_freshness` | `LVG-018` | `current_frontier_freshness` | blocking validator |
| `compact_frontier_freshness` | `LVG-019` | `compact_frontier_freshness` | blocking validator |
| `dependency_graph_freshness` | `LVG-020` | `dependency_graph_freshness` | blocking validator |
| `task_index_freshness` | `LVG-021` | `task_index_freshness` | blocking validator |
| `claim_graph_validation` | `LVG-022` | `claim_graph_validation` | blocking validator |
| `claim_language_changed` | `LVG-023` | `claim_language_changed` | blocking validator |
| `route_signature_diagnostic` | `LVG-024` | `route_signature_diagnostic` | advisory diagnostic |
| `route_orbit_diagnostic` | `LVG-025` | `route_orbit_diagnostic` | advisory diagnostic |
| `git_diff_check` | `LVG-026` | `git_diff_check` | blocking validator |
| `targeted_pdf_build` | `LVG-027` | `targeted_pdf_build` | blocking mutator |
| `continue_memory_preflight` | `LVG-028` | `continue_memory_preflight` | blocking composite mutator |
| `continue_context_resolution` | `LVG-029` | `continue_context_resolution` | advisory routing diagnostic |
| `checkpoint_transaction` | `LVG-030` | `checkpoint_transaction` | blocking transaction wrapper |
| `profile_validate_project_control` | `LVG-031` | `profile:validate_project_control` | blocking profile wrapper |
| `profile_validate_memory` | `LVG-032` | `profile:validate_memory` | blocking mutating profile wrapper |
| `profile_validate_html_explainers` | `LVG-033` | `profile:validate_html_explainers` | blocking profile wrapper |
| `profile_audit_documentation_surfaces` | `LVG-034` | `profile:audit_documentation_surfaces` | blocking profile wrapper |
| `profile_full_research_control` | `LVG-035` | `profile:full_research_control` | blocking profile wrapper |
| `profile_ci_project_control` | `LVG-036` | `profile:ci_project_control` | blocking CI wrapper |
| `mermaid_sources` | `LVG-037` | `mermaid_sources` | nested blocking validator |

Wrapper IDs describe orchestration receipts only. Their nested gates retain
their own evidence identities; wrapper PASS is not independent evidence.

## First-wave supersedence boundary

The first-wave contract set concerns `research_control_core`,
`research_control_diff`, `claim_language_changed`, `memory_sync`,
`memory_core`, `publication_validation`, local-retrieval gates,
`documentation_impact`, and advisory diagnostic gates.

- `research_control_diff` is eligible to satisfy `research_control_core` only
  under the exact same-scope predicate in the contract file.
- `research_control_diff` cannot satisfy `claim_language_changed` until P1-T03
  proves path-set, taxonomy, reviewed-context, severity, and configuration
  equivalence. The contract is therefore defined but disabled.
- `memory_core` contains publication validation in the current implementation,
  but consolidation remains disabled pending the P1-T03 failure-mode corpus.
- `memory_sync` is a mutator. Its compatibility report never supersedes
  `memory_core`, publication validation, or a post-generation check.
- Local-retrieval gates are local-only and cannot satisfy tracked-state gates.
- Advisory diagnostics cannot satisfy blocking obligations.
- Working-tree evidence cannot satisfy staged-tree evidence, and
  pre-generation evidence cannot satisfy post-generation evidence.

## Activation and rollback

All supersedence entries are `policy_only_inactive`. Activation requires the
later P1-T03 and P2 evidence gates named by the v19 plan. If any predicate
field is absent, unresolved, or unequal, both legacy invocations remain
required. Rollback is therefore the current legacy graph with no command
removed.

This catalog creates no scientific proof, ontology status, benchmark status,
Gate Chair authority, or Distance-to-GR progress.
