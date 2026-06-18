<!-- authority: control -->

# Phase 1B Ontology Before/After Review

## Scope

Task `RT-20260618-012` implements the Phase 1B packet from
`research_control/design/documentation_curator_corpus_migration_plan.md`:
`aether-flow-ontology-explainer`.

This packet migrates one public page family:

- publication brief: `markdown/publication-briefs/aether-flow-ontology.publication-brief.md`
- source spec: `markdown/html-explainer-specs/aether-flow-ontology-explainer.md`
- GitHub-facing Markdown: `github-facing/aether-flow-ontology-explainer.md`
- tracked HTML: `html/aether-flow-ontology-explainer.html`

The packet does not migrate Phase 2 pages or any corpus-wide page set.

## Before

Before Phase 1B, the public physics-status migration had Phase 1A coverage for
the exact-GR benchmark boundary and the AEther-Flow physics program. The
ontology vocabulary remained available only through source files and generated
metadata surfaces. A new reader could still confuse ontology vocabulary with a
completed GR derivation, overread AEther-flow as an older three-dimensional
fluid, or miss the live `ontology/` versus archival `legacy_ontology/`
boundary.

## After

Phase 1B adds a bounded concept explainer that:

- maps AEther, AEther-flow, observed three-dimensional space, S-time, and
  observed expansion with caution labels;
- separates ontology model, mathematical derivation burden, and empirical
  prediction;
- distinguishes live `ontology/` sources from archival `legacy_ontology/`;
- names the observer normal/readout source construction as open work;
- identifies generated GitHub-facing Markdown and tracked HTML as
  noncanonical reader surfaces; and
- binds the public page to visible source paths and the publication brief
  registry.

## Source Inspection

| Source | Inspection Result |
| --- | --- |
| `ontology/aether-and-aether-flow.md` | Current front-facing ontology vocabulary; explicitly says the ontology is not a completed first-principles substrate derivation. |
| `ontology/aether_flow_interpretation-lemen.md` | Authored interpretive source contrasting the modern four-dimensional substrate account with older static three-dimensional aether theories. |
| `ontology/README.md` | Defines `ontology/` as the live mutable ontology lane and registered TeX as scientific authority. |
| `registries/TEX_SOURCE_REGISTRY.csv` | Current ontology TeX rows are canonical, with notes preserving that the broader first-principles GR derivation is not solved. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | Active boundaries prohibit ontology promotion, benchmark promotion, completed-derivation claims, and generated-output authority. |
| `AGENTS.md` | Defines the repository authority hierarchy and generated-output boundaries. |

## Acceptance Review

| Criterion | Evidence | Status |
| --- | --- | --- |
| Explains ontology vocabulary. | Vocabulary map in GitHub Markdown and concept map in HTML. | Pass |
| Avoids older three-dimensional aether inflation. | Edge-case warnings reject wind/fluid readings in observed space. | Pass |
| Separates model, mathematics, and prediction. | Dedicated model/mathematics/prediction section in both surfaces. | Pass |
| Preserves open derivation burden. | Names observer normal/readout source construction as open work. | Pass |
| Preserves source authority. | Source Materials sections cite live source paths and noncanonical status. | Pass |
| Avoids generated-output authority. | Both public surfaces state generated noncanonical status. | Pass |
| Avoids corpus-wide migration. | Only the `aether-flow-ontology-explainer` family is added. | Pass |

## Screenshot QA

| Page | Desktop artifact | Mobile artifact | Status |
| --- | --- | --- | --- |
| AEther-Flow Ontology | `research_control/tasks/RT-20260618-012/artifacts/screenshots/aether-flow-ontology-desktop.png` | `research_control/tasks/RT-20260618-012/artifacts/screenshots/aether-flow-ontology-mobile.png` | Pass |

## Remaining Risks

- The ontology source language remains inherently interpretive; readers may
  still over-literalize metaphors if they skip the edge-case section.
- The page summarizes the registered TeX authority boundary but does not
  replace direct TeX inspection for scientific claims.
- Bootstrap may continue to report `.local` or Obsidian freshness warnings.
  Those warnings concern derivative retrieval layers and do not alter source
  authority.

## Recommendation

Phase 1B is ready for checkpoint after publication-process strict validation,
bootstrap refresh, documentation-impact validation, research-control
validation, diff validation, and checkpointing all pass.
