<!-- authority: control -->

# README Project Website Front-Door Update Review

Task: `RT-20260629-001`
Job: `AJ-RT-20260629-001-001`

## Scope

This packet integrates a human-authored root README update:

- add the project website as an under-development informational surface;
- normalize the added Markdown into stable front-door prose; and
- remove `Step-by-step-Comments/` from the displayed project map because it is
  a local untracked directory, not a tracked public repository surface.

## Evidence

- `git status --short --untracked-files=all` initially showed `M README.md`.
- `git diff -- .agents/roles/README.md` showed no diff.
- `git ls-files -- Step-by-step-Comments` showed no tracked files under that
  local directory.
- `curl -I --max-time 15 https://the-aether-flow-website.pages.dev` returned
  `HTTP/2 200`.

## Boundary

The packet does not change physics claims, ontology status, benchmark status,
Gate Chair status, derivational conclusions, role authority, validator
behavior, routing behavior, write permissions, checkpoint behavior, or
generated-output authority.

## Remaining Risk

The website URL is an external deployment target and can drift independently of
this repository. Future status, route, or deployment changes should update the
canonical README wording first and then regenerate metadata.
