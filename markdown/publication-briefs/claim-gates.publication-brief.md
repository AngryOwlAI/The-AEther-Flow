---
brief_id: "PB-CLAIM-GATES"
subject: "Claim Gates, Negative Results, And Freeze Criteria"
reader: "Technical reader, maintainer, reviewer, or summarizing AI trying to understand how AEther-Flow prevents draft/control work from becoming public overclaim."
reader_job: "Understand how proposals, audits, refutations, stress tests, completions, handoffs, freeze labels, and human gates constrain what can be claimed."
document_type: "comparison_or_boundary_map"
reading_experience: "A source-first boundary map with a lifecycle model, scoped-obstruction comparison, allowed/forbidden claim table, and summary checklist."
narrative_structure:
  - "Open with claim gates as the project's anti-overclaim mechanism."
  - "Define proposal, audit, refutation, stress test, completion, handoff, freeze, and human gate in operational terms."
  - "Explain negative results as preserved scientific information rather than project failure."
  - "Separate scoped obstruction from global no-go language."
  - "Close with source-first summary rules and unsafe phrase inflation examples."
visual_strategy: "state_model"
source_basis:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/AGENT_ROLE_REGISTRY.csv"
authority_boundaries:
  - "The page may explain claim-control machinery and examples of allowed versus forbidden phrasing, but it cannot issue a Gate Chair verdict or create a new claim boundary."
  - "Freeze labels, scoped obstructions, completion records, validators, and generated public pages must remain control evidence, not physics authority by themselves."
output_surfaces:
  - "github-facing/claim-gates-explainer.md"
  - "html/claim-gates-explainer.html"
acceptance_criteria:
  - "Defines proposal, audit, refutation, stress test, completion, handoff, freeze, and human gate without changing role authority."
  - "Explains negative-result preservation as scientific discipline rather than project failure."
  - "Separates scoped obstruction and freeze language from broad rejection of the theory."
  - "States that Gate Chair decisions are human-gated and not auto-executed by validators or documentation."
  - "Includes allowed and forbidden claim examples grounded in the claim boundary registry."
  - "Uses status-card v2 wording before broader gate examples for M_src, g_eff, and matter-sector evidence/preconditions."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Gate Chair verdict or benchmark promotion."
  - "Unregistered claim boundary creation."
  - "Freeze label converted into broad theory rejection."
  - "Rejected draft/control packet converted into global ontology rejection."
  - "Validator pass or generated documentation treated as scientific evidence."
migration_status: "reviewed"
---

# Publication Brief: Claim Gates, Negative Results, And Freeze Criteria

## P9-T03 Status-Card V2 Calibration Note

P9-T03 body guidance references `research_control/design/status_card_v2_schema.md`
and `research_control/design/accepted_status_calibration_v2.yaml` as
wording-calibration context. They are not added to `source_basis` until a
bounded HTML regeneration and publication-registry synchronization packet
updates every generated surface.

This Phase 2B page explains the project's claim-control machinery. It helps
readers understand why failed or frozen routes are preserved, how claim
promotion remains gated, and why local obstruction language must not be
inflated into broad rejection of the theory.
