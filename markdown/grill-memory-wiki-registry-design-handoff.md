# Grill Handoff: Memory, Wiki, Registry, And File-Format System

Date: 2026-06-07
Repository: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`
Purpose: continue an intense `grill-me` design session about the repository memory, wiki, registry, and file-format architecture.

## How To Resume

The grill session has resolved the first-pass scope through **Question 114**. Proceed to implementation unless the user asks to continue grilling. If a new design ambiguity appears during implementation, ask one question at a time. If a question can be answered by inspecting the repository or the reference project, inspect the codebase instead of asking the user.

Do not reopen accepted decisions unless a later decision creates a direct contradiction.

## Reference Basis

Use `/Volumes/P-SSD/AngryOwl/The Æther GR Derivation/` as a reference for prior wiki, registry, TeX-to-PDF, and validation patterns. Do not copy its `docs/`-centered filesystem directly into this reset repository.

This repository needs a different root-level structure, with format-specific lanes and skill-owned scripts.

## Accepted File-Format Authority

The user accepted the following hierarchy:

1. `.tex` is canonical for physics research and derivational claims.
2. CSV registries are canonical for routing, provenance, classification, generated-output tracking, and agent-queryable memory.
3. Markdown is canonical for GitHub documentation, AI-agent documentation, README/front-door material, and selected project-control documentation.
4. PDFs are generated human-reading artifacts from `.tex`; they are not independent scientific authority.

HTML was revised:

- HTML is **human-only**.
- HTML exists to visually explain project functionality, research-system functionality, and what the project is about.
- HTML must not be canonical for AI-agent documentation, research authority, control authority, or scientific claims.
- HTML may be generated with the `visual-explainer` skill.
- HTML should point back to its source basis through registry metadata.

## Accepted Tracking And Generation Rules

All durable project knowledge artifacts should be trackable by Git.

Tracked generated wiki outputs are acceptable, but they are generated-only:

- Humans and agents may read tracked wiki files.
- Edits happen in canonical source files and registries.
- Generated wiki notes should record source path, source hash, generation command, and generated timestamp.

`.local/` should be reserved for temporary staging, editor-specific vaults, caches, and rebuild scratch space.

## Accepted Root-Level Directory Contract

The user accepted this direction:

```text
ontology/
  tex/
  pdfs/

manuscripts/
  tex/
  pdfs/

markdown/

html/

registries/

wiki/
  markdown/
  tex/
  pdf/
  html/
  indexes/

.codex/skills/
  project-memory-system/
    SKILL.md
    scripts/
  markdown-wiki/
    SKILL.md
  tex-wiki/
    SKILL.md
  pdf-derivative-build/
    SKILL.md
  html-visual-explainer/
    SKILL.md
  ontology-promotion/
    SKILL.md
