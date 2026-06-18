<!-- authority: explanatory -->

# Tests

This folder contains Python unit tests for the repository's memory,
documentation, project-control, research-control, and explainer tooling.

## Coverage Areas

- Memory-system bootstrap and generated registry behavior.
- Obsidian/wiki extraction and local retrieval support.
- Project-change classification and documentation-surface audits.
- Research-control validation and checkpoint boundaries.
- HTML explainer enhancement, spec-depth linting, and teaching-QA validation.

## What Belongs Here

- Unit tests for scripts and project-control behavior.
- Fixtures embedded in tests when they are small and deterministic.

## What Does Not Belong Here

- Runtime output.
- Generated reports.
- Task-local artifacts.
- Large external fixtures unless a future task explicitly adds them.

## Commands

Run the full test suite:

```zsh
.venv/bin/python -m unittest discover -s tests
```

Run one test module:

```zsh
.venv/bin/python -m unittest tests.test_memory_system
```

## Authority Boundary

Tests provide evidence about expected behavior. Passing tests are not
independent scientific authority and do not replace source registries,
documentation-impact receipts, or research-control validation.

