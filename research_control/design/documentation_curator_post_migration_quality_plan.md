<!-- authority: control -->

# Documentation Curator Post-Migration Quality Plan

## Purpose

This plan governs the next Documentation Curator quality pass after the public
explainer corpus migration. It addresses three requested changes:

1. Move the full generated-noncanonical reader-surface paragraph from the top
   of GitHub-facing Markdown and tracked HTML explainers to the footer.
2. Expand each opening topic, feature, or functionality description so it gives
   a useful subject-specific orientation before source metadata or authority
   cautions.
3. Add page-specific diagrams only where a diagram improves human
   understanding of the described mechanism, boundary, lifecycle, or workflow.

This is a planning document. It does not edit any public page, source spec, HTML
output, publication brief, validator, role contract, schema, science source, or
physics claim in this transaction.

## Authority Boundary

The existing authority hierarchy remains unchanged:

- Registered TeX files carry physics and derivational claims.
- Registries carry routing, provenance, generated-output tracking, and
  agent-queryable memory.
- Registered Markdown carries front-door guidance, publication briefs, source
  specs, role and skill contracts, and project-control notes.
- GitHub-facing Markdown, tracked HTML, wiki notes, semantic extracts, Obsidian
  mirrors, and local caches are reader or retrieval derivatives.

The future implementation may improve reader surfaces. It must not promote
generated derivatives into authority, alter control behavior, issue a Gate Chair
decision, change role authority, or modify physics status.

## Evidence Inspected

The plan is based on direct inspection of:

