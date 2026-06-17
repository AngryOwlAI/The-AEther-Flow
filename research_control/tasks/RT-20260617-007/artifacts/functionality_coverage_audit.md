# Functionality Coverage Audit

Task: `RT-20260617-007`

## Coverage Finding

The subject-first reset left the active explainer set coherent, but not yet
complete for the project functionality now visible in the control surfaces.
The existing ten explainers cover the public two-lane model, ontology,
research workflow, role routing, claim gates, source authority, roles and
skills, memory, validation governance, and technical requirements.

Three functional subsystems were still better treated as first-class subjects
rather than as short paragraphs inside other pages:

- GR derivation roadmap: milestone burden chain, Distance-to-GR ledger,
  selector routing, freeze criteria, source-extension category, and finite toy
  metric-response target.
- Project-system improvement: classifier, advisory resolver, signal
  registries, one bounded maintenance AgentJob, documentation impact,
  regeneration, and validation gates.
- Documentation Curator teaching loop: subject-first Curator authority,
  Student questions, Teacher answers, curated packets, source-spec
  distillation, GitHub-facing Markdown, HTML derivatives, and advisory format
  boundaries.

## Curator Decision

New explainers were required. Adding only short prose to the existing overview
would have left these subsystems easy to miss and would have mixed distinct
operational lanes into a single page. The overview, README, and context
glossary were updated to route to the new pages.

## Format Boundary

The source-spec and HTML format remains useful validation guidance. It does
not decide which project functionality deserves coverage. The Curator decision
was based on the repository's functionality and authority surfaces; the
renderer and lint scripts were then used to keep the resulting surfaces
source-backed, structurally consistent, and validator-compatible.

## Derivative Repair

During the coverage audit, the visible `All Source Materials` lists in the
existing HTML derivatives were found to have truncated source paths such as
`EADME.md`, `egistries/...`, and `codex/skills/...`. The source evidence in
the specs and registries was intact, but the human-facing HTML list was
misleading. The task repaired those source-list paths across the tracked HTML
derivatives and refreshed generated registry/wiki surfaces through bootstrap.

## Claim Boundary

No canonical ontology, benchmark source, science draft, role contract, skill
contract, schema, validator, or routing behavior was changed. The new pages
are explanatory, generated/noncanonical reader surfaces backed by registered
source specs and registries.
