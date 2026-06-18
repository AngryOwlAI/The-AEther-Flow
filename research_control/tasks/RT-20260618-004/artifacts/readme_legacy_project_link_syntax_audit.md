# README Legacy Project Link Syntax Audit

## Scope

This audit covers the human-edited `README.md` line in the `## This repo`
section. The changed text broke Markdown link syntax around the earlier
project name, `The Æther GR Derivation`.

## Finding

The live diff removed the local absolute link target but left an unmatched
opening bracket:

```md
[The Æther GR Derivation.
```

That produced malformed Markdown and could cause the rest of the sentence to
render incorrectly.

## Correction

The README now uses plain text:

```md
The Æther GR Derivation.
```

This preserves the apparent human intent to avoid the non-portable local path
while restoring valid Markdown. No physics claim, benchmark status, ontology
authority, or control behavior changed.

## Boundary

Allowed:

- README front-door Markdown syntax repair;
- registered Markdown hash refresh;
- generated memory/wiki derivative refresh; and
- task-local control and validation records.

Forbidden:

- canonical ontology edit;
- benchmark promotion;
- science draft authority expansion;
- generated derivative as independent authority; and
- claim-boundary or routing behavior change.
