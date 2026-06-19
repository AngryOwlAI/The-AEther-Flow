<!-- authority: explanatory -->

# Phase 0 Post-Migration Page Audit

## Scope

This artifact executes Phase 0 of
`research_control/design/documentation_curator_post_migration_quality_plan.md`.
It audits the 17 reviewed publication surfaces listed in
`registries/PUBLICATION_BRIEF_REGISTRY.csv`.

No publication brief, source spec, GitHub-facing Markdown page, tracked HTML
page, contract, validator, role contract, schema, routing rule, checkpoint
gate, ontology source, science source, or physics claim was edited in this
packet.

## Method

The audit inspected, for each reviewed publication row:

- publication brief path;
- source spec path;
- GitHub-facing Markdown output;
- tracked HTML output;
- registry source-material list;
- current Markdown opening text and top authority paragraph;
- current Source Binding position;
- current HTML warning/footer placement;
- current visual strategy; and
- diagram decision for later implementation.

The source-material lists in the publication registry, publication brief
frontmatter, and source-spec frontmatter match for all 17 pages. No listed
source-material path is missing. The audited GitHub-facing Markdown and source
spec files contain no Mermaid blocks. The audited tracked HTML files contain no
inline SVG diagrams or Mermaid-rendered diagram payloads.

## Corpus-Level Findings

| Finding | Result |
| --- | --- |
| Reviewed publication rows audited | 17 |
| Registry/brief/spec source-material list mismatches | 0 |
| Missing listed source-material paths | 0 |
| GitHub-facing pages with noncanonical paragraph in the opening block | 17 |
| GitHub-facing openings meeting the future 120-220 word target | 0 |
| Current GitHub-facing opening range | 61-95 words |
| GitHub-facing Mermaid blocks | 0 |
| Source-spec Mermaid blocks | 0 |
| Tracked HTML pages with proposed `authority_footer` hook | 0 |
| Tracked HTML pages with a top/header authority notice | 13 |
| Tracked HTML pages with any `<footer>` element | 10 |
| Tracked HTML pages whose footer carries authority language | 6 |
| Tracked HTML inline SVG diagrams | 0 |

## Validator Observation

After `sync_obsidian_vault.py` refreshed the local vault and memory index,
`scripts/project_control/audit_documentation_surfaces.py` still fails on the
public GitHub-facing corpus. The remaining errors are contract drift, not
missing files:

- all 17 GitHub-facing pages are reported as missing machine-detectable
  `generated_noncanonical` authority status;
- `github-facing/aether-flow-ontology-explainer.md` is also reported as
  missing source-material markers for six source paths from its source spec;
- the script emits additional warnings for old recommended sections and
  External AI Navigation Card markers that the current brief-first publication
  process no longer uses as a universal skeleton.

This Phase 0 packet records the finding but does not repair it. Repair would
require Phase 1 contract/validator work or public-page rewrites, both outside
this audit-only scope.

Conclusion: every page needs footer-placement work in a later implementation
phase. Every page also needs opening expansion if the future 120-220 word
standard is adopted. Diagram work should be deliberate and page-specific; the
current corpus is table/layout-based rather than Mermaid/SVG-based.

## Page Matrix

