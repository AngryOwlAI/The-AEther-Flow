<!-- authority: explanatory -->

# Reader Scope Footer Relocation Phase 0 Audit

## Scope

This artifact executes Phase 0 of
`research_control/design/documentation_curator_reader_scope_footer_relocation_plan.md`.
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
- GitHub-facing Markdown path;
- tracked HTML path;
- current Markdown `Reader scope` occurrence;
- current HTML `Reader scope` occurrence;
- current Markdown authority-footer marker;
- current HTML `authority_footer` hook;
- exact visible boundary text on the Markdown and HTML surfaces; and
- whether the page needs a prose move, source-spec wording review, HTML layout
  repair, nav update, CSS update, screenshot refresh, or validator guardrail.

Memory preflight was used only for navigation. It reported a fresh local memory
index and identified the Reader Scope relocation plan as relevant context. The
canonical plan, publication registry, role contract, and project-improvement
skill were then inspected directly.

## Corpus-Level Findings

| Finding | Result |
| --- | --- |
| Reviewed publication rows audited | 17 |
| Missing GitHub-facing Markdown outputs | 0 |
| Missing tracked HTML outputs | 0 |
| GitHub-facing pages with authority-footer marker | 17 |
| Tracked HTML pages with `authority_footer` hook | 17 |
| GitHub-facing pages with a top-positioned `Reader scope` paragraph | 15 |
| GitHub-facing pages with no separate `Reader scope` paragraph | 2 |
| HTML pages with `Reader scope` in the header/opening area | 14 |
| HTML pages with `Reader scope` in the first main section but not footer-adjacent | 3 |
| HTML pages whose `Reader scope` block is immediately above the authority footer | 0 |
| Source specs containing literal `Reader scope` text or `reader_scope` hook | 0 |

Conclusion: Phase 1 should settle the explicit bottom hook and mechanical
guardrail before any public page is edited. Phase 2 through Phase 5 should not
be HTML-only edits because the current source specs do not carry literal
`Reader scope` hook instructions.

## Page Matrix

Line numbers are Phase 0 baseline evidence and will drift once the corpus is
edited.

