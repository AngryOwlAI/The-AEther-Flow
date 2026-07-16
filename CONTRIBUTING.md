<!-- authority: project_control -->

# Contributing

This repository uses tracked research-control state to manage both physics
research and project-system work. Local validation is an operational receipt:
it shows that the controlled surfaces are internally consistent, but it is not
physics proof authority and does not promote ontology, benchmark, Gate Chair,
or completed-derivation status.

## Supported Python

Use CPython 3.12 for local validation. The GitHub Actions project-control
workflow also runs Python 3.12.

## Local Environment

Create a repository-local virtual environment from the repository root:

```zsh
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
```

If `python3.12` is not installed, use the local command that resolves to
CPython 3.12 on your machine. Keep `.venv/` untracked.

## Validation Commands

Use the same Python executable consistently:

```zsh
make PYTHON=.venv/bin/python validate-project-control
```

Memory validation is decomposed by purpose. The ordinary compatibility target
runs read-only memory-core validation and the focused memory test shard. It
does not install dependencies, schedule `memory-sync` or the doctor profile,
or discover the full repository suite. Focused tests may still exercise memory
operations under their own fixture or live-acceptance boundaries:

```zsh
make PYTHON=.venv/bin/python validate-memory
```

Select setup, synchronization, core validation, local operational diagnostics,
or the test shard independently when that is the actual task:

```zsh
make PYTHON=.venv/bin/python setup-dev
make PYTHON=.venv/bin/python memory-sync
make PYTHON=.venv/bin/python memory-validate-core
make PYTHON=.venv/bin/python memory-doctor
make PYTHON=.venv/bin/python test-memory
```

For memory-tool changes and scheduled integration, retain the full compatibility
acceptance path:

```zsh
make PYTHON=.venv/bin/python validate-memory-full
```

No validation target provisions dependencies. `memory-doctor` may refresh
ignored `.local/` retrieval state, but its results are operational diagnostics
and cannot satisfy checkpoint or physics authority.

For read-only generated-surface validation:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

For research-control continuation, start with:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python scripts/research_control/continue_research.py
```

After a state-changing bounded AgentJob, synchronize generated systems before
checkpointing:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
```

## Generated-Output Policy

Edit canonical sources and registries, then regenerate derivatives. Do not
hand-edit generated wiki notes under `wiki/`, generated registry sidecars,
PDFs as authority, generated HTML, or `.local/` retrieval caches. In exact
validator language: Do not hand-edit generated wiki notes.

`.local/` may be refreshed by the memory and retrieval tools, but it is local
cache state and must not be committed as transaction evidence.

## Interpreting Validation

Validator success means the repository's tracked control surfaces and generated
derivatives are synchronized according to the current validators. It is not
physics proof authority and does not establish source-law adoption,
`MetricData(E)` adoption, `g_eff` scope expansion, matter coupling, Einstein
equations, benchmark promotion, Gate Chair verdicts, or a completed derivation.

Exact boundary phrases: not physics proof authority; Einstein equations.
