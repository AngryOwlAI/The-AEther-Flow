<!-- authority: control -->

# P4-T06 agent validation-output consumption review

## Scope

This review checks the three local-agent skill contracts and the new control
policy against the P4-T06 acceptance boundary. It also reviews the P4-T05
completion as the migration sample for compact evidence sufficiency. The review
does not change validator implementation, decision logic, exit semantics,
finding taxonomy, receipt schema, planner behavior, or scientific authority.

## Sources reviewed

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `research_control/design/agent_validation_output_consumption_policy_v1.md`
- `research_control/tasks/RT-20260716-005/jobs/completions/AJC-AJ-RT-20260716-005-001.yaml`
- `research_control/tasks/RT-20260716-005/artifacts/core_validator_reporting_migration.json`

## Contract review

| Requirement | Evidence | Result |
| --- | --- | --- |
| Summary-first consumption | All three skill contracts require a compact summary first; `continue-research` requests `continue_research.py --summary` before escalation. | PASS |
| PASS stop rule | The skills and policy stop receipt expansion for PASS unless a named audit, parity, schema, or checkpoint contract requires it. | PASS |
| Bounded failure expansion | WARN, FAIL, and BLOCKED_CONFIGURATION route through the relevant gate, stable finding IDs, a selected structured section, and at most a 200-line raw tail. | PASS |
| No unchanged polling | The contracts prohibit polling that only retransmits unchanged output and require a changed state, marker, or hypothesis. | PASS |
| Compact completion evidence | The policy requires gate ID, exact status, receipt path, SHA-256 content hash, counts, relevant finding IDs, and a tree or input fingerprint when available. | PASS |
| Local receipt boundary | `.local/validation-receipts` is explicitly untracked, non-authoritative, regenerable diagnostic cache and cannot override tracked authority. | PASS |

## P4-T05 sample-completion review

The P4-T05 completion is sufficient as a migration sample. Its compact
`core_validator_compact_receipts` block identifies PASS status, the tracked
acceptance artifact, adapter count, stable-ID and parity outcomes, byte-budget
measurements, local atomic full-receipt behavior, and the accepted staged-tree
fingerprint. Its command and validation-layer sections provide bounded outcome
summaries without embedding raw logs. The linked acceptance JSON preserves the
per-case gate IDs, statuses, exits, counts, output sizes, local receipt paths
and hashes, compatibility comparisons, and authority flags.

The sample predates P4-T06 and therefore does not normalize every gate into the
new single-entry shape directly inside the completion. In particular, some
receipt paths, content hashes, and counts reside in the linked acceptance JSON
rather than beside each completion gate. This is not a retrospective defect:
the compact completion plus its tracked acceptance artifact are sufficient to
audit P4-T05. P4-T06 makes the normalized gate-reference shape mandatory for
future relevant completion evidence.

## Boundary result

Result: **PASS**. The policy changes local-agent output consumption only.
Validation evidence remains operational and cannot promote ontology, metric,
coupling, Einstein-equation, benchmark, Gate Chair, proof, completed-derivation,
or other physics claims. `handoff-0740` and the ordinary EqSrc research route
remain unchanged.
