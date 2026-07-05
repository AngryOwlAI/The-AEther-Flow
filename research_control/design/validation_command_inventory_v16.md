<!-- authority: control -->

# Validation Command Inventory v16

This inventory tracks v16 validation commands as operational controls. A PASS
result means the named control ran successfully in the local repository state.
Successful validator results are operational receipts only. They are not proof
authority, physics-claim authority, source-law adoption, matter-coupling
derivation, Einstein-equation derivation, benchmark promotion, Gate Chair
closure, or completed-derivation evidence.

## P15 Compact Frontier Checks

| Check | Command | Purpose | Authority level | When to run |
| --- | --- | --- | --- | --- |
| compact frontier render check | `.venv/bin/python scripts/research_control/render_compact_current_frontier_v16.py --check` | Confirm compact YAML, JSON, and generated Markdown match tracked state. | `required-render-check` | After program state, latest handoff, current-frontier, or Distance-to-GR tracked-state inputs change. |
| compact frontier synchronization validation | `.venv/bin/python scripts/research_control/validate_compact_current_frontier_v16.py --json` | Fail on active-task, latest-handoff, next-route, high-risk-row, blocked-claim, authority-warning, and protected-target overpromotion drift in compact outputs. | `required-gate` | Before checkpoint when compact frontier outputs or their tracked inputs change. |
| integrated research-control validation | `.venv/bin/python scripts/research_control/validate_research_control.py` | Runs the compact synchronization hook as part of the broader research-control spine validation. | `required-gate` | Before checkpoint for research-control state changes. |
| full local validation compact check | `.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json` | Includes `compact_current_frontier_check` in the local CI-equivalent command plan. | `ci-smoke` | For local CI-equivalent runs and v16 final coverage audits. |

## P16 Consolidation Notice

P16-T02 owns the full v16 inventory update for minimum payload validation,
route-orbit hard-gate checks, target-import attack validation, claim graph
validation, dependency graph checks, documentation impact, claim-language
linting, memory bootstrap, and research-control validation. This P15-T03 entry
records the compact frontier check integration first so the new snapshot cannot
drift while later v16 inventory consolidation proceeds.

## P16-T02 Full V16 Validation Inventory

These commands are operational controls. They classify local repository state,
generated-output freshness, validator coverage, and claim-language safety.
They do not create physics authority. In particular, no command below can
authorize source-law adoption, unrestricted `RR_E` theorem status, matter
semantics, detector semantics, coupling-law adoption, matter-coupling
derivation or adoption, stress-energy semantics, matter action, Einstein
equations, benchmark promotion, Gate Chair closure, proof authority, or
completed derivation.

