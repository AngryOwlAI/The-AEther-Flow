<!-- authority: explanatory -->
---

# The Æther-Flow Interpretation of Relativity Research Project

---

<p align="center">
  <img src="assets/images/readme-banner.png" alt="Editorial cosmic banner for The Æther Research Program with the subtitle 'Ontology, exact-GR benchmark package, open derivation program, and AI research-agent system.'" width="100%" />
</p>

---

## The Research Program

The The Æther-Flow Interpretation of Relativity Research Program is a dual physics-and-AI research project.

The physics track studies whether ordinary general relativity can be interpreted, and eventually derived, from a deeper four-dimensional `Æther` / `Æther-flow` ontology. The current public benchmark keeps GR exactly at observable scale. A first-principles derivation of GR from the ontology remains open.

The AI research-agent track currently develops and tests a human-scaffolded research-agent system for theoretical physics: agent roles, routing rules, claim gates, manuscript tools, result handling, review discipline, and scientific memory. Its long-term technical goal is staged autonomy toward an autonomous theoretical-physics research system, while public release, authorship responsibility, and external outreach remain human-accountable under current governance.

### The Two Tracks

#### Physics track

- Public benchmark: an exact-GR interpretive package for `The Æther-Flow Interpretation of Relativity`.
- Current observable scale: ordinary GR, one operative metric, universal matter coupling, standard causal structure.
- Open burden: deriving the benchmark from explicit substrate structure, with effective Lorentzian metric generation as the first proof milestone.
- Negative result: the frozen derivation line is preserved under `Not Derived On Current Line`.

#### AI research-agent track

- Currently human-scaffolded AI workflow for theoretical physics research, with staged autonomy as the long-term AI-system ambition.
- Role-based routing through candidate intake, refutation, defense, gate decisions, and integration notes.
- Manuscript-centered memory through active `.tex`, PDFs, CSV routing, and the Manuscript Wiki.
- Support for exploring, testing, refuting, proving, accepting, and organizing candidate derivation steps without treating workflow status as physics proof.
- Explicit separation between physics claims, AI-methodology claims, tooling claims, open problems, and stopped results.
- A project-system improvement loop for documentation drift, validators, roles,
  schemas, memory tooling, and operational reliability.

#### How they co-develop

The physics problem gives the AI system a hard, real research environment. The AI research-agent system gives the physics program disciplined ways to explore ideas, reject failed mechanisms, preserve negative results, and avoid overclaiming. The shared target is stronger than organization alone: derive GR from the `Æther` / `Æther-flow` ontology if the required gates can actually be passed.

```text
                          THE ÆTHER-FLOW RESEARCH PROGRAM
                                      |
              +-----------------------+-----------------------+
              |                                               |
      PHYSICS RESEARCH TRACK                         AI RESEARCH-AGENT TRACK
              |                                               
  Æther / Æther-flow ontology                    
              |                                               
  Exact-GR benchmark package                     
              |                                               
  Open GR-derivation problem                     
              |                                               
  No-go and obstruction record                   
```

---

## This repo

This repo is a reset of the research program: [The Æther GR Derivation](/Volumes/P-SSD/AngryOwl/The Æther GR Derivation/) as the research system was failing to derive GR from the ontology or hard-fail the derivation, so we need to start over with a new approach.
The goal of this research program is to improve itself using the lessons learned from the previous attempt and ultimately derive GR from the Æther Flow ontology.

---

## The Æther Flow Ontology

[...]

---

## The research-agent system

[...] 

---

## Requirements

<!-- authority: control -->

### Python environment

This repository uses a local Python virtual environment for scripts.

- Runtime: Python 3.12.13 in `.venv/`
- Dependency file: `requirements.txt`
- Environment directory: `.venv/`, ignored by `.gitignore`
- Current dependency status: PyMuPDF is used for direct PDF text extraction in
  the local semantic memory system.

Create or refresh the environment from the repository root:

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run scripts with the active environment:

```zsh
python path/to/script.py
```

Or run scripts without activating the shell:

```zsh
.venv/bin/python path/to/script.py
```

When a Python script requires an external package, add one package per line to
`requirements.txt`, then rerun:

```zsh
.venv/bin/python -m pip install -r requirements.txt
```

---

## Memory, wiki, and registry system

This repository uses a source-first memory system for project knowledge.

Authority order:

1. Registered `.tex` files are canonical for physics research and derivational claims.
2. Format-specific CSV registries are canonical for routing, provenance, generated-output tracking, and agent-queryable memory.
3. Registered Markdown files are canonical for GitHub documentation, agent guidance, and project-control notes.
4. PDFs, wiki notes, wiki indexes, master registries, and HTML explainers are generated derivatives.

Generated artifacts are tracked when they are part of the project memory surface, but they are not independent authority. Update the source file and registry row, then regenerate.

Registered Markdown sources include front-door docs, scoped agent guidance,
role contracts, schema contracts, skill contracts, key research-control design
notes, ontology-adjacent explanatory notes, and Markdown source specs for
generated HTML explainers.

