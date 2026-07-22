---
authority: "control"
artifact_id: "V21-P10-HISTORICAL-READABILITY-REPORT-001"
task_id: "RT-20260722-003"
status: "PASS_WITH_LIFECYCLE_BLOCKERS_SEPARATED"
---

# V21 P10 historical-readability report

## Sample result

Every bounded historical sample resolves without inferred scientific status
or mutation:

- 1,040 historical task classifications remain readable; unknown legacy
  taxonomy fields stay explicit rather than being guessed.
- Seven candidate identities, five family identities, six lineage edges, and
  twenty-two lifecycle stages retain exact source links.
- Eight attempt events retain their complete SHA-256 chain and one explicit
  absence record.
- The pinned event-store pilot reads twelve tracked sources, emits twenty
  events in seven domains, and reproduces four declared views with zero
  mismatch and zero unmapped fields.
- Three content-addressed references resolve by full SHA-256 without changing
  their historical source paths.
- Ten stable burden definitions cover fourteen authoritative ledger rows.

## Limits preserved

The pilot still reports three unsupported legacy shapes and five documented
migration risks. Those are declared scope limits, not silent data loss. The
two lifecycle blockers concern receipt/view freshness after checkpoint; they
do not erase the sampled historical payloads.

No generated view, classification, validator, or compact receipt is treated
as independent scientific authority.
