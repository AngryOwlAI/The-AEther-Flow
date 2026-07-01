# P3-T03 Claim-Language Validation Integration Receipt

## Decision

The linter is integrated as a changed-surface gate instead of a full default
repository hard gate.

## Rationale

The P3-T02 default scan recorded existing hard-fail backlog in public/current
surfaces. Turning the full scan into an immediate global gate would collapse
P3-T03 and P3-T04 into one packet. The changed-surface gate blocks newly
changed or regenerated public/current overclaims while preserving the recorded
backlog for the next bounded remediation packet.

## Integration Points

- `validate_claim_language.py --changed` scans changed gate surfaces from Git
  diff plus untracked files.
- `validate_claim_language.py --staged` scans the staged transaction before
  commit.
- `validate_research_control.py --check-diff` runs the changed claim-language
  gate for changed public/current or active-control surfaces.
- `checkpoint_research_transaction.py` runs the changed gate after memory
  bootstrap and the staged gate before commit.

## Failure Example

`tests/fixtures/claim_language/public_overclaim.md` records a minimal public
overclaim example. Tests place that text on `README.md` and assert that it
hard-fails.

## Boundary

This is project-control validator integration only. It does not remediate the
full public backlog, adopt a source law, modify ontology, derive matter
coupling, derive Einstein equations, promote benchmark status, or complete a
derivation.
