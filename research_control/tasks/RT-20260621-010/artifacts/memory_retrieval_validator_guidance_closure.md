<!-- authority: control -->

# Memory Retrieval And Validator Guidance Closure

## Analysis

The packet resolves four registered project-improvement signals without
changing physics claims or generated-output authority.

## Changes Made

- `query_memory.py search` now supports `--literal` and `--exact-id`.
- The memory library catches SQLite FTS parse errors and retries with a safe
  literal FTS phrase while also returning exact registry-field matches.
- Exact lookup now searches all registry CSVs for control identifiers including
  `task_id`, `job_id`, `agent_job_id`, `decision_id`, `signal_id`, `edge_id`,
  source-object fields, and record paths.
- Memory status output now separates `core_validation_status`,
  `local_retrieval_status`, and `freshness_categories` with `blocking`,
  `non_blocking`, and `local_cache_only` buckets.
- `strict_yaml.py` accepts only the inline empty-list token `[]` and emits
  empty lists as `[]`.
- AgentJob schema and templates now state that memory-preflight
  `returned_object_ids` are inspected canonical source object IDs only.
- Physics-facing forbidden source-class examples now include
  `candidate_reconstruction`.
- Documentation-impact classifier and validator messages now explain when a
  no-op `documentation_impact.yaml` with `docs_update_required: false` is
  sufficient.

## Recommendation Coverage

1. Exact-ID query mode and fallback registry lookup: implemented through
   `search --exact-id`, expanded `lookup`, and FTS-error fallback.
2. Refresh path and non-blocking freshness classification: implemented through
   structured status fields and verified with `sync_obsidian_vault.py`.
3. Narrow `[]` parser support and tests: implemented in `strict_yaml.py` with
   regression coverage for `unresolved_conflicts: []`.
4. Memory-preflight template and validator guidance: implemented in schema,
   templates, and validator error text for generated retrieval IDs.
5. Forbidden-source-class vocabulary: implemented in the AgentJob template and
   ontology-law receipt examples with `candidate_reconstruction`.
6. Documentation-impact no-op guidance: implemented in classifier output,
   validator messages, schema example, and tests.
7. Separated blocking, non-blocking, and local-cache-only output: implemented in
   `query_memory.py status --json` payloads.

## Boundaries

No canonical ontology source, physics manuscript, benchmark source, generated
HTML, or generated wiki note was hand-edited. Generated memory derivatives were
refreshed through approved scripts only.
