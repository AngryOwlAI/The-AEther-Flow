<!-- authority: control -->

# Phase 1A Public Physics Status Before/After Review

## Scope

Task `RT-20260618-011` implements the Phase 1A packet from
`research_control/design/documentation_curator_corpus_migration_plan.md`.
The packet migrates two public pages:

- `exact-gr-benchmark-boundary-explainer`
- `aether-flow-physics-program-explainer`

The Phase 1B ontology page is intentionally not part of this packet.

## Before

Before this packet, the reviewed publication-process corpus contained only the
Phase 0 pilot pages:

- `project-overview-explainer`
- `source-authority-explainer`

Those pages established the public quality bar and authority model, but they
did not directly address the highest physics-status ambiguity: readers could
still confuse exact-GR benchmark adoption with a completed first-principles
substrate derivation or benchmark promotion.

## After

### Exact-GR Benchmark Boundary

The new benchmark-boundary page gives readers a compact comparison between
adoption, compatibility, derivation, and promotion. It states the conservative
benchmark boundary as ordinary GR at observable scale: one operative metric,
universal matter coupling, ordinary causal structure, and no empirical
deviation claim. It then binds benchmark authority back to:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/design/gr_derivation_burden_map.md`

The page is forbidden to prove completed derivation, benchmark promotion, Gate
Chair approval, generated-output authority, or global ontology rejection.

### AEther-Flow Physics Program

The new physics-program page frames the physics track as a research program:
ontology supplies the conceptual frame, exact GR supplies the conservative
benchmark, derivation remains an open source-side burden, negative results are
preserved, and claim promotion remains gated. It preserves qualifiers such as
`draft/control`, `source-only`, `local`, `exact-branch`,
`source-extension data`, and `human-gated`.

The page is bound to:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `research_control/README.md`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

## Screenshot QA

Screenshots were captured with Playwright through a temporary loopback server
because the Playwright wrapper blocks direct `file:` URLs. The temporary
server was stopped after capture. The committed HTML files remain single-file
documents with no external runtime, remote script, remote font, analytics,
localhost dependency, or browser-side Mermaid execution.

The Playwright console reported only the temporary server's missing
`favicon.ico` request. That 404 is not a page dependency and is not present in
the HTML source.

| Page | Desktop Evidence | Mobile Evidence | Result |
| --- | --- | --- | --- |
| Exact-GR Benchmark Boundary | `research_control/tasks/RT-20260618-011/artifacts/screenshots/exact-gr-benchmark-boundary-desktop.png` | `research_control/tasks/RT-20260618-011/artifacts/screenshots/exact-gr-benchmark-boundary-mobile.png` | Pass |
| AEther-Flow Physics Program | `research_control/tasks/RT-20260618-011/artifacts/screenshots/aether-flow-physics-program-desktop.png` | `research_control/tasks/RT-20260618-011/artifacts/screenshots/aether-flow-physics-program-mobile.png` | Pass |

Observed correction: the first desktop capture of
`exact-gr-benchmark-boundary-explainer.html` exposed clipped long source paths
inside compact ladder cards. The HTML CSS was updated to wrap inline code
paths, then all screenshots were recaptured.

## Acceptance Review

| Requirement | Evidence | Status |
| --- | --- | --- |
| No completed derivation claim. | Both pages state first-principles derivation remains open. | Pass |
| No generated-page benchmark certification. | Both pages state generated GitHub Markdown and HTML are noncanonical reader surfaces. | Pass |
| Exact-GR benchmark remains conservative and source-backed. | Benchmark language is tied to `README.md`, `registries/TEX_SOURCE_REGISTRY.csv`, and `research_control/design/gr_derivation_burden_map.md`. | Pass |
| Source-side work remains separate from claim promotion. | The physics-program page separates draft/control work, negative results, gates, and public summaries. | Pass |
| Phase 1B not migrated. | No `aether-flow-ontology-explainer` brief, source spec, GitHub page, or HTML page was created. | Pass |
| No external runtime. | HTML uses local CSS only and no script tags or remote assets. | Pass |

## Review Verdict

Phase 1A status: pass after CSS path-wrapping correction.

The two new public pages reduce public overclaim risk without changing
canonical ontology, benchmark status, Gate Chair authority, physics derivation
status, validator authority, or generated-output authority.

## Logical Next Step

After checkpoint, the next bounded migration candidate is Phase 1B:
`aether-flow-ontology-explainer`. It should remain a separate packet with its
own source-specific brief, source spec, GitHub Markdown, HTML, screenshots,
and review evidence.

