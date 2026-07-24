<!-- authority: control -->

# Quality and portability policy v1

## Incremental quality baseline

P13-T04 adopts exact hash-locked `ruff==0.16.0` and `mypy==2.3.0` for a
deliberately bounded first surface:

- `scripts/validation/api.py`
- `scripts/validation/portability.py`
- `scripts/validation/models.py`
- `tests/test_validation_api.py`
- `tests/test_validation_portability.py`

Ruff checks import ordering on the new files, pyflakes errors, and selected
`E4`, `E7`, and `E9` syntax families. The pre-existing import-order difference
in `scripts/validation/models.py` is explicitly baselined rather than changed
outside the task allowlist. Mypy uses CPython 3.12 semantics and strict checking
for the three named validation modules. This is not a whole-repository
formatting or typing claim. Historical code can move into the baseline only
through later bounded tasks.

`make validate-quality` runs the environment prerequisite, Ruff, mypy, the
shared path linter, and focused tests. Validation targets do not install or
upgrade dependencies; `make setup-dev` is the explicit provisioning step.

## Supported matrix

The supported Python series remains CPython 3.12. The
`quality_portability_matrix` GitHub Actions job declares these cells:

| Operating system | Python |
| --- | --- |
| `ubuntu-latest` | `3.12` |
| `macos-latest` | `3.12` |

The matrix makes the supported version axis explicit without expanding it.
Task-local evidence may claim only cells actually observed. A local macOS run
does not establish a hosted GitHub Actions result, and source inspection of the
workflow does not establish that either hosted cell executed.

## Prospective path policy

`scripts.validation.portability` shares the exact P10-T07 repository-relative
path limits and failure categories:

- POSIX `/` separators and no absolute, empty, `.` or `..` segments;
- Unicode NFC;
- maximum 180 characters and 220 UTF-8 bytes for the relative path;
- maximum 96 characters and 120 UTF-8 bytes for every component and filename;
- no control characters, Windows-forbidden characters, reserved device names,
  or trailing spaces or periods; and
- no distinct path spellings that collide after NFC normalization and Unicode
  casefolding.

The implementation is prospective only. It evaluates paths supplied by a
caller and never renames, truncates, deletes, or migrates historical content.
Exit code `0` means the supplied set passed, `1` means a portability finding or
casefold collision was found, and `2` is reserved by command-line parsing for
invalid invocation.

Example:

```zsh
.venv/bin/python -m scripts.validation.portability \
  --path scripts/validation/api.py \
  --path scripts/validation/portability.py \
  --json
```

## Dependency and authority boundary

The cumulative exact development lock is
`research_control/tasks/RT-20260723-020/artifacts/quality-requirements.lock`.
`requirements-dev.txt` includes that lock; the P13-T03 runtime lock and
`requirements.txt` remain the runtime-only compatibility surface.

Quality PASS receipts are operational project-control evidence only. They do
not prove physics, promote ontology or a benchmark, change Distance-to-GR,
authorize publication, or satisfy Gate Chair or checkpoint authority.
