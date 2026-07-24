<!-- authority: control -->

# P13-T06 reproducible environment operations

## What this environment is

P13-T06 uses the lightest mechanism compatible with the repository's current
workflows: an external CPython 3.12 virtual environment provisioned from the
tracked, hash-locked development requirements. It is an equivalent
fresh-machine environment, not an operating-system container.

The environment definition binds the project metadata, runtime and development
locks, validation-environment contract, and the existing Lean proof toolchain
lock by SHA-256. The bootstrap never copies the checkout, `.local`, `.venv`,
Git metadata, recursive-relay goals, credentials, or environment variables
into the external target.

## Validate the definition

From the repository root:

```zsh
.venv/bin/python \
  research_control/tasks/RT-20260724-003/artifacts/bootstrap_fresh_environment.py \
  validate --json
```

This is read-only. It checks the definition, exact input hashes, profile
commands, exclusion rules, and authority boundary.

## Build a clean environment

Choose a new absolute directory outside the checkout. It must not already
exist:

```zsh
/opt/homebrew/bin/python3.12 \
  research_control/tasks/RT-20260724-003/artifacts/bootstrap_fresh_environment.py \
  bootstrap \
  --python /opt/homebrew/bin/python3.12 \
  --target /absolute/new/path/aether-flow-fresh-env \
  --receipt /absolute/new/path/reproduction-receipt.json \
  --json
```

The bootstrap creates the virtual environment, enforces requirement hashes,
and runs the representative research-control, proof/scientific-checker, and
benchmark-equivalence profiles. Command output stays under the external
target; the receipt records only hashes, counts, statuses, and repository-
relative input identities.

## Reproduce the pinned Lean proof object

The formal proof profile is conditional because Lean is not a Python package.
Supply a Lean executable matching the tracked `4.30.0` toolchain selector,
release commit, and archive lock:

```zsh
/opt/homebrew/bin/python3.12 \
  research_control/tasks/RT-20260724-003/artifacts/bootstrap_fresh_environment.py \
  bootstrap \
  --python /opt/homebrew/bin/python3.12 \
  --target /absolute/new/path/aether-flow-fresh-env \
  --lean-bin /absolute/path/to/pinned/lean \
  --receipt /absolute/new/path/reproduction-receipt.json \
  --json
```

The profile rebuilds `SelectorKernel.olean` into the external target and
requires its SHA-256 to match the tracked proof receipt. That byte match is
software-reproduction evidence only. It is not theorem-truth adjudication,
proof authority, physical interpretation, ontology adoption, exact-GR
benchmark promotion, or completed-derivation authority.

## Platform limits

- The core environment supports CPython `3.12` on the repository's declared
  Darwin arm64 and Linux x86-64 hosts; it does not freeze an operating-system
  image.
- The existing Lean archive lock is Darwin arm64. A non-Darwin host requires a
  separately tracked archive lock before formal-build parity can be claimed.
- System certificate stores and package-index availability remain host
  prerequisites for the one-time hash-enforced Python installation.
- Validation receipts describe the tested environment. They do not promote
  any scientific or publication claim.
