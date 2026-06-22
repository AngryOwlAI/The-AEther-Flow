# Validator And Operator Workflow

The operator problem is not simply which command to run. It is which evidence chain fits the changed authority surface. A Markdown article, source spec, validator script, role contract, memory bootstrap, research-control task, and screenshot artifact do not carry the same risk or require the same proof.

AEther-Flow therefore groups checks by change type. Memory and registry refresh work uses bootstrap. Public page work uses the publication-process check plus rendered screenshot evidence. State-changing project-system AgentJobs need documentation-impact and research-control receipts. Source-bridged project-improvement sidecars need exact sidecar path evidence before checkpoint and `--check-diff` can accept them. Script, validator, schema, role, or memory-tooling changes need focused tests in addition to the control validators.

The final interpretation is bounded. PASS means the named deterministic check accepted the current state. It does not certify scientific truth, ontology adoption, benchmark promotion, completed derivation, sidecar adoption, editorial taste, or generated-output authority.

## Command Decision Matrix

| Item | Function | Boundary |
| --- | --- | --- |
| Memory or registry refresh | Run project-memory bootstrap, then validate-only. | Refresh generated derivatives through the approved path. |
| Publication page rewrite | Run strict publication check, screenshot QA, bootstrap, docs impact, and research-control checks. | Screenshots and review evidence are part of the publication receipt. |
| Project-system AgentJob | Run memory preflight, classifier, resolver, emitted-signal validation, documentation-impact, research-control, and checkpoint checks. | One bounded AgentJob per invocation. |
| Source-bridged sidecar | Run sidecar generation or validation only when an authorized source completion names project-improvement signals. | Sidecar paths are accepted only when source-bridge metadata names the exact YAML/Markdown pair. |
| Script or validator change | Run focused unit tests plus project-control validators. | Tests are evidence of behavior, not physics proof. |
| Research-control record | Run research-control validation and `--check-diff` when checking write boundaries. | Do not mutate completed records without supersession. |

## Conditional Sidecar Allowlist

| Item | Function | Boundary |
| --- | --- | --- |
| Required source bridge | A changed AgentJob source must name the generated project-improvement sidecar paths through `project_improvement_bridge`. | Unreferenced sidecar files remain outside the checkpoint and `--check-diff` allowance. |
| Exact path pair | The accepted pair is the specific YAML sidecar plus its Markdown companion. | The directory `research_control/project_improvement_handoffs/**` is not globally allowed. |
| Positive control | A qualifying source bridge plus matching sidecar pair should pass checkpoint and diff validation. | PASS confirms the rule accepted that exact state. |
| Negative control | Missing bridge metadata, path mismatch, or extra sidecar paths should fail. | Failure protects the normal handoff spine and prevents sidecar drift. |

## When Extra Evidence Is Required

| Item | Function | Boundary |
| --- | --- | --- |
| HTML changed | Capture desktop and mobile screenshots. | Visual rendering evidence. |
| Generated derivatives changed | Run bootstrap and validate-only. | Registry/wiki/hash sync. |
| Project-system state changed | Write documentation-impact receipt. | Covers live diff, generated derivatives, reason codes, and checks. |
| Sidecar paths changed | Verify source-bridge metadata and sidecar validation before checkpointing. | Sidecar existence is not signal closure or research continuation. |
| Tooling changed | Run unit tests. | Checks deterministic behavior. |

## Troubleshooting Operator Failures

| Item | Function | Boundary |
| --- | --- | --- |
| Missing screenshot | Publication registry evidence path points to absent file. | Capture or correct task artifact path. |
| Orphan public surface | GitHub, spec, or HTML exists without its paired row/path. | Synchronize brief, spec, output, and registry. |
| Orphan sidecar | A sidecar file changes without a changed source bridge naming it. | Stop before checkpoint or correct the source-bridge packet. |
| Write-path failure | Diff check sees a changed path outside the AgentJob allowlist. | Narrow the packet or stop for authorization. |
| Stale local retrieval | Obsidian, semantic, or SQLite support lags inputs. | Treat as retrieval drift unless a validator makes it hard failure. |

## PASS Result Limits

| Item | Function | Boundary |
| --- | --- | --- |
| Deterministic acceptance | The command accepted the current checked state. | Necessary transaction evidence. |
| No broad promotion | PASS does not promote physics claims, role authority, sidecar adoption, or generated outputs. | Human-gated authority remains protected. |
| Review still needed | Publication quality depends on screenshots and before/after review. | Taste and clarity are not fully deterministic. |

## Reader Scope

Reader scope: operator command-selection guide only. This page cannot change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, schemas, checkpoint gates, or physics status. It also cannot turn conditional sidecar path acceptance into a global sidecar directory allowance or sidecar adoption claim.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/validator-operator-workflow-explainer.md`
- **Related HTML:** `html/validator-operator-workflow-explainer.html`
- **Publication brief:** `markdown/publication-briefs/validator-operator-workflow.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains existing command selection by change type, bootstrap versus validate-only, publication checks, documentation-impact checks, research-control checks, conditional source-bridge sidecar checkpoint evidence, unit-test triggers, screenshot evidence, troubleshooting, final review evidence, and PASS-result limits without changing validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, role authority, schemas, checkpoint gates, sidecar adoption status, generated-output authority, or physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door, local environment, and public requirements.]
- AEther-Flow Project. (2026). `AGENTS.md` [Authority hierarchy, generated-output boundaries, and required checks.]
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Bootstrap, validate-only, docs modes, and cleanup commands.]
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system memory preflight, classifier, resolver, signal, documentation-impact, and checkpoint chain.]
- AEther-Flow Project. (2026). `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md` [Project-improvement sidecar field contract and source-bridge metadata.]
- AEther-Flow Project. (2026). `scripts/README.md` [Script groups and tooling authority boundary.]
- AEther-Flow Project. (2026). `scripts/project_control/README.md` [Project-control sidecar generation and validation guidance.]
- AEther-Flow Project. (2026). `scripts/research_control/README.md` [Checkpoint and research-control validator guidance.]
- AEther-Flow Project. (2026). `tests/README.md` [Unit-test coverage areas and command shape.]
- AEther-Flow Project. (2026). `scripts/validate_publication_process.py` [Publication brief/spec/output consistency and no-network checks.]
- AEther-Flow Project. (2026). `scripts/project_control/validate_documentation_impact.py` [Documentation-impact receipt validation.]
- AEther-Flow Project. (2026). `scripts/project_control/generate_project_improvement_handoff.py` [Project-improvement sidecar generation from qualifying completion signals.]
- AEther-Flow Project. (2026). `scripts/project_control/project_improvement_handoff_validation.py` [Sidecar schema, source-bridge, and parity validation.]
- AEther-Flow Project. (2026). `scripts/research_control/checkpoint_research_transaction.py` [Checkpoint guard for exact source-bridge sidecar paths.]
- AEther-Flow Project. (2026). `scripts/research_control/validate_research_control.py` [Tracked research-control and diff boundary checks.]
- AEther-Flow Project. (2026). `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md` [Phase 6 conditional sidecar checkpoint governance evidence.]

## Safe Operating Summary

Safe summary: Choose checks by changed authority surface, refresh generated derivatives through bootstrap, record screenshots for HTML, include documentation impact for project-system work, verify exact source-bridge evidence for sidecar paths, and treat PASS as bounded evidence.

Unsafe summary: A validator PASS proves scientific truth, approves ontology, adopts sidecars, certifies editorial quality, changes command behavior, globally allowlists the sidecar directory, or gives generated documentation independent authority.
