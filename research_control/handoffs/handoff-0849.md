<!-- authority: control -->

# handoff-0849 — P13-T03 packaging contract complete

Generation 90 completed `P13-T03` under
`AJ-RT-20260723-019-001`. The repository now has root `pyproject.toml`
metadata, two exact already-used Python distributions, a reproducible universal
lock with 82 package-index SHA-256 hashes, lock-only requirements wrappers,
hash-enforced Make and CI setup paths, external-tool and migration policy, and
deterministic classifier coverage.

The clean CPython 3.12 installation, normalized lock reproduction, task-local
contract checks, and both 87-test focused runs pass. The clean test made the
legacy hidden dependency visible: tracked validators already imported PyYAML,
so P13-T03 now declares and locks it alongside PyMuPDF. This is a
project-system dependency correction, not a new scientific assumption or a
physics result.

## Required next action

Run the one authorized governed checkpoint for
`AJ-RT-20260723-019-001`. After that commit, a fresh bounded
`improve-project-system` frame may execute `P13-T04`: incremental linting,
typing, Python and OS matrices, path-length and case-sensitivity fixtures, and
the validator API contract.

`P13-T04` has not been executed in this handoff. `P13-T02` remains blocked by
the held `P13-T01` cutover, and `P13-T01` may not reopen without explicit
publication authority plus matched current-head hosted-CI and scheduled-full
evidence.

## Authority boundary

This handoff creates no scientific, ontology, source-law, Distance-to-GR,
benchmark, proof, Gate Chair, completed-derivation, publication, push, hosted
workflow, or external-system authority. The ordinary-route exception remains
limited to the fact that dependency-ready science task `P4-T05` requires
explicit human Gate Chair authority unavailable to this relay.
