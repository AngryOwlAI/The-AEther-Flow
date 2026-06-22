<!-- authority: control -->

# Phase 6 Bridge Checkpoint Documentation Phase 0 Audit

## Analysis

Phase 0 of
`implementations_plans/phase6_bridge_checkpoint_documentation_update_plan.md`
is a preflight and evidence-lock packet. Its purpose is to establish the exact
documentation baseline before later phases update the README and public
explainer stack.

The relevant Phase 6 behavior is operational and narrow:

- project-improvement sidecar YAML/Markdown pairs are not globally
  allowlisted;
- checkpoint and `--check-diff` accept only the exact sidecar pair referenced
  by an AgentJob-allowed changed source YAML through `project_improvement_bridge`;
- the sidecar must point back to the source and preserve matching signal IDs
  plus project-system-only boundaries;
- normal research handoffs remain the `/continue-research` authority;
- sidecars are consumed by `/improve-project-system`;
- Phase 6 did not create a live sidecar instance and did not change physics
  authority.

Conclusion: Phase 0 should not rewrite public documentation. It should name the
source basis and classify each documentation surface for the later phases.

## Evidence Lock

| Evidence item | Phase 0 finding |
| --- | --- |
| Initial worktree state | `git status --short` returned no paths before Phase 0 edits. |
| Phase 6 commit | `ddfe263cbfdcbd23d4d41223942409ce13d4dfea` is `HEAD` on `main` and `origin/main`. The commit completed `RT-20260622-007`. |
| Phase 6 artifact | `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md` states the conditional sidecar allowlist rule and no-live-sidecar boundary. |
| Phase 6 documentation impact | `research_control/tasks/RT-20260622-007/documentation_impact.yaml` says the source documentation update was limited to `scripts/project_control/README.md` and `scripts/research_control/README.md`. |
| Memory preflight | `query_memory.py status --json` returned `freshness_status: PASS`, an existing vault, an existing memory index, and 320 source objects. |
| Current classifier | Before Phase 0 edits, `classify_project_changes.py --json` returned no documentation-impact or project-system requirement. |
| Current resolver | Before Phase 0 edits, `resolve_project_improvement.py --json` returned `boundary: no_action` and no open project-improvement signal. |

## Source-Surface List

### Local Planning Source

| Surface | Status | Phase 0 use |
| --- | --- | --- |
| `implementations_plans/phase6_bridge_checkpoint_documentation_update_plan.md` | Local gitignored planning reference | Governs this phased documentation update request. It is not an independent authority source. |

### Phase 6 Source Evidence

| Surface | Status | Phase 0 use |
| --- | --- | --- |
| `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md` | Task-local control artifact | Primary behavior summary for conditional sidecar allowlisting. |
| `research_control/tasks/RT-20260622-007/documentation_impact.yaml` | Task-local documentation-impact receipt | Confirms Phase 6 updated script READMEs only. |
| `git show --stat ddfe263cbfdcbd23d4d41223942409ce13d4dfea` | Git evidence | Confirms changed paths and the absence of public explainer updates in the Phase 6 commit. |

### Control Contracts And Operator Docs

