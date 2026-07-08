# Detector-Placeholder Collapse Checker Spec v1

```yaml
plan_id: "recommendations_implementation_plan_continue_task-v18"
plan_task_id: "P7-T06"
checker_id: "detector_placeholder_collapse_checker"
checker_version: "0.1.0"
support_only: true
proof_authority: false
physics_promotion_authorized: false
```

## Purpose

This specification defines the v18 P7-T06 support-only checker for
placeholder-as-detector-semantics collapse. The checker exists to keep three
states distinct:

1. `explicit_placeholder_block`: `DetPlaceholder(E_*)` or
   `missing_and_blocked` language remains a block.
2. `draft_control_source_readout_candidate`:
   `SourceReadoutCandidate_EStar_v1`, `Det_src`, or `Readout_src` language
   remains draft/control candidate language.
3. `adopted_detector_semantics`: an adoption claim is a protected authority
   state and fails closed in this support-only packet.

The checker is not detector-semantics adoption, not source detector/readout
semantics adoption, not matter-coupling derivation, and not proof authority.

## Checked Cases

The built-in suite contains five deterministic cases:

| Case | Expected |
| --- | --- |
| `explicit_placeholder_block_safe` | pass |
| `draft_control_source_readout_candidate_safe` | pass |
| `placeholder_as_adopted_detector_semantics` | fail |
| `source_readout_candidate_as_detector_semantics` | fail |
| `unprotected_adopted_detector_semantics_state` | fail |

The report status is `PASS` only when the expected pass/fail behavior and
expected fail-closed status codes are observed.

## Forbidden Overreads

The checker must flag:

- `DetPlaceholder(E_*)` or placeholder/block language treated as detector
  semantics;
- source readout candidate language treated as adopted `Det_src`,
  `Readout_src`, or detector semantics;
- source readout candidate language used to derive matter coupling;
- any unprotected adopted detector-semantics state.

## Required Outputs

```text
scripts/research_control/support_formalization/detector_placeholder_collapse_checker.py
tests/test_detector_placeholder_collapse_checker.py
research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_spec_v1.md
research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_report.json
research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_receipt.md
```

## Done Criteria Mapping

| P7-T06 criterion | Evidence |
| --- | --- |
| Flags `DetPlaceholder(E)` collapse claims | `placeholder_as_adopted_detector_semantics` fails closed. |
| Flags source readout candidate adoption collapse | `source_readout_candidate_as_detector_semantics` fails closed. |
| Distinguishes explicit placeholder/block | `explicit_placeholder_block_safe` passes as `explicit_placeholder_block`. |
| Distinguishes draft/control source-readout candidate | `draft_control_source_readout_candidate_safe` passes as `draft_control_source_readout_candidate`. |
| Distinguishes adopted detector semantics | `unprotected_adopted_detector_semantics_state` fails with `fail_unprotected_adopted_detector_semantics`. |
| No proof authority | Report fields keep `support_only=true`, `proof_authority=false`, and `physics_promotion_authorized=false`. |

## Next Route

The next bounded route is P7-T07:
`support_formalization_traceability_integration`.
