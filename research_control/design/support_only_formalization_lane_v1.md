<!-- authority: control -->

# Support-Only Formalization Lane v1

## Purpose

This design artifact completes P6-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v12.md`.
It chooses the formalization approach for support-only theorem skeletons and
names the folder path, validation commands, fallback path, and P6-T02 handoff
requirements.

The lane exists to make finite and local project-control reasoning easier to
review. It does not create physics proof authority.

## Boundary Statement

Support-only formalization has proof_authority=false. It is not proof authority, not canonical ontology adoption, not source-law adoption, not source-extension data adoption beyond exact scoped gate results, not MetricData(E) adoption, not g_eff adoption or scope expansion, not coupling-law adoption, not matter coupling, not stress-energy semantics, not a stress-energy tensor, not detector semantics, not a matter action, not Einstein equations, not benchmark promotion, and not completed derivation.

The lane also blocks canonical-ontology candidate status, protected evidence
status changes, benchmark Gate Chair closure, future source-extension
impossibility claims, and global theory rejection.

## Chosen Approach

The chosen primary approach is a standard-library Python typed algebraic
specification plus deterministic property-style `unittest` tests.

The chosen implementation folder path for future packets is:

```text
scripts/research_control/support_formalization/
```

The matching future test and fixture surfaces are:

```text
tests/test_support_only_finite_toy_tag_obstruction.py
tests/test_support_only_finite_local_witness_schema.py
tests/fixtures/research_control/support_formalization/
```

This packet does not create those implementation files. It creates the lane
contract only.

## Decision Rationale

Python typed algebraic specifications are selected because they already match
the repository's support-only checker precedent, require no new dependency, run
inside the existing virtual environment, and can represent finite tags,
source-side graph records, relabeling maps, erasure maps, and partial response
relations directly.

Lean, Coq, and Isabelle/HOL remain useful later-port candidates, but they add
local dependency friction before the finite objects are stable. A lightweight
custom checker alone is also possible, but the existing Python checker line
already provides better traceability, structured reports, and deterministic
unit-test integration.

## Validation Commands

Future P6 support-formalization packets should use the narrowest applicable
command first and then the project-control validators:

```zsh
.venv/bin/python -m unittest tests.test_support_only_finite_toy_tag_obstruction
.venv/bin/python -m unittest tests.test_support_only_finite_local_witness_schema
.venv/bin/python -m unittest discover -s tests -p 'test_support_only_*.py'
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

For this P6-T01 design packet, the applicable validators are the normal
research-control, memory, documentation-impact, dependency-graph, and git diff
checks because no support-formalization implementation files exist yet.

## Minimal Fallback

If any future dependency is unavailable, the lane falls back to Python standard
library only:

- `dataclasses` for finite source objects, tag records, untagged objects, and
  response records;
- `typing` for explicit finite map and relation signatures;
- `unittest` for deterministic examples and property-style enumerations over
  small finite families;
- JSON or the repository YAML subset for fixtures;
- no Hypothesis, no proof assistant runtime, and no external solver required.

The fallback still must emit `proof_authority=false`, preserve the boundary
statement, and treat parser or dependency failure as tooling/data-quality
failure rather than physics obstruction.

## P6-T02 Initial Formal Objects

The next packet should formalize the existing finite toy tag-removal
obstruction as support-only tooling. It should define:

- finite toy source object type;
- tag record type for orientation, normalization, and token semantics;
- untagged object type;
- tag-erasure map;
- partial response relation;
- proposition record: tag erasure makes response undefined;
- optional proposition record: no equivariant no-new-source-data totalization
  under sign or token relabeling.

These records must cite the canonical finite toy Refuter artifact and must not
import a target metric, target atlas, stress-energy semantics, detector
semantics, matter action, Einstein equations, benchmark status, or any
unscoped `g_eff` claim.

## Traceability Rules

Every support-formalization file must identify its source artifact and declare
`proof_authority=false`. Machine passing results may be cited only as support
for later review, never as source-law adoption, physics proof, or downstream GR
promotion.

P6-T02 should map its formal objects to
`research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`.
That artifact remains the canonical research-control source for the frozen
finite toy tag-removal obstruction.

## Non-Conclusions

P6-T01 does not choose a theorem prover for authoritative physics proof. It
does not mechanize P6-T02, does not introduce a new theorem statement, and does
not change the Distance-to-GR ledger. It only selects the support-only lane and
hands off the first finite toy formalization task.

Forbidden readings include:

- support-only formalization as proof authority;
- canonical ontology edit or adoption;
- source-law, MCPA, or source-extension-data adoption beyond exact scoped gate
  results;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor, detector semantics, or matter
  action;
- Einstein equations;
- benchmark promotion or benchmark Gate Chair closure;
- completed derivation;
- future source-extension impossibility;
- global theory rejection.

## Handoff

The logical next continue-research packet is P6-T02 with
`validator-engineer@0.2.0` unless a theorem statement changes, in which case a
separate selector should decide whether `ontology-formalizer@0.2.0` is needed.
P6-T02 should create only the finite toy tag-removal support formalization,
fixtures or tests, and a traceability note. It must not implement P6-T03 in the
same invocation.

## References

The AEther-Flow Research Project. (2026, June 18). *Resp_lc finite toy metric
response model Refuter stress test* [Internal research-control artifact].

The AEther-Flow Research Project. (2026, June 28). *P5-T01 support-only
mechanization boundary design* [Internal project-control artifact].

The AEther-Flow Research Project. (2026, June 30). *Handoff 0378* [Internal
research-control handoff].

The AEther-Flow Research Project. (2026, June 30). *Matter semantics
post-stress selector v1* [Internal project-control artifact].

The AEther-Flow Research Project. (2026, June 30). *Recommendations
implementation plan continue task v12* [Internal implementation plan].
