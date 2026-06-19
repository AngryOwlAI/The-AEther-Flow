<!-- authority: control -->

# Phase 5C Technical Requirements Before/After Review

## Page

`technical-requirements-explainer`

## Before

The technical-requirements subject existed historically under the retired
explainer creation process. The active publication-process registry did not
contain a reviewed Phase 5C publication packet for the current local
requirement tiers, Codex app harness assumption, Python environment,
Makefile targets, HTML screenshot QA requirements, PDF derivative path, and
tool-versus-authority boundary.

## After

The Phase 5C packet adds:

- `markdown/publication-briefs/technical-requirements.publication-brief.md`
- `markdown/html-explainer-specs/technical-requirements-explainer.md`
- `github-facing/technical-requirements-explainer.md`
- `html/technical-requirements-explainer.html`
- desktop screenshot evidence
- mobile screenshot evidence
- a reviewed publication-brief registry row

The GitHub-facing page reads as a native contributor/operator guide. The HTML
page uses an annotated requirement-tier table, command-family cards, a
source-spec-first HTML sequence, and a tool-versus-authority boundary panel.
Both surfaces state that technical capability does not grant authority and
that generated outputs remain noncanonical.

## Boundary Review

PASS:

- Requirement tiers are separated across inspection, governed Codex operation,
  Python checks, memory/wiki refresh, HTML screenshot QA, PDF derivatives, and
  tests.
- `.venv`, `requirements.txt`, Makefile targets, and repository command
  families are explained without changing them.
- Codex app is framed as the current governed harness, not as scientific
  authority or permanent lock-in.
- Node, npm, Playwright, and Mermaid are scoped to diagram or screenshot work
  where the source files require them.
- Local retrieval, generated HTML, screenshots, and tests are explicitly
  support/evidence surfaces, not source authority.
- No dependency, validator behavior, Makefile target, command semantics,
  harness policy, role authority, routing, checkpoint, generated-output
  authority, or physics claim status changed.

Remaining risk:

- The page is an operator guide, not an installation troubleshooter for every
  host machine. If a future environment needs platform-specific instructions,
  that should be a separate bounded maintenance packet.
