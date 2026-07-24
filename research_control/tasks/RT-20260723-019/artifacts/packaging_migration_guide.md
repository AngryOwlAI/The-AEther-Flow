---
authority: "control"
task_id: "RT-20260723-019"
job_id: "AJ-RT-20260723-019-001"
guide_id: "p13_t03_packaging_migration_guide"
status: "active"
---

# Migrating to the P13-T03 dependency contract

## Contributor setup

Existing entry points remain valid. Create or activate a CPython 3.12 virtual
environment and run:

```zsh
make PYTHON=.venv/bin/python setup-dev
```

The target now installs through `requirements-dev.txt` with pip hash
enforcement. Direct installs from `pyproject.toml`, unpinned `pip install`
commands, and edits to only one requirements wrapper are outside the normal
contract.

If an existing environment contains a different PyMuPDF or PyYAML version,
recreate the environment or reinstall through the hash-locked setup target.
The validation targets inspect the environment but never repair it.

## CI and automation

Repository-owned setup steps retain their current requirements-file entry
points. Each provisioning command must include `--require-hashes`; downstream
validation commands remain read-only. Cache keys and environment fingerprints
include `pyproject.toml`, the task-local lock, and both compatibility wrappers.

## Maintainer dependency change

A future dependency update must be one bounded project-system transaction:

1. Confirm that the task authorizes the package, version, license review, and
   affected setup paths.
2. Edit direct intent and relevant groups in `pyproject.toml`.
3. Regenerate the universal hash lock with the command recorded in
   `pyproject.toml`.
4. Review the package/version/hash delta and update license notices when the
   dependency set requires it.
5. Keep `requirements.txt` and `requirements-dev.txt` as lock-only
   compatibility wrappers.
6. Run the task-local packaging validator in a clean CPython 3.12 environment,
   focused tests, documentation-impact validation, research-control
   validation, memory synchronization, and the governed checkpoint.

Do not regenerate a lock merely to absorb an upstream release. Exact changes
must be intentional and reviewed.

## Conditional external runtimes

Lean, TeX, Node.js, and Playwright remain separately managed. A Python setup
does not prove those tools exist, and their absence does not invalidate a task
that does not require them. A packet that requires one must perform its own
bounded preflight.

## Rollback

Rollback means restoring one previously validated coherent set:
`pyproject.toml`, lock, wrappers, Make/CI consumers, environment policy, and
fingerprint inputs. Do not relax hashes or replace the lock with a version
range as an emergency workaround. A rollback is a new governed transaction
with its own validation and checkpoint.
