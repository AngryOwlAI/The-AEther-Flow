---
name: continue-research
description: Resolve tracked research-control state and set up or execute one bounded AgentJob per invocation.
---

# Continue Research

Use this skill for research-control continuation in Flow.

## Control Principle

The Director of Research is a first-class phase. Codex acts as Director only to
author the research-path decision; scripts validate boundaries and checkpoint
state. The Director chooses the next bounded step, roles constrain execution,
skills provide procedures, and gates control claim promotion.

## Workflow

1. Read `AGENTS.md` and `research_control/AGENTS.md`.
2. Resolve tracked state and request the Director context packet:

   ```zsh
   .venv/bin/python scripts/research_control/continue_research.py
   ```

   The script emits JSON by default. Use `--summary` only for a human-readable
   rendering of the same packet.

3. If the packet boundary is `director_decision_required`, enter Director of
   Research mode under `.agents/roles/research_ops/director-of-research.v0.1.0.md`.
   Write or reuse exactly one Director Decision Record and one AgentJob. The
   Director may create a new task only when tracked state proves that the active
   task is completed, blocked, human-gated, or the latest handoff explicitly
   requires a separate task.

4. If an existing pending or active AgentJob matches `program_state.yaml`, the
   latest DDR, the active task, and the job registry, reuse it. If pending jobs
   conflict, stop or supersede through a tracked Director/Process Integrity
   repair decision. Do not rewrite activated DDRs or AgentJobs.

5. Use an execution-role record for the AgentJob. Registered roles, task
   overlays, and one-job provisional roles are represented by
   `execution_role_ref` records under
   `research_control/tasks/<task_id>/roles/` and registered in
   `registries/ROLE_EXECUTION_REGISTRY.csv`. Base role contracts remain stable;
   task-specific adaptation must be explicit.

6. Execute exactly one authorized AgentJob unless a stop condition applies:
   human gate required, validation failure, no role fit, authority expansion,
   write-path conflict, or a planning-only/control-only Director decision.

7. After a state-changing AgentJob completion, create the durable response
   transaction: role output artifact if any, completion record, registry updates,
   new handoff pair, and `program_state.yaml` update when state changes.

8. Synchronize generated systems before commit. Always run:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
   ```

   If a changed registered TeX source has `pdf_required=true`, build that
   specific PDF derivative, then rerun the bootstrap. HTML is synchronized
   through the HTML registry when HTML exists; generated HTML is created only
   when the AgentJob explicitly authorizes it from a registered Markdown spec.

9. Run post-execution validation:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
   .venv/bin/python scripts/research_control/validate_research_control.py
   .venv/bin/python scripts/research_control/validate_research_control.py --check-diff
   ```

10. Checkpoint only after a successful state-changing transaction:

    ```zsh
    .venv/bin/python scripts/research_control/checkpoint_research_transaction.py
    ```

    The checkpoint script captures preflight dirty state, blocks unrelated
    changes, synchronizes generated systems, validates, stages only allowed
    transaction paths, and commits with a deterministic template. Push is never
    performed unless explicitly requested.

11. If the invocation is read-only, blocked, human-gated, or produces no file
    changes, report the state and do not create an empty commit.

## Checkpoint Boundaries

The checkpoint script globally allows only standard memory-system generated
registries, generated registry sidecars, and `wiki/indexes/**`. Source-specific
wiki notes, generated PDFs, generated HTML, execution-role records, and
`ROLE_EXECUTION_REGISTRY.csv` must be authorized by the AgentJob boundary.

If synchronization or validation fails, stage nothing, commit nothing, preserve
the working-tree evidence, and report failed commands, changed paths, active
task, active AgentJob, and the likely repair role.

## Reporting

Report the substantive research/control result first, then explain why the next
role follows from validated state. Do not reduce the final response to
orchestration mechanics.

Use APA 7 citations when DDRs, role artifacts, or handoffs cite documents or
materials. Pure registry metadata does not need APA citations.

Tracked `research_control/` state is authority. Local prompts, logs, previews,
or caches do not override tracked control files.
