<!-- authority: control -->

# Validation orchestration migration and rollback policy v1

Status: active project-control policy for v19 migration; legacy orchestration
remains authoritative.

## Purpose and boundary

This policy controls how validation orchestration may move from the existing
legacy command chains to a shared planner without losing acceptance coverage.
It defines migration epochs, comparison rules, feature-switch states, entry
and exit evidence, rollback triggers, and restoration procedures.

This policy does not implement a planner, activate supersedence, remove a gate,
enable a cache, change Make, CI, skills, checkpointing, or authorize physics.
Validation evidence remains operational evidence. It is not a physics proof,
scientific claim, Distance-to-GR advance, benchmark promotion, or Gate Chair
decision.

## Controlled terms

- **Legacy result**: the result produced by the currently authoritative command
  chain for the declared state and scope.
- **Candidate result**: a consolidated or planner result that is not yet
  authoritative for that scope.
- **Explained mismatch**: a difference predicted by a tracked migration
  decision whose normalized obligation, selected paths, hard findings,
  authority fields, exit status, and final-state effects remain equivalent.
- **Clean shadow transaction**: a matched legacy and candidate execution on
  the same exact repository state, scope, environment, cache state, and input
  configuration with no unexplained difference.
- **Rollback**: restoration of the last authoritative acceptance coverage and
  entry-state transaction integrity. Rollback is not merely restoration of old
  command text.

## Migration epoch state machine

| Epoch | Authoritative path | Candidate behavior | Entry requirements | Exit requirements |
| --- | --- | --- | --- | --- |
| `legacy` | Existing commands | Policy, fixtures, tracing, and non-authoritative measurements only | Current legacy validation passes or preserves a known tracked baseline | Evidence identity, gate IDs, failure-mode corpus, tracing, and this rollback policy pass |
| `legacy_consolidated` | Existing implementations after direct same-scope consolidation | Consolidated wrappers may replace proven direct duplicates | P1-T05 PASS plus task-local equivalence proof for each consolidation | First-wave equivalence audit passes with zero unexplained hard mismatch |
| `shadow_planner` | Legacy | Planner executes only for matched comparison; planner PASS cannot override legacy FAIL | Deterministic plan and receipt schemas exist; full adversarial corpus passes | At least three clean representative shadow transactions, full adversarial parity, and applicable safety evidence pass |
| `planner_authoritative` | Planner for explicitly cut-over profiles | Legacy fallback remains enabled and tested | Tracked cutover decision; all safety budgets pass; applicable activated hard guards pass | Compatibility references migrate and deprecation audit passes |
| `legacy_retired` | Planner | Compatibility artifacts retained only where policy or history requires them | Every destructive retirement cites this policy and its parity evidence; fallback retirement is separately authorized | Reference migration and retirement audit pass with no unique invariant removed |

Epoch advancement is monotonic only after a tracked PASS decision. Rollback may
move authority to any earlier safe epoch. A later epoch name in configuration
does not by itself grant authority.

## Feature switches

Future implementations may realize the following logical switches. Until a
bounded AgentJob implements and validates a switch, its safe value is the value
shown here.

| Switch | Safe value | Allowed values | Rule |
| --- | --- | --- | --- |
| `planner_mode` | `off` | `off`, `shadow`, `authoritative` | `shadow` records comparison evidence only; `authoritative` requires a tracked cutover decision |
| `cache_mode` | `off` | `off`, `read_only`, `read_write` | Any key, tree, implementation, environment, or scope uncertainty forces `off` and an uncached run |
| `output_mode` | `legacy` | `legacy`, `compact` | Compact output requires complete receipt parity and may never change status or hide a hard-finding group |
| `legacy_fallback` | `enabled` | `enabled`, `disabled` | Must remain enabled through `planner_authoritative`; disabling it is a destructive retirement action |

Switch state must appear in the validation receipt. Environment variables,
configuration files, wrapper defaults, and CI inputs are implementation
details owned by later bounded tasks; no implicit or undocumented switch may
control authority.

## Shadow comparison contract

### Comparable inputs

A matched comparison must record:

1. Exact commit or tree hash and staged versus working scope.
2. Selected profile, canonical gate IDs, path set, and configuration digest.
3. Python and dependency-lock identity plus machine or CI runner identity.
4. Cache state, instrumentation state, and feature-switch state.
5. Start and end time, duration, subprocess count, output bytes, and status.

If any comparison field differs, the executions are not a clean matched pair.

### Required result parity

The comparison must evaluate all of the following, not status alone:

- exit status and PASS, FAIL, or blocked classification;
- normalized hard-finding IDs, warning IDs, counts, and authority metadata;
- selected paths, canonical gate IDs, scope, and exact tree;
- generated changes, final staged tree, residue, and index restoration;
- receipt schema, complete finding retention, output counts, and hashes.

