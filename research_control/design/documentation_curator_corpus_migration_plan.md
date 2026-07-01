<!-- authority: control -->

# Documentation Curator Corpus Migration Plan

## Purpose

This plan defines the phased migration path for AEther-Flow public
documentation after the Documentation Curator Publication Process pilot. It
decides which project functions need public GitHub-facing Markdown and tracked
HTML coverage, which old explainer topics should be retained, renamed,
merged, or retired, and how future migration packets should be executed
without turning the whole corpus into one uncontrolled rewrite.

The plan is a project-control planning document. It does not create physics
claims, promote ontology, change role authority, authorize generated-output
authority, or migrate any public page by itself.

## Current State

The active publication process is brief-first:

- each migrated public page needs a publication brief under
  `markdown/publication-briefs/`;
- each migrated public page needs a row in
  `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- each migrated public page needs a Markdown source spec under
  `markdown/html-explainer-specs/`;
- each migrated public page may have a native GitHub-facing Markdown surface
  under `github-facing/`;
- each migrated public page may have a tracked standalone HTML derivative
  under `html/`; and
- each tracked HTML page needs screenshot QA and before/after review evidence.

The reviewed pilot pages are:

| Page | Status | Function |
| --- | --- | --- |
| `project-overview-explainer` | reviewed | Front-door orientation to the two project missions and first reading path. |
| `source-authority-explainer` | reviewed | Boundary map for canonical sources, derivatives, registries, and local retrieval layers. |

The old topic registry is retired. Historical topics may be used as evidence
of reader needs, but they are not an active creation mechanism. Future work
must route through publication briefs and the publication brief registry.

## Migration Principles

### Selection Principles

Migrate pages in this order:

1. High public overclaim risk: pages that prevent readers from confusing exact
   GR benchmark compatibility, ontology, derivation status, and generated
   explanation.
2. High operational risk: pages that prevent agents and maintainers from
   misusing research-control, AgentJob, role, memory, registry, or validator
   machinery.
3. High navigation value: pages that let new readers choose the correct source
   lane quickly.
4. Stable source basis: pages whose source bundle is mostly stable should move
   before pages whose content depends on volatile active research frontier
   state.
5. Distinct reader job: a page remains standalone only if it answers a
   different reader question from existing pages.

### Packet Size

Do not run corpus-wide migration as a single transaction. A normal migration
packet should contain one or two public pages. A three-page packet is allowed
only when the pages share the same source bundle and review evidence can still
be specific to each page.

Every packet must preserve explicit user approval. Approval for this plan is
not approval to migrate all pages.

### Surface Rules

GitHub-facing Markdown should:

- open with the subject and reader problem, not metadata;
- read as a native technical article;
- state generated noncanonical status early;
- include source binding, source materials, and authority boundaries;
- use page-specific headings;
- include tables or lists when they clarify source use;
- avoid raw teaching transcripts, old universal section skeletons, and
  generated HTML transcript shape; and
- preserve exact qualifiers such as `draft/control`, `source-only`,
  `source-extension data`, `local`, `exact-branch`, and `human-gated`.

Tracked HTML should:

- be a single-file, no-network, no-runtime derivative;
- use the medium's strengths rather than copying GitHub Markdown structure;
- include visible source grounding and non-authority language;
- use a page-specific visual strategy only when it teaches something concrete;
- avoid generic source-to-validation diagrams;
- remain readable on mobile and desktop;
- avoid external scripts, CDNs, remote fonts, analytics, hosted comments, NPX,
  localhost dependencies, and browser-side Mermaid execution; and
- receive desktop and mobile screenshot QA before review status is upgraded.

## Definition Of Done For A Page

A migrated page is done only when all of these exist and pass review:

1. Publication brief with the required fields.
2. Publication brief registry row.
3. Markdown source spec bound to the brief.
4. GitHub-facing Markdown derivative if that surface is listed.
5. Tracked HTML derivative if that surface is listed.
6. Desktop screenshot for HTML.
7. Mobile screenshot for HTML.
8. Before/after review artifact naming page-specific improvements and
   remaining risks.
9. Bootstrap refresh.
10. Publication process validation.
11. Documentation-impact validation when required by the live transaction.
12. Research-control validation.

Required command chain for normal packets:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <source-or-page> --json
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/resolve_project_improvement.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/validate_publication_process.py --root . --strict
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
git diff --check
```

