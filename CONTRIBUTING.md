<!-- authority: project_control -->

# Contributing

This repository uses tracked research-control state to manage both physics
research and project-system work. Local validation is an operational receipt:
it shows that the controlled surfaces are internally consistent, but it is not
physics proof authority and does not promote ontology, benchmark, Gate Chair,
or completed-derivation status.

## Supported Python

Use CPython 3.12 for local validation. The GitHub Actions quality matrix makes
that supported version explicit on Linux and macOS.

## Local Environment

Create a repository-local virtual environment from the repository root:

```zsh
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --require-hashes -r requirements-dev.txt
```

If `python3.12` is not installed, use the local command that resolves to
CPython 3.12 on your machine. Keep `.venv/` untracked.

Provisioning is an explicit setup operation. `pyproject.toml` owns project
metadata and dependency groups. The P13-T03 task-local `requirements.lock`
owns the exact runtime set and SHA-256 hashes; the P13-T04
`quality-requirements.lock` owns the cumulative runtime, Ruff, and mypy set.
`requirements.txt` and `requirements-dev.txt` are the runtime and development
compatibility wrappers, respectively. Validators inspect the selected
environment and never install or upgrade packages. GitHub Actions follows the
same boundary by creating its environment and installing the applicable
hash-locked requirements before it invokes validation.

## Validation Commands

Use the same Python executable consistently:

```zsh
make PYTHON=.venv/bin/python validation-environment
make PYTHON=.venv/bin/python validate-quality
make PYTHON=.venv/bin/python validate-project-control
```

`validation-environment` is a read-only prerequisite shared by every Make
validation entry point. It requires CPython 3.12 and the distributions named by
the validation contract, then emits a compact JSON receipt containing the
Python version, exact installed dependency versions, a deterministic digest of
`requirements.txt` plus `requirements-dev.txt`, and an environment fingerprint.
The digest covers `pyproject.toml`, the exact lock, and both compatibility
wrappers, including both exact locks. The environment gate also rejects an
installed runtime distribution whose version differs from the lock.
`quality-environment` separately requires exact Ruff and mypy versions before
the incremental quality profile runs. The fingerprint is suitable as one input
to later exact-tree cache keys; it is not scientific evidence or proof
authority.

If the interpreter or a required distribution is missing, validation stops
before running a gate and prints one setup command. Create the environment if
needed, then provision it explicitly:

```zsh
python3.12 -m venv .venv
make PYTHON=.venv/bin/python setup-dev
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

No validation target provisions dependencies. The explicit `setup-dev` target
and the setup steps in `.github/workflows/project-control-validation.yml` own
provisioning. `memory-doctor` may refresh ignored `.local/` retrieval state,
but its results are operational diagnostics and cannot satisfy checkpoint or
physics authority. The normative environment and fingerprint rules are in
`research_control/design/validation_environment_contract_v1.md`.

Maintainers regenerate the lock only when a bounded task authorizes dependency
changes:

```zsh
uv pip compile pyproject.toml --all-extras --universal \
  --generate-hashes \
  --output-file research_control/tasks/RT-20260723-019/artifacts/requirements.lock
```

The cumulative quality lock uses the same discipline:

```zsh
uv pip compile pyproject.toml --group dev --all-extras --universal \
  --generate-hashes \
  --output-file research_control/tasks/RT-20260723-020/artifacts/quality-requirements.lock
```

Ordinary contributors do not need `uv`; pip consumes the committed lock through
the compatibility wrappers. External tools such as Git, Make, Lean, TeX,
Node.js, and Playwright are recorded in `pyproject.toml` but are not Python
dependencies and are required only by workflows that explicitly name them.

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
