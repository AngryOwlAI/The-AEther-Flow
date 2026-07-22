<!-- authority: control -->

# Prospective artifact identity and portable-path policy

## Status and scope

This `P10-T07` control policy applies prospectively to new project-control
artifacts that explicitly adopt `artifact_path_policy_v1`. It does not move,
rename, rewrite, delete, or weaken any historical path. Existing registered
paths remain authoritative under their current source registries and Git
history. A policy PASS is operational evidence only; it is not scientific
proof, ontology adoption, benchmark authority, or publication authority.

## Identity contract

Every adopted reference uses all of the following fields:

- `identity`: `sha256:<64 lowercase hexadecimal characters>`;
- `content_sha256`: the same full digest, recomputed from resolved bytes;
- `content_path`: a repository-relative portable path;
- `stable_alias`: a unique manifest key matching
  `[a-z0-9][a-z0-9._-]{0,47}`;
- `title`: human-readable metadata that is not encoded into the filename;
- `media_type`, `source_path`, and `source_sha256`; and
- explicit non-authority and historical-path-preservation flags.

A digest prefix may be displayed for humans but cannot resolve or verify an
artifact. The pilot uses full-digest filenames under `artifacts/ca/` and checks
the full digest again after reading the bytes. Stable aliases are deterministic
manifest records, not symlinks, filesystem redirects, mutable scientific
identities, or independent authority.

## Portable-path limits

The task-local linter enforces:

| Rule | Limit or condition |
| --- | --- |
| Repository-relative path | at most 180 Unicode code points and 220 UTF-8 bytes |
| Any component | at most 96 code points and 120 UTF-8 bytes |
| Filename | at most 96 code points and 120 UTF-8 bytes |
| Separator | POSIX `/` only; absolute paths and backslashes fail |
| Normalization | Unicode NFC exactly |
| Segments | no empty, `.`, or `..` segment |
| Trailing characters | no component ending in a space or period |
| Portable characters | no control character or Windows-forbidden `< > : " \\ | ? *` |
| Reserved names | Windows device names `CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, and `LPT1`-`LPT9` fail case-insensitively |
| Candidate set | no NFC-and-casefold collision |

The 180-character repository-relative limit leaves a 70-character checkout
budget under the legacy 260-character Windows path envelope. A checkout whose
absolute root exceeds that budget must use a shorter root or an explicitly
validated long-path environment; the policy never truncates a path. The
component byte limit is below the common 255-byte macOS and Linux component
limit. Passing these conservative profiles does not claim compatibility with
every filesystem or deployment environment.

## Filename and title rule

New filenames use short stable ASCII slugs or a full content digest. Human
titles belong in structured metadata or a document heading. A title change
therefore does not force a path change. Established task IDs and historical
parent directories are preserved; the prospective filename rule applies to
new leaves created under an authorized output root.

## Resolution algorithm

1. Select the unique `stable_alias` in one validated manifest.
2. Require a full `sha256:` identity and identical `content_sha256`.
3. Lint `content_path` against the portable-path policy.
4. Read bytes from the exact repository-relative path without following an
   alias into a different authority surface.
5. Recompute SHA-256 and require exact equality.
6. Retain `source_path` as provenance; do not infer scientific status from the
   copy, alias, digest, validator, or manifest.

Any ambiguity, collision, absent byte stream, hash mismatch, normalization
drift, or path violation fails closed.

## Commands

```zsh
.venv/bin/python research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py --write --json
.venv/bin/python research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py --check --json
.venv/bin/python research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py --lint-path research_control/tasks/RT-20260722-002/artifacts/example.json --json
```

The shared validator and CI integration requested by `P13-T04` remain outside
this task. This packet supplies the validated policy, implementation, fixtures,
and content-reference pilot that a later authorized integration may consume.
