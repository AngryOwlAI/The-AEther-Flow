---
authority: "control"
artifact_id: "V21-P11-SCIENTIFIC-QA-INTEGRATION-AUDIT-001"
task_id: "RT-20260722-011"
job_id: "AJ-RT-20260722-011-001"
plan_task_id: "P11-T08"
status: "PASS_BOUNDED_ROLLOUT_TWO_REPAIRS_REQUIRED"
---

# V21 P11 scientific-QA integration audit

## Audit question

Do the completed P11 controls preserve source authority and resist false
externality, leaked process verdicts, checker-as-proof, consensus-as-proof, and
historical compatibility failures well enough for use in later bounded gates?

## Evidence boundary

This audit reads P11-T01 through P11-T07 and their existing validators as
immutable evidence. It does not repair a shared control, edit a reviewed
object, establish theorem truth, upgrade a reviewer-independence class, or
change any scientific or protected status.

## Result

The audit passes all twelve critical controls across fourteen matrix cases.
It approves P11 for bounded later-gate use under four mandatory guardrails and
does not approve unattended automation. Two exact limitations remain repair
obligations rather than hidden warnings.

| Surface | Result | Evidence |
| --- | --- | --- |
| Dependency integrity | PASS | All seven P11 completion hashes remain exact. |
| Externality and replication labels | PASS | Unsupported `external_review_completed` and `independent_replication_completed` fixtures fail closed. |
| Live review artifacts | PASS | Four P11-T07 records strict-validate as two `blind_same_model_review` and two `same_context_role_review` records. |
| Process leakage | PASS | A synthetic `task_verdict` key is rejected by the blind-packet scan. |
| Scientific self-containment | LIMITATION | P11-T07 required one task-local packet repair after process-redaction validation had already passed. |
| Checker-as-proof | PASS | Validator-only and validator-receipt-as-premise fixtures remain incomplete or invalid. |
| Consensus-as-proof | PASS | Three disagreements and seven correlated-agent false-consensus risks remain visible with no scientific-status effect. |
| Proof evidence | PASS | Formal assumptions and failures remain visible; proof and promotion authority remain false. |
| Semantic-smuggling probe | LIMITATION | Forty-three live findings were forty-three boundary false positives and zero confirmed smuggling findings. |
| Historical compatibility | PASS | Two pre-context artifacts remain readable as `legacy_unclassified`; neither is retroactively strengthened. |
| Source authority | PASS | Six canonical P11 control rows and two registered draft-science rows match current bytes and retain their declared authority. |
| Generated derivatives | PASS | Eight related wiki derivatives remain `generated_noncanonical`. |

## Findings

### P11-QA-F001 — process redaction is not scientific closure

The blind-packet validator checks canonical reconstruction and absence of
declared process-context leaks. It does not prove that the scientific excerpt
contains every definition, type, assumption, or supporting lemma needed by a
reviewer. P11-T07 exposed this distinction when the first selector packet
passed the process boundary but omitted `K_*`, `R_i`, and formal dependencies.
The parent repaired only the packet; no science source changed.

Until a separate repair adds an explicit scientific-dependency closure
contract and negative fixtures, every packet requires a parent scientific
self-containment review before review execution and no more than two bounded
repair rounds.

### P11-QA-F002 — the semantic probe is not calibrated as a live veto

The finite adversarial corpus remains useful, but its direct application to
the live `g_eff` blind packet produced forty-three duplicate or overlapping
findings on explicit negative boundary language, all dispositioned as false
positives. The probe may remain advisory for triage. It may not automatically
block, refute, approve, or promote a live claim-bearing artifact until a
separate repair adds boundary-aware negation handling, span deduplication, and
live-artifact calibration fixtures.

## Authority boundary

Audit PASS is operational evidence only. It does not establish theorem truth,
scientific status, external human review, independent replication, proof
authority, source-law or ontology adoption, physical interpretation, metric
adoption, benchmark promotion, publication, or a completed derivation. No
predecessor artifact, registered science source, source-authority row, or
Distance-to-GR ledger entry changed.
