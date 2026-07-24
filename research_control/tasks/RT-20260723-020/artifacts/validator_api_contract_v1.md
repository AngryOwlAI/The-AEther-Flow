<!-- authority: control -->

# Programmatic validator API contract v1

## Scope and authority

`scripts.validation.api` is the stable typed entry point for callers that need
the current validation planner or executor without invoking a shell command.
It adapts the canonical manifest, existing path classifier, planner, tracked
adapter bindings, and executor. It does not create policy, bypass manifest
authority, or confer source, scientific, ontology, benchmark, proof, Gate
Chair, publication, or checkpoint authority.

The v1 public names are:

- `ValidationPlanRequest`
- `ValidationExecutionRequest`
- `ValidationApiError`
- `plan_validation`
- `plan_exit_code`
- `execute_validation`

All other planner and executor modules remain available to their existing
owners but are not added to this v1 stability promise.

## Planning example

```python
from scripts.validation.api import (
    ValidationPlanRequest,
    plan_exit_code,
    plan_validation,
)

request = ValidationPlanRequest(
    profile="affected",
    paths=("scripts/validation/api.py",),
    scopes=("working",),
)
plan = plan_validation(request)
assert plan_exit_code(plan) == 0
print(plan.canonical_json())
```

Planning is pure after source reads: it classifies the supplied
repository-relative paths and returns the existing immutable `ValidationPlan`.
It never imports an execution adapter or runs a command.

## Execution example

```python
from pathlib import Path

from scripts.validation.api import (
    ValidationExecutionRequest,
    execute_validation,
)

execution = execute_validation(
    plan,
    ValidationExecutionRequest(
        receipt_root=Path(".local/validation-receipts"),
        max_workers=4,
    ),
)
raise SystemExit(execution.exit_code)
```

Execution still requires the plan's manifest hash, tracked adapter binding
contract, and executor validation to agree. Mutating gates additionally require
the caller to supply the same bounded mutation inputs required by the executor.
Receipts remain operational evidence under their existing authority fields.

## Status and exit semantics

| Condition | Status | Exit code |
| --- | --- | ---: |
| ready plan or successful execution | `READY`, `PASS`, or `WARN` | `0` |
| executed validation gate fails | `FAIL` | `1` |
| malformed request, unavailable source, manifest mismatch, or blocked configuration | `BLOCKED_CONFIGURATION` | `2` |

`plan_validation` and API setup failures raise `ValidationApiError`; the class
has `status == "BLOCKED_CONFIGURATION"` and `exit_code == 2`. A valid plan is
returned even when its classifier identifies a blocked path, and
`plan_exit_code` maps that plan to `2`. `execute_validation` returns the
existing immutable `ExecutionOutcome`, whose `exit_code` is authoritative for
the operational run.

## Compatibility boundary

The v1 API promises deterministic request normalization, current planner
parity, explicit blocked-configuration semantics, and delegation to tracked
execution bindings. It does not promise that individual gate catalogs,
profiles, obligations, receipt locations, or adapter commands never evolve;
those remain tracked configuration.
