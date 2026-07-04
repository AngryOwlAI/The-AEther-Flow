<!-- authority: science_draft -->

# Matter-Coupling DAG Next-Edge Selector v16

## Active State Summary

| Field | Value |
| --- | --- |
| Task | `RT-20260704-020` |
| Job | `AJ-RT-20260704-020-001` |
| Role | `theoretical-continuation-selector@0.1.0` |
| Plan | `recommendations_implementation_plan_continue_task-v16.md` |
| Target milestone | `matter_coupling` |
| Selector status | draft/control route decision only |

This artifact executes the selector route selected by `handoff-0565`. It does
not execute a theorem proof and does not promote any physics claim.

## DAG Source Inspection

The populated DAG at
`research_control/design/matter_coupling_dependency_dag_v1.md` contains the
required matter-coupling nodes, blocked-node burden summaries, and candidate
edges. Its own authority boundary states that it is navigational project-control
support only.

## Candidate Edge List

The selector scored the required v16 P2 candidate set. The strongest candidate
under live evidence is:

`mc_source_matter_semantics_equivalence_theorem -> mc_coupling_law_target`

This edge is close to existing certificate machinery and can produce a bounded
target-specification payload without claiming a coupling-law adoption.

## Scoring Matrix

The scoring matrix is recorded in
`matter_coupling_dag_next_edge_scoring_rubric_v16.md`.

## Selected Edge

```text
mc_source_matter_semantics_equivalence_theorem -> mc_coupling_law_target
```

## Selected Theorem-Route Family

```text
source_side_coupling_law_target_specification_under_explicit_certificates
```

## Selected Next Role Family

```text
ontology-formalizer@0.2.0
```

## Required Mathematical Payload For Selected Next Task

The next packet must define a source-side coupling-law target specification
that includes:

- domain and codomain placeholders for a future source-side coupling-law
  candidate;
- explicit source-certificate preconditions;
- fail-closed branches for missing, malformed, target-importing, or
  detector-semantic certificates;
- a statement of what future theorem or witness would be needed;
- a no-adoption status block for coupling law and matter coupling.

## Required Refuter Stress Route After Selected Task

After the target specification packet, the downstream route should include a
bounded Refuter stress packet against:

- target metric import;
- detector-semantics collapse;
- evidence-as-adoption overread;
- coupling-law adoption laundering;
- stress-energy or matter-action import;
- Einstein-equation import;
- benchmark or completed-derivation overread.

## Formalization Route

Support-only formalization may later encode the target-specification schema and
negative fixtures. Such support tooling must remain non-authoritative.

## Forbidden Conclusions

This selector does not authorize:

- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem authority;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor construction;
- matter action;
- Einstein equations;
- benchmark promotion;
- completed derivation;
- future source-extension impossibility or program-wide rejection.

## Distance-To-GR Effect

No Distance-to-GR ledger row changes. The matter-coupling burden remains
accepted only as scoped source-extension evidence/precondition, with physical
matter coupling not derived and not adopted.

## Exact Handoff

Run one bounded `ontology-formalizer@0.2.0` packet:

```yaml
route_id: "source_side_coupling_law_target_specification_under_explicit_certificates"
target_derivation_milestone: "matter_coupling"
requires_human_gate: false
```

The packet should specify the future coupling-law target. It must not adopt a
coupling law or derive matter coupling.

## Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v16* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v16.md`.

The AEther-Flow Research Project. (2026b). *Matter-coupling dependency DAG v1*
[Internal control artifact].
`research_control/design/matter_coupling_dependency_dag_v1.md`.

The AEther-Flow Research Project. (2026c). *Current frontier* [Internal control
report]. `research_control/current_frontier.md`.
