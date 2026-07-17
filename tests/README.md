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

Run the fixture-backed memory-system unit module:

```zsh
.venv/bin/python -m unittest tests.test_memory_system_unit
```

Run the two full-repository memory acceptance checks explicitly:

```zsh
.venv/bin/python -m unittest tests.test_memory_system_live
```

Run the miniature-repository Obsidian and SQLite unit module:

```zsh
.venv/bin/python -m unittest tests.test_obsidian_wiki_unit
```

Run the single read-only full-source Obsidian generation-and-search acceptance:

```zsh
.venv/bin/python -m unittest tests.test_obsidian_wiki_live
```

The broad research-control inventory is owned by six focused discovery shards:

```zsh
.venv/bin/python -m unittest tests.test_research_control_policy
.venv/bin/python -m unittest tests.test_research_control_active_state
.venv/bin/python -m unittest tests.test_research_control_continuation
.venv/bin/python -m unittest tests.test_research_control_checkpoint
.venv/bin/python -m unittest tests.test_research_control_metrics
.venv/bin/python -m unittest tests.test_research_control_live_integration
```

The policy, active-state, continuation, checkpoint, and metrics shards are the
selectable fast surfaces. The live-integration shard alone owns the declared
full-corpus research-control validation checks. The shared shard map fails
closed if a source test is added, removed, renamed, duplicated, or left
unassigned.

Direct compatibility commands remain available and still run the complete
148-test source inventory:

```zsh
.venv/bin/python -m unittest tests.test_research_control
.venv/bin/python -m unittest tests.test_validate_research_control
```

Run the memory-focused shard used by the ordinary memory acceptance profile:

```zsh
make PYTHON=.venv/bin/python test-memory
```

The shard covers the extracted memory operations, memory CLI modes,
fixture-backed memory-system behavior, miniature-repository Obsidian support,
and Make orchestration. It excludes the live validate-only,
bootstrap-idempotence, and full-source Obsidian checks and does not run the
complete repository suite. Use the full compatibility profile when a
memory-tool change requires the scheduled integration backstop:

```zsh
make PYTHON=.venv/bin/python validate-memory-full
```

## Authority Boundary

Tests provide evidence about expected behavior. Passing tests are not
independent scientific authority and do not replace source registries,
documentation-impact receipts, or research-control validation.
