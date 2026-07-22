---
authority: "control"
schema_id: "v21_blind_review_packet_v1"
plan_task_id: "P11-T01"
---

# V21 blind-review packet and context-separation schema

## Purpose and authority boundary

This task-local control schema defines a reproducible way to give a reviewer
the scientific content needed for critique while withholding workflow
outcomes and internal process context. It is operational evidence only. It
does not establish reviewer independence, proof, ontology adoption, physical
interpretation, publication, benchmark promotion, or a completed derivation.

The protocol has three distinct objects:

1. A source manifest used by the packet builder. It contains scientific
   material and process metadata in separate top-level fields.
2. A blind packet delivered to the reviewer. It contains only the scientific
   material defined below.
3. A context manifest retained beside, but never embedded in, the blind
   packet. It records what categories and hashes the reviewer received and
   which process-field names were withheld.

## Blind packet contract

The packet is canonical UTF-8 JSON with sorted keys, two-space indentation,
and one trailing newline. It has exactly these top-level fields:

- `schema_id`: `v21_blind_review_packet_v1`.
- `packet_id`: a stable review-packet identity with no task or route token.
- `review_target`: neutral title, scientific scope, and blind source bindings.
- `assumption_register`: every assumption required to interpret the supplied
  statements or construction.
- `scientific_material`: ordered definitions, statements, proof or
  construction steps, controls, and counterpressure.
- `claim_boundary`: explicit statements limiting what may be inferred.

Every source binding contains a blind source alias and the SHA-256 digest of
the exact source bytes. Repository paths remain in the source manifest and
context manifest, not in the blind packet. Every source excerpt contains its
own SHA-256 digest and must occur byte-for-byte in the bound source. Supplied
review boundaries are marked as such and must not be misrepresented as source
quotes.

## Included scientific material

The builder may include only:

- mathematical definitions and declared domains;
- assumptions and hypotheses needed to assess the result;
- theorem or candidate statements;
- proof, construction, computation, or counterexample steps;
- positive and negative controls;
- explicit scope limits and claim boundaries;
- stable blind source aliases and exact SHA-256 source/content hashes.

Assumptions are never redacted merely because they reveal a limitation. If a
required assumption cannot be preserved, packet generation fails closed.

## Forbidden process metadata

The blind packet must not contain a key or value disclosing:

- task, job, decision, plan-task, handoff, generation, lease, or checkpoint
  identity;
- route history, selected next action, worker skill, role assignment, or
  orchestration state;
- task verdict, completion state, validation status, validator outcome, test
  outcome, audit disposition, or internal confidence;
- reviewer identity, model family, prior-context access, independence label,
  or review agreement result.

The validator rejects forbidden keys recursively and rejects recognizable
workflow tokens in any packet string, including research-task, AgentJob,
decision, handoff, and plan-task identifiers. A neutral mathematical use of a
word is not sufficient to override a matched workflow token; the source
manifest must instead supply a context-safe scientific excerpt.

## Context manifest contract

The context manifest is canonical JSON and is not delivered as part of the
blind packet. It records:

- packet and blind-packet hashes;
- received material, assumption, claim-boundary, and source-alias identities;
- the exact hashes associated with received content;
- source-path bindings retained by the operator;
- names and a canonical hash of withheld process metadata fields;
- `reviewer_independence_claimed: false`.

It does not assign an independence class. P11-T02 owns that later taxonomy.

## Reproducibility and failure behavior

The builder verifies source byte hashes and exact excerpt occurrence before it
writes either output. The validator independently rebuilds the expected
objects, compares canonical bytes, scans recursively for leaks, verifies
assumption completeness, and checks that the context manifest is separate.
Any source drift, missing assumption, content alteration, forbidden key,
forbidden workflow token, or packet/context co-location is a hard failure.

## Claim boundary

Passing this protocol means only that the fixture packet is reproducible and
passes the task-local separation checks. It does not mean the reviewed
scientific object is correct, that the reviewer is independent, or that any
scientific or protected gate has been satisfied.
