<!-- authority: control -->

# P11-T03 CI Validation Maintainer Guide Receipt

## Scope

`RT-20260703-022` completed the v15 P11-T03 maintainer-guide packet by adding
the `Local Validation Pipeline` section to `research_control/README.md`.

## Maintainer Guide Coverage

- How to run locally:
  `.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json`
- Durable receipt option: `--output <path>`.
- Optional broad smoke layer: `--include-smoke-tests`.
- When to run: before checkpointing research-control transactions, after
  bootstrap or render commands that can change generated derivatives, and when a
  maintainer needs one command for the required P11 gates.
- What PASS means: the configured local control checks completed for the
  current repository state.
- What PASS does not mean: validation is not physics proof authority, source-law
  adoption, route-freeze authority, Gate Chair authority, benchmark promotion,
  completed derivation, program-wide no-go conclusion, or future source-extension
  impossibility.
- Failure interpretation: the guide names claim-language lint failures,
  research-control and registry-consistency failures, diff allowlist failures,
  generated derivative drift, documentation-impact failures, and route advisory
  diagnostics.

## Validation

- Task-local maintainer guide validator: `PASS`.
- Operational receipt only: `true`.
- Physics delta: `no_distance_delta`.

## Next Route

The next bounded continue-research packet is v15 P12-T01 claim graph schema.