Run unit tests when a packet changes scripts, validators, schemas, role
contracts, or memory-system machinery:

```zsh
.venv/bin/python -m unittest discover -s tests
```

## Phase 0: Pilot Baseline

Status: complete. Maintain only.

### Covered Pages

| Page | Public Function | Required Maintenance |
| --- | --- | --- |
| Project Overview | Front-door orientation. | Keep source paths current when `README.md`, `AGENTS.md`, `research_control/README.md`, or the publication process changes. |
| Source Authority And Generated Derivatives | Trust boundary map. | Keep authority ladder current when registries, memory tooling, or generated-surface rules change. |

### Phase 0 Tasks

- Preserve both reviewed pilot pages as the quality bar.
- Do not broaden the pilot into automatic corpus migration.
- Keep `approval_required_before_corpus_migration` set to `true` until a
  bounded packet is explicitly approved.
- If either pilot drifts, repair the pilot before adding new pages.

## Phase 1: Public Physics Status

Goal: reduce the highest public-risk ambiguity: the project has an exact-GR
benchmark and an ontology, but the first-principles GR derivation remains
open.

Recommended packet order:

1. Phase 1A: `exact-gr-benchmark-boundary-explainer` and
   `aether-flow-physics-program-explainer`.
2. Phase 1B: `aether-flow-ontology-explainer`.

### Page: Exact-GR Benchmark Boundary

Recommended filename family:
`exact-gr-benchmark-boundary-explainer`.

Document type: `comparison_or_boundary_map`.

Reader job: distinguish exact-GR benchmark adoption from substrate
derivation, ontology promotion, and Gate Chair approval.

Source basis:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/design/gr_derivation_burden_map.md`

GitHub-facing Markdown must cover:

- the exact-GR benchmark as the observable-scale conservative boundary;
- one operative metric, universal matter coupling, ordinary causal structure,
  and no empirical deviation claim;
- difference between adoption, compatibility, derivation, and benchmark
  promotion;
- the fact that PDFs and HTML are not scientific authority;
- where registered TeX carries benchmark claims; and
- what the page is forbidden to prove.

HTML must cover:

- a compact "adoption versus derivation" matrix;
- a benchmark-boundary ladder from canonical TeX to public derivative;
- a failure-mode panel for common overclaims; and
- clear source paths for the TeX registry and claim boundary registry.

Visual strategy: `source_matrix` or `comparison_or_boundary_map`.

Acceptance emphasis:

- no language implying completed derivation;
- no language implying generated public docs can certify benchmark status;
- exact-GR benchmark terms remain conservative and source-backed.

### Page: AEther-Flow Physics Program

Recommended filename family: `aether-flow-physics-program-explainer`.

Document type: `overview_article`.

Reader job: understand the physics program as a research program with a
benchmark, an open derivation burden, negative-result preservation, and a
claim-gated path forward.

Source basis:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `research_control/README.md`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

GitHub-facing Markdown must cover:

- the physics track in relation to the AI research-agent track;
- exact-GR benchmark status;
- open first-principles derivation burden;
- the role of no-go, obstruction, and freeze records;
- the difference between source-side mathematical work and claim promotion;
- the current need to preserve qualifiers such as `draft/control` and
  `source-only`; and
- how a reader should inspect sources before summarizing the physics.

HTML must cover:

- a status map separating ontology, benchmark, derivation burden, and gate
  status;
- a source path panel from README to TeX registry to claim boundaries;
- a short "safe summary / unsafe summary" section; and
- a visual distinction between public interpretation and scoped benchmark
  material.

Visual strategy: `layered_architecture`, `source_matrix`, or
`process_timeline`.

Acceptance emphasis:

- no completed-derivation claim;
- no global no-go claim beyond registered negative results;
- no promotion of speculative ontology language into accepted physics.

### Page: AEther-Flow Ontology

Recommended filename family: `aether-flow-ontology-explainer`.

Document type: `concept_explainer`.

Reader job: understand the ontology vocabulary and its limits without
mistaking ontology-adjacent prose for a complete GR derivation.

Source basis:

- `ontology/aether-and-aether-flow.md`
- `ontology/aether_flow_interpretation-lemen.md`
- `ontology/README.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `AGENTS.md`

