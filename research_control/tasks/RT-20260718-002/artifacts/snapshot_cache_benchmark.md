<!-- authority: control -->

# P10-T06 shared-snapshot and cache benchmark

## Verdict

`PASS_WITH_ACTIVATION_REJECTED`.

The controlled benchmark establishes shared-snapshot parse reduction, correct
warm exact-tree reuse, bounded cache storage, and eviction safety. It does not
support planner-authoritative cache activation. The live 37-gate manifest has
zero `exact_tree` gates, the production runner supplies no cache context, the
controlled corpus is not comparable to the frozen full or affected acceptance
corpus, and the short affected warm path remains slower than cache-disabled
execution.

The correct operational decision is to keep cache mode off by default.
Production snapshot, cache, executor, manifest, planner, runner, checkpoint,
CI, ordinary research, and physics sources remain unchanged.

## Environment and comparability

All controlled runs used commit
`e8e542fc99e2ca2ac91c5a81e44bb4290f194d8b` on `Mac15,14`, Apple M3 Ultra,
96 GiB RAM, macOS 26.5.2, Python 3.12.13, and dependency digest
`sha256:7bc3bca027f6d2be2fcb2ca0e3d9568a09c07a6d0d30b774073501da06ced98f`.
Those fields match the P0-T03 environment.

The plan shapes use 13 and 36 controlled read-and-hash gates. They preserve the
relevant cache identity, result, receipt, concurrency, and plan-size behavior,
but they are not the frozen representative affected corpus or the complete
full-profile gate union. Timing results are therefore controlled trend evidence,
not activated performance-guard or cutover evidence.

## Shared snapshot

| Shape | Consumers | Direct registry parses | Shared registry parses | Parse reduction | Direct bytes read | Shared bytes read | Result parity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Affected | 13 | 39 | 3 | 92.308% | 64,801,620 | 4,984,740 | PASS |
| Full | 36 | 108 | 3 | 97.222% | 179,450,640 | 4,984,740 | PASS |

The snapshot reduces repeated reads, parses, and hashes to one per declared
registry. Its isolated wall time is slower than direct parsing because every
consumer access performs exact-tree freshness checks. This packet therefore
claims parse reduction, not a general snapshot runtime improvement.

## Cache timing

Each mode has three retained repetitions. Medians are monotonic wall time.

| Shape | Disabled | Empty no-hit | Cold read/write | Warm hit | Warm vs cold | Warm vs disabled |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Affected, 13 gates | 0.357046 s | 0.546396 s | 0.555489 s | 0.422380 s | 23.962% faster | 18.298% slower |
| Full, 36 gates | 0.526662 s | 0.733924 s | 0.873807 s | 0.432476 s | 50.507% faster | 17.884% faster |

Every warm run had all gates hit, launched zero subprocesses, read and hashed
zero source files, and reproduced the disabled/cold normalized status,
obligations, and child-gate evidence. There were no false hits.

No-hit lookup overhead was 53.032% for the affected shape and 39.354% for the
full shape. Cold publication overhead was 55.579% and 65.914%, respectively.
Those costs are material even though the absolute controlled cold medians are
well below the provisional 45-second and 180-second profile guards.

## Storage and eviction

The 13-gate cold cache stored 47,167 bytes, or 3,628 bytes per entry. The
36-gate cold cache stored 129,241 bytes, or 3,590 bytes per entry.

An independent 13-gate drill constrained the cache to five entries. Both
executions passed with five valid entries, zero invalid entries, and 18,126
bytes after the repeat. The repeat had zero hits because the working set
exceeded the cap and thrashed. Eviction is bounded and safe, but an undersized
cache is not beneficial.

## Activation decision

Activation is rejected for this packet:

- the live manifest has 37 gates and all 37 remain `ineligible`;
- `scripts/validation/run.py` supplies no `ExecutionCacheContext`;
- the short affected warm path does not beat cache-disabled execution;
- cold and empty-lookup overhead is material;
- the controlled plan shapes are not a comparable cutover corpus; and
- P10-T06 authorizes measurement only, not production-source mutation.

The evidence supports retaining the optional implementation behind its explicit
off-by-default boundary. A future activation packet would need separately
authorized live eligibility, production context integration, and at least
three comparable successful runs over the declared affected and full gate
unions.

## Evidence boundary

The complete 209,952-byte raw result is retained locally at
`.local/p10_t06_snapshot_cache_benchmark_result.json` with digest
`sha256:08ada943b662c755ec40f1f36eb45eadbcedf8bd673f2e900e09a5d084fe3995`.
Twenty-six full executor receipts remain under
`.local/p10-t06-benchmark/receipts`; they are untracked operational evidence,
not source authority.

Benchmark execution left the tracked status exactly unchanged. This report
changes no scientific claim, Distance-to-GR row, ontology, proof status,
benchmark-promotion status, or ordinary research handoff.
