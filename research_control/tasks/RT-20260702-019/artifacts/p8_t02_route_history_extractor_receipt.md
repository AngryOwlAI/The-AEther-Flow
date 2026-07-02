<!-- authority: control -->

# P8-T02 Route-History Extractor Receipt

Generated at: `2026-07-02T06:29:55Z`

## Verdict

PASS. `extract_route_history.py` emits `route_signature_definition_v1`
signatures from tracked task, AgentJob, completion, and registry records. The
extractor is project-control tooling only. It does not add route-orbit hard
gates, freeze routes, or change physics claim authority.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `scripts/research_control/extract_route_history.py` | `266ccb62bda4eb27b8411e011e640aead31c34c0b57d91967d72fa33f6459ab3` |
| `tests/test_route_history_extractor.py` | `aa4371db52b80ec7774e668701b58325cb4c58c2fa8bfbfb8f4b80ab75cb24f6` |
| `research_control/tasks/RT-20260702-019/artifacts/p8_t02_route_history_sample.json` | `f299c9bafc576982192e38f6fe7c810745ef659119ef417ce8c6e38bd17d8fb1` |
| `implementations_plans/recommendations_implementation_plan_continue_task-v14.md` | `6687d47a0cfd03a2be28e8e92a58185685347cb9e34a8835a20de22d81992aec` |
| `research_control/design/route_signature_definition.md` | `cd7431c0c4986533a530e6a913a34ef6f6e09a77670f070ea85833951a871f79` |
| `research_control/current_frontier.md` | `8d1b0cbe36e8ff4a4e3bda29cdb5ed38021971f68fe9b1e1df12a037460cd610` |

## Sample Coverage

- Sample mode: `recent-matter-rr-e`
- Signature count: `22`
- `RT-20260701-030` Gate Chair state:
  `scoped_evidence_or_precondition_accepted`
- `RT-20260701-031` boundary synchronization state: `synchronized`
- P8-T01 extracted signature hash: `6da330470009cffcf5afcd76bcfd3d7ef5489f5c270e9e1b3671366e2fa1f368`

## Boundary

The extractor preserves raw source-evidence paths for non-default fields and
emits `unknown`, `none`, or `not_applicable` when tracked evidence does not
support a stronger normalized value. It is not a physics source, not a Gate
Chair verdict, not route-freeze authority, and not proof authority.

## Next Route

P8-T03 may implement route-orbit validator warnings or hard-fail conditions
against these extracted signatures. That validator remains a separate bounded
packet.
