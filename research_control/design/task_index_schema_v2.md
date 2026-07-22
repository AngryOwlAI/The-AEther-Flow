<!-- authority: control -->

# Research-Control Task Index Schema v2

```yaml
schema_id: "research_control_task_index_v2"
implements_plan_task_id: "P10-T02"
taxonomy_policy: "research_control/design/v21_task_taxonomy_policy.md"
supersedes_generated_schema: "research_control_task_index_v1"
authority_status: "project_control"
scientific_claims_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose

This schema defines the generated task-index v2 view. It adds normalized task
taxonomy and readable titles while preserving every v1 operational field and
the raw free-form `task_type`. The generated CSV, Markdown index, and wiki index
remain navigation derivatives; task files, job files, completion files, source
registries, and protected authority records remain canonical.

## Required CSV columns

Columns appear exactly in this order:

1. `task_id`
2. `parent_task_id`
3. `created_at`
4. `closed_at`
5. `title`
6. `task_type`
7. `work_kind`
8. `milestone`
9. `candidate_family`
10. `result_kind`
11. `authority`
12. `scope`
13. `taxonomy_source`
14. `taxonomy_confidence`
15. `status`
16. `target_derivation_milestone`
17. `milestone_burden`
18. `role_family`
19. `physics_delta`
20. `ledger_rows_changed`
21. `artifact_count`
22. `next_recommended_action`
23. `validation_status`
24. `completion_path`

`title` and `task_type` are raw readable provenance. The six normalized fields
and their source/confidence are derived under
`v21_task_taxonomy_policy_v1`. `target_derivation_milestone` remains the raw v1
compatibility field; `milestone` is the normalized field.

## Source records

The renderer reads:

- `registries/RESEARCH_TASK_REGISTRY.csv`;
- `registries/AGENT_JOB_REGISTRY.csv`;
- `registries/DIRECTOR_DECISION_REGISTRY.csv`;
- `registries/AGENT_ROLE_REGISTRY.csv`;
- `research_control/design/v21_recommendation_backlog.yaml`;
- each tracked `research_control/tasks/<task_id>/00_TASK.yaml`;
- its current AgentJob and qualifying completion when present; and
- `research_control/design/v21_task_taxonomy_policy.md`.

The renderer must preserve missing legacy metadata as blank or `unknown` and
report it; it must not invent stronger scientific meaning.

## Validation rules

- The CSV header must match the 24-column contract exactly.
- CSV and both Markdown derivatives must be byte-fresh against the renderer.
- New tasks at or after the taxonomy policy effective time must carry valid
  explicit normalized fields plus readable title and raw `task_type`.
- Historical ambiguity is visible as `unknown` or low confidence and is not a
  failure by age alone.
- Raw historical task files are not modified by classification.
- A support-only or project-system row must have `physics_delta=false`.
- Generated text may not overread proof, adoption, Gate Chair, Einstein-
  equation, benchmark, or completed-derivation authority.

Passing these rules establishes only task-index integrity. It establishes no
scientific truth, promotion, or protected authority.
