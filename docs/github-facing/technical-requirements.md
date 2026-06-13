<!-- authority: explanatory -->

# Technical Requirements

Technical requirements are tiered by what the reader needs to do: inspect, validate, regenerate, render diagrams, use local retrieval, or refresh PDFs.

Authority boundary: this page explains setup and validation paths. Scripts, registries, skill contracts, and control records remain authoritative for exact requirements.

## Requirement Tiers

| Tier | Needed for | Requirement status |
| --- | --- | --- |
| Read and inspect | GitHub browsing, source reading, local file inspection. | Browser, text editor, Git, shell. |
| Run validators | Project-control checks, memory scripts, tests. | Python `.venv` and [../../requirements.txt](../../requirements.txt). |
| Regenerate memory/wiki | Source registry refresh, generated wiki notes, semantic extracts, local indexes. | `bootstrap_memory_system.py` and memory-system skill guidance. |
| Regenerate diagram-backed HTML | Mermaid-backed tracked HTML explainers. | Node.js, npm, pinned Mermaid dependencies, Playwright Chromium. |
| Use local retrieval | Obsidian vault, semantic extracts, local caches. | Operator aid, not project authority. |
| Refresh PDFs | TeX-to-PDF derivatives. | Conditional on TeX derivative scope. |

## Core Commands

Validate memory and registry state:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Refresh memory and generated registry/wiki surfaces:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

Run project-system documentation impact validation:

```zsh
.venv/bin/python scripts/project_control/validate_documentation_impact.py
```

Run research-control validation:

```zsh
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
```

Run tests:

```zsh
.venv/bin/python -m unittest discover -s tests
```

## Operator Aids

Obsidian, browser previews, local semantic extracts, global Codex skills, and plugins can be useful. They are not repository authority. They must point back to tracked source files and registry rows.

## Source Basis

- [../../markdown/html-explainer-specs/technical-requirements-explainer.md](../../markdown/html-explainer-specs/technical-requirements-explainer.md)
- [../../README.md](../../README.md)
- [../../requirements.txt](../../requirements.txt)
- [../../Makefile](../../Makefile)
- [../../.codex/skills/project-memory-system/SKILL.md](../../.codex/skills/project-memory-system/SKILL.md)
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)

