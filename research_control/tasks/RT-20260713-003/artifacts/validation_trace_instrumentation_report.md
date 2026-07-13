<!-- authority: control -->

# P1-T04 validation trace instrumentation report

Status: `PASS`

## Result

P1-T04 adds an opt-in standard-library trace helper and focused regression
module without changing an existing runner, Make target, checkpoint, skill,
role contract, handoff, program state, or physics source. Tracing remains
disabled by default and writes only under `.local/validation-traces/`.

The final matched pair used exact working-tree snapshot
`ce7d97cc994e4e9ef343c14639f7a1f637009a574c6c0376fbce4d5c59a4cbee`,
scope `working_tree`, and cache state `disabled`.

| Measure | Uninstrumented | Instrumented | Result |
| --- | ---: | ---: | --- |
| Legacy full-profile status | PASS | PASS | identical |
| Legacy command count | 14 | 14 | identical |
| Wall duration | 108.63 s | 110.71 s | 1.915% overhead |
| Required failures | 0 | 0 | identical |
| Advisory failures | 0 | 0 | identical |

The 1.915 percent single-pair result is below the `V19-PERF-TRACE-001`
two-percent target and five-percent rollback guard. It remains provisional
trend evidence because budget activation requires at least three matched pairs
for affected, checkpoint, and full profiles.

## Trace coverage

- 25 events, all PASS.
- 17 distinct gate IDs across depth 0 through depth 2.
- The full-profile wrapper is the root event.
- Publication validation appears as a child of memory-core validation.
- Three repeated same-identity Git executions are reported with their first
  event and parent gate; none is removed or treated as extra authority.
- Canonical identity includes gate ID, scope, tree hash, cache state, and a
  non-reversible command digest.
- Trace records retain byte counts and command digests, not validator output.

The uninstrumented and instrumented full-profile receipts have identical
command labels and return codes. Focused tests separately prove deterministic
timestamp normalization, parentage, duplicate detection, recursive Python
subprocess tracing, failure-status preservation, disabled behavior, enabled
stdout/stderr parity, canonical gate mapping, and fail-open trace writes.

## Evidence hashes

| Evidence | SHA-256 |
| --- | --- |
| `scripts/validation/trace.py` | `e562078ae0e3346b4b15e6dc9ac9582f0848d1fa635d5def9b849d7bfa34a329` |
| `tests/test_validation_trace.py` | `fc7360c7d5b4780eb3b94c88bc8ed9cb162014aefbb729ef06a3fa07c7db391d` |
| Local compact trace report | `6c7d2deea33540ef8ec7c8ff9deacf2b248a89cb8050277eda1105faeb9dca6a` |
| Local raw trace JSONL | `4e7e19adfd3ddd2c7434b6ffc8bdd78833436815fdd480ef6c9d8fb16142bd45` |
| Local uninstrumented full receipt | `0dd5b0f6ee338afff154716ac7ad92feb92c2560ff66e1244dbb0cff8f46fff5` |
| Local instrumented full receipt | `42088ca254c93f6c12b1d8fc6254dcab2d778ab3528fa317e836d577b2f163f1` |

The raw trace and full receipts remain ignored local evidence. This compact
tracked report records their hashes and bounded findings without promoting
local data to authority.

## Authority boundary

This report is project-control instrumentation evidence only. Trace absence is
not PASS evidence. Trace data is not physics proof, a scientific claim, a
Distance-to-GR advance, or authority to cache, skip, supersede, deduplicate, or
remove a gate. `handoff-0740` and `EqSrc_family_closure_repair_or_stress`
remain the ordinary research authority. P1-T05 requires its own bounded packet.
