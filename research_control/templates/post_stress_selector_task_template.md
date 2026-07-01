---
authority: control
template_id: "post_stress_selector_task_template_v1"
status: "active"
created_at: "2026-07-01T08:18:00Z"
related_plan: "recommendations_implementation_plan_continue_task-v13 P3-T03"
---

# Post-Stress Selector Task Template

## Purpose

Use this template when a completed construction, audit, stress, or scoped gate
artifact needs a selector task that names the lowest-authority lawful next
route. The template is a project-control scaffold only. It does not select a
route by itself and does not create physics claim authority.

## Required Inputs

### Stress input artifact

- `stress_artifact_path`: path to the completed stress artifact, if applicable.
- `stress_verdict`: pass, fail, scoped survival, obstruction, or not applicable.
- `stress_scope`: exact scope tested.
- `stress_limits`: unresolved cases, assumptions, or invalid regimes.

### Audit input artifact

- `audit_artifact_path`: path to the completed audit artifact, if applicable.
- `audit_verdict`: pass, fail, scoped pass, smuggling risk, or not applicable.
- `audit_scope`: exact source-purity or claim-boundary scope audited.
- `audit_limits`: remaining forbidden imports or unresolved audit questions.

### Construction input artifact

- `construction_artifact_path`: path to the completed construction artifact.
- `construction_status`: draft/control, proposal-only, source-extension data,
  accepted scoped evidence/precondition, rejected, or not applicable.
- `constructed_object`: exact object name.
- `construction_limits`: missing hypotheses, unsupported promotions, or
  downstream gaps.

## Exact Object Under Classification

Record the single object being classified. Do not classify a family, route, or
project milestone unless that is the exact object emitted by the upstream
artifact.

- `object_name`:
- `object_type`:
- `object_source_path`:
- `object_status_before_selector`:
- `protected_terms_used`:

## Available Route Options

List only routes that are lawful under the current handoff, role contract,
claim boundaries, and Distance-to-GR burden map. Each available route requires
an authority basis.

| Route option | Authority basis | Required role | Required gate | Why available |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Rejected Route Options

Rejected route options must name the exact missing authority, missing source
law, missing datum, missing gate, or forbidden target import.

| Rejected route | Rejection reason | Missing authority or datum | Protected claim blocked |
| --- | --- | --- | --- |
|  |  |  |  |

## Freeze Criteria

Evaluate whether the route repeats the same burden without new mathematical
payload, reaches a scoped obstruction, or requires human-gated ontology
authority.

- `same_burden_repetition_count`:
- `new_mathematical_payload_present`:
- `scoped_obstruction_present`:
- `human_gate_required`:
- `freeze_decision`: not_frozen, freeze_route, or human_gate_required.
- `freeze_rationale`:

## Distance-to-GR Delta

State whether the selector changes any Distance-to-GR row. The default for a
post-stress selector is no status delta unless a separate protected authority
has already authorized the change.

- `milestone`:
- `burden_id`:
- `ledger_row_updated`: false
- `status_delta`: unchanged unless separately authorized.
- `downstream_unlocked`:
- `downstream_still_blocked`:

## Forbidden Conclusions

The selector must not infer any of the following from construction, audit,
stress survival, or scoped gate success alone:

- canonical ontology edit
- source-law adoption
- source-extension data adoption beyond the exact scoped gate result
- `MetricData(E)` adoption
- `g_eff` adoption or scope expansion
- coupling-law adoption
- matter-semantics adoption
- detector-semantics adoption
- matter-coupling derivation or adoption
- stress-energy semantics
- stress-energy tensor
- matter action
- Einstein equations
- benchmark promotion
- benchmark Gate Chair closure
- completed derivation
- future source-extension impossibility
- global theory rejection
- generated derivative or validator result as proof authority

## Handoff Text

Use this pattern in the handoff after a selector packet completes:

```text
Run one bounded [next-route] packet for [exact object] before any
[blocked downstream routes]. This selector records [selected route] as the
lowest-authority next step because [authority basis]. It does not authorize
[forbidden conclusions].
```

## Validation Checklist

- The stress input artifact is named or explicitly marked not applicable.
- The audit input artifact is named or explicitly marked not applicable.
- The construction input artifact is named or explicitly marked not applicable.
- The exact object under classification is singular and source-backed.
- Available route options each cite an authority basis.
- Rejected route options each cite a missing authority, missing datum, missing
  source law, missing gate, or forbidden target import.
- Freeze criteria are evaluated.
- Distance-to-GR delta is stated.
- Forbidden conclusions are listed in the completion receipt.
- Handoff text names exactly one bounded next packet.
- No protected downstream conclusion is promoted by selector wording.
- Generated outputs are treated as navigational support, not proof authority.

## Source Notes

This template operationalizes the v13 P3-T03 requirement and incorporates the
P3-T01 no-leap rule and P3-T02 high-risk selector checklist. It is reusable
scaffolding. Active authority comes only from completed task-local records,
registered rows, validators, and human gates where required.

## References

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v13* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 1). *No-leap route rule*
[Internal control note].

The AEther-Flow Research Project. (2026, July 1). *High-risk selector
checklist* [Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Handoff 0421* [Internal
research-control handoff].
