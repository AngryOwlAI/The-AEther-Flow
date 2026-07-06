<!-- authority: science_draft -->

# Fail-Closed Certificate Evaluation

## Status

```yaml
formalization_id: "support_formalization_fail_closed_certificate_evaluation_v1"
checker_id: "fail_closed_certificate_evaluation_support_formalization"
checker_version: "0.1.0"
plan_task_id: "P8-T02"
support_only: true
proof_authority: false
physics_promotion_authorized: false
source_artifact_path: "research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex"
proof_normal_form_row_id: "PNF-RT-20260706-014-003"
```

This directory contains the v17 P8-T02 support-only finite checker for the
selected fragment `fail_closed_certificate_evaluation`. It mechanizes a finite
record evaluator for source certificate branches. It does not prove a theorem,
adopt a source law, derive matter coupling, derive Einstein equations, promote
the benchmark, issue a Gate Chair verdict, or complete the derivation.

## Files

| File | Purpose |
| --- | --- |
| `fail_closed_certificate_evaluation.py` | Deterministic finite checker and JSON report CLI. |
| `test_fail_closed_certificate_evaluation.py` | Focused local test harness. |
| `validation_report.json` | Generated P8-T02 support-only checker report. |

## Fragment

The checker evaluates one `CertificateRecord` at a time. A valid source-side
record with declared source scope, declared domain and codomain, a matching
witness map, and no forbidden imports returns
`declared_equivalence_allowed`. Missing, malformed, target-importing,
detector-semantics, stress-energy, matter-action, benchmark, process-authority,
generated-authority, or scoped-evidence branches return
`declared_equivalence_blocked` with `fail_closed: true`.

## Local Commands

```zsh
.venv/bin/python -m unittest discover -s research_control/formalization/fail_closed_certificate_evaluation -p 'test_*.py'
.venv/bin/python research_control/formalization/fail_closed_certificate_evaluation/fail_closed_certificate_evaluation.py --json-output research_control/formalization/fail_closed_certificate_evaluation/validation_report.json --json
```

## Boundary

The checker is support-only. A passing report is operational reproducibility
evidence for finite branch behavior only. It has `proof_authority: false`,
`support_only: true`, and `physics_promotion_authorized: false`.

Blocked overreads include canonical ontology edit, source-law adoption,
`MetricData(E)` adoption, `g_eff` adoption or scope expansion, coupling-law
adoption, matter-coupling derivation or adoption, stress-energy semantics,
stress-energy tensor, detector semantics, matter action, Einstein equations,
benchmark promotion, Gate Chair verdict, completed derivation, future
source-extension impossibility, and global theory rejection.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v17* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Source certificate operation laws
v1* [Research-control TeX artifact].

The AEther-Flow Research Project. (2026c). *Support-only formalization target
selector* [Research-control task artifact].
