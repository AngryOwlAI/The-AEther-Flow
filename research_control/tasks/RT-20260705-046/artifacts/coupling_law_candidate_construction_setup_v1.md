<!-- authority: science_draft -->

# Coupling-Law Candidate Construction Setup v1

Task: `RT-20260705-046`

AgentJob: `AJ-RT-20260705-046-001`

Plan task: `P1-T01`

Status: `draft/control candidate-construction setup only`

## Control Boundary

This artifact implements v17 `P1-T01`: candidate-constructor packet setup.
It defines one source-side candidate-construction envelope for a later
`P1-T02` attempt. It does not construct `K_{E_*}`, adopt a coupling law,
derive matter coupling, adopt matter semantics, adopt detector semantics,
import stress-energy semantics, construct a stress-energy tensor, import a
matter action, derive Einstein equations, promote benchmark status, or claim a
completed derivation.

## Source Basis

The setup reads the following tracked sources as authority:

| Source | Use in setup |
| --- | --- |
| `source_side_coupling_law_target_specification_v1.tex` | Provides `SMScope(E)`, `SCLBundle(E)`, `DetPlaceholder(E)`, `NoTargetCouplingImportGuard_v1`, `CouplingLawCandidateValidityPredicate_v1`, fail-closed branches, and finite/local witness obligation. |
| `source_side_matter_semantics_object_certificate_manifest_v1.tex` | Provides source-side matter-semantics objects, records, bridge candidates, declared `RR_E` objects, and certificate classes. |
| `source_certificate_algebra_primitives_v1.tex` | Provides source certificate record fields, primitive certificate kinds, and missing or malformed certificate states. |
| `source_certificate_operation_laws_v1.tex` | Provides conditional operation laws and fail-closed behavior for malformed, missing, target-importing, and process-authority-dependent certificates. |
| `no_target_import_guard_map.md` | Provides forbidden import categories and process-authority laundering checks. |
| `matter_coupling_dependency_dag_v1.md` | Provides the matter-coupling dependency context and blocked downstream targets. |

## Candidate Setup

```yaml
candidate_setup:
  candidate_name: "SourceCouplingLawCandidate_EStar_v1"
  source_event_or_scope_symbol: "E_*"
  source_input_scope: "SMScope(E_*)"
  candidate_relation_symbol: "K_{E_*}"
  certificate_bundle_symbol: "SCLBundle(E_*)"
  detector_placeholder_symbol: "DetPlaceholder(E_*)"
  finite_local_witness_obligation: true
  no_target_import_guard_required: true
  max_candidate_count: 1
  adoption_requested: false
```

`SourceCouplingLawCandidate_EStar_v1` is the only candidate target named by
this setup. `K_{E_*}` is reserved as the relation or partial map to be
constructed or obstructed by P1-T02.

## Required Fields From The V16 Validity Predicate

P1-T02 must treat the following fields as hard requirements:

1. `SMScope(E_*)` is declared and finite or locally finite.
2. `SCLBundle(E_*)` contains explicit valid source certificates.
3. `DetPlaceholder(E_*)` is supplied as a source-side placeholder or explicitly
   marked `missing_and_blocked`.
4. `NoTargetCouplingImportGuard_v1` passes.
5. `K_{E_*}` names a source-side relation or partial map whose domain,
   codomain, witness payloads, and guards are source-side.
6. The finite/local witness obligation is satisfied by a concrete witness
   declaration or by one precise fail-closed obstruction.

If any field fails, P1-T02 must return exactly one primary fail-closed branch.
It must not continue by substituting scoped evidence status, registry status,
validator status, role identity, handoff status, approval status, generated
derivatives, local cache state, file order, or commit state as mathematical
premises.

## P1-T02 Construction Envelope

The next candidate-constructor packet must either:

```text
construct K_{E_*} under SourceCouplingLawCandidate_EStar_v1
```

or:

```text
return one precise construction obstruction under the V16 fail-closed branch family
```

Allowed primary obstruction families are inherited from the v16 target
specification:

- required source certificate absent;
- certificate malformed or object-mismatched;
- target, metric, benchmark, stress-energy, action, or Einstein import;
- detector semantics used or placeholder absent without blocked status;
- source-side relation or partial map missing;
- process authority used as mathematical premise;
- scoped evidence read as adoption;
- finite/local witness obligation not met.

## No-Target Import Guard

P1-T02 must reject the following as mathematical premises:

- target topology, target open sets, target neighborhoods, or target manifold
  topology;
- target smooth atlas, coordinate charts, or target differentiability class;
- target Lorentzian metric, metric signature, or proper time;
- empirical detector semantics or detector protocol;
- exact-GR benchmark behavior;
- stress-energy semantics, stress-energy tensor, or matter action;
- generated wiki, generated index, generated HTML, generated PDF, Obsidian
  notes, semantic extracts, SQLite memory, or local cache state;
- registry rows, validators, roles, handoffs, approvals, commits, or file
  order as proof.

## Distance-To-GR Effect

This setup contributes one draft/control definition payload: a bounded
candidate-construction envelope for `SourceCouplingLawCandidate_EStar_v1`.
It does not change the Distance-to-GR ledger. The matter-coupling row remains
`accepted_as_scoped_evidence_precondition`, and matter coupling remains not
derived and not adopted.

## Done Criteria Check

| Criterion | Status | Evidence |
| --- | --- | --- |
| Exactly one candidate target is named | PASS | `SourceCouplingLawCandidate_EStar_v1` is the only setup candidate. |
| Required fields from the v16 validity predicate are named | PASS | The six hard requirements above mirror the target specification. |
| The next task must construct or fail with one precise obstruction | PASS | P1-T02 construction envelope requires `K_{E_*}` construction or one primary fail-closed obstruction. |
| No adoption or matter-coupling derivation is claimed | PASS | All adoption and downstream-promotion claims are explicitly blocked. |

## Forbidden Conclusions

This setup is not source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1`
adoption, unrestricted `RR_E` theorem authority, matter-semantics adoption,
detector-semantics adoption, coupling-law adoption, matter-coupling derivation
or adoption, stress-energy semantics, stress-energy tensor construction,
matter-action import, Einstein-equation derivation, benchmark promotion, Gate
Chair closure, proof authority, completed derivation, future source-extension
impossibility, or global theory rejection.

## Next Route

Run one bounded v17 `P1-T02` `candidate-constructor@0.2.0` packet. That packet
must construct `K_{E_*}` under this setup or return one precise construction
obstruction before any audit, stress, accepted-language calibration, detector
replacement, metric-use ledger, dashboard, CI, methodology, or final v17 task.

## Source Materials

The AEther-Flow Research Project. (2026a). *Source-side coupling-law target
specification under explicit certificates v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex`

The AEther-Flow Research Project. (2026b). *Source-side matter-semantics object
and certificate manifest v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex`

The AEther-Flow Research Project. (2026c). *Source certificate algebra
primitives v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex`

The AEther-Flow Research Project. (2026d). *Source certificate operation laws
and fail-closed lemma v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`

The AEther-Flow Research Project. (2026e). *No-target-import guard map*
[Internal control note]. `research_control/design/no_target_import_guard_map.md`

The AEther-Flow Research Project. (2026f). *Matter-coupling dependency DAG v1*
[Internal control artifact]. `research_control/design/matter_coupling_dependency_dag_v1.md`
