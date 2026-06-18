<!-- authority: control -->

# Retired Explainer Process Removal Audit

## Requirement Coverage

| Requirement | Evidence | Status |
| --- | --- | --- |
| Make `PUBLICATION_BRIEF_REGISTRY.csv` the sole active public-page control surface. | `scripts/validate_publication_process.py` reads `registries/PUBLICATION_BRIEF_REGISTRY.csv` only and rejects `registries/EXPLAINER_TOPIC_REGISTRY.csv` if it exists. | Pass |
| Delete the retired topic registry. | `registries/EXPLAINER_TOPIC_REGISTRY.csv` is deleted. | Pass |
| Keep only Project Overview and Source Authority public explainer triplets. | Only `project-overview-explainer` and `source-authority-explainer` remain under `markdown/html-explainer-specs/`, `github-facing/`, and `html/`. | Pass |
| Remove teaching-loop process assets. | Deleted `markdown/teaching-packets/`, Student and Teacher role contracts, `TEACHING_QA_PACKET_SCHEMA.md`, `scripts/validate_teaching_qa.py`, `tests/test_validate_teaching_qa.py`, and `.codex/skills/aether-teaching-explainer/`. | Pass |
| Remove active teaching-QA and old explainer validators. | Bootstrap docs validation now runs only `scripts/validate_publication_process.py`; `documentation-curator@2.0.0` default validators no longer include teaching-QA or old explainer validators. | Pass |
| Remove orphan public explainer outputs. | `validate_no_orphan_public_surfaces` fails any `*-explainer` spec, GitHub Markdown, or HTML page not listed in the publication brief registry. | Pass |
| Preserve publication validator protections. | The validator still checks source-basis parity, authority-boundary language, no-network HTML, screenshot/review evidence, duplicate skeletons, generic retired vocabulary, forbidden old headings, and the approval gate. | Pass |
| Update public navigation and front-door docs. | `README.md`, `markdown/README.md`, and `markdown/html-explainer-specs/README.md` now point to the reviewed pilot pages and publication-brief process only. | Pass |
| Regenerate derived registries/wiki through bootstrap. | Bootstrap now prunes missing-path Markdown rows and stale generated wiki, semantic, and Obsidian files before validation. | Pass |
| Add tests for retired process rejection. | `tests/test_publication_process_validation.py`, `tests/test_memory_system.py`, and `tests/test_documentation_surface_audit.py` cover retired registry rejection, orphan output rejection, publication-only docs validation, active Curator validator hygiene, stale generated-file pruning, and removal of workflow-step inspector audit behavior. | Pass |

## Historical Boundary

Historical `research_control/tasks/**` records remain untouched except for the
new `RT-20260618-008` transaction. Superseded Documentation Curator role
contracts remain only because completed AgentJobs outside the task folders
still reference their registered role versions. They are not active: the sole
active Documentation Curator role is `2.0.0`, and its validators are
publication-brief based.

## Remaining Public Explainer Corpus

- `markdown/html-explainer-specs/project-overview-explainer.md`
- `markdown/html-explainer-specs/source-authority-explainer.md`
- `github-facing/project-overview-explainer.md`
- `github-facing/source-authority-explainer.md`
- `html/project-overview-explainer.html`
- `html/source-authority-explainer.html`

## Boundary Statement

This removal is project-system cleanup only. It does not modify canonical
science sources and does not promote ontology, metric, coupling, exact-GR,
Gate Chair, or completed-derivation claims.
