<!-- authority: control -->

# Finite Source-Cover Model Checker

## Purpose

The finite source-cover model checker is deterministic project-control tooling
for explicit finite/local source-cover witnesses. It converts witness data into
machine-checkable status records so later research packets can cite finite
counterexamples or finite/local pass results without treating prose as a
validator.

This checker does not prove source regularity, soldering, arbitrary
finite-variation robustness, `M_src`, `g_eff`, matter coupling, Einstein
equations, or benchmark recovery. Its output has no source-law adoption,
ontology-edit, Gate Chair, or physics-promotion authority.

## Input Contract

The checker accepts JSON and the repository's YAML witness subset. The intended
input shape covers:

- source tokens;
- quotient classes;
- chart candidates;
- chart supports and overlaps;
- transition tokens;
- inverse checks;
- cocycle checks;
- response-localization tokens;
- soldering candidates;
- finite variations; and
- bottom demonstrations.

The current reference fixture is
`research_control/tasks/RT-20260614-095/artifacts/finite_source_witness.yaml`.

## Checks

The checker runs conservative finite checks:

- `check_sep_src`: detects missing source tokens, missing quotient classes,
  duplicate quotient member sets, invalid class references, and bottom
  separation status.
- `check_chart_support` and `check_overlap_support`: confirm chart and overlap
  support are source-defined over known quotient classes.
- `check_inverse_tokens`: confirms declared source inverse tokens are actual
  finite relation inverses.
- `check_cocycle_tokens`: confirms declared source cocycle compositions equal
  the stated target transition token in finite relation algebra.
- `check_rank_coherence`: compares the rank analogue against finite support
  cardinality and overlap stability.
- `check_soldering_uniqueness`: rejects response tokens soldered to
  incompatible source supports.
- `check_variation_preservation`: requires finite variations either to preserve
  named source obligations or fail closed to bottom.
- `check_target_import_flags`: rejects target metric, target atlas, target
  topology, proper-time, benchmark, matter-coupling, Einstein-equation, and
  `g_eff` authority fields outside bottom or authority-warning contexts.
- `check_bottom_conditions`: verifies declared bottom demonstrations fail
  closed.

## Output Statuses

The checker uses the controlled status vocabulary from the implementation plan:

- `pass_candidate_local`
- `fail_nonseparation`
- `fail_topology_noncanonical`
- `fail_transition_incoherent`
- `fail_rank_incoherent`
- `fail_soldering_nonunique`
- `fail_variation_fragile`
- `fail_target_import`
- `bottom`
- `not_applicable`

The process exit code is `0` for a parsed model-check result, including finite
counterexamples. Parse failures return exit code `2` with a JSON error payload.

## CLI

```zsh
.venv/bin/python scripts/research_control/finite_source_cover_model_checker.py \
  --input research_control/tasks/RT-20260614-095/artifacts/finite_source_witness.yaml \
  --json
```

## Acceptance Boundary

A `pass_candidate_local` result means only that the finite input survived the
implemented finite/local checks. It is not a proof of general source-cover
existence or arbitrary finite-variation robustness. A failure result is an
explicit finite counterexample or data-quality obstruction for the checked
fixture only.

Ledger status, source-law adoption, and downstream GR status remain unchanged
unless a separate future physics AgentJob consumes checker output under the
normal audit, refutation, and gate sequence.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 23). *Finite source witness*
[Internal research-control artifact].

The AEther-Flow Research Project. (2026, June 23). *Recommendations
implementation plan continue task* [Internal implementation plan].
