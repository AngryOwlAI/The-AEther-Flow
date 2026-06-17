# Project-System Improvement

Project-system improvement is the repair lane for documentation drift, validators, roles, schemas, memory tooling, generated-document pipelines, signal routing, and operational reliability.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/project-system-improvement-explainer.md`
- **Related HTML:** `html/project-system-improvement-explainer.html`
- **Authority status:** `generated_noncanonical`

## Source-Backed Summary

Project-system improvement is the repair lane for the research machinery itself. It covers documentation drift, role and schema contracts, validator behavior, memory tooling, generated-document pipelines, trigger logic, signal routing, and operational reliability. The workflow begins with source inspection and a structural classifier, then uses an advisory resolver and signal registries to decide whether one bounded AgentJob is needed. A Documentation Curator job handles explanatory documentation drift; a Project-Control Maintainer or other project-system role handles contracts, validators, schemas, or control behavior. Every state-changing project-system AgentJob must record documentation impact, regenerate the source-first memory surfaces when needed, and pass research-control validation. The loop exists so the system can improve itself without turning maintenance work into physics continuation or claim promotion.

## What This Feature Does

The improvement loop routes maintenance work through the same bounded discipline used elsewhere in the project. It classifies current changes, reads advisory resolver state, checks emitted project-improvement signals against registries, selects one bounded role and AgentJob when needed, writes documentation-impact evidence, regenerates derived surfaces, and validates the result.

## Why The Project Needs It

AEther-Flow is both a physics project and an AI research-agent project. Its documentation, validators, registries, roles, schemas, generated surfaces, and memory tools can drift as the system evolves. The improvement lane lets maintainers repair the operating system without confusing that repair with a physics result or an unrestricted repository rewrite.

## How It Works

The workflow starts with authority inspection and `classify_project_changes.py`. The resolver then gives advisory routing state. Signal validation checks that emitted signals use canonical type and instance rows. If a change is needed, one bounded AgentJob handles the selected scope. Documentation impact records what changed, what generated surfaces moved, which classifier reason codes apply, and which validators were run.

## Workflow Step Inspector

1. Inspect root guidance, research-control guidance, relevant registries, and active source surfaces.
2. Classify changed paths and reason codes.
3. Resolve advisory routing state and open project-improvement signals.
4. Route at most one bounded AgentJob to the fitting project-system role.
5. Execute only within the job allowlist and source authority boundary.
6. Record documentation impact for state-changing project-system work.
7. Regenerate derived memory, registry, HTML, wiki, or GitHub-facing surfaces through the approved path.
8. Validate the transaction before treating it as checkpoint-ready.

## What It Is Not

It is not physics continuation, not a Gate Chair process, not a permission to change roles or validators without the correct project-control role, and not a rule that advisory resolver output blocks checkpointing by itself. Hard checkpoint blockers are concrete validation failures and authority-boundary violations.

## Diagram Reading Guide

No Mermaid diagram is required for this explainer. Read the workflow as a lifecycle: classify, resolve, validate signals, route one bounded job, document impact, regenerate, validate, then checkpoint only if the transaction is coherent.

## Source Authority

Authority comes from root and research-control guidance, the `improve-project-system` skill, project-improvement signal registries, and project-control scripts. This derived Markdown does not change any signal row, validator, or routing rule.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize the project-system improvement workflow
- identify the classifier, resolver, signal, and documentation-impact files
- distinguish documentation drift from control-contract drift

Before modifying project knowledge:
- read `AGENTS.md`
- read `research_control/README.md`
- inspect the project-improvement signal registries
- route through the bounded AgentJob workflow

Do not:
- do not treat project-system repair as physics continuation
- do not change validators, schemas, roles, or routing rules through a Documentation Curator job
- do not leave documentation-impact requirements unrecorded
- do not treat advisory resolver output as stronger than validator results

## Where To Go Next

- Read research-control system for validation governance.
- Read roles and skills before changing role or skill contracts.
- Read source authority before updating generated surfaces.
- Run the classifier and documentation-impact validator before checkpointing project-system work.

## All Source Materials

- `AGENTS.md`
- `research_control/README.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`
- `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/resolve_project_improvement.py`
- `scripts/project_control/collect_project_improvement_signals.py`
- `scripts/project_control/validate_documentation_impact.py`
