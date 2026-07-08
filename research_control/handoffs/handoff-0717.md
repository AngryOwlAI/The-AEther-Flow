<!-- authority: control -->

# Handoff 0717

## Summary

Completed v18 P7-T06 detector-placeholder collapse checker support-only
implementation. The checker distinguishes explicit placeholder/block,
draft/control source-readout candidate, and unprotected adopted-detector
semantics states. It flags `DetPlaceholder(E_*)` or source-readout candidate
claims that imply adopted detector semantics or matter-coupling derivation.

## Control Boundary

This handoff does not authorize `Det_src` adoption, `Readout_src` adoption,
detector-semantics adoption, source detector/readout semantics adoption,
empirical detector protocol authority, proper-time normalization, target
metric import, matter-coupling derivation, stress-energy semantics,
matter-action semantics, Einstein-equation derivation, benchmark promotion,
Gate Chair verdict, proof authority, or completed derivation.

## Evidence

- Task: `research_control/tasks/RT-20260708-024/00_TASK.yaml`
- Completion: `research_control/tasks/RT-20260708-024/jobs/completions/AJC-AJ-RT-20260708-024-001.yaml`
- Checker: `scripts/research_control/support_formalization/detector_placeholder_collapse_checker.py`
- Tests: `tests/test_detector_placeholder_collapse_checker.py`
- Spec: `research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_spec_v1.md`
- Report: `research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_report.json`

## Next Action

Run one bounded v18 P7-T07 support formalization traceability integration
packet.
