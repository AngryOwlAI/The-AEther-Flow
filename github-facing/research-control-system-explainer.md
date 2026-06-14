# Research-Control System

This page explains how the project changes itself safely: classification, bounded project-system work, documentation-impact receipts, source-backed HTML rules, validators, and checkpoint gates.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/research-control-system-explainer.md`
- **Related HTML:** `html/research-control-system-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

The research-control system is the repository's governance layer for deciding how project-system and research-continuation work may proceed. Its function is to classify changes, resolve advisory routing, create or reuse one bounded AgentJob, enforce role and write-path boundaries, require documentation-impact receipts when project machinery changes, and validate that source specs, skills, roles, registries, claim boundaries, and generated derivatives remain aligned. It matters because the project deliberately combines scientific exploration with agent workflow development; without control records, generated HTML, Markdown guidance, validators, and role contracts could drift or be mistaken for scientific authority. The system fits the larger project by making improvements reversible, auditable, and separate from physics claim promotion.

## What This Feature Does

The research-control system is the governance layer for project-system and research-continuation changes. It keeps documentation changes, validator changes, role contract changes, generated derivative refreshes, project-improvement signals, and checkpoint boundaries auditable.

## Why The Project Needs It

The project is both a physics research repo and an AI research-agent system. Machinery improvements are necessary, but they must not silently promote science claims, rewrite control authority, or hand-edit generated derivatives.

## How It Works

Operator flow:

1. Classify current changes with `scripts/project_control/classify_project_changes.py --json`.
2. Resolve advisory project-system routing with `resolve_project_improvement.py --json` when applicable.
3. Create or reuse one bounded AgentJob with explicit role, paths, validators, outputs, and stop conditions.
4. Update source docs or write a documentation-impact no-op rationale when required.
5. Regenerate memory/wiki registries through bootstrap.
6. Run project-control, research-control, diff, and test validators.
7. Checkpoint only when validators pass and changed paths match the job boundary.

## What It Is Not

It is not physics continuation, not a broad rewrite license, not a permission to edit generated HTML as authority, and not a substitute for human-gated policy decisions.

## Diagram Reading Guide

The validation-flow diagram reads from source-spec update through derivative generation, Mermaid parity, bootstrap, documentation impact, research-control validation, diff gate, and checkpoint. The boundary map shows classifier, role, AgentJob, allowed writes, forbidden surfaces, validators, receipts, and registry updates.

<!-- mermaid-diagram-id: research-control-validation-flow -->
```mermaid
flowchart TD
  Spec["Markdown source spec update"] --> Html["Generated HTML derivative"]
  Html --> Mermaid["Mermaid source parity validation"]
  Mermaid --> Bootstrap["Memory bootstrap and registry refresh"]
  Bootstrap --> DocsImpact["Documentation-impact gate"]
  DocsImpact --> ResearchControl["Research-control validation"]
  ResearchControl --> DiffGate["Diff and authority boundary gate"]
  DiffGate --> Checkpoint["Local checkpoint commit"]
```

<!-- mermaid-diagram-id: control-boundary-map -->
```mermaid
flowchart TD
  Change["Proposed project-system change"] --> Classifier["Change classifier"]
  Classifier --> Role["Recommended role boundary"]
  Role --> Job["One bounded AgentJob"]
  Job --> Allowed["Allowed writes"]
  Job --> Forbidden["Forbidden authority surfaces"]
  Allowed --> Validators["Required validators"]
  Forbidden --> Stop["Stop condition"]
  Validators --> Receipt["Completion and documentation-impact receipts"]
  Receipt --> Registry["Control registries updated"]
```

## Source Authority

The control model is grounded in `AGENTS.md`, `research_control/README.md`, improve-project-system, explainer skills, documentation-curator contracts, validation scripts, and the project-memory bootstrap.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Use continue-research for physics continuation.
- Use improve-project-system for validators, roles, memory tooling, and documentation pipelines.
- Run documentation-impact validation after project-system machinery changes.
- Stop when a required policy decision exceeds the AgentJob boundary.

## All Source Materials

- `AGENTS.md`
- `README.md`
- `research_control/README.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/SKILL.md`
- `.codex/skills/visual-explainer/subskills/mermaid-documentation/SKILL.md`
- `.agents/roles/research_ops/documentation-curator.v0.4.0.md`
- `research_control/design/html_explainer_flexible_presentation_contract.md`
- `scripts/project_control/validate_documentation_impact.py`
- `scripts/research_control/validate_research_control.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
