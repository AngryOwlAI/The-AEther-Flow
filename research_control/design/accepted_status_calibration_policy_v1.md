<!-- authority: control -->

# Accepted Status Calibration Policy v1

## Source Basis

This policy implements v17 P3-T01. It is a project-control language policy only. It changes no physics object, no canonical science source, and no derivation status.

The policy exists because several v17 rows intentionally carry scoped positive status while also carrying hard anti-overclaim boundaries. Agents must report both facts in the correct order.

## 1. Problem Statement

Some high-risk rows are neither blank failures nor unrestricted successes. They may have accepted/scoped-positive status for a narrow control purpose, evidence precondition, source-side witness, or negative-result preservation route. The current risk is symmetric:

- Overclaim risk: treating scoped positive status as a canonical ontology change, source-law adoption, matter-coupling result, stress-energy result, Einstein-equation result, benchmark promotion, Gate Chair verdict, or completed derivation.
- Underclaim risk: treating scoped positive status as basically nothing because the hard blocks are visible.

Both errors damage the research-control record. Overclaiming corrupts scientific authority. Underclaiming hides useful, bounded progress and prevents later packets from using lawful preconditions.

## 2. Calibrated Acceptance Principle

For high-risk accepted/scoped-positive rows, every status card and short summary must state:

1. Positive status first.
2. Exact scope second.
3. Blocked overread third.

The required compression is:

> The row has a scoped positive status for X; its scope is Y; it does not imply Z.

This rule preserves the positive result without weakening hard claim boundaries.

## 3. Positive-First Status-Card Model

Renderers and agents should use a three-part status-card model:

| Field | Required content | Failure mode prevented |
| --- | --- | --- |
| Positive status | The narrow thing that was accepted, completed, preserved, certified, or made available. | Fear-based underclaiming. |
| Exact scope | The row's lawful status class, authority surface, input/output boundary, and allowed downstream use. | Ambiguous promotion. |
| Blocked overread | The stronger claim that remains blocked. | Canonical or physics overclaim. |

This model is mandatory for high-risk rows involving source objects, effective metrics, matter coupling, light-cone response, narrow model certificates, frozen-negative routes, or similar derivation-critical surfaces.

## 4. High-Risk Rows Covered

This policy covers rows that contain one or more of the following risk features:

- Source-side object or source-extension evidence that might be mistaken for canonical ontology adoption.
- Effective-metric or response data that might be mistaken for unrestricted theorem authority.
- Matter-coupling, detector-semantics, stress-energy, matter-action, or Einstein-equation language.
- Frozen-negative or scoped-obstruction routes that might be mistaken for global impossibility results.
- Any row whose public summary could compress "scoped positive" into either "solved" or "basically nothing."

The policy does not create new high-risk rows. It governs how existing and future high-risk rows must be described.

## 5. Preferred Wording Patterns

Use patterns that show the bounded positive result and its blocked overread in one unit:

- "Scoped positive for [specific control purpose]; not canonical ontology adoption."
- "Accepted as [specific evidence/precondition class]; not a source law, coupling law, or benchmark promotion."
- "Certified for [narrow model/witness family]; not unrestricted theorem authority."
- "Preserved as a frozen-negative route for [specific obstruction]; not a global no-go result."
- "Available for downstream packet selection under [named boundary]; not a Gate Chair verdict or completed derivation."

Each sentence should identify the positive status before the blocked claim. The blocked claim should be explicit rather than left for inference.

## 6. Forbidden Overclaim Patterns

The following patterns are forbidden unless a separate, tracked, human-gated authority record explicitly authorizes the stronger claim:

- Canonical-ontology adoption claim.
- Source-law adoption claim.
- `RR_E` transport-completeness or invariance-law adoption claim.
- Unrestricted `RR_E` theorem-authority claim.
- Matter-semantics adoption claim.
- Detector-semantics adoption claim.
- Coupling-law adoption claim.
- Matter-coupling derivation claim.
- Matter-coupling adoption claim.
- Stress-energy semantics establishment claim.
- Stress-energy tensor construction claim.
- Matter-action derivation claim.
- Einstein-equation derivation claim.
- Benchmark-promotion claim.
- Gate Chair approval claim.
- Completed-derivation claim.
- Future source-extension impossibility claim.

Equivalent phrasings are also forbidden when they carry the same stronger claim.

## 7. Forbidden Underclaim Patterns