| Page | Phase | Current visual | Markdown opening words | Current placement finding | Diagram decision |
| --- | --- | --- | ---: | --- | --- |
| `project-overview` | Phase 5 | source matrix | 95 | Top noncanonical paragraph; Source Binding near final third; HTML source note in source section; no footer hook. | Optional compact atlas map only if it becomes a real navigation aid rather than a generic validation flow. |
| `source-authority` | Phase 5 | source matrix | 61 | Top noncanonical paragraph; Source Binding near final third; HTML source note in source section; no footer hook. | Add authority-ladder or source-to-derivative boundary diagram. |
| `aether-flow-physics-program` | Phase 2 | layered architecture | 80 | Top generated-noncanonical paragraph; HTML warning appears before main content; footer exists without the proposed hook. | Add layered status architecture. |
| `exact-gr-benchmark-boundary` | Phase 2 | source matrix | 89 | Top generated-noncanonical paragraph; HTML warning appears before main content; footer exists without the proposed hook. | Add adoption-versus-derivation boundary diagram. |
| `aether-flow-ontology` | Phase 2 | layered architecture | 83 | Top generated-noncanonical paragraph; HTML warning appears near top; footer exists without the proposed hook. | Add layered ontology/source/claim-boundary diagram. |
| `gr-derivation-roadmap` | Phase 2 | process timeline | 87 | Top generated-noncanonical paragraph; HTML warning appears near top; footer exists without the proposed hook. | Add milestone/burden timeline. |
| `claim-gates` | Phase 2 | state model | 77 | Top generated-noncanonical paragraph; HTML warning appears near top; footer exists without the proposed hook. | Add claim-state model. |
| `research-agent-workflow` | Phase 3 | process timeline | 74 | Top generated-noncanonical paragraph; HTML warning appears near top; footer exists without the proposed hook. | Add process-lane diagram. |
| `director-agentjob-lifecycle` | Phase 3 | state model | 78 | Top generated-noncanonical paragraph; HTML warning appears near top; footer exists without the proposed hook. | Add lifecycle state diagram. |
| `parent-child-synthesis` | Phase 3 | state model | 82 | Top generated-noncanonical paragraph; HTML eyebrow/notice carries authority status near top; no footer element. | Add two-lane parent/child/fusion diagram. |
| `role-routing` | Phase 3 | role matrix | 72 | Top generated-noncanonical paragraph; HTML eyebrow/notice carries authority status near top; no footer element. | Prefer role matrix or decision tree; Mermaid optional only if the decision branch is clearer than the matrix. |
| `project-system-improvement` | Phase 4 | process timeline | 75 | Top generated-noncanonical paragraph; HTML warning appears in opening area; footer exists without the proposed hook. | Add improvement-loop process diagram. |
| `documentation-curator-publication-process` | Phase 4 | process timeline | 90 | Top generated-noncanonical paragraph; HTML warning appears in opening area; footer exists without authority language or hook. | Add publication lifecycle diagram. |
| `memory-system` | Phase 4 | layered architecture | 95 | Top generated-noncanonical paragraph in Markdown; HTML authority note appears in source section rather than footer; no footer element. | Add authority/retrieval layer diagram and query workflow. |
| `validator-operator-workflow` | Phase 4 | annotated table | 81 | Top generated-noncanonical paragraph in Markdown; HTML authority status appears near the final source area; no footer element. | No primary Mermaid required; annotated decision matrix remains preferred. |
| `roles-and-skills` | Phase 4 | role matrix | 83 | Top generated-noncanonical paragraph; HTML warning appears in opening area; no footer element. | No primary Mermaid required; role/skill matrix remains preferred. |
| `technical-requirements` | Phase 4 | annotated table | 74 | Top generated-noncanonical paragraph; HTML warning appears in opening area; footer exists without the proposed hook. | No primary Mermaid required; tool-tier table remains preferred. |

## Current Opening And Authority Text

### `project-overview`

- Current opening text: AEther-Flow has two linked missions. One is a physics
  research program that keeps exact general relativity as the benchmark while
  treating first-principles derivation from an AEther or AEther-flow substrate
  as open. The other is a research-agent system that routes bounded
  theoretical, refutation, documentation, and validation work through tracked
  control records. The shared rule is simple: source authority comes first,
  generated explanation comes after.
- Current top authority paragraph: This page is a noncanonical reader surface.
  Use it to choose the next source to inspect, not as evidence that a physics
  claim, role permission, validator rule, or generated-output authority has
  changed.
- Rewrite packet: expand the opening into a first-entry map for both missions,
  the authority ladder, and the safest reading path before source metadata.

### `source-authority`

- Current opening text: The trust question in AEther-Flow is not "which page is
  clearest?" It is "which source is allowed to define the project state?"
  Public documentation can be polished and useful, but it remains downstream
  of registered TeX, registries, and registered Markdown.
- Current top authority paragraph: This page is a noncanonical reader surface.
  Use it to understand the authority ladder before citing, editing, or
  summarizing project knowledge.
- Rewrite packet: expand the opening into a source-authority boundary map that
  explains canonical sources, generated derivatives, local caches, and the
  required inspection path.

### `aether-flow-physics-program`

- Current opening text: The AEther-Flow physics program asks whether ordinary
  general relativity can be interpreted, and eventually derived, from a deeper
  four-dimensional AEther / AEther-flow ontology. The current project state is
  deliberately conservative: exact GR is preserved as the observable-scale
  benchmark, while the first-principles substrate derivation remains open.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It is useful for public orientation, but it does not promote
  ontology, certify benchmark recovery, complete the derivation, issue a Gate
  Chair decision, or change any control record.
- Rewrite packet: expand the opening around exact-GR benchmark use, open
  derivation burden, negative-result preservation, and claim gates.

### `exact-gr-benchmark-boundary`

- Current opening text: AEther-Flow uses exact general relativity as a
  conservative public benchmark. At the observable scale, the benchmark keeps
  one operative Lorentzian metric, universal matter coupling, ordinary causal
  structure, and no empirical deviation claim from ordinary GR. That boundary
  is not the same thing as a first-principles derivation from AEther /
  AEther-flow substrate structure.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains how to avoid overclaiming; it does not change
  benchmark status, certify a derivation, issue a Gate Chair verdict, or make
  HTML, PDFs, or GitHub-facing Markdown into scientific authority.
