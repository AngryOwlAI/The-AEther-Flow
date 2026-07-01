<!-- authority: control -->

# High-Risk Selector Checklist

## Purpose

This control note implements v13 P3-T02. It defines the required checklist for
high-risk selectors that operate after a matter-coupling-chain construction,
source-purity audit, Refuter stress result, or scoped Gate Chair evidence or
precondition decision.

The checklist prevents a local success from being overread as adoption,
derivation, benchmark promotion, or completed derivation. It also forces the
selector to state why any stronger downstream route remains blocked or why an
exact protected authority would allow it.

## Authority Status

This note is project-control guidance only. It is not a physics theorem, not a
source-law adoption, not a role-schema change, and not Gate Chair authority.

It does not alter canonical ontology, the Distance-to-GR ledger, role
permissions, validator semantics, source-law status, `MetricData(E)` status,
`g_eff` status, coupling-law status, matter-semantics status,
detector-semantics status, matter-coupling status, stress-energy status,
Einstein-equation status, benchmark status, or completed-derivation status.

## Scope

A selector is high-risk when it can be read by a future agent as authorizing a
move from source-side or scoped evidence into any of these protected claims:

- canonical ontology edit;
- source-law adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` adoption as law;
- source-extension data adoption beyond the exact scoped gate result;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- coupling-law adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor, or matter action;
- Einstein equations;
- benchmark promotion or benchmark Gate Chair closure;
- completed derivation;
- future source-extension impossibility; or
- global theory rejection.

## Required Checklist

Every high-risk selector output must answer each item below in its task-local
decision artifact or completion receipt.

| Item | Required question | Required answer discipline |
| --- | --- | --- |
| 1 | What exact object was just constructed, audited, stressed, or gated? | Name the object, source path, task, and result class. Do not summarize it as a stronger downstream object. |
| 2 | Is it adopted, accepted as evidence/precondition, proposal-only, or rejected? | Use the narrowest applicable status vocabulary. Allowed terms include `adopted`, `accepted_as_evidence_precondition`, `proposal-only`, `rejected`, `draft/control`, `source-extension data`, and `human-gated`. |
| 3 | Which source laws remain missing? | List missing source-side laws, selectors, transition rules, robustness rules, semantics laws, or adoption laws. If none are missing, cite the exact source and authority. |
| 4 | Which target imports are forbidden? | List forbidden target imports, including detector protocol, empirical calibration, stress-energy tensor, matter action, target metric, benchmark fit, and Einstein equations when applicable. |
| 5 | Which downstream routes are blocked? | Name each blocked downstream route explicitly, not only a generic "promotion blocked" phrase. |
| 6 | Why is the selected route the lowest-authority next route? | Explain why the next route can be executed without adopting a stronger claim or invoking protected authority. |
| 7 | Does freeze evaluation apply? | State whether repeated-burden or scoped-obstruction freeze evaluation applies, and record the result. |
| 8 | Is human gate authority required? | State whether protected Gate Chair or ontology authority is required. If required, name the exact gate scope; if not, explain why the route is still non-promotional. |
| 9 | Does this route add a new mathematical payload? | Answer yes or no. If yes, name the payload and source path. If no, state that the packet is control-only, support-only, or receipt-only. |
| 10 | Does the route repeat the same burden without new payload? | Answer yes or no and state the consequence for continuation, freeze review, or route change. |

## Selector Output Fields

High-risk selector artifacts should include a block equivalent to:

```yaml
selector_checklist:
  version: "v13_p3_t02"
  high_risk_selector: true
  exact_object: ""
  prior_result_type: ""
  status_classification: ""
  missing_source_laws: []
  forbidden_target_imports: []
  blocked_downstream_routes: []
  selected_lowest_authority_route: ""
  freeze_evaluation:
    applies: false
    result: ""
  human_gate_authority:
    required: false
    scope: ""
  new_mathematical_payload:
    present: false
    payloads: []
  repeated_burden_without_new_payload:
    present: false
    consequence: ""
  forbidden_overreads: []
  next_packet: ""
```

The exact serialization may vary by role, but the information must be present
and reviewable in tracked task-local records.

## Stronger-Route Rule

A high-risk selector may name a stronger downstream route only when one of the
following is true:

1. the tracked source artifact already establishes the prerequisite at the
   required authority level;
2. a protected Gate Chair decision explicitly grants the exact scoped authority;
3. the selector routes to a human-gated decision without treating the gate as
   already decided; or
4. the route remains a bounded source-side draft/control or audit packet that
   preserves all downstream blocks.

Absent one of those conditions, the selector must choose the lowest-authority
next route: another bounded construction, source-purity audit, Refuter stress,
dependency map, route template, boundary update, or human-gate request.

## No Schema Change

This note does not edit role contracts or registry schemas. It adds a
registered control-source checklist. Validation is therefore supplied by the
existing research-control validator, documentation-impact validator,
current-frontier renderer, dependency-graph freshness check, and memory
bootstrap.

## Forbidden Readings

This checklist must not be read as:

- source-law adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` adoption as law;
- source-extension data adoption beyond exact scoped gate result;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- coupling-law adoption;
- matter-semantics or detector-semantics adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor, or matter action;
- Einstein equations;
- benchmark promotion or benchmark Gate Chair closure;
- completed derivation;
- future source-extension impossibility;
- global theory rejection; or
- proof authority created by registry rows, validators, generated artifacts,
  commits, roles, handoffs, or local caches.

## Next Controlled Route

After this checklist is registered, the v13 sequence routes to P3-T03:
post-stress route template creation. That route should convert this checklist
and the no-leap route rule into reusable selector-template structure without
promoting physics claims.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v13* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 1). *No-leap route rule*
[Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Handoff 0420* [Internal
research-control handoff].