| Page | Phase | Source spec | GitHub Markdown | HTML | Current Markdown placement | Current HTML placement | Footer hook | Markdown already satisfies target opening? | Required later work |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `technical-requirements` | 5 | `markdown/html-explainer-specs/technical-requirements-explainer.md` | `github-facing/technical-requirements-explainer.md` | `html/technical-requirements-explainer.html` | line 9 before first section | header line 162 | Markdown line 49; HTML line 223 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `roles-and-skills` | 5 | `markdown/html-explainer-specs/roles-and-skills-explainer.md` | `github-facing/roles-and-skills-explainer.md` | `html/roles-and-skills-explainer.html` | line 9 before first section | header line 162 | Markdown line 50; HTML line 216 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `memory-system` | 5 | `markdown/html-explainer-specs/memory-system-explainer.md` | `github-facing/memory-system-explainer.md` | `html/memory-system-explainer.html` | line 9 before first section | header line 162 | Markdown line 47; HTML line 224 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `validator-operator-workflow` | 5 | `markdown/html-explainer-specs/validator-operator-workflow-explainer.md` | `github-facing/validator-operator-workflow-explainer.md` | `html/validator-operator-workflow-explainer.html` | line 9 before first section | header line 162 | Markdown line 47; HTML line 223 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `documentation-curator-publication-process` | 5 | `markdown/html-explainer-specs/documentation-curator-publication-process-explainer.md` | `github-facing/documentation-curator-publication-process-explainer.md` | `html/documentation-curator-publication-process-explainer.html` | line 9 before first section | header line 162 | Markdown line 46; HTML line 220 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `project-system-improvement` | 5 | `markdown/html-explainer-specs/project-system-improvement-explainer.md` | `github-facing/project-system-improvement-explainer.md` | `html/project-system-improvement-explainer.html` | line 9 before first section | header line 162 | Markdown line 47; HTML line 220 | no | Move Markdown prose; move HTML block; source-spec placement review; CSS check; screenshot refresh. |
| `parent-child-synthesis` | 4 | `markdown/html-explainer-specs/parent-child-synthesis-explainer.md` | `github-facing/parent-child-synthesis-explainer.md` | `html/parent-child-synthesis-explainer.html` | line 19 before first section | header line 183 | Markdown line 89; HTML line 262 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; CSS check; screenshot refresh. |
| `role-routing` | 4 | `markdown/html-explainer-specs/role-routing-explainer.md` | `github-facing/role-routing-explainer.md` | `html/role-routing-explainer.html` | line 19 before first section | header line 168 | Markdown line 94; HTML line 242 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; CSS check; screenshot refresh. |
| `research-agent-workflow` | 4 | `markdown/html-explainer-specs/research-agent-workflow-explainer.md` | `github-facing/research-agent-workflow-explainer.md` | `html/research-agent-workflow-explainer.html` | line 19 before first section | header line 175 | Markdown line 108; HTML line 265 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; CSS check; screenshot refresh. |
| `director-agentjob-lifecycle` | 4 | `markdown/html-explainer-specs/director-agentjob-lifecycle-explainer.md` | `github-facing/director-agentjob-lifecycle-explainer.md` | `html/director-agentjob-lifecycle-explainer.html` | line 17 before first section | header line 176 | Markdown line 100; HTML line 256 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; CSS check; screenshot refresh. |
| `claim-gates` | 3 | `markdown/html-explainer-specs/claim-gates-explainer.md` | `github-facing/claim-gates-explainer.md` | `html/claim-gates-explainer.html` | line 10 before first section | first main section line 251 | Markdown line 126; HTML line 439 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; preserve claim qualifiers; CSS check; screenshot refresh. |
| `gr-derivation-roadmap` | 3 | `markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md` | `github-facing/gr-derivation-roadmap-explainer.md` | `html/gr-derivation-roadmap-explainer.html` | line 11 before first section | first main section line 262 | Markdown line 130; HTML line 432 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; preserve `M_src`, `g_eff`, matter-coupling, Einstein-equation, and Gate Chair limits; CSS check; screenshot refresh. |
| `aether-flow-ontology` | 3 | `markdown/html-explainer-specs/aether-flow-ontology-explainer.md` | `github-facing/aether-flow-ontology-explainer.md` | `html/aether-flow-ontology-explainer.html` | line 10 before first section | first main section line 255 | Markdown line 99; HTML line 405 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; preserve ontology-promotion and derivation limits; CSS check; screenshot refresh. |
| `exact-gr-benchmark-boundary` | 3 | `markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md` | `github-facing/exact-gr-benchmark-boundary-explainer.md` | `html/exact-gr-benchmark-boundary-explainer.html` | line 12 before first section | header line 185 | Markdown line 71; HTML line 286 | no | Move Markdown prose; move HTML block; source-spec placement review; preserve benchmark and scientific-authority limits; CSS check; screenshot refresh. |
| `aether-flow-physics-program` | 3 | `markdown/html-explainer-specs/aether-flow-physics-program-explainer.md` | `github-facing/aether-flow-physics-program-explainer.md` | `html/aether-flow-physics-program-explainer.html` | line 12 before first section | header line 156 | Markdown line 91; HTML line 255 | no | Move Markdown prose; move HTML block; source-spec wording review because Markdown and HTML text differ; preserve ontology benchmark derivation Gate Chair and control-record limits; CSS check; screenshot refresh. |
| `project-overview` | 2 | `markdown/html-explainer-specs/project-overview-explainer.md` | `github-facing/project-overview-explainer.md` | `html/project-overview-explainer.html` | no separate Reader scope paragraph | header line 173 | Markdown line 66; HTML line 246 | yes for opening; explicit heading unsettled | Move HTML block; no Markdown prose move unless Phase 1 requires explicit `## Reader Scope`; source-spec hook review; CSS check; screenshot refresh. |
| `source-authority` | 2 | `markdown/html-explainer-specs/source-authority-explainer.md` | `github-facing/source-authority-explainer.md` | `html/source-authority-explainer.html` | no separate Reader scope paragraph | header line 171 | Markdown line 63; HTML line 247 | yes for opening; explicit heading unsettled | Move HTML block; no Markdown prose move unless Phase 1 requires explicit `## Reader Scope`; source-spec hook review; CSS check; screenshot refresh. |

## Boundary Text Audit

### `technical-requirements`

- Markdown: Reader scope: local operation requirements only. This page cannot change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics status.
- HTML: Reader scope: local operation requirements only. This page cannot change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics status.

### `roles-and-skills`

