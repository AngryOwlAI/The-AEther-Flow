# Proof-State Dashboard Publication Review

## Scope

This review covers v17 P9-T02 only: generated GitHub Markdown and standalone
HTML dashboard hardening, generated-output registration, and screenshot QA.

## Source Basis

- `markdown/publication-briefs/proof-state-dashboard.publication-brief.md`
- `markdown/html-explainer-specs/proof-state-dashboard-explainer.spec.md`
- `github-facing/proof-state-dashboard-explainer.md`
- `html/proof-state-dashboard-explainer.html`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`

## Review Findings

| Criterion | Result | Evidence |
| --- | --- | --- |
| Dashboard derives from registered sources. | PASS | The GitHub Markdown and HTML both name the publication brief, source spec, and tracked source materials. |
| Dashboard says GR is not derived. | PASS | Both surfaces state that GR has not been derived and that generated surfaces cannot derive it. |
| Dashboard uses calibrated positive-first status cards. | PASS | Both surfaces include `At A Glance` positive-status cards plus the required status table. |
| Generated surfaces are registered. | PASS | Publication brief, HTML explainer, and Markdown source registries contain dashboard rows. |
| Reader scope precedes authority footer. | PASS | GitHub Markdown and HTML use the publication-process reader-scope/authority-footer controls. |
| Screenshot QA evidence exists. | PASS | Desktop screenshot: `research_control/tasks/RT-20260706-022/artifacts/screenshots/proof-state-dashboard-desktop.png`; mobile screenshot: `research_control/tasks/RT-20260706-022/artifacts/screenshots/proof-state-dashboard-mobile.png`. |

## Screenshot QA

- Desktop viewport: `1440 x 1100`, full-page screenshot captured at `1440 x
  3180`.
- Mobile viewport: `390 x 844`, full-page screenshot captured at `390 x 4655`.
- Result: header, warning boundary, status cards, dashboard table, source
  materials, reader scope, and authority footer render. The dashboard table is
  intentionally horizontally scrollable on mobile because it preserves the
  required six-column status matrix.

## Claim Boundary

The dashboard is a generated noncanonical reader surface. It does not create
proof authority, adopt a source law, adopt `MetricData(E)`, expand `g_eff`,
derive matter coupling, construct stress-energy semantics, import matter
action, derive Einstein equations, promote benchmark status, issue a Gate
Chair verdict, complete the derivation, or make generated output scientific
authority.

## Publication Status

The proof-state dashboard is marked as `publication_pilot`. Corpus-wide
publication migration remains approval-gated by the publication process.
