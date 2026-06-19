# Technical Requirements For Reproducible Operation

Technical requirements are the local operating conditions that make AEther-Flow reproducible: the current Codex app harness for governed agent work, the Python virtual environment, dependency ledger, repository-owned scripts, Makefile targets, screenshot tooling, diagram tooling when needed, and managed PDF derivative path.

Those requirements answer only one question: what tools are needed to perform an operation. They do not answer whether the operation is authorized. Authorization still comes from tracked sources, registries, task records, role or skill contracts, AgentJob allowlists, completion evidence, claim boundaries, and checks.

The useful operator model is tiered. Read-only inspection has minimal requirements. Governed agent work currently assumes the Codex app and repo-local skills. Python validators need `.venv` and `requirements.txt`. HTML QA may need browser tooling. Diagram-backed tracked HTML may need the pinned Mermaid/Playwright setup. PDF derivatives use the managed TeX-to-PDF lane only when registered TeX derivatives are in scope.

Reader scope: local operation requirements only. This page cannot change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics status.

## Requirement Tier Matrix

| Item | Function | Boundary |
| --- | --- | --- |
| Read-only inspection | Browser or editor, shell, and Git. | Does not authorize source edits. |
| Governed agent workflow | Codex app plus repo-local skills and control files. | Current harness, not scientific authority. |
| Python checks | `.venv`, Python 3.12.13, `requirements.txt`, and repository scripts. | No dependency or command-semantics change. |
| Memory refresh | Project-memory bootstrap, optional Obsidian sync, and local memory index. | Generated retrieval remains non-authority. |
| HTML QA | Source spec, no-network HTML, browser screenshot tooling, and Playwright Chromium when needed. | No direct HTML-only authority. |
| PDF derivatives | Managed TeX-to-PDF build path for registered TeX derivatives. | PDFs remain human-reading derivatives. |

## Repository Command Families

| Item | Function | Boundary |
| --- | --- | --- |
| Environment | Use README and requirements before running Python scripts. | Prefer `.venv/bin/python` for receipts. |
| Memory | Use project-memory bootstrap for refresh and validate-only for checks. | Do not hand-edit generated wiki notes. |
| Project-system | Use memory preflight, classifier, resolver, signals, receipts, and research-control checks. | One bounded AgentJob. |
| Publication | Update brief/spec pair, GitHub Markdown, HTML, screenshots, review evidence, and strict checks. | Generated outputs stay derived. |
| Tests | Run unit tests when scripts, validators, schemas, roles, or memory machinery change. | Tests do not prove physics. |

## Scoped Tooling

| Item | Function | Boundary |
| --- | --- | --- |
| Node/npm | Used for diagram and Playwright-related workflows when required. | Not a general authority requirement. |
| Playwright | Captures rendered evidence for tracked HTML. | A screenshot is not a source contract. |
| Mermaid | Build-time diagram support only for tracked HTML. | No browser-side Mermaid runtime. |
| Codex app | Current governed AI-agent harness. | Not permanent lock-in or scientific authority. |

## Tool Authority Boundary

| Item | Function | Boundary |
| --- | --- | --- |
| Tool works | The local operation can run. | Still inspect the authority source. |
| Check passes | The configured deterministic check accepted the state. | Does not grant promotion or publication taste. |
| Cache exists | A generated or local retrieval layer is available. | Does not replace canonical source inspection. |

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/technical-requirements-explainer.md`
- **Related HTML:** `html/technical-requirements-explainer.html`
- **Publication brief:** `markdown/publication-briefs/technical-requirements.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains current local requirement tiers, Codex app harness assumptions, Python virtual environment setup, repository-owned command families, generated-memory refresh, screenshot QA, and PDF derivative build requirements without changing dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Codex app harness statement, Python environment, requirement tiers, and command families.]
- AEther-Flow Project. (2026). `AGENTS.md` [Authority hierarchy, memory requirement, generated-output boundaries, and required checks.]
- AEther-Flow Project. (2026). `research_control/README.md` [Memory preflight, classifier/resolver, documentation-impact, and research-control checks.]
- AEther-Flow Project. (2026). `requirements.txt` [Repository Python dependency ledger.]
- AEther-Flow Project. (2026). `Makefile` [Grouped local command targets.]
- AEther-Flow Project. (2026). `scripts/README.md` [Script groups and script authority boundary.]
- AEther-Flow Project. (2026). `tests/README.md` [Unit-test areas and commands.]
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Memory/wiki/registry refresh and validate-only modes.]
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system workflow and checks.]
- AEther-Flow Project. (2026). `.codex/skills/html-visual-explainer/SKILL.md` [Governed tracked HTML publication and screenshot QA.]
- AEther-Flow Project. (2026). `.codex/skills/visual-explainer/SKILL.md` [Visual explainer constraints and no external runtime for tracked pages.]
- AEther-Flow Project. (2026). `.codex/skills/pdf-derivative-build/SKILL.md` [Managed TeX-to-PDF derivative build lane.]

## Safe Operating Summary

Safe summary: Use the required tool tier, inspect the source path that owns the operation, confirm the current task allowlist, run the repository-owned command family, and preserve evidence.

Unsafe summary: A working tool, generated cache, screenshot, or PASS result creates source authority, changes dependencies, or authorizes physics claims.
