# Legacy Ontology Snapshot Audit

## Requirement Mapping

- Legacy folder exists: `legacy_ontology/`.
- TeX snapshot folder exists: `legacy_ontology/tex/`.
- PDF snapshot folder exists: `legacy_ontology/pdfs/`.
- Live ontology remains in place: `ontology/` was not removed and current
  canonical TeX files under `ontology/tex/` were not edited.
- Memory bootstrap registers legacy TeX rows with `TEX-LEGACY-ONTOLOGY-*`
  object IDs.
- Memory bootstrap registers legacy PDF rows with `PDF-LEGACY-ONTOLOGY-*`
  object IDs.
- Memory bootstrap registers legacy Markdown rows as archival noncanonical
  snapshot material.
- Wiki notes are generated through bootstrap for legacy Markdown TeX and PDF
  objects.

## Snapshot Contents

The copied TeX and PDF payload files were hash-checked against `ontology/tex/`
and `ontology/pdfs/` before documentation edits were applied to the legacy
README surfaces.

Counts after bootstrap:

- Legacy Markdown source rows: 5.
- Legacy TeX source rows: 8.
- Legacy PDF derivative rows: 8.
- Generated legacy wiki notes: 21.

## Claim Boundary

This transaction does not edit canonical ontology TeX, authorize an ontology
extension, promote the benchmark, issue a Gate Chair verdict, or claim a
completed derivation. It only adds a registered archival snapshot lane and
refreshes derivative memory/wiki surfaces.
