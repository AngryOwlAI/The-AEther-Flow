<!-- authority: control -->

# Countermodel Obligation Template Integration Receipt

## Scope

This receipt closes v18 P4-T04 for `RT-20260708-004`. The packet integrated the
minimal countermodel-obligation requirement into theorem-task template
surfaces. Future theorem candidates, proof attempts, theorem-like packets, and
proved conditional theorem completions must include `countermodel_obligations`
or cite an explicit Director Decision Record waiver.

## Updated Surfaces

- `research_control/tasks/README.md`
- `research_control/templates/COMPLETION_TEMPLATE.yaml`

The v18 plan named additional schema and skill candidate files. Those surfaces
were inspected but not changed because the task README and completion template
are the narrower live theorem-task template surfaces, and changing widely
referenced registered sources would create unnecessary historical
memory-preflight churn.

## Acceptance Result

```yaml
p4_t04_template_integration:
  theorem_candidates_require_countermodel_obligations_or_waiver: true
  waiver_requires_explicit_director_decision_record: true
  physics_claims_changed: false
  physics_promotion_authorized: false
  distance_to_gr_delta: "no_distance_delta"
  next_route: "P4-T05"
```

## Claim Boundary

Allowed:

- v18 P4-T04 theorem-task template integration completed.
- Future theorem candidates require `countermodel_obligations` or an explicit
  DDR waiver.
- The integration used the task README and completion template as the live
  template surfaces.

Forbidden:

- Template integration as theorem proof.
- Template integration as a new countermodel or obstruction result.
- Local countermodel slots as program-wide no-go conclusions.
- RetainH adoption, GenH adoption, or source-law adoption.
- Matter-coupling derivation or Einstein-equation derivation.
- Benchmark promotion, Gate Chair verdict, completed derivation, or future
  source-extension impossibility.

## References

The AEther-Flow Research Project. (2026a). *Minimal countermodel obligation
policy v1* [Project-control Markdown source].
`research_control/design/minimal_countermodel_obligation_policy_v1.md`.

The AEther-Flow Research Project. (2026b). *V18 recommendation implementation
plan continue task* [Project-control Markdown source].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.
