# Roles And Skills Catalog

AEther-Flow roles and skills are navigation aids only when read from this
public catalog. The actual authority lives in the role registry, the role or
skill contract, the task-local execution-role record, the AgentJob allowlist,
the claim boundary, the completion record, and the validators.

This page is a generated noncanonical reader surface. It does not change role
status, register roles, supersede roles, expand role authority, change skill
contracts, change validator behavior, change routing behavior, change
AgentJob allowlists, change checkpoint behavior, or promote physics claims.

## Read Order

Use this order when a role or skill matters for a real transaction:

1. Inspect `registries/AGENT_ROLE_REGISTRY.csv` for role identity, version,
   status, authority level, human-gate status, output form, and default
   validators.
2. Inspect the active role contract under `.agents/roles/` or the skill
   contract under `.codex/skills/`.
3. Inspect the task-local execution-role record under
   `research_control/tasks/<task_id>/roles/`.
4. Inspect the AgentJob allowlist and claim boundary.
5. Inspect completion evidence and validator results.

The catalog can point to those files. It cannot replace them.

## Active Roles

| Role | Family | Current status | Main responsibility | Authority boundary |
| --- | --- | --- | --- | --- |
| `director-of-research@0.2.0` | Research ops | active | Routes the next bounded research-control step and creates one AgentJob when no human gate is required. | Routing control; does not validate physics claims or promote them. |
| `project-system-director@0.1.0` | Research ops | active | Selects one bounded project-system improvement step from signals, Git state, guidance, and validators. | Project control; does not perform physics derivation. |
| `documentation-curator@2.0.0` | Research ops | active | Produces source-backed publication pages from page-specific briefs. | Project documentation; generated outputs remain noncanonical. |
| `project-control-maintainer@0.1.0` | Research ops | active | Maintains project-control markdown, role/schema/skill contracts, registries, and validator hooks when authorized. | Project control; does not edit explanatory docs unless an overlay grants it. |
| `validator-engineer@0.1.0` | Research ops | active | Improves deterministic validators, tests, and checkpoint gates. | Project-system validation; no physics claim promotion. |
| `memory-system-maintainer@0.1.0` | Research ops | active | Maintains source-first memory, wiki, registry, Obsidian, and derivative metadata tooling. | Memory-system maintenance; generated memory is retrieval only. |
| `process-integrity-auditor@0.1.0` | Research ops | active | Repairs control-state defects when the correct state is uniquely determined by tracked evidence. | Process control; no broad rewrite. |
| `ontology-formalizer@0.2.0` | Physics | active | Defines source-side primitives, assumptions, forbidden imports, and Gate 0 burdens as draft/control artifacts. | Science draft; cannot promote ontology. |
| `candidate-constructor@0.2.0` | Physics | active | Constructs one bounded candidate derivation step as a registered draft/control artifact. | Science draft; bridge attempts remain gated. |
| `refuter@0.2.0` | Physics | active | Attacks candidate steps, mechanisms, laws, or bridges and preserves local negative results. | Science draft; negative results do not become global no-go claims by default. |
| `smuggling-auditor@0.2.0` | Physics | active | Audits derivation and ontology-promotion packets for hidden target imports. | Science draft; audits do not promote claims. |
| `theoretical-continuation-selector@0.1.0` | Physics | active | Selects one bounded theoretical packet when tracked state allows continuation but no single role is determined. | Science draft; selection is not claim promotion. |
| `gate-chair@0.1.0` | Physics | status defined | Renders promotion, closure, or suspension decisions after evidence exists. | Human-gated and paused; execution and promotion require explicit tracked approval. |

## Superseded Roles

Superseded role versions remain in the registry for historical execution
records. They should not be treated as the current role unless a historical
task explicitly used that version.

Common superseded groups include:

- `documentation-curator@0.1.0` through `documentation-curator@1.0.0`, retained
  for earlier explainer, teaching-loop, and Visual Atlas records.
