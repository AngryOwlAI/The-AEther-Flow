<!-- authority: control -->

# P2-T03 Renderer Source Inventory

## Packet

- Task: `RT-20260701-034`
- AgentJob: `AJ-RT-20260701-034-001`
- Plan task: v14 `P2-T03`
- Packet type: `current_frontier_wording_update_control_packet`

## Inspected Sources

| Source | Role in packet | Finding |
| --- | --- | --- |
| `research_control/handoffs/handoff-0442.yaml` | Routing authority | Selects one bounded P2-T03 current-frontier wording pilot. |
| `implementations_plans/recommendations_implementation_plan_continue_task-v14.md` | Plan context | Requires renderer/source inspection, source-level update, regeneration, and check. |
| `scripts/research_control/render_current_frontier.py` | Renderer source | Wording was rendered from ledger fields and handoff/task state; alias-map loading was absent. |
| `research_control/design/distance_to_gr_status_aliases.yaml` | Alias source | Contains required high-risk burden aliases and `matter_coupling` object aliases, previously marked deferred to P2-T03. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | Burden-state authority | Retains raw `current_status` and layered fields; the ledger remains authority. |
| `scripts/research_control/validate_research_control.py` | Current-frontier guard | Its sync check compared the raw ledger status against the rendered table, requiring compatibility with a new `Legacy status` column. |
| `tests/test_render_current_frontier.py` | Focused renderer test | Updated to cover status-alias integration and reader-facing status rendering. |

## Determination

The correct source-level change is renderer integration, not hand editing
`research_control/current_frontier.md` and not changing the Distance-to-GR
ledger. The renderer now loads `distance_to_gr_status_aliases.yaml` as
subordinate display data, renders a `Reader-facing status` column, preserves
raw ledger `current_status` as `Legacy status`, and adds an alias pilot section
with high-risk burden and object-specific aliases.

The current-frontier sync validator now compares the authoritative ledger
`current_status` against `Legacy status`, falling back to the older
`Current status` column for backward compatibility.
