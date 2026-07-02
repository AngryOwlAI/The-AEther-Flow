---
authority: control
task_id: "RT-20260702-006"
job_id: "AJ-RT-20260702-006-001"
receipt_id: "P5-T04-PUBLIC-STATUS-REGENERATION-RECEIPT"
status: "completed"
created_at: "2026-07-02T02:10:00Z"
physics_claim_authority: false
---

# P5-T04 Public Status Regeneration Receipt

## Objective

Regenerate affected tracked HTML derivatives from the P5-T03 Markdown source
spec basis and preserve public status boundaries without changing Markdown
source specs, GitHub-facing Markdown, README, publication briefs, ontology,
ledger status, source-law status, matter-coupling status, Einstein-equation
status, benchmark status, or completed-derivation status.

## Regenerated Derivatives

The task-local renderer
`research_control/tasks/RT-20260702-006/artifacts/regenerate_p5_t04_public_status_html.py`
performed exact-match derivative replacements and wrote
`research_control/tasks/RT-20260702-006/artifacts/p5_t04_regeneration_report.json`.
The report records before/after hashes and verifies the source-basis metadata
against the P5-T03 source-spec hashes.

Affected HTML derivatives:

- `html/project-overview-explainer.html`
- `html/aether-flow-physics-program-explainer.html`
- `html/exact-gr-benchmark-boundary-explainer.html`
- `html/gr-derivation-roadmap-explainer.html`
- `html/claim-gates-explainer.html`
- `html/source-authority-explainer.html`
- `html/validator-operator-workflow-explainer.html`

## Public Status Content Added Or Refreshed

- Each affected HTML derivative now visibly names
  `research_control/design/public_status_table_source_spec.md` where the
  P5-T03 source spec requires public status grounding.
- The project overview, physics program, exact-GR boundary, claim-gates,
  source-authority, and validator/operator pages now expose the public status
  source path and blocked-overread language in reader-facing content.
- The GR derivation roadmap no longer says `g_eff`, matter coupling, and
  Einstein equations are all "not started"; it now distinguishes scoped
  source-extension `g_eff`, scoped matter-coupling evidence/preconditions, and
  not-started Einstein equations.
- The GR derivation roadmap Reader Scope and footer now use the source-spec
  wording: the page cannot expand scoped `M_src` or scoped `g_eff` status,
  derive matter coupling, derive Einstein equations, promote a benchmark, or
  issue a Gate Chair verdict.

## Derivative Boundary

This packet regenerates generated public derivatives only. It does not make
HTML authoritative and does not alter the P5-T03 Markdown source specs. The
GitHub-facing Markdown derivatives were inspected as already updated by
P5-T02 and were not changed in this packet.

## Screenshot QA

The first direct `file:` screenshot attempt was discarded because the browser
wrapper blocked `file:` navigation and produced blank screenshots. The final
QA pass served the repository over `http://127.0.0.1:8765/`, overwrote the
blank files, and captured desktop plus mobile full-page screenshots for all
seven affected HTML derivatives under:

`research_control/tasks/RT-20260702-006/artifacts/screenshots/`

Representative visual check:

- `project-overview-explainer-desktop.png`: nonblank desktop page with the
  new Public Status Boundary section and source path visible.
- `gr-derivation-roadmap-explainer-mobile.png`: nonblank mobile page with
  scoped `M_src`, scoped `g_eff`, preconditions-only matter coupling, and
  public status source material visible.

## Acceptance Review

- Generated derivatives match the P5-T03 canonical Markdown source specs on
  source basis, authority boundary, and core public status claims.
- Public brief registry consistency is preserved; no publication brief was
  changed.
- No HTML derivative is treated as independent authority.
- No source-law, matter-coupling, Einstein-equation, benchmark-promotion, or
  completed-derivation claim is promoted.
- P5-T05 remains required for the next bounded public status claim-language
  validation packet.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 2). *Handoff 0458*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 2). *Public status table source
spec* [Internal control source spec].
