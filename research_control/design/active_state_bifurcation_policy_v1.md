<!-- authority: control -->

# Active-State Bifurcation Policy v1

```yaml
schema_id: active_state_bifurcation_policy_v1
authority_status: project_control
source_plan: implementations_plans/recommendations_implementation_plan_continue_task-v18.md
plan_task_id: P1-T01
recommendation_ids:
  - V18-R08
created_at: 2026-07-07T07:22:18Z
physics_delta_allowed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose

This policy defines how active-state surfaces distinguish the ordinary research
handoff from project-system sidecars.

The policy resolves the ambiguity targeted by v18 recommendation `V18-R08`:
a project-system repair, validator update, documentation-impact receipt, or
project-improvement sidecar can be newer than the latest ordinary research
handoff without becoming the scientific next-route authority.

## Definitions

### Research Handoff

A research handoff is the tracked continuation handoff under
`research_control/handoffs/` that records the latest ordinary research
continuation authority, including the selected next route, claim boundary, and
handoff summary.

For ordinary continuation, the latest research handoff is the source local
agents should inspect to determine the next scientific or research-control
packet.

### Project-System Sidecar

A project-system sidecar is a tracked project-system repair, validator,
documentation, renderer, workflow, or sidecar handoff whose purpose is to keep
the project machinery reliable.

Project-system sidecars may repair validation infrastructure, clarify
documentation, or preserve project-improvement signals. They do not supersede
the latest research handoff as scientific next-route authority unless an
explicit tracked Director decision states that such supersession is intended
for active-state routing.

### Compatibility Pointer

Existing scripts use compact pointers such as `latest_handoff_id` in
`research_control/program_state.yaml` and rendered frontier surfaces.

Those compatibility fields remain valid for legacy consumers, but they are not
sufficient by themselves to infer scientific next-route authority once
sidecar-specific fields exist.

## Authority Rules

1. The scientific next route is decided by the latest research handoff, its
   associated Director decision, and the tracked registry rows for that
   research-control transaction.
2. A project-system sidecar may appear later in time than the latest research
   handoff. Recency alone does not make the sidecar scientific authority.
3. A sidecar may supersede active research state only when all of these are
   true:
   - a tracked Director decision explicitly authorizes active-state
     supersession;
   - the sidecar states the scope of supersession;
   - the sidecar preserves the relevant latest research handoff as historical
     context;
   - the sidecar does not claim physics promotion, proof completion, ontology
     adoption, benchmark promotion, or Einstein-equation authority unless a
     separate human Gate Chair action explicitly authorizes such a scientific
     promotion.
4. If there is no explicit supersession decision, sidecars are rendered as
   project-system status and the next research route remains sourced from the
   latest research handoff.

## Rendering Contract for P1-T02

Renderer updates should preserve existing compatibility fields and add a
dedicated bifurcation object.

```yaml
active_state_bifurcation:
  latest_research_task_id: string
  latest_research_handoff_id: string
  latest_project_system_sidecar_task_id: string | null
  latest_project_system_sidecar_status: string | null
  sidecar_supersedes_research_handoff: false
  next_research_route_source: "latest_research_handoff"
compatibility:
  latest_handoff_id: string
  latest_handoff_id_semantics: "compatibility pointer; inspect active_state_bifurcation before inferring scientific next-route authority"
```

### Field Semantics

`latest_research_task_id` identifies the task that produced the current
ordinary research handoff.

`latest_research_handoff_id` identifies the handoff governing ordinary
research continuation.

`latest_project_system_sidecar_task_id` identifies the latest project-system
sidecar task, if one is active or more recent than the latest research handoff.

`latest_project_system_sidecar_status` summarizes the sidecar status without
converting it into scientific authority.

`sidecar_supersedes_research_handoff` defaults to `false`. It may be `true`
only under the explicit supersession rule above.

`next_research_route_source` identifies the tracked source that should be used
to select the next ordinary research packet. Under normal operation it is
`latest_research_handoff`.

## Blocking Rules

Continuation should be blocked or routed to validation repair when any of the
following conditions is detected:

1. The latest research task, latest research handoff, and registry rows disagree
   about the active next route.
2. A project-system sidecar claims physics promotion, ontology adoption,
   benchmark promotion, completed derivation, or proof authority without an
   explicit human Gate Chair authorization.
3. Rendered frontier surfaces show a sidecar as the scientific next-route
   authority without an explicit supersession decision.
4. The bifurcation fields disagree across current-frontier, compact-frontier,
   and task-index renderers after the P1-T02 renderer update.
5. A project-improvement sidecar is emitted but not linked back to the research
   handoff that produced the project-improvement signal.
6. Required validators fail in a way that could hide or misclassify active
   research state.

Nonblocking project-system sidecars may continue to report validation,
documentation, renderer, or tooling status while leaving the scientific route
unchanged.

## Current-State Example

At creation time for this policy, `handoff-0676` was the latest ordinary
research handoff produced by `RT-20260707-007`. It selected the next v18 route,
`P1-T01`.

Earlier project-system work such as documentation-impact or validation-sidecar
transactions may remain important project evidence. They are not scientific
next-route authority unless a tracked Director decision explicitly says so.

For this state, a P1-T02 renderer may report no active project-system sidecar:

```yaml
active_state_bifurcation:
  latest_research_task_id: RT-20260707-008
  latest_research_handoff_id: handoff-0677
  latest_project_system_sidecar_task_id: null
  latest_project_system_sidecar_status: null
  sidecar_supersedes_research_handoff: false
  next_research_route_source: latest_research_handoff
```

## P1-T03 Validation Hooks

The follow-on validator packet should test at least these cases:

1. A later project-system sidecar does not supersede the latest research
   handoff when no explicit supersession decision exists.
2. A sidecar claiming physics promotion fails claim-language validation unless
   separately authorized by a human Gate Chair decision.
3. A new ordinary research handoff may supersede a prior ordinary research
   handoff through normal continuation.
4. Rendered bifurcation fields remain synchronized across all active-state
   renderers.

## Source Materials

The Aether-Flow Research Project. (2026). *Recommendation implementation plan:
continue task v18*.

The Aether-Flow Research Project. (2026). *v18 recommendation backlog schema*.

The Aether-Flow Research Project. (2026). *AGENTS.md root project guidance*.