- Markdown: Reader scope: role and skill navigation only. This page cannot change role status, register roles, supersede roles, expand role authority, change skill contracts, change validator behavior, change routing, change allowlists, or promote physics claims.
- HTML: Reader scope: role and skill navigation only. This page cannot change role status, register roles, supersede roles, expand role authority, change skill contracts, change validator behavior, change routing, change allowlists, or promote physics claims.

### `memory-system`

- Markdown: Reader scope: memory and retrieval orientation only. This page cannot change memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, source authority, or physics status.
- HTML: Reader scope: memory and retrieval orientation only. This page cannot change memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, source authority, or physics status.

### `validator-operator-workflow`

- Markdown: Reader scope: operator command-selection guide only. This page cannot change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, schemas, checkpoint gates, or physics status.
- HTML: Reader scope: operator command-selection guide only. This page cannot change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, schemas, checkpoint gates, or physics status.

### `documentation-curator-publication-process`

- Markdown: Reader scope: publication-process orientation only. This page cannot change role authority, validator behavior, schemas, routing, checkpoint gates, generated-output authority, or corpus-migration approval.
- HTML: Reader scope: publication-process orientation only. This page cannot change role authority, validator behavior, schemas, routing, checkpoint gates, generated-output authority, or corpus-migration approval.

### `project-system-improvement`

- Markdown: Reader scope: project-system workflow orientation only. This page cannot create or close signals, change routing behavior, change validator behavior, expand role authority, or authorize physics claim promotion.
- HTML: Reader scope: project-system workflow orientation only. This page cannot create or close signals, change routing behavior, change validator behavior, expand role authority, or authorize physics claim promotion.

### `parent-child-synthesis`

- Markdown: Reader scope: concept orientation only. This explanation cannot change the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, role authority, write permissions, or physics claim status.
- HTML: Reader scope: concept orientation only. This page cannot change the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, role authority, write permissions, or physics claim status.

### `role-routing`

- Markdown: Reader scope: role-routing reference only. This explanation cannot register roles, expand role authority, change schemas, change routing behavior, change AgentJob allowlists, or authorize claim promotion.
- HTML: Reader scope: role-routing reference only. This page cannot register roles, expand role authority, change schemas, change routing behavior, change AgentJob allowlists, or authorize claim promotion.

### `research-agent-workflow`

- Markdown: Reader scope: public workflow orientation only. This explanation cannot change routing behavior, role authority, validator requirements, write permissions, claim boundaries, or physics status.
- HTML: Reader scope: public workflow orientation only. This page cannot change routing behavior, role authority, validator requirements, write permissions, claim boundaries, or physics status.

### `director-agentjob-lifecycle`

- Markdown: Reader scope: lifecycle orientation only. This explanation cannot edit schemas, change task behavior, alter routing, expand role authority, mutate historical records, or treat completion evidence as broad proof.
- HTML: Reader scope: lifecycle orientation only. This page cannot edit schemas, change task behavior, alter routing, expand role authority, mutate historical records, or treat completion evidence as broad proof.

### `claim-gates`

- Markdown: Reader scope: claim-control explanation only. It does not create a claim boundary, issue a Gate Chair verdict, promote a benchmark, reject the global ontology, change role authority, or supersede tracked source files.
- HTML: Reader scope: claim-control explanation only. It does not create a claim boundary, issue a Gate Chair verdict, promote a benchmark, reject the global ontology, change role authority, or treat validator pass state as scientific evidence.

### `gr-derivation-roadmap`

- Markdown: Reader scope: roadmap explanation only. It does not update physics status, discharge a milestone, adopt `M_src`, derive `g_eff`, derive matter coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or supersede tracked source files.
- HTML: Reader scope: roadmap explanation only. It does not update the Distance-to-GR ledger, adopt `M_src`, derive `g_eff`, derive matter coupling, derive Einstein equations, promote a benchmark, or issue a Gate Chair verdict.

### `aether-flow-ontology`

- Markdown: Reader scope: ontology orientation only. It can help readers use the vocabulary, but it does not promote ontology, certify exact-GR recovery, complete the derivation, change a claim boundary, or supersede registered TeX sources.
- HTML: Reader scope: ontology orientation only. It does not promote ontology, certify exact-GR recovery, complete a derivation, change a claim boundary, or supersede registered TeX sources.

### `exact-gr-benchmark-boundary`

