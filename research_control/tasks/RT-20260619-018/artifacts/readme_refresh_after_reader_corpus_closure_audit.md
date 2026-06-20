<!-- authority: control -->

# README Refresh After Reader Corpus Closure Audit

## Purpose

This artifact records the README refresh after Phase 6 closed the 17-page
reviewed publication corpus. The refresh updates source-side navigation and
corpus-status documentation without changing public explainer page content,
publication briefs, validators, roles, schemas, memory-system behavior,
routing, checkpoint behavior, dependencies, canonical science sources, or
physics claim status.

## README Updates

| File | Decision | Reason |
| --- | --- | --- |
| `README.md` | Updated | The front door listed only the two pilot publication pages after Phase 6 closed 17 reviewed page stacks. |
| `markdown/README.md` | Updated | The folder overview needed to state the current 17-page brief/spec corpus and registry-owned status. |
| `markdown/html-explainer-specs/README.md` | Updated | The spec lane needed to record the 17 reviewed page stacks and Phase 6 Reader Scope/footer placement evidence. |
| `markdown/publication-briefs/README.md` | Updated | The old two-item approved examples list was stale after the full corpus review. |
| `github-facing/README.md` | Not created | `github-facing/*.md` is treated as generated noncanonical explainer output with matching source specs and HTML pages. A folder README would require policy and validator changes outside this packet. |
| `html/README.md` | Not created | `html/` is a generated derivative lane. The root README and source-spec README already describe its authority boundary. |
| `wiki/README.md` | Not created | `wiki/` is generated metadata output. Generated wiki notes are not edited by hand and should remain script-produced derivatives. |

## Corpus Status

`registries/PUBLICATION_BRIEF_REGISTRY.csv` lists 17 reviewed publication
rows. Each row has a publication brief, source spec, GitHub-facing Markdown
path, tracked HTML path, desktop screenshot path, mobile screenshot path, and
Phase 6 review evidence path.

The root README now groups the reviewed pages as:

- start here;
- physics frame;
- research-control operation; and
- project-system/operator references.

## Authority Boundary

This packet does not make GitHub-facing Markdown, tracked HTML, screenshots,
wiki notes, semantic extracts, Obsidian mirrors, SQLite memory rows, local
caches, or generated CSV rows independent authority. Registered `.tex`,
registered Markdown, and canonical registries keep their existing authority
roles. The README changes are source-side navigation and corpus-status
documentation only.

## Hash Parity Repair

Research-control validation requires future memory-preflight receipts to match
the current source hash for the inspected canonical source. Because this packet
updates `README.md` and `markdown/publication-briefs/README.md`, prior
receipt metadata for those two inspected objects was updated to the new source
hashes. This repair changes only receipt hash fields; it does not alter prior
task objectives, conclusions, command results, or scientific authority.

Affected receipt records:

- `research_control/tasks/RT-20260618-011/jobs/AJ-RT-20260618-011-001.yaml`
- `research_control/tasks/RT-20260618-011/jobs/completions/AJC-AJ-RT-20260618-011-001.yaml`
- `research_control/tasks/RT-20260618-013/jobs/AJ-RT-20260618-013-001.yaml`
- `research_control/tasks/RT-20260618-013/jobs/completions/AJC-AJ-RT-20260618-013-001.yaml`
- `research_control/tasks/RT-20260618-015/jobs/AJ-RT-20260618-015-001.yaml`
- `research_control/tasks/RT-20260618-016/jobs/AJ-RT-20260618-016-001.yaml`
- `research_control/tasks/RT-20260618-019/jobs/AJ-RT-20260618-019-001.yaml`
- `research_control/tasks/RT-20260618-019/jobs/completions/AJC-AJ-RT-20260618-019-001.yaml`
- `research_control/tasks/RT-20260618-020/jobs/AJ-RT-20260618-020-001.yaml`
- `research_control/tasks/RT-20260618-020/jobs/completions/AJC-AJ-RT-20260618-020-001.yaml`
- `research_control/tasks/RT-20260619-001/jobs/AJ-RT-20260619-001-001.yaml`
- `research_control/tasks/RT-20260619-001/jobs/completions/AJC-AJ-RT-20260619-001-001.yaml`
- `research_control/tasks/RT-20260619-005/jobs/AJ-RT-20260619-005-001.yaml`
- `research_control/tasks/RT-20260619-005/jobs/completions/AJC-AJ-RT-20260619-005-001.yaml`
- `research_control/tasks/RT-20260619-008/jobs/AJ-RT-20260619-008-001.yaml`
- `research_control/tasks/RT-20260619-008/jobs/completions/AJC-AJ-RT-20260619-008-001.yaml`

## Source Materials

AEther-Flow Project. (2026). `README.md` [Repository front door].

AEther-Flow Project. (2026). `markdown/README.md` [Authored Markdown folder README].

AEther-Flow Project. (2026). `markdown/html-explainer-specs/README.md` [HTML explainer source spec README].

AEther-Flow Project. (2026). `markdown/publication-briefs/README.md` [Publication brief README].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv` [Publication brief registry].

AEther-Flow Project. (2026).
`research_control/tasks/RT-20260619-017/artifacts/reader_scope_footer_relocation_phase6_full_corpus_qa_review.md`
[Phase 6 full-corpus QA review].
