<!-- authority: control -->

# P2-T02 Renderer Integration Note

## Decision

Renderer integration is deferred to P2-T03.

## Reasoning

P2-T02 requires either renderer integration notes or a deferred integration
handoff. The current renderer, `scripts/research_control/render_current_frontier.py`,
reads tracked state directly from:

- `research_control/program_state.yaml`
- the latest handoff named by program state
- the active task record
- `registries/DISTANCE_TO_GR_LEDGER.csv`

Changing renderer behavior in the same packet would merge P2-T02 alias data
creation with P2-T03 current-frontier wording-pilot work. The smaller correct
packet is to create `research_control/design/distance_to_gr_status_aliases.yaml`
and route the renderer consumption decision to P2-T03.

## P2-T03 Handoff Requirements

The next packet must inspect the renderer and decide whether to:

1. Load `research_control/design/distance_to_gr_status_aliases.yaml`.
2. Derive equivalent scoped-positive display strings from ledger layered
   fields.
3. Preserve the alias map as a contract source while keeping the renderer
   ledger-only.

Any renderer change must preserve ledger authority and must still display
layered status fields for high-risk rows.

## Non-Authority

This note does not change renderer behavior. It does not change physics
status, ledger status, route authority, source-law status, or benchmark
status.
