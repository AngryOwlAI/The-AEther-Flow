# Validator And Operator Workflow

AEther-Flow operators do not run every command by habit. They choose checks
from the kind of change being made: memory and registry refresh, public
publication page work, project-system control work, research-control state
work, script changes, test changes, or tracked HTML review.

This page is a generated noncanonical reader surface. It explains the existing
operator workflow, but it does not change validator behavior, command
semantics, routing behavior, documentation-impact requirements,
research-control requirements, role authority, schemas, checkpoint gates,
generated-output authority, or physics claim status.

## What Operators Need To Decide

The first question is the change type:

- A Markdown source spec, publication brief, GitHub-facing page, or tracked
  HTML page needs publication-process checks and screenshot evidence.
- A source or registry change that affects generated wiki, registry, semantic,
  Obsidian, or memory-index artifacts needs the memory bootstrap path.
- A state-changing project-system AgentJob needs classifier, resolver,
  emitted-signal validation, documentation-impact validation, bootstrap, and
  research-control checks.
- A research-control state change needs research-control validation, and
  `--check-diff` when write-path boundaries matter.
- A script or test change needs targeted or full unit tests.

The logical next step is not "run the largest command list." It is to identify
the smallest command set that covers the authority surfaces touched by the
change.

## Command Matrix

| Change or review need | Command | What the command proves |
| --- | --- | --- |
| Refresh generated memory, wiki, registry, and derivative artifacts | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py` | The generated retrieval and metadata layers can be rebuilt from tracked sources. |
| Check memory/wiki/registry state without writing | `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only` | The current generated state is mechanically consistent enough for read-only review. |
| Check governed public pages | `.venv/bin/python scripts/validate_publication_process.py --root . --strict` | Publication brief, source spec, GitHub Markdown, HTML, evidence paths, no-network HTML, source visibility, and retired-pattern guards pass. |
| Classify changed paths before routing | `.venv/bin/python scripts/project_control/classify_project_changes.py --json` | The live diff is mapped to documentation-impact and project-system reason codes. |
| Resolve project-system routing state | `.venv/bin/python scripts/project_control/resolve_project_improvement.py --json` | Current diff work and registered open project-improvement signals are compared for advisory routing. |
| Check emitted project-improvement signals | `.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted` | Completion and handoff signal entries are backed by registered signal rows and types. |
| Check documentation-impact receipts | `.venv/bin/python scripts/project_control/validate_documentation_impact.py` | The receipt covers live source changes, generated derivatives, reason codes, and required validators. |
| Check research-control records | `.venv/bin/python scripts/research_control/validate_research_control.py` | Task, decision, AgentJob, execution-role, claim-boundary, and registry constraints pass. |
| Check write-path boundaries against the diff | `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff` | Changed paths stay within the active control boundary and allowed write rules. |
| Run unit tests after tooling changes | `.venv/bin/python -m unittest discover -s tests` | The Python test suite still passes for project-control, research-control, memory, and explainer tooling. |

## Bootstrap And Validate-Only

Bootstrap writes generated derivatives. It is the correct command after
changing registered Markdown, TeX, source specs, registry rows, or other
source material that feeds wiki notes, content semantics, Obsidian mirrors,
file registries, object relationships, or memory-index state.

Validate-only checks current generated state without writing. It is useful for
read-only review and final gates, but it does not refresh stale generated
artifacts. If source material changed, validate-only by itself is insufficient.

Known `.local`, Obsidian, or memory-index freshness warnings are retrieval-layer
warnings. They do not override tracked source files, registry rows, or
research-control records.

## Documentation And Research-Control Gates

Project-system work has a stronger receipt burden than ordinary explanatory
editing. A state-changing project-system AgentJob needs
`research_control/tasks/<task_id>/documentation_impact.yaml`. The receipt must
cover changed paths, reason codes, inspected source surfaces, updated source
docs or no-op rationale, registries, generated derivatives, and validators run.

Research-control checks verify the tracked control spine. They are required
after changes to task records, Director decisions, AgentJobs, execution-role
records, completions, claim boundaries, or research-control registries. Add
`--check-diff` when the review must prove that live file changes remain inside
the authorized write boundary.

## Tests And Screenshots

Run unit tests when the change touches scripts, validators, project-control
behavior, research-control behavior, memory-system behavior, test fixtures, or
test files. Use the full test command when the impact crosses modules; use a
targeted module command only when the change is narrow and the risk is local.

Tracked HTML pages also need visual evidence. For governed publication pages,
capture desktop and mobile screenshots under the current task artifact
directory and reference both paths from
`registries/PUBLICATION_BRIEF_REGISTRY.csv`. Screenshot evidence proves the
page renders and fits the target viewports; it does not prove editorial
quality by itself.

## Troubleshooting

| Symptom | Likely cause | Correct response |
| --- | --- | --- |
| Publication check reports an orphan public page | A source spec, GitHub Markdown page, or HTML page exists without a publication brief registry row. | Add or correct the governed brief, spec, output path, and registry row in one bounded packet. |
| Publication check reports missing screenshot evidence | The registry row points to desktop or mobile screenshot paths that do not exist. | Capture screenshots into the current task artifact directory and keep the paths stable. |
| Documentation-impact check reports missing live source change | The receipt did not list a changed source path. | Update `documentation_impact.yaml` to cover the live diff; do not delete the source change to satisfy the receipt. |
| Research-control diff check reports a write-path boundary failure | A changed path is outside the AgentJob allowlist or protected by role/source-class rules. | Narrow the packet, adjust the authorized task if valid, or stop for human authorization. |
| Bootstrap reports stale `.local` retrieval state | Local Obsidian, semantic, or memory-index derivatives lag source state. | Treat as a retrieval-layer warning unless a validator makes it a hard failure; source authority remains tracked files and registries. |

## What PASS Means

Validator PASS means the deterministic checks run by that command accepted the
current state. It is necessary evidence for governed work, but it is not proof
of scientific truth, ontology adoption, benchmark promotion, completed
derivation, or publication taste.

For final review, pair PASS results with concrete evidence: changed source
paths, generated derivative paths, screenshot paths where HTML is involved,
before/after review notes, and a clear claim boundary.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door].
- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority guidance].
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Project memory system skill].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system improvement skill].
- AEther-Flow Project. (2026). `scripts/README.md` [Scripts folder guide].
- AEther-Flow Project. (2026). `tests/README.md` [Tests folder guide].
- AEther-Flow Project. (2026). `scripts/validate_publication_process.py` [Publication-process checker].
- AEther-Flow Project. (2026). `scripts/project_control/validate_documentation_impact.py` [Documentation-impact checker].
- AEther-Flow Project. (2026). `scripts/research_control/validate_research_control.py` [Research-control checker].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/validator-operator-workflow-explainer.md`
- **Related HTML:** `html/validator-operator-workflow-explainer.html`
- **Publication brief:** `markdown/publication-briefs/validator-operator-workflow.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: choose checks by changed authority surface, refresh generated
derivatives through bootstrap, validate publication pages and screenshots,
record documentation impact for project-system AgentJobs, run research-control
checks for control records, run tests for tooling changes, and treat PASS as
bounded evidence.

Unsafe summary: a validator PASS proves scientific truth, approves ontology,
certifies editorial quality, changes command behavior, or gives generated
documentation independent authority.
