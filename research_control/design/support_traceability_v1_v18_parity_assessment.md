<!-- authority: control -->

# Support Traceability v1-to-v18 Parity Assessment

## Status

- Plan task: `P9-T04`
- Migration epoch: `shadow_planner`
- Assessment result: `PASS`
- Retirement recommendation: `retain_active`
- Ordinary research handoff preserved: `handoff-0740`
- Scientific claims changed: `false`
- Distance-to-GR changed: `false`

The v1 and v18 support-traceability registries are active, support-only control
surfaces for different artifact families. Version numbering does not establish
replacement. This assessment therefore compares live entries, fail-closed
behavior, historical readability, and active invocation references before
making a retirement recommendation.

## Evidence Scope

The assessment inspected and executed:

- `scripts/research_control/support_formalization/validate_traceability_registry.py`
- `scripts/research_control/support_formalization/validate_traceability_registry_v18.py`
- `research_control/design/support_formalization_traceability_registry_v1.yaml`
- `research_control/design/support_formalization_traceability_registry_v18.yaml`
- `tests/test_support_formalization_traceability_registry.py`
- `tests/test_support_formalization_traceability_registry_v18.py`
- `tests/fixtures/support_traceability_v1/`
- `tests/fixtures/support_traceability_v18/`
- `registries/PROOF_NORMAL_FORM_REGISTRY.csv`
- `research_control/design/validation_command_inventory_v16.md`
- tracked Make, checkpoint, full-validation, validation-planner, workflow, and
  skill surfaces that could invoke the v1 validator.

The complete machine-readable entry map, mutation outcomes, source identities,
and reference inventory are retained in
`research_control/tasks/RT-20260717-016/artifacts/support_traceability_parity_report.json`.

## Entry Parity

The live v1 registry contains three entries and the live v18 registry contains
five. Their entry IDs, task IDs, checker/tool IDs, and registered source paths
have empty intersections. No v1 entry is represented by a v18 row.

| v1 entry | Current evidence | v18 disposition |
| --- | --- | --- |
| `SFR-V12-P6-T02-FINITE-TOY-TAG-REMOVAL` | Completed task `RT-20260630-028`; five referenced evidence files exist and validate | Distinct active v1 formalization; no v18 entry maps its checker, task, or source |
| `SFR-V17-P8-T02-FAIL-CLOSED-CERTIFICATE-EVALUATION` | Completed task `RT-20260706-019`; seven referenced evidence files exist and validate | Distinct active v1 formalization; no v18 entry maps its checker, task, or source |
| `SFR-V12-P6-T03-FINITE-LOCAL-WITNESS-SCHEMA` | Completed task `RT-20260630-029`; eight referenced evidence files exist and validate | Distinct active v1 formalization; no v18 entry maps its checker, task, or source |

The v18 rows instead cover the typed EqSrc orbit checker, closure countermodel
generator, no-target-import mutation tester, metric-use TeX reference
validator, and detector-placeholder collapse checker. They extend coverage;
they do not migrate the three v1 rows.

## Fail-Closed Mutation Matrix

A read-only 17-case matrix ran over the committed minimal fixtures through the
production validator functions. Every outcome matched its expected
classification.

| Mutation | v1 | v18 | Classification |
| --- | --- | --- | --- |
| Registry `support_only=false` | FAIL | FAIL | Shared |
| Registry `proof_authority=true` | FAIL | FAIL | Shared |
| Entry `support_only=false` | FAIL | FAIL | Shared |
| Entry `proof_authority=true` | FAIL | FAIL | Shared |
| Entry status drift | FAIL | FAIL | Shared |
| Report hash mismatch | FAIL | FAIL | Shared |
| Source-artifact hash mismatch | FAIL | FAIL | Shared |
| Required registry boundary phrase removed | FAIL | PASS | v1-only |
| Generated/local path substituted as source authority with matching hash | FAIL | PASS | v1-only |
| Report checker identity drift with updated hash | FAIL | PASS | v1-only |
| Source artifact `object_id` and registry metadata removed | FAIL | PASS | v1-only |
| Traceability task binding drift with updated hash | FAIL | PASS | v1-only |
| Proof-normal-form row missing | PASS | FAIL | v18-only |
| Test-evidence list empty | PASS | FAIL | v18-only |
| Validator/executable support-only flag false | PASS | FAIL | v18-only |
| Required plan-task order changed | PASS | FAIL | v18-only |
| Entry physics-promotion boundary enabled | PASS | FAIL | v18-only |

The matrix establishes complementary rather than substitutive behavior. In
particular, v18 does not enforce the following v1 obligations:

- canonical-source path exclusion for `.local/`, `wiki/`, `output/`, and
  `html/`;
- canonical artifact `object_id`, path, hash, and registry-name completeness;
- report checker ID, checker version, status, required boundary phrases,
  forbidden-authority flags, proposition coverage, formal-object mapping, and
  report-to-manifest source linkage;
- traceability-sidecar hash, task binding, support/proof boundary, exact formal
  object mapping, and required blocked-overread coverage; and
- existence of every declared v1 formalization file.

Conversely, v18 adds proof-normal-form row integrity, machine-checkable and
support-only PNF status, explicit tool-artifact hashes, nonempty test evidence,
fixed P7 task ordering, validator/executable support-only status, and explicit
physics-promotion boundary checks. These additions are valuable but do not
cover the v1-only failures or the unmatched v1 artifact families.

## Historical Readability and Active References

Both live validators pass against their current registries. All 20
v1-referenced evidence paths exist, every owning task and AgentJob is
registered as completed, and every owning completion file remains readable.
The existing v1 fixture and current-registry tests also pass without rewriting
historical receipts.

No tracked Make target, checkpoint script, full-validation runner,
validation-planner module, GitHub workflow, or Codex skill directly invokes
the v1 validator. The v1 surface is nevertheless active rather than historical:

- its registry declares `status: "active"`;
- `validation_command_inventory_v16.md` retains the v1 command for changes to
  the v1 registry or its formalization files;
- current unit and fixture coverage executes the live v1 validator; and
- tracked claim boundaries, task evidence, and handoffs continue to identify
  the v1 registry as the validating surface for its three distinct entries.

This is not an automation-migration blocker, because no automated caller must
be changed in this packet. It is evidence that `retain_historical` would be
premature.

## Recommendation

Retain the v1 validator and registry as active support-only validation:
`retain_active`.

The evidence does not support `retain_historical` or
`retire_after_migration`. Retirement would remove live validation for three
unmigrated entries and five demonstrated v1-only fail-closed behaviors.
Keeping v1 active does not make either validator proof authority and does not
change any physics, ontology, benchmark, Gate Chair, or completed-derivation
status.

## Reconsideration Conditions

A later deletion or historical-mode task must cite this assessment and prove
all of the following before changing the recommendation:

1. each of the three v1 entries is migrated to a registered replacement
   without rewriting its historical task evidence;
2. every v1-only hard failure is enforced by the replacement and the
   cross-validator mutation matrix has no false PASS;
3. v1 command-inventory, test, fixture, claim-boundary, and operator references
   are migrated or explicitly preserved by a read-only compatibility surface;
4. historical receipts and all referenced source artifacts remain readable;
5. both focused and repository-wide validation pass under the then-current
   migration epoch; and
6. the governed checkpoint records the exact staged migration with no
   scientific-authority change.

Until those conditions hold, version-number progression alone is not a valid
retirement basis.
