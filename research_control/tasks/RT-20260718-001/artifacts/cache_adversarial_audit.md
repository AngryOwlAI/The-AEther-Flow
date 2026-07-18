# P10-T05 cache adversarial safety audit

Status: `PASS`

This packet attempted to falsify the exact-tree validation cache safety
contract. It added one permanent adversarial test module and did not change
production cache, executor, live manifest, checkpoint, or physics sources.

## Adversarial matrix

| Case | Attack | Required outcome | Observed outcome |
| --- | --- | --- | --- |
| Preserved timestamp | Change same-length input bytes and restore nanosecond mtime | Miss | `MISS/absent` |
| Identity matrix | Change implementation, manifest, environment, dependency lock, base ref, profile, scope, repository, and receipt schema | Miss or unresolved key | All nine blocked |
| Result corruption | Rewrite status and finding counts while recomputing outer result hash | Corrupt | Both `MISS/corrupt`; reads disabled |
| Receipt corruption | Change receipt bytes without matching content hash | Corrupt | `MISS/corrupt`; reads disabled |
| Scope isolation | Reuse working evidence as staged and cross branch/base ref | Miss | Both `MISS` |
| Concurrent publication | Race eight independent writers for one exact key | One complete entry | One `STORED`, seven `EXISTS`, no temporary residue |
| Interrupted publication | Raise during atomic rename | No partial result | `SKIPPED`, no JSON or temporary entry; retry stores and reads |
| Final safeguards | Repeat checkpoint transaction with cache enabled | Execute every time | Two adapter calls, both `BYPASSED`, both child safeguards present |
| Rollback | Clear cache and rerun with cache off | Normalized parity | Cached and uncached status, child gates, and obligations match |

## Performance evidence

- Adversarial module: 8 tests, 0.12 seconds, 1,646 bytes of verbose output.
- Test-controlled validator adapter subprocesses: 0; all synthetic adapters ran
  in-process.
- Explicit asserted lookup outcomes across the adversarial fixtures: 3 hits and
  18 misses, blocks, or mandatory bypasses.
- Combined cache-focused suite: 37 tests in 0.365 seconds.
- Stable completed-state repository suite: 954 tests in 107.521 seconds, with
  one expected skip.

These measurements establish test cost only. They are not a production
speedup claim.

## Rollback and verdict

No false hit, wrong staged tree, missing hard finding, corrupted `PASS`,
unexplained legacy/planner mismatch, or out-of-allowlist write was observed.
The mandatory rollback trigger therefore did not fire. The explicit rollback
drill cleared local cache state and reproduced the normalized uncached result.

P10-T05 passes. `P10-T06` remains a separate benchmark packet.
