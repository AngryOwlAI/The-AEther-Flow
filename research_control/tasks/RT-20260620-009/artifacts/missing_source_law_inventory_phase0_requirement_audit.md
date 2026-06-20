<!-- authority: control -->

# Missing Source-Law Inventory Phase 0 Requirement Audit

## Analysis

Phase 0 from
`implementations_plans/missing_source_law_inventory_artifact_registry_implementation_plan.md`
is an evidence audit and schema decision. It does not create the inventory, add
a dedicated registry, change `/continue-research`, change validators, or
promote any physics claim.

The current live research state names `RT-20260614-075` and `handoff-0117`.
That state is relevant because it identifies the active missing-law family:
current canonical ontology does not derive the discriminator profiles, selector
preorder, inverse checks, cocycle checks, or finite-variation robustness needed
for `AtlasGlueDisc_src^+`, `AtlasGlue_src^+`, or `M_src` source-authority
adoption. The state blocks adoption while leaving same-milestone continuation
open.

## Phase 0 Acceptance

| Requirement | Phase 0 status | Evidence |
| --- | --- | --- |
| Inspect governing control guidance | Satisfied | `AGENTS.md`, `research_control/AGENTS.md`, and `.codex/skills/continue-research/SKILL.md` were inspected. |
| Inspect memory/bootstrap registry support | Satisfied | `bootstrap_memory_system.py` defines source registries for Markdown, TeX, PDF, and HTML; no YAML source registry exists. |
| Inspect live control evidence | Satisfied | `program_state.yaml`, `handoff-0117.yaml`, `RT-20260614-075`, `DISTANCE_TO_GR_LEDGER.csv`, and current registry rows were inspected. |
| Decide Option A or Option B | Satisfied | Option A is selected for the first rollout with constrained Markdown registration and tracked YAML by stable path. |
| Avoid a second routing system | Satisfied | `/continue-research` remains the only active selector and executor. |
| Justify artifact location | Satisfied | `research_control/missing_laws/` is a tracked control-state lane for navigation evidence and candidate backlog data. |

## Registry And Artifact Decision

Recommendation: use Option A for the first rollout.

Phase 1 should create:

```text
research_control/missing_laws/missing_source_law_inventory.yaml
research_control/missing_laws/missing_source_law_inventory.md
```

The YAML file should be the structured control input. The Markdown companion
should be the human review surface. The inventory should be read by
`/continue-research` as navigation evidence only, not as a command script.

Reasoning:

- `research_control/` is already the authority lane for tracked state,
  handoffs, tasks, completions, and control inputs.
- Current bootstrap support does not include first-class YAML source
  registration.
- Current Markdown source support is established, but
  `research_control/missing_laws/*.md` is not yet in the discovered Markdown
  globs.
- A dedicated CSV registry would add validator and bootstrap machinery before
  there is evidence that first-class row-level queryability is necessary.
- The existing `/continue-research` route already selects exactly one bounded
  AgentJob; the inventory only supplies candidate evidence and dependencies.

Phase 2 should therefore make the Markdown companion discoverable through
existing Markdown source machinery if needed. It should not create
`registries/MISSING_SOURCE_LAW_INVENTORY_REGISTRY.csv` unless Phase 1 usage
shows that YAML plus Markdown is insufficient.

## YAML Registration Finding

YAML source registration is not currently supported as a first-class memory
source registry path.

Evidence:

- `SOURCE_REGISTRY_NAMES` contains `MARKDOWN_SOURCE_REGISTRY.csv`,
  `TEX_SOURCE_REGISTRY.csv`, `PDF_DERIVATIVE_REGISTRY.csv`, and
  `HTML_EXPLAINER_REGISTRY.csv`.
- `discover_markdown_rows` handles Markdown files from explicit project lists,
  folder README paths, selected globs, `ontology`, `legacy_ontology`, and
  `markdown`.
- Existing YAML task, job, handoff, and completion files are tracked
  research-control state, but they are not registered as independent source
  objects in the memory-source registry model.

Conclusion: YAML can be a tracked control artifact by stable path, but it
should not be represented as a source-registry object without a later explicit
bootstrap and validator change.