| Check | Command | Purpose | Authority level | When to run |
| --- | --- | --- | --- | --- |
| memory preflight | `.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json` | Refresh or confirm local retrieval layers before Director routing; local retrieval remains navigation only. | `required-gate` | Before every Director routing decision or state-changing continue-research packet. |
| memory status receipt | `.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json` | Record source-object, relationship, semantic, vault, and freshness status after preflight. | `required-gate` | Before every state-changing packet and in completion evidence. |
| memory bootstrap | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py` | Regenerate registries, wiki notes, indexes, and local retrieval derivatives from canonical sources. | `required-gate` | After registered source, registry, task, handoff, or generated-output inputs change. |
| memory validate-only | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only` | Confirm generated memory/wiki/registry outputs are synchronized without writing. | `required-gate` | Before checkpoint after memory-system or registered-source changes. |
| research-control validation | `.venv/bin/python scripts/research_control/validate_research_control.py` | Validate task, DDR, AgentJob, completion, handoff, registry, claim-boundary, and schema consistency. | `required-gate` | Before checkpoint for research-control state changes. |
| research-control diff validation | `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff` | Validate only changed research-control surfaces against the active diff boundary. | `required-gate` | Before checkpoint for any transaction with research-control changes. |
| full local control validation | `.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json` | Run the configured local CI-equivalent control, registry, claim-language, render-freshness, and drift gates. | `ci-smoke` | For final v16 validation packets and broad local smoke checks. |
| documentation impact | `.venv/bin/python scripts/project_control/validate_documentation_impact.py --json` | Confirm project-system changes either update required documentation surfaces or include a valid no-op rationale. | `required-gate` | Before checkpoint for state-changing project-system work. |
| project-improvement signal parity | `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted --json` | Confirm nonblank project-improvement signals have required registry/sidecar handling. | `required-gate` | Before checkpoint when completions or handoffs may emit project-improvement signals. |
| claim-language linter | `.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json` | Detect overclaims, target imports, bare high-risk acceptance wording, premature EFE claims, and validator-as-proof language in changed surfaces. | `required-gate` | Before checkpoint for changed claim-language-bearing surfaces. |
| current frontier render check | `.venv/bin/python scripts/research_control/render_current_frontier.py --check` | Confirm `research_control/current_frontier.md` matches tracked authority surfaces. | `required-render-check` | After program state, handoff, Distance-to-GR, or current-frontier inputs change. |
| current frontier repair render | `.venv/bin/python scripts/research_control/render_current_frontier.py --write` | Regenerate current-frontier snapshot from tracked authority surfaces. | `required-render-check` | When the render check reports drift or after active state changes. |
| compact frontier render check | `.venv/bin/python scripts/research_control/render_compact_current_frontier_v16.py --check` | Confirm compact YAML, JSON, and generated Markdown match tracked state. | `required-render-check` | After program state, latest handoff, current-frontier, or Distance-to-GR tracked-state inputs change. |
| compact frontier synchronization validation | `.venv/bin/python scripts/research_control/validate_compact_current_frontier_v16.py --json` | Fail on active-task, latest-handoff, next-route, high-risk-row, blocked-claim, authority-warning, and protected-target overpromotion drift in compact outputs. | `required-gate` | Before checkpoint when compact frontier outputs or their tracked inputs change. |
| dependency graph render check | `.venv/bin/python scripts/research_control/render_dependency_graph.py --check` | Confirm dependency graph JSON, DOT, and Markdown outputs are fresh. | `required-render-check` | After task, handoff, registry, current-frontier, or claim-boundary inputs change. |
| dependency graph repair render | `.venv/bin/python scripts/research_control/render_dependency_graph.py --json output/research_dependency_graph.json --markdown wiki/indexes/research_dependency_graph.md --dot output/research_dependency_graph.dot` | Regenerate dependency graph support artifacts. | `required-render-check` | When dependency graph freshness check reports drift. |
| claim graph generate check | `.venv/bin/python scripts/research_control/generate_claim_graph_v1.py --check` | Confirm claim graph outputs are fresh relative to tracked source authority. | `required-render-check` | After claim-boundary, Distance-to-GR, source-status, or frontier inputs change. |
| claim graph validation | `.venv/bin/python scripts/research_control/validate_claim_graph_v1.py --json` | Validate claim graph guard rows, non-promotion boundaries, and generated-authority warnings. | `required-gate` | Before final v16 validation and after claim graph inputs or outputs change. |
| minimum physics payload validation | `.venv/bin/python scripts/research_control/validate_minimum_physics_payload.py --live --json` | Validate live opt-in minimum-payload records and route-orbit policy fields; project-control evidence only. | `required-gate` | For physics packets with minimum-payload records and in final v16 validation. |
| minimum payload fixture regression | `.venv/bin/python scripts/research_control/validate_minimum_physics_payload.py --fixture-dir tests/fixtures/minimum_physics_payload --json` | Confirm known good/bad minimum-payload fixtures still classify correctly. | `ci-smoke` | When minimum payload policy, fixtures, or validator code changes. |
| route-orbit hard-gate check | `.venv/bin/python scripts/research_control/validate_route_orbits.py --sample recent-matter-rr-e --json` | Enforce route-orbit hard failures when the validator finds repeated no-payload route candidates. | `required-gate` | For route-orbit policy work and final v16 validation when hard-gate behavior is in scope. |
| route-orbit advisory diagnostic | `.venv/bin/python scripts/research_control/validate_route_orbits.py --sample recent-matter-rr-e --json --advisory-only` | Emit route-orbit diagnostics without blocking, for Director context and trend monitoring. | `advisory-diagnostic` | During routine continuation and when a hard gate is not the active packet boundary. |
| physics progress metrics | `.venv/bin/python scripts/research_control/report_physics_progress_metrics.py` | Report payload-density, route-orbit, same-burden, and gate-ready diagnostics. | `advisory-diagnostic` | During continuation context, final validation, and route-orbit review packets. |
| route signature extraction | `.venv/bin/python scripts/research_control/extract_route_signatures.py --sample recent-matter-coupling --json` | Extract route signatures for orbit analysis and Director context. | `advisory-diagnostic` | When selecting or reviewing repeated matter-coupling routes. |
| target-import fixture validation | `.venv/bin/python -m unittest tests/test_target_import_attack_fixtures.py tests/test_target_import_attack_validator.py` | Confirm target-import taxonomy, fixture catalog, and claim-language integration reject target imports and allow source-safe controls. | `required-gate` | After target-import taxonomy, fixture, linter, or attack-suite changes and in final v16 validation if implemented. |
| target-import claim-language focused test | `.venv/bin/python -m unittest tests/test_validate_claim_language.py` | Confirm claim-language taxonomy still rejects target imports, EFE overreads, source-law overreads, and validator-as-proof claims. | `ci-smoke` | When claim-language taxonomy, reviewed contexts, or attack fixtures change. |
| status-field compatibility validation | `.venv/bin/python scripts/research_control/validate_status_field_compatibility.py --json` | Validate v16 layered status-field compatibility and warning records. | `required-gate` | When layered status fields or risky status compatibility records change. |
| support-only formalization traceability | `.venv/bin/python scripts/research_control/support_formalization/validate_traceability_registry.py --json` | Validate support-only formalization proof-to-source traceability without granting proof authority. | `support-only` | When support-only formalization registry or formalization files change. |
| support-only formalization tests | `.venv/bin/python -m unittest tests/test_support_formalization_traceability_registry.py tests/test_support_only_finite_local_witness_schema.py tests/test_support_only_finite_toy_tag_obstruction.py` | Exercise support-only formalization helpers and traceability receipts. | `support-only` | When support-only formalization helpers or registry entries change. |
| git whitespace check | `git diff --check` | Confirm staged/working diff has no whitespace errors. | `required-gate` | Before checkpoint for every local transaction. |
| checkpoint transaction | `.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <JOB_ID>` | Re-run transaction checks, stage the allowed boundary, and create the deterministic research-control commit. | `required-gate` | Only after all state-changing transaction checks pass. |

## Authority Classification

- `required-gate`: a blocking operational control for the packet class named in
  the `When to run` column.
- `required-render-check`: a freshness check or deterministic render command
  for generated support artifacts.
- `advisory-diagnostic`: nonblocking context for Director routing; it can
  inform the next packet but cannot prove or promote a claim.
- `support-only`: formalization or regression support that must remain
  traceable to sources and explicitly lacks proof authority.
- `ci-smoke`: broader regression coverage used for local or final validation
  confidence; it is not a substitute for task-specific required gates.
