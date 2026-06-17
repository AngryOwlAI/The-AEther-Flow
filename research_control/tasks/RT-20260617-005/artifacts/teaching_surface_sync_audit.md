# Teaching Surface Sync Audit

## Scope

`RT-20260617-005` synchronized the explanatory documentation surfaces that
lagged the completed HTML teaching-loop system change from `RT-20260617-004`.

## Updated Surfaces

- `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- `markdown/html-explainer-specs/research-control-system-explainer.md`
- `html/roles-and-skills-explainer.html`
- `html/research-control-system-explainer.html`
- `github-facing/roles-and-skills-explainer.md`
- `github-facing/research-control-system-explainer.md`
- `github-facing/role-routing-explainer.md`

## Findings Resolved

- The roles-and-skills explainer cited older Documentation Curator role
  versions and omitted Documentation Student, Documentation Teacher,
  `TEACHING_QA_PACKET_SCHEMA`, and `aether-teaching-explainer`.
- The research-control-system explainer cited Documentation Curator v0.7.0 and
  did not describe teaching-loop validation or teaching-packet documentation
  impact.
- The role-routing GitHub-facing teaching page lacked the standard
  GitHub-facing reader sections and synchronized Mermaid blocks required by
  `research_control/design/github_facing_explainer_contract.md`.

## Boundaries Preserved

- No role contract changed.
- No schema contract changed.
- No validator changed.
- No routing behavior changed.
- No canonical science source changed.
- Generated HTML and GitHub-facing Markdown remain noncanonical derivatives.
- Teaching packets remain explanatory support only.