- Rewrite packet: expand the opening around adoption, compatibility,
  derivation, ontology promotion, and Gate Chair boundaries.

### `aether-flow-ontology`

- Current opening text: AEther-Flow ontology is the project's vocabulary for
  what the relativistic mathematics is about. It names a deeper
  four-dimensional substrate, its ordered motion, and the observer-level
  experience of space, time, and expansion. That vocabulary is useful, but it
  is not by itself a first-principles derivation of general relativity.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It can orient readers to the ontology, but it does not
  promote ontology, certify exact-GR recovery, complete the derivation, change
  a claim boundary, or supersede registered TeX sources.
- Rewrite packet: expand the opening around vocabulary, model status,
  mathematical burden, and empirical-prediction boundary.

### `gr-derivation-roadmap`

- Current opening text: The GR derivation roadmap is the project's control
  surface for the open first-principles derivation problem. It names the
  sequence of burdens that would have to be discharged before the project
  could move from AEther / AEther-flow source structure to an exact-GR
  benchmark promotion.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the roadmap, but it does not update physics
  status, discharge a milestone, adopt `M_src`, derive `g_eff`, derive matter
  coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair
  verdict, or supersede tracked source files.
- Rewrite packet: expand the opening around milestones, evidence status,
  draft/control labels, blocked burdens, and human-gated burdens.

### `claim-gates`

- Current opening text: AEther-Flow uses claim gates to keep research work
  honest. A proposal can be useful, a stress test can fail, and a route can be
  frozen without any of those events becoming a public physics verdict.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the claim control model, but it does not create a
  claim boundary, issue a Gate Chair verdict, promote a benchmark, reject the
  global ontology, change role authority, or supersede tracked source files.
- Rewrite packet: expand the opening around proposal, audit, refutation,
  freeze, completion, handoff, negative-result preservation, and Gate Chair
  limits.

### `research-agent-workflow`

- Current opening text: AEther-Flow uses a research-agent workflow to keep
  theoretical work auditable. The workflow does not replace scientific proof,
  human gates, or source authority. It is the operating discipline that turns a
  request into one bounded transaction with explicit sources, role limits,
  checks, and completion evidence.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the workflow, but it does not change routing
  behavior, role authority, validator requirements, write permissions, claim
  boundaries, or physics status.
- Rewrite packet: expand the opening around classification, memory preflight,
  one AgentJob, checks, completion, and handoff.

### `director-agentjob-lifecycle`

- Current opening text: AEther-Flow records research-control work as a durable
  chain: task, Director Decision Record, AgentJob, execution-role record,
  completion, handoff, and registry rows. The chain lets future maintainers
  inspect what was authorized, what was done, what was checked, and what
  remains blocked or next.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the record lifecycle, but it does not edit
  schemas, change task behavior, alter routing, expand role authority, mutate
  historical records, or treat completion evidence as broad proof.
- Rewrite packet: expand the opening around DDR, AgentJob, execution role,
  completion, handoff, registry row, supersession rules, and immutable-record
  constraints.

### `parent-child-synthesis`

- Current opening text: Parent-child parallel synthesis is an internal
  perspective structure for future physics AgentJobs. It lets the project
  compare two child perspectives under a parent review without breaking the
  external control invariant: one Director decision, one outer AgentJob, one
  execution-role record, one completion record, and one final fused output.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the mode, but it does not change the one-job
  rule, AgentJob schema, execution-role schema, validators, routing behavior,
  role authority, write permissions, or physics claim status.
- Rewrite packet: expand the opening around the one-job invariant, inherited
  authority, child draft/control outputs, conflict handling, PASS-blocking
  unresolved conflicts, and fused output.

### `role-routing`

- Current opening text: AEther-Flow separates role identity from current job
  authority. A registered role tells the Director what kind of work a role can
  normally perform. The execution-role record and AgentJob allowlist decide
  what one job may actually do.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains role routing and execution contracts, but it does
  not register roles, expand role authority, change schemas, change routing
  behavior, change AgentJob allowlists, or authorize claim promotion.
- Rewrite packet: expand the opening around registered roles, overlays,
  provisional roles, task-local execution records, allowlists, and the
  difference between role names and current authority.

### `project-system-improvement`

- Current opening text: AEther-Flow separates physics continuation from
  project-system improvement. Physics continuation advances source-side
  research under claim gates. Project-system improvement repairs or clarifies
  the machinery around the research: documentation drift, control-contract
  drift, validator gaps, memory retrieval issues, and routing ambiguity.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the project-system improvement loop, but it does
  not create signals, resolve signals, change validators, change routing
  behavior, expand role authority, change AgentJob allowlists, or authorize
  physics claim promotion.
