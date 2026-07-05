# Source Model Zoo Validation and Selector v16

## Status

- Task: `RT-20260705-021`
- Plan task: `P10-T03`
- Status: support-only validation and selector receipt.
- Physics authority: none.
- Selected next use: target-import attack suite.
- Immediate continuation route: `P11-T01` negative-result reader-language audit.

This artifact validates `research_control/design/source_model_zoo_v1.md`
against the P10-T03 checklist. It does not adopt source laws, discharge
`EqSrc`, adopt `RetainH` or `GenH`, derive matter coupling, introduce detector
semantics, recover Einstein equations, recover benchmark behavior, or promote
any physics claim.

## Source Basis

- `implementations_plans/recommendations_implementation_plan_continue_task-v16.md`
- `research_control/handoffs/handoff-0593.yaml`
- `research_control/design/source_model_zoo_schema_v1.md`
- `research_control/design/source_model_zoo_v1.md`
- `research_control/design/source_certificate_instance_library_index_v1.md`

## Validation Method

Each model was checked for the following P10-T03 requirements:

1. finite or local source scope;
2. allowed reuse;
3. blocked overreads;
4. no matter-coupling claim;
5. no detector-semantics claim;
6. no Einstein-equation claim;
7. no benchmark-recovery claim;
8. at least one certificate instance or obstruction mapping.

The check is source-side and syntactic/semantic over the registered project
control artifact. It is not a proof checker and not physics evidence.

## Model Validation Matrix

| Model | Scope | Reuse present | Blocked overreads present | No matter coupling | No detector semantics | No Einstein equations | No benchmark recovery | Certificate or obstruction evidence | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SMZ-IDENTITY-001` | finite | yes | yes | yes | yes | yes | yes | `SCI-NEG-VALIDATOR-PASS-001` | pass |
| `SMZ-TRANSPORT-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-TRANSPORT-001`; `SCI-NEG-MALFORMED-001` | pass |
| `SMZ-RELABEL-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-INVARIANCE-001`; `SCI-NEG-DETECTOR-001` | pass |
| `SMZ-FACTOR-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-FACTORIZATION-001`; `SCI-NEG-FACTOR-CHANGE-001` | pass |
| `SMZ-GAP-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-NEG-MISSING-001`; `SCI-NEG-MALFORMED-001` | pass |
| `SMZ-RRE-SEP-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-NEG-SCOPED-EVIDENCE-001`; `OB-SMZ-RRE-SEP-001` | pass |
| `SMZ-TARGET-REJECT-001` | finite/local | yes | yes | yes | yes | yes | yes | `SCI-NEG-TARGET-METRIC-001`; `SCI-NEG-STRESS-ENERGY-001` | pass |
| `SMZ-DETECTOR-REJECT-001` | finite/local | yes | yes | yes | attempted detector input is rejected | yes | yes | `SCI-NEG-DETECTOR-001` | pass |

## Aggregate Result

- Models checked: 8.
- Models passing P10-T03 checks: 8.
- Models failing P10-T03 checks: 0.
- Models with finite/local scope: 8.
- Models with allowed reuse and blocked overreads: 8.
- Models with at least one certificate instance or obstruction: 8.
- Models claiming matter coupling: 0.
- Models claiming detector semantics as source authority: 0.
- Models claiming Einstein equations: 0.
- Models claiming benchmark recovery: 0.

## Selected Next Use

Selected next use: target-import attack suite.

Rationale:

- The model zoo contains direct target-import, detector-semantics, stress-energy,
  and benchmark overread guards.
- P14 explicitly requires attack fixtures for hidden target-side or
  process-authority imports.
- The zoo is already finite/local, so it can support deterministic attack-suite
  fixtures without changing physics authority.
- Selecting this future use does not skip P11 through P13. It records the
  intended reuse when the plan reaches P14.

Non-selected uses:

- Formalization support: available later, but less directly matched to the
  current v16 risk being mitigated.
- Coupling-law target candidate testing: deferred because P10-T03 does not
  authorize matter-coupling derivation or adoption.
- Red-team packet inclusion: useful as supporting material, but P13 first needs
  a one-question packet.
- Negative-result explainer: useful for P11, but the zoo's strongest direct
  contribution is adversarial target-import coverage.
- No-op with evidence: unnecessary because a concrete later use is available.

## Selector Guard

The selected next use is future reuse only. It does not create a standing gate,
does not validate a physics theorem, and does not convert model-zoo records into
source-law adoption, proof authority, benchmark authority, or completed
derivation authority.

## Machine-Readable Receipt

```yaml
validation_packet_id: "source_model_zoo_validation_and_selector_v16"
task_id: "RT-20260705-021"
validated_artifact: "research_control/design/source_model_zoo_v1.md"
models_checked: 8
models_passing: 8
models_failing: 0
finite_or_local_scope_all: true
allowed_reuse_all: true
blocked_overreads_all: true
certificate_or_obstruction_all: true
matter_coupling_claim_count: 0
detector_semantics_claim_count: 0
einstein_equation_claim_count: 0
benchmark_recovery_claim_count: 0
selected_next_use: "target_import_attack_suite"
immediate_next_plan_task: "P11-T01"
physics_promotion_authorized: false
proof_authority: false
completed_derivation_authorized: false
```

## References

Plan and local source basis listed in `Source Basis`; citation formatting is
not used for local control artifacts in this receipt.
