<!-- authority: control -->

# Publication Process Requirement Audit

## Requirement Coverage

| PRD requirement | Implementation evidence | Status |
| --- | --- | --- |
| Replace the prior active presentation process with a brand-new publication process. | `research_control/design/documentation_curator_publication_process.md`; `.agents/roles/research_ops/documentation-curator.v2.0.0.md` | Pass |
| Do not reuse old validator functionality or process files as active implementation. | Deleted old validator scripts; bootstrap now runs `scripts/validate_publication_process.py` and teaching QA only for docs validation. | Pass |
| Preserve source authority and generated-output boundaries. | `documentation_curator_publication_process.md`; both pilot HTML pages and GitHub Markdown pages state noncanonical generated-output status. | Pass |
| Add page-specific publication briefs. | `markdown/publication-briefs/project-overview.publication-brief.md`; `markdown/publication-briefs/source-authority.publication-brief.md`; `registries/PUBLICATION_BRIEF_REGISTRY.csv` | Pass |
| Revise the topic registry to track concepts and migration status rather than reader blocks. | `registries/EXPLAINER_TOPIC_REGISTRY.csv` now tracks document family, brief ID, migration status, source bundle, and output surfaces. | Pass |
| Update the Documentation Curator role. | v1.0.0 is superseded; v2.0.0 is active with publication-process validators. | Pass |
| Update HTML and visual explainer skill guidance. | `.codex/skills/html-visual-explainer/SKILL.md`; `.codex/skills/visual-explainer/SKILL.md` | Pass |
| Remove old active validation categories and add new publication validation. | `scripts/validate_publication_process.py`; `tests/test_publication_process_validation.py`; bootstrap integration | Pass |
| Build Project Overview and Source Authority pilots. | New source specs, GitHub Markdown, HTML, publication briefs, registry rows, and screenshots. | Pass |
| Run desktop and mobile screenshot QA. | Four PNG files under `research_control/tasks/RT-20260618-007/artifacts/screenshots/` | Pass |
| Create a before/after review artifact. | `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md` | Pass |
| Require explicit user approval before corpus-wide migration. | Publication process doc, topic registry deferred rows, validator approval gate, and pilot review all preserve the block. | Pass |
| Treat old task records as historical only. | Superseded marker on old design contract; v1.0.0 role superseded; v2.0.0 is active. | Pass |
| Avoid external runtime, NPX, CDN, or network-required HTML. | New validator checks no-runtime tokens; pilot HTML contains only inline CSS and no script/runtime imports. | Pass |

## Validator Coverage

The new validator checks:

- publication brief registry shape;
- topic registry migration state;
- migrated brief/spec/output consistency;
- no external runtime in tracked HTML;
- source material visibility in HTML and GitHub Markdown;
- noncanonical generated-output boundary text;
- retired structural fields in migrated source specs;
- duplicate migrated section skeletons;
- generic visual language;
- screenshot evidence; and
- explicit approval gate for corpus-wide migration.

## Boundary Statement

This transaction does not modify canonical science sources and does not
promote ontology, exact-GR benchmark, metric, coupling, Gate Chair, or
completed-derivation claims.
