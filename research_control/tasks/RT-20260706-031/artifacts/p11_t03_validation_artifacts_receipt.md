# P11-T03 Validation Artifact Collector Receipt

Authority: operational receipt only. This receipt and the generated validation
summaries are not physics proof authority, source-law adoption, benchmark
promotion, Gate Chair verdict, or completed-derivation evidence.

## Outputs

| Path | Purpose |
| --- | --- |
| `scripts/research_control/collect_validation_artifacts.py` | Collects the existing local CI-equivalent validation report into compact JSON and Markdown summaries. |
| `output/validation_summary.json` | Machine-readable validation summary for CI and local review. |
| `output/validation_summary.md` | Human-readable validation summary for CI and local review. |
| `tests/test_collect_validation_artifacts.py` | Focused tests for collector summary boundaries and output writing. |
| `research_control/tasks/RT-20260706-031/artifacts/validate_p11_t03_validation_artifacts.py` | Task-local validator for P11-T03 required outputs and boundaries. |

## Boundary

The collector reports local validation status only. It does not change
Distance-to-GR status, does not adopt source laws, does not derive matter
coupling, does not derive Einstein equations, and does not promote benchmark
or completed-derivation claims.

## Validation

- Collector syntax check: PASS.
- Focused collector unit tests: PASS.
- Collector generation: PASS.
- Task-local validation artifact check: PASS.
