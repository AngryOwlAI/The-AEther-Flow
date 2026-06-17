# GitHub-Facing Markdown Transcript Repair Audit

## Problem

The previous GitHub-facing Markdown reset copied the teaching-loop interaction
shape into public `github-facing/*.md` pages. That made support-role dialogue
visible as documentation structure instead of letting the Documentation Curator
distill those exchanges into finished reader-facing explanation.

## Root Cause

The GitHub-facing contract treated Student/Teacher-style questions as a
recommended reader device, and the focused audit test accepted a page section
named `Student Questions And Teacher Answers`. That made transcript leakage
possible even though the Documentation Curator role says Student and Teacher
outputs must not write tracked docs directly.

## Repair

- Updated `research_control/design/github_facing_explainer_contract.md` to say
  teaching-loop insights must be distilled into finished prose, diagrams,
  examples, workflow guidance, or practical checks.
- Updated `scripts/project_control/audit_documentation_surfaces.py` to reject
  the raw transcript heading and `Student` or `Teacher` role markers in
  `github-facing/*.md`.
- Updated `tests/test_documentation_surface_audit.py` so Curator-specific page
  shapes remain accepted while raw teaching-loop transcripts fail.
- Updated `scripts/spec_depth_lint.py` and `tests/test_spec_depth_lint.py` so
  teaching-enabled GitHub-facing pages are not forced to contain a `Common
  questions` section. The lint preserves the subject-first self-reference guard
  without dictating one public-page section shape.
- Rewrote all 13 root GitHub-facing Markdown pages to remove public
  Student/Teacher transcript sections and replace them with direct functional
  explanations, workflow guidance, practical reader rules, or public-page
  teaching-loop boundaries.

## Boundary

No canonical ontology source, science draft, tracked HTML derivative, generated
wiki note, role contract, schema contract, routing behavior, benchmark status,
or Gate Chair status was changed by hand. The repaired pages remain
generated-noncanonical GitHub-facing explainers.
