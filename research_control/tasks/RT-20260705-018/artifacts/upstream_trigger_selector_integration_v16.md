<!-- authority: control -->

# Upstream Trigger Selector Integration v16

## Purpose

This artifact integrates the P9-T01 `EqSrc`, `RetainH`, and `GenH` trigger list
into future selector packets, theorem-setup packets, and DAG edge ranking.

The integration is routing guidance only. It does not discharge `EqSrc`, adopt
`RetainH`, adopt `GenH`, adopt source laws, derive matter coupling, promote a
benchmark, issue a Gate Chair verdict, or complete the derivation.

## Source Basis

- P9-T01 trigger list:
  `research_control/design/eqsrc_retainh_genh_trigger_list_v16.md`.
- P2 scoring dimension:
  `dependency_on_missing_eqsrc_retainh_genh`.
- Current frontier route:
  `Run one bounded P9-T02 upstream trigger selector integration packet.`

## Selector Integration Rule

Every future selector packet that ranks a matter-coupling theorem or
construction edge must include an `upstream_primitive_trigger_status` block
before it selects the route.

The selector must evaluate the selected edge against the P9-T01 trigger rules:

1. `EqSrc` is triggered only when the packet removes explicit certificate
   premises, seeks family-wide source equivalence, needs equivalence across
   arbitrary source-family variation, or claims certificate equivalence
   independent of certificate records.
2. `RetainH` is triggered only when the packet preserves certificate structure
   or source semantics under `H`, claims stability under an `H`-indexed
   operation, or needs retention to sustain matter-sector continuity.
3. `GenH` is triggered only when the packet constructs or enumerates an
   `H`-indexed generated family, requires generator closure, or uses generated
   family structure as theorem input.

If no trigger rule fires, the selector must keep the upstream primitive
horizon-only and continue ranking the ordinary selected theorem edge.

## DAG Ranking Integration

The P2 scoring rubric already contains
`dependency_on_missing_eqsrc_retainh_genh`. Future selectors must interpret
that score as follows:

| Trigger status | Ranking effect | Required selector action |
| --- | --- | --- |
| none triggered | Low dependency penalty. Continue ordinary edge ranking. | Record non-trigger reasons for all three primitives. |
| exactly one triggered | High dependency penalty unless that primitive is the packet objective. | Route exactly one bounded upstream primitive packet or explain why the selected edge is deferred. |
| multiple triggered | Very high dependency penalty. | Prefer a narrower edge, split the primitive work, or issue a bounded selector decision explaining the dependency order. |
| trigger evidence ambiguous | Treat as not selected yet. | Route one bounded selector clarification packet, not a physics promotion. |

The score is route-selection evidence only. It is not a proof, not a source-law
adoption, and not a Distance-to-GR burden discharge.

## Theorem-Setup Integration Rule

Every future theorem-setup packet that touches matter-coupling dependencies
must state whether the selected theorem requires `EqSrc`, `RetainH`, or `GenH`.

The setup record must include:

- selected theorem or construction edge;
- explicit certificate premises retained or removed;
- whether family-wide source variation is used;
- whether any `H`-indexed retention or generator claim is used;
- non-trigger or trigger reason for each primitive;
- downstream claim blocks.

If a setup packet triggers an upstream primitive, it must route the primitive
as a bounded next packet rather than silently importing it as an assumption.

## Required Completion Fragment

Future selector and theorem-setup completions must include this block:

```yaml
upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: "explicit certificate records retained; no record-independent equivalence claim"
  RetainH:
    triggered: false
    reason: "no H-indexed retention claim"
  GenH:
    triggered: false
    reason: "no generated-family closure or theorem-input claim"
```

When a primitive is triggered, the `reason` field must cite the exact P9-T01
trigger rule and the source artifact section that makes the primitive
necessary.

## Current P9-T02 Trigger Evaluation

The present packet does not trigger an upstream primitive route:

```yaml
upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: "P9-T02 integrates selector guidance only; it does not remove explicit certificate premises or claim record-independent equivalence."
  RetainH:
    triggered: false
    reason: "P9-T02 integrates selector guidance only; it does not claim H-indexed retention or matter-sector continuity under H."
  GenH:
    triggered: false
    reason: "P9-T02 integrates selector guidance only; it does not construct a generated H-indexed source family or require generator closure."
```

## Forbidden Overread

The following readings are blocked:

- selector integration as proof of `EqSrc`;
- trigger-status recording as `RetainH` or `GenH` adoption;
- a low dependency score as a theorem that upstream primitives are unnecessary
  forever;
- a high dependency score as a no-go theorem;
- generated derivatives, validators, handoffs, or commits as physics evidence;
- human authorization for project-control execution as downstream matter
  coupling, benchmark, or completed-derivation authority.

## Distance-to-GR Effect

This artifact changes routing discipline only. It does not update the
Distance-to-GR ledger, discharge a burden, create a source law, adopt an
upstream primitive, or promote any downstream physics claim.

## Handoff

The next bounded packet is P10-T01:

```yaml
route_id: "source_model_zoo_schema_v16"
role_family: "ontology-formalizer@0.2.0"
consultation_role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define a finite/local source model zoo schema for certificate, obstruction, and target-import test models."
requires_human_gate: false
```

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` [Internal project control plan].

The Aether-Flow Research Project. (2026). `research_control/design/eqsrc_retainh_genh_trigger_list_v16.md` [Internal project-control trigger policy].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260704-020/artifacts/matter_coupling_dag_next_edge_scoring_rubric_v16.md` [Internal route-selection artifact].
