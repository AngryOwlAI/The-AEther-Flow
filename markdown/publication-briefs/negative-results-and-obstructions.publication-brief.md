---
brief_id: "PB-NEGATIVE-RESULTS-AND-OBSTRUCTIONS"
subject: "Negative Results And Obstructions"
reader: "Technical reader, maintainer, reviewer, or future agent trying to understand frozen routes and scoped obstructions without overreading them."
reader_job: "Understand why negative results are useful constraints, which current routes are frozen or obstructed, and what remains open."
document_type: "comparison_or_boundary_map"
reading_experience: "A source-first boundary map that treats negative results as reusable control knowledge, not as a defeat narrative or proof of broad impossibility."
narrative_structure:
  - "Open with the reason negative results are preserved as first-class research outputs."
  - "Define frozen local route, scoped obstruction, minimal countermodel, certificate gap, and open continuation in plain technical language."
  - "Summarize the current v15 inventory entries without replacing their source artifacts."
  - "Separate what each result blocks from what it explicitly does not block."
  - "Close with safe public language rules and source-inspection guidance."
visual_strategy: "source_matrix"
source_basis:
  - "research_control/design/negative_result_inventory_v15.md"
  - "research_control/design/frontier_theorem_inventory.md"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "AGENTS.md"
authority_boundaries:
  - "The brief may describe scoped frozen or obstructed routes as constraints on specific attempted routes."
  - "The brief cannot convert scoped negative results into program-wide rejection, future source-extension impossibility, benchmark promotion, or completed derivation."
  - "Tracked source artifacts and registries remain authority; any future public page is derivative."
  - "This brief does not create a publication action, source spec, GitHub-facing page, HTML output, screenshot review, or corpus migration."
output_surfaces:
  - "markdown/html-explainer-specs/negative-results-and-obstructions-explainer.md"
  - "github-facing/negative-results-and-obstructions-explainer.md"
  - "html/negative-results-and-obstructions-explainer.html"
acceptance_criteria:
  - "States that negative results are valuable constraints."
  - "States that scoped obstructions are not program-wide rejection claims."
  - "States that frozen local routes do not prove future source-extension impossibility."
  - "States that exact source artifacts remain authority."
  - "Uses status-card v2 order for public negative-result summaries: scoped status, exact route scope, blocked overread, and next burden."
  - "Uses the v15 negative-result inventory as the primary source basis."
  - "Does not imply publication action from the brief itself."
forbidden_patterns:
  - "Program-wide rejection from a scoped obstruction."
  - "Future source-extension impossibility from a frozen local route."
  - "Benchmark promotion or completed derivation."
  - "Treating validators, generated wiki notes, generated public pages, or this brief as physics authority."
  - "Using negative results as a matter-semantics, detector-semantics, coupling-law, matter-coupling, stress-energy, matter-action, or Einstein-equation claim."
migration_status: "deferred"
---

# Publication Brief: Negative Results And Obstructions

## P9-T03 Status-Card V2 Calibration Note

P9-T03 body guidance references `research_control/design/status_card_v2_schema.md`
and `research_control/design/accepted_status_calibration_v2.yaml` as
wording-calibration context. They are not added to `source_basis` until a
bounded HTML regeneration and publication-registry synchronization packet
updates every generated surface.

This deferred publication brief prepares a future public-safe explainer about
negative results. It does not publish that explainer. Its immediate function is
to define the reader job, source basis, claim boundaries, and acceptance criteria
for a later source-spec packet.

The source message is narrow. Negative results are valuable because they record
where a route failed, froze, or requires explicit missing evidence. They prevent
the same overread from being repeated and give future packets reusable
constraints. They are not by themselves a broad rejection of the research
program.

The future explainer should use the v15 inventory as its primary source. It
should distinguish a frozen local route from a scoped obstruction, a certificate
gap, a minimal countermodel, and an open continuation route. Each inventory
entry should be summarized through two questions: what does this block, and
what does it not block?

The public wording must remain fail-closed. A frozen finite route does not prove
future source-extension impossibility. A scoped obstruction does not become a
program-wide rejection claim. A countermodel or certificate gap does not supply
matter semantics, detector semantics, coupling law, matter coupling,
stress-energy semantics, matter action, Einstein equations, benchmark
promotion, or completed derivation.

Exact source artifacts and registries remain the authority. A future
GitHub-facing Markdown page or HTML page would be a generated reader surface and
must cite the source inventory rather than replacing it.
