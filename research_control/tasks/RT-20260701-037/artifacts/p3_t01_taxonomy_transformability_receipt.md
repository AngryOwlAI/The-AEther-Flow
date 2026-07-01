# P3-T01 Taxonomy Transformability Receipt

## Direct Transformability

The taxonomy can be consumed by a deterministic linter because it provides:

- `severity_levels` with blocking behavior.
- `surface_policy` with current/public, current/control, intentional-example, historical, and generated-derivative policies.
- `context_rules.bare_status_terms` for near-term detection.
- `phrase_classes[*].forbidden_patterns` for exact/regex phrase matching.
- `phrase_classes[*].bad_phrases` for fixtures and tests.
- `phrase_classes[*].corrective_language` for deterministic diagnostics.
- `required_phrase_coverage.plan_phrases` for acceptance tests.
- `next_linter_contract` for P3-T02 input, output, engine, and failure-policy requirements.

## Minimum P3-T02 Implementation Contract

The logical next step is a bounded linter implementation packet that reads the YAML taxonomy, scans configured current/public/control surfaces, downgrades explicitly marked historical or intentional bad-example surfaces, emits machine-readable findings, and fails on current/public or current/control hard-fail findings.

## Non-Authority Statement

Transformability is a software property. It is not proof authority, physics authority, or Gate Chair authority.
