<!-- authority: task-local control -->

# V21 Proof-Evidence Registration Schema

## 1. Status and boundary

```yaml
schema_id: "v21_proof_evidence_record_v1"
authority: "task-local project control"
status: "active for P11-T03 evidence fixtures"
created_by_task_id: "RT-20260722-009"
created_by_job_id: "AJ-RT-20260722-009-001"
plan_task_id: "P11-T03"
proof_authority: false
physics_promotion_authorized: false
```

This schema makes theorem statements, formal sources, proof-object hashes,
toolchains, dependency locks, trust-base declarations, and build receipts
queryable as separate evidence. It does not collapse those records into a
single word such as “proved,” and it never infers physical interpretation,
ontology adoption, empirical support, external review, or protected promotion.

A conforming record says only what exact formal object was checked, under what
declared foundations, from what bytes, with what build evidence, and with what
explicit limitations. The canonical theorem or science source remains the
authority for the statement and scope. A proof assistant checks the encoded
formal statement; it does not establish translation fidelity or physical
meaning by itself.

## 2. Normative machine contract

<!-- BEGIN V21_PROOF_EVIDENCE_SCHEMA_JSON -->
```json
{
  "schema_id": "v21_proof_evidence_record_v1",
  "schema_version": 1,
  "record_type": "proof_evidence_registration",
  "required_top_level_fields": [
    "schema_id",
    "record_id",
    "subject",
    "theorem_statement",
    "proof_sources",
    "proof_objects",
    "toolchain",
    "trusted_foundation",
    "build",
    "claim_boundary",
    "authorization_layers",
    "forbidden_conclusions"
  ],
  "subject_fields": [
    "theorem_id",
    "theorem_scope",
    "claim_status"
  ],
  "theorem_statement_fields": [
    "path",
    "sha256",
    "authority_status"
  ],
  "proof_source_fields": [
    "path",
    "sha256",
    "language",
    "role"
  ],
  "proof_object_fields": [
    "artifact_id",
    "format",
    "sha256",
    "retained_path",
    "retention_status",
    "reproducible",
    "clean_build_count"
  ],
  "toolchain_fields": [
    "tool",
    "version",
    "release_tag",
    "release_commit",
    "lock_path",
    "lock_sha256",
    "archive_name",
    "archive_sha256",
    "dependencies"
  ],
  "trusted_foundation_fields": [
    "policy_id",
    "kernel",
    "foundation_version",
    "allowed_foundations",
    "allowed_admitted_axioms",
    "admitted_axioms",
    "theorem_axiom_report_count",
    "theorem_with_axiom_dependency_count",
    "forbidden_declaration_scan",
    "status"
  ],
  "build_fields": [
    "adapter_id",
    "script_path",
    "script_sha256",
    "result_status",
    "clean_build_count",
    "proof_object_byte_reproducible",
    "proof_object_sha256",
    "validation_receipt_path",
    "validation_receipt_sha256",
    "source_hash_verified",
    "proof_object_hash_verified"
  ],
  "retention_statuses": [
    "tracked_artifact",
    "hashed_untracked_build_output"
  ],
  "result_statuses": [
    "PASS_MACHINE_CHECKED_NO_AXIOM_DEPENDENCIES",
    "PASS_WITH_FORMAL_ASSUMPTION_WARNING",
    "FAIL"
  ],
  "non_promotional_claim_statuses": [
    "draft/control",
    "proposal-only",
    "source-extension data"
  ],
  "protected_authorization_fields": [
    "proof_authority",
    "downstream_physics_promotion_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
    "publication_authority"
  ]
}
```
<!-- END V21_PROOF_EVIDENCE_SCHEMA_JSON -->

Unknown fields, unknown enum values, malformed hashes, missing live sources,
source/hash drift, toolchain-lock drift, proof-object/build hash disagreement,
unreported formal assumptions, and any true protected authorization fail
closed. Historical records are not rewritten; migration creates a new
evidence record that cites their exact bytes.

## 3. Evidence layers