Legacy FAIL is blocking during `shadow_planner`, even when the candidate
passes. Candidate FAIL with legacy PASS is also a repair condition. Any
unexplained selected-path, hard-finding, authority-field, exit-status,
generated-state, or receipt-loss mismatch blocks advancement. Majority
agreement, performance improvement, and repeated execution do not resolve a
semantic mismatch.

### Minimum evidence before cutover

Before `planner_authoritative`, the cutover packet must retain:

- the complete P1-T03 adversarial equivalence corpus with zero unexplained
  blocking mismatch;
- at least three clean representative shadow transactions spanning affected,
  checkpoint, and full behavior;
- one uncached final staged-tree checkpoint comparison;
- scheduled-full and CI evidence when those surfaces are being cut over;
- all non-negotiable v19 safety-budget results;
- profile-specific performance evidence required by any hard guard proposed
  for activation.

`V19-PERF-TRACE-001` remains provisional until at least three matched pairs
exist for each of affected, checkpoint, and full profiles. Three full-profile
pairs satisfy only the full-profile portion. No hard performance guard may be
activated from an aggregate that lacks its required profile evidence.

## Rollback triggers

The first occurrence of any safety trigger blocks cutover or restores the last
authoritative path:

| Trigger | Immediate response | Required proof before resumption |
| --- | --- | --- |
| Missing hard finding or authority field | Set `planner_mode=off`; restore legacy authority | Repaired adversarial fixture and matched live parity |
| Wrong path or gate selection | Disable candidate selection and cache | Change-family and unknown-path fail-closed tests pass |
| Wrong staged tree, residue, or index restoration failure | Abort transaction and restore the entry index | No-commit checkpoint drill proves exact final state |
| Cross-tree, cross-environment, or cross-implementation cache reuse | Set `cache_mode=off`; discard the suspect local receipt | Conservative cache-key audit and uncached parity pass |
| Compact output loses a finding, count, group, or receipt reference | Set `output_mode=legacy` | Full-receipt and adversarial output parity pass |
| Activated performance hard guard is exceeded | Restore the last authoritative orchestration for that profile | Three comparable PASS results satisfy the guard after repair |
| Legacy fallback fails during migration | Halt retirement and restore the fallback wrapper | Explicit fallback smoke and full acceptance pass |
| Unique live acceptance or invariant disappears | Restore the removed gate or live case | Obligation inventory proves coverage is present again |

Rollback never edits completed task history, canonical science, ontology,
manuscripts, physics registries, or scientific state. Suspect local caches and
receipts may be invalidated because they are non-authoritative operational
state.

## Restoration matrix

| Surface | Restoration action | Acceptance evidence |
| --- | --- | --- |
| Make | Restore the last authoritative target composition or force the legacy wrapper | Exact target plan plus legacy full PASS |
| CI | Restore the last accepted workflow and unfiltered scheduled-full job | Official workflow dispatch with complete gate union |
| Skills and roles | Restore explicit legacy validation obligations without changing role authority | Skill classification, role, documentation-impact, and research-control validation |
| Checkpoint | Force the legacy checkpoint path, restore entry index on failure, and validate the final staged tree | No-commit drill plus governed transaction PASS |
| Cache | Disable reads and writes; run uncached | Exact-tree uncached receipt and no suspect reuse |
| Output | Restore legacy rendering while retaining full receipts | Status and full-finding parity |

Restoration changes orchestration only. It must not rewrite scientific state or
treat validation PASS as claim authority.

## Destructive retirement citation gate

Any AgentJob that deletes, disables, or makes unreachable a legacy command
owner, wrapper, alias, validator, live acceptance, scheduled path, or fallback
must cite this policy in its `allowed_read_paths` and completion `source_basis`.
It must also name the replacement obligation, parity evidence, rollback switch,
reference-migration evidence, and retained historical-readability path.

The current v19 future-task inventory is:

| Plan task | Retirement character | Citation disposition |
| --- | --- | --- |
| `P3-T04` | Conditional retirement of misleading documentation modes | Required only if the retirement branch is selected |
| `P9-T04` | Assessment only | No deletion in that task; any later retirement must cite this policy |
| `P11-T05` | Destructive compatibility retirement | Citation is mandatory in its AgentJob and deprecation ledger |

No active destructive-retirement AgentJob exists at P1-T05. A future job that
omits the citation is invalid even if the implementation plan names the
retirement generally.

## Evidence retention and authority

Full raw comparison and trace output stays in ignored local receipt storage or
an authorized task artifact when required. Tracked compact reports record
hashes, counts, statuses, relevant gate IDs, and the no-physics boundary. Raw
local evidence is not an independent source of project or scientific
authority.

`handoff-0740` and `EqSrc_family_closure_repair_or_stress` remain the ordinary
research authority. This policy does not supersede either surface.
