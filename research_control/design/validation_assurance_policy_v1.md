---
authority: "control"
schema_id: "validation_assurance_policy_v1"
status: "active"
owner: "validator-engineer"
plan_task_id: "P13-T05"
task_id: "RT-20260724-002"
claim_boundary_id: "CB-V21-P13-T05-ASSURANCE-001"
---

# Validation Assurance Policy v1

## Purpose

This policy adds bounded operational evidence for selected project-control
validators. It combines branch coverage, generated properties, targeted
mutation testing, dependency-vulnerability auditing, static Python security
analysis, and the existing semantic-smuggling adversarial fixtures.

No score, finding count, or passing tool establishes correctness, semantic
completeness, scientific truth, ontology adoption, a completed derivation,
Distance-to-GR progress, benchmark status, proof authority, or publication
authority.

## Fixed Scope

The incremental coverage surface is
`scripts/validation/assurance.py` and
`scripts/validation/portability.py`. The floor is 85 percent across statement
and branch opportunities reported by Coverage.py. The property suite also
exercises timestamp-free goal-state hashing and fingerprint classification,
but the large goal-state helper is not folded into this narrow percentage.

Mutation testing is limited to the
`scripts.validation.assurance.evaluate_mutation` evidence-gate function, uses
only `tests/test_validation_assurance.py`, and targets a 100 percent
killed-or-explicitly-dispositioned score for measured mutants. Skipped
mutants do not improve the score. Survived, suspicious, timed-out, or untested
mutants are unresolved unless each has a recorded task-local disposition.

Bandit scans selected Python validation and checkpoint paths. An
undispositioned high-severity finding blocks the gate. Lower-severity findings
remain visible and receive task-local review. pip-audit scans the exact
hash-locked development environment; every reported vulnerability requires an
explicit disposition, regardless of whether upstream metadata supplies a
severity.

The P11-T04 semantic-smuggling corpus remains a required non-regression test.
It is adversarial fixture evidence only and does not establish semantic
completeness.

## Execution Tiers

The ordinary assurance target runs exact dependency checks, property and unit
tests, branch coverage, the adversarial fixture suite, and high-severity static
code scanning. The dependency audit and targeted mutation campaign are
separate scheduled or task-local targets because they are slower and may
depend on current vulnerability metadata or a fork-capable runtime.

Raw logs belong under ignored `.local/assurance/`. Durable task evidence is a
compact normalized report with exact tool versions, commands, source hashes,
counts, dispositions, and authority limits.

## External Tool Basis

The distribution pages are used only for current version identity and the
documented operational purpose of each tool. They do not supply scientific or
proof authority.

### References

Batchelder, N., & contributors. (2026). *Coverage.py* (Version 7.15.2)
[Computer software]. Python Package Index. https://pypi.org/project/coverage/

Boxed. (2026). *mutmut* (Version 3.6.0) [Computer software]. Python Package
Index. https://pypi.org/project/mutmut/

HypothesisWorks. (2026). *Hypothesis* (Version 6.161.2) [Computer software].
Python Package Index. https://pypi.org/project/hypothesis/

OpenStack Security Group. (2026). *Bandit* (Version 1.9.4) [Computer
software]. Python Package Index. https://pypi.org/project/bandit/

Python Packaging Authority. (2026). *pip-audit* (Version 2.10.1) [Computer
software]. Python Package Index. https://pypi.org/project/pip-audit/