| Layer | Required evidence | What it does not establish |
| --- | --- | --- |
| Theorem statement | Canonical path, statement hash, theorem ID, and exact scope | That the formal encoding is faithful or physically meaningful |
| Formal source | Formal-language path, hash, and role | That a successful compile proves the canonical statement |
| Proof object | Format, hash, retention state, and clean-build count | Permanent proof authority or scientific adoption |
| Toolchain | Tool, version, release identity, dependency lock, and archive hash | Trust in undeclared external dependencies |
| Trusted foundation | Kernel, permitted foundation, admitted-axiom list, axiom reports, and forbidden-declaration scan | That allowed foundations are physically true |
| Build | Adapter, script hash, validation receipt, source/proof hash parity, and reproducibility | Translation fidelity, external review, or empirical confirmation |
| Claim boundary | Mathematical status separated from authority and promotion booleans | Ontology adoption, physical interpretation, or completed derivation |

The layers are not interchangeable. In particular, a proof-object hash is not
a theorem-statement hash, toolchain identity is not a trust decision, and a
validator PASS is not a proof or promotion verdict.

## 4. Trust and warning semantics

The companion `trusted_foundation_policy.md` controls the trust-base fields.
For this v1 packet:

1. `PASS_MACHINE_CHECKED_NO_AXIOM_DEPENDENCIES` requires an exact toolchain,
   a clean forbidden-declaration scan, at least one theorem axiom report, zero
   reported theorem dependencies, and an empty admitted-axiom list.
2. A declared, policy-allowed admitted axiom is visible as
   `PASS_WITH_FORMAL_ASSUMPTION_WARNING`. The record may not be described as
   axiom-free, and mathematical status becomes
   `machine_checked_with_formal_assumption_warning`.
3. An undeclared or policy-disallowed axiom, `sorry`, `admit`, custom axiom,
   unsafe declaration, missing trust metadata, or failed build is `FAIL`.
4. All three outcomes retain `proof_authority: false` and
   `physics_promotion_authorized: false`.

Formal failure is a tooling or formal-evidence outcome. It is not, by itself,
a physical refutation or a no-go theorem about the project ontology.

## 5. P2-T05 migration path

The fixture suite contains one live migration record for
`EQSRC-SELECTOR-KERNEL-LEAN-V1`. It links:

- the registered P2-T03 theorem statement and its SHA-256;
- the P2-T05 `SelectorKernel.lean` source and SHA-256;
- the pinned Lean 4.30.0 lock, release, and archive SHA-256;
- the task-local build script and validation receipt hashes;
- the reproducible `.olean` hash from two clean builds;
- six theorem axiom reports with zero reported dependencies; and
- the unchanged proposal-only, no-promotion claim boundary.

The `.olean` file is intentionally represented as
`hashed_untracked_build_output`: its exact hash is durable, while the local
build output is not falsely represented as tracked scientific authority. A
future policy may retain a proof object in an approved tracked artifact store,
but that would require a separate bounded task and source-authority decision.

## 6. Query and downstream use

Downstream P11 review packets may query the task completion, current program
state, this registered schema, the deterministic validation report, and the
compact receipt. They must cite the theorem source and proof evidence
separately. P11-T07 may exercise this evidence as one review input only after
all its dependencies are complete; it may not treat the adapter as a review,
replication, proof-authority, or promotion gate.

## 7. Forbidden conclusions

Every record includes these exact guards:

- `validator PASS as proof authority`
- `formalization as physical interpretation`
- `ontology adoption`
- `physics promotion`
- `completed derivation`

Additional prohibited readings include source-law adoption, canonical ontology
editing, a physical-gauge verdict, general EqSrc discharge, external human
review, independent replication, benchmark promotion, publication authority,
future source-extension impossibility, and global theory rejection.

## References

The AEther-Flow Research Project. (2026). *EQSRC no-natural-selector and
nonuniqueness theorem v1* [Internal canonical research artifact].

The AEther-Flow Research Project. (2026). *P2-T05 selector-kernel Lean build*
[Internal task-local build instructions].

The AEther-Flow Research Project. (2026). *V21 scientific status schema*
[Internal project-control schema].
