---
authority: "control"
task_id: "RT-20260723-019"
job_id: "AJ-RT-20260723-019-001"
policy_id: "p13_t03_packaging_environment_policy_v1"
status: "active"
---

# P13-T03 packaging and environment policy

## Scope

This policy governs the normal Python environment used by repository scripts,
tests, validators, and memory tooling. It is project-system control only. It
does not install or authorize scientific software, promote physics claims,
establish proof authority, or change the scientific status of any artifact.

## Authoritative dependency surfaces

The dependency contract is a coherent four-file set:

1. `pyproject.toml` declares the supported Python series, direct dependency
   intent, named empty dependency groups, and external-tool metadata.
2. `research_control/tasks/RT-20260723-019/artifacts/requirements.lock` is the
   pip-installable, exact, SHA-256-hashed resolution.
3. `requirements.txt` is the compatibility entry point for existing runtime
   setup paths and includes the lock.
4. `requirements-dev.txt` is the compatibility entry point for existing
   contributor setup paths and includes `requirements.txt`.

The committed lock is installation authority. `pyproject.toml` is maintainer
intent and must resolve byte-for-byte to the same lock body. The compatibility
wrappers must not contain independent package constraints.

The supported normal-path interpreter is CPython 3.12. The complete
normal-path third-party Python set is the already-used
`PyMuPDF==1.27.2.3` and `PyYAML==6.0.3`. PyMuPDF supports PDF extraction;
PyYAML supports tracked YAML control parsing. Every distribution line in the
lock must be exact and must carry one or more SHA-256 hashes. Adding a
distribution, changing a version, changing the Python series, or relaxing hash
enforcement requires a separate bounded project-system task.

## Installation and validation

Ordinary setup uses:

```zsh
python -m pip install --require-hashes -r requirements-dev.txt
```

The Make setup target and every repository-owned CI provisioning step use
`--require-hashes`. Validation targets do not provision dependencies; they
fail closed when the active environment does not satisfy the declared Python
series and exact distribution versions.

Maintainers regenerate the task-local lock only under an authorized dependency
task:

```zsh
uv pip compile pyproject.toml --all-extras --universal \
  --generate-hashes \
  --output-file research_control/tasks/RT-20260723-019/artifacts/requirements.lock
```

`uv` is a lock-maintenance tool, not a normal-path project dependency. The
supported maintenance range is recorded in `pyproject.toml`; the lock remains
pip-installable and does not require `uv` for ordinary setup.

## External tools

Git and Make are repository-operation prerequisites. Lean, TeX, Node.js, and
Playwright are conditional external runtimes: they are required only by a
packet or workflow that explicitly names them. They are not Python
dependencies, and this policy does not provision or upgrade them.

## Licensing and authority

P13-T03 introduces no new operational third-party dependency: both locked
distributions were already used by the repository. Installed distribution
metadata identifies PyMuPDF as dual licensed under GNU Affero GPL 3.0 or an
Artifex commercial license and PyYAML as MIT licensed. Their upstream licenses
and distribution notices remain controlling. The repository-level `LICENSE`
and `NOTICES` preserve the general third-party boundary; this task grants no
license waiver and performs no package publication.

## Failure behavior

Setup or validation fails when the Python series differs, the exact installed
version differs, a wrapper bypasses the lock, a required hash is absent, the
lock cannot be reproduced from `pyproject.toml`, or a repository-owned setup
path installs without hash enforcement. Repair the coherent source set through
a bounded task; do not patch an installed environment or one wrapper as
transaction evidence.