- `AGENTS.md` and `research_control/AGENTS.md`;
- `.codex/skills/improve-project-system/SKILL.md`;
- `.codex/skills/html-visual-explainer/SKILL.md`;
- `research_control/design/documentation_curator_publication_process.md`;
- `research_control/design/github_facing_explainer_contract.md`;
- `research_control/design/html_explainer_flexible_presentation_contract.md`;
- `research_control/design/documentation_curator_corpus_migration_plan.md`;
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`;
- `registries/HTML_EXPLAINER_REGISTRY.csv`;
- representative parent-child publication brief, source spec, GitHub-facing
  Markdown, and tracked HTML output.

Observed state:

- The corpus has 17 registered publication pages.
- The GitHub-facing pages commonly place the generated-noncanonical warning
  near the top, before the reader has enough subject context.
- Several HTML pages place the generated-noncanonical warning in the hero or
  header notice, while some already include footer source binding.
- The current GitHub-facing and source-spec corpus contains no Mermaid blocks.
- The HTML corpus contains no registered Mermaid inline SVG parity markers for
  these migrated pages.
- The existing publication process already rejects decorative generic diagrams
  and allows page-specific visual strategy choices.

## Required Presentation Change

### GitHub-Facing Markdown

Future Markdown revisions should use this order:

1. H1 page title.
2. Expanded subject description: two to four concise paragraphs that explain
   what the subject is, what it does in the project, why it matters, how it fits
   nearby systems, and which authority boundary constrains it.
3. Main reader sections, tables, examples, safe/unsafe summaries, and optional
   Mermaid diagram.
4. Footer source and authority block.

The full paragraph beginning with "This page is a generated noncanonical reader
surface..." belongs in the footer block, not immediately after the title. The
existing `## Source Binding` section can become `## Source Binding And
Authority` if that improves clarity, but it must remain near the end of the
file.

The top of the page may still contain a brief subject category or reader job,
but it must not lead with the full generated-surface disclaimer.

### Tracked HTML

Future HTML revisions should use this order:

1. Hero/title area with a subject-specific lead.
2. A summary or opening explanation that teaches the subject before warning
   boilerplate.
3. Page-local visual/table/workflow sections.
4. Source materials.
5. Footer with source binding and the full generated-noncanonical authority
   paragraph.

The footer should be marked with a stable control hook such as:

```html
<footer data-explainer-control="authority_footer">
```

The full generated-surface paragraph should be visible in that footer. Header
eyebrows such as "Generated noncanonical reader surface" should be removed or
replaced with subject-specific labels unless a future validator keeps a short
non-authority marker for machine detection. The full paragraph must not remain
in the hero notice.

## Expanded Description Standard

Each revised opening description should be source-backed and subject-specific.
It should answer:

- What is the topic, feature, or functionality?
- What project problem does it solve?
- Which source files or registries ground it?
- What adjacent systems does it connect to?
- What can a reader safely do after understanding it?
- What must not be inferred from the page?

Recommended length:

- GitHub-facing Markdown opening: 120-220 words before the first major section.
- HTML hero lead plus first summary: 120-240 words total, excluding visible
  source chips or source lists.

Do not expand the opening by repeating source metadata. The added detail should
teach the mechanism or boundary.

## Diagram Standard

Diagrams are optional but should be used when they teach structure better than
prose or a table. A diagram is justified when the subject contains:

- state transitions;
- lifecycle steps;
- authority layers;
- role-routing branches;
- parallel lanes;
- source-to-derivative relationships;
- claim-boundary comparisons; or
- workflow checkpoints.

Markdown diagrams should use Mermaid when the diagram is beneficial. HTML
diagrams should be rendered at build time as inline SVG or equivalent
standalone local visual output. Do not use browser-side Mermaid, CDN scripts,
remote fonts, `npx`, localhost bridge artifacts, or any network-required
runtime in tracked HTML.

Every diagram must include reader-purpose prose and source-basis prose. A
diagram that could be dropped into many unrelated pages fails review.

## Implementation Phases

### Phase 0: Audit And Rewrite Packets

Scope:

- Inspect all 17 publication brief rows, source specs, GitHub-facing Markdown
  files, and tracked HTML files.
- Build a per-page audit artifact that records current opening text, current
  top authority paragraph, current footer binding, current visual strategy, and
  diagram decision.
- Verify each page topic against its publication brief and source materials.
- Do not edit public outputs in this phase.

Required checks:

- `scripts/validate_publication_process.py --root . --strict`
- `scripts/project_control/audit_documentation_surfaces.py`
- bootstrap validate-only

Exit criterion:

- A page-by-page audit confirms which pages need diagram work and which need
  prose-only opening expansion.

### Phase 1: Contract And Validator Guard

Scope:

- Update the GitHub-facing and HTML publication contracts to specify footer
  placement for the full generated-noncanonical paragraph.
- Add or adjust validator tests so future pages cannot move the full paragraph
  back into the top hero/opening position.
- Add an HTML `authority_footer` convention if a deterministic marker is
  useful.
- Do not rewrite corpus pages in this phase unless the validator change needs
  one minimal fixture.

Role boundary:

- Project-Control Maintainer, because this phase changes contract or validator
  behavior.

Exit criterion:

- Validator behavior and tests pass while implementation packets remain
  blocked pending user approval.

### Phase 2: Physics Status And Claim-Boundary Pages

Pages:

- `aether-flow-physics-program`
- `exact-gr-benchmark-boundary`
- `aether-flow-ontology`
- `gr-derivation-roadmap`
- `claim-gates`

Purpose:

- Expand the openings so readers can distinguish benchmark adoption, ontology
  vocabulary, derivation burden, source-extension/draft-control language, claim
  gates, negative results, freeze criteria, and Gate Chair boundaries.

Diagram decisions:

- Add diagrams for all five pages unless the Phase 0 audit proves a current
  table or matrix is clearer.
- Preferred forms: layered architecture, authority ladder, burden timeline,
  claim-gate state model, and adoption-versus-derivation boundary map.

Exit criterion:

- No page suggests ontology promotion, completed derivation, benchmark
  promotion, or Gate Chair approval.

### Phase 3: Research-Control Operation Pages

Pages:

- `research-agent-workflow`
- `director-agentjob-lifecycle`
- `parent-child-synthesis`
- `role-routing`

Purpose:

- Explain how requests become bounded tasks, how Director decisions and
  AgentJobs become durable records, how parent-child synthesis works inside one
  physics AgentJob, and how role names differ from execution authority.

Diagram decisions:

- Add diagrams for `research-agent-workflow`, `director-agentjob-lifecycle`,
  and `parent-child-synthesis`.
- Use a decision-tree or role-matrix visual for `role-routing`; Mermaid is
  optional because a compact role matrix may be clearer than a graph.

Parent-child required detail:

- The expanded opening must state one Director decision, one outer AgentJob,
  one execution-role record, one completion record, and one fused output.
- It must state that child outputs are draft/control support artifacts.
- It must state that unresolved declared blocking conflict prevents PASS
  completion.
- It must not imply that all non-physics tasks use this mode.

### Phase 4: Project-System, Documentation, Memory, And Operator Pages

Pages:

- `project-system-improvement`
- `documentation-curator-publication-process`
- `memory-system`
- `validator-operator-workflow`
- `roles-and-skills`
- `technical-requirements`

Purpose:

- Make operational pages more useful without turning tool availability,
  validators, role catalogs, or generated documentation into authority.

Diagram decisions:

- Add diagrams for `project-system-improvement`,
  `documentation-curator-publication-process`, and `memory-system`.
- Do not require Mermaid diagrams for `validator-operator-workflow`,
  `roles-and-skills`, or `technical-requirements`; dense command matrices,
  role matrices, and tool-tier tables are likely more useful. Add Mermaid only
  if the audit finds a specific decision branch that a table cannot explain.

Exit criterion:

- Pages separate executable authority from navigation, retrieval, validator
  pass state, and tool setup.

### Phase 5: Overview And Cross-Page Coherence

Pages:

- `project-overview`
- `source-authority`

Purpose:

- Make the overview and source-authority pages function as first-entry maps for
  humans and external AI readers.

Diagram decisions:

- Add a compact atlas/navigation diagram to `project-overview` only if it does
  not become a generic source-to-validation graphic.
- Add an authority-ladder or source-to-derivative boundary diagram to
  `source-authority`.

Exit criterion:

- The overview points readers to the right page family, and source authority
  makes the canonical-versus-derivative boundary visually obvious.

### Phase 6: Full QA, Regeneration, And Checkpoint

Scope:

- Regenerate tracked HTML from updated source specs.
- Synchronize GitHub-facing Markdown with the revised source basis and core
  claims.
- Render any Mermaid diagrams into governed HTML inline SVG or equivalent
  local visuals.
- Refresh memory/wiki/registry derivatives through the bootstrap path.
- Capture desktop and mobile screenshots for each changed HTML page.

Required checks:

- `scripts/validate_publication_process.py --root . --strict`
- project-memory bootstrap
- project-memory validate-only
- documentation-impact validation
- research-control validation
- research-control diff validation
- `git diff --check`

Exit criterion:

- Every changed page has footer authority placement, expanded subject
  description, source-backed diagram decision, rendered QA evidence, and PASS
  validation receipts.

## Page-By-Page Recommendation Matrix

| Page | Function to re-check | Opening expansion target | Diagram decision |
| --- | --- | --- | --- |
| `project-overview` | First-entry map for two project missions and the authority spine. | Explain the two missions, authority ladder, and safest first reading path before source metadata. | Optional compact atlas map; avoid generic validation flow. |
| `source-authority` | Boundary between canonical sources and generated or local derivatives. | Explain the authority ladder, derivative surfaces, and what must be inspected before editing. | Add authority-ladder or source-to-derivative diagram. |
| `aether-flow-physics-program` | Physics program status and benchmark-disciplined research lane. | Explain exact-GR benchmark use, open derivation burden, negative-result preservation, and claim gates. | Add layered status architecture. |
| `exact-gr-benchmark-boundary` | Difference between exact-GR adoption and first-principles derivation. | Explain adoption, compatibility, derivation, ontology promotion, and Gate Chair boundaries. | Add adoption-versus-derivation boundary diagram. |
| `aether-flow-ontology` | Ontology vocabulary and its limits. | Explain vocabulary, model status, mathematical burden, and empirical-prediction boundary. | Add layered ontology/source/claim-boundary diagram. |
| `gr-derivation-roadmap` | Ordered burden chain and current frontier. | Explain milestones, evidence status, draft/control labels, and blocked or human-gated burdens. | Add milestone/burden timeline. |
| `claim-gates` | Claim-control lifecycle and negative-result preservation. | Explain proposal, audit, refutation, freeze, completion, handoff, and Gate Chair limits. | Add claim-state model. |
| `research-agent-workflow` | Bounded request-to-completion workflow. | Explain classification, memory preflight, one AgentJob, checks, completion, and handoff. | Add process-lane diagram. |
| `director-agentjob-lifecycle` | Durable control-record chain. | Explain DDR, AgentJob, execution role, completion, handoff, registry row, and supersession rules. | Add lifecycle state diagram. |
| `parent-child-synthesis` | Internal perspective decomposition within one physics AgentJob. | Expand the one-job invariant, inherited authority, child draft/control outputs, conflict handling, and fused output. | Add two-lane parent/child/fusion diagram. |
| `role-routing` | Registered role, overlay, provisional role, and execution record boundaries. | Explain why a role name is not current authority until task-local execution records and allowlists are inspected. | Prefer role matrix or decision tree; Mermaid optional. |
| `project-system-improvement` | Documentation/control/validator/memory drift routing. | Explain classifier evidence, registered signals, advisory resolver, bounded AgentJob, receipts, and closure evidence. | Add improvement-loop process diagram. |
| `documentation-curator-publication-process` | Brief-first publication workflow. | Explain brief, source spec, GitHub Markdown, HTML, screenshot QA, review evidence, and retired-process boundary. | Add publication lifecycle diagram. |
| `memory-system` | Registries, wiki, semantic extracts, Obsidian, SQLite, and freshness warnings. | Explain support-versus-authority split and why memory preflight never replaces source inspection. | Add authority/retrieval layer diagram and query workflow. |
| `validator-operator-workflow` | Correct command chain by change type. | Explain command families, bootstrap versus validate-only, screenshot evidence, and PASS limits. | No primary Mermaid required; annotated decision matrix preferred. |
| `roles-and-skills` | Dense navigation catalog for roles and skills. | Explain active, superseded, human-gated, and task-local execution authority boundaries. | No primary Mermaid required; role/skill matrix preferred. |
| `technical-requirements` | Local tool tiers for reproducible operation. | Explain Codex app, Python environment, Makefile, Node/Playwright/Mermaid/PDF scopes, and tool-versus-authority boundary. | No primary Mermaid required; tool-tier table preferred. |

## Stop Conditions

Pause implementation if any phase would require:

- canonical ontology or TeX edits;
- benchmark promotion;
- completed-derivation language;
- Gate Chair decision;
- schema, role, skill, routing, validator, or checkpoint behavior change
  outside an explicitly approved Project-Control Maintainer phase;
- browser-side Mermaid or network-required assets in tracked HTML;
- direct HTML-only edits without source-spec and GitHub-facing synchronization;
- corpus-wide public page rewrites without explicit user approval.

## Recommended Next Step

The logical next step is Phase 0: create a page-by-page audit artifact that
records current top-warning placement, footer status, opening-description
adequacy, and diagram recommendation for all 17 pages. After that audit, seek
explicit approval for Phase 1 before changing contracts or validators.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].

AEther-Flow Project. (2026). `research_control/AGENTS.md` [Research-control
authority and editing rules].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_publication_process.md`
[Documentation Curator publication process].

AEther-Flow Project. (2026).
`research_control/design/github_facing_explainer_contract.md`
[GitHub-facing explainer contract].

AEther-Flow Project. (2026).
`research_control/design/html_explainer_flexible_presentation_contract.md`
[HTML explainer presentation contract].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_corpus_migration_plan.md`
[Documentation Curator corpus migration plan].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`
[Publication brief registry].

AEther-Flow Project. (2026). `registries/MARKDOWN_SOURCE_REGISTRY.csv`
[Markdown source registry].

AEther-Flow Project. (2026). `registries/HTML_EXPLAINER_REGISTRY.csv`
[HTML explainer registry].