- Markdown: Reader scope: boundary explanation only. It does not change benchmark status, certify a derivation, issue a Gate Chair verdict, or make HTML, PDFs, or GitHub-facing Markdown into scientific authority.
- HTML: Reader scope: boundary explanation only. It does not change benchmark status, certify a derivation, issue a Gate Chair verdict, or make HTML, PDFs, or GitHub-facing Markdown into scientific authority.

### `aether-flow-physics-program`

- Markdown: Reader scope: public orientation only. This explanation cannot promote ontology, certify benchmark recovery, complete the derivation, issue a Gate Chair decision, or change any control record.
- HTML: Reader scope: public orientation only. It does not promote ontology, certify benchmark recovery, complete the derivation, issue a Gate Chair decision, or change any control record.

### `project-overview`

- Markdown: This page is a generated noncanonical reader surface. It orients readers to the physics research lane, the research-agent workflow lane, the source-authority spine, page-family routes, and first-reading paths without creating physics claims, role authority, routing behavior, validator authority, write permissions, or generated-output authority.
- HTML: Reader scope: first-entry orientation only. This page cannot certify a derivation, expand a role, change routing, change validators, grant write permission, or make generated documentation authoritative.

### `source-authority`

- Markdown: This page is a generated noncanonical reader surface. It teaches source-authority and derivative-surface boundaries, authority-layer reading order, source-to-derivative use, generated-page failure modes, and source-first checklists without creating physics claims, control authority, role authority, routing behavior, validator authority, write permissions, or generated-output authority.
- HTML: Reader scope: source-authority orientation only. This page cannot change the hierarchy, replace a registry, promote ontology, certify a benchmark, issue a Gate Chair verdict, expand roles, or modify routing behavior.

## Phase Decisions

### Phase 1

Required before public-page edits:

- Define whether GitHub-facing Markdown must use an explicit `## Reader Scope`
  heading on every page or whether `project-overview` and `source-authority`
  may keep the current footer-authority paragraph without a separate Reader
  Scope section.
- Define the HTML hook as
  `section[data-explainer-control="reader_scope"]` immediately before
  `footer[data-explainer-control="authority_footer"]`.
- Decide whether the section navigation should include the bottom scope block.
  Current pages do not require a nav update if the block is treated as a final
  boundary check rather than a main content destination.
- Add a narrow validator guardrail only after the target pattern is locked.

### Phase 2

Pilot `project-overview` and `source-authority`.

- Markdown already has no top Reader scope paragraph.
- HTML still needs relocation from the header to immediately above the footer.
- Source specs need hook-placement review if Phase 1 requires an explicit
  `reader_scope` hook.
- CSS and screenshot QA are required for both changed HTML pages.

### Phase 3

Physics status and claim-boundary pages require Markdown prose moves and HTML
layout repair. The `aether-flow-physics-program`, `aether-flow-ontology`,
`gr-derivation-roadmap`, and `claim-gates` pages also need source-spec wording
review because the Markdown and HTML boundary text are not exact matches.
`exact-gr-benchmark-boundary` has matching boundary text but still needs the
placement move.

### Phase 4

Research-control operation pages require Markdown prose moves, HTML layout
repair, source-spec wording review, CSS checks, and screenshot refresh. The
main mismatch is `This explanation` in Markdown versus `This page` in HTML.

### Phase 5

Project-system, memory, operator, role, and requirement pages require Markdown
prose moves and HTML layout repair. Their Markdown and HTML Reader scope text
already match, so wording repair is not required unless Phase 1 chooses a new
universal wording convention.

## Stop Conditions Preserved

Pause later implementation if a relocation would require changing canonical
TeX, ontology status, benchmark status, derivation status, Gate Chair status,
role authority, schema behavior, validator behavior beyond the approved Phase
1 guardrail, routing behavior, checkpoint behavior, or generated-output
authority. Pause also if a page loses source paths, loses the generated
noncanonical warning, loses the authority footer, or screenshot QA reveals
mobile overflow or unreadable footer flow.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy,
generated-output boundaries, and project-system improvement guidance].

AEther-Flow Project. (2026). `research_control/AGENTS.md` [Research-control
authority and editing rules].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_reader_scope_footer_relocation_plan.md`
[Reader Scope footer relocation plan].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`
[Publication brief registry].

AEther-Flow Project. (2026).
`.agents/roles/research_ops/documentation-curator.v2.0.0.md` [Documentation
Curator role contract].
