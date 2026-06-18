<!-- authority: control -->

# Phase 2A GR Derivation Roadmap Before/After Review

## Scope

Task `RT-20260618-013` implements the Phase 2A packet from
`research_control/design/documentation_curator_corpus_migration_plan.md`:
`gr-derivation-roadmap-explainer`.

This packet migrates one public page family:

- publication brief: `markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md`
- source spec: `markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md`
- GitHub-facing Markdown: `github-facing/gr-derivation-roadmap-explainer.md`
- tracked HTML: `html/gr-derivation-roadmap-explainer.html`

The packet does not migrate Phase 2B or any corpus-wide page set.

## Before

Before Phase 2A, the project had Phase 1 public pages for benchmark boundary,
physics-program status, and ontology vocabulary. A reader could still see
active research-control language such as `Resp_lc`, `M_src`, `AtlasGlue_src^+`,
source extension, finite toy model, freeze criteria, and Gate Chair status
without a public roadmap explaining how those terms fit into the burden chain.

That gap created a risk that draft/control objects, validator pass state, or
generated public pages would be mistaken for physics evidence.

## After

Phase 2A adds a bounded decision/lifecycle guide that:

- presents the ordered milestone chain from source ontology to benchmark
  promotion;
- explains ledger statuses such as `not started`, `draft object exists`,
  `constructive witness exists`, `accepted`, `frozen negative`, and
  `human-gated`;
- names future physics AgentJob fields `target_derivation_milestone` and
  `milestone_burden`;
- explains `new_mathematical_payload` as an auditability rule rather than
  success proof;
- preserves `Resp_lc`, `M_src`, `AtlasGlue_src^+`, source-extension, finite
  toy, draft/control, source-only, local exact-branch, and human-gated
  qualifiers; and
- states that generated GitHub-facing Markdown and tracked HTML are
  noncanonical reader surfaces.

## Source Inspection

| Source | Inspection Result |
| --- | --- |
| `research_control/design/gr_derivation_burden_map.md` | Defines the milestone chain, future AgentJob fields, mathematical payload rule, constructive preference, source-extension category, finite toy target, and freeze criteria. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | Records current burden rows including accepted `Resp_lc`, draft object exists for `M_src`, not-started downstream metric/coupling/equation burdens, frozen negative finite toy route, and human-gated benchmark promotion. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | Active boundaries prohibit ontology edits, benchmark promotion, completed derivation language, generated-output authority, source-authority laundering, and global no-go inflation. |
| `registries/AGENT_JOB_REGISTRY.csv` | Shows that task outputs are bounded transactions with allowlists, completion paths, and validation receipts rather than standalone physics authority. |
| `research_control/README.md` | Explains the one-job rule, future physics milestone fields, Distance-to-GR ledger, memory preflight, and documentation-impact discipline. |
| `AGENTS.md` | Defines source authority hierarchy and generated-output boundaries. |

## Acceptance Review

| Criterion | Evidence | Status |
| --- | --- | --- |
| Explains the roadmap milestones. | Milestone ladder in GitHub Markdown and process timeline in HTML. | Pass |
| Explains status categories. | Status Terms section and status chips in HTML. | Pass |
| Names future AgentJob fields. | Future Physics Job Fields section in GitHub Markdown and Future Job Fields section in HTML. | Pass |
| Preserves current-frontier qualifiers. | Current Frontier Caution section in both surfaces. | Pass |
| Avoids validator-as-physics-evidence claims. | Burden And Evidence matrix and What Validators Cannot Prove section. | Pass |
| Avoids global no-go inflation. | Freeze Criteria section preserves scoped route-control meaning. | Pass |
| Avoids corpus-wide migration. | Only the `gr-derivation-roadmap-explainer` family is added. | Pass |

## Screenshot QA

| Page | Desktop artifact | Mobile artifact | Status |
| --- | --- | --- | --- |
| GR Derivation Roadmap | `research_control/tasks/RT-20260618-013/artifacts/screenshots/gr-derivation-roadmap-desktop.png` | `research_control/tasks/RT-20260618-013/artifacts/screenshots/gr-derivation-roadmap-mobile.png` | Pass after screenshots are captured |

## Remaining Risks

- The roadmap is volatile because current-frontier rows can change through
  future physics AgentJobs; readers must inspect the live ledger before making
  current-status summaries.
- The page explains scientific control state but does not replace direct
  inspection of the cited scientific artifacts.
- Bootstrap may continue to report `.local` or Obsidian freshness warnings.
  Those warnings concern derivative retrieval layers and do not alter source
  authority.

## Recommendation

Phase 2A is ready for checkpoint after publication-process strict validation,
bootstrap refresh, documentation-impact validation, research-control
validation, diff validation, screenshot QA, and checkpointing all pass.
