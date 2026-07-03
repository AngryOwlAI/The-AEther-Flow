<!-- authority: control -->

# P7-T03 Refuter Role/Template Update Receipt

## Scope

This receipt records the v15 P7-T03 project-control update. The packet updates
the active Refuter role contract and the generic completion template so future
Refuter packets that report an obstruction, countermodel, certificate gap,
local freeze, blocked overread, or repeated burden must produce a precise
`refuter_obstruction_record`.

## Updated Surfaces

- `.agents/roles/physics/refuter.v0.2.0.md` now requires future Refuter
  obstruction records to name the actual `failed_premise`, align with
  `research_control/design/refuter_obstruction_schema_v1.md`, and preserve
  protected global no-go and future-source-extension-impossibility flags unless
  a separate theorem and human-gated authority explicitly authorize them.
- `research_control/templates/COMPLETION_TEMPLATE.yaml` now includes a
  `refuter_obstruction_record` block with the P7-T01 schema fields, fixture
  catalog path, protected conclusion defaults, and explicit
  `vague_failure_language_sufficient_for_pass: false`.
- `research_control/tasks/RT-20260703-011/artifacts/validate_p7_t03_refuter_role_template_update.py`
  validates that both surfaces contain the required P7-T03 contract text.

## PASS Rule

Future Refuter packets cannot pass by saying only that a proof "needs more
work", "future work remains", "generalization was not attempted", or
"insufficient time". A PASS must state a concrete failed premise such as a
missing primitive, invalid certificate, unsupported transition, target import,
nonunique construction, malformed proof step, or declared finite/local
countermodel.

## Claim Boundary

This is project-control guidance only. It is not proof authority, not a live
Refuter result, not source-law adoption, not source-extension data adoption,
not matter-semantics adoption, not detector-semantics adoption, not coupling-law
adoption, not matter-coupling derivation or adoption, not `MetricData(E)`
adoption, not `g_eff` scope expansion, not stress-energy semantics, not a matter
action, not Einstein-equation evidence, not benchmark promotion, not a Gate
Chair verdict, not completed derivation, not a program-wide no-go conclusion,
and not future source-extension impossibility.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 3). *Refuter obstruction schema
v1* [Internal project-control schema].
`research_control/design/refuter_obstruction_schema_v1.md`

The AEther-Flow Research Project. (2026, July 3). *Refuter countermodel fixture
catalog v1* [Internal project-control catalog].
`research_control/design/refuter_countermodel_fixture_catalog_v1.md`
