<!-- authority: control -->

# Handoff handoff-0908 — P9-T01 source-derived benchmark protocol

## Disposition

P9-T01 is complete and ready for one governed checkpoint.

The packet defines:

- `SourceDerivedBenchmarkProtocol_v1`;
- six typed benchmark-case templates, all `NOT_RUN`;
- `TargetImportFirewall_v1`;
- `TargetImportFirewallSoundness_v1`; and
- a Gate E readiness checklist with overall status
  `NOT_READY_NO_BENCHMARK_CASE_EXECUTED`.

The theorem is deliberately protocol-level. Given a complete properly typed
finite provenance DAG, no forbidden or target root reaching the source stage,
immutable source outputs sealed before target-oracle access, and frozen
revision identity, topological induction shows that sealed source outputs are
invariant under target-root variation. This prevents agreement from being
manufactured by reusing the target theory upstream. It does not establish that
the source theory produces a physical observable.

## Scientific status

- Benchmark cases executed: `0`.
- Benchmark cases passed: `0`.
- Gate D: unchanged `NOT_READY`.
- Gate E: `NOT_READY_NO_BENCHMARK_CASE_EXECUTED`.
- Effective metric, physical dynamics, Einstein equations, and exact-GR
  recovery: not established.
- Distance-to-GR delta: none.
- Benchmark promotion, proof, publication, and push authority: absent.

The protocol treats target metrics, target solutions, the Einstein–Hilbert
action, Einstein equations, target residuals, desired agreement, target-tuned
parameters, target-contaminated code or training data, and benchmark success as
forbidden upstream roots. The target oracle remains closed until source
outputs, code, environment, randomness policy, and provenance hashes are
sealed.

## Next bounded route

First run one governed checkpoint for
`AJ-RT-20260729-012-001`.

After checkpoint, execute at most one P9-T02
`candidate-constructor@0.2.0` packet:

> Construct or derive a source state whose effective geometry, matter vacuum,
> and perturbative behavior recover the Minkowski benchmark within declared
> scope.

P9-T02 must freeze the case manifest before target comparison. If the current
source ontology does not supply a required input or derived object, the result
must be `FAIL` or `INCONCLUSIVE`; it may not repair the source calculation
using target data. Any oracle-informed rerun is a new nonblind revision and
cannot count as the original benchmark result.

## Claim boundary

This handoff authorizes only the checkpoint and, afterward, one bounded
source-only P9-T02 construction or precise failure/inconclusive packet. It does
not authorize target-informed tuning, a benchmark pass or promotion, Gate D
repair, a Gate E verdict, canonical ontology or source-law change, physical
metric or dynamics adoption, Einstein equations, exact-GR recovery, proof,
publication, push, completed derivation, global no-go, or future source-
extension impossibility.

## Evidence

- Completion:
  `research_control/tasks/RT-20260729-012/jobs/completions/AJC-AJ-RT-20260729-012-001.yaml`
  (`645d5934a58ded9cafbbbd3af59ad9d3aa91efd5ec9bfe51ab231fd7488c07c4`)
- Protocol:
  `research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex`
  (`88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007`)
- Case schema:
  `research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_case_schema_v1.yaml`
  (`5045de8fbaeb6c80b89ec88b71143a8aeaca1c892efadc4b7293cb438ee808d8`)
- Firewall:
  `research_control/tasks/RT-20260729-012/artifacts/target_import_firewall_v1.yaml`
  (`ccb9297f817a9b4eeb886834a510e1f21d518a2668bc3fde9695b909d6884acf`)
- Gate E checklist:
  `research_control/tasks/RT-20260729-012/artifacts/gate_e_readiness_checklist_v1.yaml`
  (`a9cefe08cc6bc8b0653fdfc72144d24e54fb14e565f8a499be49093bc615bb76`)

No project-improvement sidecar is required.
