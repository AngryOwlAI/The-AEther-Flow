# P3-T02 Linter Acceptance Receipt

## Implemented Behavior

- `scripts/project_control/validate_claim_language.py` loads `claim_language_linter_taxonomy_v1` with the repository strict YAML parser.
- The linter scans default P3-T02 surfaces and explicit `--paths`.
- It emits JSON with `status`, counts, scanned paths, config errors, and finding records.
- It emits human-readable pass or failure summaries when `--json` is omitted.
- It hard-fails current public surfaces and active handoff/control surfaces.
- It downgrades historical task, handoff, and registry surfaces to warnings.
- It downgrades explicitly reviewed intentional-example contexts to warnings through `research_control/design/claim_language_linter_reviewed_contexts.yaml`.
- It supports exact regex detection and near-term detection for bare `accepted` near high-risk objects.
- It recognizes scoped-positive wording and explicit denied/blocked-claim contexts.

## Required Test Coverage

| Requirement | Test |
| --- | --- |
| Public overclaim hard-fails | `test_public_overclaim_hard_fails` |
| Historical artifact overclaim warning-only | `test_historical_artifact_overclaim_is_warning_only` |
| Scoped-positive wording passes | `test_scoped_positive_wording_passes` |
| `accepted_as_scoped_evidence_precondition` passes | `test_accepted_as_scoped_evidence_precondition_passes` |
| Bare `accepted` near high-risk row fails or warns as configured | `test_bare_accepted_near_high_risk_row_fails` |
| Active handoff overclaim hard-fails | `test_active_handoff_overclaim_hard_fails_as_control` |
| Explicit denied claim context passes | `test_explicit_denial_context_passes` |
| No-target certificate overread fails | `test_no_target_certificate_overread_fails` |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption overread fails | `test_rr_e_transport_law_adoption_overread_fails` |
| Validator-as-proof overread fails | `test_validator_as_proof_overread_fails` |
| Reviewed context downgrade is explicit and scoped | `test_reviewed_context_downgrades_route_context` |
| JSON CLI output is machine-readable | `test_json_cli_output` |

## Verification

```text
.venv/bin/python -m unittest tests.test_validate_claim_language
Ran 12 tests
OK
```

`research_control/current_frontier.md` scans clean after scoped-positive and denial-context handling.

## Non-Authority Statement

The linter is a deterministic project-control tool. It does not prove, adopt, promote, or reject any physics claim.
