---
name: pdf-derivative-build
description: Front door for managed TeX-to-PDF derivative builds.
---

# PDF Derivative Build

Use this skill when building registered project PDFs from registered TeX source.

Managed builds use `pdflatex` and write only to the derivative PDF lanes:

- `ontology/pdfs/`
- `manuscripts/pdfs/`

Scratch builds for unregistered TeX must write only under `.local/` and must not
update registries.

Implementation is delegated to:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/build_pdf_derivatives.py
```
