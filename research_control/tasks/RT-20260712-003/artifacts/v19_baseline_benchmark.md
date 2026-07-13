<!-- authority: control -->

# V19 P0-T03 baseline benchmark

## Result

P0-T03 captured both the exact current P0-T02 state and a repaired clean-clone
baseline. The exact current tree ran 584 tests in 565.154 seconds: 582 passed
and two state-contract tests failed because the primary worktree is intentionally
dirty and its generated folder map lacks the five rows that appear only after
P0-T02 is represented as tracked. The test bootstrap changed only
`FOLDER_MAP.md`; that change was removed and the primary fingerprint returned
exactly to `4019c100423a662610ae1e0c50308b9d587f5f5526a970aed320c61d1783086a`.

A disposable clean clone containing the same P0-T02 tree plus only those five
observed generated folder-map rows passed all 584 tests in 515.455 seconds. Its
working fingerprint was unchanged by the suite. Both runs are single
indicative measurements with temporary instrumentation overhead; neither is a
controlled performance comparison with the 507.215-second historical run.

## Focused baseline conditions

- The authoritative legacy Make path is currently blocked before the suite.
  With the real index, registered P0-T02 files are untracked. With an alternate
  index, memory validate-only reports the P0-T02 folder map stale. P0-T03 did
  not stage, regenerate, or repair P0-T02.
- Dependency-graph freshness still fails for JSON, Markdown, and DOT outputs;
  the observed check took 48.742 seconds.
- Task-index validation still reports four hard freshness/parity errors and
  297 historical warnings; the observed check took 1.108 seconds.
- Local vault lint still reports 11 ignored local-retrieval issues. Three runs
  took 0.297, 0.231, and 0.230 seconds; the median was 0.231 seconds.

## Instrumented clean baseline

- 584 tests passed.
- Nine dependency-graph builds were derived from current test call paths.
- 18,457 registry CSV parser constructions were observed.
- 90 Python `subprocess.Popen` launches were observed; sampled unique
  descendants were a lower bound of 33.
- Captured output was 2,697 bytes, approximately 674 characters-per-four token
  proxy units.
- The legacy path has no result-cache contract, so cache hits and misses are
  recorded as zero rather than interpreted as cold-cache evidence.

Raw stdout and stderr remain in ignored `.local/v19-baseline/` directories.
The durable JSON receipt records a SHA-256 hash for every retained log and raw
measurement manifest.

## Authority boundary

This is project-system performance and failure-state evidence only. It changes
no validator, test, orchestration source, scientific claim, Distance-to-GR
status, ontology, benchmark status, or research handoff. `handoff-0740` remains
the ordinary scientific continuation authority. The next v19 task is P0-T04.