- `director-of-research@0.1.0`, retained for older Director records before the
  current bridge-or-fail routing discipline.
- `ontology-formalizer@0.1.0`, `candidate-constructor@0.1.0`,
  `refuter@0.1.0`, and `smuggling-auditor@0.1.0`, retained for older physics
  draft/control records.

The registry `status` field is the deciding signal. A public catalog sentence
cannot revive a superseded contract.

## Skill Entry Points

| Skill | Owns | Does not own |
| --- | --- | --- |
| `.codex/skills/continue-research/SKILL.md` | Research-control continuation, Director routing, one bounded AgentJob, memory preflight, execution-role records, parent-child synthesis, checkpoint boundaries. | Project-system repair unless the active AgentJob explicitly authorizes it. |
| `.codex/skills/improve-project-system/SKILL.md` | Project-system improvement, classifier/resolver usage, signal validation, documentation-impact receipts, one bounded project-system AgentJob. | Physics derivation, scientific claim promotion, or Gate Chair decisions. |
| `.codex/skills/project-memory-system/SKILL.md` | Bootstrap, validate-only, documentation publication validation modes, generated registry/wiki/memory refresh, local-noise cleanup. | Replacing canonical sources or treating generated retrieval as authority. |
| `.codex/skills/html-visual-explainer/SKILL.md` | Governed tracked HTML publication pages, publication-brief binding, no-network HTML, GitHub Markdown pairing, screenshot QA. | Direct HTML-only edits outside the source-spec path. |
| `.codex/skills/visual-explainer/SKILL.md` | Visual treatment for source-backed HTML explainers, role matrices, annotated tables, diagrams, and screenshot review discipline. | Public deployment or external runtime use for tracked HTML. |

## Validator Families

| Role group | Typical validators | Interpretation |
| --- | --- | --- |
| Physics draft and routing roles | `validate_research_control`; `claim_boundary_phrase_scan` | Checks control-state and unsafe-claim boundaries. It is not a physics proof. |
| Documentation Curator | `bootstrap_memory_system`; `validate_research_control`; `validate_documentation_impact`; `scripts/validate_publication_process.py --root .` | Checks generated-memory sync, control state, documentation-impact receipt, and publication-process safety. |
| Project-control and validator roles | `validate_documentation_impact`; `validate_research_control`; `unittest` when scripts or tests change | Checks project-system edits and deterministic behavior. |
| Memory-System Maintainer | `bootstrap_memory_system`; `validate_documentation_impact`; `validate_research_control`; `unittest` | Checks source-first memory/tooling changes and generated derivative refresh. |
| Gate Chair | `validate_research_control`; `claim_boundary_phrase_scan` plus explicit tracked human approval | A defined role status is not execution approval. |

Validator PASS means the transaction satisfies configured checks. It does not
turn generated documentation into authority and does not promote physics
claims.

## Safe Use

Safe summary: use this catalog to locate active role rows, historical role
rows, and skill entry points; then inspect the authoritative source files.

Unsafe summary: a catalog row grants write permission, a superseded role is
active because it appears in a table, a skill entry point can bypass the
AgentJob allowlist, or the Gate Chair can execute without tracked approval.

## Source Materials

- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv` [Agent role registry].
- AEther-Flow Project. (2026). `.agents/roles/` [Versioned role contracts].
- AEther-Flow Project. (2026). `.codex/skills/continue-research/SKILL.md` [Research continuation skill].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system improvement skill].
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Project memory system skill].
- AEther-Flow Project. (2026). `.codex/skills/html-visual-explainer/SKILL.md` [Governed HTML publication skill].
- AEther-Flow Project. (2026). `.codex/skills/visual-explainer/SKILL.md` [Visual explainer skill].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- **Related HTML:** `html/roles-and-skills-explainer.html`
- **Publication brief:** `markdown/publication-briefs/roles-and-skills.publication-brief.md`
- **Authority status:** generated noncanonical reader surface
