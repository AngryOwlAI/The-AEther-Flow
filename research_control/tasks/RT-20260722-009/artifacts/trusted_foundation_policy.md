<!-- authority: task-local control -->

# Trusted-Foundation Policy for V21 Proof Evidence

## Status

```yaml
policy_id: "v21_proof_evidence_trusted_foundation_policy_v1"
task_id: "RT-20260722-009"
plan_task_id: "P11-T03"
authority: "task-local project control"
proof_authority: false
physics_promotion_authorized: false
```

## Purpose

This policy makes the formal trust base explicit. “Trusted” means only that a
record names the kernel, version, permitted foundational mechanisms, admitted
axioms, and evidence used to classify a build. It does not mean that the
encoded theorem is a faithful translation of a canonical source, that its
assumptions are physically admissible, or that any ontology or interpretation
has been adopted.

## V1 trust classes

| Class | Required declaration | Result |
| --- | --- | --- |
| Kernel and core foundation | Exact proof assistant, version, release identity, and dependency lock | Required metadata; not proof authority |
| No reported theorem dependencies | Axiom report for each named theorem and zero reported dependencies | `PASS_MACHINE_CHECKED_NO_AXIOM_DEPENDENCIES` when all other checks pass |
| Declared allowed admitted axiom | Exact axiom identity listed in both `allowed_admitted_axioms` and `admitted_axioms` | `PASS_WITH_FORMAL_ASSUMPTION_WARNING`; never “axiom-free” |
| Undeclared or disallowed axiom | Any admitted axiom absent from the policy allowlist | `FAIL` |
| Formal gap | `sorry`, `admit`, custom axiom, unsafe declaration, missing source, or missing trust metadata | `FAIL` |

The v1 policy allowlist for admitted axioms is empty for the P2-T05 migration.
A future task may define a nonempty, narrowly scoped allowlist, but the axiom
must remain visible and must force the warning result. A warning cannot be
upgraded to an axiom-free result by validator configuration.

## P2-T05 trust declaration

- Kernel: Lean 4 kernel.
- Foundation version: Lean 4.30.0, pinned to release `v4.30.0`.
- Dependency set: empty beyond the Lean core distribution, as recorded by the
  toolchain lock.
- Named theorem axiom reports: six.
- Reported theorem dependencies: zero.
- Forbidden declaration scan: no `sorry`, `admit`, custom `axiom`, or unsafe
  declaration.
- Proof-object evidence: one `.olean` SHA-256 reproduced across two clean
  builds.

This declaration supports the scoped statement that the encoded propositions
were machine-checked under the declared Lean core environment with no reported
axiom dependencies. It does not establish P2-T03 translation fidelity,
current-ontology derivation, selector-law adoption, physical gauge status,
general EqSrc, or any downstream GR burden.

## Failure visibility

The adapter must preserve every failure and warning in its report. It may not
drop a failed fixture, replace a warning with PASS, infer that a build failure
refutes the theorem, or infer that a successful build proves a physical claim.
Missing proof objects may remain durable by hash only when their retention
status says `hashed_untracked_build_output`; a blank tracked path must not be
misrepresented as a retained artifact.

## Non-conclusions

The following never follow from this policy or its validator:

- proof authority;
- theorem truth beyond the exact encoding and declared foundations;
- formal-to-canonical translation fidelity;
- ontology or source-law adoption;
- physical interpretation, physical gauge, or empirical support;
- external review or independent replication;
- benchmark promotion, publication authority, or completed derivation;
- future source-extension impossibility or global theory rejection.

## References

The AEther-Flow Research Project. (2026). *P2-T05 selector-kernel Lean build*
[Internal task-local build instructions].

The AEther-Flow Research Project. (2026). *Support-only formalization lane v1*
[Internal project-control design].
