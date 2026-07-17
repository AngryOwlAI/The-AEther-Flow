# P6-T07 Local Validation Wrapper Audit

## Outcome

Make and the local full validation runner now delegate gate selection to the
shared validation planner. The five closed profiles are exposed as Make
targets, while `validate-project-control` and the historical Python runner are
explicit compatibility entry points. During `shadow_planner`, both surfaces
leave command execution with the unchanged private legacy chain.

The focused implementation and compatibility corpus passes. Both required full
shadow entry points also pass against stable closed task state.

## Wrapper Map

| Entry point | Shared request | Execution behavior |
| --- | --- | --- |
| `make validate-fast` | `fast`, explicit paths | selection only |
| `make validate-affected` | `affected`, explicit paths | selection only |
| `make validate-checkpoint-plan` | `checkpoint`, staged paths | selection only |
| `make validate-full` | `full`, explicit empty path set | selection only |
| `make validate-doctor` | `doctor`, local-retrieval scope | selection only |
| `make validate-project-control` | `full` | shared selection then legacy execution |
| `run_full_research_control_validation.py` | `full` | shared selection then legacy execution |

The shared full plan and wrapper plan select the same 27 gate IDs in the same
order at manifest hash
`7d9f04c5b06e7a5385cf7e101dbbdf4cc265f9ab1ee3a0307b2b435f5657747b`.

## Compatibility and Authority

- The runner no longer defines `ValidationCommand` or `base_command_plan`.
- Its retained `command_plan()` and `coverage_map()` APIs are deprecated,
  manifest-derived projections for existing read-only callers; they neither
  select nor execute gates.
- `--plan-only`, `--json`, `--output`, `--tail-chars`, and the historical
  `--include-smoke-tests` argument remain accepted. The latter is a declared
  no-op because `full` already selects the repository test shard.
- Planner configuration failures and legacy Make failures preserve their
  respective exit codes.
- The report schema no longer labels itself local-CI-equivalent. Compatibility
  fields state `ci_equivalent=false`, and every invocation emits deprecation
  status.
- The ordinary research route remains `handoff-0740`; no program state,
  handoff, ontology, derivation, benchmark, proof, or physics claim changed.

## Validation

- 17 focused wrapper and existing orchestration tests: PASS.
- 47 combined wrapper, runner, orchestration, profile, checkpoint-import, and
  validation-artifact compatibility tests: PASS.
- Shared full-plan manifest hash and selected gate sequence parity: PASS.
- Make dry-run mapping and one-chain ownership checks: PASS.
- The first full Make probe reached the 832-test suite and exposed one expected
  active-transaction assertion. After stable task closure, that exact test
  passed in isolation.
- Final `make validate-project-control`: PASS; 832 tests, one expected skip.
- Final historical Python runner: PASS; shared planner PASS, legacy executor
  PASS, 832 tests, one expected skip, no required failures, exit code 0.
- Scientific claims changed: false.
- Ordinary research handoff preserved: `handoff-0740`.
