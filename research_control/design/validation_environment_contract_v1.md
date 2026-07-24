<!-- authority: control -->

# Validation environment contract v1

## Purpose and authority

This contract separates environment provisioning from validation. A validator
evaluates an already provisioned environment. It must not create a virtual
environment, install a package, upgrade a package, or otherwise change the
dependency state whose behavior it is measuring.

This is project-control authority only. Environment checks, fingerprints,
tests, receipts, and checkpoint commits are not physics proof authority and do
not promote ontology, benchmark, Gate Chair, or completed-derivation status.

## Supported environment

The v1 local and CI validation environment is:

- CPython `3.12`;
- project metadata and groups from `pyproject.toml`;
- the exact hash-locked runtime dependency set at
  `research_control/tasks/RT-20260723-019/artifacts/requirements.lock`;
- the cumulative runtime and quality-tool dependency set at
  `research_control/tasks/RT-20260723-020/artifacts/quality-requirements.lock`;
- compatibility wrappers in `requirements.txt` and `requirements-dev.txt`;
  and
- installed distributions `PyMuPDF` and `PyYAML`, the complete third-party
  runtime set currently required by repository validation, plus exact `mypy`
  and `ruff` distributions for the bounded quality profile.

`PyMuPDF` and `PyYAML` are exact-pinned in `pyproject.toml`, and the task-local
lock records package-index SHA-256 hashes for their resolved artifacts.
`requirements.txt` preserves the runtime pip entry point by including the
runtime lock. `requirements-dev.txt` preserves the development entry point by
including the cumulative quality lock. Neither wrapper carries independent
version ranges.
The v1 `dependency_lock_digest` is the deterministic digest of the complete
metadata, lock, and wrapper surfaces. Exact installed distribution versions are
also recorded separately in the environment fingerprint and must match the
declared pin.

## Provisioning boundary

Provisioning is explicit:

```zsh
python3.12 -m venv .venv
make PYTHON=.venv/bin/python setup-dev
```

CI may create an environment and install requirements in setup steps before a
validation command. A Make target whose purpose is validation, synchronization,
doctor diagnostics, testing, or documentation audit must not invoke `pip
install` or depend on `setup-dev`.

## Environment prerequisite gate

`make validation-environment` is the common read-only prerequisite for Make
validation entry points. It performs these checks in order:

1. the selected `PYTHON` path is executable;
2. the interpreter major and minor version equal `3.12`;
3. every required distribution is installed at the exact locked version;
4. the project metadata, both locks, and both compatibility wrappers exist; and
5. a compact PASS receipt and environment fingerprint can be produced.

`make quality-environment` adds exact `mypy==2.3.0` and `ruff==0.16.0`
requirements after the common runtime check. This split keeps runtime-only
legacy and memory validation entry points compatible while making quality-tool
requirements explicit for `make validate-quality`.

A failure exits before the requested validation gate runs. The error names the
missing prerequisite and provides one bounded remediation command. The gate
does not invoke pip and does not modify installed package state.

## Deterministic dependency digest

The `dependency_lock_digest` is SHA-256 over this ordered byte stream:

```text
pyproject.toml + NUL + file bytes + NUL
research_control/tasks/RT-20260723-019/artifacts/requirements.lock + NUL + file bytes + NUL
research_control/tasks/RT-20260723-020/artifacts/quality-requirements.lock + NUL + file bytes + NUL
requirements.txt + NUL + file bytes + NUL
requirements-dev.txt + NUL + file bytes + NUL
```

Paths use the repository-relative spellings shown above and UTF-8 encoding.
The ordering is fixed by `VALIDATION_REQUIREMENT_FILES` in `Makefile`.

## Environment fingerprint

The fingerprint input is canonical compact JSON with lexicographically sorted
keys:

```yaml
schema_id: "validation_environment_v1"
python_implementation: string
python_version: string
dependency_lock_digest: lowercase_sha256
installed_distributions:
  PyMuPDF: exact_version_string
  PyYAML: exact_version_string
```

`environment_fingerprint` is the lowercase SHA-256 of those canonical JSON
bytes. A Python patch-version change, dependency-specification change, required
distribution version change, or interpreter-implementation change therefore
changes the fingerprint. Future cache work may use this value only as one
component of the complete evidence-identity key.

The quality gate emits its own compact prerequisite receipt containing exact
`mypy` and `ruff` versions. The common environment fingerprint intentionally
continues to inventory only runtime distributions while its dependency digest
covers both locks; this avoids making runtime-only gates depend on installed
development tools.

## Receipt contract

The compact gate receipt contains:

- `gate_id: validation_environment`;
- `status: PASS`;
- `provisioning: false`;
- `schema_id`;
- `python_implementation` and `python_version`;
- `dependency_specification_files`;
- `dependency_lock_digest`;
- `installed_distributions`; and
- `environment_fingerprint`.

The receipt describes the evaluated environment. It does not establish that a
later validator passed and cannot satisfy a staged-tree or scientific
obligation by itself.

## Validation and rollback

Acceptance requires missing-interpreter and missing-dependency failures, an
explicit setup-then-check fixture, identical installed-package inventory before
and after validation, dry-run proof that validation plans contain no package
installation, the bounded Ruff/mypy/path profile, and the current
`legacy_consolidated` project-control acceptance.

Rollback the Make prerequisite wiring if explicit setup documentation becomes
unavailable or if the digest becomes nondeterministic. Preserve CI setup steps,
the hash-enforcing requirements compatibility paths, ordinary research handoff
`handoff-0740`, and every physics claim boundary.
