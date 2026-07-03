<!-- authority: control -->

# V15 Validation Command Inventory

## Scope

This inventory implements v15 P11-T01. It records the validation commands
needed for research-control transactions before P11-T02 turns them into a
repeatable CI or local CI-equivalent entry point.

The inventory is operational project-control evidence only. It does not change
physics status, establish proof authority, authorize claim promotion, or alter
Distance-to-GR status.

## Use Levels

| Level | Meaning |
| --- | --- |
| `required-preflight` | Must run before Director routing or project-knowledge changes when the continue-research skill applies. |
| `required-sync` | Must run after state-changing source or registry changes before checkpoint. |
| `required-gate` | Must pass before checkpoint for the applicable transaction state. |
| `required-render-check` | Must pass when the transaction changes the rendered surface or its inputs. |
| `advisory-diagnostic` | Supplies route-risk evidence but is not by itself a physics verdict. |
| `ci-smoke` | Useful as a repeatable regression layer for P11-T02 and later CI/local-CI work. |

## Command Inventory

| Category | Command | Purpose | Authority level | When required |
| --- | --- | --- | --- | --- |
| memory bootstrap | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py` | Regenerate registered memory/wiki/semantic derivative surfaces from canonical sources and registries. | `required-sync` | After changing registered sources, registries, research-control state, or generated-memory inputs. |
| memory validate-only | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only` | Confirm generated memory/wiki/semantic derivative surfaces match canonical sources and registries without rewriting. | `required-gate` | Before checkpoint and in read-only CI-equivalent validation. |
| memory preflight | `.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json` | Check local retrieval freshness and refresh local retrieval caches when needed before routing. | `required-preflight` | Before continue-research Director routing and again after bootstrap if local retrieval drift was repaired. |
| research-control validation | `.venv/bin/python scripts/research_control/validate_research_control.py` | Validate task, DDR, AgentJob, completion, handoff, role overlay, claim-boundary, and registry spine consistency. | `required-gate` | After research-control state changes and before checkpoint. |
| research-control diff validation | `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff` | Check the current diff against the active AgentJob write-path allowlist and control boundaries. | `required-gate` | Before checkpoint on an unstaged working tree. |
| research-control staged diff validation | `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff --staged-only` | Check staged transaction paths against the active AgentJob write-path allowlist and control boundaries. | `required-gate` | Inside checkpoint or any manual staged verification. |
| claim-language changed-file lint | `.venv/bin/python scripts/project_control/validate_claim_language.py --json --changed` | Scan changed claim-language gate surfaces for hard-fail wording and reviewed historical warnings. | `required-gate` | Before checkpoint for claim-language gate paths in the working tree. |
| claim-language staged lint | `.venv/bin/python scripts/project_control/validate_claim_language.py --json --staged` | Scan staged claim-language gate surfaces for hard-fail wording and reviewed historical warnings. | `required-gate` | Inside checkpoint or any manual staged verification. |
| documentation-impact validation | `.venv/bin/python scripts/project_control/validate_documentation_impact.py --json` | Validate documentation-impact receipt handling for project-system or documentation-affecting changes. | `required-gate` | Before checkpoint when the classifier says documentation impact is required. |
| documentation-impact staged validation | `.venv/bin/python scripts/project_control/validate_documentation_impact.py --staged` | Validate staged documentation-impact handling. | `required-gate` | Inside checkpoint or manual staged verification. |
| project-change classification | `.venv/bin/python scripts/project_control/classify_project_changes.py --json` | Classify changed paths and identify documentation-impact and project-system implications. | `required-gate` | Before documentation-impact validation and checkpoint. |
| project-improvement signal validation | `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted --json` | Validate emitted project-improvement signals and sidecar routing records. | `required-gate` | After completions or handoffs that can emit project-improvement signals. |
| registry consistency | `.venv/bin/python scripts/research_control/validate_research_control.py` | Enforce registry column, value, duplicate-id, role, decision, job, task, handoff, and claim-boundary consistency. | `required-gate` | Before checkpoint for any control registry change. |
| generated registry consistency | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only` | Enforce generated registry metadata and source-hash consistency for memory/wiki derivative registries. | `required-gate` | Before checkpoint when generated registries or registered Markdown/TeX sources change. |
| current frontier render write | `.venv/bin/python scripts/research_control/render_current_frontier.py --write` | Regenerate `research_control/current_frontier.md` from tracked control state. | `required-sync` | After program state or latest handoff changes. |
| current frontier render check | `.venv/bin/python scripts/research_control/render_current_frontier.py --check` | Confirm `research_control/current_frontier.md` is fresh relative to tracked control state. | `required-render-check` | Before checkpoint when frontier inputs changed. |
| dependency graph render write | `.venv/bin/python scripts/research_control/render_dependency_graph.py --json output/research_dependency_graph.json --markdown wiki/indexes/research_dependency_graph.md --dot output/research_dependency_graph.dot` | Regenerate the navigational dependency graph artifacts from tracked state. | `required-sync` | After control state, registry, or handoff changes that affect the graph. |
| dependency graph check | `.venv/bin/python scripts/research_control/render_dependency_graph.py --check` | Confirm dependency graph JSON, Markdown, and DOT artifacts are fresh. | `required-render-check` | Before checkpoint when graph inputs changed. |
| theorem inventory check | `.venv/bin/python scripts/research_control/validate_research_control.py` | Runs the integrated `validate_frontier_theorem_inventory` check for theorem-inventory required fields and source paths. | `required-gate` | Before checkpoint whenever theorem-inventory data or related research-control records change. |
| route-orbit extraction pilot | `.venv/bin/python scripts/research_control/extract_route_history.py --sample recent-matter-rr-e --json` | Extract recent route signatures for route-orbit diagnostic review. | `advisory-diagnostic` | When route-risk diagnostics or freeze-review inputs are being evaluated. |
| route-orbit check | `.venv/bin/python scripts/research_control/validate_route_orbits.py --sample recent-matter-rr-e --json --advisory-only` | Validate repeated route-orbit candidates against the route-history schema without converting the advisory to a physics verdict. | `advisory-diagnostic` | Before freeze-review decisions or route-orbit control changes. |
| v15 route-signature pilot | `.venv/bin/python scripts/research_control/extract_route_signatures.py --sample recent-matter-coupling --json` | Project v15 route signatures for the matter-coupling sample used by P10 route-orbit hardening. | `advisory-diagnostic` | When maintaining the P10 route-signature tooling or P10-derived policy. |
| source-extension classification check | `.venv/bin/python scripts/research_control/validate_research_control.py` | Runs integrated source-extension classification receipt enforcement for post-policy source-extension completions. | `required-gate` | Before checkpoint for source-extension routes or changes to source-extension classification policy. |
| source-extension focused tests | `.venv/bin/python -m unittest tests.test_research_control.ResearchControlTests.test_source_extension_completion_requires_classification_receipt tests.test_research_control.ResearchControlTests.test_source_extension_classification_receipt_requires_required_fields tests.test_research_control.ResearchControlTests.test_source_extension_classification_receipt_accepts_valid_record tests.test_research_control.ResearchControlTests.test_roadmap_selector_accepts_source_extension_category` | Exercise the source-extension classification validator rules added for v15 P6-T03. | `ci-smoke` | In P11-T02 local CI-equivalent smoke coverage and after source-extension validator edits. |
| route-orbit focused tests | `.venv/bin/python -m unittest tests.test_route_orbit_validator tests.test_route_history_extractor tests.test_route_signature_extractor` | Exercise route-history extraction, route-orbit validation, and v15 route-signature projection. | `ci-smoke` | In P11-T02 local CI-equivalent smoke coverage and after route-orbit tooling edits. |
| frontier render focused tests | `.venv/bin/python -m unittest tests.test_render_current_frontier tests.test_render_dependency_graph` | Exercise renderers that back current-frontier and dependency-graph freshness checks. | `ci-smoke` | In P11-T02 local CI-equivalent smoke coverage and after renderer edits. |
| claim-language focused tests | `.venv/bin/python -m unittest tests.test_validate_claim_language` | Exercise claim-language taxonomy and changed-path gate behavior. | `ci-smoke` | In P11-T02 local CI-equivalent smoke coverage and after claim-language linter edits. |
| project-control smoke tests | `.venv/bin/python -m unittest discover -s tests` | Run the repository test suite as a broad local CI smoke layer. | `ci-smoke` | For full local CI-equivalent validation when runtime budget permits or before final integration. |
| whitespace diff check | `git diff --check` | Detect whitespace errors in the transaction diff. | `required-gate` | Before checkpoint for all state-changing transactions. |
| checkpoint transaction | `.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <job_id>` | Re-run required gates, stage allowed paths, and commit the bounded transaction. | `required-gate` | Final step after a successful state-changing AgentJob. |

## Minimal P11-T02 Local CI Sequence

P11-T02 should turn the inventory into a deterministic entry point. The
minimum local CI-equivalent sequence is:

1. `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only`
2. `.venv/bin/python scripts/research_control/render_current_frontier.py --check`
3. `.venv/bin/python scripts/research_control/render_dependency_graph.py --check`
4. `.venv/bin/python scripts/project_control/validate_claim_language.py --json --changed`
5. `.venv/bin/python scripts/project_control/validate_documentation_impact.py --json`
6. `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted --json`
7. `.venv/bin/python scripts/research_control/validate_research_control.py`
8. `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff`
9. `.venv/bin/python scripts/research_control/validate_route_orbits.py --sample recent-matter-rr-e --json --advisory-only`
10. `git diff --check`

If runtime budget permits, P11-T02 may add:

```zsh
.venv/bin/python -m unittest discover -s tests
```

## Boundary

No physics delta.

This inventory does not make validation, CI, generated registries, memory
derivatives, route-orbit diagnostics, or test success into physics evidence.
Those surfaces are operational receipts only. They do not authorize canonical
ontology edits, source-law adoption, matter semantics, detector semantics,
coupling-law adoption, matter-coupling derivation or adoption, `MetricData(E)`
adoption, `g_eff` scope expansion, stress-energy semantics, stress-energy
tensor construction, matter action, variation principle, Einstein equations,
benchmark promotion, Gate Chair verdicts, completed derivation, program-wide
no-go conclusions, or future source-extension impossibility.
