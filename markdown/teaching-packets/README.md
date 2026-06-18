<!-- authority: explanatory -->

# Teaching Packets

This folder contains curated teaching Q&A packets used by the Documentation
Curator.

## Purpose

Teaching packets preserve the useful output of a bounded Student and Teacher
loop. The Student asks reader-centered questions. The Teacher answers from the
selected source bundle. The Documentation Curator then distills those answers
into finished explanatory documentation.

## What Belongs Here

- Curated Q&A packets with declared source specs, source materials, claim
  boundaries, and authority status.
- Reader-confusion analysis, examples, non-examples, glossary notes, and
  source-bound answers that help improve final docs.

## What Does Not Belong Here

- Public-facing raw transcript sections.
- Canonical role, schema, validator, or routing changes.
- Physics claim promotion.
- Generated HTML or generated GitHub-facing Markdown.

## Authority Boundary

Teaching packets are explanatory support only. They do not override source
materials, registries, role contracts, validators, routing behavior, claim
gates, or generated-output boundaries.

## Relevant Check

```zsh
.venv/bin/python scripts/validate_teaching_qa.py --root .
```

