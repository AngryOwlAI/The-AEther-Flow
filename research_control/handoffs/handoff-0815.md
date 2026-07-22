---
authority: "control"
handoff_id: "handoff-0815"
task_id: "RT-20260722-005"
status: "ready_for_director"
---

# Handoff 0815 — Review-context classification complete

P11-T02 completed an additive review-context classification contract. It
distinguishes same-context role review, blind same-model review,
different-model review, human expert review, independent replication, and
unknown. Each new record separately reports model family, prompt context, data
access, institution, human authorship, code base, and method.

Twenty-four task-local checks and twelve focused tests pass. The fixture corpus
covers all six classes, rejects unsupported external-review and
independent-replication wording, and confirms that both a minimal legacy
fixture and a historical review remain readable as `legacy_unclassified`.

This result calibrates provenance language only. It does not execute a review,
prove reviewer independence, complete an external review or replication,
validate science, or exercise protected authority.

P11-T01 and P11-T02 now provide the qualifying dependency evidence for
P11-T04. The next bounded packet may build deterministic semantic-smuggling
fixtures for aliases, split encodings, equivalent forms, misleading
certificates, and prompt-level interpretations while measuring false positives
and false negatives. It must retain human and blind review and must not claim
semantic completeness.