GitHub-facing Markdown must cover:

- `AEther`, `AEther-flow`, observed three-dimensional space, `S-time`, and
  observed expansion as ontology vocabulary;
- gravity-as-reorganization language as heuristic unless a TeX source states a
  stronger claim;
- live `ontology/` versus archival `legacy_ontology/`;
- current missing derivational layer: source construction of observer
  normal/readout or equivalent source-side bridge;
- why older three-dimensional aether intuitions are not the model; and
- source authority hierarchy for ontology claims.

HTML must cover:

- a concept map of ontology vocabulary and caution labels;
- a live-versus-legacy source comparison;
- a "model, mathematics, prediction" separation panel; and
- a short edge-case section for over-literal fluid analogies.

Visual strategy: `bespoke_mermaid_diagram`, `layered_architecture`, or
`annotated_table`.

Acceptance emphasis:

- no ontology promotion;
- no claim that the ontology has already forced GR;
- no use of generated wiki or PDF as independent ontology source.

## Phase 2: Derivation Burdens, Gates, And Negative Results

Goal: explain the controlled derivation frontier without converting
draft/control work into public scientific authority.

Recommended packet order:

1. Phase 2A: `gr-derivation-roadmap-explainer`.
2. Phase 2B: `claim-gates-explainer`.

### Page: GR Derivation Roadmap

Recommended filename family: `gr-derivation-roadmap-explainer`.

Document type: `decision_or_lifecycle_guide`.

Reader job: see the ordered burden chain from source ontology through
benchmark promotion and understand where current research is blocked or
draft/control.

Source basis:

- `research_control/design/gr_derivation_burden_map.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `research_control/README.md`
- `AGENTS.md`

GitHub-facing Markdown must cover:

- each milestone in the burden map;
- current status categories such as `not started`, `draft object exists`,
  `blocked by missing primitive`, `human-gated`, and `frozen negative`;
- the required `target_derivation_milestone` and `milestone_burden` fields for
  future physics AgentJobs;
- the mathematical payload rule;
- source-extension and finite toy model categories;
- why validation status is not physics evidence; and
- where to find the Distance-to-GR ledger.

HTML must cover:

- a milestone ladder with status chips;
- a burden-versus-evidence matrix;
- a current-frontier caution panel that preserves `Resp_lc`, `M_src`, and
  `AtlasGlue_src^+` qualifiers if those terms are included; and
- a freeze-criteria explanation that avoids global no-go inflation.

Visual strategy: `process_timeline`, `state_model`, or `source_matrix`.

Acceptance emphasis:

- no page-local update to physics status;
- no completed bridge, `g_eff`, matter coupling, Einstein-equation, or
  benchmark-promotion claim;
- volatile current-frontier statements must cite tracked control sources.

### Page: Claim Gates, Negative Results, And Freeze Criteria

Recommended filename family: `claim-gates-explainer`.

Document type: `comparison_or_boundary_map`.

Reader job: understand how proposals, refutations, audits, freeze labels, and
human gates prevent overclaiming.

Source basis:

- `AGENTS.md`
- `research_control/README.md`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- relevant completion records only when the packet explicitly names them

GitHub-facing Markdown must cover:

- proposal, audit, refutation, stress test, completion, handoff, and gate
  concepts;
- negative-result preservation as scientific discipline, not project failure;
- freeze criteria and scoped obstruction language;
- Gate Chair as human-gated and not auto-executed;
- difference between rejected draft/control packet and broad rejection of the theory;
  and
- examples of unsafe phrase inflation.

HTML must cover:

- a claim-lifecycle state model;
- a scoped-obstruction versus global-no-go comparison;
- an "allowed claim / forbidden claim" table from the claim boundary registry;
  and
- a source-first checklist for summarizing failed lines.

Visual strategy: `state_model`, `decision_tree`, or `annotated_table`.

Acceptance emphasis:

- no Gate Chair verdict;
- no unregistered claim boundary;
- no conversion of freeze labels into broad theory rejection.

## Phase 3: Research-Control Operation

Goal: make the governed research-agent workflow understandable to maintainers
and future agents without expanding any role or AgentJob authority.

Recommended packet order:

1. Phase 3A: `research-agent-workflow-explainer` and
   `director-agentjob-lifecycle-explainer`.
2. Phase 3B: `parent-child-synthesis-explainer` and
   `role-routing-explainer`.
3. Phase 3C: decide whether `research-control-system-explainer` is needed as
   a standalone operator page or should remain merged into Phase 3A pages.

### Page: Research-Agent Workflow

Recommended filename family: `research-agent-workflow-explainer`.

Document type: `workflow_guide`.

Reader job: understand how the project routes bounded scientific and
project-system work through source-first control records.

Source basis:

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `registries/AGENT_ROLE_REGISTRY.csv`

GitHub-facing Markdown must cover:

- two linked missions and why the agent system exists;
- continuation versus project-system improvement;
- one bounded AgentJob per invocation;
- memory preflight as navigation, not authority;
- role contracts and execution-role records;
- validators as boundary checks, not scientific verdicts; and
- how humans stay responsible for gates and public release.

HTML must cover:

- a workflow map from user request to classification, routing, AgentJob,
  validation, completion, and handoff;
- a lane split between physics continuation and project-system improvement;
- a boundary panel for generated artifacts; and
- a compact "when to stop" decision tree.

Visual strategy: `process_timeline`, `decision_tree`, or
`layered_architecture`.

Acceptance emphasis:

- no autonomous-proof claim;
- no role authority expansion;
- no claim that external retrieval layers override tracked control state.

### Page: Director Decisions And AgentJob Lifecycle

Recommended filename family: `director-agentjob-lifecycle-explainer`.

Document type: `decision_or_lifecycle_guide`.

Reader job: know how Director Decision Records, AgentJobs, execution roles,
completion records, handoffs, and registries fit together.

Source basis:

- `research_control/README.md`
- `research_control/AGENTS.md`
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`

GitHub-facing Markdown must cover:

- lifecycle stages and immutable-after-creation records;
- allowlists, validators, claim boundaries, and stop conditions;
- relation between task, DDR, AgentJob, execution role, completion, and
  handoff;
- when superseding is required instead of editing;
- why a completion record is evidence for a transaction, not broad proof; and
- common operator mistakes.

HTML must cover:

- a lifecycle state diagram;
- a record-type matrix;
- an allowlist and validation checklist; and
- examples of safe versus unsafe edits.

Visual strategy: `state_model` or `process_timeline`.

Acceptance emphasis:

- no edits to schemas or task behavior during page migration unless separately
  authorized;
- no implied permission to mutate historical control records.

### Page: Parent-Child Parallel Synthesis

Recommended filename family: `parent-child-synthesis-explainer`.

Document type: `concept_explainer`.

Reader job: understand the `parent_child_parallel_synthesis` execution mode
without mistaking child outputs for separate AgentJobs or extra authority.