- Rewrite packet: expand the opening around classifier evidence, registered
  signals, advisory resolver state, bounded AgentJobs, receipts, and closure
  evidence.

### `documentation-curator-publication-process`

- Current opening text: AEther-Flow public documentation is written through the
  Documentation Curator Publication Process. The process exists because a
  structurally valid page can still be weak documentation: it can repeat a
  template, hide the subject behind metadata, add generic diagrams, or imply
  that generated reader surfaces carry authority they do not have.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains how public pages are planned, written, reviewed,
  and checked. It does not change role authority, validator behavior, schemas,
  routing, checkpoint gates, source authority, generated-output authority,
  corpus-migration approval, or physics claim status.
- Rewrite packet: expand the opening around brief, source spec, GitHub
  Markdown, HTML, screenshot QA, review evidence, and the retired-process
  boundary.

### `memory-system`

- Current opening text: AEther-Flow memory is source-first. The memory system
  helps a maintainer or agent find the right source, but it does not replace
  the source. A lookup hit, wiki note, semantic extract, Obsidian mirror,
  SQLite row, or `.local` cache is useful only when it points back to a
  registered source file and the relevant registry row.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the existing memory and retrieval system, but it
  does not change memory-system behavior, registry schema, validator behavior,
  routing behavior, role authority, checkpoint behavior, generated-output
  authority, source authority, or physics claim status.
- Rewrite packet: expand the opening around support-versus-authority,
  registries, wiki, semantic extracts, Obsidian, SQLite, freshness warnings,
  and why memory preflight never replaces source inspection.

### `validator-operator-workflow`

- Current opening text: AEther-Flow operators do not run every command by
  habit. They choose checks from the kind of change being made: memory and
  registry refresh, public publication page work, project-system control work,
  research-control state work, script changes, test changes, or tracked HTML
  review.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It explains the existing operator workflow, but it does not
  change validator behavior, command semantics, routing behavior,
  documentation-impact requirements, research-control requirements, role
  authority, schemas, checkpoint gates, generated-output authority, or physics
  claim status.
- Rewrite packet: expand the opening around command families, bootstrap versus
  validate-only, screenshot evidence, PASS limits, and change-type selection.

### `roles-and-skills`

- Current opening text: AEther-Flow roles and skills are navigation aids only
  when read from this public catalog. The actual authority lives in the role
  registry, the role or skill contract, the task-local execution-role record,
  the AgentJob allowlist, the claim boundary, the completion record, and the
  validators.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It does not change role status, register roles, supersede
  roles, expand role authority, change skill contracts, change validator
  behavior, change routing behavior, change AgentJob allowlists, change
  checkpoint behavior, or promote physics claims.
- Rewrite packet: expand the opening around active, superseded, human-gated,
  and task-local execution authority boundaries.

### `technical-requirements`

- Current opening text: Technical requirements are the local operating
  conditions that make AEther-Flow reproducible: the current Codex app harness
  for governed agent work, the Python virtual environment, dependency ledger,
  repository-owned scripts, Makefile targets, screenshot tooling, and PDF
  derivative path.
- Current top authority paragraph: This page is a generated noncanonical
  reader surface. It does not change dependencies, validators, Makefile
  targets, command semantics, harness policy, role authority, routing behavior,
  checkpoint behavior, generated-output authority, or physics claim status.
  Tool availability is support, not permission.
- Rewrite packet: expand the opening around Codex app use, Python environment,
  Makefile command families, Node/Playwright/Mermaid/PDF scopes, and
  tool-versus-authority boundaries.

## Phase 0 Exit Criterion

Phase 0 is complete as an audit packet. The audit confirms:

- which pages need prose expansion: all 17 pages;
- which pages need footer-authority placement work: all 17 pages;
- which pages need diagram work: the Phase 2, Phase 3, and selected Phase 4
  and Phase 5 pages named in the page matrix;
- which pages should keep table or matrix-first visual treatment:
  `validator-operator-workflow`, `roles-and-skills`, and
  `technical-requirements`, with `role-routing` remaining matrix-first unless
  a later decision tree proves clearer.

The logical next step is Phase 1. It should reconcile the old
`audit_documentation_surfaces.py` expectations with the current brief-first
publication contract, then add the footer-authority guard. It should not start
without explicit approval.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].

AEther-Flow Project. (2026). `.agents/roles/research_ops/documentation-curator.v2.0.0.md`
[Documentation Curator role contract].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`
[Publication brief registry].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_post_migration_quality_plan.md`
[Post-migration quality plan].

AEther-Flow Project. (2026). `registries/MARKDOWN_SOURCE_REGISTRY.csv`
[Markdown source registry].

AEther-Flow Project. (2026). `registries/HTML_EXPLAINER_REGISTRY.csv`
[HTML explainer registry].
