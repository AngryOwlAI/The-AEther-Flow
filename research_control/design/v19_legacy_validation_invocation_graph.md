<!-- authority: control -->

# V19 legacy validation invocation and obligation graph

This P0-T04 inventory maps the current legacy validation owners without changing command behavior. Provisional gate IDs are seed identifiers for the later canonical manifest; role and skill declarations are obligations, not independent execution evidence.

## Result

- Status: `PASS`
- Provisional gates: `37`
- Concrete validation invocations: `53`
- Skill obligations: `6`
- Role obligations: `32` across 13 active roles
- Direct same-state subset/superset pairs: `3`
- Legitimate cross-scope repetitions: `6`
- Unresolved invocations: `0`
- Physics or Distance-to-GR delta: `none`

## Owner counts

| Owner class | Invocations |
| --- | ---: |
| `checkpoint` | 16 |
| `ci` | 2 |
| `local_runner` | 15 |
| `make` | 20 |

## Direct same-state supersets

| Subset | Superset | Evidence |
| --- | --- | --- |
| `MPC-08` | `MPC-09` | Same owner, same tree state; `--check-diff` runs the core spine and then adds diff/claim checks. |
| `RUN-10` | `RUN-11` | Same owner, same tree state; `--check-diff` runs the core spine and then adds diff/claim checks. |
| `CHK-W06` | `CHK-W07` | Same owner, same tree state; `--check-diff` runs the core spine and then adds diff/claim checks. |

Working-tree and staged-tree repetitions are deliberately not collapsed. The final checkpoint commands with explicit `--staged` or `--staged-only` inspect the Git index. Signal parity and memory validate-only lack staged modes, so their final checkpoint nodes are labeled `working_files_index_synchronized`, not staged-index evidence.

## Current owner drift

| Finding | Class | Summary |
| --- | --- | --- |
| `DRIFT-01` | `hard_finding` | Make/CI and the local runner own different command sets. |
| `DRIFT-02` | `hard_finding` | The local runner is not CI-equivalent. |
| `DRIFT-03` | `direct_duplicate` | Plain research-control validation immediately precedes its same-state --check-diff superset in three owners. |
| `DRIFT-04` | `nested_duplicate` | Memory validate-only already invokes publication validation before Make invokes publication validation directly. |
| `DRIFT-05` | `cross_job_duplicate` | GitHub's separate memory job repeats memory validate-only already nested in the main Make job. |
| `DRIFT-06` | `scope_guard` | Checkpoint working and final validations cannot be collapsed solely by command text. |
| `DRIFT-07` | `obligation_drift` | Role and skill declarations use labels and command strings that do not form a shared executable plan. |
| `DRIFT-08` | `local_authority` | Local retrieval health is mixed into validate-memory but is non-authoritative for tracked project state. |

## Nested relationships

- Memory bootstrap and validate-only invoke publication-process validation and Mermaid source validation internally.
- Research-control `--check-diff` runs the complete research-control core and integrates changed-claim validation.
- GitHub's main job invokes the Make project-control wrapper; the separate memory job repeats memory validate-only in another clean-checkout job.
- The checkpoint wrapper performs bounded synchronization, conditional PDF generation, working-file validation, explicit staged-index gates, residue checks, and optional commit mechanics.

## Obligation interpretation

The 13 active roles declare validator labels. Their current label frequencies are:

- `bootstrap_memory_system`: 2
- `check_diff`: 1
- `claim_boundary_phrase_scan`: 7
- `scripts/validate_publication_process.py --root .`: 1
- `unittest`: 3
- `validate_documentation_impact`: 5
- `validate_research_control`: 13

`claim_boundary_phrase_scan` is satisfied inside the research-control core; it is not a requirement to spawn a separate process once per declaring role. Skill command blocks likewise compile to conditional obligations tied to a transaction scope.

## P5 manifest seed

The JSON graph is suitable seed input for P5 because each provisional gate records implementation, authority class, mutation behavior, condition, and nested gates. Canonical evidence identity, supersedence, profiles, cache keys, and orchestration authority remain deferred to their named v19 tasks.

## Authority boundary

This graph is operational control evidence only. It does not change validators, tests, CI, Make, skills, roles, checkpoint behavior, scientific sources, claim status, benchmark status, proof authority, or the ordinary research route at `handoff-0740`.
