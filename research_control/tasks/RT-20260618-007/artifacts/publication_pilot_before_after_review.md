<!-- authority: control -->

# Publication Pilot Before/After Review

## Scope

Task `RT-20260618-007` rebuilt the Project Overview and Source Authority
public explainers as the pilot set for the Documentation Curator Publication
Process. The review covers:

- `markdown/html-explainer-specs/project-overview-explainer.md`
- `github-facing/project-overview-explainer.md`
- `html/project-overview-explainer.html`
- `markdown/html-explainer-specs/source-authority-explainer.md`
- `github-facing/source-authority-explainer.md`
- `html/source-authority-explainer.html`

## Before

The previous active implementation used a universal section and validator
contract. The PRD required that this active process be removed rather than
reused. The old process left these implementation risks:

- page quality depended on repeated structural fields rather than a
  page-specific reader brief;
- topic tracking mixed concept inventory with reader block enforcement;
- GitHub Markdown parity could become structural sameness instead of
  source-and-claim consistency;
- active validators encoded the old page model; and
- pilot evidence did not include publication-specific screenshot review.

## After

The new pilot uses page-local publication briefs, native GitHub-facing
Markdown, and standalone HTML with visible source grounding. The two pages no
longer depend on a universal heading skeleton or page-block registry.

Project Overview now functions as a compact front door:

- it names the project missions without promoting physics claims;
- it gives a first reading path through source, authority, workflow, and
  publication materials; and
- it preserves generated-output boundaries in both HTML and Markdown.

Source Authority now functions as a boundary map:

- it presents the authority ladder from registered TeX through generated
  derivatives and local retrieval;
- it explains safe use of generated pages; and
- it states failure modes where derivatives must lose to registered sources.

## Screenshot QA

Screenshots were captured with Playwright through a temporary localhost server
because the Playwright wrapper blocks direct `file:` URLs. The temporary
server was stopped after capture. The committed HTML remains standalone and
does not depend on localhost or network runtime.

- Desktop Project Overview:
  `research_control/tasks/RT-20260618-007/artifacts/screenshots/project-overview-desktop.png`
- Mobile Project Overview:
  `research_control/tasks/RT-20260618-007/artifacts/screenshots/project-overview-mobile.png`
- Desktop Source Authority:
  `research_control/tasks/RT-20260618-007/artifacts/screenshots/source-authority-desktop.png`
- Mobile Source Authority:
  `research_control/tasks/RT-20260618-007/artifacts/screenshots/source-authority-mobile.png`

Observed correction: the first Project Overview mobile capture exposed a
long source-path chip overflow. The HTML source-chip CSS was updated to wrap
within the container, and the screenshots were recaptured. The final mobile
Project Overview screenshot is 390 pixels wide, matching the target viewport.

## Review Verdict

Pilot status: pass.

Reasoning:

- Each page has a publication brief and a matching registry row.
- GitHub Markdown reads as native Markdown rather than a generated HTML
  transcript.
- HTML is no-network, source-grounded, and visually distinct per page.
- Source authority and generated-derivative boundaries remain explicit.
- The pilot does not authorize corpus-wide migration.

## Remaining Gate

Corpus-wide migration remains blocked until explicit user approval after this
pilot review.