Source basis:

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `research_control/AGENTS.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `registries/AGENT_JOB_REGISTRY.csv`
- relevant validated completion examples when selected by the packet

GitHub-facing Markdown must cover:

- the external invariant: one Director decision, one outer AgentJob, one
  execution-role record, one completion record, one fused output;
- inherited authority, allowlists, claim boundaries, validators, and stop
  conditions;
- child outputs as supporting draft/control artifacts;
- how unresolved parent-child conflict blocks PASS completion; and
- why this mode is not a route around conflict review.

HTML must cover:

- a two-lane parent/child execution diagram;
- an invariant checklist;
- a conflict-resolution panel; and
- a "not separate AgentJobs" warning.

Visual strategy: `bespoke_mermaid_diagram`, `state_model`, or
`annotated_table`.

Acceptance emphasis:

- no route around one-job rule;
- no child-output authority inflation;
- no claim that all future non-physics work uses this mode.

### Page: Role Routing And Execution Contracts

Recommended filename family: `role-routing-explainer`.

Document type: `reference_catalog`.

Reader job: know how registered roles, task overlays, provisional roles, and
execution-role records constrain actual work.

Source basis:

- `research_control/README.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `.agents/schemas/ROLE_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- active role contracts under `.agents/roles/`

GitHub-facing Markdown must cover:

- registered role versus task overlay versus one-job provisional role;
- active physics roles and active research-ops roles;
- role authority level and may/may-not fields;
- recurring provisional-role review as project-system signal;
- why role presence does not expand a current AgentJob allowlist; and
- where to inspect the execution-role record for the actual job.

HTML must cover:

- a role matrix with authority, outputs, validators, and gate status;
- a routing decision table;
- a provisional-role lifecycle note; and
- a warning against template-by-convention promotion.

Visual strategy: `role_matrix` or `decision_tree`.

Acceptance emphasis:

- no role registration changes;
- no role authority expansion;
- no omission of human-gated status for Gate Chair.

### Merge Decision: Research Control System

Historical filename family: `research-control-system-explainer`.

Recommendation: defer as a standalone page until after Phase 3A. Its content
overlaps strongly with `research-agent-workflow-explainer` and
`director-agentjob-lifecycle-explainer`.

Create it only if review finds a remaining reader job that is not covered:
"operate the `research_control/` directory itself as a reference surface." If
created, make it an operator guide focused on directories, registries,
validation commands, and immutable-record rules, not a third generic workflow
overview.

## Phase 4: Project-System And Publication Machinery

Goal: explain how non-physics project-system work is classified, routed,
validated, and published without giving documentation surfaces authority.

Recommended packet order:

1. Phase 4A: `project-system-improvement-explainer`.
2. Phase 4B: `documentation-curator-publication-process-explainer`.
3. Phase 4C: `validator-operator-workflow-explainer`.

### Page: Project-System Improvement Loop

Recommended filename family: `project-system-improvement-explainer`.

Document type: `workflow_guide`.

Reader job: know how documentation drift, control drift, validator gaps,
memory issues, and routing ambiguity become bounded project-system work.

Source basis:

- `AGENTS.md`
- `research_control/README.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/resolve_project_improvement.py`
- `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`
- `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`

GitHub-facing Markdown must cover:

- classification before routing;
- current Git diff versus registered open signals;
- advisory resolver status;
- signal type registry and signal instance registry;
- one bounded AgentJob per invocation;
- documentation-impact receipts; and
- evidence requirements for resolved signals.

HTML must cover:

- a signal-to-AgentJob flow;
- a classifier/resolver/gate comparison table;
- a resolution evidence checklist; and
- failure modes such as orphan signals or missing documentation impact.

Visual strategy: `process_timeline`, `decision_tree`, or `source_matrix`.

Acceptance emphasis:

- no physics continuation;
- no signal resolution without evidence;
- no resolver output treated as hard checkpoint gate by itself.

### Page: Documentation Curator Publication Process

Recommended filename family:
`documentation-curator-publication-process-explainer`.

Document type: `workflow_guide`.

Reader job: understand how public pages are planned, briefed, written,
reviewed, and validated under the active publication process.

Source basis:

- `research_control/design/documentation_curator_publication_process.md`
- `.agents/roles/research_ops/documentation-curator.v2.0.0.md`
- `markdown/publication-briefs/README.md`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `scripts/validate_publication_process.py`
- `research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md`
- `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md`

GitHub-facing Markdown must cover:

- publication brief as quality control surface;
- document types and page-local headings;
- medium-specific divergence between GitHub Markdown and HTML;
- visual strategy as reader-specific, not mandatory decoration;
- pilot-first discipline and explicit approval before new page packets;
- screenshot QA and before/after review; and
- retirement of Visual Atlas, topic-registry creation path, and active
  teaching-packet fallback.

HTML must cover:

- a publication lifecycle from brief to review evidence;
- a document-type palette;
- a "do not migrate this way" anti-pattern panel; and
- a review checklist anchored to source authority.

Visual strategy: `process_timeline`, `annotated_table`, or `decision_tree`.

Acceptance emphasis:

- old `documentation-curator-teaching-loop-explainer` should not return as an
  active page. If teaching artifacts are discussed, they are historical or
  non-authoritative support only.
- no revival of old universal section headings;
- no validation-as-quality overstatement.

### Page: Validator And Operator Workflow

Recommended filename family: `validator-operator-workflow-explainer`.

Document type: `contributor_operator_guide`.

Reader job: run the correct validation chain for documentation, memory,
project-control, and research-control work.

Source basis:

- `README.md`
- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `scripts/README.md`
- `tests/README.md`
- `scripts/validate_publication_process.py`
- `scripts/project_control/validate_documentation_impact.py`
- `scripts/research_control/validate_research_control.py`

GitHub-facing Markdown must cover:

- validation by change type;
- bootstrap versus validate-only;
- publication validation;
- documentation-impact validation;
- research-control validation and `--check-diff`;
- unit-test trigger conditions;
- Playwright screenshot evidence for HTML; and
- what validator PASS does and does not mean.

HTML must cover:

- a command matrix;
- a troubleshooting guide for common failures;
- a "when to run tests" decision tree; and
- an evidence checklist for final review.

Visual strategy: `decision_tree`, `annotated_table`, or `process_timeline`.

Acceptance emphasis:

- no new validator behavior;
- no obsolete validator commands from retired Visual Atlas flow;
- no claim that validators certify scientific truth or publication taste.

## Phase 5: Memory, Registries, Roles, And Operator Reference

Goal: provide durable reference pages for the repository's agent-queryable
memory and role/tool catalogs without replacing the registries themselves.

Recommended packet order:

1. Phase 5A: `memory-system-explainer`.
2. Phase 5B: `roles-and-skills-explainer`.
3. Phase 5C: `technical-requirements-explainer`.

### Page: Memory, Registries, Wiki, And Retrieval Surfaces

Recommended filename family: `memory-system-explainer`.

Document type: `reference_catalog`.

Reader job: understand how source registries, wiki notes, content semantics,
Obsidian vault mirrors, and local retrieval relate to authority.

Source basis:

- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/WIKI_ARTIFACT_REGISTRY.csv`
- `registries/OBSIDIAN_VAULT_REGISTRY.csv`
- `registries/CONTENT_SEMANTIC_REGISTRY.csv`
- `FOLDER_MAP.md`