```

Important constraints:

- Preserve the existing `ontology/` folder and its current files.
- Do not remove ontology files.
- Do not create a root `docs/` directory for this new repository design.
- Python and Bash scripts should be associated with skills.
- Shared registry/wiki/PDF orchestration scripts should live under `.codex/skills/project-memory-system/scripts/`.

## Accepted Ontology Model

The ontology is canonical, but not frozen.

Current rule:

1. `ontology/` holds the current canonical ontology package.
2. `manuscripts/` holds research work, derivations, objections, candidate extensions, and proposed amendments.
3. A new ontology idea should first be developed in `manuscripts/tex/`.
4. If it passes the project gate, it may be promoted into `ontology/tex/`.
5. Its PDF is rebuilt into `ontology/pdfs/`.
6. Registries record the source manuscript, affected ontology file, status, and provenance.
7. Wiki notes regenerate from the updated source and registry state.

Accepted ontology promotion packet:

- Source research `.tex` file in `manuscripts/tex/`
- Generated PDF in `manuscripts/pdfs/`
- Markdown promotion note explaining the change in plain language
- Registry update linking source manuscript to affected ontology file
- Status field: `proposed`, `accepted`, `rejected`, or `superseded`
- Verification that the ontology update does not silently change established GR-benchmark claims
- Rebuilt ontology PDF after acceptance

## Accepted Registry Architecture

Use a layered registry model:

```text
registries/MARKDOWN_SOURCE_REGISTRY.csv
registries/TEX_SOURCE_REGISTRY.csv
registries/PDF_DERIVATIVE_REGISTRY.csv
registries/HTML_EXPLAINER_REGISTRY.csv
registries/FILE_OBJECT_REGISTRY.csv
```

Authority model:

- Format-specific registries contain the real judgment.
- `FILE_OBJECT_REGISTRY.csv` is a generated master query surface.
- The master registry should be generated from the format-specific registries, not hand-edited.

`PDF_DERIVATIVE_REGISTRY.csv` rule:

- It is only for project PDFs generated from registered `.tex` files.
- Each PDF row must point to its source `.tex`, source hash, build command, build status, and generated PDF path.
- Orphan project PDFs should fail validation.
- External reference PDFs, if needed later, should use a separate lane and registry, not `PDF_DERIVATIVE_REGISTRY.csv`.

## Accepted Common Metadata Schema

All registries should share a common core schema:

```csv
object_id,path,format,role,authority_status,audience,source_hash,related_source,generated_from,generated_outputs,owner_skill,validation_status,last_validated_at,notes
```

Format-specific fields may extend this schema.

Examples:

- TeX: `pdf_required`, `claim_status`, `research_status`, `ontology_promotion_status`
- PDF: `source_tex_path`, `source_tex_hash`, `build_command`, `build_status`
- Markdown: `github_facing`, `agent_documentation`, `contains_mermaid`, `contains_math`
- HTML: `human_visual_only`, `source_basis`, `visual_explainer_skill_version`

`object_id` values should be human-readable, stable, and format-prefixed.

Examples:

```text
MD-ONTOLOGY-AETHER-AND-AETHER-FLOW
TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY
PDF-ONTOLOGY-AETHER-FLOW-GEOMETRY
HTML-PROJECT-OVERVIEW
WIKI-TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY
```

## Accepted Markdown Math And Diagrams

Markdown should target GitHub-native rendering:

- Inline math: `$E = mc^2$`
- Display math:

```markdown
$$
G_{\mu\nu} = 8\pi T_{\mu\nu}
$$
```

Mermaid diagrams should be embedded directly in Markdown fences.

HTML may render formulas visually for humans, but HTML is not the source of mathematical authority.

## Accepted Initial Implementation Boundary

The first implementation pass should be infrastructure-only.

It should:

- preserve `ontology/` exactly as the current canonical ontology package
- create `manuscripts/tex/` and `manuscripts/pdfs/`
- create `markdown/`, `html/`, `registries/`, and `wiki/`
- create the accepted `.codex/skills/*` structure
- register existing ontology `.tex`, `.pdf`, and `.md` files
- generate wiki notes and indexes from those files
- validate source-to-derivative relationships

It should not:

- rewrite ontology claims
- alter equations
- rename existing ontology files
- promote new research content
- import the old repo's live research-control state

## Accepted Decisions After Question 21

Question 21: Generated wiki notes have their own registry entries in a generated-only `registries/WIKI_ARTIFACT_REGISTRY.csv`.

Question 22: Every format-specific registry uses the same common core columns in the same order, followed by format-specific extension columns.

Question 23: The accepted common core column order is:

```csv
object_id,path,format,role,authority_status,audience,source_hash,related_source,generated_from,generated_outputs,owner_skill,validation_status,last_validated_at,notes
```

Question 24: `object_id` remains stable across file renames.

Question 25: Registry validation fails on duplicate `object_id` values across all registries, not just within one CSV.

Question 26: `source_hash` uses SHA-256 over the file bytes exactly as stored.

Question 27: Generated artifacts store both the current source hash and their own artifact hash.

Question 28: `registries/TEX_SOURCE_REGISTRY.csv` appends:

```csv
pdf_required,pdf_object_id,pdf_path,claim_status,research_status,ontology_promotion_status,equation_scope
```

Question 29: `registries/PDF_DERIVATIVE_REGISTRY.csv` appends:

```csv
source_tex_object_id,source_tex_path,source_tex_hash,pdf_hash,build_command,build_status,built_at
```

Question 30: `PDF_DERIVATIVE_REGISTRY.csv` requires one row for every project PDF under `ontology/pdfs/` and `manuscripts/pdfs/`; unregistered project PDFs fail validation.

Question 31: External/reference PDFs are excluded from `PDF_DERIVATIVE_REGISTRY.csv` and may later use a separate `REFERENCE_SOURCE_REGISTRY.csv` if needed.

Question 32: `registries/MARKDOWN_SOURCE_REGISTRY.csv` appends:

```csv
github_facing,agent_documentation,contains_mermaid,contains_math
```

Question 33: Markdown files under `markdown/` are canonical authored Markdown sources; generated Markdown wiki notes live only under `wiki/markdown/` and are registered in `WIKI_ARTIFACT_REGISTRY.csv`.

Question 34: Root-level `README.md` and `AGENTS.md` are registered in `MARKDOWN_SOURCE_REGISTRY.csv`.

Question 35: `registries/HTML_EXPLAINER_REGISTRY.csv` appends:

```csv
human_visual_only,source_basis,source_basis_hash,html_hash,visual_explainer_skill_version
```

Question 36: Every tracked `.html` file under `html/` requires an `HTML_EXPLAINER_REGISTRY.csv` row; `.local/html_wikis/` remains untracked scratch output.

Question 37: The HTML registry fails validation if `human_visual_only` is not exactly `true` for every row.

Question 38: Generated `registries/WIKI_ARTIFACT_REGISTRY.csv` appends:

```csv
source_object_id,source_path,source_object_hash,wiki_hash,wiki_kind,generated_at
```

Question 39: `WIKI_ARTIFACT_REGISTRY.csv` is fully generated and never hand-edited.

Question 40: `FILE_OBJECT_REGISTRY.csv` is fully generated and never hand-edited.

Question 41: Generated registries use sidecar metadata files rather than CSV comments, including:

```text
registries/FILE_OBJECT_REGISTRY.meta.json
registries/WIKI_ARTIFACT_REGISTRY.meta.json
```

Question 42: Registry timestamps use UTC ISO 8601 with a `Z` suffix.

Question 43: Empty optional registry fields use empty CSV cells rather than sentinel strings such as `none`, `n/a`, or `null`.

Question 44: Boolean registry fields use lowercase `true` or `false` only.

Question 45: Path fields always use repository-relative POSIX paths, never absolute paths.

Question 46: Validators fail if a registry path points outside the repository or includes `..` traversal.

Question 47: Validators fail on tracked `.DS_Store` files inside canonical artifact lanes such as `ontology/`, `manuscripts/`, `markdown/`, `html/`, `registries/`, or `wiki/`.

Question 48: Validators operate on tracked and registered project files, while ignored untracked local noise such as `.DS_Store` can be cleaned by a separate hygiene command.

Question 49: The first implementation includes `.codex/skills/project-memory-system/scripts/clean_local_noise.py` to remove ignored local noise from canonical lanes.

Question 50: The initial validator distinguishes `ERROR` from `WARNING`; errors block validation success and warnings do not.

Question 51: Stale generated PDFs and wiki notes are `ERROR`, not `WARNING`.

Question 52: Missing generated wiki notes are an `ERROR` after the wiki system is enabled.

Question 53: The first implementation bootstraps wiki notes for all existing registered ontology `.tex`, ontology PDFs, root/front-door Markdown, and authored Markdown files.

Question 54: Generated wiki notes are metadata-only for the first implementation.

Question 55: Generated wiki notes do not include source excerpts in the first implementation.

Question 56: Every generated wiki note begins with an explicit non-authority banner.

Question 57: Wiki notes are grouped by source format under `wiki/markdown/`, `wiki/tex/`, `wiki/pdf/`, and `wiki/html/`.

Question 58: Each wiki note filename derives from lowercased, slugified `object_id`, not from the source file basename.

Question 59: Generated wiki notes include metadata backlinks to related objects such as source TeX to generated PDF and generated PDF back to source TeX.

Question 60: `wiki/indexes/` includes generated index pages by authority status, format, owner skill, and ontology promotion status.

Question 61: Initial wiki index pages are Markdown files, not HTML.

Question 62: Generated wiki notes and indexes are committed/tracked in Git.

Question 63: The first implementation creates placeholder `SKILL.md` files for all accepted skill lanes before every script is fully implemented.

Question 64: Shared registry, wiki, PDF, and validation orchestration lives under `.codex/skills/project-memory-system/scripts/`, with specialized skills delegating to those shared scripts.

Question 65: `markdown-wiki`, `tex-wiki`, `pdf-derivative-build`, `html-visual-explainer`, and `ontology-promotion` are workflow front doors that call shared scripts rather than owning duplicate implementations.

Question 66: The first implementation includes `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py` as a single operator-facing command to create directories, seed registries, generate wiki artifacts, and validate the result.

Question 67: The bootstrap script is idempotent.

Question 68: The bootstrap script refuses to overwrite existing hand-edited authored source registry rows unless run with an explicit update flag such as `--refresh-existing`.

Question 69: Generated registries and wiki notes are regenerated without requiring `--refresh-existing`.

Question 70: Existing ontology `.tex` files are classified as `authority_status=canonical` and `role=ontology_source`, with notes preserving the boundary that this does not prove the broader first-principles derivation is solved.

Question 71: Existing ontology PDFs are classified as generated derivatives with `authority_status=generated_noncanonical`.

Question 72: `ontology/aether-and-aether-flow.md` is classified as ontology-adjacent explanatory documentation.

Question 73: `markdown/grill-memory-wiki-registry-design-handoff.md` is registered as project-control Markdown.

Question 74: This grill session's accepted decisions are appended back into this handoff file as a decision log before implementation.

Question 75: Tracked HTML explainers are generated from registered source prompt/spec files rather than authored directly as standalone `.html`.

Question 76: HTML explainer source specs live under `markdown/html-explainer-specs/` and are registered in `MARKDOWN_SOURCE_REGISTRY.csv` with `role=html_explainer_source_spec`.

Question 77: `HTML_EXPLAINER_REGISTRY.csv` requires each row's `source_basis` to point to a registered Markdown source spec object ID, not just a free-text path.

Question 78: Hand-authored HTML is forbidden in tracked `html/` for the first implementation.

Question 79: Visual-explainer generation records the generating skill version when available, or otherwise a local skill directory hash such as `local-unversioned:<hash>`.

Question 80: The first `pdf-derivative-build` implementation uses `pdflatex` as the required default builder.

Question 81: The PDF builder runs `pdflatex` three times per TeX file.

Question 82: PDF builds happen in an isolated temporary build directory rather than next to the `.tex` source.

Question 83: Failed PDF builds preserve the temporary build directory path in error output for debugging.

Question 84: Successful PDF builds update `PDF_DERIVATIVE_REGISTRY.csv` automatically with `source_tex_hash`, `pdf_hash`, `build_command`, `build_status`, and `built_at`.

Question 85: The PDF builder refuses to build a `.tex` file unless it has a `TEX_SOURCE_REGISTRY.csv` row for managed project builds.

Question 86: The builder supports a `--scratch` mode for unregistered TeX that writes only under `.local/` and never updates registries.

Question 87: Ontology PDFs and manuscript PDFs use filename parity with their source TeX basenames.

Question 88: The validator fails if a registered PDF path does not match the source TeX basename and lane mapping.

Question 89: All existing ontology `.tex` files have `pdf_required=true` in the initial bootstrap.

Question 90: Manuscript `.tex` files default to `pdf_required=true` when added under `manuscripts/tex/`, unless explicitly marked as draft/control text that does not require a PDF.

Question 91: TeX rows include `equation_scope` values from a controlled vocabulary rather than free text.

Question 92: The first `equation_scope` vocabulary is:

```text
none
local_equations
derivation_sequence
gr_benchmark
control_only
```

Question 93: `claim_status` uses a controlled vocabulary.

Question 94: The first `claim_status` vocabulary is:

```text
benchmark_claim
open_derivation_claim
proposal
rejected
superseded
control_only
explanatory_only
```

Question 95: `research_status` uses a controlled vocabulary.

Question 96: The first `research_status` vocabulary is:

```text
canonical_ontology
active_manuscript
draft
paused
stopped_negative_result
rejected
superseded
project_control
```

Question 97: `ontology_promotion_status` uses only:

```text
proposed
accepted
rejected
superseded
not_applicable
```

Question 98: Current ontology `.tex` rows use `ontology_promotion_status=accepted`.

Question 99: Non-ontology TeX rows default to `ontology_promotion_status=not_applicable` unless explicitly part of a promotion packet.

Question 100: Ontology promotion packets are represented as Markdown notes first, then optionally TeX/manuscript artifacts if the promotion needs formal derivation.

Question 101: Ontology promotion notes live under `markdown/ontology-promotions/` and are registered in `MARKDOWN_SOURCE_REGISTRY.csv` with `role=ontology_promotion_note`.

Question 102: A promotion note is required before any manuscript content can be promoted into `ontology/tex/`.

Question 103: Ontology promotion requires a validator check that no established exact-GR benchmark claim was silently changed.

Question 104: The first implementation includes only the registry fields and placeholder skill boundary for ontology promotion, not a full promotion validator.

Question 105: `README.md` is updated in the first implementation to document the new memory/wiki/registry architecture.

Question 106: `AGENTS.md` is updated to instruct agents to use the registry/wiki system before making project-knowledge changes.

Question 107: Implementation starts after the first-pass scope is complete and this handoff is updated.

Question 108: The first implementation includes lightweight tests or smoke checks for the registry bootstrap and validator.

Question 109: The first implementation uses Python's standard-library `unittest` rather than adding `pytest`.

Question 110: The local verification command is:

```text
.venv/bin/python -m unittest discover -s tests
```

Question 111: CI integration is deferred until after the local memory/wiki/registry system works.

Question 112: The first implementation includes a final validation command:

```text
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Question 113: `bootstrap_memory_system.py` supports `--check` as an alias for `--validate-only`.

Question 114: The implementation checklist is appended to this handoff before code changes.

## Implementation Checklist

- [x] Create accepted root directories and skill folders without altering ontology source files.
- [x] Add minimal `SKILL.md` front doors for `project-memory-system`, `markdown-wiki`, `tex-wiki`, `pdf-derivative-build`, `html-visual-explainer`, and `ontology-promotion`.
- [x] Implement shared bootstrap, registry generation, wiki generation, PDF-build support, local-noise cleanup, and validation helpers under `.codex/skills/project-memory-system/scripts/`.
- [x] Seed authored source registries for current ontology TeX, current ontology-adjacent Markdown, root/front-door Markdown, and project-control Markdown.
- [x] Generate derivative registries, master `FILE_OBJECT_REGISTRY.csv`, sidecar `.meta.json` files, wiki notes, and wiki indexes.
- [x] Update `README.md` with the memory/wiki/registry architecture and commands.
- [x] Update `AGENTS.md` with authority hierarchy, generated-output boundaries, and validation requirements.
- [x] Add `unittest` smoke checks for bootstrap idempotence, validation failure modes, generated registry regeneration, and wiki-note coverage.
- [x] Run `.venv/bin/python -m unittest discover -s tests`.
- [x] Run `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only`.

## Post-Implementation State

Implemented first-pass memory/wiki/registry infrastructure.

Verification commands passed:

```text
.venv/bin/python -m unittest discover -s tests
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Known boundary: existing ontology PDFs were registered as current derivatives but not rebuilt during the first pass. The next substantive step is a registry review followed by an optional managed PDF rebuild.

## Pending Question To Ask Next

None for the first-pass implementation. Continue by executing the checklist.

## Discussion State

Current state: first-pass design scope accepted and implemented. This file records accepted decisions through Question 114, completed implementation status, and the next boundary: registry review plus optional managed PDF rebuild.

## Registry Review and Derivative Verification Follow-up

Date: 2026-06-08 UTC.

Role executed: Registry Review and Derivative Verification Officer.

Outcome:

- Reviewed the seeded `TEX_SOURCE_REGISTRY.csv`, `PDF_DERIVATIVE_REGISTRY.csv`, and `MARKDOWN_SOURCE_REGISTRY.csv` rows.
- Confirmed the eight ontology TeX rows remain correctly classified as canonical ontology benchmark sources with `claim_status=benchmark_claim`, `research_status=canonical_ontology`, `ontology_promotion_status=accepted`, and `equation_scope=gr_benchmark`.
- Corrected the stale older-repository authority statement at the top of `ontology/aether-and-aether-flow.md`; the Markdown note now points to this reset repo's registered TeX and registry authority model instead of the old `docs/` manifest.
- Added the missing local `tex_shared/` inputs required by the registered ontology TeX files, removing the hidden dependency on the predecessor repository for managed PDF rebuilds.
- Fixed the PDF builder/bootstrap contract so managed rebuilds stamp `built_at` in `PDF_DERIVATIVE_REGISTRY.csv`.
- Fixed authored-registry bootstrap behavior so normal bootstrap refreshes mechanical fields such as source hashes while preserving reviewed semantic judgments.
- Rebuilt all registered ontology PDFs through `.venv/bin/python .codex/skills/project-memory-system/scripts/build_pdf_derivatives.py`.
- Refreshed generated registries and wiki metadata after the rebuild.

Verification passed:

```zsh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Current PDF derivative status: all eight ontology PDFs are managed rebuilds with `build_status=built` and `built_at=2026-06-08T01:04:12Z`.

Next boundary: prepare a clean local checkpoint commit if desired. Do not push unless explicitly authorized.

Possible future improvement: add first-class dependency tracking for shared TeX support files, such as a support-source registry or dependency-hash fields, so a future edit to `tex_shared/` can be detected as a source-to-PDF freshness event before rebuild.
