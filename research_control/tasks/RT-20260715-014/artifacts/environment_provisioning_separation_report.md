# P3-T07 validation environment separation report

## Result

V19 `P3-T07` is complete within its project-system boundary. Every public
Make validation entry point now traverses one non-provisioning
`validation-environment` prerequisite. The prerequisite validates the selected
interpreter and installed distributions, then emits a deterministic receipt.
Dependency installation remains an explicit `setup-dev` action and remains an
explicit CI setup step.

## Environment contract

- Supported interpreter: CPython 3.12.
- Required installed distribution: `PyMuPDF`.
- Dependency specification inputs: `requirements.txt` and
  `requirements-dev.txt`.
- Dependency lock digest:
  `62997f5a81cb422703d6e25fbaa4bcc5a294bb13ed2eeaac05a5800edc604f83`.
- Environment fingerprint:
  `11d74e983c23d78f5c2546926aad9b35934c7a69a594949e4c0a61127b2699fc`.
- Validation is read-only with respect to installed packages.

The dependency digest is a canonical SHA-256 over the ordered requirement-file
paths and their bytes. The environment fingerprint binds that digest to the
interpreter implementation and version plus the normalized required installed
distribution versions. The exact algorithm and receipt schema are controlled
by `research_control/design/validation_environment_contract_v1.md`.

## Verification evidence

1. A missing interpreter failed before validation with exit code 2 and concise
   `setup-dev` remediation.
2. A clean CPython 3.12 virtual environment without PyMuPDF failed with exit
   code 2 and named the missing distribution.
3. Running the explicit `setup-dev` target in that fixture installed
   PyMuPDF 1.27.2.3; the next environment check passed.
4. The clean fixture package-state hash was identical before and after
   validation:
   `f384ddcb28bce9b880f753c69ec1f98cd7ab4be2fd2df190fe2cee2df5c6dcf9`.
5. The project environment package-state hash was identical before and after
   the HTML validation route:
   `95c96bb50f8f5cdf9d46e5444b8438c58b38a23be8e53856114c1b15ab2a11b1`.
6. Dry-run plans for the environment, memory, project-control, HTML, and
   documentation-audit targets contained one environment check and no
   provisioning command.
7. The existing orchestration shard passed 9 tests, `validate-memory` passed
   its 86-test affected profile, and the post-regeneration HTML validation
   route passed.
8. After governed staging made the new registered sources visible to Git, the
   complete `validate-project-control` route passed all 634 repository tests
   in 600.899 seconds; total route duration was 642.92 seconds.

The first HTML validation attempt, made before regenerating the registered
Markdown derivative after changing `CONTRIBUTING.md`, correctly failed on a
stale source hash. Regeneration resolved that expected convergence condition;
no validation behavior was weakened.

## Preserved boundaries

- `.github/workflows/project-control-validation.yml` is unchanged and retains
  its explicit dependency-install step.
- `requirements.txt` and `requirements-dev.txt` are unchanged.
- Validator implementations and test sources are unchanged.
- `handoff-0740` remains the ordinary research authority.
- No ontology, derivation, benchmark, scientific claim, or physics-promotion
  authority changed.

## Next dependency-ready packet

On a successful governed checkpoint, v19 `P4-T01` becomes the next separately
bounded packet. It is not implemented here.
