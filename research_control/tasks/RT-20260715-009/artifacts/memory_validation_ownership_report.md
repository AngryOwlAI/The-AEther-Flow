<!-- authority: control -->

# P3-T03 Memory Validation Ownership Report

## Result

P3-T03 separates the three memory validation concerns into independently
selectable gates while retaining the legacy composite profile:

| Gate ID | Owner and input | Output and acceptance meaning |
| --- | --- | --- |
| `memory_core` | Memory-system tracked registries and generated tracked surfaces through one immutable snapshot | Blocking tracked-state report with 13 stable check IDs. Publication and local retrieval are absent. |
| `publication_validation` | `scripts/validate_publication_process.py` over the selected repository root | Blocking publication-process report with structured error warning and finding counts. This is the sole gate that directly invokes the active publication validator. |
| `local_retrieval_health` | Local Obsidian mirror semantic extracts SQLite index and their tracked registry bindings | Advisory report by default. An authorized memory-maintenance caller may explicitly select required mode. The gate is read-only and has no scientific authority. |
| `memory_legacy_composite` | The three explicit gate results above | Compatibility profile preserving the current aggregate PASS or FAIL result until planned legacy retirement. |

The live current-state receipt records PASS for all four surfaces. Memory core
reports 13 checks and zero findings. Each external gate reports one check and
zero findings. The composite reports 15 checks and zero findings.

## Implementation boundary

- `memory_operations.py` now composes independently owned validation reports
  without changing child finding IDs.
- `publication.py` provides the only direct adapter to the active publication
  validator and exposes a compact JSON CLI receipt.
- `local_retrieval.py` exposes advisory local-cache health and an explicit
  maintenance-only required mode. It does not write tracked or local files.
- `bootstrap_memory_system.py` keeps compatibility helper names but routes
  them and `validate_all()` through the explicit adapters.
- Focused tests prove publication blocking behavior, local retrieval advisory
  behavior, explicit required-mode behavior, stable child finding identity,
  and legacy composition.

The compatibility wiring edit is the single tracked exception to the four
planned P3-T03 paths. It is necessary to avoid retaining a second publication
execution owner. No Make CI checkpoint skill role or P3-T04 behavior changed.

## Equivalence and safety evidence

- Seven focused memory-operation and ownership tests pass.
- Twelve independent publication-process fixture tests pass.
- All 53 existing memory-system failure and compatibility fixtures pass.
- Live `publication_validation`, `local_retrieval_health`, `memory_core`, and
  `memory_legacy_composite` receipts pass.
- `bootstrap_memory_system.py --validate-only` preserves the current aggregate
  PASS result.
- A synthetic stale local-cache finding remains a warning in default mode and
  becomes an error only under explicit required mode. It never enters
  `memory_core`.
- Publication errors remain errors in both their independent gate and the
  legacy composite fixture.

Full command receipts and source hashes are in
`memory_validation_ownership_receipt.json`. Validation evidence is operational
only. It does not change canonical physics sources, Distance-to-GR status,
proof authority, benchmark authority, Gate Chair authority, or ordinary
research routing.

## Preserved authority

`handoff-0740` and its `EqSrc_family_closure_repair_or_stress` route remain the
ordinary research authority. This project-system task does not update
`program_state.yaml`, `current_frontier.md`, or any research handoff.

On checkpoint PASS the dependency-ready next v19 task is P3-T04, separately
bounded under its own Memory-System Maintainer AgentJob.