| Surface | Registry or status | Phase 0 decision |
| --- | --- | --- |
| `AGENTS.md` | `MD-AGENTS`, source hash `fadaed73748fd5b31668c3eea46c971dc0dd873fa7b7abf15a302c19ece94ba9` | Already states sidecars are separate project-system bridge artifacts consumed by `/improve-project-system`. No Phase 0 edit. |
| `research_control/AGENTS.md` | `MD-AGENTS-RESEARCH-CONTROL`, source hash `3faecd98ff3d9bad48962a1d1b590210b80523659c0b950c22b291dd540f5a90` | Already preserves normal handoff authority and sidecar project-system boundary. No Phase 0 edit. |
| `.codex/skills/continue-research/SKILL.md` | `MD-SKILL-CONTINUE-RESEARCH`, source hash `e73434596f2e97dcdbe2c948dc55b34d923539c6637df0256199517edac8b425` | Confirms the regular research-continuation surface remains separate from project-system improvement sidecars. No Phase 0 edit. |
| `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md` | `MD-SCHEMA-PROJECT-IMPROVEMENT-HANDOFF-SCHEMA`, source hash `63c993717553852e34add3d56e7e24ba29ddcdb0c3184ed05cbccf64b87de16c` | Primary schema source for sidecar status, parity, and bridge fields. No Phase 0 edit. |
| `.agents/schemas/README.md` | Registered schema-folder README | Already names the project-improvement handoff schema. No Phase 0 edit. |
| `scripts/project_control/README.md` | `MD-README-SCRIPTS-PROJECT-CONTROL`, source hash `efcf156e9a1aa2e6d0c1e484dd315f23fe3bcb37c651da87c844f37c069c38c9` | Already states sidecars are not globally allowlisted and names exact bridge-reference behavior. No Phase 0 edit. |
| `scripts/research_control/README.md` | `MD-README-SCRIPTS-RESEARCH-CONTROL`, source hash `03090f78534032b29f0bf5441c1fc6b30d161078bf8b223b3a75ebef9d080742` | Already states checkpoint accepts generated sidecar pairs only through active AgentJob source-YAML reference. No Phase 0 edit. |
| `research_control/design/documentation_curator_post_migration_quality_plan.md` | `MD-RESEARCH-CONTROL-DESIGN-DOCUMENTATION-CURATOR-POST-MIGRATION-QUALITY-PLAN`, source hash `b2295d58ee49703d20dbbb3e9f480a6447580011855a2acd9cf571219da730fd` | Provides prior documentation-quality context for source-backed page review. No Phase 0 edit. |
| `research_control/design/documentation_curator_corpus_migration_plan.md` | `MD-RESEARCH-CONTROL-DESIGN-DOCUMENTATION-CURATOR-CORPUS-MIGRATION-PLAN`, source hash `98f6263f816795d3d18fb551613fab102c569860209678f6eaa96d92e5119960` | Provides prior corpus-publication context for source-spec and brief boundaries. No Phase 0 edit. |

### Front-Door And Scoped README Files

| Surface | Phase 0 decision | Reason |
| --- | --- | --- |
| `README.md` | Edit in Phase 1 | It explains project-system improvement and signals, but does not yet explain `project_improvement_bridge`, bridge sidecars, or the conditional checkpoint allowlist rule at front-door level. |
| `markdown/README.md` | No-op | Folder semantics remain current. No Phase 6 behavior changes how authored Markdown sources are organized. |
| `markdown/publication-briefs/README.md` | No-op | Corpus status and brief-first rules remain current. |
| `markdown/html-explainer-specs/README.md` | No-op | It describes the 17 reviewed page stacks and Reader Scope footer rule. Phase 6 bridge checkpoint behavior does not change source-spec folder semantics. |
| `.agents/schemas/README.md` | No-op | It already names the project-improvement handoff schema. |
| `scripts/project_control/README.md` | No-op | Phase 6 already updated it with the conditional allowlist boundary. |
| `scripts/research_control/README.md` | No-op | Phase 6 already updated it with the checkpoint-sidecar boundary. |

## Page-Impact Matrix

