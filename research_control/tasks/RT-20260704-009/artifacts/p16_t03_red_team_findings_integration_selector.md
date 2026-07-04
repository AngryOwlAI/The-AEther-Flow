<!-- authority: control -->

# P16-T03 Red-Team Findings Integration Selector

Task: `RT-20260704-009`

Role: `project-control-maintainer@0.2.0`

Selected route: `no-op with evidence`

Proof authority: false

Physics promotion authorized: false

## Scope

This selector handles the P16-T02 internal red-team pilot findings. It selects exactly one route from the P16-T03 candidate list and does not implement a theorem repair, source-extension audit, route freeze, public documentation update, validator update, or external outreach packet.

## Candidate Route Review

| Candidate route | Decision | Reason |
| --- | --- | --- |
| theorem repair | not selected | P16-T02 found known certificate-gap and burden issues but no new theorem defect requiring immediate repair. |
| claim-language remediation | not selected | The changed-path claim-language lint passes with historical/provenance warnings only. No new unguarded promotion wording was introduced by P16-T02. |
| source-extension audit | not selected | The reviewed source-extension classification checklist already enforces fail-closed status discipline for missing or ambiguous classification. |
| route freeze | not selected | P16-T02 did not establish a repeated-burden freeze condition or global obstruction. |
| public docs update | not selected | Public status safety is already represented by the exists / does-not-exist source spec; no new user-facing text delta was required. |
| validator update | not selected | P16-T02 found a copy-risk hazard, not a deterministic validator gap requiring code changes before P17. |
| external human outreach packet | not selected | P16 remains advisory-only; no reviewer contact is authorized or needed before P17. |
| no-op with evidence | selected | The vulnerabilities are known, scoped, and already represented in tracked control surfaces. The correct action is to preserve the evidence and proceed to the negative-result publication track. |

## Selection Rationale

The P16-T02 red-team report identifies serious scientific vulnerabilities: explicit valid certificates remain required, matter-coupling downstream burdens remain blocked, source-extension evidence is not derivation support, and the proof-assistant pilot is narrow support only. It also identifies process vulnerabilities around overreading templates, graphs, public summaries, and formalization pilots.

These findings do not require a new repair packet before P17 because they do not expose a new contradiction, a new unguarded promotion, a missing deterministic validator hook, or a public documentation defect in the changed P16 surfaces. The project already has control surfaces that state the relevant blocks and overread guards.

## Stronger Adoption Status

Stronger adoption remains blocked. The selected `no-op with evidence` route does not waive red-team issues and does not convert vulnerabilities into accepted proof status.

Blocked targets remain:

- source-law adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- stress-energy semantics;
- matter action;
- Einstein equations;
- benchmark promotion;
- Gate Chair verdict;
- completed derivation.

## Done Criteria Receipt

Exactly one next route selected: `PASS`

Stronger adoption remains blocked: `PASS`

No physics promotion: `PASS`

Next route: one bounded P17-T01 negative-result inventory packet.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan continue task v15* [Implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *P16-T02 internal red-team pilot report v15* [Research-control report]. `research_control/tasks/RT-20260704-008/artifacts/internal_red_team_pilot_report_v15.md`.

The AEther-Flow Research Project. (2026c). *Source extension classification checklist v1* [Control checklist]. `research_control/design/source_extension_classification_checklist_v1.md`.

The AEther-Flow Research Project. (2026d). *Public status exists / does-not-exist source spec* [Control source spec]. `research_control/design/public_status_exists_does_not_exist_source_spec.md`.
