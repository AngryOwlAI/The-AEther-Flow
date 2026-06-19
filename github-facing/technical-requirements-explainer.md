# Technical Requirements For Reproducible Operation

Technical requirements are the local operating conditions that make
AEther-Flow reproducible: the current Codex app harness for governed agent
work, the Python virtual environment, dependency ledger, repository-owned
scripts, Makefile targets, screenshot tooling, and PDF derivative path.

This page is a generated noncanonical reader surface. It does not change
dependencies, validators, Makefile targets, command semantics, harness policy,
role authority, routing behavior, checkpoint behavior, generated-output
authority, or physics claim status. Tool availability is support, not
permission.

## Operating Model

The repository separates three questions:

1. What tools are needed to perform a local operation?
2. Which source file or registry says that operation is valid?
3. Which task, role, AgentJob, completion record, and checks prove this
   transaction stayed inside its boundary?

The technical requirement answers only the first question. `README.md` states
that the governed research-agent workflow currently assumes the Codex app, and
that read-only inspection, normal Git use, and Python validators can still run
outside the Codex app. `AGENTS.md` and `research_control/README.md` then keep
authority with tracked sources, registries, task records, claim boundaries, and
checks.

## Requirement Tiers

| Tier | Needed tools | Repository evidence | Does not authorize |
| --- | --- | --- | --- |
| Read-only inspection | Browser or editor, shell, Git | `README.md`; `AGENTS.md` | Editing source truth, changing registries, or treating generated docs as authority. |
| Governed agent workflow | Codex app plus repo-local `.codex/` skills, prompts, and configuration | `README.md`; `.codex/skills/improve-project-system/SKILL.md` | Scientific authority, permanent harness lock-in, or future harness parity claims. |
| Python checks and scripts | `.venv`, Python 3.12.13, `requirements.txt`, repository scripts | `README.md`; `requirements.txt`; `scripts/README.md` | New dependencies, changed command semantics, or skipped documentation-impact receipts. |
| Memory and wiki refresh | Project memory bootstrap, optional Obsidian sync, local memory index | `README.md`; `.codex/skills/project-memory-system/SKILL.md`; `Makefile` | Making `.local`, wiki notes, semantic extracts, or Obsidian mirrors authoritative. |
| HTML screenshot QA | Tracked source spec, no-network HTML, browser screenshot tooling, Playwright Chromium when needed | `.codex/skills/html-visual-explainer/SKILL.md`; `.codex/skills/visual-explainer/SKILL.md` | Direct HTML-only edits, browser-side Mermaid execution, or public deployment. |
| PDF derivatives | Managed TeX-to-PDF build path for registered TeX derivatives | `.codex/skills/pdf-derivative-build/SKILL.md` | Treating PDFs as canonical scientific authority or building unregistered scratch output outside `.local/`. |
| Unit-test evidence | Python test runner and test modules | `tests/README.md`; `Makefile` | Treating tests as physics proof or as replacements for source registries. |

## Command Families

Use repository-owned command families from the source files rather than
inventing ad hoc local shortcuts.

| Work | Source path to inspect | Command family |
| --- | --- | --- |
| Python environment | `README.md`; `requirements.txt` | Create `.venv`, activate it, install from `requirements.txt`, then run scripts through `.venv/bin/python`. |
| Memory refresh | `.codex/skills/project-memory-system/SKILL.md`; `Makefile` | Run `bootstrap_memory_system.py` for refresh and `bootstrap_memory_system.py --validate-only` for read-only checks. |
| Project-system routing | `.codex/skills/improve-project-system/SKILL.md`; `research_control/README.md` | Run memory preflight, classify current Git changes, resolve advisory routing, then run required project-system checks. |
| Publication pages | `.codex/skills/html-visual-explainer/SKILL.md`; `.codex/skills/visual-explainer/SKILL.md` | Update the publication brief and source spec first, then produce GitHub Markdown, tracked HTML, screenshots, review evidence, and strict publication-process checks. |
| Tests | `tests/README.md`; `Makefile` | Run the full test suite when scripts, validators, schemas, role contracts, or memory-system machinery change. |
| PDF derivatives | `.codex/skills/pdf-derivative-build/SKILL.md` | Build only registered TeX derivatives into their managed PDF lanes; write scratch builds under `.local/`. |

## HTML And Diagram Constraints

Tracked HTML is a generated human-only derivative. The governed path is:

1. Write or update the page publication brief under `markdown/publication-briefs/`.
2. Write or update the source spec under `markdown/html-explainer-specs/`.
3. Produce GitHub-facing Markdown under `github-facing/`.
4. Produce no-network tracked HTML under `html/`.
5. Capture desktop and mobile screenshot evidence under the task artifacts.
6. Refresh generated registries, wiki notes, and local retrieval support through
   the approved bootstrap path.

The HTML page may use local reading enhancements only when the document still
reads without JavaScript. It must not depend on remote fonts, remote CSS,
external scripts, browser-side Mermaid rendering, hosted comments, or network
assets.

## Failure Boundaries

Common operational mistakes have the same pattern: the tool works, therefore
the user assumes authority changed. That inference is invalid.

- A working `.venv` does not authorize a registry edit.
- Codex app access does not make the app scientific authority.
- A screenshot proves rendered evidence exists; it is not a source contract.
- A generated HTML page can clarify a workflow; it cannot create one.
- A local memory hit can route attention; it cannot replace canonical source
  inspection.
- A test or check PASS means the checked contract passed; it is not a broad
  scientific verdict.

The correction is always source-first: inspect the relevant source path,
registry row, role or skill contract, AgentJob allowlist, completion evidence,
and claim boundary.

## Operator Sequence

1. Identify the work tier: inspection, governed agent work, Python check,
   memory refresh, HTML screenshot QA, PDF derivative, or tests.
2. Inspect the listed source path before running commands.
3. Confirm the current task or AgentJob allows the write path if any source
   changes are involved.
4. Run the narrow command family from the repository source.
5. Preserve output evidence in the task packet when the workflow requires it.
6. Treat generated outputs and `.local` surfaces as support, not authority.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door and requirements].
- AEther-Flow Project. (2026). `AGENTS.md` [Root authority hierarchy].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control operation].
- AEther-Flow Project. (2026). `requirements.txt` [Python dependency ledger].
- AEther-Flow Project. (2026). `Makefile` [Grouped local command targets].
- AEther-Flow Project. (2026). `scripts/README.md` [Repository script boundaries].
- AEther-Flow Project. (2026). `tests/README.md` [Test coverage and command guidance].
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Memory and registry refresh].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system improvement workflow].
- AEther-Flow Project. (2026). `.codex/skills/html-visual-explainer/SKILL.md` [Governed HTML publication].
- AEther-Flow Project. (2026). `.codex/skills/visual-explainer/SKILL.md` [Visual explainer constraints].
- AEther-Flow Project. (2026). `.codex/skills/pdf-derivative-build/SKILL.md` [Managed PDF derivative builds].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/technical-requirements-explainer.md`
- **Related HTML:** `html/technical-requirements-explainer.html`
- **Publication brief:** `markdown/publication-briefs/technical-requirements.publication-brief.md`
- **Authority status:** generated noncanonical reader surface
