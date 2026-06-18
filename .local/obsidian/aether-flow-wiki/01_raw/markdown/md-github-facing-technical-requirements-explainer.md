# Technical Requirements

Technical requirements are tiered by task: reading the repo, operating the current Codex app AI-agent harness, running validators, regenerating memory, rendering diagrams, using local retrieval, and refreshing PDFs do not require the same tools.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/technical-requirements-explainer.md`
- **Related HTML:** `html/technical-requirements-explainer.html`
- **Authority status:** `generated_noncanonical`

## Requirement Tiers

```mermaid
flowchart TD
  Read["Read and inspect"] --> Python["Python .venv<br/>validators and memory scripts"]
  Read --> Codex["Codex app<br/>current AI-agent harness"]
  Codex --> Python
  Python --> Bootstrap["Memory/wiki regeneration"]
  Bootstrap --> Mermaid["Node and Mermaid<br/>diagram-backed HTML"]
  Bootstrap --> Retrieval["Optional local retrieval<br/>Obsidian and SQLite"]
  Python --> Pdf["PDF refresh<br/>LaTeX tooling when needed"]
  Retrieval --> Boundary["Operator aid<br/>not project authority"]
  Mermaid --> Boundary
  Pdf --> Boundary
```

## Installation Strategy

Not every reader needs every tool. Read-only inspection needs the repository and
normal Markdown rendering. Validation and memory regeneration need the Python
environment. Diagram-backed HTML regeneration needs Node, npm, Mermaid
dependencies, and browser/rendering support. PDF refresh needs LaTeX only when
refreshing PDF derivatives.

Operating the governed AI-agent workflow currently needs the Codex app. The
repo-local `.codex/` skills, prompts, and agent configuration files are written
for that harness. This is a current operating requirement, not a claim that the
project can never move to another harness. A future custom or third-party AI
harness would need to preserve the same tracked state, role boundaries,
allowlists, validators, checkpoint discipline, and generated-derivative rules
before it should be treated as equivalent.

Start with the Python environment and `requirements.txt`, because validators
and bootstrap are central to repository consistency. Add diagram, retrieval, or
PDF tooling only for the derivative lane being regenerated. Obsidian and
global Codex plugins are operator aids unless project-local guidance or skill
contracts make them part of a tracked workflow.

## Practical Matrix

| Tier | Needed For | Source Evidence |
| --- | --- | --- |
| Read and inspect | Understanding files and source boundaries | `README.md`, `AGENTS.md` |
| Codex app harness | Reproducing the governed AI-agent workflow as practiced here | `README.md`, `.codex/skills/README.md`, `.codex/agents/README.md`, `.codex/prompts/README.md` |
| Python validators | Project-control and memory checks | `requirements.txt`, `Makefile` |
| Memory regeneration | Registries, wiki, semantic, and vault refresh | `project-memory-system` skill |
| Mermaid rendering | Governed diagram-backed HTML | Mermaid subskill and package files |
| Local retrieval | Search and local reading aids | `obsidian-wiki` and memory skill |
| PDF refresh | Human-reading PDF derivatives | `pdf-derivative-build` skill |

## Boundary Rule

A tool requirement does not create authority. The Codex app is the current operating harness for the governed AI-agent workflow, while Python, Node, Mermaid, Obsidian, LaTeX, and plugins are means of inspection, execution, or regeneration. Source files, registries, task records, and validators decide whether the result is acceptable.

## For GitHub Readers And AI Agents

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- identify which tool tier applies to a task;
- recognize the current Codex app harness boundary;
- separate project requirements from operator aids;
- find setup and skill-contract sources.

Before modifying project knowledge:
- use the relevant validator or bootstrap command;
- avoid claiming optional local tools are project authority;
- inspect source authority when tool output disagrees with tracked state.

Do not:
- require every reader to install every optional aid;
- treat Codex app availability as scientific or control authority by itself;
- treat local retrieval as canonical;
- change dependency policy through explanatory prose.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `requirements.txt`
- `Makefile`
- `.codex/skills/README.md`
- `.codex/agents/README.md`
- `.codex/prompts/README.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`
- `.codex/skills/pdf-derivative-build/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package.json`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/package-lock.json`