## Selected Design

The selected design is:

1. Treat `missing_source_law_inventory.yaml` as tracked control data.
2. Treat `missing_source_law_inventory.md` as the human-readable companion.
3. Keep both under `research_control/missing_laws/`.
4. Let `/continue-research` consume the YAML only after live state names a
   derivation-critical missing source-side law.
5. Keep inventory rows as evidence and backlog data, not execution commands.
6. Defer dedicated CSV registry creation.
7. Add validation only after Phase 1 establishes the artifact shape.

This design preserves the implementation plan's correction: no second
pipeline, no batch packet generator, and no autonomous law adoption.

## Boundary Findings

1. `handoff-0117` supports a missing source-side law or selector continuation,
   not adoption of supplied finite data.
2. The Distance-to-GR ledger marks `m_src` and `finite_variation_robustness`
   as blocked by missing primitive evidence tied to `RT-20260614-075`.
3. The current ontology derivation attempt is a scoped obstruction. It does
   not prove global impossibility or future source-extension impossibility.
4. Inventory seed rows must preserve the exact boundary:
   `blocked_adoption_open_continuation`.
5. Generated wiki, semantic, Obsidian, and registry-metadata surfaces remain
   retrieval support only.

## Phase 1 Requirements

Phase 1 should:

- create the YAML and Markdown inventory files;
- populate active control metadata from `program_state.yaml` and
  `handoff-0117.yaml`;
- add only evidence-backed seed candidates;
- classify every candidate as `derivation_critical_missing_source_law`,
  `ordinary_gap`, `workflow_inconvenience`, or `not_yet_classified`;
- preserve forbidden overreads for adoption, benchmark, metric, coupling,
  Einstein-equation, Gate Chair, and global-rejection claims;
- avoid any ontology adoption or canonical ontology edit.

## Memory Preflight Receipt

The memory status command returned `freshness_status: PASS` with 301 source
objects, an existing SQLite memory index, and an existing local Obsidian vault.
These retrieval layers were used only for navigation.

The targeted lookup
`.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup TEX-RESEARCH-CONTROL-RESP-LC-CURRENT-ONTOLOGY-ATLAS-GLUE-DERIVATION-ATTEMPT --json`
returned the primary source object
`TEX-RESEARCH-CONTROL-RESP-LC-CURRENT-ONTOLOGY-ATLAS-GLUE-DERIVATION-ATTEMPT`.
Canonical inspection used `registries/TEX_SOURCE_REGISTRY.csv`, path
`research_control/tasks/RT-20260614-075/artifacts/116_RESP_LC_CURRENT_ONTOLOGY_ATLAS_GLUE_DERIVATION_ATTEMPT.tex`,
and source hash
`6eb83b8e714641730d28e53af3f43757ae262912deb7b958d571c7ea656e2c0d`.

## Recommendation

The logical next step is Phase 1: create the tracked YAML inventory and
Markdown companion under `research_control/missing_laws/`, then populate the
first candidate rows only from canonical task, handoff, ledger, and registry
evidence.

## Can It Be Improved?

An improvement will be to make `continue_research.py` report the matching
inventory candidate ID in its JSON context packet after the inventory has been
used manually at least once. That should be a later small enhancement, not part
of Phase 0 or Phase 1.

## References

The AEther-Flow Research Project. (2026, June 20). *Handoff 0117*
[Internal research-control handoff]. `research_control/handoffs/handoff-0117.yaml`

The AEther-Flow Research Project. (2026, June 20). *Missing source-law
inventory artifact registry implementation plan* [Implementation plan].
`implementations_plans/missing_source_law_inventory_artifact_registry_implementation_plan.md`

The AEther-Flow Research Project. (2026, June 20). *Resp_lc current-ontology
AtlasGlue derivation attempt* [Internal research-control artifact].
`research_control/tasks/RT-20260614-075/artifacts/116_RESP_LC_CURRENT_ONTOLOGY_ATLAS_GLUE_DERIVATION_ATTEMPT.tex`

The AEther-Flow Research Project. (2026). *Project memory system bootstrap
script* [Repository tool].
`.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