Tracked HTML explainers are human-only generated derivatives. A tracked
`html/*.html` file is valid only when it is backed by a registered Markdown
source spec under `markdown/html-explainer-specs/` with `title`, `purpose`,
`audience`, `output_path`, `renderer_skill`, `source_materials`,
`claim_boundary`, and `human_visual_only: true`. Modify the spec first, then
regenerate the HTML output.

Bootstrap or refresh the memory system:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

Validate without writing:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Run smoke tests:

```zsh
.venv/bin/python -m unittest discover -s tests
```

Run the full memory-system acceptance chain, including generated memory refresh,
local vault sync, linting, tests, and query smoke checks:

```zsh
make validate-memory
```

Initialize and sync the local Obsidian memory vault:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/sync_obsidian_vault.py
```

Query the combined CSV, relationship, vault, and content-semantic memory system:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
```

Clean ignored local noise from canonical lanes:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/clean_local_noise.py --dry-run
```

---

## Research-control workflow

Research-control continuation is tracked under `research_control/`. Use
`.codex/skills/continue-research/SKILL.md` as the entry point.

## Project-system improvement workflow

Project-system improvement is tracked separately from physics continuation.
Use `.codex/skills/improve-project-system/SKILL.md` when a change affects
roles, schemas, validators, checkpoint gates, memory tooling, control-marked
skill guidance, project-control documentation, or generated-doc pipelines.

Mixed Markdown files use authority markers. Explanatory sections describe
current behavior without changing obligations. Control sections change or define
agent behavior, routing, authority, validator expectations, allowed paths,
commands, schemas, stop conditions, or workflow gates.

Decision vocabulary:

| Term | Use when | Authority and outputs | Boundary |
| --- | --- | --- | --- |
| `continue-research` | Continue physics research-control from tracked state, handoffs, and the active task boundary. | Uses `.codex/skills/continue-research/SKILL.md`; may route one bounded research AgentJob through the Director-controlled control spine. | Does not repair project-system machinery unless the routed task explicitly allows it. |
| `improve-project-system` | Repair or clarify the research system itself: roles, schemas, validators, checkpoint gates, memory tooling, skill guidance, docs, or generated-doc pipelines. | Uses `.codex/skills/improve-project-system/SKILL.md`; may resolve one signal, one classifier result, or one bounded project-system AgentJob. | Does not perform physics derivation, promote claims, or edit canonical science sources. |
| Project-System Director | A project-system boundary or routing question must be resolved before work proceeds. | Creates a project-system Director Decision Record and selects one bounded non-scientific AgentJob. | Does not execute the selected job or expand role authority by convention. |
| Documentation Curator | Explanatory documentation, documentation registries, documentation-source specs, source-backed human HTML explainers, or documentation-impact receipts drift from current machinery. | Updates allowed explanatory Markdown, `markdown/html-explainer-specs/*.md`, spec-backed `html/*.html` derivatives, and documentation-impact records when required. | Does not change control contracts, workflow commands, routing, validators, permissions, scientific claim status, or HTML as independent authority. |
| Project-Control Maintainer | Skill contracts, role contracts, schema contracts, control registries, or control-marked mixed Markdown need functional maintenance. | Edits allowed control markdown and project-control contracts under one AgentJob allowlist. | Does not edit explanatory-only sections unless a task overlay explicitly grants `explanatory_markdown` permission. |
| Validator Engineer | Deterministic validator, checkpoint gate, or test behavior is missing, unclear, or incorrect. | Edits allowed validator scripts, tests, documented validator contracts, and registry rows. | Does not use model judgment as a validator substitute or decide human policy questions. |
| Memory-System Maintainer | Source-first memory, wiki, registry, Obsidian, query, or derivative metadata tooling needs maintenance. | Edits allowed memory-system scripts, registry generation rules, query tooling, and related skill documentation. | Does not make generated artifacts authoritative or alter claim-promotion semantics. |

Classify current Git changes:

```zsh
.venv/bin/python scripts/project_control/classify_project_changes.py --json
```

Resolve the next bounded project-system action:

```zsh
.venv/bin/python scripts/project_control/resolve_project_improvement.py --json
```

Resolver output is advisory routing state. Checkpoint blocking is defined by
validator failures and concrete authority-boundary violations, not by the
resolver seeing future work. Completion records do not need a fresh resolver
snapshot just because high or critical signals remain open; resolver snapshots
are optional handoff context unless the AgentJob sets
`resolves_signal_routing: true`. Routing-resolution completions must preserve
repo-relative `resolver_snapshots.before` and `resolver_snapshots.after`
paths to JSON output from `resolve_project_improvement.py --json` and include
nonblank `routing_delta_summary`. The hard validator checks only summary
presence and minimal resolver-shape fields: the advisory flags, checkpoint
gate source, selected signal, open signals, and change classification.
Ordinary validator and documentation jobs do not inherit that burden.

Validate documentation impact:

```zsh
.venv/bin/python scripts/project_control/validate_documentation_impact.py
```

Project-improvement signal types are defined in
`registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`; concrete emitted
signals are recorded in `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.
The type registry owns allowed signal kinds and default routing metadata.
Severity remains on the concrete signal instance because the same signal type
can be low or critical depending on the transaction context and concrete
conflict.
A project-system AgentJob should execute at most one bounded improvement and write
`research_control/tasks/<task_id>/documentation_impact.yaml` when the
transaction changes project-system sources. Source-doc-only handling is valid
only for plain documentation edits outside a project-system AgentJob.
Registered high/critical signals are routed before current Git-change work;
registered low/medium signals remain backlog unless no current project-system
action is pending. Documentation-impact records are mechanically checked:
source changes, generated derivatives, classifier reason codes, and required
validators must match the live transaction.
Signal rows that leave the open backlog by moving to `resolved`, `completed`,
`closed`, or `rejected` must include `resolved_by_job_id`,
`resolution_evidence_path`, and `resolved_at`; otherwise future work can be
erased without a bounded AgentJob receipt. For `resolved`, `completed`, and
`closed`, `resolution_evidence_path` must point to a completion YAML with
`validation_status: "PASS"` and a matching `job_id`. For `rejected`, it may
instead point to a Director decision record that names the signal and explains
the rejection. Signal rows do not duplicate validator command strings; the
referenced completion record owns command evidence through `command_results`.
One bounded AgentJob may close multiple project-improvement signals only when
its `objective` names every closed signal ID and its completion record lists
the same IDs in `resolved_project_improvement_signals` with a nonblank
`coherent_resolution_summary`. For shared closures, every signal row must use
the resolving job's canonical `completion_path` from
`registries/AGENT_JOB_REGISTRY.csv` as `resolution_evidence_path`.

Validate that completion or handoff-emitted signals are represented in the
canonical registry:

```zsh
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
```

Signal detection is structural: completion and handoff YAML files are parsed
for nonblank `project_improvement_signals` entries, and signal types are read
from the canonical type registry rather than duplicated local constant sets.

---

## Project map

```
.
├── .agents/
│   ├── roles/
│   └── schemas/
├── .codex/
│   ├── prompts/
│   │   └── Repo-local prompt templates for visual explanations and reviews.
│   └── skills/
│       ├── project-memory-system/
│       │   └── scripts/
│       ├── improve-project-system/
│       ├── grill-me/
│       ├── markdown-wiki/
│       ├── tex-wiki/
│       ├── pdf-derivative-build/
│       ├── obsidian-wiki/
│       ├── html-visual-explainer/
│       ├── ontology-promotion/
│       └── visual-explainer/
├── AGENTS.md
│   └── Root instructions for research agents working in this repository.
├── LICENSE
│   └── Project license.
├── Makefile
│   └── Single-command validation wrappers for repository operators.
├── README.md
│   └── Project overview, environment setup, and file map.
├── requirements.txt
│   └── Python dependency ledger for repository scripts.
├── assets/
│   └── images/
│       ├── readme-banner.png
│       └── readme-banner-old*.png
├── html/
│   └── Generated human-only visual explainers backed by Markdown specs.
├── markdown/
│   ├── grill-memory-wiki-registry-design-handoff.md
│   ├── html-explainer-specs/
│   │   └── Source specs for tracked human-only HTML explainers.
│   └── ontology-promotions/
├── manuscripts/
│   ├── tex/
│   └── pdfs/
├── ontology/
│   ├── aether-and-aether-flow.md
│   ├── tex/
│   └── pdfs/
├── registries/
│   ├── AGENT_ROLE_REGISTRY.csv
│   ├── AGENT_JOB_REGISTRY.csv
│   ├── DIRECTOR_DECISION_REGISTRY.csv
│   ├── RESEARCH_TASK_REGISTRY.csv
│   ├── CLAIM_BOUNDARY_REGISTRY.csv
│   ├── MARKDOWN_SOURCE_REGISTRY.csv
│   ├── TEX_SOURCE_REGISTRY.csv
│   ├── PDF_DERIVATIVE_REGISTRY.csv
│   ├── HTML_EXPLAINER_REGISTRY.csv
│   ├── PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv
│   ├── PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv
│   ├── WIKI_ARTIFACT_REGISTRY.csv
│   ├── OBSIDIAN_VAULT_REGISTRY.csv
│   ├── CONTENT_SEMANTIC_REGISTRY.csv
│   ├── OBJECT_RELATIONSHIP_REGISTRY.csv
│   └── FILE_OBJECT_REGISTRY.csv
├── research_control/
│   └── Tracked Director decisions, AgentJobs, completions, handoffs, and templates.
├── scripts/
│   ├── project_control/
│   │   └── Project-system classifiers, resolvers, and documentation-impact validators.
│   └── research_control/
│       └── Research-control validators and continuation helpers.
├── tests/
│   └── Memory-system smoke checks.
├── tex_shared/
│   └── Shared LaTeX inputs used by ontology and manuscript TeX builds.
├── wiki/
│   ├── markdown/
│   ├── tex/
│   ├── pdf/
│   ├── html/
│   └── indexes/
└── Step-by-step-Comments/
    ├── README.md
    └── Comments - Phase-1.md through Comments - Phase-5.md
```

Local or generated files intentionally excluded from the project map include
`.venv/`, `.DS_Store`, `.local/`, and other ignored operating-system or build artifacts.