GitHub-facing Markdown must cover:

- source-first memory principle;
- registry rows as canonical routing/provenance/memory metadata;
- generated wiki notes as derivative metadata;
- Obsidian and SQLite retrieval as local non-authority layers;
- memory preflight requirements for future AgentJobs;
- freshness warnings as warnings, not source authority; and
- bootstrap regeneration boundaries.

HTML must cover:

- a source-to-derivative relationship graph;
- an authority-colored layer diagram;
- a query workflow panel; and
- a stale-local-retrieval troubleshooting section.

Visual strategy: `layered_architecture`, `source_matrix`, or
`bespoke_mermaid_diagram`.

Acceptance emphasis:

- no `.local` or Obsidian authority promotion;
- no generated wiki hand edits;
- no replacement of source inspection with memory lookup.

### Page: Roles And Skills Catalog

Recommended filename family: `roles-and-skills-explainer`.

Document type: `reference_catalog`.

Reader job: find active role and skill responsibilities without treating the
catalog as a role contract.

Source basis:

- `registries/AGENT_ROLE_REGISTRY.csv`
- active role contracts under `.agents/roles/`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/SKILL.md`

GitHub-facing Markdown must cover:

- active versus superseded roles;
- physics roles and research-ops roles;
- skill entry points and what they own;
- default validators by role;
- human-gated roles;
- where real authority lives; and
- why this page is a navigation catalog only.

HTML must cover:

- a searchable-looking but static role matrix;
- active/superseded grouping;
- a skill-to-workflow map; and
- cautions against using a catalog as current execution authority.

Visual strategy: `role_matrix` or `annotated_table`.

Acceptance emphasis:

- no role status changes;
- no hidden replacement of `AGENT_ROLE_REGISTRY.csv`;
- no stale superseded role presented as active.

### Page: Technical Requirements

Recommended filename family: `technical-requirements-explainer`.

Document type: `contributor_operator_guide`.

Reader job: know what environment is required for inspection, validators,
memory refresh, HTML screenshot QA, PDF work, and governed Codex-agent
operation.

Source basis:

- `README.md`
- `requirements.txt`
- `Makefile`
- `scripts/README.md`
- `tests/README.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/pdf-derivative-build/SKILL.md`

GitHub-facing Markdown must cover:

- requirement tiers: read-only inspection, governed Codex workflow, Python
  validators, memory/wiki regeneration, HTML screenshot QA, PDF builds;
- `.venv` usage and `requirements.txt`;
- Makefile targets and validator commands;
- Node/Playwright only where diagram or screenshot workflows require them;
- Codex app as current harness, not scientific authority; and
- local retrieval tools as optional support.

HTML must cover:

- an environment tier table;
- command blocks grouped by task;
- troubleshooting notes for missing dependencies; and
- a boundary panel separating tool availability from authority.

Visual strategy: `annotated_table` or `troubleshooting_guide`.

Acceptance emphasis:

- no permanent harness lock-in claim;
- no unsupported future harness parity claim;
- no dependency additions by documentation alone.

## Phase 6: Optional Or Deferred Surfaces

These pages are not recommended for immediate migration. They should be
created only if a specific reader job remains uncovered after Phases 1 through
5.

| Candidate | Recommendation | Reason |
| --- | --- | --- |
| `research-control-system-explainer` | Defer or merge. | Most content belongs in research-agent workflow and Director/AgentJob lifecycle pages. |
| `documentation-curator-teaching-loop-explainer` | Do not migrate under this name. | Teaching-loop creation path is retired as active public-page process. Replace with Documentation Curator Publication Process page. |
| Visual Atlas process page | Do not migrate. | Superseded process; cite only as historical if needed. |
| Legacy Ontology Snapshot page | Optional later. | Useful only if readers repeatedly confuse `legacy_ontology/` with live ontology. |
| Folder Map / Repository Navigator page | Optional later. | `README.md`, `FOLDER_MAP.md`, and Project Overview may be sufficient. |
| Current Frontier Status page | Defer. | High drift risk. Create only from stable tracked control sources and use explicit date/status boundaries. |

## Corpus Coverage Matrix

| Project function | Required public coverage | Page family |
| --- | --- | --- |
| Repository front door | Already covered. | `project-overview-explainer` |
| Source authority and derivatives | Already covered. | `source-authority-explainer` |
| Physics program status | Required. | `aether-flow-physics-program-explainer` |
| Exact-GR benchmark boundary | Required. | `exact-gr-benchmark-boundary-explainer` |
| Ontology vocabulary and limits | Required. | `aether-flow-ontology-explainer` |
| Derivation milestone burdens | Required. | `gr-derivation-roadmap-explainer` |
| Claim gates and negative results | Required. | `claim-gates-explainer` |
| Research-agent workflow | Required. | `research-agent-workflow-explainer` |
| AgentJob lifecycle | Required. | `director-agentjob-lifecycle-explainer` |
| Parent-child synthesis | Required while this is the default physics mode. | `parent-child-synthesis-explainer` |
| Role routing and execution contracts | Required. | `role-routing-explainer` |
| Project-system improvement | Required. | `project-system-improvement-explainer` |
| Publication process | Required. | `documentation-curator-publication-process-explainer` |
| Validation and operator commands | Required. | `validator-operator-workflow-explainer` |
| Memory, wiki, registries, local retrieval | Required. | `memory-system-explainer` |
| Roles and skills catalog | Required. | `roles-and-skills-explainer` |
| Technical requirements | Required if the repo is shared with operators. | `technical-requirements-explainer` |
| Research-control directory reference | Deferred or merged. | `research-control-system-explainer` |
| Retired teaching loop | Retired as active page. | No direct migration. |

## Recommended Next Packet

The logical next packet is Phase 1A:

1. `exact-gr-benchmark-boundary-explainer`
2. `aether-flow-physics-program-explainer`

Reasoning: these two pages reduce the highest public misunderstanding risk.
They establish the distinction between benchmark adoption, physics program
status, and open derivation before later pages discuss ontology vocabulary,
derivation roadmaps, current obstructions, or agent workflow.

Phase 1A should not include the ontology page. The ontology page is valuable,
but it is safer after the benchmark boundary page makes adoption versus
derivation explicit.

## Phase Execution Checklist

For each approved packet:

1. Confirm the exact pages in scope.
2. Run memory preflight and inspect the canonical sources named by memory hits.
3. Re-read the active publication process, active Documentation Curator role,
   and current publication brief registry.
4. Draft page-specific publication briefs.
5. Add publication brief registry rows with `migration_status` no higher than
   `publication_brief_drafted` until outputs exist.
6. Draft or update Markdown source specs.
7. Author GitHub-facing Markdown as native articles.
8. Author tracked HTML as standalone no-network pages.
9. Capture desktop and mobile screenshots.
10. Write before/after review artifacts.
11. Raise migration status only after review evidence exists.
12. Refresh bootstrap-generated registries, wiki notes, folder map, and local
    retrieval surfaces as required by the active toolchain.
13. Run validators.
14. Summarize residual risks and the next packet.

## Stop Conditions

Stop before writing or promoting a page if:

- the page would need canonical ontology edit or ontology adoption;
- the page would need benchmark promotion or Gate Chair verdict;
- the page would depend on generated wiki, HTML, PDF, Obsidian, semantic
  extract, or `.local` cache as authority;
- the page would revive the retired topic-registry or teaching-packet creation
  path;
- the page would require external runtime in tracked HTML;
- the page would create a public current-frontier claim without a stable
  tracked source and explicit date/status boundary;
- the packet would exceed the approved page count; or
- validation fails.

## References

The AEther-Flow Research Project. (2026, June 18). *AGENTS.md* [Root project
guidance]. `AGENTS.md`.

The AEther-Flow Research Project. (2026, June 18). *Documentation Curator
Publication Process* [Internal project-control design note].
`research_control/design/documentation_curator_publication_process.md`.

The AEther-Flow Research Project. (2026, June 18). *Documentation Curator
v2.0.0* [Role contract].
`.agents/roles/research_ops/documentation-curator.v2.0.0.md`.

The AEther-Flow Research Project. (2026, June 18). *GR Derivation Burden Map*
[Internal project-control design note].
`research_control/design/gr_derivation_burden_map.md`.

The AEther-Flow Research Project. (2026, June 18). *Publication Brief
Registry* [Control registry]. `registries/PUBLICATION_BRIEF_REGISTRY.csv`.

The AEther-Flow Research Project. (2026, June 18). *Publication Process
Requirement Audit* [Task artifact].
`research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md`.

The AEther-Flow Research Project. (2026, June 18). *Research Control*
[Internal project-control documentation]. `research_control/README.md`.