The following patterns are forbidden because they erase bounded progress:

- "Scoped adoption/evidence/precondition is basically nothing."
- "Accepted/scoped-positive status does not matter because promotion is blocked."
- "The row is only a non-result."
- "There is no usable downstream status."
- "All hard-blocked rows are equivalent to failures."
- "A frozen-negative route means the project learned nothing."

If a row has accepted/scoped-positive status, agents must report that status before listing blocked overreads.

## 8. Public-Summary Compression Rule

Public or front-door summaries may be shorter than control records, but they must not invert the status-card order. The minimum public-safe sentence is:

> Scoped positive for [X] within [Y]; not [Z].

If there is not enough space to include all three elements, the summary must link to or name the full control record rather than compressing away scope or blocked overread.

## 9. Full-Control Non-Conclusion Rule

A full control record may include negative, obstructed, frozen, or blocked conclusions, but it must not turn scoped status into a program-wide conclusion. In particular:

- A blocked adoption decision is not a proof that future source-extension is impossible.
- A frozen-negative route is not a global rejection of the research program.
- A scoped positive result is not a completed derivation.
- A policy-language calibration is not physics evidence.

When uncertainty remains, the record must name the uncertainty and route the next bounded packet.

## 10. Renderer and Linter Implementation Requirements

Future renderer and linter work must implement this policy through machine-readable fields or equivalent deterministic checks. The minimum fields are:

- `positive_status`
- `exact_scope`
- `blocked_overread`
- `evidence_source`
- `no_physics_delta`

Required linter behavior:

- Flag high-risk rows that contain a positive status but omit exact scope.
- Flag high-risk rows that contain exact scope but omit the blocked overread.
- Flag summaries that lead with blocked overread and bury or omit the positive status.
- Flag "basically nothing" underclaim language when the row has accepted/scoped-positive status.
- Flag overclaim language that implies ontology adoption, source-law adoption, coupling-law adoption, matter coupling, stress-energy, matter action, Einstein equations, benchmark promotion, Gate Chair verdict, completed derivation, or future source-extension impossibility.

The linter may allow short public summaries only when they preserve the positive-first, exact-scope, blocked-overread sequence.

## 11. Examples

| Surface | Preferred calibrated statement | Forbidden compression |
| --- | --- | --- |
| `M_src` | `M_src` has scoped positive source-object evidence/precondition status for the named packet; it is not canonical ontology adoption or a source-law adoption. | "`M_src` is adopted" or "`M_src` is basically nothing." |
| `g_eff` | `g_eff` is available as scoped effective-metric response evidence under the recorded witness boundary; it is not unrestricted theorem authority, benchmark promotion, or Einstein-equation derivation. | "`g_eff` proves GR" or "`g_eff` does not count." |
| `matter_coupling` | The row has scoped positive control status for selecting or preparing a matter-coupling packet; it is not matter-coupling derivation, adoption, stress-energy semantics, stress-energy tensor construction, or matter-action derivation. | "Matter coupling is solved" or "the packet is only blocked." |
| `Resp_lc` | `Resp_lc` has scoped light-cone response status for the named finite/witness regime; it is not detector-semantics adoption or unrestricted response theorem authority. | "`Resp_lc` adopts detector semantics" or "`Resp_lc` means nothing." |
| `NarrowMSCertEq_v1` | `NarrowMSCertEq_v1` is certified only for the named narrow model and equation-class boundary; it is not a general matter-source certificate or Einstein-equation result. | "Matter sources are certified" or "the certificate is useless." |
| Frozen-negative routes | The route preserves a scoped obstruction or negative result for future routing; it is not a global no-go theorem and not evidence that future source-extension is impossible. | "The project is disproved" or "nothing was learned." |

## 12. No-Physics-Delta Boundary

This policy changes reporting language only. It does not modify canonical physics sources, formal definitions, source-side laws, ontology, metric claims, coupling claims, matter semantics, detector semantics, stress-energy semantics, matter action, Einstein-equation claims, exact-GR benchmark status, or Gate Chair authority.

## References

The AEther-Flow Research Project. (2026). *Current research-control frontier* [Research-control report]. `research_control/current_frontier.md`.

The AEther-Flow Research Project. (2026). *Handoff 0626* [Research-control handoff]. `research_control/handoffs/handoff-0626.yaml`.

The AEther-Flow Research Project. (2026). *Recommendations implementation plan continue task v17* [Project-control plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.
