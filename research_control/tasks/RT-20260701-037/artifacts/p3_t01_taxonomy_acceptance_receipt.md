# P3-T01 Taxonomy Acceptance Receipt

## Result

`research_control/design/claim_language_linter_taxonomy.yaml` satisfies the P3-T01 control requirement.

## Acceptance Checks

| Requirement | Status | Evidence |
| --- | --- | --- |
| Machine-readable taxonomy | PASS | YAML file has schema id, version, surface policy, severity levels, context rules, phrase classes, required phrase coverage, and next-linter contract. |
| Eighteen required phrase classes | PASS | `phrase_classes` contains class numbers 1 through 18. |
| Required example phrases represented | PASS | `required_phrase_coverage.plan_phrases` maps every listed P3-T01 required phrase to a class id. |
| Severity assignments | PASS | Each phrase class has current/public, current/control, and historical severity fields. |
| Public/current hard failures | PASS | Current public and current control policies hard-fail forbidden wording. |
| Historical warnings separated | PASS | Historical artifacts and intentional bad examples downgrade to warnings only. |
| No physics promotion | PASS | Authority rules set proof and promotion fields to false, and task boundaries forbid adoption or promotion. |

## Claim Boundary

This receipt does not authorize source-law adoption, matter-coupling derivation, Einstein-equation derivation, benchmark promotion, or completed-derivation language. It only closes P3-T01 and routes to P3-T02 linter implementation.