| Page stack | Decision | Named source basis for any later edit |
| --- | --- | --- |
| `project-system-improvement` | Edit in later phase | `AGENTS.md`; `research_control/AGENTS.md`; `.codex/skills/improve-project-system/SKILL.md`; `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`; `scripts/project_control/README.md`; `scripts/project_control/resolve_project_improvement.py`; Phase 6 artifact. |
| `validator-operator-workflow` | Edit in later phase | `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`; `scripts/project_control/project_improvement_handoff_validation.py`; `scripts/research_control/checkpoint_research_transaction.py`; `scripts/research_control/validate_research_control.py`; `scripts/project_control/README.md`; `scripts/research_control/README.md`; Phase 6 artifact. |
| `research-agent-workflow` | Limited edit candidate | `AGENTS.md`; `research_control/AGENTS.md`; `.codex/skills/continue-research/SKILL.md`; `.codex/skills/improve-project-system/SKILL.md`; `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`. |
| `director-agentjob-lifecycle` | Limited edit candidate | `.agents/schemas/AGENT_JOB_SCHEMA.md`; `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`; `registries/AGENT_JOB_REGISTRY.csv`; Phase 6 task files. |
| `source-authority` | Limited edit candidate | `AGENTS.md`; `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`; `registries/MARKDOWN_SOURCE_REGISTRY.csv`; `registries/HTML_EXPLAINER_REGISTRY.csv`. |
| `memory-system` | Audit-only | Existing page already covers wiki, Obsidian, SQLite, and bootstrap as retrieval support rather than authority. Update only if later public-doc edits create fresh retrieval-sync guidance. |
| `technical-requirements` | Audit-only | Existing page covers local command families at a high level. Update only if later phases add required operator commands beyond current README/script guidance. |
| `documentation-curator-publication-process` | Audit-only | Phase 6 did not change brief-first publication or screenshot/review discipline. |
| `roles-and-skills` | Audit-only | Phase 6 did not change role contracts. Prior bridge role versions are already registry-backed and should not be rewritten from this Phase 0 audit. |
| `role-routing` | Audit-only | No role routing behavior changed in Phase 6. |
| `project-overview` | Audit-only | Use only if Phase 1 front-door review finds the overview needs one bridge sentence. |
| `claim-gates` | No-op | Checkpoint sidecar validation is operational evidence, not physics claim-gate evidence. |
| `aether-flow-physics-program` | No-op | No physics-program claim changed. |
| `aether-flow-ontology` | No-op | No ontology source or adoption state changed. |
| `exact-gr-benchmark-boundary` | No-op | No benchmark boundary changed. |
| `gr-derivation-roadmap` | No-op | No derivation milestone or burden changed. |
| `parent-child-synthesis` | No-op | No parent-child synthesis rule changed. |

## Derivative And Retrieval Boundary

Phase 0 marks no generated wiki note, generated metadata sidecar, GitHub-facing
Markdown derivative, or tracked HTML derivative for hand edit. Later phases
must update source specs first when public explainer content changes, then
synchronize GitHub-facing Markdown and HTML through the governed publication
pipeline.

If later phases regenerate retrieval surfaces, the generated outputs remain
noncanonical. The authority remains the registered source, registry row, and
task receipt.

For this Phase 0 packet, `FOLDER_MAP.md` is a generated bootstrap output and
is recorded as a derivative receipt, not as an edited source of authority.

## Phase 0 Exit Criteria

| Criterion | Result |
| --- | --- |
| No documentation page is selected for edit without a named source basis. | Satisfied. Every edit or limited-edit candidate above names source basis. |
| No generated wiki or generated metadata file is marked for hand edit. | Satisfied. Generated surfaces are validation or regeneration outputs only. |
| Phase 0 does not rewrite public docs. | Satisfied. README, source specs, publication briefs, GitHub-facing Markdown, and HTML are later-phase targets only. |
| Phase 0 preserves project-system-only sidecar semantics. | Satisfied. The audit does not create sidecars, resolve signals, or alter research handoff authority. |

## Recommendation

Proceed to Phase 1. The narrow README update should add the bridge at
front-door level without expanding it into an operator manual:

1. State that research-discovered project-system issues can be bridged into
   the improvement lane through validated project-improvement sidecars.
2. State that normal research handoffs remain `/continue-research` authority.
3. State that sidecars are consumed by `/improve-project-system`.
4. State that checkpoint and diff validation accept sidecars only through the
   exact source-YAML bridge rule.
5. Preserve generated-output and physics authority boundaries.

## Can It Be Improved?

An improvement will be to give Phase 1 a small README diff and a separate
Phase 2 brief-impact audit. That keeps the front-door correction reversible and
prevents README wording from prematurely selecting all public explainer edits.

## References

The AEther-Flow Research Project. (2026, June 22). *Phase 6 bridge checkpoint
governance documentation update plan* [Implementation plan].
`implementations_plans/phase6_bridge_checkpoint_documentation_update_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 6 checkpoint allowlist governance* [Project-control artifact].
`research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`

The AEther-Flow Research Project. (2026, June 22). *Project improvement
handoff schema* [Project-control schema].
`.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`

The AEther-Flow Research Project. (2026). *Root agent guidance and authority
hierarchy* [Project-control guidance]. `AGENTS.md`

The AEther-Flow Research Project. (2026). *Publication brief registry*
[Documentation-control registry]. `registries/PUBLICATION_BRIEF_REGISTRY.csv`
