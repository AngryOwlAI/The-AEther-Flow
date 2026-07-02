<!-- authority: control -->

# P9-T02 Red-Team Review Template Receipt

## Scope

RT-20260702-025 updates
`research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml` so future
external red-team review packets have explicit v14 sections.

## Template Sections Added

- `object_under_attack`
- `source_files_reviewed`
- `status_being_tested`
- `definitions_attacked`
- `hidden_target_imports`
- `no_target_certificate_overread`
- `circularity_checks`
- `process_authority_checks`
- `evidence_as_adoption_checks`
- `rr_e_collapse_checks`
- `overclaim_checks`
- `finite_counterexamples`
- `comparison_to_known_constraints`
- `recommendation`

## Boundary

The template remains project-control scaffolding. It does not validate a future
review result, adopt or reject a physics object, issue a Gate Chair verdict,
promote benchmark status, authorize source-law adoption, or claim completed
derivation.

The global red-team artifact validator remains unchanged in this packet. The
task-local validator checks that the template still contains every legacy
validator field and all v14 review sections.

## Verification

The task-local command is:

```zsh
.venv/bin/python research_control/tasks/RT-20260702-025/artifacts/validate_p9_t02_red_team_review_template.py --output research_control/tasks/RT-20260702-025/artifacts/p9_t02_red_team_review_template_report.json --json
```
